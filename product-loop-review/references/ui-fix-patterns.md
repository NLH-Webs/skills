# Khuôn sửa giao diện — và cái bẫy của từng khuôn

Mỗi khuôn: **triệu chứng → cách sửa → bẫy**. Ví dụ code theo React + Tailwind; ý tưởng dùng được cho mọi stack.

---

## 1. Việc bị giấu vì luật lọc sai tầng
**Triệu chứng:** đơn đang chờ nằm trong "Lưu trữ" vì luật backend chỉ xét ngày tạo.
**Sửa (giao diện):** lấy toàn bộ (`window=all`) rồi chia ở client:
```ts
const ARCHIVE_AFTER_DAYS = 30;
function isInArchive(o: Order, manual: Set<string>) {
  if (manual.has(String(o.id))) return true;
  return o.status === 'done' && Date.now() - new Date(o.created_at).getTime() > ARCHIVE_AFTER_DAYS * 86_400_000;
}
```
**Bẫy:** tải tất cả chỉ ổn khi số lượng nhỏ (hàng chục–vài trăm). Ghi vào "chưa sửa": backend nên lọc theo trạng thái. Nút "Lưu trữ tay" lưu ở trình duyệt thì phải **đọc lại lúc khởi tạo** và nói rõ nó chỉ theo máy.

## 2. Giờ lệch múi
**Sửa:** mọi chỗ hiển thị giờ nghiệp vụ đi qua một hàm định dạng theo múi giờ nghiệp vụ:
```ts
const parts = (iso: string) => Object.fromEntries(new Intl.DateTimeFormat('en-GB', {
  timeZone: 'Asia/Ho_Chi_Minh', day: '2-digit', month: '2-digit', year: 'numeric',
  hour: '2-digit', minute: '2-digit', hourCycle: 'h23',
}).formatToParts(new Date(iso)).map(p => [p.type, p.value]));
```
**Bẫy:** đừng sửa chỗ lưu (backend đang đúng); đừng quên màn "xem lại trước khi gửi" hay in chuỗi ISO thô.

## 3. Modal vỡ ở khung hẹp
**Sửa:** dưới breakpoint lớn → toàn màn hình, xếp dọc; phần nội dung trên giới hạn `max-h-[45%]` và tự cuộn, phần chat/nút dưới luôn thấy.
```tsx
className="w-screen h-[100dvh] rounded-none lg:w-[68vw] lg:max-w-[1220px] lg:min-w-[760px] lg:h-[86vh] lg:rounded-2xl"
```
**Bẫy:** class mặc định của component dialog (`sm:rounded-lg`, `max-w-lg`) vẫn thắng ở breakpoint giữa — ghi đè đủ các breakpoint.

## 4. Dark mode
**Triệu chứng:** nền tối, chữ tối. Gốc: bản vá toàn cục `.dark .bg-white {…}` chỉ đổi nền; màu chữ viết bằng hex không đổi.
**Sửa:** thay hex bằng **biến vai trò** của hệ thiết kế (vd `bg-surface`, `bg-surface-sunken`, `text-fg`, `text-fg-muted`, `text-fg-subtle`, `border-line`, `bg-fg text-fg-inverse` cho nút chính). Style inline thì dùng `var(--bg-raised)`, `var(--text-primary)`…
Có thể thay hàng loạt bằng bảng ánh xạ (hex → token) chạy trên đúng các file đang sửa, rồi soát lại phần còn sót.
**Bẫy:**
- Chữ trắng *trên nền màu* (nút xanh, avatar) phải giữ trắng — đừng thay mù `#fff`.
- Kiểm light mode sau khi sửa: token phải cho ra đúng màu cũ ở light.
- `color-mix(in srgb, var(--tone) 12%, var(--bg-raised))` cho nền nhạt của một màu — tự đúng ở cả hai chế độ.

## 5. Hệ màu trạng thái (nhìn một giây là biết)
**Sửa:** mỗi giai đoạn một họ màu, dùng ở dải màu trên đầu thẻ, nền đầu thẻ, nhãn, thanh tiến độ; tab lọc có chấm cùng màu → tab chính là chú giải.

| Giai đoạn | Màu | Ghi chú |
|---|---|---|
| Chờ nhận | hổ phách | đang đợi ai đó |
| Đang làm | xanh dương | |
| Chờ duyệt | tím | chờ người đặt |
| Đang sửa / bị chặn | hồng đỏ | cần chú ý |
| Hoàn thành | xanh lá | |
| Lưu trữ | xám, mờ nhẹ | |

Cài bằng một biến CSS mỗi họ màu:
```css
.tone-waiting { --tone: var(--state-warn); } .tone-done { --tone: var(--state-ok); } …
.tone-head { background: color-mix(in srgb, var(--tone) 9%, var(--bg-raised)); }
.tone-pill { background: color-mix(in srgb, var(--tone) 16%, var(--bg-raised)); color: color-mix(in srgb, var(--tone) 72%, var(--text-primary)); }
.tone-fill { background: var(--tone); }
```
**Bẫy:**
- Viền trên thẻ: class `border-[#xxx]` chung sẽ đè `border-top-color` — dùng `border-t-[color:var(--tone)]` trong cùng chuỗi class.
- Biểu đồ và dashboard phải dùng **cùng** màu cho cùng trạng thái.
- Màu kèm chữ, luôn luôn.
- **Tín hiệu phụ (gấp, quá hạn) không được trùng màu với một giai đoạn.** Chip "Gấp" màu hổ phách nằm trên đầu thẻ "Chờ nhận" cũng hổ phách → thẻ gấp và thẻ thường trông y hệt. Cho tín hiệu phụ một **dạng** riêng chứ không chỉ một màu: viền vòng đỏ quanh thẻ, chip đặc màu (chữ đảo màu), thêm chữ vào nhãn ("Chờ nhận · Gấp"), và đưa lên đầu danh sách.

## 6. Thẻ cho biết điều quan trọng nhất
- Hiện **hạn chót** (tô màu theo độ gấp) thay cho ngày tạo không nhãn; đơn xong thì hiện "Tạo dd/mm".
- Hiện **mã đơn** thay nhãn cố định lặp ở mọi thẻ.
- Hiện **ảnh người làm** nếu có (`avatar_url`), không chỉ chữ cái đầu.
- Ẩn nút hành động sai trạng thái ("Nhận việc" trên đơn xong).

## 7. Hiệu ứng khi gõ / focus
- **Ô có khung + input bên trong:** tắt outline của input (`outline-none focus-visible:outline-none`), đưa focus lên khung: `focus-within:border-fg/30 focus-within:shadow-[0_0_0_3px_…]`. Thêm nút × xoá khi đã gõ.
- **Input form:** focus = đổi viền + quầng mờ 3px, `transition: border-color .15s, box-shadow .15s`.
- **Thẻ hiện ra khi lọc/tìm:** fade + trượt 4px, 180ms, tắt khi `prefers-reduced-motion`.
  **Bẫy:** `animation-fill-mode: both` giữ `transform: none` sau khi chạy → giết hiệu ứng nâng thẻ khi hover. Dùng `backwards`.

## 8. Form: từ "phức tạp, khó hiểu" sang gọn
Luật:
1. **Tối đa 3 bước** (Loại → Nội dung → Gửi).
2. **Tối đa 3 ô bắt buộc**, hỏi bằng câu thường: "Tóm tắt trong một dòng", "Chuyện gì đang xảy ra?", "Cần xong khi nào?".
3. Độ dài tối thiểu chỉ đủ loại "abc" (5–10 ký tự), không hơn.
4. **Chọn nhanh bằng chip** thay cho bộ chọn ngày khi có thể ("Hôm nay · Ngày mai · 3 ngày · 1 tuần"), vẫn giữ bộ chọn đầy đủ.
5. Ô "trang/hệ thống": chip gợi ý + ô tự do, **không** ép phải là URL.
6. Mọi thứ khác gập trong **"Thêm chi tiết (không bắt buộc)"**; tự mở khi đã có dữ liệu (màn sửa).
7. **Lỗi nằm dưới đúng ô**, viền đỏ, tự xoá khi gõ, cuộn tới lỗi đầu tiên.
8. Nhãn chữ thường, cỡ đọc được (13–14px), không VIẾT HOA 10px.
9. Màn xem lại: định dạng người đọc được + cam kết thời gian phản hồi.
10. Đóng khi đã bắt đầu điền → hỏi trước; Esc đóng như mọi modal khác.
**Bẫy:** giữ nguyên **payload gửi backend** (đổi giao diện, không đổi hợp đồng API). Nếu màn "sửa yêu cầu" dùng chung hàm kiểm tra, nó cũng được nới — nói rõ trong PR. Xoá code chết (chip mẫu, hằng số) thay vì để lại.

## 9. Tab phụ (báo cáo, tài liệu, changelog…)
- Bỏ lớp vỏ riêng của tab (nền, padding, tiêu đề to lặp) → một **thanh công cụ**: mô tả ngắn bên trái, nút chính của tab bên phải, cùng kiểu nút chính.
- Nút chính của trang chỉ hiện ở tab nó thuộc về (một màn — một nút chính).
- **Số đặt cạnh nhau phải cùng phạm vi, hoặc nhãn nói rõ khác phạm vi** ("tháng này" vs "tính đến hôm nay").
- Nhãn trung tính cho sự thật trung tính ("Chưa nhận order"), nhãn đỏ cho vấn đề thật ("Trễ 3 order").
- Link không có ảnh xem trước → hiện tên miền thay khung trống.
- Bảng hẹp: dời cột ghi chú xuống dưới tên thay vì cho cuộn ngang.
- Ngôn ngữ thống nhất (không "Published" giữa giao diện tiếng Việt), ngày `dd/mm/yyyy`.

## 10. Điện thoại
Mở 375×812 chế độ chạm, đi lại mọi màn. Khuôn sửa:
1. **Thanh điều hướng dọc → thanh tab dưới** dưới `md`: icon + nhãn, cao ≥56px, `pb-[env(safe-area-inset-bottom)]`; nội dung chừa đáy `pb-[calc(88px+env(safe-area-inset-bottom))]`. Desktop giữ nguyên.
2. **Lề 16px** trên điện thoại thay lề desktop.
3. **Input ≥16px** trên điện thoại (dùng token cỡ chữ thân bài nếu ≥16px) — nếu không iOS Safari phóng to trang mỗi lần chạm và không tự thu lại.
   ```css
   @media (max-width: 767px) {
     input:not([type=checkbox]):not([type=radio]), textarea, select { font-size: var(--size-body) !important; }
   }
   ```
4. **Vùng chạm 40–44px** chỉ trên điện thoại: `max-md:min-h-[44px]` (hoặc token `min-h-tap`) cho nút thẻ, tab lọc, nút chính, nút đóng.
5. **Form thành sheet toàn màn** với nút hành động **dính đáy** (`position: sticky; bottom: 0`) + safe-area; nút 48px, chip 40px. Nền thanh dính phải cùng nền hộp ở cả dark mode.
6. **Modal có layout inline style** (không sửa bằng class được): gắn class móc (`.editor-overlay`, `.editor-box`, `.editor-2col`) và ghi đè trong media query bằng `!important`: toàn màn, một cột.
7. **Menu chỉ hiện khi hover** → luôn hiện trên thiết bị chạm: `[@media(hover:none)]:opacity-100`.
8. `100vh` → `100dvh` cho khung gốc.
9. Chữ nút không được xuống dòng: `whitespace-nowrap`.
**Bẫy:**
- Sau khi sửa mobile, **đo lại desktop**: thanh dọc hiện, thanh dưới ẩn, cỡ input/tab như cũ.
- Module chạy trong iframe của một app mẹ có điều hướng riêng trên điện thoại → thanh tab dưới có thể chồng lên; ghi vào "cần xem trên máy thật".
- Hàng rào thiết kế có thể đếm "cỡ chữ viết tay" — dùng token cỡ chữ (`text-caption`, `var(--size-body)`) thay số.
