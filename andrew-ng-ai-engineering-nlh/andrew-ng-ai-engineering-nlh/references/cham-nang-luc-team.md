# Chấm năng lực, tuyển và đào tạo team theo bản đồ của Ng

Lưu ý: Ng chưa công bố thang cấp độ chính thức. Thang dưới đây do NLH đặt để dùng nội bộ, bám theo các kỹ năng con Ng đã nêu.

## Thang bốn mức (NLH)

| Mức | Tên | Nhìn thấy được khi |
|---|---|---|
| 0 | Chưa có | Chưa làm việc này bao giờ, hoặc làm mà không biết mình đang làm gì |
| 1 | Làm theo | Làm được khi có hướng dẫn từng bước hoặc có người kèm |
| 2 | Tự làm | Tự làm việc thường ngày đúng chuẩn, tự biết khi nào cần hỏi |
| 3 | Tự quyết & dạy | Tự chọn đánh đổi, giải thích được vì sao bằng lời thường, dạy được người khác |

Mục tiêu đội: mỗi kỹ năng con quan trọng có **ít nhất một người thật ở mức 3** và **ít nhất hai người ở mức 2** (để không ai là người duy nhất nắm). Claude không tính vào số người.

## Bảng tự chấm (điền cho từng người)

Mỗi người tự chấm, rồi người dẫn đội chấm lại dựa trên việc đã làm thật; chỗ lệch nhiều là chỗ cần nói chuyện.

```
Người: …            Vai: …             Ngày chấm: …
Kỹ năng 1 — AI:     1.1 _ 1.2 _ 1.3 _ 1.4 _ 1.5 _ 1.6 _
Kỹ năng 2 — Nền:    2.1 _ 2.2 _ 2.3 _ 2.4 _ 2.5 _
Kỹ năng 3 — Agent:  3.1 _ 3.2 _ 3.3 _ 3.4 _ 3.5 _
Kỹ năng 4 — Định hình: 4.1 _ 4.2 _ 4.3 _ 4.4 _
Ví dụ việc thật chứng minh mức cao nhất: …
Muốn lên mức ở kỹ năng: …
```

Gộp bảng của cả đội thành một lưới người × kỹ năng con. Cột nào không có ô mức 3 là chỗ phải tuyển hoặc đào tạo trước.

## Bài thử việc — mỗi kỹ năng một bài, làm trên việc thật

Nguyên tắc: xem cách người ta làm việc thật trong vài giờ, không dựa vào trắc nghiệm hay lời kể.

- **Kỹ năng 1 — kiểm chất lượng AI.** Đưa 30 đầu ra thật của một tính năng AI (ví dụ hồ sơ hoặc lead đã phân loại). Yêu cầu: chấm được/không, gom lỗi thành nhóm, đếm, đề xuất sửa nhóm lớn nhất trước, viết 3–5 tiêu chí chấm. Người giỏi sẽ xem dữ liệu trước rồi mới đặt tiêu chí.
- **Kỹ năng 2 — đánh đổi.** Đưa một tình huống thật (ví dụ: con số học viên ở hai portal lệch nhau, hoặc một trang tải chậm). Yêu cầu: giải thích bằng lời thường cho Nhi nguyên nhân có thể nằm ở tầng nào, có những cách sửa nào, mỗi cách đổi cái gì lấy cái gì. Người giỏi nói được đánh đổi mà không cần thuật ngữ.
- **Kỹ năng 3 — dùng agent.** Giao sửa một tính năng nhỏ trên bản xem thử trong 2–3 giờ bằng Claude Code. Chấm: có lên kế hoạch và soát kế hoạch không, có cho agent cách tự kiểm không, có nộp ảnh chụp làm bằng chứng không, có dừng agent đúng lúc không, có để lại ghi chú bàn giao và cập nhật CLAUDE.md không, có đụng vào dữ liệu thật không.
- **Kỹ năng 4 — định hình.** Cho nói chuyện 15 phút với hai người dùng thật (học viên, giảng viên hoặc nhân viên vận hành), rồi đề xuất một thay đổi kèm lý do và cách đo xem thay đổi có hiệu quả không. Người giỏi hỏi nhiều, nói ít, và đề xuất gắn với giá trị cho người dùng.

## Lộ trình đào tạo theo chỗ hổng

- **Hổng kỹ năng 1.** Giao làm chủ bộ kiểm chất lượng của một tính năng AI đang chạy: lập bảng ca thử, cùng Nhi chấm mẫu, chạy lại sau mỗi lần sửa trong một tháng.
- **Hổng kỹ năng 2.** Mỗi tuần một buổi đọc lại một quyết định kỹ thuật agent đã làm trong dự án thật và giải thích đánh đổi cho người khác; bắt đầu từ phần dữ liệu dùng chung.
- **Hổng kỹ năng 3.** Làm cặp với người mức 3 trên một khối thật; sau mỗi lượt chạy viết rút kinh nghiệm vào CLAUDE.md.
- **Hổng kỹ năng 4.** Mỗi tháng ngồi dự một buổi học hoặc một ca vận hành thật; đọc phần "vì sao" của PRD trước khi làm; tự viết bản mô tả cho một việc nhỏ.

## Khi tuyển người

- Ưu tiên theo cột trống trên lưới năng lực, không theo chức danh.
- Với đội nhỏ dùng nhiều agent, người đáng tuyển nhất thường là người **mức 3 ở kỹ năng 2 và 3** (soát được đánh đổi agent chọn, lái được quy trình) và **ít nhất mức 2 ở kỹ năng 1.4** (kiểm chất lượng AI).
- Luôn dùng bài thử việc thật ở trên; xem cả cách họ giải thích cho người không làm kỹ thuật.

## Khi cả đội học chứng chỉ Claude

Đối chiếu nội dung chứng chỉ với 20 kỹ năng con: đánh dấu phần chứng chỉ phủ, phần không phủ. Phần không phủ (thường là kiểm chất lượng AI trên dữ liệu thật của NLH, dữ liệu dùng chung, định hình sản phẩm) học qua việc thật ở lộ trình trên. Lưới năng lực của đội cũng là một cách trình bày năng lực rõ ràng khi làm hồ sơ đối tác.

## Dùng bản đồ ngoài NLH

- **Khoá "Tôi Xây Công Ty Bằng AI".** Học viên là nhà sáng lập, không phải kỹ sư: trọng tâm là kỹ năng 4 và kỹ năng 3, cộng một phiên bản rất gọn của kỹ năng 1.4 (tự chấm 10–20 đầu ra AI của mình) và thẻ từ vựng đánh đổi của kỹ năng 2. Bốn giai đoạn sản phẩm giúp học viên hiểu vì sao hệ thống 30 ngày là "chạy được" chứ chưa phải "chịu tải".
- **Tư vấn cho doanh nghiệp khách.** Lưới người × kỹ năng con dùng được làm bảng chẩn đoán năng lực AI của đội khách trước khi đề xuất gói.
