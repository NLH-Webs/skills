# Âm thanh

## Chuỗi mặc định (`scripts/tieng.py`)
1. **Giọng sạch** — mono 48 kHz → highpass 90 / lowpass 13,5k → `arnndn` (RNNoise, mix 0,9) → `afftdn` → nén nhẹ → `dynaudnorm` (m ≤ 6) → cổng êm giữa câu (`agate` range 0,2) → nén → `dynaudnorm`.
   - `dynaudnorm` m = 8–15 kéo to cả tiếng ồn ở khoảng nghỉ → giữ m ≤ 6.
   - Mô hình RNNoise: bộ BSD `richardpl/arnndn-models` (vd. `cb.rnnn`). Ghi vào sổ như một tài sản.
2. **Tiếng động** (swish, tick, chop, riser…) tự tổng hợp hoặc có giấy phép; nén theo giọng (sidechain) để không đè lời.
3. **Nhạc nền** — mức ~0,32 (≈ −18 LU dưới giọng), **né giọng** bằng sidechain (attack 30 ms, release 600 ms — nhả chậm để không "bơm"), nâng ≈ +7 dB ở thẻ tiêu đề/thẻ kết. Vào 1,5s, ra 3s.
   - Bản dài: nối nhiều bài chéo 3s, **không lặp một bài** (bài có đuôi tắt dần tạo lỗ giữa video).
   - Nhạc đổi khi mạch đổi; cân nhắc im lặng ở câu nặng.
4. **Độ to** — lặp chỉnh gain tới −12,7 LUFS ±0,08 (limiter 192 kHz, trần −1,2 dB).
5. **Nén AAC 192k → đo lại trên MP4.** Đỉnh thật > −0,8 dBTP → hạ trần limiter đúng phần vượt, làm lại. Lý do: một tiếng động gắt từng làm bản WAV −1,1 dBTP ra MP4 +2,4 dBTP.

## Kiểm
- LUFS/dBTP đo **trên file giao**, không trên WAV trung gian.
- So "nền ồn" trước/sau (phân vị 10% theo khung 25 ms ở khoảng nói) — giọng sạch phải thấp hơn ≥ 5 dB.
- File tạm `.tmp.mp4` phải được thay vào file chính (kiểm giờ ghi file và dung lượng); đừng tin dòng log.
- Máy không thay tai: báo rõ "chưa nghe bằng tai" nếu chưa nghe.
