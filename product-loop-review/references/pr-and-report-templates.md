# Khuôn commit, PR và câu trả lời cuối

## Commit
Một commit một chủ đề. Dòng đầu theo quy ước repo (`fix(ui): …`, `feat(ui): …`). Thân kể **vấn đề đo được → cách sửa**, không kể quá trình:
```
fix(ui): <màn> — <3–5 chữ về thứ đã sửa>

<Vấn đề 1, kèm con số/dòng code>. <Cách sửa>.
<Vấn đề 2>. <Cách sửa>.

<Hàng rào đã hạ mốc: tên chỉ số cũ -> mới>.
```
Trên Windows: viết thân vào file rồi `git commit -F <file>` (xem tooling-pitfalls).

## Chia PR
- Giữ dưới giới hạn file của repo. Vượt → tách theo chủ đề: (1) bảng/thẻ/dark/mobile layout, (2) form, (3) tab phụ + mobile pass.
- PR sau phụ thuộc PR trước → base là nhánh PR trước, dòng đầu thân ghi "Chồng lên #N — duyệt #N trước". Nếu PR trước đã merge và nhánh bị xoá, mở lại với base là nhánh tích hợp.
- Không đẩy nhánh chính, không tự merge.

## Thân PR
```markdown
## Summary
<1–2 câu: đi qua sản phẩm thế nào (ở máy, dữ liệu thử, vai gì), sửa phạm vi nào. Backend có đổi không.>

### Đã sửa
| Nhìn từ vai | Vấn đề (đo được) | Sửa |
| --- | --- | --- |
| PM / CS | <vd: phần lớn đơn đang chờ nằm trong Lưu trữ vì luật lọc chỉ xét tuổi (file:dòng)> | <cách sửa> |
| QA | … | … |

### Tìm thấy, chưa sửa (cần quyết định hoặc repo khác)
- **<Vai>:** <vấn đề> — <cần ai/ở đâu>.

## Test plan
- [x] lệnh verify của repo xanh
- [x] <phép đo lại, từng khung: hẹp / desktop / 375px / dark>
- [ ] Người duyệt: <việc chỉ người thật làm được — gửi thử một đơn thật trên staging, xem trên iPhone thật trong app mẹ>

<dòng ghi công theo quy ước>
```

## Câu trả lời cuối cho người nhờ
Ngắn, kết quả trước, không kể quá trình:
1. **Một câu:** đã đi qua gì, sửa ở đâu — link PR.
2. **Bảng theo vai** (Vai · Tìm thấy · Trạng thái) — gộp dòng nhỏ, giữ dòng có con số.
3. **Điều người nhờ nên biết:** thay đổi hành vi họ chưa yêu cầu (vd ẩn một mục menu), việc không làm được (vd không gửi đơn thật), file ở máy bị thay (vd `.env`).
4. **Việc của họ:** duyệt PR nào trước, kiểm gì trên máy thật.

Tiêu đề in đậm cho mỗi ý mới; không mở đầu bằng "Tuyệt vời/Đã xong!".
