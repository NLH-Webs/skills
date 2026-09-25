"""In transcript một khoảng giây thành dòng dễ đọc, đánh dấu khoảng lặng (‖giây) để chọn chỗ cắt.

    python in_tu.py transcript.json 3590 4030 > doan.txt

Mỗi dòng: giây bắt đầu + tối đa 16 từ; xuống dòng khi lặng > 1s. "‖2.4" = sau từ đó lặng 2,4s.
Đọc file ra này trước khi chọn đoạn — đừng chọn đoạn từ phụ đề tự động của nền tảng (mốc lệch, không có từng từ).
"""
import sys

from chung import doc_tu

if len(sys.argv) < 4:
    sys.exit(__doc__)
W = [w for w in doc_tu(sys.argv[1]) if float(sys.argv[2]) <= w["s"] <= float(sys.argv[3])]
dong, t0 = [], None
for i, w in enumerate(W):
    t0 = w["s"] if t0 is None else t0
    lang = W[i + 1]["s"] - w["e"] if i + 1 < len(W) else 9
    dong.append(w["t"] + (f" ‖{lang:.1f}" if lang > 0.6 else ""))
    if len(dong) >= 16 or lang > 1.0:
        print(f"{t0:7.1f} {' '.join(dong)}")
        dong, t0 = [], None
if dong:
    print(f"{t0:7.1f} {' '.join(dong)}")
