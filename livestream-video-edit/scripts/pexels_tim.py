"""Tìm hình phụ (b-roll) trên Pexels bằng API chính thức, chụp lưới ảnh đại diện để DUYỆT BẰNG MẮT trước khi tải.

    export PEXELS_API_KEY=...            (không bao giờ ghi khoá vào file trong repo, không in ra màn hình)
    python pexels_tim.py truy-van.json tien-to [--doc] [--ra tim/]

truy-van.json: {"tien-to-ten": "từ khoá tiếng Anh", ...}   vd {"l7-bongden": "light bulb glowing dark"}
--doc: tìm khổ dọc (short 9:16); mặc định khổ ngang ≥1920.
Ra: tim/ung-vien.json (mọi ứng viên, gộp với lần trước) và tim/<tien-to>-luoi-N.jpg (mỗi dòng một khoá, 5 ứng viên đánh số 0–4).
Chọn số trên lưới rồi tải bằng pexels_tai.py. Lưới dễ lừa: xem kỹ ô tối/đen, chữ in trên hình, logo, mặt người nhìn thẳng máy.
"""
import argparse
import io
import json
import os
from concurrent.futures import ThreadPoolExecutor

import requests
from PIL import Image, ImageDraw, ImageFont

ap = argparse.ArgumentParser()
ap.add_argument("truy_van"); ap.add_argument("tien_to"); ap.add_argument("--doc", action="store_true"); ap.add_argument("--ra", default="tim")
g = ap.parse_args()
KEY = os.environ.get("PEXELS_API_KEY")
if not KEY:
    raise SystemExit("thiếu biến môi trường PEXELS_API_KEY")
H = {"Authorization": KEY}
Q = json.load(open(g.truy_van, encoding="utf-8"))
os.makedirs(g.ra, exist_ok=True)
UV = os.path.join(g.ra, "ung-vien.json")
cu = json.load(open(UV, encoding="utf-8")) if os.path.exists(UV) else {}
try:
    font = ImageFont.truetype("arial.ttf", 20)
except OSError:
    font = ImageFont.load_default()


def tim(key):
    r = requests.get("https://api.pexels.com/videos/search", headers=H, timeout=30,
                     params={"query": Q[key], "orientation": "portrait" if g.doc else "landscape", "per_page": 12, "size": "large"})
    r.raise_for_status()
    ds = []
    for v in r.json().get("videos", []):
        can = (lambda f: f["height"] >= 1900) if g.doc else (lambda f: f["width"] >= 1900)
        files = [f for f in v["video_files"] if f.get("width") and f.get("height") and f["file_type"] == "video/mp4" and can(f)]
        if not files or (v["width"] > v["height"]) == g.doc or v["duration"] < 6:
            continue
        f = min(files, key=lambda f: abs((f["height"] if g.doc else f["width"]) - 1920))
        pics = v.get("video_pictures") or []
        ds.append({"id": v["id"], "url": v["url"], "tac_gia": v["user"]["name"], "dai": v["duration"], "file": f["link"],
                   "anh": pics[len(pics) // 2]["picture"] if pics else v.get("image")})
    return key, {"q": Q[key], "cands": ds[:5]}


with ThreadPoolExecutor(6) as ex:
    for key, kq in ex.map(tim, Q):
        cu[key] = kq; print(key, len(kq["cands"]))
json.dump(cu, open(UV, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def anh(u):
    try:
        return Image.open(io.BytesIO(requests.get(u, timeout=30).content)).convert("RGB")
    except Exception:
        return None


keys = list(Q)
tw, th = (180, 320) if g.doc else (320, 180)
for n in range(0, len(keys), 14):
    nhom = keys[n:n + 14]
    img = Image.new("RGB", (200 + 5 * (tw + 8), len(nhom) * (th + 12)), "white"); d = ImageDraw.Draw(img)
    for r_, key in enumerate(nhom):
        y = r_ * (th + 12)
        d.text((6, y + th // 2 - 10), key, fill="black", font=font)
        with ThreadPoolExecutor(5) as ex:
            ims = list(ex.map(anh, [c["anh"] for c in cu[key]["cands"]]))
        for i, im in enumerate(ims):
            if im is None: continue
            im.thumbnail((tw, th)); x = 200 + i * (tw + 8)
            img.paste(im, (x, y)); d.rectangle([x, y, x + 26, y + 24], fill="black"); d.text((x + 7, y + 2), str(i), fill="white", font=font)
    out = os.path.join(g.ra, f"{g.tien_to}-luoi-{n // 14}.jpg"); img.save(out, quality=85); print(out)
