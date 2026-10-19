# 03 — KIẾN TRÚC CẢNH & KẾ HOẠCH SẢN XUẤT

> Mục tiêu: dựng **một lần**, dùng lại cho **nhiều tập**. Mỗi tập mới chỉ thêm ~20–30% asset mới.

---

## 1. Kiến trúc asset — 3 tầng

```
TẦNG A — CỐ ĐỊNH (dựng 1 lần, dùng mọi tập)
 ├─ Nhân vật: MẦM (rig + 7 trạng thái lá L0–L6 + 12 biểu cảm mặt)
 ├─ Nhân vật phụ cố định: Bông, Mẹ, Thầy Tũn, Người Áo Mưa Xám
 ├─ Đám đông: 1 thân mẫu + 8 bộ màu áo + 6 phụ kiện (random)
 ├─ Bối cảnh lõi: Phòng Mầm · Ban công chung cư · Hẻm · Lớp học · Xe buýt trường
 ├─ Bộ đồ họa: thẻ LUẬT / VẤN ĐỀ / LUẬT RIÊNG, bộ đếm số, khung letterbox, end card
 └─ Âm thanh: SFX "tách-tách… pốp", jingle 2 s, 3 track nhạc nền (vui / căng / cinematic)

TẦNG B — THEO MÙA (dùng 4–6 tập)
 ├─ Đội trẻ siêu năng lực (Tai Nghe, Mũ Len Đỏ, Găng Vàng…)
 ├─ Xe van, nhà kho ven sông, sân thượng thành phố đêm
 └─ Biến thể Người Áo Mưa Xám (mỗi tập lộ thêm 1 chi tiết)

TẦNG C — THEO TẬP (mới mỗi tập)
 ├─ Bối cảnh/đạo cụ riêng của năng lực (tập 1: thế giới macro — hạt cơm, giọt nước, kiến)
 ├─ Infographic khoa học riêng
 └─ Hiệu ứng năng lực riêng (VFX)
```

## 2. Danh mục bối cảnh tập 1

| Mã | Bối cảnh | Tầng | Shot dùng | Ghi chú dựng |
|---|---|---|---|---|
| S01 | Phòng Mầm (chung cư) | A | 1.1–1.2, 3.11, 7.1 | Cửa sổ nhìn ra hẻm, gầm giường có tất đỏ (giữ nguyên mọi tập) |
| S02 | Ban công tầng 5 + hẻm | A | 1.3–1.5, 4.7, 5.18 | Có cây chuối dưới hẻm (đáp ở 5.19) |
| S03 | Xe buýt trường (trong) | A | 1.7–1.9 | Ghế xanh, cửa sổ vàng |
| S04 | Vũ trụ nguyên tử / sân vận động | C | 2.2–2.4 | Toàn đồ họa phát sáng trên nền tối |
| S05 | Nhà ngoại ngày Tết (flashback) | C | 3.1–3.5 | Grading ấm + vignette |
| S06 | Lớp học | A | 3.9, 4.3–4.4 | |
| S07 | Thế giới MACRO (bàn ăn, ly trà sữa, hạt cơm, giọt nước, lá chuối, tổ kiến) | C | 4.2, 4.5, 5.2–5.23 | **Bối cảnh quan trọng nhất tập 1** — DOF rất nông, bokeh lớn |
| S08 | Hội chợ trường đêm | B | 6.1–6.10 | Đèn dây, gian hàng mái tôn |
| S09 | Nhà kho ven sông | B | 7.7–7.20 | Ánh trăng xuyên mái, bụi bay |
| S10 | Đường phố + xe van | B | 7.2–7.5 | |

## 3. Quy chuẩn hình ảnh

| Hạng mục | Quy chuẩn |
|---|---|
| Phong cách | 3D low-poly, flat shading, rim-light màu kem; không texture chi tiết |
| Bảng màu | Nền: tím đêm #1B1A2E, be #E8DCC4, xanh trời nhạt. Nhân vật: cam #FF7A1A, xanh lá #7BC950, kem #F3E9D2 |
| Ánh sáng theo hồi | H1–H5: sáng, bão hòa vừa · H6–H7: tối, tương phản cao, đèn đơn sắc (cam/tím) |
| Khung hình | 1920×1080, 24 fps. H6–H7 letterbox 2.39:1 (thanh đen 138 px mỗi bên) |
| Camera | Ống kính ảo 35 mm (thường), 100 mm macro (thế giới tí hon), lia/đẩy chậm liên tục |
| Thế giới macro | DOF f/1.4 ảo, hạt bụi lơ lửng, vật thể thật (hạt cơm, giọt nước) dùng shader bán trong suốt |

## 4. Hai quy trình sản xuất (chọn 1 theo nguồn lực)

### Quy trình A — 3D Blender (chất lượng ổn định, giống video gốc nhất)

| Bước | Công cụ | Đầu ra |
|---|---|---|
| 1. Kịch bản + phiếu tập | Google Docs / file MODULE_MOI | Storyboard dạng bảng (như 02) |
| 2. Lồng tiếng nháp | TTS (Vbee, FPT.AI, ElevenLabs) | Track VO nháp để căn timing |
| 3. Animatic | Blender Grease Pencil / ảnh tĩnh trên timeline | Video nháp đúng thời lượng |
| 4. Dựng & animate | Blender (EEVEE) | Render từng shot |
| 5. VO chính | Thu giọng thật hoặc TTS đã chỉnh | WAV 48 kHz |
| 6. Dựng phim + chữ + SFX | DaVinci Resolve / Premiere / CapCut | Bản 16:9 |
| 7. Cắt Shorts | CapCut (reframe 9:16) | 5 Shorts |

### Quy trình B — AI tạo hình (nhanh, rẻ, cần kiểm soát đồng bộ)

| Bước | Công cụ gợi ý | Mẹo giữ nhất quán |
|---|---|---|
| 1. Model sheet Mầm | Midjourney / Flux / Ideogram | Dùng prompt cố định ở MODULE_MOI §2.5, chọn 1 ảnh gốc làm **character reference** |
| 2. Ảnh key cho từng shot | Cùng công cụ, bật character reference + style reference | Luôn ghi trạng thái lá "sprout state: L_" vào prompt |
| 3. Ảnh → video 3–5 s | Kling / Runway / Veo / Hailuo | 1 hành động/shot, camera đơn giản |
| 4. VO | TTS tiếng Việt (giọng nam trẻ, hơi hài) | Giữ cùng 1 giọng, cùng tốc độ cho cả series |
| 5. Dựng | CapCut / Premiere | Chữ trên màn hình làm **trong phần mềm dựng**, không để AI vẽ chữ |

> Khuyến nghị: bắt đầu bằng **Quy trình B** để test thị trường 3–5 tập, rồi chuyển sang A khi kênh có lượt xem ổn định (A cho nhân vật đồng nhất 100%, quan trọng cho merch).

## 5. Lịch sản xuất 1 tập (chu kỳ 14 ngày)

| Ngày | Việc | Người phụ trách | Kiểm tra |
|---|---|---|---|
| 1–2 | Chọn chủ đề, điền Phiếu tập, nghiên cứu + kiểm chứng số liệu | Biên kịch | Bảng §5 file 01 |
| 3–4 | Viết storyboard + VO | Biên kịch | Checklist 4.1 file 01 |
| 5 | TTS nháp + animatic | Dựng phim | Thời lượng ±5% |
| 6–10 | Dựng hình/animate (hoặc gen AI) | Hoạ sĩ 3D / AI operator | Checklist 4.2 |
| 11 | VO chính + nhạc + SFX | Âm thanh | Checklist 4.3 |
| 12 | Dựng tổng, chữ, letterbox, end card | Dựng phim | Xem lại toàn bộ 1 lượt |
| 13 | Thumbnail ×3 phương án, tiêu đề ×3, cắt 5 Shorts | Thiết kế | Checklist 4.4 |
| 14 | Đăng tập dài + lên lịch Shorts | Quản lý kênh | |

## 6. Kế hoạch phát hành & tăng trưởng

| Thời điểm | Hành động |
|---|---|
| T−3 ngày | Đăng Short #1 (cold open) làm teaser, cuối Short: "Tập đầy đủ thứ Bảy" |
| T0 (thứ Bảy 19:00) | Đăng tập dài. Ghim bình luận câu hỏi đôi |
| T+1 → T+5 | Mỗi ngày 1 Short (#2→#5), mỗi Short gắn link "Related video" về tập dài |
| T+7 | Community post: thăm dò "Tập sau Mầm nên có năng lực gì?" (4 lựa chọn từ ngân hàng chủ đề) |
| Liên tục | Trả lời bình luận dưới tên "Mầm" (giọng nhân vật) — tăng gắn kết |

**Chỉ số theo dõi:** CTR thumbnail ≥ 6% · Giữ chân 30 s đầu ≥ 70% · AVD ≥ 45% · Shorts → tập dài ≥ 2% click.

## 7. Lộ trình mùa 1 (6 tập)

| Tập | Năng lực | Bông / cốt truyện mùa | Manh mối Người Áo Mưa Xám |
|---|---|---|---|
| 1 | Thu nhỏ bằng con kiến | Bông lộ năng lực phóng to | Giữ chiếc tất đỏ; miễn nhiễm LUẬT 3 |
| 2 | Dừng thời gian | Gặp "Mũ Len Đỏ" — người dừng thời gian | Vẫn cử động khi thời gian dừng |
| 3 | Tàng hình | Đội bị theo dõi | Nhìn thẳng vào Mầm đang tàng hình |
| 4 | Thở dưới nước | Cứu người dưới sông Sài Gòn | Để lại dấu chân khô trên mặt nước |
| 5 | Đọc suy nghĩ | Bông nghi ngờ đội | Đầu óc bà ấy hoàn toàn **im lặng** |
| 6 | Nhân bản chính mình | Lộ mặt Người Áo Mưa Xám? | Bà ấy cũng đi tất lệch… |

## 8. Ngân sách tham khảo / tập (Quy trình B)

| Khoản | Ước tính |
|---|---|
| Gói AI hình + video (tháng) | 30–100 USD |
| TTS tiếng Việt | 10–25 USD |
| Nhạc license | 0 (YouTube Audio Library) – 15 USD |
| Thời gian | 40–60 giờ người / tập (1–2 người) |

> Số tiền chỉ là ước tính tham khảo — giá công cụ thay đổi thường xuyên, hãy kiểm tra lại trước khi đăng ký.
