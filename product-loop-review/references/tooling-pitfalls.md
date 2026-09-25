# Bẫy công cụ — đã dẫm, ghi lại để lần sau không dẫm

## Trình duyệt tự động
- **Giả lập viewport rộng trong khung preview hẹp → ảnh bị thu nhỏ** tới mức không đọc được. Đo bằng JS (`getBoundingClientRect`, `getComputedStyle`), ảnh chỉ để minh hoạ. Hoặc dùng trình duyệt thật có cửa sổ rộng (nhưng phải đăng nhập lại ở đó).
- **`window.confirm/alert` chặn mọi lệnh tiếp theo.** Đừng bấm nút sẽ bật hộp thoại gốc; nếu cần thử luồng đó, tạm thay `window.confirm` bằng hàm trả `true/false` rồi trả lại (xem measurement-recipes).
- **Esc ở một form đã có dữ liệu** có thể bật hộp xác nhận — kiểm trang còn phản hồi bằng một lệnh JS nhỏ trước khi đi tiếp.
- **HMR để lại lỗi console của bản sửa dở** (`X is not defined`). Tải lại trang rồi mới đọc console.
- **Ảnh chụp giữa lúc cuộn** có thể trắng một mảng — kiểm DOM trước khi kết luận phần tử không vẽ.
- Công cụ `find` theo ngôn ngữ tự nhiên hay trượt với chữ tiếng Việt → tìm nút bằng `textContent` trong JS.
- Đăng nhập: người dùng tự gõ trong khung trình duyệt; phiên của khung preview và của trình duyệt thật là **riêng**.

## PowerShell 5.1 (Windows)
- **Chuỗi nháy kép ăn backtick** (`` ` `` là ký tự thoát) → template literal JS/TS bị hỏng khi thay chuỗi. Dùng nháy đơn hoặc here-string `@' … '@`, hoặc công cụ Edit.
- **Here-string nhiều dòng truyền cho lệnh ngoài bị tách theo dấu nháy bên trong** (`git commit -F -` với nội dung có `"…"`). Viết nội dung ra file rồi `git commit -F <file>`.
- File có `CRLF`: so khớp chuỗi nhiều dòng phải chuẩn hoá `\r\n` → `\n` trước, không thì "MISSING" dù nhìn thấy giống hệt.
- `Get-Content` mặc định đọc sai UTF-8 → thêm `-Encoding utf8` khi đọc tiếng Việt; ghi bằng `[IO.File]::WriteAllText(path, text, (New-Object Text.UTF8Encoding $false))`.
- `&&` không có trong 5.1 — dùng `;` hoặc `if ($?) { … }`.

## Git / GitHub
- Hook có thể chỉ cho phép `git push <nhánh feature>` và `gh pr create` **khi đứng một mình** — đừng nối với lệnh khác trong cùng một lần chạy.
- Hook `pre-push` chạy cả bộ kiểm tra (vài phút) — chạy trước ở máy để biết kết quả, tránh đẩy hỏng.
- Người duyệt có thể merge PR trước giữa lúc mình làm PR sau → nhánh base bị xoá, `gh pr create` báo "Base ref must be a branch". `git fetch --prune`, kiểm `git log origin/dev..HEAD` chỉ còn commit mới, mở PR vào nhánh tích hợp.
- Không commit file cấu hình máy (`.claude/launch.json`, `.env`).

## Hàng rào thiết kế (design check có baseline)
- Chỉ số tăng (thêm hex, thêm cỡ chữ viết tay) → đỏ. Đừng nới baseline: đổi sang token (`var(--…)`, `text-caption`, `color-mix(…var(--x)…)`), hoặc khai báo màu **một lần** trong biến CSS rồi dùng lại.
- Chỉ số giảm → công cụ gợi ý "hạ mốc" → hạ trong cùng commit, để lần sau không ai thêm lại được.
- Export hằng số từ file component làm hỏng Fast Refresh (cảnh báo lint) → tách hằng số ra file util riêng.
