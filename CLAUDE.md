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
**Lần cuối:** 2026-09-05 — bốn việc trong cùng một phiên:

1. **Cột Quốc gia bảng Xếp hạng** — điền đủ 100/101 dòng (tra độc lập qua web search, không
   phải từ WURI — chú ý các tên trùng nhiều trường thật: "Franklin University" → Thuỵ Sĩ không
   phải Ohio, "Saint Louis University" → Philippines không phải Missouri). Dòng "Trinity College"
   (hạng 73) để trống vì không xác minh được — ghi rõ trong `RANKINGS_SOURCE_NOTE`. Thêm
   Bangladesh + Campuchia vào bảng ISO2→cờ.
2. **Routine tự động thêm tin ĐMST hằng ngày** — skill `atlas-tin-tuc` (global, tại
   `~/.claude/skills/`) trỏ tới file canonical **trong chính repo**:
   `_claude/routine-tin-tuc.md` (để cloud routine clone repo là đọc được ngay, không cần máy
   Sơn). Routine cloud `"Atlas - tin ĐMST hàng ngày"` (`trig_01D8yWiiAKk8kzQbBoPsVrwD`) chạy
   06:00 giờ VN mỗi ngày, tự tìm tin + build + `git push` thẳng lên `main` nếu tìm được tin đủ
   tin cậy (đã xác nhận trước, routine không hỏi lại). Không có tin phù hợp thì tự bỏ qua lượt.
   Quản lý/xem log tại claude.ai/code/routines.
3. **Sửa lỗi hiển thị mục Tin tức** — `.news-summary` là thẻ `<p>` nên bị dính luật chung
   `p{max-width:65ch}`, chữ bị bó hẹp dù card rộng — đã gỡ. Thêm ảnh thumbnail cho mỗi tin, lấy
   từ `og:image` thật của chính bài gốc (6/7 tin có, 1 tin — Oxford — nguồn không có og:image
   nên để trống, không chèn ảnh giả). Routine tự động ở mục 2 cũng đã cập nhật để lấy `image`
   cho tin mới thêm sau này.
4. **Thêm pill "Hướng dẫn sử dụng"** cạnh "Về dự án" — hướng dẫn ngắn song ngữ (tương tác quả
   cầu/bản đồ, lọc bảng Xếp hạng, đọc tin). **Pill "Góp ý" (Google Form) CHƯA làm** — Drive API
   ở đây không tạo được Google Form (chỉ Docs/Sheets/Slides), sếp tự tạo form ở forms.new rồi
   gửi link để gắn vào pill.

Đã build, kiểm `node --check` + cân bằng thẻ mỗi lần, test bằng http.server + browser (cả
desktop/mobile), publish Artifact, `git push` cho cả 4 việc (commit `97c3353` → `98e7818`).

Việc mở còn lại: **pill Góp ý chờ link Google Form từ sếp**; mục 24-category của WURI (cần tải
lại PDF, bản trích cũ đã mất theo scratchpad phiên trước); thêm case flagship mới.
(Claude)
