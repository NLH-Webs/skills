# Riêng tư và nội dung nhạy cảm

Buổi live đã phát công khai **không** có nghĩa được cắt lại, phóng to, đăng lại mọi thứ trong đó. Video cắt lại sống lâu hơn, được chia sẻ rộng hơn, và khung phóng to làm chữ nhỏ trở nên đọc được.

## 1. Thông tin cá nhân trên màn hình
Hay gặp khi người nói chia sẻ màn hình (demo sản phẩm, hồ sơ, bảng tính, app nội bộ):
- Họ tên đầy đủ + ngày/giờ sinh (đặc biệt **của trẻ em**), số điện thoại, email, địa chỉ, số tài khoản.
- Tên và vai trò nhân viên trong app nội bộ, danh sách khách hàng/học viên.
- Tên tài khoản người xem trên thẻ bình luận (chấp nhận ở cỡ nhỏ khi là ngữ cảnh câu hỏi; không phóng to).

### Cách dò cho đủ
1. Xem lưới khung dày (0,5–2s) toàn bộ đoạn chia sẻ màn hình.
2. Tìm thấy một lần → **giả định nó xuất hiện lại**: trang được cuộn lên/xuống, mở lại tab. Dùng `scripts/do_mau.py` với một màu đặc trưng của trang đó để liệt kê mọi cụm giây nó hiện (đo "nền" trước: logo kênh cùng màu cũng khớp).
3. Ở từng cụm: đo vị trí dòng chữ trên vài khung (trang cuộn làm dòng di chuyển) → khai vùng che **rộng tay** phủ hết các vị trí.
4. Làm mờ **ở bước dựng đoạn thô / a-roll** (hoặc ở nguồn bằng `scripts/che_vung.py`) — mọi cảnh phóng to (G2) kế thừa vùng mờ.
5. Mở lưới quanh từng vùng và **thử đọc**. Đọc được một ký tự số là chưa đạt.
6. Báo người nhờ: đã che gì, còn gì hiện (vd. nội dung nhận xét tính cách của một đứa trẻ vẫn hiện trên màn hình và trong lời nói) → **để người nhờ quyết** giữ chương đó hay không.

Người nói tự chia sẻ thông tin **của chính họ** (người lớn): không che, nhưng nhắc trong báo cáo.

## 2. Nội dung nhạy cảm trong lời nói — bỏ và báo
- **Khẳng định sức khoẻ/y tế** không có cơ sở (vd. "hồ sơ này cho biết cơ quan nào trong cơ thể con bạn yếu") → rủi ro quảng cáo; bỏ câu nhấn mạnh nhất, báo phần còn lại.
- **Lời hứa / khuyến mãi chưa chắc** (vd. hứa tặng quà cho học viên một khoá mà chính người nói bảo chưa hỏi đội vận hành) → bỏ, báo.
- **Câu đùa về tự tử, tự hại, bạo lực**, kể cả đùa nội bộ → bỏ.
- **Chuyện nội bộ team, chuyện cân nặng/ngoại hình người khác, người thứ ba vắng mặt** → bỏ hoặc hỏi.
- **Tên thương hiệu nghe không chắc** → không ghi lên phụ đề (bỏ riêng tên đó).

## 3. Báo cáo
Mục riêng "Cần quyết" ở đầu báo cáo, mỗi dòng: chuyện gì · đã xử lý thế nào · lựa chọn còn lại. Không chôn vào cuối.
