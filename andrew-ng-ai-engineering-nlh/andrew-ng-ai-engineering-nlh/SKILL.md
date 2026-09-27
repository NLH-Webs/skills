---
name: andrew-ng-ai-engineering-nlh
description: "Áp Bản đồ kỹ năng AI Engineering của Andrew Ng (DeepLearning.AI, 08–09/2026) vào NhiLe Holdings: chia bốn nhóm kỹ năng giữa Nhi, Claude và team IT; xác định mỗi sản phẩm đang ở giai đoạn nào để làm nhanh hay làm chắc; dựng bài kiểm chất lượng (eval) cho các tính năng AI như hồ sơ, phân loại lead, bot; nói các đánh đổi kỹ thuật bằng lời thường để Nhi lái được agent; đối chiếu quy trình 7 mũ với cách dùng coding agent của Ng; chấm năng lực, tuyển và đào tạo team. Dùng khi Nhi nhắc Andrew Ng, bản đồ kỹ năng, AI engineering, “team IT cần giỏi gì”, “tuyển dev”, “đào tạo đội”, “chứng chỉ Claude”, “đánh giá năng lực”, “tính năng AI chạy đúng không”, “đo chất lượng AI”, “eval”, “làm nhanh hay làm kỹ”, “MVP hay làm chắc”, “sản phẩm này tới đâu rồi”, “vibe code”, “agent làm hỏng”, “chọn kiến trúc”, “dữ liệu dùng chung”, hoặc khi sắp thêm AI vào một portal. Chạy kèm weinberg-egoless-cowork (lớp con người) và nhile-pm-designer (file mũ 1–3)."
---

# Andrew Ng — Bản đồ kỹ năng AI Engineering, áp cho NhiLe Holdings

Nguồn: chuỗi thư của Andrew Ng trên The Batch (DeepLearning.AI), từ 14/08 đến 25/09/2026. Bản đồ được tổng hợp từ việc phân tích hơn 10.000 tin tuyển dụng, hàng chục cuộc phỏng vấn chuyên gia, nhà tuyển dụng, cùng dữ liệu khảo sát. Ng nói rõ đây là kỹ năng mà **mọi** người làm phần mềm đều cần, không chỉ người mang chức danh "kỹ sư AI" — giống như ai làm phần mềm cũng phải biết dùng điện toán đám mây.

## Vì sao NLH cần bản đồ này

NLH đang xây nhiều portal với ít người, dùng Claude làm phần lớn việc viết. Bản đồ của Ng trả lời ba câu Nhi đang cần:
1. **Ai giữ kỹ năng nào** — Nhi, Claude và team IT, để đội nhỏ mà không hổng chỗ nào.
2. **Làm nhanh hay làm chắc** — tuỳ sản phẩm đang ở giai đoạn nào (Ng gọi đây là một trong những điều khó học nhất nhưng quan trọng nhất).
3. **Tính năng AI có chạy đúng không** — vì AI không trả lời giống nhau mỗi lần, cần một cách đo có kỷ luật.

## Bốn nhóm kỹ năng, bằng lời thường

| # | Kỹ năng (Ng) | Nói gọn | Ở NLH |
|---|---|---|---|
| 1 | **Xây và vận hành ứng dụng AI** | AI không cho kết quả đoán trước được; người giỏi biết đo, lái và kiểm soát nó cho ổn định. Cốt lõi: vòng **kiểm chất lượng + soi lỗi** có kỷ luật | Hồ sơ năm hệ thống, phân loại lead ở Marketing Hub, bot trợ lý, ghép cặp N-ơi, các tính năng AI trong Learn/Instructor |
| 2 | **Nền tảng kỹ thuật phần mềm** | Hiểu phần mềm chạy thế nào để thấy có những **đánh đổi** nào (nhanh, rẻ, chắc, an toàn…) và chỉ đường cho agent bằng đúng ngôn ngữ | Bộ não dữ liệu dùng chung, cách các portal nối nhau, quyền theo vai trò, bảo mật dữ liệu học viên |
| 3 | **Dùng coding agent** | Biết agent làm được gì, yếu ở đâu, khi nào can thiệp, khi nào để nó tự chạy; cho nó cách **tự kiểm** bài mình | Quy trình 7 mũ chạy trong Claude Code / Cowork |
| 4 | **Định hình thứ được xây** | Agent ngày càng giỏi làm đúng bản mô tả, nên việc quý nhất chuyển sang **quyết định bản mô tả có gì**: hiểu người dùng, hiểu kinh doanh, lái vòng xây, dám nhận việc tới cùng | Thế mạnh tự nhiên của Nhi — và kỹ năng team cần học thêm |

Nền dưới cả bốn: **học liên tục**, vì công cụ đổi hằng tháng.

Chi tiết từng kỹ năng con (6 + 5 + 5 + 4) kèm nghĩa ở NLH: đọc `references/ban-do-chi-tiet.md`. Thang chấm năng lực, bài thử việc, lộ trình đào tạo: đọc `references/cham-nang-luc-team.md`.

## 1. Ai giữ kỹ năng nào ở NLH

Ng nhận xét ranh giới giữa người làm sản phẩm, người thiết kế và lập trình viên đang mờ đi: dev phải biết định hình sản phẩm, còn người làm sản phẩm cũng đang học xây. Với NLH, chia như sau:

- **Nhi — chủ của kỹ năng 4.** Hiểu người dùng tới gốc, biết kinh doanh, nói chuyện và dẫn dắt, dám nhận việc tới cùng — đúng bốn kỹ năng con của "định hình thứ được xây". Hai chỗ cần bù: (a) **từ vựng đánh đổi** của kỹ năng 2 — không cần viết code, nhưng cần biết có những đánh đổi nào để lái agent; (b) **làm giám khảo** trong vòng kiểm chất lượng của kỹ năng 1 — Nhi là người có gu nhất để chấm đầu ra AI đúng hay sai.
- **Claude (agent) — làm phần lớn việc tay của kỹ năng 2 và 3**, nhưng có những điểm yếu Ng gọi tên: làm quá tay, thiếu chặt chẽ khi không ai bắt tự kiểm, dừng giữa chừng, và có thể làm những việc phá huỷ. Về dữ liệu, Ng nói thẳng: chọn sai cách tổ chức dữ liệu thì AI không biết là mình không biết. Vì vậy Claude phải **nói ra đánh đổi** ở mỗi điểm quyết định và không bao giờ tự quyết cấu trúc dữ liệu dùng chung một mình.
- **Team IT — chủ của kỹ năng 3, người soát kỹ năng 2, người vận hành kỹ năng 1.** Ít nhất một người phải đủ nền tảng để soát lại đánh đổi agent đã chọn; mọi người đều phải biết giao việc cho agent kèm cách tự kiểm. Team cũng cần học dần kỹ năng 4 (ngồi nghe học viên, hiểu vì sao làm) để không chỉ chờ lệnh.

Phép thử đội hình: với mỗi kỹ năng con quan trọng, có ít nhất **một người thật** (không chỉ Claude) đạt mức "tự làm được" chưa? Chỗ nào trống là chỗ phải tuyển hoặc đào tạo trước.

## 2. Sản phẩm đang ở giai đoạn nào — làm nhanh hay làm chắc

Ng coi việc chọn cách làm theo giai đoạn dự án là một trong những kỹ năng khó nhất: làm quá kỹ lúc đầu là phí, làm quá sơ sài khi sản phẩm đã lớn là tự đụng trần. Chính sách "mọi thứ phải kiểm đủ kiểu mới được đưa lên" cho mọi dự án là phản tác dụng. Bốn giai đoạn của NLH:

| Giai đoạn | Là gì | Kiểm chất lượng AI | Kiến trúc | Lấy phản hồi |
|---|---|---|---|---|
| **0. Thử ý** | Bản để Nhi và vài người bấm thử một ý tưởng | Tự xem 10–20 kết quả thật, đánh dấu được/không và ghi vì sao | Làm gọn, chưa cần tối ưu tốc độ, chi phí | Kéo 2–3 người dùng thật ra hỏi |
| **1. MVP có người thật** | Một lớp, một nhóm người dùng thật đang dùng | 50–200 ca thử + bảng tiêu chí viết ra; mỗi lần sửa chạy lại | Bắt đầu tính quyền, lỗi, sao lưu | Phỏng vấn ngắn nhiều người, xem hành vi dùng |
| **2. Vận hành hằng ngày** | Đội hoặc học viên dựa vào mỗi ngày, có tiền và dữ liệu thật | Hàng trăm tới hàng nghìn ca, có máy chấm được đối chiếu với người chấm, theo dõi hệ quả (học viên có ở lại, lead có chốt không) | Cân kỹ đánh đổi: nhanh, luôn mở, khớp, chắc, dễ sửa, chi phí | Khảo sát cộng đồng alumni, số liệu dùng thật |
| **3. Nền tảng** | Nhiều portal hoặc nhiều trường dùng chung | Như giai đoạn 2, cộng kiểm riêng cho từng khách | Tách dữ liệu từng khách, quyền chặt, có ghi nhận ai làm gì | Số liệu lớn, thử A/B |

Luật riêng của NLH: **phần dữ liệu dùng chung luôn tính cao hơn sản phẩm một bậc.** Một portal ở giai đoạn 0 vẫn phải ghi dữ liệu vào bộ não chung theo chuẩn giai đoạn 2, vì dữ liệu tổ chức sai là thứ khó sửa nhất về sau — và tầm nhìn dài hạn cùng hướng đóng gói cho nhiều trường sống nhờ phần này.

Mỗi khi làm việc với một sản phẩm, Claude nói giai đoạn trong một dòng: **"Sản phẩm này đang ở giai đoạn … nên khối này làm theo chuẩn …"**. Nếu thấy Nhi đang làm quá kỹ cho một bản thử, hoặc quá sơ sài cho thứ đã có người dùng thật, nói thẳng.

## 3. Kiểm chất lượng tính năng AI (kỹ năng Ng coi là quan trọng nhất)

Ng chỉ ra điều phân biệt người giỏi xây hệ thống AI là có dẫn dắt được **vòng kiểm chất lượng và soi lỗi** có kỷ luật hay không. Cách làm cho người không đọc code:

1. **Gom ca thật.** Lấy đầu ra thật của tính năng (ví dụ 30 bản hồ sơ, 50 lead đã phân loại) vào một bảng tính, mỗi dòng một ca.
2. **Nhi chấm trước.** Được / không được, kèm một câu vì sao. Đây là "gu" của Nhi biến thành dữ liệu.
3. **Soi lỗi theo nhóm.** Gom các ca "không được" thành vài loại lỗi (bịa thông tin, sai giọng, bỏ sót dữ liệu, quá chung chung…), đếm mỗi loại. Sửa **loại nhiều nhất trước**, không sửa theo ca đập vào mắt.
4. **Viết tiêu chí.** Từ các loại lỗi, viết 3–5 tiêu chí chấm bằng lời thường.
5. **Chạy lại sau mỗi lần sửa.** Mỗi lần đổi prompt, đổi mô hình hay đổi dữ liệu, chạy lại cả bộ ca, xem tốt lên hay xấu đi — không nhìn một ví dụ rồi kết luận.
6. **Tự động dần theo giai đoạn.** Tới giai đoạn 1–2, cho một máy chấm (AI chấm theo tiêu chí) làm phần lớn, nhưng định kỳ so với điểm Nhi chấm. Ng gọi đây là **chấm lại chính bộ chấm**: nếu máy chấm lệch với Nhi thì sửa máy chấm trước.

Chọn cách chấm: thứ đo được bằng luật (có đủ trường không, đúng định dạng không) thì chấm bằng máy; thứ cần gu (giọng văn, độ sâu, độ đúng người) thì AI chấm theo tiêu chí; thứ nhạy cảm hoặc có tiền thì luôn có người chấm.

Với tính năng AI đụng tới dữ liệu người (hồ sơ, hành vi, lịch sử học), thêm kiểm **an toàn**: người dùng cố tình gõ lệnh lạ để bẻ AI, nguy cơ lộ dữ liệu người khác, và ai được xem gì.

## 4. Nói đánh đổi bằng lời thường (kỹ năng 2 cho Nhi)

Ng nói người hiểu nền tảng sẽ lái agent tốt hơn hẳn người để agent tự đoán. Nhi không cần viết code, chỉ cần biết tên các đánh đổi. Thẻ từ vựng:

- **Nhanh** — bấm là ra ngay hay phải chờ.
- **Luôn mở** — có lúc nào sập, không vào được không.
- **Khớp** — hai nơi cùng hiện một con số (ví dụ số học viên ở CRM và ở trang vận hành) có lúc nào lệch nhau không.
- **Chắc** — lần nào cũng chạy đúng.
- **Dễ sửa** — mai đổi một thứ thì tốn bao lâu.
- **Đơn giản** — ít bộ phận, ít chỗ hỏng.
- **Chi phí** — tiền máy chủ, tiền gọi AI, tiền dịch vụ ngoài.
- **An toàn & riêng tư** — ai được xem, lộ ra thì sao.

Luật cho Claude: ở mỗi điểm quyết định kỹ thuật, nói **đang đổi cái nào lấy cái nào** trong 1–2 câu, kèm một ví dụ ở NLH. Không liệt kê cả tám nếu chỉ hai cái liên quan.

Trước khi thêm bất kỳ bảng hay trường nào vào bộ não dữ liệu chung, Claude tự trả lời (rồi xin Nhi gật): ai đọc, ai ghi, giữ bao lâu, cần khớp tới mức nào, ai được xem, và khi nhiều trường cùng dùng thì dữ liệu từng trường tách nhau thế nào.

## 5. Quy trình 7 mũ nhìn qua cách dùng agent của Ng

Ng mô tả việc dùng coding agent theo ba bước — **lên kế hoạch → thực hiện → đưa lên và theo dõi** — và nói đây vẫn là vòng đời phần mềm cũ, chỉ khác là công sức dời từ viết code sang quyết định làm gì, thiết kế, viết bản mô tả và kiểm kết quả. Đối chiếu với 7 mũ:

| Bước của Ng | Mũ ở NLH | Cần thêm |
|---|---|---|
| Lên kế hoạch | Mũ 1–4 (PRD → luồng → giao diện → thiết kế kỹ thuật) | Một bước **soát kế hoạch** trước khi làm: hỏi lại các giả định chính, chỗ hở bảo mật, chỗ làm quá tay |
| Thực hiện | Mũ Dev + QA | Chọn **mức tự chủ** cho từng việc (hỏi-đáp từng bước / giao một khối / cho chạy tới khi đạt); luôn đưa agent **cách tự kiểm** (bài kiểm, ảnh chụp làm bằng chứng, bộ ca chất lượng) để nó tự khép vòng; người soát ở những cổng đã chọn |
| Đưa lên và theo dõi | Mũ Release | Bước **theo dõi sau khi lên**: định kỳ cho agent đọc lỗi và nhật ký, đề xuất sửa; có cổng chặn trước khi đụng bản thật |

Năm kỹ năng con của việc dùng agent, rút gọn cho NLH:
- **Lái quy trình** — biết khi nào quay lại bước trước. Ng nhấn mạnh quy trình vòng đi vòng lại: phản hồi ở bước sau thường buộc sửa bước trước.
- **Cho agent tự chủ đúng mức** — và chạy an toàn: agent **không bao giờ có quyền ghi vào cơ sở dữ liệu thật chứa dữ liệu học viên** nếu không qua cổng chặn; làm trên bản xem thử trước.
- **Soát bài** — kiểm hành vi và chức năng, bắt agent nộp ảnh chụp làm bằng chứng, dùng bộ ca chất lượng, cho AI soát code và bảo mật, người soát ở chỗ đáng soát.
- **Chỉnh agent và môi trường** — mỗi dự án có file bối cảnh thường trực (CLAUDE.md) ghi kiến trúc, quy ước, cách truy cập dữ liệu; gắn skill và kết nối cần thiết, **dọn bớt skill trùng hoặc cũ** vì chúng làm agent rối; sau mỗi lượt chạy rút bài học ghi vào bối cảnh.
- **Hiểu agent chạy thế nào** — để nhận ra khi nó đi lệch.

Ng cũng phản bác quan niệm "cứ để agent chạy một mình hàng giờ": việc đó đôi khi có ích, nhưng giá trị thực tế so với chi phí đã bị thổi phồng. Cách hiệu quả nhất là vòng ngắn, có người phán đoán và can thiệp — khớp với cách Nhi làm: xem, bấm thử, chỉnh.

## 6. Học liên tục — thành nhịp của đội

Công cụ agent tiến bộ nhanh hơn ba kỹ năng còn lại, nên Ng khuyên có **thói quen** thử công cụ mới và chỉnh quy trình. Ở NLH:
- Mỗi tháng một buổi thử công cụ hoặc cách làm mới trên một việc thật nhỏ, rồi quyết giữ hay bỏ.
- Sau mỗi khối lớn: một đoạn rút kinh nghiệm ngắn, cập nhật vào CLAUDE.md và ghi chú bàn giao.
- Khi cả đội học chứng chỉ, đối chiếu nội dung chứng chỉ với bản đồ để thấy phần nào còn thiếu.

## Cách Claude trả lời khi skill chạy

Khi được nhờ soi một sản phẩm, một khối việc hay năng lực đội theo bản đồ này, trả lời theo khung:
1. **Giai đoạn** của sản phẩm (một dòng) và chuẩn tương ứng.
2. **Bốn kỹ năng**: mỗi kỹ năng một câu — đang ổn hay đang hổng, ai đang giữ.
3. **Ba chỗ hổng lớn nhất**, xếp theo rủi ro — ưu tiên dữ liệu dùng chung và tính năng AI chưa có bộ kiểm.
4. **Một khối lớn tiếp theo** (một đoạn) — phần chi tiết để team làm.

Lời thường, không thuật ngữ; từ chuyên ngành nào buộc phải dùng thì giải thích bằng hình ảnh đời thường. Đưa thứ nhìn và bấm được (bảng, bản xem thử) thay vì mô tả dài.

## Giới hạn

- Bản đồ viết cho người làm phần mềm nói chung. NLH áp cho một đội nhỏ có nhà sáng lập không viết code, nên việc chia vai ở mục 1 và bốn giai đoạn ở mục 2 là **cách NLH điều chỉnh**, không phải lời Ng.
- Tính đến các thư Ng đã đăng, bản đồ chưa có thang cấp độ chính thức; thang trong `references/cham-nang-luc-team.md` là của NLH.
- Ng nói sẽ tiếp tục cập nhật bản đồ. Khi dùng cho quyết định lớn (tuyển người, đổi kiến trúc), tìm bản mới nhất trên The Batch.
