# File kế hoạch dựng (một file cho một video)

Kế hoạch là **dữ liệu**, động cơ dựng là **code dùng chung**. Tách như vậy để: dựng video mới = viết file mới; sửa một chữ = sửa kế hoạch rồi dựng lại riêng lớp chữ.
Khoá dùng cụm chữ **như máy nghe** (chữ thường, chưa sửa) để neo — động cơ tìm cụm trên các từ đã lọc sạn.

Ví dụ (nội dung minh hoạ, số giây minh hoạ):
```python
# video07.py — "Hỏi đáp tập 2" · nguồn B 60:04–97:10
NGUON = "B"                       # nguồn nào (transcript, bố cục, phụ đề đối chiếu, file video)
CANH_GOC = True                   # xen cảnh "khung gốc" (slide + ô người nói, cả khung) trong đoạn bố cục slide
BANG_TRANG = [(4431.0, 5184.5)]   # giây nguồn có bảng trắng/màn hình demo: xen khung phóng to vùng màn hình (G2)
BO_CUC_SUA = [(6703.5, 6790.5, "S")]              # sửa tay bố cục khi bộ dò ghi sai / "?"
G2_CAT = {"S": (532, 312, 1388, 550)}             # vùng màn hình cần phóng to, theo từng loại bố cục (x, y, w, h)
CHE = [(3993.5, 4012.0, 500, 540, 1000, 230)]     # làm mờ: giây nguồn đầu, cuối, x, y, w, h

DOAN = [                                          # theo thứ tự phát: móc trước, thân sau
    dict(s=3842.27, e=3850.59, vai="moc"),        # câu móc 1
    dict(s=4079.39, e=4084.37, vai="moc"),        # câu móc 2
    dict(s=3604.07, e=3629.59, vai="than"),
    ...
]
QUYET = [(3629.6, 3689.6, "Bỏ đoạn chờ câu hỏi (phụ thuộc chat)"), ...]
CHOT = "cụm đầu câu chốt"                         # giữ lặng trước câu này
MO = dict(nhan="Tên chương trình · Tập 2", y="Bạn hỏi, tôi [[trả lời]]", nen="HỎI ĐÁP")   # thẻ tiêu đề

BANG_TU_THEM = [("sao háo", "self-help"), ("đốp bơm min", "dopamine"), ("dô", "vô"), ...]   # sửa chữ hiển thị (cụm → cụm)
GIU_HOA = {"TikTok", "YouTube", ...}              # từ giữ viết hoa khi lớp hiển thị hạ chữ thường

CHUONG = [(None, "01", "Tốt hơn hay [[đi tìm]] tốt hơn", "Tốt hơn hay đi tìm tốt hơn"),   # (cụm neo | None = đầu thân bài,
          ("cụm mở chương hai", "02", "Học đi đôi với [[làm]]", "Học đi đôi với làm")]     #  số, tiêu đề có nhấn, chữ chip)
THE = [("cụm neo thẻ", dict(loai="the", nen="giay", tren="Dòng trên", y="dòng [[nhấn]]", duoi="dòng dưới"), 2.4)]
      # thẻ chữ toàn khung: (cụm neo, nội dung, giây). nen: giay (sáng) | muc (tối). so=8 để hiệu ứng đếm số
BANG = [("cụm bắt đầu bảng", "cụm kết thúc", "L",                        # bảng liệt kê: (cụm bắt đầu, cụm/giây kết thúc, bên, mục)
         dict(ds=[("chạy bộ", "Chạy bộ"), ("ăn chay", "Ăn chay"), ("đọc sách", "[[Đọc sách]]")]))]
HINH = [("cụm neo", "v07-xecu", "B", ""),                                 # b-roll: (cụm neo, file, kiểu, nhãn)
        ("cụm neo khác", "v07-giaovien", "W", "Trở thành [[giáo viên giỏi]]")]
KW = ["hệ thống", "cảm xúc", ...]                                         # từ khoá tô màu trong phụ đề (short ≤10)
```

## Ghi chú từng khoá
- `[[...]]` = phần nhấn (màu nhấn). Mỗi tiêu đề/thẻ nhấn **một** cụm.
- **THE (thẻ chữ toàn khung)**: là lời người nói rút gọn — không bịa ý. Không đặt thẻ ngay sau chương có cùng ý (trùng).
- **BANG (bảng liệt kê)**: mục hiện dần khi người nói nhắc tới (neo từng mục bằng cụm máy nghe). Bảng dùng khung người nói nhỏ một bên → **không đặt trong đoạn chỉ có ô người nói tí hon** (bố cục D).
- **HINH kiểu**: `B` toàn khung (≈3s) · `W` cửa sổ + ô tròn người nói · `S2` chia đôi (người nói + hình) · `O` người nói một bên + bảng.
  `W/S2/O` cần mặt người nói đủ to trong nguồn → chỉ dùng ở đoạn mặt toàn khung hoặc ô người nói lớn.
- **Tiền tố b-roll theo video** (`v07-…`) để sổ và thư mục không đụng nhau giữa các video.
- **BANG_TU_THEM** áp theo thứ tự, cụm dài trước cụm ngắn (vd. "người việt nam" trước "người việt"; tên thương hiệu có chữ "tim" (team) trước luật lẻ "tim"→"team"). Chỉ thay một từ đơn khi chắc trong video đó từ ấy không mang nghĩa khác ("thả tim" ≠ "team").
- **Chạy thử khô** in lịch khối: mọi mốc phải tìm thấy; hai khối không đè; thẻ không sát chương; b-roll không rơi vào đoạn màn hình là bằng chứng.
