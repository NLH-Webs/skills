# Nguồn, brief và chọn đoạn

## 1. Brief cho từng video (viết TRƯỚC khi mở dòng thời gian)
| Mục | Câu hỏi |
|---|---|
| Mục đích | Video này để làm gì — giáo dục, bán khoá học, xây thương hiệu, kéo về kênh chính? |
| Người xem | Ai, đang biết gì, đang ở đâu (lướt short hay ngồi xem dài)? |
| Ý lõi | Một câu. Nếu không viết được một câu thì đoạn chọn đang lan man. |
| Cảm giác để lại | Được hiểu, được thúc, được dỗ dành, bị thách thức… |
| Hành động | Theo dõi, xem bản dài, đăng ký khoá, không gì cả |
| Mode | Short dày / dài tiết chế (mặc định) |
| Điều không được xảy ra | Nội dung nhạy cảm, riêng tư, câu dễ bị cắt ngữ cảnh |
| Đoạn khó | Chỗ phụ thuộc chat, chỗ chia sẻ màn hình, chỗ nói nhỏ/ồn |

**Bản đồ quyết định** (mốc → nội dung → trạng thái người xem → xử lý → vì sao → phương án đơn giản hơn). Mỗi thứ thêm vào phải qua bộ lọc: giải quyết vấn đề gì · thêm gì cho hiểu/cảm · vì sao ở đây · bỏ đi video có tệ hơn không (không tệ hơn → bỏ).

## 2. Bóc chữ
- Mô hình: Whisper; tiếng Việt dùng PhoWhisper-large (chuyển sang CTranslate2 float16, chạy faster-whisper trên GPU). `word_timestamps=True`, `vad_filter` nhẹ.
- Chuẩn hoá Unicode NFC ngay khi ghi (so khớp cụm sai nếu lẫn NFD).
- Ghi `transcript.json` dạng `{"segments":[{"words":[{"w","s","e"}]}]}`.
- Tách tiếng 16 kHz mono cho bộ lọc: `ffmpeg -i nguon.mp4 -ac 1 -ar 16000 am-16k.wav`.
- Nếu video đã đăng: tải phụ đề tự động (định dạng json3/vtt) — **chỉ để đối chiếu chữ nghe sai**, không dùng làm mốc.

## 3. Đọc để chọn
- `python scripts/in_tu.py transcript.json <từ> <đến> > doan.txt` rồi đọc hết. Đừng chọn đoạn từ trí nhớ hay từ tóm tắt.
- Đánh dấu trên bản in:
  - **Câu móc**: ngắn (2–8s), tự đứng được, gây tò mò/va chạm/cảm xúc (vd. một câu cảnh báo hậu quả, một câu lật ngược niềm tin, một con số bất ngờ).
  - **Câu chốt**: câu kết ý trọn — giữ nguyên khoảng lặng ngay trước (tạo nhịp).
  - **Phụ thuộc chat/màn hình**: "các bạn thả tim đi", "ủa sao nó không lên" → thường bỏ.
  - **Lặp ý**: nói lại lần hai không thêm gì → bỏ lần sau.
  - **Nhạy cảm**: sức khoẻ, tiền, người thứ ba, trẻ em, câu đùa có thể bị hiểu sai → bỏ hoặc hỏi.
- Đoạn đã dùng ở video khác của cùng đợt: tránh trùng (ghi lại khoảng đã dùng cho từng video).

## 4. Cấu trúc
**Bản dài (8–16 phút):** 3 câu móc → thẻ tiêu đề (nhãn chương trình · tiêu đề có 1 từ nhấn · chữ nền lớn) → thân bài 5–15 đoạn → 4–8 chương → thẻ kết. Chương đặt theo chuyển ý thật, tên chương 2–6 chữ, rút từ lời nói.
**Short (45–90s):** hook (lời thật) từ khung 0 → thân → câu chốt trọn → thẻ kết 2,5–5s. Xem `11-short-doc.md`.
**Bản đồ cường độ:** êm → bối cảnh → dâng → nhấn → đỉnh → gỡ → suy ngẫm → kết. Không dựng cả video ở mức đỉnh.

## 5. Ra mốc
`python scripts/moc.py transcript.json "cụm đầu|cụm cuối|a|b" ...` → `dict(s=…, e=…)`.
- Cụm phải là **chữ máy nghe** (kể cả nghe sai), không phải chữ đã sửa.
- "KHÔNG THẤY": cụm vắt qua dấu câu hoặc từ đệm → dùng cụm ngắn hơn / cụm kề bên.
- Mốc đầu đoạn thân nên bắt đầu ở đầu câu; cắt giữa câu chỉ khi phần trước là đệm hoặc nói dở.

## 6. Sổ quyết định
Mọi khoảng bỏ giữa hai đoạn giữ: `(giây đầu, giây cuối, "lý do")`. Lý do hay gặp: phụ thuộc chat · lỗi kỹ thuật (mất màn hình, nhạc chen) · lặp ý · nhạy cảm · nghe không rõ · lời hứa/khuyến mãi chưa chắc còn hiệu lực. Sổ này là thứ người nhờ đọc để quyết định giữ lại gì.
