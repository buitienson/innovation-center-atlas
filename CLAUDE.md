# Innovation Center Atlas

Trang web tham khảo cá nhân (không phải văn bản HaUI/Bộ) — bản đồ toàn cầu (quả cầu 3D
+ lược đồ khu vực) các trung tâm nghiên cứu/CGCN/ĐMST của đại học trên thế giới, mạng lưới
ĐMST Việt Nam (HANISA, VNEI, các quỹ), xếp hạng ĐMST đại học, và một mục Tin tức ĐMST
hằng ngày do Sơn tự cập nhật.

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
**Lần cuối:** 2026-09-06 — hai việc:

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
   **Việc mở:** đây là danh mục tĩnh do Sơn tự thêm tay, **chưa nối vào routine
   `atlas-tin-tuc` hằng ngày** — cần quyết định có nên để routine đó tự phát hiện thông
   báo tuyển chọn/cuộc thi mới rồi ghi thêm vào `FUNDING[]` hay không trước khi làm tiếp.
2. **Sửa thông báo fallback quả cầu 3D** — trước đây hễ `initGlobe()` lỗi vì bất kỳ lý do
   gì (kể cả three.js tải từ cdnjs.cloudflare.com bị chặn bởi Tracking Prevention/ad-blocker
   của trình duyệt, hoặc mạng chập chờn) đều hiện chung một câu "thiết bị không hỗ trợ
   WebGL" — sai và gây hiểu lầm khi WebGL thực ra vẫn chạy tốt. Nay tách hai trường hợp
   (`webglAvailable()` false → thật sự không hỗ trợ; `window.THREE` chưa có dù WebGL vẫn
   chạy → thư viện bị chặn/lỗi tải) với hai thông báo khác nhau, và thêm một lần thử tải
   lại từ cdn.jsdelivr.net trước khi bỏ cuộc. Bắt nguồn từ việc sếp báo Edge trên MacBook
   không mở được quả cầu dù hôm trước vẫn chạy bình thường.

Đã build, kiểm `node --check` + cân bằng thẻ, test bằng http.server + browser (cả tab mới
+ đổi ngôn ngữ EN + giả lập chặn CDN để xác nhận thông báo mới đúng), publish Artifact,
`git push` (commit `e17b367`).

Việc mở còn lại: quyết định có nối routine `atlas-tin-tuc` với `FUNDING[]` hay không (mục 1
ở trên); pill Góp ý chờ link Google Form từ sếp; mục 24-category của WURI (cần tải lại PDF,
bản trích cũ đã mất theo scratchpad phiên trước); thêm case flagship mới.
(Claude)
