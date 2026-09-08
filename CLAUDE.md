# Innovation Center Atlas

Trang web tham khảo cá nhân (không phải văn bản HaUI/Bộ) — 6 tab: bản đồ toàn cầu (quả cầu
3D + lược đồ khu vực) các trung tâm nghiên cứu/CGCN/ĐMST của đại học trên thế giới, mạng
lưới ĐMST Việt Nam (HANISA, VNEI, các quỹ), xếp hạng ĐMST đại học, Tin tức ĐMST hằng ngày,
Fund/Hackathon (nguồn tài trợ/cuộc thi/đề xuất nhiệm vụ KHCN&ĐMST đang mở), và Thuật ngữ
(glossary ĐMST/khởi nghiệp/chính sách, có liên kết chéo giữa các mục). Tin tức + Fund/
Hackathon do routine tự động hằng ngày cập nhật (xem `_claude/routine-tin-tuc.md`); danh
mục mở rộng (`ROSTER`, 839 mục ở tab Toàn cầu — đếm lại bằng script, đừng chép số cũ) có hạ
tầng mở rộng bằng Gemini `url_context` đã chạy tay thành công nhiều lượt (xem
`_claude/routine-roster-grow.md`), **chưa lên cloud routine tự động**; các mục còn lại Sơn
tự sửa tay khi cần.

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
**Lần cuối:** 2026-09-08 (tiếp nữa) — tìm nguồn danh bạ thay thế cho Thái Lan và Indonesia
(việc mở từ lượt trước). Kết quả: `ROSTER` 831 → **839**.

- **Thái Lan (+7)** — tìm ra nguồn RẤT TỐT: `sciencepark.wu.ac.th/rsp` (trang của Đại học
  Walailak liệt kê "เครือข่ายอุทยานวิทยาศาสตร์ภูมิภาค" — mạng lưới 16 trường tham gia chương
  trình Regional Science Park của Bộ ĐH KH&CN Thái Lan, CÓ SẴN link riêng từng trường trong
  HTML — đúng kiểu nguồn tốt như `itma.my`). Chạy `roster_grow_worker.py` trên nguồn này chỉ
  giữ lại 2/16 (Gemini không dùng link có sẵn trên trang, tự đoán domain khác và đa số đoán
  sai) — nên đã lấy trực tiếp 7 link thật `WebFetch` trích được từ HTML nguồn, tự kiểm sống
  bằng đúng hàm `check_url()`, merge tay (giống cách làm với Singapore lượt trước — xem lý do
  ở mục lỗi bên dưới). Thêm: Mae Jo University Science Park, Naresuan University Science
  Park, Mae Fah Luang University Science Park, Phibulsongkram Rajabhat University Science
  Park, Khon Kaen University Science Park, Suranaree University of Technology Science Park
  (Technopolis), SAI Park (Science and Industrial Park, KMUTT — xác nhận qua `WebFetch` đây
  LÀ đơn vị khác với "Knowledge Exploitation and Innovation Center" đã có sẵn trong ROSTER
  cùng trường, không phải trùng lặp). Thái Lan: 6→13.
- **Indonesia (+1)** — không tìm được nguồn danh bạ nhiều-tổ-chức nào dùng tốt. Đã thử:
  `sentraki.dgip.go.id/kampus` (616 tổ chức thật của DJKI nhưng không có link riêng, phân
  trang qua query `?page=N` — xác nhận đổi nội dung thật khi đổi số trang, nhưng đa số là
  trường nhỏ/tôn giáo ít người biết nên Gemini đoán domain sai gần hết; trang chi tiết từng
  tổ chức bị chặn bởi tường lửa Imperva "Error 15" khi truy cập trực tiếp — rủi ro dùng
  nguồn này không ổn định); `id.wikipedia.org/wiki/Taman_sains` (không nhắc tên STP Indonesia
  nào); 2 file PDF (UNESCAP, ADB) mô tả danh sách STP nhưng cả hai đều chặn `WebFetch`/`curl`
  403. Tìm tay từng STP nổi tiếng: `stp.ipb.ac.id` (IPB Science Techno Park) SỐNG, đã merge;
  `stp.unpad.ac.id` (Unpad STP, dù có trong kết quả tìm kiếm) và `technopark.surakarta.go.id`
  (Solo Technopark) đều KHÔNG sống khi kiểm bằng `check_url()` — đã loại. Indonesia: 6→7 (vẫn
  mỏng nhất trong 3 nước ưu tiên — Thái Lan/Philippines đã đủ sâu hơn).

**Lỗi phát sinh khi dùng `roster_grow_worker.py` trên nguồn CÓ SẴN link riêng (khác lỗi false-
positive lượt trước, vốn xảy ra khi nguồn KHÔNG có link):** khi trang nguồn có anchor
`<a href>` thật cho từng tổ chức, Gemini `url_context` vẫn không trích đúng các href đó mà tự
đoán domain khác (đa số đoán sai, bị `check_url()` loại đúng) — nghĩa là công cụ hiện tại
đáng tin khi cần ƯỚC LƯỢNG domain từ tên tổ chức (trường hợp Malaysia/Philippines), nhưng
KHÔNG đáng tin khi cần TRÍCH XUẤT link có sẵn trên trang. Với loại nguồn thứ hai này, cách làm
đúng hiện tại là tự đọc `WebFetch`/trình duyệt lấy href thật rồi tự kiểm `check_url()` — ngoại
lệ này đã áp dụng cho Singapore (lượt trước) và Thái Lan (lượt này), đều ghi rõ trong commit.

**Việc mở, ưu tiên không đổi:** Indonesia vẫn mỏng nhất (7 mục) — cần tìm nguồn danh bạ nhiều-
tổ-chức tốt hơn `sentraki.dgip.go.id` (nguồn thật nhưng khó khai thác vì lý do trên); có thể
thử: PDF khác không bị 403, hoặc trang chính phủ tỉnh/thành liệt kê STP địa phương, hoặc hỏi
sếp có nguồn nào biết sẵn. Campuchia/Myanmar/Brunei vẫn CHƯA ĐỘNG TỚI — độ ưu tiên thấp hơn.

**Lần trước:** 2026-09-08 (tiếp) — làm sâu Đông Nam Á theo đúng ưu tiên đã chốt (SEA "chuẩn"
trước khi mở rộng Châu Á/thế giới). Tìm nguồn danh bạ thật kiểu `itma.my` cho từng nước:

- **Philippines** — nguồn `info.ipophil.gov.ph/itso/itsos-by-region/` (danh bạ CHÍNH THỨC
  của IPOPHL, mạng lưới 77 ITSO — trang render bằng JS, phải đọc qua `get_page_text` sau khi
  trang tải xong, không phải `WebFetch` tĩnh). Chạy `roster_grow_worker.py`, Gemini giữ lại
  14/20 mục sau kiểm sống. Merge tay 13 mục (bỏ "De La Salle University" trùng với mục
  "DLSU Innovation and Technology Office" đã có sẵn trong ROSTER — cùng một đơn vị, khác
  tên), đổi tên mỗi mục thành "<Trường> ITSO" cho khớp quy ước đặt tên hiện có (mục cũ đặt
  tên theo đơn vị cụ thể, không phải tên trường trần). Philippines: 4→17.
- **Singapore** — nguồn `enterprisesg.gov.sg/.../coi-directory` (danh bạ Centres of
  Innovation chính thức của Enterprise Singapore). `roster_grow_worker.py` KHÔNG dùng được ở
  đây — xem lỗi mới bên dưới. Đã tự kiểm sống 7 URL thật (lấy từ nội dung trang qua
  `WebFetch`, kiểm lại bằng đúng hàm `check_url()` trong `roster_common.py` cho cùng mức độ
  nghiêm ngặt) rồi merge tay — **đây là ngoại lệ, không qua worker**, vì worker không trích
  được link riêng từng trung tâm từ trang này (xem bên dưới). Singapore: 3→10.
- **Indonesia** — thử nguồn `sentraki.dgip.go.id/kampus` (danh bạ Sentra KI chính thức của
  DJKI, 616 tổ chức, phân trang) — chỉ giữ được 1/12 mục sau kiểm sống, và mục đó cũng dính
  lỗi mới nên đã loại (xem bên dưới). Trang chỉ hiện 12 mục ở trang 1 (phân trang JS, không
  đổi URL) nên nguồn này cần cách khai thác khác (duyệt bằng trình duyệt thật + phân trang
  tay) mới dùng được — CHƯA làm được lượt này, để lại việc mở.
- **Thái Lan** — chưa tìm được một trang danh bạ tổng hợp có link riêng từng đơn vị (mạng
  lưới UBI của Bộ ĐH KH&CN Thái Lan — trang `mua.go.th` cũ đã chết tên miền; chưa tìm được
  trang thay thế). Để lại việc mở.
- **Campuchia/Myanmar/Brunei** — chưa tìm được nguồn danh bạ thật (chỉ có từng viện lẻ, không
  phải danh bạ nhiều đơn vị). Để lại việc mở, CHƯA động tới.

**Lỗi false-positive MỚI phát hiện + đã vá** trong `roster_grow_worker.py` (không phải
`roster_common.py` — sửa đúng file, không đụng module dùng chung để giữ an toàn): khi trang
nguồn không có link riêng cho từng tổ chức (Indonesia, Singapore ở trên), Gemini có xu hướng
điền URL = CHÍNH TRANG NGUỒN thay vì URL riêng của tổ chức — và trang nguồn dĩ nhiên luôn
"sống" nên lọt qua `check_url()` (hàm đó chỉ kiểm sống/parking/redirect, không so sánh với
nguồn). Đã thêm một điều kiện hẹp trong `roster_grow_worker.py` (không phải `roster_common.py`):
loại bỏ bất kỳ candidate nào có domain trùng domain của chính `--source-urls` đã giao. Test
lại trên Indonesia + Singapore xác nhận lọc đúng (0 mục lọt qua khi không có link riêng).

Số liệu hiện tại (đếm lại bằng script Python đọc `src/atlas.html`, đừng chép số cũ):
`ROSTER` **831** (Philippines 17, Singapore 10, Malaysia 23, Thailand 6, Indonesia 6 —
Campuchia/Myanmar/Brunei vẫn 0), `NEWS` 9, `FUNDING` 21, `TERMS` 30. Đã `python3 build.py`,
kiểm `node --check` + cân bằng thẻ div/section, xem thử bằng `python3 -m http.server` +
Browser pane (số liệu hiển thị đúng trên trang, không lỗi console) trước khi commit + push.

**Việc mở, ưu tiên không đổi**: Thái Lan/Indonesia còn mỏng (6 mỗi nước) — cần tìm cách khai
thác `sentraki.dgip.go.id` qua nhiều trang (phân trang JS, không đổi URL — cần duyệt trình
duyệt thật rồi giao từng trang cho Gemini bằng cách khác, hoặc chấp nhận chỉ lấy trang 1 mỗi
lượt) và tìm nguồn thay cho `mua.go.th` (đã chết) cho Thái Lan. Campuchia/Myanmar/Brunei vẫn
CHƯA ĐỘNG TỚI — ưu tiên thấp hơn làm sâu 2 nước trên trước khi mở nước mới hoàn toàn.

**Cạm bẫy nhắc lại:** `_claude/roster-grow-queue.md` vẫn KHÔNG khớp việc thật đã làm — đừng
tin số trong file đó, kiểm ROSTER thật bằng script (`roster_common.load_roster`).

**Lần trước:** 2026-09-08 (đầu phiên) — dựng xong hạ tầng mở rộng `ROSTER` bằng Gemini
`url_context` (không tốn token Claude), vá 4 lớp false-positive trong `check_url()`
(`roster_common.py`), merge thật 97 `url` còn thiếu + 25 mục Đông Nam Á (Malaysia 4→23,
Indonesia +3, Philippines +1, Thailand +2, dùng nguồn `itma.my` cho Malaysia). Ngoài ra xác
nhận quả cầu 3D lỗi trên máy sếp là driver GPU hỏng ở hệ điều hành (`edge://gpu` báo
`VENDOR=0x0000 DEVICE=0x0000`) — sếp đã khởi động lại máy nhưng CHƯA XÁC NHẬN đã hết lỗi
chưa, cũng chưa xác nhận lỗi font tiếng Việt vỡ dấu đã hết chưa — vẫn là việc mở.

**Lần trước nữa:** 2026-09-07 — routine tự động thêm 2 tin + 2 cơ hội tài trợ/cuộc thi vào
`src/atlas.html` (RND to Startup 2026, VK Connect 2026, đặt hàng nhiệm vụ KH&CN cây Bách bộ
VQG Xuân Sơn). Đã build + kiểm + commit + push. Chưa publish lại Artifact (routine tự động
không tự làm bước này).
(Claude)
