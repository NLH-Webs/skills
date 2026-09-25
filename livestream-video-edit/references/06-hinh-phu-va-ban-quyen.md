# Hình phụ (b-roll), nhạc ngoài, giấy phép

## Vai trò trước, hình sau
Viết được "người xem cần thấy cái này vì ___" mới chèn: bằng chứng · bối cảnh · minh hoạ ẩn dụ · khuếch đại cảm xúc · giải thích · reset chú ý. Hình cụ thể hơn hình stock chung chung.
- Short: b-roll dày (~3s mỗi hình, 10–25 hình/phút tuỳ nhịp). Bản dài: ít hơn, có vai trò rõ.
- Không che thứ đang là bằng chứng: màn hình demo, bản vẽ trên bảng, tài liệu đang được chỉ.
- Đoạn nói về trẻ em/gia đình: dùng hình stock trung tính, không dùng ảnh thật của người trong câu chuyện trừ khi người nhờ đưa.

## Nguồn được phép
- Pexels / Pixabay qua **API chính thức** (giấy phép cho dùng thương mại, không bắt buộc ghi công).
- Nhạc: thư viện có giấy phép dùng thương mại + kênh kiếm tiền (vd. Mixkit Stock Music Free License).
- Tư liệu do người nhờ quay/cung cấp.
- **Không**: tải từ TikTok/YouTube/Facebook của người khác; lấy từ thư mục "tham khảo" (chỉ để học, không để dùng); ảnh AI giả người thật.

## Quy trình (`scripts/pexels_tim.py` → duyệt → `scripts/pexels_tai.py`)
1. Viết truy vấn tiếng Anh theo **ý** câu nói (không dịch từng chữ): "một ngọn lửa xíu xiu" → `small candle flame dark`.
2. Chạy tìm → **mở lưới và nhìn**. Loại: ô đen/rất tối, có chữ in/logo, người nhìn thẳng máy nói (dễ nhầm là người thật trong câu chuyện), sai văn hoá/ngữ cảnh (tarot cho "tử vi"), trùng hình đã dùng.
3. Tải, chuẩn hoá (30 fps, đúng khung, ≤16s, bỏ tiếng), **ghi sổ**: file · nguồn · tác giả · giấy phép · link gốc · ngày · dùng ở video nào.
4. Kiểm độ sáng **từng khung** ở đoạn thực sự dùng: lưới 1 khung/giây từng không bắt được đoạn màn đen có chữ teaser trong một clip tư liệu → phải dò độ sáng từng khung, cắt bỏ đoạn bẩn thành file "sạch".

## Tự kiểm sổ
Mọi file hình/nhạc/tiếng động trong video có dòng sổ; không dòng sổ = không được giao.
