# Gộp hai người ra quyết định vào một agent
Cách để một agent đứng được giữa **người vẽ đích** (chủ sản phẩm, tầm nhìn, gu) và **người vẽ hành lang** (kỹ sư trưởng, kiến trúc, dữ liệu) — và **cắt được vòng duyệt hai lần**.

Đây là phương pháp. Bảng trọng tài thật của một tổ chức cụ thể nằm ở kho riêng của tổ chức đó.

---

## 1. Nói thẳng trước: "giỏi hơn cả hai cộng lại" nghĩa là gì
Agent **không** giỏi hơn ở chỗ mỗi người giỏi nhất. Người bán hàng 15 năm đọc được khách trong một cuộc gọi; kỹ sư 8 năm nhìn một migration là biết nó nổ ở đâu. Agent không có hai thứ đó.

Agent giỏi hơn ở **đúng bốn chỗ**:
1. **Không quên** — nhớ cả hai bộ luật cùng lúc, mọi lúc.
2. **Bắt được mâu thuẫn** — hai người ngồi hai bàn nên không thấy luật của mình va luật người kia. Agent thấy cả hai.
3. **Làm xong bài tập trước khi hỏi** — phần lớn vòng duyệt bị đốt vào *"cái này đã kiểm chưa"*.
4. **Kiên định** — con người quyết khác nhau lúc mệt và lúc khỏe.

Bốn thứ đó **đủ để bỏ phần lớn vòng duyệt** — không phải vì agent khôn hơn, mà vì nó không để việc tới bàn khi chưa chín.

## 2. Ba người, ba câu hỏi khác nhau
Xung đột "ai quyết" tan ngay khi thấy ba người đang trả lời **ba câu khác nhau**:

| | Câu hỏi | Không lấn sang |
|---|---|---|
| **Người vẽ đích** | Làm gì, cho ai, có đúng lúc không? | Không quyết cách làm kỹ thuật |
| **Người vẽ hành lang** | Có được phép làm thế không? | Không quyết sản phẩm làm gì cho ai |
| **Agent** | Làm thế nào cho đúng cả hai? | Không quyết 6 việc ở §5 nhóm C |

> **Luật gốc:** một người vẽ đích, một người vẽ hành lang, **agent đi đường bên trong hành lang tới đích đó — và chỉ dừng lại hỏi khi đích nằm ngoài hành lang.**

## 3. Luật gốc trước khi vào bảng — một người phải có tiếng nói cuối ở một miền
Trước khi liệt kê từng va chạm, hai người phải chốt **một luật gốc**, không thì mỗi va chạm lại thành một cuộc thương lượng. Cách chốt đã chạy được trong thực tế:

> **Va chạm nào chạm ĐỘ BỀN — kiến trúc, dữ liệu, bảo mật, chi phí gỡ — thì người vẽ hành lang thắng. Không thương lượng, không chia đôi.**
> **Nhưng làm gì · cho ai · có đúng lúc không — vẫn là của người vẽ đích.** Người vẽ hành lang không lấn sang.

Vì sao chia như vậy chứ không phải ngược lại: thứ xây cho lâu dài mà không kỹ thì sập, và người vẽ đích thường không nhìn được móng. Nhưng biên thứ hai cũng không phải phép lịch sự — **độ bền không có người dùng là thất bại kinh điển của đội kỹ thuật**: sản phẩm dựng chắc như thép, không ai xài. Người vẽ đích giữ ba biên đó là để bảo vệ chính người vẽ hành lang khỏi lặp lại thất bại ấy.

Với luật gốc này, phần lớn bảng trọng tài tự trả lời. Câu đầu tiên agent hỏi khi gặp va chạm không phải "ai đúng" mà là **"cái này có chạm độ bền không?"** Có → xong. Không → mới tra bảng.

## 3b. Bảng trọng tài — thứ quyết định thành bại
**Gộp hai bộ não không phải là nối hai danh sách luật.** Nhét cả hai vào mà không có trọng tài thì agent gặp va chạm sẽ **chọn vế nào tiện cho mình** — và sẽ luôn tìm được một câu luật để biện minh.

Giá trị nằm ở việc viết ra: **chỗ nào hai người va nhau, ai thắng, và trong điều kiện nào.**

Sáu kiểu va chạm gặp ở gần như mọi tổ chức, kèm luật chia đã dùng được:

| Va ở đâu | Luật chia |
|---|---|
| **Ship nhanh vs ship hoàn hảo** | **Chạm độ bền → người vẽ hành lang thắng.** Chưa đủ bền thì không ship, kể cả người vẽ đích muốn nhanh. Người vẽ đích giữ quyền *có làm tính năng này không*; người vẽ hành lang giữ quyền *nó đã đủ bền để ra chưa*. Cái giá phải nói rõ từ đầu: ra sản phẩm chậm hơn. |
| **Rào thừa vs quy trình bắt buộc** | **Chạm độ bền → giữ rào.** Kiểm phiên bản, chặn commit sai, ghi quyết định — giữ hết. Agent chỉ được **đổi hình thức** cho nhẹ với con người (tài liệu do agent viết, không bắt người vẽ đích ký), không được bỏ rào. |
| **Thu nhiều dữ liệu vs thu tối thiểu** | **Hai câu hỏi khác nhau, hai người khác nhau.** Thu bao nhiêu trường *định danh* = độ bền và pháp lý → người vẽ hành lang, thu tối thiểu. Giữ *hành vi* đã cắt danh tính để học = mục đích sản phẩm → người vẽ đích. Kết quả: **thu HÀNH VI rộng, thu DANH TÍNH hẹp.** Sự kiện (ai-làm-gì-lúc-nào) thu tối đa; trường định danh thu tối thiểu, khoá người là **mã** chứ không phải email. Cách duy nhất để cả hai cùng đúng — và là cách xoá dữ liệu cá nhân bằng một thao tác thay vì một dự án. |
| **Dài hạn vs cửa sổ thị trường** | **Lõi theo dài hạn, vỏ theo thị trường — và ranh giới lõi/vỏ do người vẽ hành lang vẽ.** Lõi (danh tính, sự kiện, hồ sơ, quyền) không có ngoại lệ vì cửa sổ thị trường. Vỏ (màn hình, cách bán) là *làm gì cho ai* → người vẽ đích. |
| **Dùng đồ có sẵn vs không phụ thuộc nhà cung cấp** | **Lõi tự làm, vỏ đi thuê — cái gì là lõi do người vẽ hành lang quyết.** Người vẽ đích chỉ dùng công cụ có sẵn trong phần đã được phép thuê. Vỏ thuê thoải mái, miễn có lớp adapter. |
| **Duyệt bằng mắt vs duyệt bằng bằng chứng** | **Agent nộp CẢ HAI trong một gói** — và nếu chỉ đủ một nửa thì **nửa bằng chứng phải có trước**. Chưa có bằng chứng thì chưa được đưa người vẽ đích bấm. |

**Một va chạm hay bị bỏ sót:** người này ghét thủ tục, người kia coi ghi chép là điều kiện ship. → **Tài liệu là việc của AGENT, không phải việc của người chủ.** Agent tự viết, người chủ không đọc, không ký. Xung đột biến mất hoàn toàn chỉ nhờ đổi đúng người viết.

**Luật dùng bảng:** gặp va chạm → tra bảng. Trả lời được → **quyết, ghi lại, đi tiếp, không hỏi ai**. Không trả lời được → nhóm C, và sau khi có câu trả lời thì **thêm một dòng vào bảng**. Bảng dài dần, việc phải lên bàn ít dần. Đó là cơ chế tự giảm vòng duyệt.

## 4. Hai bộ lọc chạy trước, mỗi lần
Trước khi bất cứ thứ gì rời tay agent, chạy **cả hai** bộ lọc — của người vẽ đích và của người vẽ hành lang. Trượt bất kỳ câu nào → **agent tự sửa rồi chạy lại**.

> Đưa lên bàn một thứ chưa qua bộ lọc là **tự đẻ thêm một vòng duyệt**.

## 5. Ba nhóm quyết định — cái thật sự cắt vòng duyệt

**Nhóm A — agent tự quyết, chỉ ghi sổ.** *(mục tiêu ~70%)*
Đủ **cả ba**: bảng trọng tài hoặc luật đã có tiền lệ · gỡ được dưới một ngày · không chạm tiền, dữ liệu cá nhân, lời hứa ra ngoài.
→ Quyết, ghi lại, làm. **Không ai phải duyệt.**

**Nhóm B — agent quyết, gửi kèm bản một phút.** *(~25%)*
→ Agent quyết và làm luôn, đồng thời gửi một trang: quyết gì · vì sao · cái mất · đường thoát. **Im lặng 24 giờ = thông qua.** Bị lắc thì đổi, không cãi.

**Nhóm C — phải lên bàn.** *(≤ 5%)* Đúng sáu loại, không thêm:
1. **Tiền** — giá, chính sách hoàn tiền, phí mới.
2. **Lời hứa ra ngoài** — thứ khách sẽ đọc và tin.
3. **Dữ liệu cá nhân và pháp lý** — thu thêm trường, đổi cách xoá, dữ liệu trẻ em.
4. **Kiến trúc không gỡ được** — đổi khoá chính, đổi hợp đồng dữ liệu, chọn nhà cung cấp cho lõi.
5. **Người** — phân vai, dừng hợp tác, mở quyền.
6. **Bảng trọng tài không phủ** — hai bộ lọc ra kết quả ngược nhau và bảng không có dòng nào trả lời.

**Loại 6 quan trọng nhất:** mỗi lần dùng tới nó, bảng trọng tài dài thêm một dòng và lần sau không cần hỏi nữa.

## 6. Khuôn "một bàn thay vì hai bàn"
Khi buộc phải lên bàn, nộp **đúng một trang**, đủ sáu mục:

| Mục | Nội dung |
|---|---|
| **Ai cần chốt** | Người nào — ghi rõ, đừng để hai người chờ nhau |
| **Cho người duyệt bằng mắt** | Một bản bấm được, hoặc hai bản cạnh nhau. Không mô tả bằng chữ trừu tượng |
| **Cho người duyệt bằng bằng chứng** | Migration, kiểm thử, ảnh hưởng hợp đồng dữ liệu, **đường thoát nếu sai** |
| **Hai đường** | Đặt cạnh nhau, nói rõ **cái mất mỗi bên** — không đưa một đường rồi xin gật |
| **Agent khuyến nghị** | Chọn cái nào, vì sao, **độ chắc** |
| **Nếu không ai trả lời trong 48 giờ** | Agent làm gì theo mặc định an toàn |

Dòng cuối là thứ **thật sự cắt vòng duyệt** — nút thắt lớn nhất không phải bất đồng, mà là **chờ**.

## 7. Năm số để biết cơ chế có chạy không
| Số | Mốc |
|---|---|
| Tỷ lệ A / B / C | Tháng 1: 40/40/20 → tháng 6: 70/25/5 |
| Số dòng thêm vào bảng trọng tài | Giảm dần |
| **Tỷ lệ bị lắc ở nhóm B** | **> 10% = agent tự quyết quá tay** → siết lại |
| Số lần quay lại vì thiếu bằng chứng | → 0 |
| Số vòng duyệt trung bình mỗi sản phẩm | 2+ → 1 |

Năm số này mới là bằng chứng, không phải điểm agent tự chấm.

## 8. Điều kiện duy nhất khiến cơ chế này hỏng
Cơ chế chỉ chạy nếu **cả hai người cùng chịu buông nhóm A**. Nếu một trong hai vẫn muốn xem hết mọi thứ, tỷ lệ nhóm C sẽ tự bò lên 30% và mọi thứ quay về như cũ — **không phải vì agent dở, mà vì cơ chế chưa được cho phép chạy**.

Đây là quyết định của hai con người, không phải của agent. Nói thẳng điều đó ngay từ đầu, đừng để sáu tháng sau mới phát hiện.
