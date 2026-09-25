# Câu hỏi theo vai — và lỗi hay gặp

Đi theo đúng thứ tự dòng chảy sản phẩm. Ba vai đầu (PM, UX, UI) là **product trio** — quyết định trước khi ai viết code, nên lỗi của họ nặng nhất. Mỗi vai: câu hỏi gốc → chỗ nhìn → lỗi hay gặp (đã thấy thật) → cách đo.

---

## 1. Product Manager — làm gì, cho ai, ưu tiên gì
**Câu gốc:** người dùng có làm xong việc chính không, và có việc nào *biến mất* khỏi tầm mắt?

Nhìn vào: bảng việc chính, lưu trữ/lọc mặc định, các mục điều hướng.

Lỗi hay gặp:
- **Việc bị giấu theo tuổi, không theo trạng thái.** Luật "lưu trữ = tạo hơn 30 ngày" làm đơn *đang chờ* biến khỏi bảng chính. Đo: đếm đơn chưa xong trong mục lưu trữ; đọc luật lọc ở backend.
- **Mục điều hướng dẫn tới ngõ cụt** ("Đang phát triển"). Một mục menu là một lời hứa; chưa làm thì ẩn.
- **Lời hứa bị định nghĩa mà không hiển thị** — hằng số SLA, class CSS có sẵn nhưng không màn nào dùng. Tìm: `grep` hằng số/class không có chỗ gọi.

## 2. UX Designer / Researcher — luồng, chỗ kẹt
**Câu gốc:** đi từ đầu đến cuối có chỗ nào kẹt, mất dữ liệu, hoặc không thoát ra được?

Lỗi hay gặp:
- **Modal tràn khung hẹp** — nút đóng và nửa nội dung nằm ngoài màn hình. Đo: `getBoundingClientRect()` của hộp so với `innerWidth`.
- **Đóng form là mất sạch bản nháp**, không hỏi. Esc không đóng một modal nhưng đóng modal khác (không nhất quán).
- **Form quá nhiều bước, quá nhiều ô bắt buộc**, độ dài tối thiểu tuỳ tiện, ô chỉ nhận URL, lỗi hiện từng cái một ở cuối form.
- **Bong bóng chat xuống dòng từng chữ** — hàng flex co theo nội dung nên `max-width: 80%` tính trên… chính nó.

## 3. UI Designer — đẹp, đúng hệ, đọc được trong một giây
**Câu gốc:** nhìn một giây có phân biệt được trạng thái không? Dark mode có đọc được không?

Lỗi hay gặp:
- **Mọi thẻ cùng một màu**, trạng thái chỉ nằm trong một nhãn nhỏ.
- **Dark mode nửa vời:** một bản vá toàn cục đổi `bg-white` thành tối nhưng chữ mã hex vẫn tối → chữ tối trên nền tối. Đo: bật `.dark`, đọc `getComputedStyle(el).color` và nền.
- **Tiêu đề lặp:** tiêu đề trang + tiêu đề to y hệt bên trong tab.
- **Nút trông như nút mà không bấm được** (nhãn vai trò viền như button).
- **Hai nút chính cạnh nhau** tranh nhau ("Tạo order" và "Tạo release" trên cùng màn).
- **Vòng focus lồng trong ô** (ô tìm kiếm có viền, input bên trong lại có vòng focus riêng).

## 4. Tech Lead / Solution Architect — kiến trúc, chặn sai lầm kỹ thuật
**Câu gốc:** code có nói dối không, và luật có nằm đúng tầng không?

Lỗi hay gặp:
- **Comment nói một đằng, code làm một nẻo.**
- **Luật nghiệp vụ sai nằm ở backend** (lọc theo tuổi) — giao diện lách được, nhưng phải ghi lại cho backend.
- **Trạng thái cá nhân lưu ở trình duyệt** (localStorage) cho thứ lẽ ra cả đội thấy.
- **Lỗi hydrate** (`<div>` trong `<p>`), cảnh báo console bị bỏ qua lâu ngày.

## 5. Developers — frontend, backend
**Câu gốc:** có nút chạy mà không làm gì? có code chết?

Lỗi hay gặp:
- **Nút ghi vào kho mà không ai đọc lại** (state khởi tạo rỗng thay vì đọc kho; component nhận prop rồi bỏ qua).
- **So sánh nhãn hiển thị với trạng thái thô** (`o.status === 'blocked'` trên đối tượng đã map sang nhãn "Bị chặn") → điều kiện không bao giờ đúng.
- **Code chết:** hằng số, component, class không còn chỗ dùng. Xoá, đừng để lại "phòng khi".

## 6. QA / Tester — tìm lỗi trước người dùng
**Câu gốc:** giờ, múi giờ, rỗng, dài, lỗi mạng, bấm đúp — cái nào vỡ?

Lỗi hay gặp:
- **Lệch múi giờ:** bộ chọn lưu `+07:00` nhưng hiển thị bằng giờ máy → máy +08 thấy 19:00 cho hạn 18:00. Đo: đổi/đọc `Intl.DateTimeFormat().resolvedOptions().timeZone`, so chuỗi lưu với chuỗi hiện.
- **Chuỗi ISO thô trên màn xem lại** (`2026-09-29T18:00:00+07:00`).
- **Nút xuất hiện sai trạng thái** ("Nhận việc" trên đơn đã xong).
- **Lỗi cũ không tự xoá** khi người dùng đã sửa ô.
- **Không có test cho logic nghiệp vụ** — chỉ có test cho hạ tầng.

## 7. DevOps / Release Engineer — chạy, build, lên production an toàn
**Câu gốc:** người mới chạy được ở máy trong 10 phút không? CI có bắt được lỗi vừa thấy không?

Lỗi hay gặp: `.env` ở máy lỗi thời so với `.env.example`; CI chỉ kiểm build mà không kiểm giao diện; hàng rào thiết kế có baseline nhưng không ai hạ mốc khi tốt lên.

## 8. Data Analyst — đo sau khi ra mắt
**Câu gốc:** đo được người dùng rớt ở bước nào không? số trên dashboard có trung thực?

Lỗi hay gặp:
- **Chỉ có page view**, không có sự kiện "mở form / tới bước N / gửi" → không đo được phễu.
- **Số khác phạm vi đặt cạnh nhau như cùng loại** ("N nhận *tháng này*" cạnh "M trễ *tính đến hôm nay*"). Sửa nhãn đơn vị, không đổi phép tính.
- **Nhãn đổ lỗi:** người chưa được giao việc bị gắn "Cần chú ý".
- **Màu biểu đồ không khớp màu trạng thái** ở bảng chính.

## 9. Product Marketing / Growth — làm cho người ta dùng
**Câu gốc:** người mới có hiểu tính năng không, chữ có dễ hiểu không?

Lỗi hay gặp: chữ tiếng Anh lẫn tiếng Việt ("Published"), định dạng ngày lạ ("9 thg 8 2026"), mô tả tính năng kết thúc bằng "…" trông như bị cắt, thiếu trạng thái rỗng có lời mời hành động.

## 10. Customer Success / Support — nhận phản hồi, đưa ngược về PM
**Câu gốc:** khi người dùng hỏi "đơn của tôi đâu / bao giờ xong", màn hình có trả lời được không?

Lỗi hay gặp: đơn cũ chưa xong bị giấu; không thấy hạn chót trên thẻ (chỉ thấy ngày tạo không nhãn); không hiển thị cam kết thời gian phản hồi; thao tác quản lý chỉ hiện khi rê chuột → trên điện thoại không làm được.

---

## Vai phụ nhưng phải soi: điện thoại
Không phải một vai, nhưng là khung mà cả 10 vai hay quên. Mở 375×812 chế độ chạm và kiểm:
- Thanh điều hướng dọc ăn bao nhiêu % chiều ngang? Có nhãn không?
- Input dưới 16px → iOS Safari phóng to trang khi chạm.
- Vùng chạm dưới 44px (nút thẻ, tab lọc, nút đóng).
- Menu chỉ hiện khi hover → không bao giờ hiện trên điện thoại.
- Form dài: nút "Tiếp" có nằm dưới nếp gấp không?
- `100vh` nhảy khi thanh trình duyệt co giãn → dùng `100dvh`.
- Có cuộn ngang ở màn nào không?
