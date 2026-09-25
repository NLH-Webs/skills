"""Lưới khung hình có mốc giờ — để TỰ NHÌN video trước khi báo xong.

    python luoi_khung.py video.mp4 ra.jpg [--moi 20] [--tu 0] [--den 0] [--cot 6] [--rong 384]

--moi: mỗi bao nhiêu giây lấy một khung. Không lấy bằng filter fps (mốc lệch khi file đang ghi/không đều khung):
script seek chính xác từng mốc rồi ghép, nên nhãn giờ trên mỗi ô là giờ thật.
Mẹo: lưới 20s để soát tổng thể; lưới 0,5–2s quanh chỗ nghi ngờ (khung đen, chữ đè mặt, thông tin riêng tư).
"""
import argparse
import os
import tempfile

from PIL import Image, ImageDraw, ImageFont

from chung import FF, chay, dai

ap = argparse.ArgumentParser()
ap.add_argument("video"); ap.add_argument("ra")
ap.add_argument("--moi", type=float, default=20); ap.add_argument("--tu", type=float, default=0); ap.add_argument("--den", type=float, default=0)
ap.add_argument("--cot", type=int, default=6); ap.add_argument("--rong", type=int, default=384)
g = ap.parse_args()
den = g.den or dai(g.video) - 0.05
tmp = tempfile.mkdtemp(prefix="luoi-")
try:
    font = ImageFont.truetype("arial.ttf", 18)
except OSError:
    font = ImageFont.load_default()
moc, t = [], g.tu
while t <= den:
    moc.append(t); t += g.moi
anh = []
for i, t in enumerate(moc):
    p = os.path.join(tmp, f"{i:04d}.jpg")
    chay([FF, "-v", "error", "-y", "-ss", f"{t:.3f}", "-i", g.video, "-frames:v", "1", "-vf", f"scale={g.rong}:-2", p])
    im = Image.open(p).convert("RGB"); d = ImageDraw.Draw(im)
    nhan = f"{int(t // 3600):02d}:{int(t % 3600 // 60):02d}:{t % 60:06.3f}"
    d.rectangle([0, 0, 150, 24], fill="black"); d.text((4, 3), nhan, fill="yellow", font=font)
    anh.append(im)
w, h = anh[0].size
hang = (len(anh) + g.cot - 1) // g.cot
out = Image.new("RGB", (w * g.cot, h * hang), "black")
for i, im in enumerate(anh):
    out.paste(im, ((i % g.cot) * w, (i // g.cot) * h))
out.save(g.ra, quality=88)
print(g.ra, f"{len(anh)} khung")
