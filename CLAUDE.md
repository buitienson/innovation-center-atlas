# Innovation Center Atlas

Trang web tham khảo cá nhân (không phải văn bản HaUI/Bộ) — 6 tab: bản đồ toàn cầu (quả cầu
3D + lược đồ khu vực) các trung tâm nghiên cứu/CGCN/ĐMST của đại học trên thế giới, mạng
lưới ĐMST Việt Nam (HANISA, VNEI, các quỹ), xếp hạng ĐMST đại học, Tin tức ĐMST hằng ngày,
Fund/Hackathon (nguồn tài trợ/cuộc thi/đề xuất nhiệm vụ KHCN&ĐMST đang mở), và Thuật ngữ
(glossary ĐMST/khởi nghiệp/chính sách, có liên kết chéo giữa các mục). Tin tức + Fund/
Hackathon do routine tự động hằng ngày cập nhật (xem `_claude/routine-tin-tuc.md`); danh
mục mở rộng (`ROSTER`, ~786 mục ở tab Toàn cầu) có sẵn hạ tầng cho một routine hằng ngày
**riêng** chạy trên Gemini (không tốn token Claude) để mở rộng dần (xem
`_claude/routine-roster-grow.md` — **hiện đang CHẶN**: key Gemini hiện có bị 0 hạn mức
Google Search grounding, cần sếp quyết định hướng đi tiếp — đọc mục "Tình trạng hiện tại"
trong file đó); các mục còn lại Sơn tự sửa tay khi cần.

**Live:** https://buitienson.github.io/innovation-center-atlas/
**Artifact (bản xem/sửa nhanh):** https://claude.ai/code/artifact/175ea757-eca9-4a87-acc8-47981ab5b129
**GitHub:** https://github.com/buitienson/innovation-center-atlas

## Cấu trúc

- `src/atlas.html` — **file nguồn để sửa**. Một fragment HTML/CSS/JS gộp (không có
  `<html>/<head>/<body>`, đúng khuôn của Artifact tool), dán thẳng vào `Artifact.publish`
  khi cần xem/sửa trên claude.ai.
- `build.py` — bọc `src/atlas.html` thành `index.html` chuẩn (thêm DOCTYPE/html/head/body)
  để deploy GitHub Pages. Chạy `python3 build.py` sau mỗi lần sửa `src/atlas.html`.
- `index.html` — bản đã bọc, **generated, đừng sửa tay** — sửa `src/atlas.html` rồi build lại.
- Repo git riêng, remote trỏ thẳng GitHub Pages — `git push` là lên live ngay.

## Quy trình sửa

1. Sửa `src/atlas.html`.
2. `python3 build.py` để tái tạo `index.html`.
3. Kiểm nhanh: `node --check` trên script inline (script >10000 ký tự) + đếm cân bằng thẻ
   `div/section` trước khi publish.
4. Nếu cần xem/sửa trên claude.ai: `Artifact.publish` với nội dung `src/atlas.html`
   (dùng `url` của Artifact ở trên để cập nhật đúng bản cũ, đừng tạo Artifact mới).
5. `git add -A && git commit && git push` để lên GitHub Pages.

## Nguồn tham khảo còn lưu (không thuộc kho git, tránh phình repo)

Các file thô dùng để dựng dữ liệu (roster CGCN/TTO thế giới ~786 mục, geocode cache, PDF
WURI ranking đã tải, script cào/gộp dữ liệu) đang nằm ở thư mục scratchpad của phiên làm
việc — **sẽ mất khi phiên kết thúc**. Cần giữ lâu dài thì chuyển thủ công vào
`01-nguon/` ở đây trước khi đóng phiên.

## Quy tắc nội dung — nhắc lại vì đã bị vi phạm nhiều lần trong lúc dựng

**Không đưa bình luận về quy trình/phương pháp thu thập dữ liệu lên trang công khai.**
Không viết kiểu "nguồn X bị lỗi", "chưa xác minh", "kết quả tìm kiếm diện rộng chưa thẩm
định" vào các trường `org`/`caveat`/ghi chú hiển thị cho người đọc — chỉ giữ sự thật khách
quan, hữu ích (vd "năm tài chính kết thúc 30/6" thì được, "agent tải PDF bị lỗi" thì không).
Sếp đã bắt bỏ đúng loại nội dung này nhiều lần (screenshot legend/ghi chú phân loại, danh
sách Miền Bắc/Miền Nam không đại diện, disclaimer trên quả địa cầu).

---
**Lần cuối:** 2026-09-08 — commit mới nhất `3657795`. Thêm tab **Fund/Hackathon** (21 mục,
nối vào routine tin tức hằng ngày) và tab **Thuật ngữ/Glossary** (30 mục, liên kết chéo).
Phóng to quả cầu 3D chiếm gần trọn màn hình, bỏ hẳn lưới wireframe kinh/vĩ tuyến, sửa thông
báo fallback phân biệt đúng "máy không hỗ trợ WebGL" với "thư viện tải lỗi". Đổi tên site:
"Atlas of University Innovation Centers"→"Atlas of Innovation Centers",
"Atlas Trung tâm Nghiên cứu, Đổi mới sáng tạo"→"Atlas Trung tâm Đổi mới sáng tạo". Sửa ghi
chú vùng Đông Nam Á/Việt Nam cho trung thực (tỷ lệ VN áp đảo là do độ sâu thu thập dữ liệu
khác nhau giữa các nước, không phải một phát hiện thật).

**Xác nhận quả cầu 3D lỗi trên máy sếp là driver GPU hỏng ở hệ điều hành** — dùng
`claude-in-chrome` xem trực tiếp Edge/Chrome thật của sếp, `edge://gpu` báo
`VENDOR=0x0000 DEVICE=0x0000`, mọi hardware-acceleration "Disabled" — không phải lỗi code.
Sếp đã khởi động lại máy sau đó nhưng **CHƯA XÁC NHẬN** `edge://gpu` đã ra số thật chưa, cũng
chưa xác nhận lỗi font tiếng Việt vỡ dấu (ảnh chụp trước đó) đã hết chưa — việc mở.

**Dựng xong hạ tầng mở rộng `ROSTER` bằng Gemini** (không tốn token Claude), đã chạy tay
thành công, chưa lên cloud routine tự động: `_claude/tools/roster_common.py` (module dùng
chung, có `check_url()` — lưới an toàn chống Gemini bịa URL, đã vá 4 lớp false-positive thật
lúc dựng: trang parking domain HTTP 200, JS redirect ẩn tới trang parking, site thật bị coi
nhầm "thin" vì `<head>` dài, site thật dùng redirect cùng dạng với trang parking — giải quyết
bằng cách theo dấu redirect 1 bước rồi mới phán). `roster_grow_worker.py` thêm tổ chức MỚI từ
một URL nguồn cụ thể (dùng Gemini `url_context`, KHÔNG dùng `google_search` — quota
`google_search` trên key hiện có = 0 không billing, đã xác nhận qua nhiều lần test).
`roster_fill_websites.py` điền `url` còn thiếu cho mục đã có sẵn. Kết quả thật đã merge:
điền 97 `url` còn thiếu, thêm 25 mục Đông Nam Á có thật đã kiểm sống từng URL (Malaysia
4→23, Indonesia +3, Philippines +1, Thailand +2, dùng nguồn `itma.my` cho Malaysia).

Số liệu hiện tại (đếm lại bằng script Python đọc `src/atlas.html`, đừng chép số cũ):
`ROSTER` **811** (221 còn thiếu `url`), `NEWS` 9, `FUNDING` 21, `TERMS` 30.

**Việc mở, ưu tiên rõ theo yêu cầu của sếp**: rà cho hết Đông Nam Á lên "chuẩn" TRƯỚC khi mở
rộng Châu Á/thế giới. Malaysia đã có độ sâu thật; Thái Lan/Indonesia/Philippines mới nhích
nhẹ; Singapore/Campuchia/Myanmar/Brunei chưa động tới. Bước kế tiếp: tìm nguồn danh bạ thật
cho từng nước còn thiếu (kiểu `itma.my`), chạy `roster_grow_worker.py --source-urls <url>`.

**Cạm bẫy:** `_claude/roster-grow-queue.md` (38 `[pending]`/1 `[done]`) KHÔNG khớp việc thật
đã làm (Malaysia/Indonesia/Philippines/Thailand đã có tiến triển nhưng chưa đánh dấu trong
file này) — đừng tin số trong file đó, kiểm ROSTER thật bằng script.

Chi tiết đầy đủ (kể cả câu lệnh tiếp tục) ở `Brain/_shared/so-ban-giao.md`, mục
`2026-09-08 · Innovation Center Atlas`.

**Lần trước:** 2026-09-07 — routine tự động thêm 2 tin + 2 cơ hội tài trợ/cuộc thi vào
`src/atlas.html` (RND to Startup 2026, VK Connect 2026, đặt hàng nhiệm vụ KH&CN cây Bách bộ
VQG Xuân Sơn). Đã build + kiểm + commit + push. Chưa publish lại Artifact (routine tự động
không tự làm bước này).
(Claude)
