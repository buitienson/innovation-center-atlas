# Innovation Center Atlas

Trang web tham khảo cá nhân (không phải văn bản HaUI/Bộ) — 6 tab: bản đồ toàn cầu (quả cầu
3D + lược đồ khu vực) các trung tâm nghiên cứu/CGCN/ĐMST của đại học trên thế giới, mạng
lưới ĐMST Việt Nam (HANISA, VNEI, các quỹ), xếp hạng ĐMST đại học, Tin tức ĐMST hằng ngày,
Fund/Hackathon (nguồn tài trợ/cuộc thi/đề xuất nhiệm vụ KHCN&ĐMST đang mở), và Thuật ngữ
(glossary ĐMST/khởi nghiệp/chính sách, có liên kết chéo giữa các mục). Tin tức + Fund/
Hackathon do routine tự động hằng ngày cập nhật (xem `_claude/routine-tin-tuc.md`); các
mục còn lại Sơn tự sửa tay khi cần.

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
**Lần cuối:** 2026-09-06 — thêm tab thứ 6 **"Thuật ngữ"** (Glossary), theo gợi ý của sếp
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

---
**Lần trước:** 2026-09-06 — ba việc:

1. **Thêm tab thứ 5 "Fund/Hackathon"** — danh mục nguồn tài trợ/cuộc thi/hackathon/thông
   báo đề xuất nhiệm vụ KHCN&ĐMST, ưu tiên nguồn Việt Nam (Bộ KH&CN, NAFOSTED, NATIF, Sở
   KHCN Hà Nội/TP.HCM/Đà Nẵng) trước quốc tế. Tham khảo cách trình bày mục "Tìm kiếm Hội
   nghị, hội thảo" của `tra-cuu-tap-chi.pages.dev` (thẻ card, badge hạn nộp đổi màu theo
   mức khẩn — đỏ ≤7 ngày/cam ≤30/xanh còn xa, "còn N ngày"). Có chip lọc theo loại
   (hackathon/cuộc thi/quỹ tài trợ/đề xuất nhiệm vụ), ô tìm kiếm, toggle "chỉ hiện còn
   hạn" (mặc định bật). 19 mục ban đầu, mỗi mục đã tra web trực tiếp và có link nguồn thật
   — mục nào không xác minh được ngày cụ thể thì để `deadline:null` (hiện "Xem hạn tại
   trang chính thức"), không bịa ngày. Loại khỏi danh sách: "VICEE Israel Hackathon" (không
   tìm được nguồn công khai — chỉ có trong hồ sơ nội bộ, không đạt chuẩn "phải có link
   nguồn thật" của trang) và "Samsung Solve for Tomorrow 2026" (đã dừng nhận hồ sơ mới
   nhưng không có ngày đóng cụ thể để gắn vào mô hình dữ liệu deadline-based).
2. **Nối mục Fund/Hackathon vào routine `atlas-tin-tuc` hằng ngày** — routine (cả bản
   local lẫn cloud, canonical tại `_claude/routine-tin-tuc.md`) nay làm hai việc độc lập
   mỗi lượt chạy: Phần A tìm tin cho `NEWS[]` (như cũ), Phần B tìm cơ hội tài trợ/cuộc
   thi/hackathon/đề xuất nhiệm vụ KHCN&ĐMST **đang mở**, ưu tiên Việt Nam, cho `FUNDING[]`
   — tối đa ~2-3 mục/lượt, bỏ qua phần nào không có gì đủ tin cậy (không có nghĩa là lỗi),
   không bịa hạn nộp (`deadline:null` nếu không xác minh được), chỉ thêm mục còn actionable
   (mục đã đóng hạn thì không thêm, khác với `NEWS[]` vốn là log lịch sử). Cả hai mảng
   commit chung một lượt. Đã cập nhật mô tả skill `atlas-tin-tuc` (global,
   `~/.claude/skills/`) để phản ánh phạm vi mới.
3. **Sửa thông báo fallback quả cầu 3D** — trước đây hễ `initGlobe()` lỗi vì bất kỳ lý do
   gì (kể cả three.js tải từ cdnjs.cloudflare.com bị chặn bởi Tracking Prevention/ad-blocker
   của trình duyệt, hoặc mạng chập chờn) đều hiện chung một câu "thiết bị không hỗ trợ
   WebGL" — sai và gây hiểu lầm khi WebGL thực ra vẫn chạy tốt. Nay tách hai trường hợp
   (`webglAvailable()` false → thật sự không hỗ trợ; `window.THREE` chưa có dù WebGL vẫn
   chạy → thư viện bị chặn/lỗi tải) với hai thông báo khác nhau, và thêm một lần thử tải
   lại từ cdn.jsdelivr.net trước khi bỏ cuộc. Bắt nguồn từ việc sếp báo Edge trên MacBook
   không mở được quả cầu dù hôm trước vẫn chạy bình thường.

Đã build, kiểm `node --check` + cân bằng thẻ, test bằng http.server + browser (cả tab mới
+ đổi ngôn ngữ EN + giả lập chặn CDN để xác nhận thông báo mới đúng), publish Artifact,
`git push` (commit `e17b367` → `b77a59d`, gồm cả bản cập nhật routine ở mục 2).

Việc mở còn lại: pill Góp ý chờ link Google Form từ sếp; mục 24-category của WURI (cần tải
lại PDF, bản trích cũ đã mất theo scratchpad phiên trước); thêm case flagship mới; theo dõi
lượt chạy routine đầu tiên có Phần B để xem chất lượng mục `FUNDING[]` tự thêm.
(Claude)
