---
name: product-loop-review
description: Mở sản phẩm web đang chạy lên, tự bấm như người dùng thật, soi nó lần lượt qua 10 vai của vòng đời sản phẩm (PM → UX → UI → Tech Lead → Dev → QA → DevOps → Data → Marketing → Customer Success), đo mọi phát hiện bằng bằng chứng, rồi TỰ SỬA giao diện — kể cả hệ màu trạng thái, dark mode, hiệu ứng khi gõ, làm gọn form, các tab phụ và tối ưu cho điện thoại — và mở PR nhỏ, dễ duyệt. Dùng khi được nhờ "mở web lên trải nghiệm như người dùng thật", "đi qua các vai PM/UX/UI/QA…", "review UX UI rồi sửa", "đưa feedback và sửa giao diện", "product trio xem giúp", "audit giao diện module này", "form khó hiểu quá", "dark mode sai", "không phân biệt được trạng thái", "tối ưu mobile", hoặc khi ai đó dán link PR/repo và bảo "xem trải nghiệm rồi sửa". Không dùng để viết PRD cho ý tưởng chưa có sản phẩm (dùng nhile-pm-designer) hay để review code thuần không chạy app.
---

# Review vòng đời sản phẩm — bấm thật, đo thật, sửa thật

## Việc của skill này
Nhận một sản phẩm web **đang chạy được**, trả về ba thứ:
1. **Bảng phản hồi theo vai** — mỗi dòng một vấn đề, có bằng chứng đo được, ghi rõ *đã sửa* hay *chưa sửa, vì sao*.
2. **Các PR sửa giao diện** — nhỏ, theo thứ tự ưu tiên, mỗi PR tự kiểm được.
3. **Một câu trả lời ngắn cho người nhờ** — kết quả trước, việc họ cần làm tiếp sau.

Người nhờ thường **thêm yêu cầu giữa chừng** ("thêm màu cho trạng thái", "dark mode sai", "form rối quá", "làm nốt 3 tab kia", "tối ưu mobile"). Đó là bình thường — mỗi yêu cầu là một bước trong quy trình dưới, làm xong bước đang dở rồi nhận tiếp, không bỏ ngang.

## 10 luật gốc
1. **Chạy ở máy, trên dữ liệu thử — không bấm lung tung trên production.** Code mình sửa là code ở máy; production là đơn thật của người thật. Chỉ mở production để *xem* khi không có cách nào khác, và nói ra.
2. **Không gõ mật khẩu, không tự bấm nút không quay lại được.** Đăng nhập: nhờ người dùng tự gõ. Gửi đơn, nhận việc, xoá, đăng: dừng ở bước xem lại, hỏi trước.
3. **Mọi phát hiện phải có bằng chứng.** Một con số đo được, một dòng code, một ảnh chụp, một lệnh chạy ra kết quả. "Có vẻ chật" không phải phát hiện; "nút cao 30px, chuẩn chạm là 44px" mới là phát hiện.
4. **Báo cáo và comment là gợi ý, code mới là sự thật.** Một comment ghi "dưới 900px sẽ xếp dọc" mà code đặt `min-width: 760px` thì code thắng — và đó là một phát hiện.
5. **Soi đủ bốn khung:** màn hẹp (khung nhúng/tablet) · desktop · điện thoại 375px chạm · dark mode. Lỗi nằm ở chỗ không ai mở.
6. **Sửa gốc, không vá mặt.** Màu chữ tối trên nền tối vì bản vá `.dark .bg-white` chỉ đổi nền → đổi sang biến vai trò (token), đừng vá thêm một lớp nữa.
7. **Giao diện chỉ hiển thị; luật nghiệp vụ sai ở máy chủ thì ghi lại.** Được phép lách ở giao diện nếu an toàn và nói rõ; không tự sửa backend trong PR giao diện.
8. **Màu không bao giờ là tín hiệu duy nhất.** Mỗi màu trạng thái đi kèm chữ; mỗi lỗi form đi kèm câu giải thích.
9. **Chữ trên màn hình là chữ của người dùng.** Tiếng Việt thường, nói sự thật đằng sau con số ("tính đến hôm nay"), không đổ lỗi ("Chưa nhận order" thay vì "Cần chú ý" cho người chưa được giao việc).
10. **Để lại chỗ tốt hơn lúc đến.** Hàng rào tự động của repo (lint, design check, baseline) chỉ được giữ hoặc siết — hạ mốc khi con số tốt lên, không bao giờ nới.

## Quy trình

### Bước 0 — Dựng chỗ chạy (≤ 10 phút)
- Đọc `README`/`CLAUDE.md` của repo: lệnh chạy, cổng, môi trường, luồng git, file cấm sửa (kit/lõi dùng chung).
- So `.env` với `.env.example`: `.env` cũ thường trỏ nhầm backend/đăng nhập. Sao lưu rồi thay.
- Chạy dev server qua công cụ preview (không chạy bằng shell). Mở trang, **nhờ người dùng đăng nhập** bằng tài khoản thử.
- Tạo nhánh làm việc từ nhánh tích hợp (thường `dev`), đúng tiền tố repo quy định.

### Bước 1 — Bấm thật như người dùng, đi đủ màn
Đi hết: danh sách → chi tiết → tạo mới (đến bước xem lại, **không gửi**) → lọc/tìm → lưu trữ → từng tab phụ. Với mỗi màn: chụp ảnh ở khung hẹp và desktop, đọc chữ (`get_page_text`), đọc console. Ghi mọi chỗ "khựng": phải nghĩ mới hiểu, bấm không ra gì, chữ bị cắt, số trông mâu thuẫn.

### Bước 2 — Soi qua 10 vai
Với từng vai, hỏi đúng câu của vai đó — danh sách câu hỏi và lỗi hay gặp ở `references/role-checklists.md`. Tóm tắt:

| Vai | Câu hỏi gốc |
|---|---|
| PM | Người dùng có làm xong việc chính không? Có việc nào **biến mất** khỏi tầm mắt? |
| UX | Luồng có chỗ nào kẹt, mất dữ liệu, không thoát ra được? |
| UI | Nhìn một giây có phân biệt được trạng thái? Có đúng hệ thiết kế, đủ dark mode? |
| Tech Lead | Code có nói dối (comment ≠ hành vi)? Luật nằm sai tầng? |
| Dev | Có nút chạy mà không làm gì? Có code chết? |
| QA | Giờ, múi giờ, rỗng, dài, lỗi, bấm đúp — cái nào vỡ? |
| DevOps | Chạy ở máy có dễ không? CI/kiểm tra tự động có bắt được lỗi này không? |
| Data | Đo được người dùng rớt ở bước nào không? Số trên dashboard có trung thực? |
| Marketing/Growth | Người mới có hiểu tính năng không? Chữ có dễ hiểu? |
| Customer Success | Khi người dùng kêu "đơn của tôi đâu", có trả lời được không? |

### Bước 3 — Đo từng phát hiện
Mỗi nghi ngờ → một phép đo. Công thức đo có sẵn (JS chạy trong trang) ở `references/measurement-recipes.md`: nút nhỏ hơn 44px, tràn ngang, input dưới 16px (iOS phóng to), cuộn lồng nhau, hiệu ứng nào chạy khi gõ, múi giờ, màu thật trong dark mode, `window.confirm` chặn trình duyệt tự động.
Rồi mở code tìm **gốc**: dòng nào gây ra, luật backend nào đứng sau.

### Bước 4 — Chia: sửa ngay hay ghi lại
- **Sửa ngay:** thuộc giao diện repo này, không đụng file lõi dùng chung, không cần quyết định sản phẩm mới.
- **Ghi lại (mục "Tìm thấy, chưa sửa"):** cần backend, cần sửa kit/template dùng chung, cần người chủ quyết (xoá một tính năng, đổi cam kết SLA), thiếu đo lường/test.

### Bước 5 — Sửa theo thứ tự này
1. **Việc bị giấu / dữ liệu sai** — đơn biến khỏi bảng, giờ lệch múi, số hiển thị sai.
2. **Nút chết / hành động sai** — bấm không làm gì, nút xuất hiện sai trạng thái.
3. **Bố cục vỡ** — modal tràn, chữ xuống dòng từng chữ, cuộn ngang.
4. **Dark mode** — chuyển sang token vai trò.
5. **Hệ màu trạng thái** — mỗi giai đoạn một màu, tab làm chú giải.
6. **Hiệu ứng tương tác** — focus, gõ, xuất hiện.
7. **Form** — làm gọn (xem luật form ở `references/ui-fix-patterns.md`).
8. **Các tab phụ** — cùng khuôn: một thanh công cụ + nội dung, bỏ tiêu đề lặp.
9. **Điện thoại** — thanh tab dưới, input ≥16px, vùng chạm ≥44px, form thành sheet toàn màn, `100dvh`.

Khuôn sửa cho từng loại (và cái bẫy của mỗi khuôn) ở `references/ui-fix-patterns.md`.

### Bước 6 — Kiểm sau mỗi lần sửa
- Tải lại trang (HMR để lại lỗi console cũ — đừng đọc nhầm).
- Kiểm lại đúng phép đo ở bước 3, ở cả bốn khung (hẹp · desktop · 375px · dark) — light mode không được vỡ khi sửa dark, desktop không được đổi khi sửa mobile.
- Chạy lệnh kiểm tra của repo (`verify`/`test`/`lint`/design check). Con số hàng rào giảm thì **hạ mốc baseline** trong cùng commit.

### Bước 7 — Commit và PR
- Mỗi commit một chủ đề, thân commit kể *vấn đề đo được → cách sửa*.
- Tôn trọng giới hạn số file/PR của repo: vượt thì tách PR (chồng nhánh nếu phụ thuộc, nói rõ thứ tự duyệt).
- Không đẩy thẳng nhánh chính, không tự merge. Khuôn PR và báo cáo ở `references/pr-and-report-templates.md`.
- Bẫy công cụ (PowerShell nuốt backtick, hook chặn lệnh nối, CRLF…) ở `references/tooling-pitfalls.md`.

### Bước 8 — Trả lời người nhờ
Câu đầu: đã làm gì, ở đâu (link PR). Sau đó bảng theo vai (gọn), rồi 2–3 việc **họ** cần làm (duyệt PR, gửi thử một đơn thật trên staging, xem trên điện thoại thật). Không kể quá trình.

## Cửa chặn — phạm một cái là chưa được giao
1. Đã bấm gửi/xoá/nhận việc trên dữ liệu thật mà chưa hỏi.
2. Có phát hiện không kèm bằng chứng.
3. Sửa dark mode mà light mode đổi, hoặc sửa mobile mà desktop đổi, không ai kiểm.
4. Nới một hàng rào tự động (baseline, lint rule) để PR qua.
5. Đưa dữ liệu nội bộ (tên người, URL máy chủ, tài khoản thử) vào repo công khai.

## Tài liệu kèm
- `references/role-checklists.md` — câu hỏi và lỗi hay gặp cho từng vai.
- `references/measurement-recipes.md` — đoạn JS đo trong trang, cách đọc kết quả.
- `references/ui-fix-patterns.md` — khuôn sửa: màu trạng thái, dark mode, modal, form, hiệu ứng gõ, tab phụ, điện thoại.
- `references/pr-and-report-templates.md` — khuôn commit, PR, bảng phản hồi, câu trả lời cuối.
- `references/tooling-pitfalls.md` — bẫy công cụ khi làm trên Windows/PowerShell, trình duyệt tự động, hook.
