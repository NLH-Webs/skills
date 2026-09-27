# Bản đồ chi tiết — 4 kỹ năng, 20 kỹ năng con, nghĩa ở NLH

Tóm bằng lời của Claude từ các thư của Andrew Ng trên The Batch (14/08 – 25/09/2026). Mỗi kỹ năng con gồm: Ng nói gì · Ở NLH nghĩa là gì · Dấu hiệu đang hổng.

Mục lục: Kỹ năng 1 (6 kỹ năng con) · Kỹ năng 2 (5) · Kỹ năng 3 (5 + quy trình) · Kỹ năng 4 (4) · Nền: học liên tục

---

## Kỹ năng 1 — Xây và vận hành ứng dụng AI

Khác biệt gốc: phần mềm thường chạy đoán trước được, còn AI thì không — hỏi cùng một câu có thể ra câu trả lời khác. Mọi kỹ năng con dưới đây là để đo, lái và kiểm soát sự khó đoán đó.

### 1.1 Hiểu mô hình ngôn ngữ
**Ng nói.** Hiểu mô hình đọc đầu vào và sinh đầu ra ra sao để biết khi nào tin được, khi nào nó dễ sai: chọn mô hình đọc được ảnh hay chỉ chữ, cân nhắc nhồi gì vào phần nó được đọc, mốc kiến thức, mức suy nghĩ, gọi công cụ. Từ đó chọn đúng mô hình hoặc kết hợp nhiều mô hình, và biết khi nào cần tinh chỉnh riêng hay tự chạy mô hình.
**Ở NLH.** Chọn mô hình nào cho việc nào: việc cần gu và độ sâu (hồ sơ, nội dung) khác việc lặp lại số lượng lớn (phân loại lead) — dùng mô hình rẻ cho việc lặp, mô hình mạnh cho việc cần phán đoán.
**Dấu hiệu hổng.** Dùng một mô hình đắt cho mọi việc; hoặc ngạc nhiên khi AI "không biết" chuyện mới xảy ra.

### 1.2 Cho mô hình đúng dữ liệu
**Ng nói.** AI cần bối cảnh tốt mới cho kết quả tốt. Quyết định cái gì đưa thẳng vào lời nhắc, cái gì để mô hình tự tra khi cần; chọn cách lưu hợp với kiểu dữ liệu (chỉ mục tìm theo nghĩa, đồ thị quan hệ, lớp diễn giải trên dữ liệu bảng); và xây đường ống biến tài liệu (chữ, PDF, trang web, ảnh) thành dữ liệu sạch, luôn mới.
**Ở NLH.** Kho tri thức BaZi và các hệ thống khác, tài liệu khoá học, lịch sử học viên — cần quyết định phần nào luôn nằm sẵn trong lời nhắc, phần nào tra theo từng người. Dữ liệu cũ, bẩn làm AI sai mà không báo.
**Dấu hiệu hổng.** Dán cả kho tài liệu vào mỗi lần hỏi; không ai chịu trách nhiệm cập nhật dữ liệu nguồn.

### 1.3 Xây hệ thống agent
**Ng nói.** Có một dải từ quy trình cố định (các bước gọi AI theo thứ tự định sẵn) tới agent tự quyết bước tiếp theo. Phải chọn điểm trên dải đó, bước nào dùng code, bước nào dùng AI, có đường lùi khi lỗi; chọn công cụ cho agent, cách nhớ, cách giữ bối cảnh qua phiên dài, khi nào cần nhiều agent phối hợp. Đưa lên dùng thật cần hàng rào an toàn, chống đầu vào cố tình phá, chống rò dữ liệu, và quản trị.
**Ở NLH.** Chuỗi Prompt A → B → C → D của hồ sơ là một quy trình cố định — hợp lý vì dễ kiểm. Bot trợ lý là agent — cần hàng rào chặt hơn.
**Dấu hiệu hổng.** Dùng agent tự do cho việc lẽ ra chỉ cần vài bước cố định; hoặc agent có quyền làm quá nhiều mà không có giới hạn.

### 1.4 Phát triển dựa trên kiểm chất lượng (quan trọng nhất)
**Ng nói.** Đây là thứ phân biệt người giỏi: dẫn dắt được vòng kiểm chất lượng và soi lỗi có kỷ luật. Gồm: xem dữ liệu để hiểu cái gì đang sai trước khi đặt thước đo, chọn đo cái gì, chọn chấm bằng luật máy, bằng AI chấm, hay bằng người, và chấm lại chính bộ chấm theo thời gian.
**Ở NLH.** Mọi tính năng AI (hồ sơ, phân loại lead, bot, ghép cặp) cần một bảng ca thử và tiêu chí do Nhi chấm mẫu. Xem mục 3 trong SKILL.md.
**Dấu hiệu hổng.** Sửa prompt rồi nhìn một ví dụ thấy "ổn hơn" là xong; không ai biết lần sửa trước làm tốt lên hay xấu đi.

### 1.5 Vận hành AI khi đã có người dùng
**Ng nói.** AI khác phần mềm thường ở độ khó đoán, chi phí và độ trễ. Cần theo dõi hiệu suất, phát hiện khi hành vi mô hình trôi dần, xử lý sự cố và tấn công bằng lời nhắc độc, kiểm hồi quy trước mỗi lần cập nhật theo mức rủi ro, và chọn đòn bẩy đúng để giảm chi phí và độ trễ (đổi mô hình, rút gọn quy trình, tinh chỉnh).
**Ở NLH.** Khi nhà cung cấp đổi phiên bản mô hình, hồ sơ có thể đổi giọng mà không ai hay — cần bộ ca để chạy lại. Theo dõi tiền gọi AI mỗi tháng theo từng tính năng.
**Dấu hiệu hổng.** Không biết tháng này tốn bao nhiêu cho AI, cho tính năng nào; phát hiện lỗi qua lời phàn nàn của học viên.

### 1.6 Nền tảng học máy
**Ng nói.** Mô hình hiện đại được xây bằng các kỹ thuật học máy; kể cả khi chỉ dùng mô hình của người khác, các khung nghĩ như cân bằng giữa học vẹt và học quá chung, soi lỗi, và chăm chút dữ liệu vẫn còn nguyên giá trị.
**Ở NLH.** Khi muốn dự đoán (học viên nào sắp bỏ học, lead nào sắp chốt) từ dữ liệu hành vi, cần người hiểu nền này — không phải lúc nào cũng giải bằng lời nhắc.
**Dấu hiệu hổng.** Mọi bài toán đều cố giải bằng cách viết lời nhắc dài hơn.

---

## Kỹ năng 2 — Nền tảng kỹ thuật phần mềm

Ng: người hiểu sâu phần mềm chạy thế nào làm tốt hơn hẳn người làm theo cảm hứng mà không hiểu. Agent tối ưu theo cái nó được bảo; nền tảng là cách nói đúng điều cần giữ. Agent cũng kéo mọi người về phía biết cả trước lẫn sau (giao diện lẫn máy chủ).

### 2.1 Xây ứng dụng đủ tầng
**Ng nói.** Hiểu các phần: thành phần giao diện, lưu tạm để nhanh, cách hiển thị trang, thiết kế cổng giao tiếp giữa các phần, đăng nhập, quản lý phiên, xử lý chạy ngầm, lưu trữ, kiểm thử, bảo mật, khả năng tiếp cận cho người khuyết tật.
**Ở NLH.** Khi một trang chậm, phải biết lỗi nằm ở tầng nào để chỉ đúng chỗ cho agent. Đăng nhập một lần cho mọi portal là quyết định tầng này.
**Dấu hiệu hổng.** "Chậm thì bảo agent làm nhanh lên" mà không biết chậm ở đâu.

### 2.2 Quản lý dữ liệu (khó sửa nhất nếu sai)
**Ng nói.** Bắt đầu từ cách dữ liệu sẽ được đọc và ghi; từ đó chọn lưu gì, dạng nào, bao lâu, kiểu kho nào; lo giao dịch, nhiều người ghi cùng lúc, sạch, khớp, mới; lo riêng tư, quản trị, tuân thủ; và biết cho cấu trúc dữ liệu lớn lên. Chọn sai thì AI không biết là mình không biết.
**Ở NLH.** Đây là "bộ não nội bộ" — tầng phải bền nhất trong tầm nhìn dài hạn. Dữ liệu hồ sơ và hành vi học viên còn là dữ liệu nhạy cảm.
**Dấu hiệu hổng.** Mỗi portal tự tạo bảng riêng cho cùng một khái niệm (học viên, khoá, lớp); con số ở hai nơi không khớp.

### 2.3 Thiết kế kiến trúc hệ thống
**Ng nói.** Kiến trúc do yêu cầu quyết định (bao nhiêu người dùng, cần nhanh tới đâu, trần chi phí), không do sở thích: chọn nền tảng, ranh giới trước–sau, chia hệ thống thành phần, đặt trạng thái ở đâu, gộp một khối hay tách nhỏ, chọn công nghệ bằng thử nghiệm. Kiến trúc đúng thay đổi theo giai đoạn.
**Ở NLH.** Chín portal cùng dựa vào một lớp dữ liệu và quyền — đây là quyết định kiến trúc lớn nhất; giao diện từng portal có thể đổi tự do.
**Dấu hiệu hổng.** Chọn công nghệ vì "nghe nói tốt"; hoặc đập đi làm lại kiến trúc khi sản phẩm còn chưa có người dùng.

### 2.4 An toàn và bền bỉ
**Ng nói.** Chọn tỉ lệ kiểm thử phù hợp rủi ro; thiết kế cho lúc hỏng (giới hạn tần suất, xuống cấp nhẹ nhàng thay vì sập hẳn, khoanh vùng thiệt hại); đưa bảo mật vào sớm; dùng AI quét lỗ hổng nhưng vẫn cần người hiểu bảo mật để hành động.
**Ở NLH.** Một portal hỏng không được kéo sập cả hệ; dữ liệu học viên phải có sao lưu và phân quyền theo vai trò.
**Dấu hiệu hổng.** Chưa từng thử khôi phục từ bản sao lưu; ai cũng có quyền quản trị.

### 2.5 Mở rộng và vận hành
**Ng nói.** Vòng đời phát triển, cấu hình môi trường, chiến lược phát hành, cổng kiểm tự động trước khi lên bản thật, hạ tầng thuê ngoài, theo dõi có cảnh báo và xử lý sự cố, các kỹ thuật chịu tải, quản lý phiên bản, soát code, cập nhật thư viện và trả nợ kỹ thuật.
**Ở NLH.** Mỗi portal có bản xem thử trước bản thật; có người nhận cảnh báo khi lỗi; định kỳ dọn nợ cũ.
**Dấu hiệu hổng.** Sửa thẳng trên bản thật; lỗi chỉ được biết khi Nhi tự bấm thấy.

---

## Kỹ năng 3 — Dùng coding agent

Phần này tiến bộ nhanh nhất trong bốn kỹ năng. Quy trình nền: **lên kế hoạch** (tìm hiểu, viết bản mô tả gồm yêu cầu, thiết kế kỹ thuật, kiến trúc, rồi lập kế hoạch thực hiện và soát nó) → **thực hiện** (xây, kiểm, xác minh, cân giữa tự chủ của agent và giám sát của người) → **đưa lên và theo dõi** (có cổng chặn, cho agent đọc nhật ký, phát hiện vấn đề, đề xuất cải tiến). Việc mới hoàn toàn thì bản mô tả có thể sơ; việc sửa trên hệ thống cũ thì cần chặt.

### 3.1 Lái quy trình
**Ng nói.** Quyết định mỗi bước cần bao nhiêu công người, bao nhiêu công agent; khi nào quay lại bước trước; cân tốc độ, chi phí, rủi ro, công sức.
**Ở NLH.** Người lái là người nắm khối việc trong team (không phải Nhi). Phản hồi khi Nhi bấm thử thường buộc quay về mũ 1–3 — đó là bình thường.
**Dấu hiệu hổng.** Đi thẳng một chiều qua 7 mũ dù bước sau đã lộ ra lỗi ở bước trước.

### 3.2 Cho agent tự chủ đúng mức
**Ng nói.** Chọn mức tự chủ theo việc (hỏi-đáp, giao một khối lớn, chạy tới khi đạt), quản lý bối cảnh qua các giai đoạn, biết khi nào chạy song song nhiều agent, quản lý sự chú ý của người khi có nhiều phiên cùng lúc, và chạy an toàn với quyền hạn và cổng chặn để tránh rò rỉ, mất dữ liệu, gây hại.
**Ở NLH.** Agent làm trên bản xem thử; không có quyền ghi vào dữ liệu thật của học viên nếu không qua cổng; một người không trông quá nhiều phiên cùng lúc.
**Dấu hiệu hổng.** Agent từng xoá hoặc ghi đè dữ liệu thật; người trông năm phiên cùng lúc và không soát kỹ phiên nào.

### 3.3 Soát bài
**Ng nói.** Thiết kế kiểm tra hợp với việc (hành vi lẫn chức năng), bắt agent nộp ảnh chụp làm bằng chứng, dùng bộ ca và AI chấm cho phần cần gu, quyết định soát tự động tới đâu, dùng agent soát code và kiểm bảo mật, kiến trúc, chèn người soát ở chỗ đáng, và xác minh sau khi đưa lên.
**Ở NLH.** Mũ QA không chỉ "bấm thử thấy được" mà có danh sách kịch bản người dùng thật để chạy lại mỗi lần.
**Dấu hiệu hổng.** Agent báo "xong" và được tin ngay.

### 3.4 Chỉnh agent và môi trường
**Ng nói.** Gắn skill, plugin, kết nối, và dọn bớt khi lỗi thời; dùng móc tự động cho các bước lặp; giữ file bối cảnh thường trực (Ng gọi tên AGENTS.md và CLAUDE.md) ghi thông tin mã nguồn, kiến trúc, phong cách, cách truy cập dữ liệu; giữ trạng thái giữa các phiên và các agent; rút bài học sau mỗi lượt chạy; đặt quy ước để agent dễ tìm đường trong mã; phối hợp bối cảnh giữa các agent của cả đội.
**Ở NLH.** Mỗi repo có CLAUDE.md và ghi chú bàn giao; skill trùng nhau (hai phiên bản của cùng một skill, nhiều file nói cùng một thứ) cần gộp hoặc tắt bớt.
**Dấu hiệu hổng.** Mỗi phiên mới phải giải thích lại từ đầu; agent dùng nhầm skill cũ.

### 3.5 Hiểu agent chạy thế nào
**Ng nói.** Hiểu agent tìm trong mã nguồn ra sao, quản lý phần được đọc thế nào, thêm công cụ ảnh hưởng tới bối cảnh ra sao, agent và agent con tương tác thế nào, agent được dựng bằng cách bọc một khung điều khiển quanh mô hình. Hiểu để nhận ra các kiểu hỏng: làm quá tay, mất chặt chẽ khi không có bước tự kiểm, dừng giữa chừng, làm việc phá huỷ.
**Ở NLH.** Team IT cần hiểu tới mức này; Nhi chỉ cần biết bốn kiểu hỏng để nhận ra.
**Dấu hiệu hổng.** Ngạc nhiên khi gắn thêm nhiều kết nối thì agent làm kém đi.

---

## Kỹ năng 4 — Định hình thứ được xây

Ng: trước đây người làm sản phẩm và người thiết kế quyết định làm gì, lập trình viên làm theo. Nay vai trò mờ đi; người biết định hình không phải chờ ai quyết từng việc.

### 4.1 Lái vòng xây
**Ng nói.** Phần mềm được xây qua vòng: làm một ít → lấy phản hồi → quyết bước tiếp. Người giỏi nghiêng về hành động, làm từng mẻ nhỏ, biết lúc nào làm bản thử để thử một ý, lúc nào làm MVP đưa người dùng, lúc nào đầu tư hệ thống cấp doanh nghiệp; biết lúc nào hỏi người dùng, lúc nào chạy thử nghiệm kỹ thuật; quyết dựa trên tầm nhìn, giai đoạn, khả thi, rủi ro, công sức, ngân sách. Dự án trưởng thành thì biết đặt chỉ số chính và quản lý để cải thiện chúng.
**Ở NLH.** Khớp với cách Nhi làm ngược từ đích. Team cần học làm mẻ nhỏ thay vì gom một bản lớn.
**Dấu hiệu hổng.** Làm mấy tuần mới cho người dùng thấy.

### 4.2 Ra quyết định sản phẩm
**Ng nói.** Không cần thành người làm sản phẩm, nhưng sẽ phải quyết những điều bản mô tả không nói; không có bản mô tả thì tự viết được. Cần cảm quan sản phẩm, cảm quan thiết kế cơ bản, cảm quan kinh doanh cơ bản (đưa ra thị trường, quy mô thị trường, lãi lỗ trên mỗi đơn vị); tất cả bắt rễ từ thấu hiểu người dùng, được mài liên tục bằng phỏng vấn nhanh 2–3 người, khảo sát hàng trăm người, thử A/B, phân tích hành vi số đông.
**Ở NLH.** Thế mạnh của Nhi. Team học bằng cách ngồi nghe học viên và đọc "vì sao" trong PRD.
**Dấu hiệu hổng.** Dev hỏi Nhi từng quyết định nhỏ mà bản mô tả không ghi.

### 4.3 Giao tiếp và dẫn dắt
**Ng nói.** Kỹ năng AI mở rộng phạm vi sang marketing, tài chính, pháp lý…; nên phải biết nói chuyện, căn chỉnh và điều phối các bên. Người hiểu AI còn có vai trò giúp người ngoài ngành hiểu cái gì khả thi, cái gì không, để dẫn tổ chức đi tới.
**Ở NLH.** Người trong team IT biết giải thích cho đội vận hành, marketing, kế toán bằng lời thường — đúng tinh thần cả tổ chức cùng chuyển đổi.
**Dấu hiệu hổng.** Mọi trao đổi giữa IT và các đội khác đều phải qua Nhi.

### 4.4 Nhận việc tới cùng
**Ng nói.** Nhiều người, kể cả lãnh đạo, chưa hiểu AI làm được gì nên chưa biết hướng nào tốt; người có kỹ năng lấp khoảng trống đó: tự thấy vấn đề, đề xuất, làm — tôn trọng ưu tiên của tổ chức nhưng không chờ chỉ đạo từng chi tiết. Nhận một việc từ đầu tới cuối, chịu trách nhiệm khi có sự cố, hành động khi chưa rõ, bền bỉ qua thất bại, đo mình bằng giá trị tạo ra chứ không bằng số việc đã tick.
**Ở NLH.** Đây là thứ giúp giảm việc Nhi phải phân luồng bằng đầu mình.
**Dấu hiệu hổng.** Báo cáo "đã làm xong task" nhưng không ai nói được người dùng được gì.

---

## Nền: học liên tục
**Ng nói.** Theo dõi mặt trận công nghệ, thử công cụ mới, chỉnh quy trình, học mãi. Ông cảnh báo: người từ công ty lớn sang startup hay đòi quy trình quá chậm, người từ startup sang công ty lớn hay đụng trần vì chỉ quen cách nhanh mà kém chính xác — nên học cả hai.
**Ở NLH.** Đội vừa làm sản phẩm mới (giai đoạn 0–1) vừa giữ sản phẩm đang chạy (giai đoạn 2) — chính là cơ hội học cả hai nhịp.
