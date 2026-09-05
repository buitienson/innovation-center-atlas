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
**Lần cuối:** 2026-09-05 — điền cột Quốc gia cho bảng Xếp hạng WURI Top 100 (đã để trống ở
lần trước vì PDF gốc của WURI không in cột này). Tra cứu độc lập từng trường (không phải từ
WURI) — agent con xác minh qua web search, đặc biệt các tên trùng với nhiều trường thật:
"Franklin University" → Thuỵ Sĩ (Lugano, không phải Ohio), "Saint Louis University" → Philippines
(SLU Baguio, không phải Missouri, khác với "University of Baguio" cũng có trong danh sách),
"National University of Management" → Campuchia. Thêm 2 quốc gia còn thiếu trong bảng ISO2 của
trang (Bangladesh, Campuchia) để hiện đúng cờ. Một dòng ("Trinity College", hạng 73) để trống
vì không xác minh được trong 4 trường thật cùng tên — ghi rõ lý do trong `RANKINGS_SOURCE_NOTE`
thay vì đoán liều. Đã build, kiểm `node --check` + cân bằng thẻ, test live bằng http.server +
browser (xem đúng cờ/tên nước từng dòng), publish Artifact, `git push`.

Trước đó (cùng ngày): dựng nhà cho dự án (trước đó làm hoàn toàn trong scratchpad của phiên
chat, sẽ mất khi đóng phiên): clone lại repo GitHub Pages vào đây, tách `src/atlas.html`
(nguồn để sửa) khỏi `index.html` (bản build qua `build.py`). Điền nốt mục Xếp hạng bằng WURI
Ranking 2026 Top 100 (đồng hạng giữ đúng bản gốc) — **live, commit `e23fce9`.**

Việc mở còn lại: mục 24-category của WURI (cần tải lại PDF, bản trích cũ đã mất theo scratchpad
phiên trước), cập nhật Tin tức, thêm case flagship mới. Xem thêm mục "Chờ điền" nếu có.
(Claude)
