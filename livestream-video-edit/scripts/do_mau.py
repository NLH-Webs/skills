"""Dò những giây một "dấu hiệu màu" xuất hiện trên màn hình nguồn — dùng để tìm MỌI lần một trang chứa thông tin
riêng tư (hồ sơ, tên + ngày sinh, số điện thoại…) hiện lên, kể cả lúc cuộn trang, để làm mờ cho đủ.

    python do_mau.py nguon.mp4 3970 4360 --mau "190,90,90;255,170,90" [--buoc 0.5] [--nen 0] [--nguong 4000]

--mau: khoảng màu viết theo R,G,B: "Rmin,Gmin,Bmin;Rmax,Gmax,Bmax" (vd. chữ tiêu đề màu cam của trang hồ sơ).
--nen: số điểm ảnh khớp màu khi trang KHÔNG hiện (logo kênh cùng màu cũng khớp) — chạy thử một giây trống để đo.
In ra các cụm giây có số điểm > nen + nguong, kèm đỉnh. Cách dùng:
  1) chụp 1 khung có thông tin riêng tư, chọn một màu đặc trưng của trang đó;
  2) chạy script → danh sách cụm giây; 3) mở từng cụm bằng luoi_khung.py để xem vị trí dòng cần che;
  4) khai vùng che (giây đầu, cuối, x, y, w, h) — che rộng tay, vì trang cuộn làm dòng chữ di chuyển.
Script chỉ là lưới an toàn: trang có thể hiện thông tin mà không có màu đó. Vẫn phải xem bằng mắt.
"""
import argparse

import cv2
import numpy as np

import chung  # noqa: F401  (in chữ Việt ra console Windows)

ap = argparse.ArgumentParser()
ap.add_argument("video"); ap.add_argument("tu", type=float); ap.add_argument("den", type=float)
ap.add_argument("--mau", required=True); ap.add_argument("--buoc", type=float, default=0.5)
ap.add_argument("--nen", type=int, default=0); ap.add_argument("--nguong", type=int, default=4000)
g = ap.parse_args()
lo, hi = [np.array(list(map(int, x.split(",")))[::-1]) for x in g.mau.split(";")]   # R,G,B → B,G,R
cap = cv2.VideoCapture(g.video)
hit = []
for t in np.arange(g.tu, g.den, g.buoc):
    cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000)
    ok, f = cap.read()
    if not ok:
        continue
    n = int(cv2.inRange(f, lo, hi).astype(bool).sum())
    if n > g.nen + g.nguong:
        hit.append((float(t), n))
cum = []
for t, n in hit:
    if cum and t - cum[-1][1] <= g.buoc * 2.5:
        cum[-1][1] = t; cum[-1][2] = max(cum[-1][2], n)
    else:
        cum.append([t, t, n])
for a, b, n in cum:
    print(f"{a:9.1f} – {b:9.1f}s  đỉnh {n} điểm")
print(f"{len(cum)} cụm")
