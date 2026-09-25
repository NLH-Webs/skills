"""Đổi cặp cụm chữ đầu/cuối thành mốc cắt chính xác (giây nguồn), chừa 0,3s hai đầu nhưng không lấn sang từ bên cạnh.

    python moc.py transcript.json "cụm đầu|cụm cuối|từ giây|đến giây" ["...|...|a|b" ...]

In ra dạng dán thẳng vào kế hoạch: dict(s=..., e=...)  # câu đầy đủ
"KHÔNG THẤY" nghĩa là cụm không khớp nguyên văn với transcript (máy nghe khác, hoặc có dấu câu/từ đệm chen giữa):
thử cụm ngắn hơn, hoặc in lại đoạn bằng in_tu.py để chép đúng chữ máy nghe.
"""
import sys

from chung import doc_tu, tim_cum

if len(sys.argv) < 3:
    sys.exit(__doc__)
W = doc_tu(sys.argv[1])
for arg in sys.argv[2:]:
    c0, c1, a, b = arg.split("|")
    a, b = float(a), float(b)
    r0 = tim_cum(W, c0, a, b)
    if not r0:
        print("KHÔNG THẤY", c0)
        continue
    k0 = r0[0]
    r1 = tim_cum(W, c1, W[k0]["s"], b, cuoi=True)
    if not r1:
        print("KHÔNG THẤY", c1)
        continue
    k1 = r1[0] + r1[1] - 1
    s = max(W[k0]["s"] - 0.3, (W[k0 - 1]["e"] + 0.05) if k0 else 0)
    e = min(W[k1]["e"] + 0.3, W[k1 + 1]["s"] - 0.05) if k1 + 1 < len(W) else W[k1]["e"] + 0.3
    cau = " ".join(W[i]["w"] for i in range(k0, k1 + 1))
    print(f"dict(s={s:.2f}, e={e:.2f})  # {cau[:110]}")
