---
name: livestream-video-edit
description: Dựng một buổi livestream / talking head dài thành video ngắn dọc 9:16 (short, Reels, TikTok) và video dài ngang 16:9 (YouTube có chương) bằng code — bóc chữ có mốc từng từ, chọn đoạn theo ý, lọc sạn, cắt cảnh theo bố cục nguồn (mặt, slide, bảng trắng, chia sẻ màn hình), phụ đề chữ động, thẻ chữ, b-roll có sổ bản quyền, nhạc né giọng, chuẩn độ to, làm mờ thông tin riêng tư, tự kiểm rồi tự nhìn khung hình trước khi giao. Dùng khi được nhờ "cắt short từ live", "edit video dài từ buổi live", "làm clip dọc/ngang từ video này", "dựng lại video có phụ đề + b-roll", "làm bìa YouTube + chương + srt", "sửa phụ đề sai chính tả / viết hoa tên riêng", "tiếng to nhỏ không đều", "che thông tin cá nhân trên màn hình", hoặc khi có một file video dài/transcript và cần ra nhiều video thành phẩm. Không dùng cho dựng phim có kịch bản quay mới, hoạt hình thuần, hay chỉ cần sửa một lệnh ffmpeg lẻ.
---

# Dựng video từ livestream — chọn đúng ý, cắt sạch, tự kiểm bằng mắt

## Việc của skill này
Nhận **một video nguồn dài** (livestream, podcast, bài giảng) và yêu cầu kiểu "cắt short", "làm bản dài", trả về:
1. **Video thành phẩm**: short dọc 1080×1920 và/hoặc bản dài ngang 1920×1080, 30 fps, AAC 48 kHz.
2. **Đồ đi kèm**: bìa, phụ đề `.srt`, mốc chương (bản dài), sổ nguồn gốc b-roll/nhạc, file tự kiểm.
3. **Một báo cáo ngắn**: xong gì, ở đâu, cần người nhờ quyết gì, chưa kiểm gì.

## 12 luật gốc (vì sao ở từng dòng)
1. **Brief trước, dựng sau.** Mỗi video có: mục đích, người xem, ý lõi một câu, cảm giác cần để lại, đoạn khó. Mỗi thứ thêm vào (chữ, b-roll, zoom, tiếng động) phải trả lời được "người xem cần cái này lúc này vì ___". Không trả lời được thì bỏ.
2. **Short dựng dày, bản dài tiết chế** — trừ khi người nhờ nói khác. Short: chữ động, thẻ chữ, b-roll ~3s, tiếng động. Bản dài: cắt thẳng là chính, ít chữ nhấn, b-roll có vai trò rõ.
3. **Không bịa chữ trên hình.** Mọi chữ trên hình (hook, thẻ, phụ đề) là lời người nói, được sửa chính tả chứ không được đổi ý. Chữ biên tập duy nhất được phép: tên chương, nhãn nhỏ, thẻ kết do người nhờ cung cấp.
4. **Chữ không bao giờ đè mặt.** Dò mặt, tính vùng mặt trên khung ra, đặt chữ tránh ra. Chữ nằm trong 80% bề ngang giữa và đáy chữ không thấp hơn 79% chiều cao (chừa chỗ giao diện nền tảng).
5. **Không quá 3 giây một khung hình không đổi** (short: trần 3,9s nếu theo khuôn hook). Đổi hình = cắt, đổi cỡ khung, b-roll, thẻ chữ, khung phóng to màn hình. Cắt theo nghĩa, không theo đồng hồ — trần chỉ là lưới an toàn.
6. **Độ to cố định, đo sau khi nén.** Mặc định −12,7 LUFS tích hợp, đỉnh thật ≤ −1 dBTP, **đo trên file MP4 cuối** (AAC có thể làm đỉnh vọt +3 dB).
7. **Tên riêng và thuật ngữ viết đúng** (Việt Nam, người Việt, AI, tên người, tên sản phẩm). Máy bóc chữ trả chữ thường và nghe sai từ mượn — phải có bảng sửa và quét trước khi giao.
8. **Riêng tư trước đẹp.** Thông tin cá nhân hiện trên màn hình nguồn (tên đầy đủ + ngày sinh, số điện thoại, email, hồ sơ trẻ em) phải được dò hết và làm mờ; nội dung nhạy cảm (khẳng định sức khoẻ, lời hứa chưa chắc, câu đùa về tự tử…) thì bỏ và báo lại.
9. **Mọi hình/nhạc ngoài có sổ.** File, nguồn, tác giả, giấy phép, link, ngày tải, dùng ở đâu. Không lấy từ TikTok/YouTube/Facebook của người khác, không lấy từ thư mục "tham khảo".
10. **Mốc từng từ là sự thật, không phải phụ đề tự động.** Chọn đoạn, cắt, dò câu đều trên transcript có mốc từng từ; phụ đề tự động của nền tảng chỉ dùng để **đối chiếu chữ nghe sai**.
11. **Tự nhìn trước khi báo xong.** Chạy tự kiểm máy, rồi mở lưới khung hình bằng mắt. Máy đo không bắt được: chữ sai nghĩa, b-roll lạc đề, khung phóng to vào chỗ trống, thông tin riêng tư lọt.
12. **Không tự đăng, không tự gửi.** Giao file ở máy; đăng, gửi, đẩy code là việc của người nhờ (hoặc hỏi trước).

## Quy trình

### Bước 0 — Nhận việc, dựng brief (hỏi ít, hỏi đúng)
- Xác định: nguồn (file nào, đoạn nào), bao nhiêu video, khổ nào, cho kênh/thương hiệu nào (màu, font, logo, thẻ kết), hạn.
- Chỉ hỏi những gì đổi hướng dựng: thương hiệu/màu, có dùng thông tin khoá học/sản phẩm ở thẻ kết không, có nội dung nào tránh. Còn lại tự suy ra rồi nói rõ đã chọn gì.
- Viết brief ngắn cho từng video + **bản đồ quyết định** (mốc → xử lý → vì sao). Xem `references/01-nguon-va-chon-doan.md`.

### Bước 1 — Bóc chữ có mốc từng từ + đọc bố cục nguồn
- Bóc chữ bằng Whisper (tiếng Việt: PhoWhisper-large bản CTranslate2 qua faster-whisper, `word_timestamps=True`), chuẩn NFC, ghi ra `transcript.json` đúng dạng trong `scripts/chung.py`.
- Tải phụ đề tự động của nền tảng (nếu video đã đăng) để đối chiếu chữ.
- Phân loại bố cục nguồn theo thời gian (mặt toàn khung / slide + ô người nói / người nói lớn + hộp slide / bảng trắng / chia sẻ màn hình / màn đen). Chụp khung đại diện mỗi loại và **tự nhìn**. Xem `references/03-bo-cuc-va-canh.md`.

### Bước 2 — Chọn đoạn
- In transcript theo khoảng (`scripts/in_tu.py`), đọc hết phần định dùng. Đánh dấu: ý lõi, câu móc (hook) mạnh, câu chốt, đoạn phụ thuộc chat/màn hình (thường bỏ), đoạn nhạy cảm.
- Bản dài: 3 câu móc ngắn (2–8s) → thẻ tiêu đề → thân bài nhiều đoạn → chương 4–8. Short: 1 hook là lời thật khớp khuôn hook → thân 45–90s → câu chốt trọn.
- Đổi cụm chữ thành mốc bằng `scripts/moc.py`. Ghi mọi đoạn bỏ kèm lý do vào sổ quyết định (`QUYET`).

### Bước 3 — Kế hoạch dựng (một file cho một video)
Khai trong một file kế hoạch: đoạn (móc/thân), sổ quyết định, câu chốt, thẻ tiêu đề, chương, thẻ chữ, bảng liệt kê, b-roll, từ khoá, bảng sửa chữ, tên riêng giữ hoa, và các khai báo bố cục (khung gốc, bảng trắng, sửa bố cục, vùng che). Lược đồ đầy đủ: `references/02-ke-hoach-dung.md`.

### Bước 4 — Lọc sạn
`scripts/loc_dem.py`: bỏ nói hụt/lặp, tiếng đệm, rút khoảng lặng > 0,55s còn 0,25s, giữ lặng trước câu chốt. Bẫy đã gặp (phủ định, "ai ai" = AI, "mãi mãi") đã cài sẵn — đọc `references/04-phu-de.md` trước khi nới. Nếu cắt mất hơn 1/3 thì dừng và xem lại sổ cắt.

### Bước 5 — Hình phụ
Tìm theo ý câu nói (`scripts/pexels_tim.py`), **duyệt lưới bằng mắt** (ô tối, chữ in, logo, sai ngữ cảnh), tải và ghi sổ (`scripts/pexels_tai.py`). Không đặt b-roll che chỗ màn hình đang là bằng chứng (demo, bảng vẽ). Xem `references/06-hinh-phu-va-ban-quyen.md`.

### Bước 6 — Dựng
Động cơ dựng (tự viết hoặc đã có sẵn ở máy): cắt a-roll theo khoảng giữ → lịch cắt → cảnh (ffmpeg từng cảnh) → lớp chữ/đồ hoạ (HTML + GSAP chụp bằng trình duyệt headless, xuất PNG-in-MOV) → ghép một dải → tiếng. Kiến trúc và các thuật toán cần có: `references/10-dong-co-dung.md`. Short dọc: `references/11-short-doc.md`.
- **Chạy thử khô** (chỉ in lịch khối) trước khi dựng thật: mọi mốc thẻ/b-roll/chương phải khớp; thẻ không chồng chương; b-roll không rơi vào đoạn chỉ có ô người nói tí hon.
- Có thông tin riêng tư → làm mờ ngay ở bước dựng a-roll (mọi cảnh phóng to kế thừa). Xem `references/07-rieng-tu.md`.

### Bước 7 — Tiếng
`scripts/tieng.py`: giọng sạch (RNNoise + khử ồn + nén + cổng êm) → tiếng động → nhạc né giọng → −12,7 LUFS → nén AAC → đo lại trên MP4, vượt trần thì hạ trần làm lại. Xem `references/05-am-thanh.md`.

### Bước 8 — Tự kiểm, tự nhìn, giao
- Máy: độ dài/khung/fps, cảnh dài nhất ≤ 3s, chữ ngoài vùng an toàn = 0, chữ đè mặt = 0, khung đen = 0, NFC, sổ đủ, LUFS/dBTP **trên file cuối**, file tạm không còn sót.
- Mắt: `scripts/luoi_khung.py` lưới 20s toàn video + lưới dày quanh chỗ nghi; quét phụ đề tìm tên riêng viết thường và từ nghe sai; xem bìa (chữ không đè mặt — chọn khung bằng `scripts/mat_tren_bia.py`).
- Giao: đường dẫn file, bảng kết quả, **việc cần người nhờ quyết** (riêng tư, nội dung nhạy cảm, chữ đoán nghĩa), việc chưa kiểm (vd. chưa nghe bằng tai). Checklist đầy đủ: `references/08-tu-kiem-va-ban-giao.md`.

## Khi nào đọc file nào
| Việc | File |
|---|---|
| Brief, chọn đoạn, hook, chương | `references/01-nguon-va-chon-doan.md` |
| Viết file kế hoạch dựng | `references/02-ke-hoach-dung.md` |
| Nguồn có slide / bảng trắng / chia sẻ màn hình | `references/03-bo-cuc-va-canh.md` |
| Phụ đề, lọc sạn, sửa chữ nghe sai, viết hoa | `references/04-phu-de.md` |
| Lọc ồn, nhạc, độ to, đỉnh thật | `references/05-am-thanh.md` |
| B-roll, nhạc ngoài, giấy phép, sổ | `references/06-hinh-phu-va-ban-quyen.md` |
| Thông tin cá nhân, trẻ em, nội dung nhạy cảm | `references/07-rieng-tu.md` |
| Trước khi báo "xong" | `references/08-tu-kiem-va-ban-giao.md` |
| Lỗi đã trả giá — đọc trước mỗi dự án | `references/09-bai-hoc.md` |
| Tự dựng / sửa động cơ dựng | `references/10-dong-co-dung.md` |
| Short dọc, hook, duyệt 60 giây | `references/11-short-doc.md` |

## Script đi kèm (`scripts/`, Python 3.10+, cần ffmpeg trong PATH hoặc biến `FFMPEG`)
| Script | Làm gì |
|---|---|
| `in_tu.py` | In transcript một khoảng giây, đánh dấu khoảng lặng — để đọc và chọn đoạn |
| `moc.py` | Cặp cụm đầu/cuối → mốc cắt chính xác, chừa 0,3s không lấn từ bên cạnh |
| `loc_dem.py` | Lọc nói hụt, đệm, lặng → khoảng giữ + sổ cắt |
| `tieng.py` | Giọng sạch + nhạc né giọng + độ to + đo đỉnh thật sau AAC |
| `pexels_tim.py` / `pexels_tai.py` | Tìm b-roll (API chính thức) + lưới duyệt / tải, chuẩn hoá, ghi sổ |
| `luoi_khung.py` | Lưới khung có mốc giờ thật để tự nhìn |
| `do_mau.py` | Dò mọi giây một trang (có thông tin riêng tư) hiện trên màn hình nguồn |
| `che_vung.py` | Làm mờ vùng theo thời gian |
| `mat_tren_bia.py` | Chọn khung người nói cho bìa để chữ không đè mặt |

Khoá API (Pexels…) chỉ đọc từ biến môi trường; không ghi vào file trong repo, không in ra màn hình.
