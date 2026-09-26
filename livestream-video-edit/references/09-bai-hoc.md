# Bài học đã trả giá (đọc trước mỗi dự án)

## Hình
1. **Ô người nói phủ lên nền phải có `setpts=PTS-STARTPTS`**, nếu không lóe khung đen đầu cảnh.
2. **B-roll ngắn hơn cảnh** → cảnh hụt khung, lệch cả dòng thời gian. Dùng `tpad=stop_mode=clone` và kiểm số khung từng cảnh.
3. **Ghép nhiều lớp .mov bằng `-itsoffset` hụt 1 khung mỗi ranh giới** (chớp mất chữ mỗi 15s) → ghép lớp chuyển động thành **một dải liền**, lấp khoảng trống bằng khung trong suốt, overlay một lần.
4. **Cảnh sau khi a-roll hết** làm ffmpeg treo → kẹp `-ss` trong độ dài a-roll.
5. Logo nguồn ở mép → khung cắt không vượt qua logo.
6. **Bộ dò bố cục nhầm** (người nói ô lớn + hộp slide bị xếp là "slide" → cắt ra nửa mặt; màn hình demo bị ghi "?"): luôn xem khung đại diện bằng mắt và sửa tay.
7. **Khung gốc làm phụ đề đè chữ slide** → đặt khung gốc trong cửa sổ phía trên, phụ đề dưới cửa sổ.
8. Tư liệu tự quay có đoạn màn đen chữ teaser giữa clip: lưới 1 khung/giây không bắt được → dò độ sáng **từng khung** ở đoạn thực sự dùng.
9. Cảnh W/S2/O trong đoạn ô người nói tí hon → vỡ hạt/cắt nhầm. Chỉ dùng B ở đó.

## Chữ
10. `.dong { width: max-content }` thiếu → phụ đề 2 dòng co còn nửa cỡ.
11. Câu vắt qua thẻ giấy → tách câu tại ranh giới cảnh (mực trên giấy, trắng trên nền tối).
12. Đo đáy chữ lúc chữ đứng yên.
13. **"ai ai" = AI**: bộ lọc nói hụt từng bỏ một nửa → phụ đề "ai". Đã chặn; vẫn quét "ai" đứng riêng và đọc ngữ cảnh.
14. **"việt nam" viết thường** vì luật "người việt" chạy trước "việt nam" → luôn khai cụm dài trước.
15. Bong bóng lời kéo sang cảnh khác kiểu → đè mặt. Phụ đề đặt cạnh mặt so le lệch trái → tràn 80%.
16. Chip chương đè đầu người nói ở góc trên trái → ẩn chip khi đầu chạm góc.

## Tiếng
17. Chuỗi giọng cũ (dynaudnorm m 8/15) kéo to tiếng ồn khoảng nghỉ → m ≤ 6 + RNNoise + cổng êm.
18. Bài nhạc có đuôi tắt dần → đừng lặp bài, nối bài khác.
19. **Đỉnh thật phải đo sau AAC** (WAV −1,1 → MP4 +2,4 dBTP).
20. **Sửa code bằng thay chuỗi lớn có thể xoá mất dòng quan trọng** (đã từng mất dòng thay file tạm vào file chính → file giao vẫn là bản cũ, log in số đẹp). Sau mỗi lần vá: đọc lại hàm, kiểm giờ ghi và dung lượng file giao.

## Quy trình
21. Phần mở đầu lấy từ giữa bài → lọc sạn **từng phần riêng**; chỉ nối hai khoảng giữ khi liền kề thật.
22. Chạy song song 4 tiến trình thỉnh thoảng lỗi thoáng qua → chạy lại riêng video lỗi. Đừng để hai tiến trình cùng ghi một file giao.
23. Vá file bằng heredoc dễ mất `\` và `\n` → dùng công cụ sửa file hoặc `chr(10)`.
24. Console Windows mặc định cp1252 → in chữ Việt lỗi; đặt `stdout.reconfigure(encoding="utf-8")`.
25. Thư viện tách nền (rembg) có thể bị chặn bởi phiên bản scipy → dựng môi trường riêng cho bước bìa.
26. Kế hoạch đọc lúc khởi động động cơ: sửa kế hoạch khi động cơ đang chạy **không** có tác dụng cho lượt đó → dựng lại lớp chữ sau.
