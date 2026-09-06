# Innovation Center Atlas

Trang web tham khảo cá nhân (không phải văn bản HaUI/Bộ) — 6 tab: bản đồ toàn cầu (quả cầu
3D + lược đồ khu vực) các trung tâm nghiên cứu/CGCN/ĐMST của đại học trên thế giới, mạng
lưới ĐMST Việt Nam (HANISA, VNEI, các quỹ), xếp hạng ĐMST đại học, Tin tức ĐMST hằng ngày,
Fund/Hackathon (nguồn tài trợ/cuộc thi/đề xuất nhiệm vụ KHCN&ĐMST đang mở), và Thuật ngữ
(glossary ĐMST/khởi nghiệp/chính sách, có liên kết chéo giữa các mục). Tin tức + Fund/
Hackathon do routine tự động hằng ngày cập nhật (xem `_claude/routine-tin-tuc.md`); danh
mục mở rộng (`ROSTER`, ~786 mục ở tab Toàn cầu) có sẵn hạ tầng cho một routine hằng ngày
**riêng** chạy trên Gemini (không tốn token Claude) để mở rộng dần (xem
`_claude/routine-roster-grow.md` — **routine chưa được tạo trên cloud, chờ sếp nhập
`GEMINI_API_KEY` khi tạo**); các mục còn lại Sơn tự sửa tay khi cần.

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
**Lần cuối:** 2026-09-06 — hai việc, bắt nguồn từ hai lần sếp chỉ ra lỗi thật trong phiên:

1. **Sửa thêm lỗi tải quả cầu 3D** — bản sửa trước (thêm CDN dự phòng, tách thông báo lỗi)
   vẫn còn một lỗ hổng: toàn bộ logic thử-lại chỉ chạy khi sự kiện `load` của trang bắn ra,
   nhưng nếu yêu cầu tải three.js từ CDN đầu tiên **treo** (mạng chập chờn/bị lọc, không hẳn
   là báo lỗi ngay) thì chính `load` cũng có thể không bao giờ bắn — khiến logic thử-lại
   không bao giờ chạy. Đã sửa: bắt đầu tải three.js ngay lập tức (không đợi `load` nữa, chỉ
   lệnh `initGlobe()` mới đợi vì cần layout đã ổn định), và mỗi lần thử tải đua với hạn 8
   giây riêng — treo im lặng cũng bị tính là thất bại thay vì chờ vô thời hạn. Đã tự dựng
   một server cục bộ giữ kết nối mở không phản hồi để xác nhận: bản cũ sẽ treo mãi, bản mới
   time-out đúng ở mốc 8 giây rồi chuyển sang thử CDN dự phòng.
2. **Dựng hạ tầng cho routine mở rộng `ROSTER` bằng Gemini** — sếp muốn "cày" cho hết mọi
   đơn vị ĐMST trên thế giới; đã giải thích không có nguồn nào liệt kê "tất cả" và đề xuất
   thay bằng routine mở rộng theo lô nhỏ, có kiểm soát, chạy trên Gemini để không tốn token
   Claude, dừng khi hết hạn mức. Dùng `EnterPlanMode` để chốt thiết kế trước khi code (sếp
   chọn: **tách routine riêng**, không gộp vào `routine-tin-tuc.md`, vì cần secret
   `GEMINI_API_KEY` riêng). Phát hiện quan trọng khi rà `gemini_worker.py` (skill dùng chung
   `gemini-delegate` ở Brain): script đó **không có khả năng duyệt web**, dùng nguyên trạng
   cho việc tìm tổ chức có thật sẽ khiến Gemini bịa — nên viết script riêng
   `_claude/tools/roster_grow_worker.py`, bật **Google Search grounding** của Gemini API
   (`tools:[{"google_search":{}}]`, đã xác minh qua tài liệu Gemini hiện hành) cộng thêm một
   lớp tự kiểm tra URL còn sống bằng HTTP trước khi tin — đây mới là chốt chặn thật, vì
   grounding giảm chứ không loại bỏ hết khả năng bịa. Đã tạo thêm hàng đợi nguồn
   `_claude/roster-grow-queue.md` (34 mục khởi điểm, ưu tiên Đông Nam Á/Châu Phi/Trung
   Đông/Trung Á — các khu vực mỏng nhất theo đếm thật từ `ROSTER` hiện có, không phải đoán)
   và file hướng dẫn canonical `_claude/routine-roster-grow.md` (cùng khuôn
   `routine-tin-tuc.md`). **Chưa tạo cloud routine thật** — cần sếp tự nhập
   `GEMINI_API_KEY` khi tạo trigger qua skill `schedule`, và nên tự chạy tay
   `roster_grow_worker.py` một lần để kiểm kết quả trước khi để chạy tự động hằng ngày (xem
   mục "Kiểm chứng" trong `_claude/routine-roster-grow.md`).

Đã build, kiểm `node --check` + cân bằng thẻ, publish Artifact, `git push` (commit
`29f2a9d` cho mục 1; mục 2 là file hạ tầng mới, chưa chạm `src/atlas.html`).

Việc mở: sếp cần tự thử lại quả cầu 3D trên Edge/MacBook để xác nhận lỗi 1 đã hết; sếp cần
chạy tay routine mở rộng roster lần đầu + tạo cloud routine hằng ngày cho nó.

---
**Lần trước:** 2026-09-06 — thêm tab thứ 6 **"Thuật ngữ"** (Glossary), theo gợi ý của sếp
khi bàn "cần thêm gì để thành wikipedia ĐMST Việt Nam" — chọn thuật ngữ vì đây là loại nội
dung ổn định (khác tin tức/hạn nộp phải cập nhật liên tục). 30 thuật ngữ, chia 5 nhóm (mô
hình tổ chức, tài chính & đầu tư, công nghệ & ĐMST, chính sách & pháp lý VN, khởi nghiệp
chung), mỗi thuật ngữ có mục "Liên quan" render thành chip bấm được để nhảy tới định nghĩa
liên kết — **đây là điểm liên kết chéo (cross-reference) thật sự đầu tiên của trang**, khác
với 5 tab kia vốn độc lập nhau. Có chip lọc theo nhóm + ô tìm kiếm, giống mẫu UI của tab
Fund/Hackathon.

Hai việc thẩm định trước khi viết nội dung chính sách VN (tránh lặp lỗi cũ về tên bộ đã đổi):
tra web xác nhận ngày/nội dung Nghị quyết 57-NQ/TW (Bộ Chính trị, 22/12/2024) và Nghị quyết
193/2025/QH15 (Quốc hội, 19/2/2025, cho phép viên chức KH&CN công lập tham gia quản lý
doanh nghiệp spin-off) — cả hai đưa thẳng vào mục "Chính sách & pháp lý VN". Riêng mục NIC,
tra thấy Bộ Kế hoạch & Đầu tư (cơ quan chủ quản cũ) đã sáp nhập vào Bộ Tài chính (Nghị định
29/2025/NĐ-CP, 24/2/2025) nhưng **không tìm được nguồn xác nhận NIC đã chuyển về đâu** — nên
định nghĩa NIC cố ý không nêu tên bộ chủ quản cụ thể, chỉ ghi "cơ quan chủ quản đã có thay
đổi qua các đợt sắp xếp bộ máy... tra cổng chính thức của NIC", đúng tinh thần "không bịa dữ
liệu" đã có sẵn ở mục Quy tắc nội dung.

Một lỗi tìm ra khi tự test tính năng "bấm liên quan để nhảy tới định nghĩa": code dùng
`requestAnimationFrame` để trì hoãn việc cuộn trang — nhưng trình duyệt tạm dừng
`requestAnimationFrame` vô thời hạn với tab/pane đang ẩn (bị phát hiện khi tự test bằng
Claude Browser vì pane preview mặc định ở trạng thái ẩn), khiến toàn bộ hành vi cuộn+highlight
lặng lẽ không chạy. Đã bỏ `requestAnimationFrame` vì bước render trước đó (`innerHTML =`)
vốn đã đồng bộ, không cần trì hoãn gì cả — sau khi sửa, xác nhận lại bằng cách kiểm state
DOM trực tiếp (giá trị ô tìm kiếm, chip đang chọn, `boxShadow`, và test tách riêng
`scrollIntoView({behavior:'auto'})` để chứng minh lỗi nằm ở việc trì hoãn chứ không phải ở
logic tìm phần tử).

Đã build, kiểm `node --check` + cân bằng thẻ (không trùng `id` thuật ngữ, không có
`related` trỏ tới id không tồn tại — kiểm bằng script), test cả 6 tab + đổi ngôn ngữ EN bằng
browser, publish Artifact, `git push` (commit `4d3519f`).

Việc mở: các tab khác (Toàn cầu/Việt Nam/Xếp hạng) đang có sẵn đề xuất nâng thành hồ sơ chi
tiết như CASES cho vài đơn vị VN đầu tàu — chưa làm, đây mới là bước "wikipedia hoá" tiếp
theo nếu sếp muốn đi tiếp; xem thêm gợi ý lúc bàn hướng trong lịch sử chat.
(Claude)
