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
**Lần cuối:** 2026-09-06 tối — hai việc chẩn đoán, chưa xong, sếp cần quyết định tiếp:

1. **Quả cầu 3D trên Edge — xác nhận KHÔNG PHẢI lỗi code.** Xin quyền
   computer-use xem trực tiếp Edge của sếp (chỉ xem, không click/gõ được —
   giới hạn cứng của công cụ với trình duyệt): trang tải xong đầy đủ, nhưng
   hiện đúng thông báo "không hỗ trợ WebGL" (`nowebgl`), không phải bản "thư
   viện bị chặn" (`libfail`) vừa sửa tối nay. Nghĩa là `canvas.getContext
   ('webgl')` trên máy/Edge của sếp thật sự trả về null — nguyên nhân nằm ở
   cấu hình máy/trình duyệt (hardware acceleration bị tắt, GPU bị Edge đưa
   vào danh sách chặn...), không phải thứ sửa được từ phía code trang web.
   Cần sếp tự gõ `edge://gpu` khi rảnh (tôi không gõ hộ được) để xác nhận
   nguyên nhân cụ thể — chưa gõ được vì sếp đang dùng điện thoại.
2. **Routine mở rộng ROSTER bằng Gemini — chạy thử thất bại, đã truy đến tận
   gốc.** Test tay bằng key Gemini hiện có (đọc từ `~/.zshrc`, không ghi ra
   file/log) qua cả `roster_grow_worker.py` lẫn `curl` trực tiếp, lặp lại
   nhiều lần trong ~20 phút: gọi Gemini **bình thường** luôn thành công, gọi
   **kèm Google Search grounding** (đúng cái routine cần) luôn **429
   RESOURCE_EXHAUSTED ngay lập tức**. Kết luận: **hạn mức grounding của
   key/project này = 0** (không phải key hết hạn mức chung) — khả năng do
   Google cắt hạn mức miễn phí 50-80% từ 12/2025, và bật billing (nếu chưa
   bật) sẽ xoá toàn bộ hạn mức miễn phí khác chứ không chỉ mở khoá grounding.
   Đã nâng cấp `roster_grow_worker.py` để tự chẩn đoán đúng lỗi này ở mọi lần
   chạy sau (phân biệt "chỉ grounding bị chặn" với "cả key hết hạn mức").
   **Chưa tạo cloud routine** — đã ghi chi tiết đầy đủ + 3 hướng lựa chọn vào
   mục "Tình trạng hiện tại" của `_claude/routine-roster-grow.md`, chờ sếp
   đọc `ai.dev/rate-limit` (cần đăng nhập, tôi không xem hộ được) rồi chọn
   hướng.

Không git push gì cho mục 1 (đã push tối nay trước đó, xem "Lần trước"). Mục
2 chỉ có thay đổi tài liệu + code chẩn đoán (`roster_grow_worker.py`,
`routine-roster-grow.md`) — sẽ commit cùng lúc viết mục này.

Việc mở, cần sếp làm khi rảnh: (1) gõ `edge://gpu`, báo lại dòng WebGL nói gì;
(2) đọc `ai.dev/rate-limit`, quyết bật billing / dùng key khác / đổi routine
sang chạy trên Claude+WebSearch / bỏ tự động hoá — xem 3 lựa chọn trong
`_claude/routine-roster-grow.md`.

---
**Lần trước:** 2026-09-06 — hai việc, bắt nguồn từ hai lần sếp chỉ ra lỗi thật trong phiên:

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
(Claude)
