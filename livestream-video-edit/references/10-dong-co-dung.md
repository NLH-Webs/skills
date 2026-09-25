# Động cơ dựng — kiến trúc để tự viết hoặc sửa

Skill không kèm động cơ đầy đủ (gắn với thương hiệu, font, mẫu đồ hoạ của từng kênh). Đây là kiến trúc đã chạy ổn cho short dọc và bản dài ngang, đủ để dựng lại.

## Các bước của một lượt dựng
```
kế hoạch + giu.json (khoảng giữ theo giây nguồn)
 1. a-roll      : ffmpeg trim từng khoảng giữ (gom các khoảng gần nhau thành nhóm đọc chung một input) + khe tiêu đề đen
                  → aroll.mp4 (CRF 12, GOP 30, PCM). Làm mờ riêng tư (CHE) ngay ở đây: split → crop → boxblur → overlay enable=between(t)
 2. ánh xạ giờ  : out2src(t) / src2out(s) giữa giờ video ra và giây nguồn
 3. khối        : neo THE/BANG/HINH/CHUONG bằng cụm chữ trên các từ ĐÃ lọc → khoảng giờ ra; báo mốc không thấy
 4. lịch cắt    : mốc khối + ranh giới đoạn + ranh giới bố cục; lấp ≤ 3s ưu tiên khe giữa từ; bỏ nhát < 0,8s trừ mốc bắt buộc
 5. cảnh        : mỗi nhát → kiểu (TITLE/END/T/O/B/W/S2 theo khối; C/G/G2 theo bố cục S/L/D + BANG_TRANG; F/Z xen kẽ)
 5b. dò mặt     : đọc tuần tự aroll, 5 lần/giây, Haar cascade trong vùng ô người nói; trung vị theo cảnh
 6. hình học    : mỗi cảnh → (vùng cắt nguồn → ô đích, bo góc); vùng mặt trên khung ra (để tránh chữ)
 8. dựng cảnh   : ffmpeg song song (6 luồng) mỗi cảnh một file; nền + mặt nạ bo góc + bóng đổ + ô người nói/b-roll;
                  zoompan "trôi" 3,5% để hình không đứng; tpad clone; KIỂM SỐ KHUNG từng cảnh = round(dài × 30)
                  → concat -c copy → nen.mp4
 9. phụ đề      : từ đã lọc (bỏ trong thẻ) → khối ≤ 7 từ, tách theo cảnh; đặt dưới mặt hoặc cạnh mặt; tô từ khoá
10. chuyển động : sự kiện (thẻ tiêu đề, quét, chớp, nhãn, chip chương, bảng, phụ đề) → HTML + GSAP, trình duyệt headless
                  (Playwright, 4 trình duyệt song song, đoạn ≤ 450 khung), chụp PNG trong suốt → một dải PNG-in-MOV liền
11. ghép        : nen.mp4 + dải chuyển động (overlay một lần) + tiếng thô → video; ghi -chuong.txt, sổ phụ đề
12. tiếng       : tiếng động theo sự kiện + scripts/tieng.py
```

## Công tắc nên có
- `THU=1` — chạy thử khô: in lịch khối, dừng trước bước dựng cảnh.
- `GIU_CANH=1` — giữ các cảnh đã dựng, chỉ dựng lại lớp chữ/chuyển động + ghép + tiếng (sửa chữ nhanh).
- Chọn video bằng biến môi trường (`VIDEO=7`) → nạp `long_kh/long7.py`; chọn thương hiệu bằng hash trên mẫu HTML (`motion.html#thuonghieu`).

## Mẫu đồ hoạ (HTML)
- Biến màu theo vai trò trên `body.<thuong-hieu>`: màu nhấn, màu nhấn đậm, chữ trên màu nhấn, nền giấy, nền mực.
- Hai nền thẻ: **giấy** (sáng, chữ mực) và **mực** (tối, chữ trắng) — xen kẽ để đổi nhịp.
- Thẻ tiêu đề: nhãn chương trình · tiêu đề (1 cụm nhấn) · chữ nền lớn mờ.
- Thẻ kết: logo, tên, dòng chữ do người nhờ cung cấp, ảnh trang sản phẩm cuộn nhẹ nếu có.
- Mọi animation theo một timeline dừng (seek được) để chụp từng khung xác định.

## Kích thước tham chiếu (ngang 1920×1080)
Phụ đề: đáy ≤ 853 (79%), dải từ 680; X 192–1728 (80%). Cửa sổ khung gốc G: (384, 40, 1152, 525). G2: cao 620 từ y 40, rộng theo tỉ lệ vùng cắt, giữa khung. Người nói giữa C: (400, 70, 1120, 940). Ô tròn người nói W: (1452, 136, 300, 300).

## Tốc độ tham khảo (GPU tầm trung, 6 luồng ffmpeg)
Bản dài 15 phút: dựng cảnh + chuyển động + tiếng ≈ 25–35 phút. Short 60s: ≈ 3–5 phút. Chạy tối đa 2 bản dài song song.
