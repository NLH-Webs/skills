# Thang chấm craft — mũ PM + UX + UI
**Dùng để:** tự chấm ba file bàn giao (`01-prd.md` · `02-ux-flow.md` · `03-ui-spec.md`) trước khi đưa người duyệt.
**Tổng:** 100 điểm · 25 tiêu chí (PRD 40 · UX 30 · UI 30) · **5 cửa chặn** · sàn đưa người duyệt: **90**.
**Cách chấm:** mỗi tiêu chí cho 1 trong 3 mức — Đạt (đủ điểm) · Tạm (nửa điểm) · Trượt (0). Phạm một cửa chặn thì cả tài liệu 0 điểm, không tính phần còn lại.
**Chấm mù:** người chấm không phải người viết. Cùng một người vừa viết vừa chấm thì điểm không dùng được.

---

## 0. Cách dùng
1. Viết xong một file (`01-prd.md`, `02-ux-flow.md`, `03-ui-spec.md`) → **một phiên độc lập chấm mù**: chỉ đọc file + thang này, không biết ai viết, không thấy hội thoại.
2. Mỗi tiêu chí chấm 3 mức: **Đạt** (đủ điểm) · **Tạm** (nửa điểm) · **Trượt** (0). Mỗi mức phải kèm **câu trích trong file** làm bằng chứng.
3. Ngưỡng: **≥ 90** đưa người chủ duyệt · **75–89** agent sửa rồi chấm lại · **< 75** viết lại · **phạm cửa chặn** trả lại ngay, không cần chấm tiếp.
4. Kết quả ghi vào thư mục chấm (điểm từng tiêu chí · bằng chứng · 3 việc phải sửa) và bài học vào nhật ký học.

## 1. Chia điểm
| File | Mũ | Điểm |
|---|---|---|
| `01-prd.md` | Mũ 1 · PM | 40 |
| `02-ux-flow.md` | Mũ 2 · UX | 30 |
| `03-ui-spec.md` | Mũ 3 · UI | 30 |
| **Tổng** |  | **100** |

## 2.1 01-prd.md — Mũ 1 · PM (40 điểm)
_Chọn đúng vấn đề, chốt phạm vi, đo được, biết khi nào dừng._

| # | Tiêu chí | Điểm | Mô tả |
|---|---|---|---|
| P1 | Cắm vào hệ thống lớn | 6 | Mở đầu nói rõ: dùng cho vai nào trong bộ vai đã chốt, đọc/ghi đối tượng chung nào, nhận việc từ đâu, chuyển việc cho ai — đối chiếu bản đồ. |
| P2 | Vấn đề kể bằng một người thật, có số hôm nay | 4 | Có một người cụ thể đi qua hệ thống và dừng ở đâu; hậu quả ghi bằng con số đo được trước khi làm. |
| P3 | Chỉ đúng rễ, không chữa triệu chứng | 4 | Nói rõ vấn đề mọc từ rễ nào; nếu là lá thì phải nói rễ của nó đã sửa chưa. |
| P4 | Đủ bốn mảnh của một phương án | 5 | Nói được: đối tượng nào · trạng thái nào · luật chặn gì · ai được báo. Thiếu một mảnh là chưa phải phương án. |
| P5 | Ai xem, ai sửa theo bộ vai đã chốt | 4 | Với mỗi dữ liệu đụng tới: vai nào sửa, vai nào xem, vai nào chỉ thấy phần của mình, vai nào không thấy. |
| P6 | Dữ liệu cá nhân đúng chuẩn | 5 | Hỏi đồng ý trước khi thu; chỉ thu thứ dùng tới; trẻ em có người giám hộ; có đường xoá và xuất; ghi nhật ký ai xem gì. |
| P7 | Không khoá mất đường bán cho trường khác | 3 | Mọi dữ liệu mới có nhãn Đơn vị (tenant); không viết cứng tên tổ chức mình vào lõi; trường xuất được dữ liệu của họ. |
| P8 | Phạm vi cắt theo thời gian, nói rõ cái không làm | 3 | Có mức thời gian cho trước (một tuần / hai tuần), cắt việc cho vừa; liệt kê thứ cố tình không làm lần này. |
| P9 | Đo được và có tiêu chí dừng | 3 | Một chỉ số dẫn trước, đo được trong 2 tuần; và câu “nếu … thì dừng, không làm tiếp”. |
| P10 | Cắt tới thứ không bỏ được | 3 | Liệt kê thứ đã cân nhắc rồi bỏ, và nói vì sao bỏ mà việc vẫn xong. Một màn thêm vào phải trả lời được: bỏ nó thì ai không làm được việc gì. |

## 2.2 02-ux-flow.md — Mũ 2 · UX (30 điểm)
_Hành trình, luồng màn hình, trạng thái, chuyển tay._

| # | Tiêu chí | Điểm | Mô tả |
|---|---|---|---|
| U1 | Hành trình đủ chặng, có phần sau khi mua | 3 | Vẽ đủ: biết tới → cân nhắc → mua → dùng → quay lại; không dừng ở lúc bấm mua. |
| U2 | Đủ trạng thái rỗng, lỗi, đang tải, quá hạn | 5 | Mỗi màn có bốn trạng thái này, mỗi trạng thái có chữ cụ thể và một việc làm tiếp. |
| U3 | Chuyển tay có tên người và có hạn | 5 | Mỗi bước ghi rõ: việc này ai nhận tiếp, trong bao lâu, quá hạn thì ai được báo. |
| U4 | Không hỏi lại thứ hệ thống đã biết | 4 | Mọi ô nhập đều kiểm: dữ liệu này hệ thống có chưa? Có thì điền sẵn, cho sửa. |
| U5 | Người dùng luôn biết việc tiếp theo là gì | 4 | Mỗi màn chính có một ô “việc tiếp theo” nói đúng một việc nên làm ngay. |
| U6 | Có đường lùi và đường sửa sai | 3 | Việc nào cũng có cách trả về, huỷ, hoặc sửa; huỷ và trả về bắt buộc ghi lý do. |
| U7 | Mở đầu và kết thúc được thiết kế | 3 | Phút đầu và phút cuối của hành trình có chủ ý: người dùng nhớ gì, cảm gì, mang gì đi. |
| U8 | Để lại dấu vết dữ liệu cho vòng sau | 3 | Mỗi bước quan trọng ghi lại được: ai làm, lúc nào, kết quả ra sao — để sau này đo, học và cải tiến, không phải đoán. |

## 2.3 03-ui-spec.md — Mũ 3 · UI (30 điểm)
_Bố cục, thành phần, chữ trên màn hình, chuẩn thị giác._

| # | Tiêu chí | Điểm | Mô tả |
|---|---|---|---|
| I1 | Một màn một việc chính | 4 | Mỗi màn có đúng một nút chính; các việc phụ nhẹ hơn về thị giác. |
| I2 | Chữ trên màn bằng lời người dùng | 5 | Không thuật ngữ máy, không tên biến, không tiếng Anh khi có từ tiếng Việt; mỗi câu nói được người đọc phải làm gì. |
| I3 | Số và ngày hiển thị cho người đọc | 4 | Ngày viết kiểu người Việt; tiền có đơn vị và dấu phân cách thống nhất; thời gian chờ đổi ra giờ/ngày. |
| I4 | Cảnh báo nói hậu quả và cách sửa | 4 | Mỗi cảnh báo trả lời: đang sai gì, ai bị ảnh hưởng, bấm gì để sửa. |
| I5 | Dùng được trên điện thoại | 3 | Xem và làm được việc chính trên màn hình điện thoại; không có bảng tràn ngang. |
| I6 | Dùng lại tên gọi và thành phần chung | 4 | Cùng một thứ thì gọi cùng một tên ở mọi trang; dùng lại thành phần đã có thay vì vẽ mới. |
| I7 | Nói thật chỗ chưa có, không hiện số giả | 6 | Phần chưa nối dữ liệu phải nói rõ trên màn; không bao giờ hiện số mẫu như số thật. |

## 3. Cửa chặn — phạm là 0 điểm toàn bài
| # | Cửa chặn | Nghĩa là |
|---|---|---|
| 1 | Lộ dữ liệu người khác | Bất kỳ đường nào cho người không có quyền đọc dữ liệu cá nhân, nhất là trẻ em và ngày giờ sinh. |
| 2 | Không cắm vào bản đồ | File không trả lời được câu “cắm vào hệ thống lớn ở đâu”. |
| 3 | Số giả đứng lẫn số thật | Màn hình hiện số mẫu mà không ghi rõ là mẫu. |
| 4 | Đưa code cho người chủ duyệt | Cổng duyệt không có thứ nhìn hoặc bấm được. |
| 5 | Không có tiêu chí dừng | Không nói được khi nào thì dừng, khi nào là xong. |

## 4. Soi kiến trúc — 5 câu, không tính điểm (Bucky Fuller · ESG)
Dùng khi quyết thứ thuộc **móng** hoặc **khung** (chọn cách lưu dữ liệu, thêm một hệ mới, đổi nhà cung cấp), và soi lại mỗi quý. Không chấm từng file — vì hỏi mỗi file thì thành hình thức.
| # | Câu hỏi | Nghĩa là |
|---|---|---|
| E1 | Cho đi nhiều hơn lấy | Cái này tạo ra nhiều giá trị hơn chi phí nó bắt người khác gánh (thời gian đội, tiền máy chủ, rác dữ liệu) chưa? |
| E2 | Hỏng một chỗ có sập cả hệ không | Nếu trang này chết, các trang khác còn chạy không? Dữ liệu có mất không? |
| E3 | Dùng ít, được nhiều | Có cách nào dùng thứ đã có sẵn thay vì dựng thêm một hệ mới không? |
| E4 | Mười năm nữa còn đúng không | Quyết định này khoá mình vào một nhà cung cấp, một công nghệ, hay một cách nghĩ nào không? |
| E5 | Trim tab | Đòn bẩy nhỏ nhất, rẻ nhất mà đổi được hướng cả hệ — làm cái đó trước. |

## 4b. Thang chấm số 2 — sản phẩm dạy học (chưa làm)
Giáo án, buổi Zoom, workshop, thử thách **không chấm bằng thang này**: chúng không có màn hình, không có trạng thái, người dùng là học viên đang học. Sẽ có thang riêng dựa trên Marshall Thurber (học qua trò chơi và trải nghiệm), Peak-End, và cách dạy bằng thẻ viết tay — làm khi tới sản phẩm dạy học đầu tiên.

## 5. người chủ duyệt gì ở Gate 1
1. Phần chuẩn người chủ đang chiếm **54/100** điểm — nặng vậy đúng ý chưa (mức tối thiểu prompt yêu cầu là 30).
2. Tiêu chí nào thừa, hoặc thiếu thứ người chủ hay soi mà chưa có.
3. Năm cửa chặn đã đủ chưa.

## Changelog
v0.1 — 2026-09-18 — Bản đầu: 23 tiêu chí (PRD 9 · UX 7 · UI 7), 5 cửa chặn, ngưỡng 90.
