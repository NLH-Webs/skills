# Tự kiểm và bàn giao

## 1. Kiểm máy (ghi ra file `…-tu-kiem.json` cạnh video)
| Mục | Đạt |
|---|---|
| File | Đúng khung (1920×1080 / 1080×1920), 30 fps, độ dài khớp kế hoạch |
| Nhịp | Không cảnh nào > 3,0s (short theo khuôn hook: ≤ 3,9s); đếm số lần đổi hình |
| Chữ | 0 ô chữ ngoài 80% giữa, 0 đáy chữ dưới 79% chiều cao, 0 thẻ vi phạm, **0 chữ đè mặt** |
| Khung đen | 0 khung đen ngoài chủ ý (thẻ tối không tính) |
| NFC | Mọi chuỗi chữ đã chuẩn NFC |
| Sổ | Mọi b-roll/nhạc/tiếng động có dòng sổ |
| Tiếng | −12,7 ± 0,1 LUFS, đỉnh ≤ −1,0 dBTP (±0,2) — **đo trên file giao** |
| File tạm | Không còn `.tmp.*` cạnh file giao; giờ ghi file giao mới hơn lần dựng cuối |

## 2. Kiểm mắt (không bỏ qua)
- Lưới 20s toàn video (`scripts/luoi_khung.py`): khung đen, chữ đè mặt, b-roll lạc đề, khung phóng to vào chỗ trống, thẻ bình luận/tên người xem lộ to.
- Lưới 0,5–2s quanh: mọi vùng làm mờ, chuyển chương, đoạn chia sẻ màn hình, thẻ chữ.
  Lưới lấy bằng filter `fps` cho mốc lệch và có thể bắt khung lỡ khi file đang ghi — dùng seek từng mốc.
- Quét phụ đề hiển thị: tên riêng viết thường, "ai" có phải AI, từ phương ngữ đã thống nhất chưa, chữ nghe sai còn sót.
- Bìa: chữ không đè mặt, chữ là lời thật, nhãn chương trình/tập đúng.

## 3. Bìa ngang
Người tách nền (rembg) dán sát phải, chữ lớn bên trái (2 dòng + 1 khối màu nhấn). Người càng khép tay càng to, càng lấn chữ → chọn khung bằng `scripts/mat_tren_bia.py` (mép trái mặt > mép phải khối chữ + 40px). Chữ ngắn hơn trước khi chọn khung khác. Xem ảnh bìa bằng mắt.

## 4. Bàn giao
Mỗi video: `…-16x9.mp4` (hoặc `-9x16`), `…-bia.png`, `…-16x9.srt`, `…-chuong.txt` (bản dài; dòng đầu "0:00 Mở đầu"), `…-tu-kiem.json`.

Báo cáo ngắn, theo thứ tự:
1. Kết quả + đường dẫn từng file (bảng: video · nguồn · dài · số chương).
2. Kết quả tự kiểm (một dòng mỗi video, số thật).
3. **Cần quyết** (riêng tư, nhạy cảm, đoạn tự bỏ).
4. Chữ sửa theo nghĩa chưa duyệt (vài ví dụ + nơi có danh sách đủ).
5. Chưa kiểm gì (vd. chưa nghe bằng tai, chưa thử trong phần mềm dựng khác).
Không tự đăng, không tự gửi, không đẩy lên kho chung khi chưa được bảo.
