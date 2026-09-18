# Cách chấm một agent sản phẩm — ba vòng
Rút từ một đợt huấn luyện agent sản phẩm có thật. Đây là phần **phương pháp**; số liệu và tình huống thật nằm ở kho riêng.

## Vì sao cần ba vòng, không phải một
Một agent có thể đạt điểm rất cao mà vẫn chưa biết nghĩ. Ba vòng tách ba thứ khác nhau:

| Vòng | Đo gì | Bộ đề lấy từ đâu | Mốc qua |
|---|---|---|---|
| **1 · Trí nhớ** | Agent có tra đúng sổ không | Những thứ người chủ **đã chốt**, đã ghi trong tài liệu agent được đọc | ≥ 70% |
| **2 · Suy luận** | Agent có nghĩ giống người chủ ở chỗ người chủ **chưa nói** không | Tình huống **chưa từng chốt**, không có đáp án ở đâu. Người chủ chấm gật/lắc | ≥ 8/12 |
| **3 · Sổ dự đoán** | Agent có **đúng với thực tế** không | Chính các đề xuất agent đưa ra trong lúc làm việc thật | đúng ≥ 3/4 sau 90 ngày |

**Kết quả thật của đợt chấm gốc:** vòng 1 đạt **95%** · vòng 2 rớt xuống **33%** · sau khi nạp bài học từ vòng 2 thì vòng 2 lặp lại đạt **100%**.

Cú rơi xuống 33% là chỗ đáng tiền nhất trong cả đợt. **Điểm cao ở vòng 1 không chứng minh gì** ngoài việc tài liệu đủ và tra được.

## Vòng 1 — chấm trí nhớ
**Cách chạy:** một phiên độc lập, chỉ được đọc bộ tài liệu + bộ đề. **Không thấy đáp án, không thấy hội thoại.**
**Soạn đề:** 20 tình huống người chủ đã chốt, mỗi câu ghi rõ nguồn. Không có nguồn thì không đưa vào đề. Ít nhất 5 câu là **những lần agent từng trả lời sai rồi bị sửa** — đó là chỗ hay sai lại.
**Đọc kết quả:** điểm cao chỉ nói bộ nhớ ổn. Chỗ sai mới đáng đọc, và thường không phải "thiếu tri thức" mà là **tri thức để sai chỗ**:
- Luật tả *"ba mức là gì"* nhưng không tả *"khi nào dùng mức nào"* → agent vớ mức mạnh nhất.
- Luật nằm chôn trong mô tả một giai đoạn agent chưa tới → khi tra thì không ra.
> **Một luật chôn trong mô tả giai đoạn thì coi như chưa có.** Luật phải nằm ở chỗ agent đọc mọi phiên.

## Vòng 2 — chấm suy luận
**Cách chạy:** 12 tình huống **chưa từng được chốt**. Agent phải tự quyết, cấm viết "tuỳ trường hợp" hay "cần hỏi thêm". Người chủ chấm **gật / nửa / lắc**, không có đáp án sẵn.
**Soạn đề:** mỗi câu chạm một vùng agent sẽ phải tự quyết khi làm thật — tiền · quyền · nội dung đang chạy · bàn giao người · mở rộng · luật dữ liệu · tiếp thị · lịch. Bắt agent ghi thêm một dòng bắt buộc: **"chỗ em không chắc"** — chính dòng đó chỉ ra agent tự biết mình yếu ở đâu.
**Đọc kết quả:** đừng đọc từng câu. Đọc **dạng lệch**. Trong đợt gốc, 8 chỗ lệch gom về đúng năm bệnh B1–B5 (xem SKILL.md). Sửa năm bệnh có giá trị hơn sửa tám câu.

## Vòng 2 lặp lại — và cái bẫy
Sau khi nạp năm bệnh, chạy lại 12 tình huống mới: **12/12**.
**Nhưng đừng đọc con số đó là "xong".** Bộ đề vòng lặp lại do **chính agent soạn**, ngay sau khi chính agent rút ra năm bệnh. Người ra đề và người làm bài là cùng một cái đầu — agent có thể vô thức viết những câu mà bài học vừa học trả lời gọn.
> **Luật:** bộ đề vòng sau phải do **người khác đặt tình huống**, hoặc lấy **ca thật đang xảy ra trong tuần**. Đó là bộ đề duy nhất không ai soạn thiên vị được.

Một bẫy nữa: khi người chủ gật **cả gói** thay vì soi từng câu, mọi con số agent tự bịa trong các câu trả lời đó **cũng thành luật**. Phải đánh dấu riêng những con số agent tự đặt, để sau này không ai tưởng là của người chủ.

## Vòng 3 — sổ dự đoán (thước đo thật)
Hai vòng đầu đều có **một trần chung: người chủ**. Không thể ra "giống người chủ nhưng giỏi hơn" từ một quy trình mà tín hiệu duy nhất là sự đồng ý của người chủ — trần của học sinh là thầy. Muốn vượt thì phải có **tín hiệu thứ hai: thực tế**.

**Cách làm:** chọn 4–5 chỉ số kết quả thật của doanh nghiệp, đo được tự động. Mỗi lần agent đề xuất một thứ đáng kể, ghi **trước khi làm**:

| Ngày | Agent đề xuất | Dự đoán số nào đổi | Đổi bao nhiêu | Kiểm ngày | Thực tế | Đúng/Sai |
|---|---|---|---|---|---|---|

**Không ghi thì đề xuất đó không được tính là đúng, dù kết quả có tốt.**

**Cách đọc sau 90 ngày:** đúng ≥ 3/4 → agent đang nghĩ đúng về hệ thống · đúng 2/4 → bằng tung đồng xu, xem lại lý lẽ chứ không phải trí nhớ · đúng ≤ 1/4 → agent đang lặp lại gu người chủ mà không hiểu vì sao gu đó đúng, quay lại từ đầu.

**Vì sao bắt buộc:** đây là thứ duy nhất làm agent **sai được**. Một agent không sai được thì cũng không giỏi lên được.

## Nhật ký học
Mỗi lần agent bị sửa, ghi một dòng: **ngày · agent làm sai gì · người chủ nói gì (nguyên văn) · rút ra gì · đã cập nhật file nào.**
Cột "nguyên văn" quan trọng nhất — diễn giải lại là đã mất một phần ý.

## Tiêu chí dừng
Viết **trước** khi bắt đầu huấn luyện, không phải lúc đã mệt:
> Dừng dự án agent nếu tới ngày X chưa qua một bộ đề suy luận ở mức ≥ 8/12, **hoặc** chưa có một sản phẩm thật được người tiếp nhận dựng được mà không phải hỏi lại người chủ.

Chi phí thật của việc huấn luyện agent không phải tiền máy — là **thời gian phán đoán của người chủ**, tài nguyên khan nhất. Không có tiêu chí dừng thì nó ăn mãi.
