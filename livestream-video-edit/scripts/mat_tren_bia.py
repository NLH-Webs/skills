"""Chọn khung người nói cho bìa ngang TRƯỚC khi dựng bìa: tính mép trái mặt sẽ nằm ở đâu trên bìa.

Kiểu bìa: người đã tách nền (rembg), cao H px, dán sát phải (cách mép phải P px) trên canvas rộng C px;
chữ lớn nằm bên trái. Người càng khép tay (vùng cắt hẹp) thì càng to và càng lấn sang chữ.

    python mat_tren_bia.py nguon.mp4 4780 4855 5095 ... [--cao 690] [--canvas 1280] [--phai 30] [--chu-toi 640]

In mép trái mặt trên bìa cho từng giây; "ĐẠT" khi mép trái mặt > chu-toi + 40 (chữ không chạm mặt).
Cần: pip install rembg opencv-python pillow. Mặt dò bằng Haar cascade (mặt nhìn thẳng).
"""
import argparse

import cv2
from PIL import Image
from rembg import remove

import chung  # noqa: F401  (in chữ Việt ra console Windows)

ap = argparse.ArgumentParser()
ap.add_argument("video"); ap.add_argument("giay", nargs="+", type=float)
ap.add_argument("--cao", type=int, default=690); ap.add_argument("--canvas", type=int, default=1280)
ap.add_argument("--phai", type=int, default=30); ap.add_argument("--chu-toi", type=int, default=640)
g = ap.parse_args()
casc = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
cap = cv2.VideoCapture(g.video)
for t in g.giay:
    cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000)
    ok, f = cap.read()
    if not ok:
        print(t, "không đọc được khung"); continue
    fs = casc.detectMultiScale(cv2.cvtColor(f, cv2.COLOR_BGR2GRAY), 1.1, 6, minSize=(120, 120))
    if not len(fs):
        print(t, "không thấy mặt"); continue
    x, y, w, h = max(fs, key=lambda q: q[2] * q[3])
    cut = remove(Image.fromarray(cv2.cvtColor(f, cv2.COLOR_BGR2RGB)))
    bb = cut.getchannel("A").point(lambda a: 255 if a > 40 else 0).getbbox()
    sc = g.cao / (bb[3] - bb[1])
    trai = g.canvas - g.phai - (bb[2] - x) * sc
    print(f"{t:8.1f}  mép trái mặt {trai:6.0f}  đỉnh đầu {(y - bb[1]) * sc:5.0f}  {'ĐẠT' if trai > g.chu_toi + 40 else 'lấn chữ'}")
