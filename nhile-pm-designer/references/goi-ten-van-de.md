# Cách gọi tên vấn đề và viết phương án
**Dùng trước khi viết PRD.** Sáu bước, một khuôn tám dòng, ba mức can thiệp, năm lý do nói không.
Mục đích: không mở việc cho một triệu chứng khi chưa biết nó mọc từ rễ nào.

## 1. Bảng luồng đang nói gì (đọc ra từ 48 bước)
1. **Chỗ đứt nằm ở khoảng giữa, không nằm trong từng trang.** Gần như cả 21 chỗ đứt đều ở lúc chuyển tay giữa hai nhà ga. Từng sản phẩm tốt; khoảng giữa chưa có chủ.
2. **"Làm tay" không phải chỗ đau nhất.** 9 bước làm tay vẫn xong. 21 chỗ đứt thì không máy làm cũng không ai được giao → việc rơi im lặng (19 việc tư vấn quá hạn tới 106 ngày).
3. **Luồng ra tiền đứt nhiều nhất:** L1 8 đứt, L2 5, L3 4.
4. **8 chỗ đứt của L1 mọc từ một rễ** (không có "Người" chung) → viết thành MỘT vấn đề, không phải ba.
5. **Chưa có bước tự chuyền nào bắc qua hai trang** → đang là nhiều ứng dụng, chưa là một hệ thống.
6. **Không ai được báo** (không nơi nào sinh thông báo) → làm mọi chỗ đứt khác vô hình; hệ không tự sửa được.

## 2. Sáu bước gọi tên vấn đề
| # | Bước | Câu hỏi chính | Sai kiểu thường gặp |
|---|---|---|---|
| B1 | Kể một người thật đi qua hệ thống | Ai · muốn gì · qua trang nào · dừng ở đâu | Bắt đầu bằng tính năng ("CRM cần nút gộp") |
| B2 | Chỉ một chỗ đứt chính + hậu quả bằng số | Bao nhiêu người, bao nhiêu tiền, bao nhiêu giờ | "Trải nghiệm chưa tốt", "dữ liệu lộn xộn" |
| B3 | Hỏi vì sao tới khi chạm đúng rễ | Rễ nào? Hai triệu chứng cùng rễ → gộp làm một | Mở 3 việc cho 3 màn hiện 3 số khác nhau |
| B4 | Chỉ tên chủ nhà + người chịu khoảng giữa | Ai được ghi dữ liệu · ai bị hỏi khi việc rơi | Giao cho "team IT" |
| B5 | Phương án = 4 mảnh | Đối tượng · trạng thái · luật chặn · ai được báo | "Làm màn hình gộp lead" |
| B6 | "Xong" bằng thứ nhìn thấy được | Một câu người chủ tự kiểm trong 2 phút + con số ở B2 đổi | Nghiệm thu bằng ảnh chụp màn hình |

**Ví dụ khuôn đã điền:** *(ví dụ có thật nằm ở kho riêng — khuôn dưới đây là phần dùng chung)*

## 3. Khuôn viết (copy và điền)
1. **Người:** ai, muốn gì
2. **Đường đi:** qua trang nào → trang nào
3. **Đứt ở:** chỗ chuyển tay nào
4. **Hậu quả:** con số hôm nay
5. **Rễ:** một trong năm rễ
6. **Chủ nhà · người chịu khoảng giữa:** tên
7. **Phương án:** đối tượng · trạng thái · luật chặn · ai được báo
8. **Xong khi:** câu tự kiểm bằng mắt + con số mới

## 4. Thứ tự làm — bốn câu hỏi xếp thứ tự việc
1. **Có lộ dữ liệu người khác không?** Làm trước mọi thứ. Và không chờ tới lúc lộ: mặc định thiết kế theo **PDPA Singapore** và **Luật Bảo vệ dữ liệu cá nhân Việt Nam** (hiệu lực 01/01/2026, thay NĐ 13/2023; hướng dẫn tại NĐ 356/2025) — hỏi đồng ý trước khi thu, chỉ thu thứ dùng tới, dữ liệu trẻ em cần người giám hộ, có đường xoá và xuất dữ liệu, ghi nhật ký ai xem gì.
2. **Rễ hay lá?** Sửa **hết rễ** rồi mới làm nhánh và lá — làm đúng thứ tự thì phần sau nhanh hơn hẳn. Ngoại lệ duy nhất: lá đang chảy máu (lộ dữ liệu, mất tiền, khách bỏ đi) thì vá tạm, ghi sổ nợ, sửa gốc sau.
3. **Móng → khung → mặt tiền.** Người chủ thường nhìn được mặt tiền, không nhìn được móng; nên phần móng là việc của agent: chặn, đề xuất khác, hoặc ghi nợ (mục 4b).
4. **Bán cho trường khác được không?** Chuẩn giáo dục quốc tế là **điều kiện cần, chưa đủ**.
   - *Đáng theo khi bán cho trường:* đăng nhập chung (SAML/OpenID) · **LTI 1.3** (cắm lớp vào hệ học của trường) · **OneRoster** (nhận danh sách lớp, trả điểm) · **xAPI** (dấu vết học) · **WCAG** (trường công thường bắt buộc).
   - *Chưa cần vội:* QTI (ngân hàng đề), SCORM (chuẩn cũ) — làm khi có trường đòi.
   - *Chuẩn không lo giúp, phải tự làm:* Đơn vị (tenant) tách bạch · bộ mặt riêng từng trường · trường tự xuất/mang dữ liệu đi · cam kết vận hành (trực, sao lưu, đền bù).
   - *Đề xuất của agent:* khoá sẵn **phần móng** ngay từ giờ (Đơn vị, mã người, nhật ký, đường xuất dữ liệu) vì sau này sửa rất đắt; các chuẩn nối làm khi có trường đầu tiên ký, lúc đó mới biết trường dùng hệ nào.

## 4b. Agent can thiệp thế nào (luật 12 trong SKILL.md)
Người chủ nhìn sản phẩm để biết bước tiếp; phần móng agent nhìn thay. Ba mức, lần nào cũng kèm thứ nhìn được:
- **DỪNG** — việc sẽ phải làm lại hoặc gây hại (lộ dữ liệu · sửa lá của rễ chưa sửa · khoá mất đường white label). Nói rõ vì sao + đưa việc thay thế.
- **ĐỀ XUẤT KHÁC** — có cách rẻ hơn/bền hơn: đặt cạnh nhau cách người chủ nói · cách agent đề xuất · cái mất mỗi bên.
- **GHI NỢ** — làm theo ý người chủ, nhưng ghi sổ nợ trong README (nợ gì, vì sao nhận, hạn trả).
Quyết định cuối vẫn của người chủ; im lặng làm theo khi thấy hướng sai là agent sai.

## 5. Khi nào nói không
- Không kể được bằng một người thật.
- Không có con số hôm nay → không biết lúc nào xong.
- Không có tên người chịu khoảng giữa.
- Là lá của một rễ đang chờ sửa.
- Chỉ là "thêm một màn hình" khi chưa chốt trạng thái và luật chặn.

## Changelog
v0.2 — 2026-09-18 — người chủ sửa mục 4 (PDPA + Luật DLCN VN; sửa hết rễ mới tới lá; chuẩn quốc tế là cần chưa đủ) và thêm mục 4b cách agent can thiệp.
v0.1 — 2026-09-18 — Bản đầu: 6 quan sát từ bảng luồng, 6 bước, khuôn viết, 4 câu hỏi ưu tiên, 5 lý do nói không.
