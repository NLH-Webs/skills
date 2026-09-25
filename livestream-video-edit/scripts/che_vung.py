"""Làm mờ các vùng có thông tin riêng tư theo thời gian (boxblur), giữ nguyên tiếng.

    python che_vung.py vao.mp4 ra.mp4 "3993.5,4012,500,540,1000,230" "4085,4104,500,540,1000,230" [--manh 24]

Mỗi vùng: giây đầu, giây cuối, x, y, rộng, cao — theo toạ độ và thời gian CỦA FILE VÀO.
Nên che ở file nguồn (trước khi cắt ghép) hoặc ngay lúc dựng đoạn thô: mọi cảnh cắt/phóng to sau đó đều
kế thừa vùng mờ, không sót ở cảnh phóng to. Che ở video cuối chỉ đúng khi toạ độ không đổi theo cảnh.
Sau khi che: mở lưới 0,5s quanh từng vùng (luoi_khung.py) và đọc thử — chữ không được đọc ra.
"""
import argparse

from chung import FF, chay

ap = argparse.ArgumentParser()
ap.add_argument("vao"); ap.add_argument("ra"); ap.add_argument("vung", nargs="+"); ap.add_argument("--manh", type=int, default=24)
g = ap.parse_args()
fc, lab = [], "0:v"
for i, v in enumerate(g.vung):
    t0, t1, x, y, w, h = [float(q) for q in v.split(",")]
    x, y, w, h = int(x), int(y), int(w), int(h)
    ra = "v" if i == len(g.vung) - 1 else f"r{i}"
    fc.append(f"[{lab}]split[m{i}][c{i}];[c{i}]crop={w}:{h}:{x}:{y},boxblur={g.manh}:3[b{i}];"
              f"[m{i}][b{i}]overlay={x}:{y}:enable='between(t,{t0:.3f},{t1:.3f})'[{ra}]")
    lab = ra
chay([FF, "-v", "error", "-y", "-i", g.vao, "-filter_complex", ";".join(fc), "-map", "[v]", "-map", "0:a?",
      "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-pix_fmt", "yuv420p", "-c:a", "copy", g.ra])
print(g.ra)
