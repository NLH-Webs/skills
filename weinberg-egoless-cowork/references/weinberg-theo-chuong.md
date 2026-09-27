# Weinberg theo từng chương — tóm ý, áp dụng ở NhiLe, câu hỏi tự soát

Tóm ý bằng lời của Claude (không trích nguyên văn). Sách gồm 5 phần, 13 chương và lời kết. Đọc phần nào cần — không cần đọc hết.

Mục lục
- Phần 1 — Lập trình là việc con người làm: Ch.1 Đọc chương trình · Ch.2 Thế nào là chương trình tốt · Ch.3 Nghiên cứu việc lập trình thế nào
- Phần 2 — Lập trình là hoạt động xã hội: Ch.4 Nhóm · Ch.5 Đội · Ch.6 Dự án
- Phần 3 — Lập trình là hoạt động cá nhân: Ch.7 Các kiểu việc · Ch.8 Tính cách · Ch.9 Khả năng giải quyết vấn đề · Ch.10 Động lực, đào tạo, kinh nghiệm
- Phần 4 — Công cụ: Ch.11 Ngôn ngữ · Ch.12 Nguyên tắc thiết kế ngôn ngữ · Ch.13 Công cụ khác
- Phần 5 — Lời kết: trách nhiệm

---

## Phần 1 — Lập trình là việc con người làm

### Ch.1 Đọc chương trình
**Ý chính.** Ở mọi nghề viết, người ta học bằng cách đọc cả bài hay lẫn bài dở; riêng lập trình thì hầu như không ai đọc bài của người khác. Đọc một chương trình, ta thấy dấu vết của: giới hạn của máy, giới hạn của ngôn ngữ, giới hạn của người viết, những quyết định lịch sử từ thuở ban đầu, và — hiếm khi — sự chuẩn bị cho thay đổi. Cấu trúc của cả chương trình có thể bị quyết định bởi số người và cách chia việc của nhóm viết ra nó. Sách kể trường hợp xích mích giữa người trong đội gây ra lỗi mãi nhiều năm sau mới lộ.
**Ở NhiLe.** Mỗi portal cần một "bản đọc" bằng lời thường: làm gì, dựa vào đâu, chỗ nào tạm, đổi chỗ nào thì gãy chỗ nào. Người đọc bản này là Nhi, người mới trong team, và các phiên Claude sau. Khi kiểm kê nợ cũ, tìm cả những chỗ tồn tại chỉ vì một giới hạn đã không còn.
**Tự soát.** Lần gần nhất có ai (người hoặc một phiên Claude khác) đọc lại phần vừa làm là khi nào? Portal này có chỗ nào chỉ tồn tại vì cách chia việc cũ của team?

### Ch.2 Thế nào là chương trình tốt
**Ý chính.** "Tốt" không có nghĩa chung; chỉ có tốt theo bối cảnh: đáp ứng yêu cầu tới đâu, có đúng hạn không và lịch có dao động nhiều không, có sửa được khi điều kiện đổi không và tốn bao nhiêu, hiệu quả theo nghĩa nào và đang đánh đổi gì. Không chạy thì mọi thứ khác vô nghĩa; trễ thì thường mất giá trị. Gần như mọi chương trình đều bị sửa trong đời, nhưng hiếm cái được viết với ý định sẽ bị sửa. Sách kể thí nghiệm giao cùng một việc với mục tiêu khác nhau: nhóm được bảo "làm cho hiệu quả" tốn thời gian gấp mấy lần nhưng chương trình tiết kiệm tài nguyên hơn hẳn — người làm tối ưu đúng cái họ được bảo. Ta không tìm chương trình tốt nhất, mà tìm cái đáp ứng yêu cầu. Yêu cầu lớn lên cùng chương trình; làm phần mềm là quá trình học của cả hai phía.
**Ở NhiLe.** Mục B trong SKILL.md: chốt thứ tự Đúng / Kịp / Đổi được / Hiệu quả trước mỗi khối, và nói ra. Chấp nhận yêu cầu đổi sau khi Nhi bấm thử là một phần của quy trình, không phải "đổi ý".
**Tự soát.** Khối này đang tối ưu cái gì — và có ai nói ra điều đó chưa? Nếu mai thêm một vai trò hay một trường học, phần nào phải viết lại?

### Ch.3 Nghiên cứu việc lập trình thế nào
**Ý chính.** Quan sát người làm việc thì chính sự quan sát làm họ đổi cách làm. Thí nghiệm trên sinh viên không nói được nhiều về người làm nghề thật. Đo được chưa phải là biết; biết nên đo cái gì mới là biết.
**Ở NhiLe.** Khi đo team, đo AI, hay làm số liệu cho bài học SMU: đo cái gì thì người ta sẽ làm đẹp cái đó. Chọn thước đo gắn với kết quả cho người dùng (xem "Đo khi không đọc được code" trong SKILL.md), không gắn với hoạt động.
**Tự soát.** Nếu team biết mình được đo bằng chỉ số này, họ sẽ làm gì khác đi? Điều đó có tốt cho người dùng không?

## Phần 2 — Lập trình là hoạt động xã hội

### Ch.4 Nhóm
**Ý chính.** Phần lớn việc học và gỡ rối diễn ra trong nhóm không chính thức. Sách kể chuyện dời một góc nước uống đi cho gọn, và thế là mất luôn chỗ mọi người tình cờ hỏi nhau — việc chậm hẳn. Con người khó thấy lỗi trong bài của chính mình vì muốn giữ hình ảnh bản thân nhất quán (bất hòa nhận thức); cách chữa là lập trình không cái tôi — coi sản phẩm là của đội và chủ động mời người khác soát. Môi trường làm việc (chỗ ngồi, vách ngăn, tiếng ồn) ảnh hưởng tới năng suất nhiều hơn người ta nghĩ.
**Ở NhiLe.** Team chia giữa Việt Nam và Singapore cần một "góc nước uống" có chủ đích: kênh chung, file chung, nơi người ta hỏi nhau mà không qua Nhi. Soát không cái tôi áp cho cả Claude: tự nêu chỗ yếu, mời vòng soát khác bên.
**Tự soát.** Trong team, người ta hay hỏi nhau ở đâu? Nếu chỗ đó biến mất thì sao? Ai là người duy nhất đang soát bài của người khác?

### Ch.5 Đội
**Ý chính.** Đội thành hình khi có mục tiêu mà mọi người thật sự chấp nhận. Lãnh đạo là ảnh hưởng, và nó chuyển từ người này sang người khác tùy việc. Đội kiểu dân chủ — người giỏi phần nào dẫn phần đó — thường bền hơn kiểu phân cấp; Weinberg chỉ ra mô hình phân cấp đến từ quân đội thế kỷ 19, không phải từ quan sát những hệ thống chạy tốt. Đội cần cả người dẫn việc lẫn người giữ nhịp quan hệ. Khi khủng hoảng, đội hay quay về phân cấp. Nên chọn người vì kỹ năng làm việc với người khác ngang với kỹ năng chuyên môn.
**Ở NhiLe.** Chia mũ theo việc, để người giỏi phần nào dẫn phần đó. Khi tuyển hay ghép đội, nhìn cả cách họ phối hợp chứ không chỉ bài kiểm tra kỹ thuật.
**Tự soát.** Mục tiêu của khối này đã được cả đội chấp nhận, hay chỉ được giao xuống? Ai đang giữ nhịp đội?

### Ch.6 Dự án
**Ý chính.** Dự án lớn tốn sức phối hợp: thêm người không cộng thẳng ra thêm việc. Người không thể thay thế là rủi ro — Weinberg khuyên người quản lý xử lý tình trạng đó càng sớm càng tốt, vì ai rồi cũng có lúc ốm, nghỉ hay rời đi. Người quản lý phụ trách việc mình không hiểu sẽ thưởng cho vẻ bề ngoài: ai đến sớm, ai trông bận. Tổ chức nhiều tầng làm thông tin méo dần khi đi lên đi xuống. Ước lượng trung thực quý hơn ước lượng đẹp.
**Ở NhiLe.** Biến tri thức trong đầu một người (và trong một cuộc chat) thành file mà người khác đọc được. Nhi là người không đọc code nên càng cần thước đo nhìn/bấm được để tránh bẫy "vẻ bề ngoài".
**Tự soát.** Nếu người nắm phần này nghỉ một tuần, việc gì dừng? Mình đang khen ai vì kết quả, và khen ai vì trông có vẻ chăm?

## Phần 3 — Lập trình là hoạt động cá nhân

### Ch.7 Các kiểu việc
**Ý chính.** "Lập trình" gồm nhiều việc khác hẳn nhau — phân tích, thiết kế, viết, kiểm thử — mỗi việc cần một kiểu năng lực. Người nghiệp dư học về *vấn đề* của mình, lập trình chỉ là phương tiện; người nhà nghề học về *nghề*, còn vấn đề chỉ là một bước trong sự phát triển của họ. Phần lớn chênh lệch giữa những người làm cùng một việc đến từ cách họ hiểu việc phải làm.
**Ở NhiLe.** Đây là nền của pipeline nhiều mũ. Nhi ở phía "người hiểu vấn đề" — một vị trí có giá trị, không phải điểm yếu; Claude và team đứng phía nhà nghề. Nối hai phía bằng câu đích rõ ràng.
**Tự soát.** Việc này đang cần kiểu năng lực nào — và người (hay mũ) đang làm có đúng kiểu đó không? Mọi người có cùng hiểu "xong" nghĩa là gì không?

### Ch.8 Tính cách
**Ý chính.** Không có một "tính cách lập trình viên". Vài đặc điểm có vẻ quan trọng: chịu được áp lực, thích nghi với thay đổi nhanh, cẩn thận chính xác, khiêm tốn đủ để thấy lỗi mình, đủ vững để bảo vệ điều đúng, và óc hài hước. Các bài trắc nghiệm tính cách dự đoán hiệu quả công việc rất kém.
**Ở NhiLe.** Khi chọn người, nhìn cách họ làm trong việc thật (thử việc, một khối nhỏ có thật) hơn là trắc nghiệm. Nếu dùng hồ sơ tính cách — kể cả các hệ thống hồ sơ của NhiLe — coi đó là gợi ý để hiểu người và ghép đội, không phải căn cứ tuyển hay loại. Với Claude, "khiêm tốn" nghĩa là tự nêu chỗ chưa chắc; "vững" nghĩa là dám dừng Nhi lại khi cần.
**Tự soát.** Quyết định về người này dựa trên việc họ đã làm, hay dựa trên hình dung về họ?

### Ch.9 Khả năng giải quyết vấn đề
**Ý chính.** Chỉ số thông minh nói rất ít về khả năng làm phần mềm. Điều quan trọng là cách giải: nhận ra đúng vấn đề, thoát khỏi lối mòn khi bị kẹt, biết lúc nào nên tạm dừng hay nhờ người. Bài khó thường vì bỏ sót một yếu tố; khi đã biết yếu tố đó thì lời giải trông hiển nhiên, người sau không hiểu nổi vì sao người trước kẹt — và chính người trước cũng bắt đầu nghi ngờ mình. Cũng đừng tin quá những lời giải thích thành công nghe hợp lý sau khi sự đã rồi.
**Ở NhiLe.** Mục "Khi bị kẹt hoặc bị loạn" trong SKILL.md. Mỗi lần gỡ được, ghi yếu tố bị bỏ sót vào ghi chú bàn giao — đó là tài sản học tập của team.
**Tự soát.** Chúng ta đang bỏ sót yếu tố nào? Đã thử nhìn từ phía người dùng, phía dữ liệu, phía người vận hành chưa?

### Ch.10 Động lực, đào tạo, kinh nghiệm
**Ý chính.** Hai đòn bẩy lớn lên hiệu suất là muốn làm (động lực) và biết cách làm (đào tạo). Tiền hiếm khi đủ để giữ người giỏi. Học nhanh nhất khi có phản hồi nhanh về việc mình làm tốt hay dở; không có phản hồi thì người ta tự thử hệ thống bằng các biến tấu. Kinh nghiệm chỉ có giá trị khi có phản hồi và suy ngẫm, không chỉ là số năm. Học bằng đọc bài của người khác và bằng làm việc thật.
**Ở NhiLe.** Phản hồi cho team gắn với sản phẩm cụ thể và đến sớm. Người mới học từ ghi chú bàn giao và bản đọc hệ thống. Với khóa dạy doanh nhân xây hệ thống AI: cho học viên "đọc" một hệ thống thật đã chạy trước khi tự xây — đúng lời khuyên học viết bằng cách đọc.
**Tự soát.** Người này lần cuối nhận phản hồi rõ ràng về việc của mình là khi nào? Họ học từ đâu ngoài việc tự làm?

## Phần 4 — Công cụ

### Ch.11 Ngôn ngữ
**Ý chính.** Con người không nghĩ như máy — đó là lý do ta dùng máy. Ngôn ngữ lập trình là cầu nối để giúp phía con người, vì máy thì chẳng bao giờ than. Nếu người làm hoàn hảo thì chẳng cần ngôn ngữ trung gian; ngôn ngữ tồn tại vì giới hạn của đầu người. Lỗi hay nảy sinh ở chỗ ngôn ngữ khiến người ta kỳ vọng một đằng, máy làm một nẻo.
**Ở NhiLe.** Master prompt, file bàn giao, tên gọi là "ngôn ngữ" giữa Nhi, team và Claude — thiết kế nó cho đầu người đọc, không cho máy.
**Tự soát.** Người mới đọc master prompt này có hiểu đúng ý Nhi không, hay phải hỏi lại?

### Ch.12 Nguyên tắc thiết kế ngôn ngữ
**Ý chính.** Đầu người chỉ giữ được một ít thông tin cùng lúc, nên ngôn ngữ tốt cần: đồng nhất (một thứ luôn mang một nghĩa, một cách viết), gọn (ít khái niệm), gần (thứ liên quan nằm cạnh nhau), thẳng (đọc một mạch). Sao chép cùng một thứ ra nhiều chỗ dễ sinh lỗi vì sửa một chỗ quên chỗ kia — nên gom về một nơi dùng chung.
**Ở NhiLe.** Từ điển chung cho tên gọi; bộ giao diện dùng chung cho mọi portal; một bộ não dữ liệu chung thay vì mỗi portal một bản sao.
**Tự soát.** Có thứ nào đang mang hai tên? Có thứ nào đang được sao chép ở nhiều portal thay vì dùng chung?

### Ch.13 Công cụ khác
**Ý chính.** Phần lớn nội dung đã lỗi thời (thẻ đục lỗ, xếp hàng chờ máy). Ý còn giữ: công cụ gỡ lỗi, kiểm thử, môi trường làm việc phải được thiết kế theo con người dùng nó; công cụ tốt làm ngắn vòng từ lúc làm tới lúc thấy kết quả.
**Ở NhiLe.** Với người không đọc code, công cụ quan trọng nhất là **bản xem thử bấm được** — vòng từ "Claude làm" tới "Nhi thấy" càng ngắn thì càng học nhanh.
**Tự soát.** Từ lúc làm xong tới lúc Nhi bấm thử được mất bao lâu? Có rút ngắn được không?

## Phần 5 — Lời kết: trách nhiệm
**Ý chính.** Máy tính khuếch đại ý định của người dùng nó — tốt hay xấu. Nó có thể dùng để giúp con người sống tốt hơn, hoặc để theo dõi và khống chế họ. Người làm ra phần mềm không đứng ngoài trách nhiệm đó.
**Ở NhiLe.** Hệ thống giữ hồ sơ, hành vi và dữ liệu cá nhân sâu của học viên, cộng đồng. Mỗi tính năng đụng tới dữ liệu người cần trả lời: giúp người dùng tốt lên hay chỉ giúp mình khai thác họ; ai thấy dữ liệu, dùng vào đâu, người dùng có biết không.
**Tự soát.** Nếu người dùng thấy toàn bộ cách mình dùng dữ liệu của họ, họ có thấy ổn không?
