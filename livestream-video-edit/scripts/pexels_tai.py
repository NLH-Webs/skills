"""Tải b-roll đã duyệt từ lưới, chuẩn hoá (30 fps, đúng khung, cắt ≤16s, bỏ tiếng) và GHI SỔ nguồn gốc.

    export PEXELS_API_KEY=...
    python pexels_tai.py '{"l7-bongden": 0, "l7-song": 2}' "tên dự án/video" --so manifest.csv [--ra b-roll/] [--doc] [--tim tim/]

Sổ (manifest.csv) mỗi dòng: file, nguồn, tác giả, giấy phép, link gốc, ngày tải, dùng ở đâu.
Không ghi sổ = không được dùng hình đó. Giấy phép Pexels cho dùng thương mại, không bắt buộc ghi công — vẫn ghi để tra lại.
"""
import argparse
import csv
import datetime
import json
import os
import tempfile
from concurrent.futures import ThreadPoolExecutor

import requests

from chung import FF, chay

ap = argparse.ArgumentParser()
ap.add_argument("chon"); ap.add_argument("nhan"); ap.add_argument("--so", required=True)
ap.add_argument("--ra", default="b-roll"); ap.add_argument("--doc", action="store_true"); ap.add_argument("--tim", default="tim")
g = ap.parse_args()
R = json.load(open(os.path.join(g.tim, "ung-vien.json"), encoding="utf-8"))
CHON = json.loads(g.chon)
os.makedirs(g.ra, exist_ok=True)
W_, H_ = (1080, 1920) if g.doc else (1920, 1080)
hom_nay = datetime.date.today().isoformat()


def tai(item):
    key, i = item
    c = R[key]["cands"][i]
    ten = f"{key}-pexels-{c['id']}.mp4"; out = os.path.join(g.ra, ten)
    if not os.path.exists(out):
        tmp = os.path.join(tempfile.gettempdir(), ten)
        with requests.get(c["file"], stream=True, timeout=300) as r:
            r.raise_for_status()
            with open(tmp, "wb") as f:
                for ch in r.iter_content(1 << 20): f.write(ch)
        chay([FF, "-v", "error", "-y", "-i", tmp, "-t", "16", "-an", "-vf",
              f"fps=30,scale={W_}:{H_}:force_original_aspect_ratio=increase:flags=lanczos,crop={W_}:{H_},setsar=1",
              "-c:v", "libx264", "-preset", "fast", "-crf", "17", "-pix_fmt", "yuv420p", out])
        os.remove(tmp)
    return [ten, "Pexels", c["tac_gia"], "Pexels License (dùng thương mại, không bắt buộc ghi công)", c["url"], hom_nay, g.nhan]


with ThreadPoolExecutor(5) as ex:
    dong = list(ex.map(tai, CHON.items()))
co = set()
if os.path.exists(g.so):
    co = {r[0] for r in csv.reader(open(g.so, encoding="utf-8-sig"))}
moi = [d for d in dong if d[0] not in co]
with open(g.so, "a", newline="", encoding="utf-8-sig") as f:
    csv.writer(f).writerows(moi)
print(f"{len(dong)} file, {len(moi)} dòng sổ mới")
