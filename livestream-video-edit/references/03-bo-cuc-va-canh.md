# Bố cục nguồn và kiểu cảnh

## 1. Phân loại bố cục nguồn (theo thời gian)
Livestream đổi bố cục liên tục. Dò tự động (so khung 2 fps với mẫu từng loại), rồi **xem khung đại diện bằng mắt** — bộ dò hay nhầm.

| Mã | Nguồn trông thế nào | Cắt ra sao |
|---|---|---|
| F | Mặt người nói toàn khung | Cắt quanh mặt (F thường, Z phóng gần) |
| S | Slide/màn hình lớn + ô người nói nhỏ ở một góc (vd. ô 0,321,532,502) | Ô người nói phóng vào giữa (C) xen khung gốc (G) |
| L | Người nói ô lớn + hộp slide đè một bên | Như S nhưng cắt trong vùng không có hộp slide (vd. x < 1030) |
| D | Màn hình/bảng trắng + ô người nói **tí hon**, hoặc màn đen | Không cắt mặt (sẽ vỡ hạt); chỉ xen G và G2 |
| ? | Bộ dò không chắc | Xem bằng mắt rồi khai `BO_CUC_SUA` |

Toạ độ ô người nói **khác nhau giữa các buổi** và **đổi ngay trong một buổi** (ô nhỏ nhảy góc khi chia sẻ màn hình). Đo lại cho từng nguồn.

## 2. Kiểu cảnh
| Kiểu | Là gì | Khi nào |
|---|---|---|
| F / Z | Khung 16:9 cắt quanh mặt; Z phóng gần hơn (1,26×), đỉnh đầu ~33% | Xen kẽ F/Z mỗi nhát để đổi hình khi nói liền |
| C | Người nói (cắt từ ô) đặt giữa khung trên nền tối | Đoạn S/L |
| G | Khung gốc trọn bề ngang (bỏ dải logo trên) trong một cửa sổ phía trên, phụ đề dưới cửa sổ | Mỗi 3 cảnh S/L một lần, để thấy slide |
| G2 | **Vùng màn hình phóng to** (bản vẽ, trang demo) trong cửa sổ cao ~620px, đáy trên dải phụ đề | Đoạn bảng trắng/demo: xoay C → G2 → C → G (S) hoặc G2 → G (D) |
| O, W, S2 | Người nói + bảng / cửa sổ b-roll + ô tròn / chia đôi | Theo khối trong kế hoạch |
| B | B-roll toàn khung | Khối b-roll |
| T | Thẻ chữ toàn khung | Khối thẻ |

## 3. Luật cắt
- **Lịch cắt**: mốc khối (thẻ, b-roll, bảng) + ranh giới đoạn + ranh giới bố cục; lấp để không nhát nào > 3s, ưu tiên cắt ở khe giữa từ (gần 2,6s).
- **Không vượt logo nguồn** (vd. logo ở x ≥ 1720 → khung cắt không qua x 1712).
- **Mặt**: dò Haar cascade 5 lần/giây trên a-roll; mỗi cảnh lấy trung vị vị trí mặt trong cảnh, cỡ mặt lấy trung vị cả loại bố cục (ổn định, không giật).
- **Vùng mặt trên khung ra** (để tránh chữ): từ tâm mặt và cỡ mặt, chừa tóc (≈ tâm − 0,78·cỡ) và cằm (≈ tâm + 0,52·cỡ).
- **Chip chương** ẩn khi đầu người nói chạm góc trên trái.
- **Bong bóng lời** không kéo sang cảnh sau khác kiểu (từng đè mặt).
- Hiệu ứng vào cửa sổ: trượt ngắn từ dưới (≈0,34s), không mờ dần từ 0.

## 4. Đoạn bảng trắng / chia sẻ màn hình
- Người xem cần **thấy thứ đang được vẽ/chỉ** → dùng G2 nhiều (≈ 1/2 số cảnh), G để thấy cả người nói + câu hỏi đang ghim.
- Vùng G2: bỏ thanh công cụ, logo, thẻ bình luận; một vùng cho mỗi loại bố cục (`G2_CAT`).
- **Không đặt W/S2/O trong đoạn D** (cắt mặt từ ô tí hon → vỡ hạt, hoặc cắt nhầm vào màn hình). Chỉ B.
- Thẻ bình luận của người xem hiện trên nguồn: chấp nhận khi nó là câu hỏi đang được trả lời (ngữ cảnh), nhưng không phóng to tên tài khoản.
