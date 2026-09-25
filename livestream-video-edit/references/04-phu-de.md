# Phụ đề, lọc sạn, sửa chữ

## 1. Lọc sạn (`scripts/loc_dem.py`)
Làm trên mốc từng từ + năng lượng tiếng, **không** trên phụ đề câu.
| Loại | Luật | Vì sao |
|---|---|---|
| Nói hụt/lặp | Cụm n từ (1–14) lặp ngay sau trong 2s (n ≤ 4) hoặc 10s (n > 4) → bỏ lần đầu | Lần sau thường trọn hơn |
| Đệm đơn | à, ừ, ờ, ờm, ưm… | |
| Đệm đuôi | "vậy đó", "nha", "nhé", "các bạn ơi" — chỉ khi đứng riêng (lặng > 0,2s hai bên) | Giữa câu là nghĩa, không phải đệm |
| Lặng | Khe > 0,55s mà năng lượng thật sự thấp → còn 0,25s | Khe giữa từ nhưng có tiếng (thở, cười, nhạc) thì giữ |
| Câu chốt | Giữ nguyên khoảng lặng ngay trước | Tạo nhịp |

**Bẫy đã trả giá (đã cài sẵn — đừng gỡ):**
- **Phủ định**: không bao giờ bỏ "không/chưa/đừng/chẳng/hông" (trừ khi nó là bản nói hụt của chính nó) — bỏ nhầm là đảo nghĩa câu.
- **Lặp có chủ ý**: máy nghe chữ "AI" thành "ai ai" → bộ lọc tưởng nói lắp, bỏ một nửa → phụ đề ra "ai" (người nào). "mãi mãi" là điệp từ. Khai trong `GIU_LAP`.
- **Đại từ sau giới từ**: "của mình mình…" không phải nói lắp.
- Cắt mất > 1/3 thời lượng thô → dừng, đọc sổ cắt.

## 2. Hiển thị phụ đề
- Mỗi dòng ≤ 4 từ (quá thì 2 dòng), tối đa ~7 từ/khối; tách câu tại ranh giới cảnh (phần trên thẻ giấy chữ mực, phần trên nền tối chữ trắng).
- Đáy chữ ≤ 79% chiều cao, chữ trong 80% bề ngang giữa; khi người nói cúi thấp (cằm chạm dải phụ đề) → dời phụ đề sang bên cạnh mặt, hai dòng, **không so le lệch trái** (từng tràn khỏi 80%).
- Đo đáy chữ lúc chữ **đã đứng yên** (cuối hiệu ứng), không đo lúc tạo.
- Từ khoá tô màu: một cụm/khối; short ≤ 10 từ khoá cả video, cách nhau ≥ 3,5s.
- Nhãn khung chữ HTML: `.dong { width: max-content }` — thiếu dòng này, dòng lệch làm `scrollWidth` vượt khung và phụ đề 2 dòng co còn nửa cỡ (lỗi từng nằm trong nhiều bản không ai thấy).

## 3. Sửa chữ nghe sai
Máy bóc chữ sai nhiều nhất ở: từ mượn tiếng Anh, tên riêng, tên sản phẩm/app, từ địa phương, chữ viết tắt.
Quy trình:
1. In đoạn đã chọn, gạch chữ lạ ("sao háo", "đốp bơm min", "phờ ranh tia", "tếch tót", "klót").
2. Đối chiếu **phụ đề tự động của nền tảng** cùng mốc (thường đúng từ mượn hơn) → self-help, dopamine, frontier, TikTok, Claude.
3. Hai nguồn đều không chắc → **không đoán vào phụ đề**: bỏ câu đó (ghi `QUYET`) hoặc giữ nguyên âm và báo người nhờ. Ví dụ: tên hãng một thiết bị nghe thành hai tên khác nhau → cắt riêng tên hãng.
4. Ghi vào `BANG_TU_THEM` (cụm → cụm), cụm dài trước.
5. Lập danh sách "chữ sửa theo nghĩa, chưa duyệt" gửi người nhờ.

Phương ngữ (vd. "dô" = "vô"): chọn một cách viết và giữ nhất quán trong cả đợt video; nên theo cách phụ đề nền tảng đang viết.

## 4. Viết hoa
Máy trả chữ thường; lớp hiển thị thường hạ chữ mọi từ không nằm trong danh sách giữ hoa. Phải khai:
- Tên nước, dân tộc, ngôn ngữ: **Việt Nam, người Việt, tiếng Việt, châu Âu, châu Á, Sài Gòn**… (thêm "người việt nam" TRƯỚC "người việt", nếu không "nam" còn thường).
- Tên người, tên con, tên nhóm, tên thương hiệu, tên sản phẩm, app, trường.
- AI, IT, IQ, DNA, CEO…
Trước khi giao: quét file sổ phụ đề (chữ hiển thị) tìm `\b(ai|việt nam|tên riêng…)\b` viết thường, **đọc ngữ cảnh** từng chỗ ("ai" = AI hay "người nào").

## 5. SRT
Xuất từ đúng các khối phụ đề đã hiển thị (chữ đã sửa, đã viết hoa), mốc theo video thành phẩm. Kiểm số dòng SRT = số khối phụ đề.
