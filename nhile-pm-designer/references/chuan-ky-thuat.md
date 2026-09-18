# Chuẩn kỹ thuật một PM phải tôn trọng
PM và Designer không viết mã, nhưng **mọi dòng trong PRD đều biến thành một quyết định kỹ thuật**. File này là những chuẩn mà nếu PRD đi ngược, đội kỹ thuật sẽ phải trả lại — và họ đúng.

Đây là **quy ước dùng chung**, đã bỏ mọi thứ riêng của một tổ chức cụ thể. Con số, tên máy chủ và schema thật nằm ở kho riêng.

---

## 1. Mười một câu hỏi bộ lọc — chạy trước khi chốt spec
Đây là bộ lọc của một kỹ sư trưởng có 8 năm dựng hệ thống. Một PRD không qua được bộ này thì đội kỹ thuật sẽ chặn ở cửa sau, tốn hơn nhiều.

1. **Test 300 năm** — 300 năm sau người ta còn cần cái này không? Không → đừng xây.
2. **Test cái tôi** — việc này vì bức tranh chung hay vì thoả mãn cá nhân?
3. **Test sản phẩm** — tạo ra thứ con người cần, hay thứ mình thích?
4. **Test liên bộ phận** — bộ phận kia **thật sự** muốn gì? **Đã hỏi họ chưa?**
5. **Test phản hồi** — đang nhận phản hồi, hay đang tìm lý do để không đổi?
6. **Test di sản** — nếu đội kỹ thuật ngày mai không còn, sản phẩm tự sống được không?
7. **Test dữ liệu** — dữ liệu này 100 năm sau còn giá trị không?
8. **Test "ngày mai tôi chết"** — sản phẩm chạy tiếp không · có ai bị kẹt vì tôi không · người sau hiểu và tiếp được không? **Đủ cả ba mới đạt.**
9. **Test DRI** — ai chịu trách nhiệm việc này? **Không nói được một tên cụ thể → chưa rõ ràng.**
10. **Test đơn giản** — người dùng có phải đọc hướng dẫn mới dùng được không? Có → thiết kế lại.
11. **Test chất lượng ship** — mình có tự hào ship cái này không? Ngại → chưa đủ tốt.

**Cổng quy trình đi kèm:** bắt buộc lấy ý kiến các bộ phận khác **trước khi xây**. Và ngược lại: đội kỹ thuật không được tự quyết spec. Hai vế cùng lúc, không chọn một.

## 2. Sáu luật kiến trúc PM không được vi phạm
1. **Test 300 năm đứng trước mọi feature.**
2. **Tách dữ liệu bất biến khỏi dữ liệu đổi được.** Bất biến = bản chất con người, hành trình phát triển, hành vi. Đổi được = công cụ, giao diện, công nghệ, quy trình. Tách để lõi không chết khi công nghệ đổi.
3. **Ghi hành trình, không ghi ảnh chụp.** Lưu cả quá trình, không chỉ trạng thái hiện tại.
4. **Moat nằm ở dữ liệu hành trình, không ở tính năng.** *Giá trị = dữ liệu × thời gian.* Đối thủ chép được giao diện, không chép được mười năm dữ liệu.
5. **Làm thứ người cần, không phải thứ mình thích.** Vi phạm → sản phẩm thành rác.
6. **Dữ liệu là di sản.** Phân tầng quyền và chính sách dữ liệu là **kiến trúc lõi**, không phải việc làm sau.

## 3. Lớp Apple — sáu nguyên tắc thực thi
- **DRI** — mỗi việc **một** người chịu trách nhiệm, không phải một hội đồng.
- **Đơn giản** — nếu phải dạy người dùng cách dùng thì thiết kế đã hỏng. Đơn giản ở mặt trước, phức tạp ở phía sau.
- **Kiểm soát trọn tầng** — không phụ thuộc nhà cung cấp cho phần **lõi** giá trị.
- **Riêng tư theo thiết kế** — thu ít nhất có thể · xử lý tại thiết bị khi được · minh bạch và cho người dùng quyền · bảo mật là nền, không phải lớp phủ.
- **Chỉ ship khi đủ tốt** — *"tạm được" không tồn tại.* Ship "cho có" rồi sửa sau là cách tạo ra rác.
- **Đi qua làn của nhau** — kỹ sư phải hiểu thiết kế và nội dung; **kỹ năng diễn đạt được đánh giá ngang kỹ năng viết mã**. Nếu kỹ sư không giải thích được tính năng cho người làm nội dung hiểu thì tính năng đó chưa đủ rõ.

## 4. Đặt tên đường dẫn API — PRD nào nhắc tới API phải theo
```
https://{api_domain}/api/{scope}/{resource}[/{id}][/{sub-resource}]
```
- `/api` là tiền tố toàn cục, đặt một lần ở tầng ứng dụng. Controller **không** tự thêm.
- **Bốn loại `scope`, không có loại thứ năm:**
  1. **Portal (BFF)** — endpoint chỉ phục vụ đúng một portal, gom nhiều nguồn thành một phản hồi cho màn hình đó.
  2. **Domain dùng chung** — tài nguyên dùng cho từ hai portal trở lên. Scope = tên tài nguyên số nhiều.
  3. **Portal + domain lồng nhau** — hiện chỉ một portal dùng, nhưng về kiến trúc là domain riêng, sau có thể chia sẻ.
  4. **Hạ tầng** — `auth`, `health`, `realtime`.

**Quy tắc đặt tên (client và backend phải giống nhau tuyệt đối):**

| Luật | Đúng | Sai |
|---|---|---|
| Tài nguyên số nhiều | `/api/users` | `/api/user` |
| kebab-case | `/api/auth/token/mini-app` | `/api/auth/token/miniApp` |
| Người dùng hiện tại là `me` | `/api/users/me` | `/api/users/{uid}` |
| ID ở cuối đoạn của thực thể | `/api/users/:id/dock` | `/api/dock?userId=...` |
| Hành động không RESTful → dùng danh từ | `POST /api/space/signals` | `POST /api/space/send-signal` |
| Lọc và phân trang bằng query string | `/api/leads?stage=new&page=2` | `/api/leads/stage/new/page/2` |
| **Không có động từ trong đường dẫn** | `DELETE /api/users/:id` | `/api/users/delete/:id` |

**Khuôn trả lời chuẩn:** thành công `{ data, meta? }` · lỗi `{ statusCode, message, errors[] }`. PRD không được tự đặt khuôn khác.

## 5. Quy ước bảng dữ liệu
- Cột ở cấp trên cùng = thứ **truy vấn được, có chỉ mục, thuộc lõi**.
- `metadata` (jsonb) = thứ tuỳ ngữ cảnh, mở rộng được.
- `payload` (jsonb) = kho sự kiện, **bất biến**.
- Mọi bảng có `created_at` + `updated_at` kèm múi giờ, mặc định `now()`.
- **Migration là nguồn sự thật, không phải seed.** Máy chạy tự động chỉ chạy migration; sửa seed mà quên migration nghĩa là bản thật không đổi.
- Đổi một danh mục = viết **migration mới**, không sửa migration cũ. Migration bất biến = lịch sử kiểm toán được.

## 6. Năm luật viết nội dung và ghi lịch sử
1. **Một loại nội dung, một chủ.** Nói rõ bộ phận nào sở hữu loại nào; các bên khác chỉ **ghép nội dung đã xuất bản và đang hiện**.
2. **Bản đồ nội dung và lịch sử là hình chiếu chỉ-đọc**, không phải quyền ghi chung.
3. **Ghi cùng một khối phải kèm số phiên bản mong đợi** — không bao giờ để người ghi sau đè người ghi trước trong im lặng.
4. **Lịch sử chỉ thêm, và đã được làm sạch**: không chứa khoá lưu trữ, không đường dẫn ký sẵn, không token, không dữ liệu người học.
5. **REST là chuẩn.** Cơ chế thời gian thực chỉ là *gợi ý làm mới* — client vẫn phải tự lấy lại dữ liệu khi mở màn, khi kết nối lại, khi quay lại tab.

## 7. Khuôn ghi quyết định — dùng thay cho "sổ nợ kỹ thuật" tự chế
Mỗi quyết định kiến trúc ghi đủ sáu mục:

| Mục | Nội dung |
|---|---|
| **Bối cảnh** | Vì sao phải quyết bây giờ |
| **Quyết định** | Chốt cái gì, cụ thể tới mức làm được |
| **Lý lẽ** | Vì sao chọn thế này |
| **Cái mất** | Đánh đổi gì, rủi ro gì |
| **Đường thoát** | Nếu sau này sai thì đổi bằng cách nào, tốn bao nhiêu |
| **Ai duyệt** | Tên người + ngày |

Mục **Đường thoát** là mục hay bị bỏ nhất và cũng là mục cứu nhiều tiền nhất: nó buộc người quyết phải nghĩ trước *nếu chọn sai thì gỡ thế nào*. Một quyết định không có đường thoát là một cái khoá, không phải một lựa chọn.

## 8. Quy tắc làm việc trên mã nguồn
- **Không đẩy thẳng lên nhánh chính.** Luôn nhánh riêng + pull request.
- **Conventional Commits bắt buộc** — `feat` · `fix` · `docs` · `style` · `refactor` · `perf` · `test` · `build` · `ci` · `chore` · `revert`. Có hook chặn; không tự bỏ qua hook.
- Nêu đủ bằng chứng khi báo xong: migration, kiểm thử, kiểu dữ liệu, chạy thật.
- **Không báo "xong giao diện" khi mới đổi backend.** Hai kho là hai việc.

## 9. Bốn chỗ PM và kỹ sư trưởng chắc chắn va nhau
Biết trước để thoả thuận, đừng để va giữa sprint.

| Va ở đâu | PM thường muốn | Kỹ sư trưởng thường chốt | Cách gỡ |
|---|---|---|---|
| **Ship nhanh vs ship đủ tốt** | Bản tối thiểu, học rồi sửa | *"Tạm được không tồn tại"* | Thoả thuận trước: cái gì được ra bản thử, cái gì phải hoàn chỉnh mới ra |
| **Cửa sổ thị trường vs 300 năm** | Tính năng thắng trong 18–24 tháng | Không qua test 300 năm là chặn ở cửa | Tách rõ: lớp lõi theo 300 năm, lớp giao diện theo thị trường |
| **Đo nhiều vs thu ít** | Theo dõi dày để đo hành vi | Dữ liệu không tồn tại thì không lộ được | Chốt một luật ưu tiên **trước** khi viết spec theo dõi |
| **Tài liệu là việc phụ vs điều kiện ship** | Viết sau | Thiếu ghi chép = trượt test "ngày mai tôi chết" | Đưa ghi chép vào định nghĩa "xong", không phải việc thêm |

## 10. Hai chỗ mâu thuẫn hay gặp trong chính bộ chuẩn — phải có trọng tài
Mọi bộ chuẩn đủ lâu đều tự mâu thuẫn. Hai chỗ kinh điển:

1. **"Thu ít nhất có thể" vs "dữ liệu là moat, mỗi ngày thu thêm là dày thêm".** Hai luật này chặn nhau trực tiếp. Không có ai làm trọng tài thì mỗi bên trích luật có lợi cho mình. **Phải chốt một quy tắc ưu tiên viết ra giấy** trước khi thiết kế bất kỳ bảng theo dõi nào.
2. **"Đội kỹ thuật không được tự quyết spec" vs "DRI có quyền quyết định chiến thuật".** Ranh giới *chiến thuật* và *chiến lược* thường không được định nghĩa ở đâu cả. **PM phải chốt ranh giới này trước**, không thì mỗi lần va lại cãi từ đầu.

Khi gặp mâu thuẫn trong chuẩn: **đừng chọn vế tiện cho mình**. Nêu cả hai ra, nói rõ mình chọn vế nào và vì sao, ghi vào sổ quyết định theo khuôn §7.
