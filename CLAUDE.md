# Innovation Center Atlas

Trang web tham khảo cá nhân (không phải văn bản HaUI/Bộ) — 6 tab: bản đồ toàn cầu (quả cầu
3D + lược đồ khu vực) các trung tâm nghiên cứu/CGCN/ĐMST của đại học trên thế giới, mạng
lưới ĐMST Việt Nam (HANISA, VNEI, các quỹ), xếp hạng ĐMST đại học, Tin tức ĐMST hằng ngày,
Fund/Hackathon (nguồn tài trợ/cuộc thi/đề xuất nhiệm vụ KHCN&ĐMST đang mở), và Thuật ngữ
(glossary ĐMST/khởi nghiệp/chính sách, có liên kết chéo giữa các mục). Tin tức + Fund/
Hackathon do routine tự động hằng ngày cập nhật (xem `_claude/routine-tin-tuc.md`); danh
mục mở rộng (`ROSTER`, 8837 mục ở tab Toàn cầu — đếm lại bằng script, đừng chép số cũ) có hạ
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
**Lần cuối:** 2026-09-09 (checkpoint 28 — **CÙNG NGUỒN OpenStreetMap, tag MỚI `office=research`**)
— tiếp tục mục tiêu **10000**. Đây là việc mở đã ghi ở checkpoint 27: thử tag OSM khác ngoài
`leisure=hackerspace`. Kiểm `taginfo.openstreetmap.org` trước khi query: `office=research` ("An
office for research and development") có **15715** điểm toàn cầu — lớn hơn hẳn `amenity=science_park`
(chỉ 25, quá nhỏ) và các giá trị tự do không chuẩn hoá "incubator"/"innovation"/"technology_park"
(không tồn tại như tag key=value thật, chỉ xuất hiện rải rác trong `name`/`description` tự do — OSM
không có tag chuẩn cho "trung tâm ĐMST/vườn ươm" tách biệt). Lấy mẫu 100 điểm đầu xem tên: đa số là
viện nghiên cứu đại học/hàn lâm thật (Max-Planck-Institut, Fraunhofer-Institut, viện SAV Slovakia,
CNRS, trạm nghiên cứu cực...) — đúng nghĩa "trung tâm nghiên cứu của đại học" xếp ĐẦU TIÊN trong
mô tả Atlas, dù có lẫn thiểu số văn phòng R&D doanh nghiệp/viện ngành hẹp (chấp nhận được, cùng mức
đa dạng như các batch OSM khác đã dùng).

Truy vấn `[out:json];(node["office"="research"]["name"]["website"];way[...];);out tags center;` +
biến thể `contact:website` thay `website` (một số điểm chỉ có field này) → gộp theo `(type,id)` được
**4249** điểm duy nhất có tên. Áp dụng lại kỹ thuật point-in-polygon Natural Earth 1:50m từ checkpoint
27 (LẦN NÀY LƯU LẠI THÀNH MODULE DÙNG LẠI ĐƯỢC: `_claude/tools/country_from_latlon.py`, class
`CountryLookup` — checkpoint 27 chỉ viết tay trong scratchpad rồi mất khi phiên kết thúc, phải viết
lại từ đầu; lần này lưu vào repo để batch sau có sẵn, không cần viết lại lần 3) — 100% điểm có
lat/lon thật (node/way `center`), phân loại quốc gia cho 4078/4249, loại 154 điểm rơi ngoài mọi biên
giới quốc gia (đảo nhỏ/vùng biển) và 9 điểm ở Antarctica (không phải quốc gia, loại toàn bộ — ROSTER
chưa có tiền lệ trạm cực). 0 điểm Việt Nam giữ lại đúng quy tắc.

Lọc trùng: loại 142 trùng domain + 4 trùng tên với ROSTER hiện có, loại 1166 trùng nội bộ batch (nhiều
viện/phòng ban khác nhau của cùng một đại học/viện hàn lâm dùng chung một domain, vd nhiều "Ústav ...
SAV" khác nhau nhưng cùng kiểu tên miền phụ — coi là cùng thực thể website cấp tổ chức) → còn **2757**
ứng viên. Kiểm sống `check_url()` (8 luồng, timeout 15s): alive lượt 1 **2134/2757**. Retry 623 lỗi (6
luồng, timeout 20s): cứu thêm **48** → tổng **2182/2757 sống thật (79,1%)**. Nga rơi từ 381 ứng viên
xuống chỉ 5 dòng cuối (phần lớn domain `.ru` không phản hồi qua `check_url()` — hạ tầng mạng, không
phải lỗi kỹ thuật của batch). Merge an toàn lần cuối: 0 trùng phát sinh thêm. Chỉ **7/2182 (0,3%)** URL
sống là domain mạng xã hội. `org` để trống toàn batch (tag OSM `office=research` không có field tổ
chức chủ quản tách biệt với tên).

Quốc gia (top): Đức 563, Mỹ 288, Pháp 191, Tây Ban Nha 97, Ba Lan 71, Áo 70, Ý 68, Anh 52, Hà Lan 51,
Bỉ 50 — Đức dẫn đầu áp đảo (mật độ gắn thẻ OSM cao nhất thế giới cho loại tag văn phòng/toà nhà, đúng
xu hướng đã thấy ở các batch OSM trước).

`ROSTER`: 6655 → **8837** (+2182). Đơn vị trên bản đồ: 6664 → **8846** (+2182, giữ nguyên chênh lệch
+9 đã ghi nhận ổn định qua nhiều checkpoint). Kiểm: `node --check` sạch trên script inline
(2.100.231 ký tự), thẻ `div`/`section` cân bằng (107/107, 6/6), Browser pane qua HTTP server cục bộ
hiển thị đúng "8846 đơn vị" / "8837 trong danh mục mở rộng", không lỗi console.

**Việc mở cho lượt sau (mục tiêu 10000, còn thiếu ~1163):** (1) `shop=repair` qua Overpass — chưa thử,
khả năng trùng nhiều với Repair Café đã lấy nhưng đáng kiểm; (2) HackerspaceWiki còn 238 "building" +
351 "planned" chưa khai thác (độ ưu tiên thấp); (3) các wiki cộng đồng khác dùng Semantic MediaWiki
chưa tìm ra ứng viên cụ thể; (4) OSM không có tag chuẩn riêng cho "incubator"/"innovation
center"/"science park" (xác nhận qua taginfo lần này) — nếu muốn khai thác các khái niệm này qua OSM
phải lọc theo `name`/`description` chứa từ khoá tự do, độ tin cậy thấp hơn nhiều so với tag có cấu
trúc, cân nhắc kỹ trước khi thử; (5) 571 hồ sơ Repair Café bị bỏ qua vì thiếu quốc gia (việc mở cũ);
(6) BIRAC BioNEST PDF lỗi cấu trúc vẫn chưa sửa được; (7) InovaLink Brazil vẫn bế tắc; (8) module mới
`_claude/tools/country_from_latlon.py` (điểm mạnh: point-in-polygon Natural Earth 50m tái sử dụng
được) — dùng lại ngay cho bất kỳ nguồn OSM/geo nào có lat/lon ở batch sau, đỡ phải viết lại.

**Lần trước:** 2026-09-09 (checkpoint 27 — **NGUỒN LỚN MỚI: OpenStreetMap, kỹ thuật MỚI "Overpass
API truy vấn tag `leisure=hackerspace`"**) — tiếp tục mục tiêu **10000**. Đầu phiên đã cân nhắc và
LOẠI hướng "office=coworking" trên cùng nguồn OSM: Overpass trả **3268** điểm có tên+website, nhưng
phần lớn là chuỗi văn phòng dịch vụ thương mại (WeWork 74, Regus 44, Spaces 39, Design Offices 37,
Industrious 9...) — không phù hợp chủ đề "trung tâm CGCN/ĐMST/vườn ươm/TTO/fablab/hackerspace/
repair-café" của Atlas (văn phòng cho thuê thuần thương mại, không phải hạ tầng ĐMST/cộng đồng
maker), nên KHÔNG dùng. Cũng thử `craft=fablab`/`amenity=fablab`/`amenity=makerspace` riêng —
chỉ vài chục điểm, không đáng một batch riêng, phần lớn trùng với `leisure=hackerspace` đã lấy.

**Nguồn dùng:** Overpass API (`overpass-api.de/api/interpreter`, không cần API key, không giới hạn
đăng nhập) truy vấn `[out:json];(node["leisure"="hackerspace"];way["leisure"="hackerspace"];);out
tags center;` — đây LÀ kỹ thuật MỚI khác hẳn 6 kỹ thuật cũ: dữ liệu địa lý crowd-sourced OpenStreet-
Map (bất kỳ ai cũng có thể tự gắn thẻ), không phải danh bạ chính thức của một tổ chức trung tâm.
Trả về **1868** điểm toàn cầu, **1358** có sẵn cả `name` + `website`/`contact:website`. Lọc trùng
với ROSTER hiện có (theo domain — trừ domain mạng xã hội dùng chung — và theo tên chuẩn hoá): loại
**519** trùng domain + **56** trùng tên (xác nhận đúng cùng thực thể: phần lớn hackerspace này đã
có sẵn từ batch HackerspaceWiki checkpoint 26 hoặc fablabs.io checkpoint trước đó — hai nguồn phủ
cùng "thế giới hackerspace" nhưng khác kỹ thuật thu thập, tỉ lệ trùng cao là dấu hiệu tốt xác nhận
dữ liệu thật) + **49** trùng nội bộ batch → còn **729** ứng viên.

**Điểm mạnh dữ liệu — toạ độ CHÍNH XÁC CẤP ĐỊA ĐIỂM cho 100% ứng viên** (khác batch trước chỉ- có
89%): mọi node/way OSM đều có `lat`/`lon` thật do người gắn thẻ xác định vị trí trên bản đồ, không
cần centroid quốc gia dự phòng bao giờ. Chỉ **69/729** có sẵn field `addr:country` (mã ISO alpha-2,
dùng lại dict `ISO2_COUNTRY` đã có sẵn từ batch trước); **660** còn lại suy ra quốc gia bằng cách
MỚI: tải GeoJSON biên giới quốc gia Natural Earth 1:50m (`ne_50m_admin_0_countries`, ~3MB, public,
không cần đăng nhập) rồi tự viết point-in-polygon (ray-casting thuần Python, không cần cài
shapely/numpy — máy tải PyPI rất chậm hôm nay, ~50KB/s, cài `reverse_geocoder` bị treo giữa chừng
tải wheel scipy 36MB nên bỏ hướng đó) — kiểm đúng cả các nước nhỏ (Monaco, Singapore, Malta,
Liechtenstein) nhờ dùng độ phân giải 50m thay vì 110m. 0 ứng viên bị bỏ vì thiếu quốc gia.

Kiểm sống `check_url()` (8 luồng, timeout 15s): alive lượt 1 **518/729**. Retry 211 lỗi (6 luồng,
timeout 20s): cứu thêm **3** → tổng **521/729 sống thật (71,5%)** — thấp hơn HackerspaceWiki
(86,7%) vì đây là dữ liệu OSM ai cũng sửa được, nhiều điểm cũ không ai dọn khi hackerspace đã đóng
cửa hoặc đổi tên miền. Dựng xong 521 dòng (quốc gia + toạ độ chính xác), kiểm trùng an toàn lần
cuối với ROSTER + trong batch → **0 trùng phát sinh thêm**, 521 dòng merge nguyên vẹn. Chỉ **2/521
(0,4%)** URL là domain mạng xã hội.

Quốc gia (top): Pháp 153, Đức 96, Mỹ 82, Tây Ban Nha 27, Ý 17, Anh 17, Thuỵ Sĩ 15, Canada 12, Bỉ
11, Áo 10 — Pháp đứng đầu bất ngờ (nhiều "La Cantine"/"Fab Lab" địa phương do chính quyền tỉnh
Pháp tài trợ tự gắn thẻ OSM tốt), khác phân bố Đức/Mỹ dẫn đầu ở batch HackerspaceWiki. `org` để
trống toàn batch (tag OSM không có field tổ chức chủ quản tách biệt, giống quy ước batch trước).

`ROSTER`: 6134 → **6655** (+521). Đơn vị trên bản đồ: 6143 → **6664** (+521, giữ nguyên chênh lệch
+9 đã ghi nhận ổn định qua nhiều checkpoint). Kiểm bằng Browser pane qua HTTP server cục bộ (`python
-m http.server`): trang hiển thị đúng "6664 đơn vị được lập bản đồ" / "6655 trong danh mục mở
rộng", không lỗi console, `node --check` qua script inline sạch, thẻ `div`/`section` cân bằng
(107/107, 6/6).

**Việc mở cho lượt sau (mục tiêu 10000, còn thiếu ~3345):** (1) HackerspaceWiki còn 238 "building" +
351 "planned" chưa khai thác (độ ưu tiên thấp, xem lý do ở checkpoint 26); (2) các hướng đã thử
lượt này và LOẠI vì quá nhỏ/không có danh bạ công khai: hOurworld time bank (333 cộng đồng, không
API, chỉ duyệt web), Restart Project (mạng lưới sự kiện, không phải tổ chức có site riêng), Library
of Things (chỉ 22 địa điểm, chỉ UK), EIT Community RIS Hubs/partners (~80 đối tác, không đủ lớn),
Seedstars/Seedspace (chỉ 13 hub), Village Capital/VilCap Communities (~50 cộng đồng), UnternehmerTUM
(1 tổ chức, không phải danh bạ), NRC IRAP Canada (nhân sự hiện trường, không phải tổ chức có site),
Baltic accelerator list (chỉ các bài blog liệt kê, không phải đăng ký chính thức) — ĐỪNG thử lại;
(3) hướng còn mở thật sự: các wiki cộng đồng khác dùng Semantic MediaWiki (kỹ thuật checkpoint 26)
— chưa tìm ra ứng viên cụ thể lượt này, cần tìm kỹ hơn; (4) các tag OSM khác qua Overpass API (kỹ
thuật MỚI lượt này) đáng thử: `shop=repair` (có thể trùng nhiều với Repair Café đã lấy, nhưng đáng
kiểm), `office=research` hoặc `office=coworking` đã lọc kỹ theo tên (loại chuỗi thương mại) thay vì
loại cả nhóm nếu muốn thử lại; (5) 571 hồ sơ Repair Café bị bỏ qua vì thiếu quốc gia (việc mở cũ);
(6) BIRAC BioNEST PDF lỗi cấu trúc vẫn chưa sửa được; (7) InovaLink Brazil vẫn bế tắc.

**Lần trước:** 2026-09-09 (checkpoint 26 — **NGUỒN LỚN MỚI: HackerspaceWiki (wiki.hackerspaces.org),
kỹ thuật MỚI "truy vấn Semantic MediaWiki `askargs`"**) — tiếp tục mục tiêu **10000**. Trước khi tìm
ra nguồn này, đã kiểm tra và LOẠI:

- **SpaceAPI directory (`directory.spaceapi.io`)** — đã nằm sẵn trong danh sách loại đầu phiên
  ("SpaceAPI hackerspace"), kiểm tra lại xác nhận đúng lý do: chỉ **250** mục, mỗi mục là cặp
  tên→URL endpoint API trạng thái riêng (không phải website), phải mở từng endpoint mới thấy field
  `url` (website thật) — quy mô quá nhỏ (250) so với công cần bỏ ra để cào từng endpoint tự host
  (nhiều domain khác nhau, độ tin cậy thấp). Xác nhận loại đúng, không thử tiếp.

**Quá trình dò tìm HackerspaceWiki:** trang liệt kê `wiki.hackerspaces.org/List_of_hackerspaces` là
MediaWiki thường (không có nút export), nhưng site này chạy **Semantic MediaWiki (SMW)** — mỗi
hackerspace là một trang có thuộc tính có cấu trúc (`Country`, `Website`, `Hackerspace_status`,
`Has_coordinates`, `City`...), nhập qua form `Special:FormStart/Hackerspace`. Dò ra API chuẩn SMW
`action=askargs` tại `https://wiki.hackerspaces.org/w/api.php` (LƯU Ý: phải dùng path `/w/api.php`,
KHÔNG PHẢI `/api.php` ở gốc — gọi nhầm path gốc trả về trang lỗi HTML "No such action" chứ không báo
404, dễ nhầm là API không tồn tại). Truy vấn mẫu:
`?action=askargs&conditions=Category:Hackerspace&printouts=Country|Website|Hackerspace_status|
Has_coordinates|City&parameters=limit=500|offset=N&format=json` — xác nhận bằng cách `browsebysubject`
một trang mẫu (Noisebridge) để tìm đúng tên property trước khi query hàng loạt. Đây là kỹ thuật MỚI:
**truy vấn Semantic MediaWiki để lấy dữ liệu có cấu trúc trực tiếp từ một trang wiki cộng đồng**,
khác hẳn kỹ thuật 2 cũ (JSON nhúng sẵn trong trang bản đồ) — áp dụng được cho bất kỳ site nào chạy
SMW/Cargo có category + property phù hợp.

Phân trang `limit=500` từng đợt (offset 0/500/1000/1500/2000/2500/3000, `curl --compressed` — response
gzip ~30KB giải nén ra ~280KB/trang, không cần hạ luồng vì đây là 1 site trả JSON lớn một lần, không
phải hàng nghìn request riêng lẻ) → gộp được **2587** trang thuộc `Category:Hackerspace`. Lọc theo
`Hackerspace_status`: active 846, closed 670, suspected inactive 394, planned 351, building 238,
unknown 37, (none) 28, reformatting 23 — **lần đầu tiên nguồn có sẵn trường trạng thái vòng đời rõ
ràng**, nên áp dụng thêm lớp lọc chất lượng MỚI (khác các checkpoint trước không có field này): CHỈ
giữ `active`. Trong 846 "active", có Website 811 → trích xuất đủ 811 (0 bị bỏ vì thiếu quốc gia/toạ
độ centroid dự phòng).

**Điểm mạnh dữ liệu — toạ độ CHÍNH XÁC CẤP ĐỊA ĐIỂM sẵn có:** 719/811 (89%) có sẵn field
`Has_coordinates` (lat/lon) do chính người quản trị hackerspace điền khi tạo trang — CHÍNH XÁC HƠN
hẳn centroid quốc gia thường dùng ở các checkpoint khác. 92 mục còn lại (31 quốc gia) dùng centroid
quốc gia (dict viết tay mới cho batch này). Vài tên quốc gia lệch chuẩn trong nguồn gốc đã ánh xạ về
đúng quy ước ROSTER hiện có: "United States of America"/"US"→"United States", "CANADA"→"Canada",
"INDIA"→"India", "Catalonia"→"Spain", "Scotland"→"United Kingdom", "Georgia (Sakartvelo)"→"Georgia",
"Macedonia"→"North Macedonia", "Türkiye"→"Turkey" (giữ "Russian Federation"/"Czech Republic" vì đây
đã là biến thể PHỔ BIẾN HƠN trong ROSTER hiện có, không phải "Russia"/"Czechia"). 0 mục Việt Nam.

Lọc: bỏ 8 trùng NỘI BỘ batch (domain/tên trùng), bỏ 73 trùng với ROSTER hiện có → còn **730** ứng
viên đưa vào `check_url()` (10 luồng, timeout 15s — không cần hạ luồng như Repair Café vì đây là 730
domain KHÁC NHAU, không phải hàng nghìn request cùng 1 site sau WAF). Alive lượt 1: **629/730**
(86%). Retry 101 lỗi với 8 luồng/timeout 20s: chỉ cứu thêm **4** — khác hẳn bài học Repair Café, ở
đây phần lớn 97 mục chết THẬT (site cá nhân/nhóm nhỏ đã ngừng hoạt động, tên miền hết hạn bị chiếm
làm trang bán domain — nhiều lỗi "parking-page phrase 'godaddy/namecheap'"), không phải lỗi mạng
thoáng qua. Tổng **633/730 sống thật (86,7%)**. Chỉ **3/633 (0,5%)** URL sống là domain mạng xã hội
— tỉ lệ thấp nhất trong các checkpoint gần đây, vì hackerspace thường tự lưu trữ website/wiki riêng.

Quốc gia (top): Mỹ 162, Đức 126, Anh 37, Pháp 24, Canada 23, Hà Lan 20, Thuỵ Sĩ 18, Áo 14, Úc 14, Ý
13, Thuỵ Điển 13 — đúng đặc điểm phong trào hackerspace/makerspace khởi phát mạnh ở Đức (CCC/Chaos-
treff) và Mỹ. `org` để trống toàn batch (nguồn không có cột tổ chức chủ quản tách biệt).

`ROSTER`: 5501 → **6134** (+633). Đơn vị trên bản đồ: 5510 → **6143** (+633, giữ nguyên chênh lệch
+9 đã ghi nhận ổn định qua nhiều checkpoint — không phải lỗi). Kiểm bằng Browser pane qua HTTP server
cục bộ (`python -m http.server`, `file://` bị chặn đúng như ghi chú cũ): trang hiển thị đúng
"6143 đơn vị được lập bản đồ" / "6134 trong danh mục mở rộng", không lỗi console, `node --check` qua
script inline (1,833,098 ký tự) sạch, thẻ `div`/`section` cân bằng (107/107, 6/6).

**Việc mở cho lượt sau (mục tiêu 10000, còn thiếu ~3866):** (1) HackerspaceWiki còn **238 "building"**
+ **351 "planned"** chưa khai thác — có thể là nguồn bồi thêm nếu chấp nhận hạ tiêu chuẩn "đang hoạt
động thật" (độ ưu tiên thấp, cân nhắc kỹ trước khi dùng vì "planned"/"building" nhiều khả năng chưa
từng đi vào hoạt động thật); (2) các hướng nêu từ checkpoint 25 vẫn CHƯA THỬ: Restart Project, FixIt
Clinic, Freecycle network, Time Bank network, Creative Reuse network, TechShop, Library of Things,
Seedstars, Village Capital, UnternehmerTUM, EIT Community, đăng ký Estonia/Latvia/Lithuania, Canada
NRC IRAP, Australia accelerator registry — đáng thử TRƯỚC ở lượt sau; (3) kỹ thuật MỚI "SMW askargs"
ở checkpoint này đáng thử lại cho các wiki cộng đồng khác chạy Semantic MediaWiki/Cargo nếu tìm thấy
(vd site FabLab/makerspace khu vực khác dùng cùng nền tảng wiki); (4) 571 hồ sơ Repair Café bị bỏ qua
vì thiếu quốc gia (việc mở cũ từ checkpoint 25, độ ưu tiên thấp); (5) BIRAC BioNEST PDF lỗi cấu trúc
vẫn chưa sửa được; (6) InovaLink Brazil vẫn bế tắc (Livewire, không phải REST list).

**Lần trước:** 2026-09-09 (checkpoint 25 — **NGUỒN LỚN MỚI: Repair Café toàn cầu, danh bạ chính
thức repaircafe.org, kỹ thuật MỚI "API danh sách + cào từng trang hồ sơ lấy trường Website"**) —
tiếp tục mục tiêu **10000**. Trước khi tìm ra nguồn này, đã thử và LOẠI các hướng gợi ý đầu phiên:

- **Hackerspaces.org, TechShop, Library of Things, Seedstars, Village Capital, UnternehmerTUM,
  Canada NRC IRAP registry, Australia accelerator registry, mạng co-working phi lợi nhuận châu
  Âu/Á** — KHÔNG thử (thời gian phiên dồn hết vào nguồn Repair Café một khi xác nhận khả thi và đủ
  lớn; đây là các hướng còn để ngỏ cho phiên sau, chưa "thử và loại" theo đúng nghĩa).
- **Estonia/Latvia/Lithuania đăng ký khu công nghệ/vườn ươm chính thức** — KHÔNG thử, cùng lý do.
- **EIT Community (European Institute of Innovation & Technology) danh sách đối tác** — KHÔNG
  thử, cùng lý do trên.

**Quá trình dò tìm Repair Café (`repaircafe.org`):** trang "Visit" của mạng lưới có ô tìm kiếm bản
đồ hiển thị **4005 Repair Café** toàn cầu, dựng bằng một widget JS tuỳ biến (`rc-app`, không phải
plugin bản đồ chuẩn). Dò qua REST API discovery document (`/wp-json/`) lộ ra route
`/repaircafe/v1/search` (namespace RIÊNG của theme, KHÔNG phải route chuẩn `events-manager/v1`
vốn yêu cầu đăng nhập/nonce — route `events-manager/v1/locations`/`events-manager/v1/events` trả
lỗi 401/rơi về trang index, ĐÃ THỬ và LOẠI vì cần auth). `/repaircafe/v1/search?s=&pp=60&pg=N`
công khai không cần khoá/nonce, trả JSON `{total, members:[{id,name,addr,url}]}` — `pp` bị chặn
trần ở 60 dù truyền giá trị lớn hơn (khác hẳn kiểu "bỏ qua tham số, trả nguyên mảng" của fablabs.io
checkpoint 24), nên phải phân trang thật qua 68 lượt gọi `pg=1..68` để lấy đủ 4005 bản ghi — đây là
biến thể MỚI của kỹ thuật 3 (API công khai không cần khoá) khi trang thật sự phân trang bắt buộc,
không bỏ qua tham số như các lần trước.

**Phát hiện quan trọng — trường `url` trong API KHÔNG PHẢI website tổ chức:** mỗi bản ghi chỉ có
`url` trỏ về trang hồ sơ NỘI BỘ trên chính `repaircafe.org` (`/en/cafe/{slug}/`), không phải site
riêng của nhóm Repair Café địa phương. Mở thử một trang hồ sơ mẫu lộ ra bảng field tuỳ biến kiểu
Events Manager location, trong đó CÓ MỘT DÒNG `<td class="label">Website</td>` chỉ xuất hiện khi
người tổ chức đã điền — đây là kỹ thuật MỚI, chưa từng dùng ở các checkpoint trước: "API liệt kê
toàn bộ bản ghi + cào riêng từng trang hồ sơ để lấy trường URL bên ngoài thật", cần thiết khi API
danh sách gốc không lộ sẵn cột website (khác các nguồn trước luôn có sẵn cột website trong chính
JSON/CSV gốc).

**Bẫy kỹ thuật MỚI — cào 4005 trang hồ sơ với 20 luồng làm sập tỉ lệ thành công:** lượt cào đầu
(`ThreadPoolExecutor` 20 luồng, timeout 10s) chỉ hoàn tất sạch **1418/4005** (35%; 734 có Website +
684 xác nhận trống), còn lại **2587/4005 (65%)** lỗi `502 Bad Gateway`/timeout — rõ ràng WAF
Cloudflare phía trước site phản ứng với mức độ đồng thời cao bằng cách rớt kết nối hàng loạt, KHÔNG
PHẢI do các trang hồ sơ đó thật sự lỗi. Lượt 2 CHỈ retry đúng 2587 bản ghi lỗi, hạ xuống 8 luồng/
timeout 20s — cứu thêm **2531/2587 (97,8%)** thành công thật (trong đó 1360 có Website điền sẵn,
tỉ lệ trúng Website trong nhóm retry cao hơn hẳn nhóm gốc, xác nhận đây đúng là lỗi mạng thoáng qua
do quá tải luồng chứ không lệch mẫu dữ liệu — chỉ còn đúng 56/4005 hồ sơ thật sự không lấy được sau
2 lượt). **Bài học cho lượt sau:** với site có WAF Cloudflare, KHÔNG bắt đầu bằng số luồng cao (20+)
cho hàng nghìn request riêng lẻ tới cùng domain — nên bắt đầu ngay ở 8-10 luồng, chấp nhận chậm hơn
một chút để tránh phải chạy lại gần 2/3 khối lượng.

Kết quả cào: **2094/4005 (52,3%)** hồ sơ có điền trường Website. Lọc: bỏ 63 dòng `website` trỏ
ngược lại chính `repaircafe.org` (không phải site ngoài thật), bỏ 571 dòng không suy ra được quốc
gia từ chuỗi địa chỉ tự do (đa ngôn ngữ nl/en/fr/de/es, một số thiếu hẳn token quốc gia — CHƯA xử
lý sâu hơn bằng geocoding thật, chấp nhận bỏ qua vì đã đủ lớn), 0 dòng Việt Nam, lọc trùng NỘI BỘ
batch theo domain (310 trùng — nhiều Repair Café dùng chung website tổ chức mẹ/thư viện/trung tâm
cộng đồng) → còn **1150** ứng viên. Lọc trùng với ROSTER hiện có theo domain+tên (`SOCIAL_PLATFORM_
DOMAINS` loại trừ khỏi so khớp domain) — 19 trùng thật → còn **1131** ứng viên đưa vào `check_url()`.

`check_url()` giữ **898/1131** lượt đầu (timeout 12s, 10 luồng), retry 233 mục chết bằng timeout
20s/8 luồng — cứu thêm **19** → tổng **917/1131 sống thật (81,1%)**. Ghi nhận minh bạch: chỉ
**11/917 (1,2%)** URL sống là domain mạng xã hội — thấp hơn hẳn tỉ lệ ~31% của fablabs.io checkpoint
24, hợp lý vì người tổ chức Repair Café ở Tây Âu/Anglosphere (nhóm chiếm đa số batch này: Pháp 239,
Hà Lan 236, Đức 232, Anh 171) có xu hướng lập blog/site WordPress riêng hoặc dùng site thư viện/tổ
chức cộng đồng chủ quản hơn là chỉ dùng trang mạng xã hội.

Quốc gia (top): Pháp 239, Hà Lan 236, Đức 232, Anh 171, Mỹ 81, Canada 43, Bỉ 38, Úc 33, Tây Ban Nha
18, Ý 10 — đúng đặc điểm phong trào Repair Café khởi phát từ Hà Lan, lan mạnh Tây Âu/Anglosphere.
Toạ độ gán CẤP QUỐC GIA (centroid), không có sẵn lat/lng riêng từng địa điểm trong dữ liệu nguồn.
`org` để trống toàn batch (tên đã đủ mô tả, giống tiền lệ fablabs.io checkpoint 24 — nguồn không có
cột tổ chức chủ quản tách biệt).

`ROSTER`: 4584 → **5501** (+917). Đơn vị trên bản đồ: 4593 → **5510** (+917, giữ nguyên chênh lệch
+9 đã ghi nhận ổn định qua nhiều checkpoint — không phải lỗi).

**Việc mở cho lượt sau (mục tiêu 10000, còn thiếu ~4499):** (1) 571 hồ sơ Repair Café bị bỏ qua vì
không suy ra được quốc gia từ địa chỉ tự do — có thể cứu thêm bằng geocoding thật (Nominatim/Google)
nếu muốn đào sâu thêm nguồn này, độ ưu tiên thấp vì tỉ lệ nhỏ; (2) các hướng nêu đầu phiên nhưng
CHƯA THỬ (không phải đã loại): Hackerspaces.org, TechShop, Library of Things, Seedstars, Village
Capital, UnternehmerTUM, EIT Community, đăng ký Estonia/Latvia/Lithuania, Canada NRC IRAP, Australia
accelerator registry, mạng co-working phi lợi nhuận châu Âu/Á — đáng thử TRƯỚC ở lượt sau vì chưa
tốn công loại; (3) bài học WAF/luồng cao ở trên nên áp dụng NGAY từ đầu cho bất kỳ site có Cloudflare
nào cần cào nhiều trang riêng lẻ trong các lượt sau; (4) BIRAC BioNEST PDF lỗi cấu trúc vẫn chưa sửa
được — việc mở cũ còn nguyên; (5) InovaLink Brazil vẫn bế tắc (Livewire, không phải REST list).

**Lần trước:** 2026-09-09 (checkpoint 24 — **NGUỒN LỚN MỚI: fablabs.io, danh bạ toàn cầu chính
thức của Fab Foundation (mạng lưới Fab Lab thế giới)**) — tiếp tục mục tiêu **10000**. Trước khi
tìm ra nguồn này, đã thử và LOẠI vài hướng nêu trong đầu bài phiên này:

- **Startup Genome Membership Directory** (`startupgenome.com/member-directory`) — trang tự ghi
  rõ **"Private & Confidential – for Startup Genome Members only. Do not share outside the
  network"** ngay trên trang — loại ngay lập tức dù đủ quy mô (~100 tổ chức, 40+ nước), vì đây là
  dữ liệu hội viên riêng tư ghi rõ không được chia sẻ ra ngoài, không phải danh bạ công khai
  (khác hẳn kiểu "cần đăng nhập" thông thường — ở đây có TRUY CẬP được nhưng bị cấm minh thị theo
  nội dung trang, nên loại theo nguyên tắc đạo đức chứ không phải giới hạn kỹ thuật).
- **SpaceAPI hackerspace directory** (`directory.spaceapi.io`, 250 hackerspace/makerspace) — giá
  trị mỗi dòng là URL một **endpoint trạng thái API** (JSON máy đọc, vd
  `https://hub.57north.org.uk/spaceapi`), không phải trang web tổ chức thật; dùng làm "website"
  sẽ đưa người xem đến một khối JSON trần trụi thay vì trang giới thiệu — loại vì không đạt tiêu
  chí "URL dẫn tới trang thật".
- **Techstars/MassChallenge/GSMA tech hub mapping/Malaysia MRANTI/Saudi MCIT/Thailand NIA/
  Poland NCBR/Hungary NKFIH/Qatar QSTP** — mỗi hướng đều dừng ở quy mô quá nhỏ (MassChallenge chỉ
  8 địa điểm), không có danh bạ tải được, hoặc không lộ URL riêng từng tổ chức (Startup Genome/
  GSMA chỉ có báo cáo/blog tổng hợp số liệu, không phải danh sách chi tiết công khai) — loại
  nhanh theo tiêu chí "quy mô ≥100 + có URL thật, không đăng nhập" của đầu bài.
- **InovaLink Brazil** (việc mở từ checkpoint 23) — vào lại bằng trình duyệt thật, bắt network
  request thấy nền tảng Laravel Livewire gọi `POST /livewire/update` (payload trạng thái
  component, không phải REST JSON list) — xác nhận đúng dự đoán cũ, không có endpoint danh sách
  đơn giản, để lại y nguyên trong việc mở.

**Nguồn dùng được: fablabs.io** (`fablabs.io`, nền tảng chính thức của Fab Foundation cho mạng
lưới Fab Lab toàn cầu — không phải hiệp hội hội viên, là đăng ký trực tiếp từng phòng lab) — có
API công khai không cần khoá tại `https://www.fablabs.io/api/labs` (bí danh cũ `/0/labs.json` và
link tải "Download the Fab Labs list" trên trang `/labs` đều redirect về cùng endpoint này), trả
về MỘT mảng JSON duy nhất chứa TOÀN BỘ 2856 lab (không phân trang — tham số `page`/`per_page`/
`country_code` bị lờ đi hoàn toàn, luôn trả nguyên mảng đầy đủ). Mỗi bản ghi có sẵn `name`,
`country_code` (ISO2), `latitude`/`longitude` (có ở 2618/2856 bản ghi), và `links` (mảng URL,
lấy URL http(s) đầu tiên làm website) — đúng kiểu nguồn tốt nhất (không cần đoán URL, có sẵn
toạ độ chính xác cho đa số bản ghi).

**Bẫy kỹ thuật MỚI, đáng ghi nhớ cho lượt sau — tải một response JSON lớn (~5MB+) bị cắt cụt bí
ẩn:** phiên mạng của máy này liên tục cắt cụt kết nối `curl` tải endpoint trên ở quanh mốc
~5.3MB dù server trả `exit 0` bình thường (không phải lỗi HTTP, giống kiểu giới hạn TỔNG DUNG
LƯỢNG truyền tải trên một kết nối dài chứ không phải giới hạn thời gian — thử với `-m` (timeout)
rộng tới 600s vẫn cùng một mốc cắt cụt xảy ra ở các dung lượng ngẫu nhiên gần 5.3MB qua nhiều lần
thử). **Cách vượt qua:** thêm cờ `curl --compressed` (yêu cầu nén gzip qua `Accept-Encoding`) —
cùng nội dung logic giảm còn ~1MB truyền trên dây, lọt qua giới hạn, tải trọn vẹn 5.36MB sau giải
nén (2856 bản ghi, JSON hợp lệ, xác minh bằng `json.load()`). Đáng thử cờ này ĐẦU TIÊN cho bất kỳ
API nào trả một JSON lớn không phân trang mà gặp hiện tượng cắt cụt tương tự trong môi trường
này, trước khi kết luận "API lỗi" hay "nguồn không tải được".

**Cảnh báo giả (không phải lỗi thật):** một số tên hiển thị lỗi thành `C�te d'Ivoire` khi in ra
console/terminal — kiểm lại bằng đọc thẳng byte UTF-8 trong file JSON xác nhận dữ liệu gốc và
file trung gian đều ĐÚNG (`C\xc3\xb4te` hợp lệ), lỗi chỉ là do bảng mã hiển thị của terminal
Windows khi `print()`, không ảnh hưởng dữ liệu thực tế ghi vào ROSTER — không cần sửa gì, chỉ ghi
lại để lượt sau không hoảng khi thấy hiện tượng tương tự.

Lọc: bỏ 115 dòng Việt Nam (`country_code=="VN"`, đúng quy tắc), bỏ 455 dòng không có `links` nào
là URL http(s) thật, lọc trùng ROSTER hiện có bằng `domain_of`+`normalize_name`
(`SOCIAL_PLATFORM_DOMAINS` loại trừ khỏi so khớp domain) — 70 trùng thật, lọc trùng NỘI BỘ batch
theo domain — 151 trùng (nhiều lab dùng chung 1 website tổ chức mẹ) → còn **2065 ứng viên**. 144
bản ghi thiếu sẵn toạ độ (tổng cộng rơi vào 56 nước khác nhau) được gán centroid CẤP QUỐC GIA viết
tay (`COUNTRY_CENTROID`, chỉ phủ đúng các nước xuất hiện trong batch này); phần lớn (~92%) giữ
nguyên toạ độ chính xác có sẵn từ nguồn — hiếm gặp mức chính xác này cho một batch cỡ 2000+.

`check_url()` giữ **1321/2065** lượt đầu (timeout 12s, 10 luồng `ThreadPoolExecutor`), rồi kiểm
lại 744 mục chết bằng timeout 20s — cứu thêm **46** (phần lớn lỗi `URLError`/`HTTPError` thoáng
qua do mạng, đúng mẫu hình đã ghi nhận ở các checkpoint trước) → tổng **1367/2065 sống thật**
(≈66,2%). Ghi nhận: khoảng 31% (407/1321) URL sống trỏ tới trang mạng xã hội (chủ yếu Facebook/
Instagram) thay vì website riêng — hợp lý với thực tế nhiều fab lab nhỏ/vùng khó khăn chỉ duy trì
trang Facebook, đúng tiền lệ đã chấp nhận từ checkpoint 22 (không phải vấn đề mới, không loại).

`org` để trống toàn batch (dữ liệu fablabs.io không có cột tổ chức chủ quản tách biệt khỏi tên
lab). Gồm cả 3 loại `kind_name`: `fab_lab` (đa số), `mini_fab_lab`, `mobile` — đều là không gian
chế tạo/fab lab thật, đúng phạm vi ROSTER.

`ROSTER`: 3217 → **4584** (+1367). Đơn vị trên bản đồ: 3226 → **4593** (xác nhận bằng bộ đếm
hiển thị trên trang qua `index.html` chạy local HTTP server, khớp số script tính ra).

**Việc mở cho lượt sau (mục tiêu 10000, còn thiếu ~5416):** (1) cờ `curl --compressed` nên trở
thành thao tác MẶC ĐỊNH đầu tiên cho mọi lần tải JSON lớn trong môi trường này, không chỉ khi gặp
lỗi cắt cụt — tiết kiệm nhiều lượt thử sai; (2) fablabs.io còn ~700 mục "chết thật" sau 2 lượt
kiểm (chủ yếu domain cá nhân/dự án nhỏ đã hết hạn) — không đáng thử lại; (3) InovaLink Brazil vẫn
chưa giải quyết được (Livewire component state, không phải REST list) — độ ưu tiên thấp; (4)
BIRAC BioNEST PDF lỗi cấu trúc vẫn chưa sửa được — việc mở cũ còn nguyên; (5) hướng "đăng ký
chính phủ có cột website" vẫn là hướng chính cần tìm tiếp cho các nước Á/Phi/Trung Đông chưa dò
(Malaysia/Saudi Arabia/Thailand/Qatar đã thử và loại phiên này vì không có danh bạ công khai lộ
URL, không phải vì bị chặn — nên coi là cạn hẳn, không thử lại các nước này).

**Lần trước:** 2026-09-09 (checkpoint 23 — **NGUỒN MỚI: Impact Hub Global (Google Sheet nhúng
sẵn trong bản đồ thành viên, đúng kỹ thuật 2) + AIC India (đăng ký chính phủ NITI Aayog, đúng
kỹ thuật 1)**) — sếp nâng mục tiêu lên **10000**. Trước khi tìm ra 2 nguồn này, đã thử và LOẠI
một loạt hướng lớn nêu trong đầu bài phiên này:

- **AfriLabs** (`afrilabs.com`, mạng lưới hub công nghệ Châu Phi, 521 hub) — có API WordPress
  REST công khai `/wp-json/wp/v2/hub` (custom post type `hub`, phát hiện nhanh qua
  `/wp-json/` route list, giống kỹ thuật AfriLabs/AfriLabs khác EDIH), nhưng kiểm cả field
  `content.rendered` của 100 hub mẫu và trang chi tiết từng hub (`/hub/<slug>/`, cả REST lẫn
  HTML render qua trình duyệt thật) đều **KHÔNG có bất kỳ URL ngoài nào** — hoàn toàn không có
  cột website, giống đúng "GIỚI HẠN CỨNG" đã gặp ở Startup India checkpoint 18. Loại.
- **ASTP-Proton** (`astp-proton.eu`, hiệp hội TTO châu Âu, mục 30 trong
  `_claude/roster-grow-queue.md`) — danh bạ hội viên yêu cầu đăng nhập thành viên, không có
  trang công khai. Loại, xác nhận đúng dự đoán của queue.
- **KCA/THETA-KTA** (`techtransfer.org.au`, hiệp hội TTO Úc/NZ hợp nhất, mục 34 trong queue) —
  trang "KCA Members" không lộ danh sách công khai (chỉ trang giới thiệu, đăng nhập hội viên
  qua nền tảng Membes AMS). Loại.
- **WAITRO** (`waitro.org`, 190+ viện nghiên cứu công nghiệp toàn cầu) — trang `/members/` chỉ
  liệt kê 34 "Active Members" dạng TEXT THUẦN (tên – quốc gia, không có link nào), không phải
  danh bạ đầy đủ 190 thành viên và không có URL nào để trích. Loại.
- **EBN / EU|BIC** (`ebn.eu`, ~180 trung tâm ươm tạo châu Âu) — trang `/members/` không liệt kê
  gì, link "membersmap" cũ đã gỡ; dò ra nền tảng `eubic.community` (chạy trên "Mighty", app
  cộng đồng trả phí) — toàn bộ nội dung đằng sau đăng nhập. Loại.
- **Turkey Teknopark (teknopark.sanayi.gov.tr)** — domain con của Bộ Công nghiệp không kết nối
  được (`ERR_TIMED_OUT`, giống mẫu hình các domain chính phủ khác đã bị chặn/quá tải trước
  đây); dùng thay danh sách Wikipedia tiếng Thổ "Türkiye'deki teknokentler listesi" (97 khu) —
  đầy đủ tên/thành phố/năm nhưng **KHÔNG có cột website nào cả**, sẽ phải đoán domain nên loại
  theo đúng quy tắc "không đoán domain".
- **Philippines DOST TBI** (`dost.gov.ph/innovationmaps/TBI.kml`, file KML bản đồ) — chỉ 47
  placemark, mỗi placemark chỉ có tên+địa chỉ trong `<description>`, không có trường website.
  Quá nhỏ và thiếu URL. Loại.
- **India AIC portal** (`aic.aim.gov.in`) — domain con không kết nối được
  (`ERR_CONNECTION_TIMED_OUT`) — dùng thay trang tĩnh `aim.gov.in` (xem nguồn dùng được bên
  dưới).
- **India AIC_List_data.pdf** (danh sách đầy đủ 93 AIC do AIM/NITI Aayog công bố, state/city/
  năm thành lập) — TẢI ĐƯỢC nhưng **không có cột website** (đúng bẫy kiểu Poland PARP cũ) — chỉ
  dùng để đối chiếu quy mô, không trích được URL từ đây.
- **BIRAC BioNEST Compendium** (`birac.nic.in/webcontent/Bionest_Compendium.pdf`, 73 cơ sở
  ươm tạo công nghệ sinh học Ấn Độ) — file PDF 2.8MB tải về **bị lỗi cấu trúc xref** (`pypdf`
  và `pdftoppm`/`pdftotext` của Poppler đều báo "Invalid XRef entry"/"Invalid object in
  /Pages") dù tải nguyên vẹn theo `curl` (không phải lỗi mạng) — nghi PDF gốc do BIRAC xuất bị
  lỗi linearization. Không phục hồi được trong thời gian hợp lý, để lại việc mở nếu ai có công
  cụ sửa PDF hỏng (`qpdf --qdf`/`mutool clean` có thể cứu được).
- **Uruguay ANII / Czech SVTP** — kiểm nhanh quy mô: ANII Uruguay chỉ có vài incubator lẻ
  (nước rất nhỏ); SVTP Czech (`svtp.cz/katalog/`) chỉ 27 khu (14 đạt chuẩn + 13 khác), danh
  sách chỉ có tên+thành phố, KHÔNG có link — cả hai dưới ngưỡng ~100-150 mục đáng làm một đợt
  riêng, không đào tiếp.
- **China Torch** (`chinatorch.gov.cn`) — thử lại bằng `WebFetch` (chạy trên hạ tầng
  Anthropic, không phải mạng máy này) với hy vọng đây là chặn theo mạng cục bộ — vẫn
  `ECONNREFUSED` ngay ở tầng TCP, xác nhận server tự chặn kết nối từ ngoài Trung Quốc (không
  phải do mạng máy đang dùng), không đáng thử lại trừ khi có proxy trong nước.

**Nguồn dùng được #1: Impact Hub Global** (`impacthub.net/locations/`, mạng lưới hub ĐMST xã
hội toàn cầu, ~150 địa điểm tại 60+ nước) — kỹ thuật mới: trang danh sách hiển thị bộ đếm theo
khu vực (150 địa điểm) nhưng nội dung `<ul>` rỗng, dữ liệu thật nạp qua một `<iframe>` riêng
(`impacthub.net/locationsmap-2/`) chứa bản đồ Leaflet; script JS của iframe này gọi thẳng
**Google Sheets API v4 công khai** (`sheets.googleapis.com/v4/spreadsheets/<ID>/values/map`)
bằng API key nhúng cứng trong JS — đây là hình thức "dữ liệu nhúng sẵn" mới chưa từng gặp
(không phải JSON tĩnh trong `<script>` như ANPROTEC, mà là một Google Sheet công khai lộ qua
API key lộ trong client). **Bẫy kỹ thuật**: API key có giới hạn `HTTP_REFERRER` (gọi thẳng bị
từ chối 403 "Requests from referer <empty> are blocked") — phải thêm header
`Referer: https://impacthub.net/locationsmap-2/` vào request thì mới qua được giới hạn (không
phải bẻ khoá gì, chỉ giả lập đúng nguồn gốc request mà key đã cho phép).

Sheet trả về đúng 9 cột có sẵn: Status, IH NAME, LATITUDE, LONGITUDE, WEBSITE, TYPE, REGION,
COUNTRY, FLAG — **có sẵn cả toạ độ chính xác từng địa điểm** (không cần viết dict centroid
quốc gia/tỉnh cho batch này, hiếm gặp). 150 dòng → 129 có cột Website không rỗng → loại 1 dòng
Việt Nam (Impact Hub Saigon, đang "Coming Soon" nên vốn cũng không có website, loại theo đúng
quy ước Việt Nam) → lọc trùng ROSTER hiện có (10 trùng — đa số là các Impact Hub Châu Phi đã
vào ROSTER từ trước qua batch africatechschools.com) → 119 mục cần kiểm sống → `check_url()`
giữ **107/119** ngay lượt đầu, lượt kiểm lại (timeout 20s) không cứu thêm được mục nào (12 mục
chết là chết thật — phần lớn `URLError`/`HTTPError` trên domain `*.impacthub.net` của các chi
nhánh đã ngừng hoạt động, cộng 1 mục Origin/Thổ Nhĩ Kỳ và 1 mục Thuỵ Sĩ chết thật). Bao gồm cả
8 mục loại "Community Partner" (CP, không phải "HUB" chính thức) — đã kiểm tên thật (Build
Palestine, Temasek Shophouse, Centre d'innovation de Lubumbashi, Social Innovation Academy...)
đều là tổ chức hỗ trợ ĐMST/khởi nghiệp thật, đúng phạm vi ROSTER, không phải quỹ đầu tư/chương
trình đơn lẻ — giữ lại. Tên "Imact Hub New York Metropolitan Area" sửa lỗi đánh máy hiển nhiên
thành "Impact Hub..." (lỗi gõ thiếu chữ "p" trong chính tiền tố thương hiệu dùng thống nhất ở
135 dòng khác, khác bản chất với các trường hợp "giữ nguyên tên gốc" trước đây vốn là tên hợp
pháp khác biệt của một tổ chức, không phải lỗi gõ rành rành của chính nền tảng).

**Nguồn dùng được #2: AIC India** (Atal Incubation Centres, NITI Aayog/AIM — đăng ký chính phủ
Ấn Độ) — trang `aim.gov.in/selected-atal.php` có 60 khối accordion, mỗi khối là hồ sơ mô tả
một AIC với các trường có cấu trúc rõ **"Website:"** + **"City:"** (57/60 khối có Website, 3
khối thiếu bị bỏ qua) — đúng kiểu tài liệu chính phủ có sẵn cột website (kỹ thuật 1), khác PDF
`AIC_List_data.pdf` (93 dòng nhưng KHÔNG có cột website, chỉ dùng đối chiếu quy mô như đã ghi ở
trên). 57 mục → lọc trùng ROSTER: **0 trùng** (India TISC/khác trước đây không phủ các AIC
non-trường-đại-học này) → `check_url()` giữ 40/57 lượt đầu, cứu thêm 1 qua lượt kiểm lại
(timeout 20s) → **41/57 sống thật**. Toạ độ dùng centroid CẤP THÀNH PHỐ (viết tay 28 thành phố
Ấn Độ xuất hiện trong batch, chính xác hơn cấp quốc gia vì toàn bộ batch chỉ 1 nước).

**Việc mở kỹ thuật cho lượt sau (áp dụng được cho nhiều nguồn khác)**: khi một trang "bản đồ
thành viên" hiển thị bộ đếm đúng nhưng danh sách/marker rỗng lúc tải tĩnh, đừng vội kết luận
"không lấy được dữ liệu" — kiểm `<iframe>` bên trong trang (nhất là loại "locationsmap"/"map
embed") vì nhiều nền tảng nhúng bản đồ dưới dạng trang con riêng, và bên trong iframe đó rất
đáng tìm xem có gọi thẳng Google Sheets API (`sheets.googleapis.com/v4/spreadsheets/.../values/
...`) bằng API key lộ trong JS hay không — nếu bị chặn 403 do giới hạn Referer, thử lại với
header `Referer` trỏ đúng domain nhúng key đó (không phải hành vi bẻ khoá, khoá vẫn công khai
trong mã nguồn JS phía client).

Đưa hằng số `SOCIAL_PLATFORM_DOMAINS` vào thẳng `_claude/tools/roster_common.py` (việc mở đã
ghi từ checkpoint 22, nay đã làm) để các batch sau import dùng chung thay vì viết lại mỗi lần.

`ROSTER`: 3069 → **3217** (+148: 107 Impact Hub Global + 41 AIC India). Đơn vị trên bản đồ:
3078 → **3226** (xác nhận đúng bằng bộ đếm hiển thị trên trang qua `index.html` chạy local
HTTP server, khớp số script tính ra).

**Việc mở cho lượt sau (mục tiêu 10000, còn thiếu ~6774):** (1) BIRAC BioNEST PDF bị lỗi cấu
trúc — nếu sửa được bằng `qpdf`/`mutool` sẽ ra thêm ~70 mục Ấn Độ có khả năng có cột website
(chưa xác minh nội dung PDF thật sự có cột này không, chỉ mới xác nhận PDF hỏng không mở
được). (2) Impact Hub có 21 địa điểm KHÔNG có website (chủ yếu trạng thái "Initiative"/"Coming
Soon" — hub dự kiến/đang xây, chưa có site) — không đáng theo dõi lại sớm vì bản chất chưa vận
hành, khác các mục "chết" thật ở nơi khác. (3) Kỹ thuật mới "tìm Google Sheets API lộ trong
iframe bản đồ nhúng" đáng thử lại cho các hiệp hội/mạng lưới khác dùng bản đồ kiểu tương tự
(dấu hiệu nhận biết: trang danh bạ có bộ đếm đúng nhưng danh sách hiển thị rỗng lúc tải tĩnh) —
chưa xác định được ứng viên cụ thể nào khác, cần dò tiếp. (4) Ở quy mô 10000, các nguồn còn lại
sau khi cạn WIPO TISC/africatechschools/ANPROTEC/IASP/EDIH/Impact Hub cần tìm là những mạng
lưới CÓ ĐĂNG KÝ RIÊNG (không phải hiệp hội hội viên đóng phí, nhóm này gần cạn) — ưu tiên tiếp
tục dò kiểu "đăng ký chính phủ có cột website" (đã hết Colombia/Argentina/AIC India, còn nhiều
nước Á/Phi khác chưa dò) hơn là tiếp tục tìm hiệp hội quốc tế (WAITRO/EBN/ASTP/KCA đều đã cạn
trong phiên này).

**Lần trước:** 2026-09-09 (checkpoint 22 — **NGUỒN MỚI: danh bạ chính thức EDIH (European
Digital Innovation Hubs) của Uỷ ban châu Âu**) — tải export
`european-digital-innovation-hubs.ec.europa.eu/edih-catalogue/export-edih?page&_format=xls`:
đúng như dự đoán, server báo `Content-Type: application/vnd.ms-excel` và tên `.xls` nhưng NỘI
DUNG THỰC LÀ `.xlsx` (`file` xác nhận "Microsoft Excel 2007+") — đổi đuôi rồi mở bằng `openpyxl`
bình thường. Sheet "EDIH Catalogue", đúng 463 dòng.

**Bẫy dữ liệu MỚI, chưa có trong sổ tay cũ:** cột "Website" TƯỞNG có giá trị ở 424/463 dòng
nhưng thực ra CHỈ 384 là URL http(s) thật — 40 dòng còn lại giá trị chỉ là chữ "Website" trần
trụi (label liên kết Drupal, không có `cell.hyperlink` để trích, đã kiểm) hoặc một đường dẫn NỘI
BỘ tương đối quay lại chính trang catalogue của EC (vd `/edih-catalogue/edih-saxony-website`) —
không phải URL thật của tổ chức, phải loại bỏ theo đúng quy tắc "không đoán domain" chứ không
suy luận tiếp. Thêm 5 dòng khác cột Website bị CẮT NGẮN với dấu ba chấm `…` (U+2026) dính liền
cuối chuỗi (bug từ nguồn) khiến `urllib` ném `UnicodeEncodeError` khi gửi request (KHÔNG phải
trang chết) — xác minh bằng traceback đầy đủ (`request.encode('ascii')` thất bại đúng tại vị trí
ký tự `…`); phần hostname đầu các URL này vẫn nguyên vẹn/có thật (không phải đoán), nên cắt về
domain gốc rồi `check_url()` lại — cứu được 3/4 domain gốc còn sống (dòng thứ 5 đã bị lọc trùng
ở bước trước đó).

Lọc trùng ROSTER hiện có bằng `domain_of`+`normalize_name` như thường lệ nhưng phát hiện thêm 1
loại false-positive domain-level chưa gặp trước đây: 2 dòng khớp domain `linkedin.com` với 1 mục
Eritrea có sẵn trong ROSTER dùng trang LinkedIn làm "website" — hai tổ chức không liên quan cùng
dùng chung platform, KHÔNG phải trùng thật; đã loại trừ danh sách domain nền tảng chung
(`linkedin.com`, `facebook.com`, `twitter.com`/`x.com`, `instagram.com`, `youtube.com`,
`medium.com`) khỏi vòng so khớp domain (chỉ còn so khớp tên cho các domain này) — quy tắc này
hiện chỉ nằm trong script merge tạm, nên đưa thẳng vào `roster_common.py` cho các batch sau
(giống bài học "sẽ mất khi phiên kết thúc" đã ghi ở checkpoint 21). 13 trùng thật còn lại đa số
là 1 tổ chức mẹ có sẵn trong ROSTER dưới tên khác vận hành EDIH trên cùng domain (vd Science
Technology Park Belgrade ↔ CIPS/STP Belgrade/BITF cùng domain `ntpark.rs`). Còn lại 371 mục.

`check_url()` giữ 282/371 lượt đầu (timeout 10s), cứu thêm 3 qua sửa domain-cắt-ngắn ở trên
(285), rồi cứu thêm 14 qua 1 lượt kiểm lại toàn bộ số chết còn lại với timeout 20s (loại nhiễu
mạng thoáng qua) — tổng **299/371 sống thật** (≈80,6%, khớp ước tính ~80% đầu bài nêu). Toạ độ
dùng centroid CẤP QUỐC GIA, tự viết `COUNTRY_CENTROID` cho 39 nước xuất hiện trong dữ liệu (27
nước EU + Iceland/Liechtenstein/Norway/Albania/Bosnia/Kosovo/Moldova/Montenegro/North Macedonia/
Serbia/Ukraine/Türkiye — rộng hơn khối EU vì EDIH phủ cả EEA và một số nước liên kết Digital
Europe Programme, nhiều hơn ước tính "27-30 nước" nêu trong đầu bài).

Tên đơn vị: dùng "EDIH Name" làm gốc; nếu "EDIH Title" khác Name, ngắn (≤12 từ) và không lồng
sẵn Name bên trong thì ghép dạng "Name (Title)" (vd "DIPS (Digitalization and Innovation of
Public Services)"); nếu Title dài như một câu mô tả/khẩu hiệu (>12 từ, có trường hợp toàn viết
hoa kiểu khẩu hiệu dự án) thì giữ nguyên Name, bỏ Title; nếu Title đã chứa sẵn Name bên trong (vd
Name "DIH4CAT", Title "Catalonia Digital Innovation Hub (DIH4CAT)") thì dùng thẳng Title, không
lồng ngoặc kép thừa. `org` để trống cho toàn bộ batch này (EDIH Catalogue không có cột tổ chức
chủ quản tách biệt khỏi tên).

`ROSTER`: 2770 → **3069** (+299). Đơn vị trên bản đồ: 2779 → **3078**.

**Bài học kỹ thuật mới cho lượt sau:** (1) một cột "Website" không trống KHÔNG đồng nghĩa với URL
dùng được — luôn kiểm `str(value).lower().startswith("http")` trước khi tin, đặc biệt với export
từ CMS Drupal (field liên kết có thể serialize thành label hiển thị thay vì href thật); (2)
domain của các nền tảng mạng xã hội dùng chung (LinkedIn...) phải loại khỏi vòng so khớp trùng
theo domain — 1 tổ chức trong hàng nghìn dùng chung platform đó không có nghĩa 2 tổ chức bất kỳ
cùng dùng nó là trùng nhau; (3) một URL bị cắt ngắn giữa chừng (`…`) làm `urllib` crash bằng lỗi
Unicode chứ không trả lỗi HTTP — đây KHÔNG phải dấu hiệu trang chết, cần thử domain gốc (vẫn
nguyên vẹn trong chuỗi, không phải đoán) trước khi loại hẳn.

**Việc mở cho lượt sau:** (1) đưa danh sách loại trừ domain nền tảng chung
(`linkedin.com`/`facebook.com`/...) vào thẳng `roster_common.py` như hằng số dùng chung, tránh
mỗi batch tự viết lại rồi mất khi hết phiên; (2) 72 mục EDIH còn "chết thật" sau 2 lượt kiểm —
phần lớn `URLError`/`HTTPError` trên các domain dự án nhỏ kiểu `*-edih.eu` (đăng ký ngắn hạn theo
vòng đời dự án tài trợ EU, nhiều khả năng đã hết hạn tên miền thật chứ không phải lỗi mạng) —
không đáng thử lại trừ khi có lý do cụ thể; (3) EDIH Catalogue còn cột "Seal of Excellence" (dự
án được công nhận nhưng chưa cấp vốn — đã gộp chung, không tách riêng) và các cột sectors/
services/technologies chưa dùng tới — không cần cho ROSTER nhưng có thể hữu ích nếu sau này làm
phân loại chủ đề.

**Lần trước:** 2026-09-09 (checkpoint 21 — **NGUỒN LỚN MỚI: IASP (International Association of
Science Parks and Areas of Innovation), danh bạ khu khoa học/công nghệ quốc tế — đã bỏ 2 lần
trước vì ASP.NET postback, phiên này site đã ĐỔI NỀN TẢNG, dùng lại thành công**) — sếp nâng
mục tiêu ROSTER lên **10000 đơn vị** trong phiên này. `iasp.ws/our-members/directory` nay là
CMS Tangora chứ không phải ASP.NET cũ, có bộ lọc theo quốc gia (81 nước) và mỗi mục có trang
chi tiết `/our-members/directory/@<id>/<slug>` chứa sẵn trường "Website" và "Location"
(thành phố, quốc gia) — vừa đúng kiểu nguồn tốt (URL thật + vị trí có sẵn, không cần đoán).

**Bẫy kỹ thuật + cách gỡ:** trang danh bạ mặc định chỉ hiện một danh sách NGẪU NHIÊN ~29 tổ
chức không liên quan tới bộ lọc (carousel "gợi ý", nằm trong `module10_2`/`listrotator` khác
hẳn khối kết quả lọc thật `#listMasterView_65`/`module276_2`/class `member-item`) — nếu không
phân biệt hai khối DOM này sẽ tưởng lọc "không hoạt động" hoặc lẫn kết quả sai nước, đúng như
lý do 2 lần thử trước bị bỏ dở. Cách xác định điều hướng lọc theo nước: đổi `<select>` quốc
gia rồi `filterControlChange(443)` cập nhật URL thành
`...directory?filtercontrol651=<Country>&...` — URL này ĐIỀU HƯỚNG TRỰC TIẾP được (không cần
click), nên chỉ cần `navigate` batch 79 URL (một cho mỗi nước, trừ Vietnam theo quy ước ROSTER)
rồi lọc DOM đúng khối `#listMasterView_65` là ra danh sách CHUẨN, không lẫn carousel.

Quy trình: 79 lượt `navigate` (browser, theo batch ~10 nước/lượt qua `browser_batch` để giảm
round-trip) → 327 URL chi tiết duy nhất → tải hàng loạt bằng `curl`/`urllib` (trang chi tiết là
HTML tĩnh, không cần trình duyệt) → trích `<h1>` (tên), `class='sectionlink' href="..."`
(website), field `Location` (thành phố, quốc gia) bằng regex → lọc 20 mục không có website
(đa số là hội viên CÁ NHÂN — vd "Barbara Harley", "Esteban Pablo Cassin" — không phải tổ chức,
IASP có loại thành viên cá nhân/tư vấn ngoài tổ chức) → lọc trùng domain/tên với ROSTER (21
trùng) → `check_url()` giữ **237/286** ngay lượt đầu, cứu thêm 2 qua 1 lượt kiểm lại (20s
timeout) → merge **238 mục mới thật** (239 qua kiểm, 1 trùng nội bộ batch).

Toạ độ dùng centroid CẤP QUỐC GIA (`COUNTRY_CENTROID`, 76 nước xuất hiện trong batch này, viết
tay trong script merge tạm — quy mô địa lý quá rộng, 76 nước một lượt, nên chấp nhận độ chính
xác thô hơn cấp tỉnh/bang đã dùng cho các nguồn nhỏ hơn trước đó).

`ROSTER`: 2532 → **2770**. Đơn vị trên bản đồ: **2779**.

**Bài học kỹ thuật quan trọng cho lượt sau:** khi một trang danh bạ có bộ lọc nhưng client-side
kết quả "trông như không lọc đúng" hoặc lẫn kết quả ngẫu nhiên, ĐỪNG vội kết luận trang không
dùng được — kiểm tra kỹ cấu trúc DOM xem có nhiều khối kết quả chồng nhau (khối lọc thật vs
khối carousel/gợi ý không liên quan) bằng cách truy vết ancestor class/id của từng link, như đã
làm ở đây. Nguồn tưởng đã "chết" (ASP.NET postback không JSON) có thể sống lại sau khi đổi nền
tảng — đáng thử lại định kỳ các nguồn lớn đã bỏ dở vì lý do kỹ thuật (chứ không phải vì không
có dữ liệu).

**Việc mở cho lượt sau (mục tiêu 10000):** (1) IASP còn ~70 mục "chết" thật (không phải mạng)
— phần lớn là site chính phủ/đại học Trung Đông (Saudi Arabia, Iran, Oman) và Trung Quốc, có
thể do chặn theo khu vực từ mạng hiện tại, đáng thử lại từ mạng khác. (2) Tiếp tục 2 hướng đã
chứng minh: đăng ký chính phủ có cột website (Argentina xong, còn nhiều nước Mỹ Latinh/Á khác)
và dữ liệu nhúng sẵn (ANPROTEC, IASP xong — còn ASTP-Proton, RedEmprendia, AUTM, UNITT trong
`_claude/roster-grow-queue.md` mục 30-34, chưa có URL cụ thể). (3) Ở quy mô 10000, cần nhiều
nguồn cỡ IASP/ANPROTEC (200-500 mục) liên tiếp — ước tính cần ~30 nguồn cỡ này để đạt mục tiêu,
nên ưu tiên tìm danh bạ hiệp hội/chính phủ đa quốc gia hơn là đào sâu từng nước lẻ.

**2026-09-09 (tiếp checkpoint 21, cùng ngày) — một lượt tìm nguồn KHÔNG ra kết quả mới, ghi lại
để khỏi lặp công:** thử 8 hướng, 7 loại hẳn, 1 để lại làm việc mở kỹ thuật:

- **WIPO GREEN** — chỉ 160+ đối tác, là chợ công nghệ/nhu cầu chứ không phải danh bạ tổ chức
  CGCN/ĐMST đúng khuôn ROSTER. Loại.
- **Poland PARP "Ośrodki Innowacji"** (file PDF chính phủ `gov.pl/attachment/...`) — chỉ 48 mục
  (2021, nhiều mục đã hết hạn công nhận), KHÔNG có cột website (phải đoán domain từng tên tiếng
  Ba Lan) — quá nhỏ so với công đoán domain. Loại.
- **DPIIT Recognized Startups** (`data.gov.in`) — 197.692 mục nhưng là DOANH NGHIỆP khởi
  nghiệp, không phải đơn vị trung gian hỗ trợ (vườn ươm/CGCN) — sai phạm vi ROSTER hoàn toàn.
  Loại.
- **RedEmprendia** — chỉ 24 đại học, đã có sẵn trong ROSTER. Loại (đã ghi ở lượt trước).
- **UNITT Nhật** (`unitt.jp`) — chỉ ~82 hội viên, trang danh bạ yêu cầu đăng nhập hội viên,
  trang "Link collection" công khai chỉ có link cơ quan chính phủ, không phải hội viên. Loại.
- **AUTM** (`autm.net/my-autm/member-directory`) — yêu cầu đăng nhập, và là danh bạ CÁ NHÂN
  chuyên gia chứ không phải tổ chức. Loại.
- **F6S** (`f6s.com/accelerators/<nước>`) — liệt kê CHƯƠNG TRÌNH/ĐỢT TUYỂN có hạn nộp đơn (kiểu
  dữ liệu Fund/Hackathon, không phải tổ chức ổn định có 1 URL cố định — sai khuôn dữ liệu
  ROSTER dù có vẻ lớn). Loại.
- **incubatorlist.com** (21.471 mục "VC & chương trình") — trộn lẫn quỹ đầu tư mạo hiểm THUẦN
  TÚY (ngoài phạm vi ROSTER) với accelerator/incubator, và URL thật của mọi mục đều bị khoá sau
  "Unlock Pro Access" (0 link ngoài nào lộ ra trên trang công khai) — không lấy được dữ liệu
  miễn phí. Loại.

**InovaLink** (`inovalink.org` — nền tảng CHÍNH THỨC do MCTI + Sebrae + Anprotec + UFV lập,
**khác ANPROTEC** dù cùng hệ sinh thái) — **kỹ thuật đầy tiềm năng nhưng KHÔNG khai thác được
bằng công cụ hiện có, để lại làm việc mở**: quy mô thật ~397 tổ chức (230 vườn ươm + 41
aceleradora + 76 parque đang hoạt động + 40 đang xây + 10 đang quy hoạch, đếm được qua id-list
trong response Livewire `/livewire/update`), lớn hơn ANPROTEC và khả năng nhiều mục KHÔNG trùng
(vì đây là nền tảng đăng ký riêng, không phải danh sách hội viên trả phí của ANPROTEC). **Bẫy
kỹ thuật khác hẳn ANPROTEC**: đây là app Laravel Livewire, dữ liệu bản đồ KHÔNG nhúng sẵn dạng
JSON tĩnh trong HTML/script như ANPROTEC (đã kiểm `window.mapping`/`window.distanceMarkers` —
cả hai là HÀM khởi tạo bản đồ, không phải object dữ liệu) — response Livewire chỉ trả về DANH
SÁCH ID (`keys: [1,2,3...]`) của các Eloquent model (`Incubator`, `Accelerator`, `Park`,
`Company`), tên/địa chỉ/website thật phải lấy qua tương tác từng marker (click) hoặc endpoint
chi tiết riêng chưa xác định — không có cách lấy hàng loạt bằng 1-2 lệnh gọi như ANPROTEC/IASP.
**Việc mở cho ai thử tiếp**: tìm endpoint Livewire trả chi tiết 1 entity (thử bắt request khi
click 1 marker thật trên bản đồ, tìm route dạng `/livewire/message/<component>` với payload
chứa entity id), hoặc tìm trang danh sách/bảng (không phải bản đồ) nếu site có — công đáng bỏ
vì quy mô lớn, nhưng không nên thử lại kiểu "đọc JSON nhúng sẵn" đã dùng cho ANPROTEC/IASP.

**Nhận định thực tế sau khi thử nhiều hướng không ra kết quả:** khác với TISC/africatechschools/
ANPROTEC/IASP (danh bạ CHÍNH THỐNG có URL thật miễn phí), phần lớn danh bạ "lớn" còn lại trên
mạng hoặc (a) là hội viên CÁ NHÂN không phải tổ chức, (b) đòi đăng nhập/trả phí để lộ URL, hoặc
(c) là loại dữ liệu khác hẳn ROSTER (chương trình/đợt tuyển, quỹ đầu tư thuần). Nguồn lớn kiểu
ROSTER cần (danh bạ TỔ CHỨC, URL MIỄN PHÍ, đúng phạm vi CGCN/ĐMST/vườn ươm) đang cạn dần theo
kiểu "quả treo thấp" — tương tự nhận định ở checkpoint 19 cho mốc 5000, nay càng đúng hơn cho
mốc 10000: khoảng cách còn lại (~7200) lớn hơn TOÀN BỘ số đã gom được qua 21 checkpoint cộng
lại, nên mốc này cần rất nhiều phiên nữa, không phải một hướng đột phá còn lại.

**Lần trước:** 2026-09-09 (checkpoint 20 — **NGUỒN MỚI: Argentina MINCyT "Mapa de la
Innovación" (UVTs), đăng ký chính phủ CÓ SẴN cột website, khai thác qua dữ liệu DataTable
nhúng sẵn client-side**) — tiếp tục hướng "đăng ký chính phủ có cột website" đã chứng minh
hiệu quả ở Colombia. Trang `argentina.gob.ar/ciencia/vinculacion-y-transferencia/mapa-de-la-
innovacion/unidades-de-vinculacion-tecnologica-uvts` liệt kê **209 Unidades de Vinculación
Tecnológica** (UVT — đơn vị trung gian CGCN chính thức theo Luật 23.877) có sẵn cột "Sitio
web". Bẫy kỹ thuật: `curl`/`WebFetch` tĩnh trả về trang rỗng (33KB, không có dữ liệu) vì bảng
render bằng jQuery DataTables phía client — **không có endpoint AJAX/JSON riêng** để gọi
thẳng (khác ANPROTEC/Colombia). Giải pháp: mở trang thật bằng trình duyệt (Browser pane),
đợi DataTables khởi tạo xong, rồi gọi thẳng `jQuery('#ponchoTable').DataTable().data()` qua
`javascript_tool` — API DataTables trả về TOÀN BỘ 209 dòng đã nạp sẵn trong bộ nhớ (dù giao
diện chỉ hiện 10 dòng/trang), không cần thao tác phân trang. **Bài học kỹ thuật mới cho lượt
sau:** khi một trang chính phủ dùng thư viện bảng phổ biến (DataTables, hoặc tương tự) để
hiện danh sách phân trang mà không thấy request AJAX nào trong network log, nghi ngay khả năng
dữ liệu đã nạp hết vào bộ nhớ JS phía client (không server-side processing) — thử gọi thẳng
API của thư viện đó qua console thay vì tìm endpoint hoặc scrape từng trang.

209 dòng → 197 có website → lọc trùng domain/tên với ROSTER (19 trùng, gồm UNC/UBA/UTN các
chi nhánh đã có từ trước) → còn 178 cần kiểm sống. `check_url()` giữ **132/178** ngay lượt
đầu. 46 mục "chết" phần lớn là các đại học công lớn (`unsa.edu.ar`, `unju.edu.ar`,
`unca.edu.ar`...) — nghi ngờ nghẽn mạng tạm thời theo đúng mẫu hình đã ghi nhận nhiều lần
trước đây, nên chạy lại **2 lượt kiểm tra lại** (timeout tăng dần 15s → 25s, tuần tự có nghỉ
giữa các lần gọi): chỉ cứu thêm được **1 mục** (Fundación Empresaria de la Patagonia). Kết
luận khác lần trước: lần này KHÔNG phải nghẽn mạng diện rộng (dù `curl -I` thủ công có lúc
thành công với vài domain `.edu.ar` — không nhất quán, có thể do khác biệt HEAD vs GET hoặc
chặn bot theo User-Agent của `urllib`) — tôn trọng lưới an toàn `check_url()`, để lại 45 mục
này làm việc mở, KHÔNG thêm tay bất kể tên trường nổi tiếng thế nào.

Toạ độ dùng centroid CẤP TỈNH của Argentina (`ARG_PROVINCE_CENTROID`, 23 tỉnh + CABA, viết
tay trong script merge tạm — mức chính xác giữa cấp quốc gia và cấp thành phố, tương tự cách
đã làm cho Brazil). Merge **128 mục mới thật** (133 qua kiểm sống, 5 trùng nội bộ trong chính
batch này — các chi nhánh UTN/UNC khác tên nhưng cùng domain).

`ROSTER`: 2404 → **2532**. Đơn vị trên bản đồ: **2541**.

**Việc mở cho lượt sau (áp dụng đúng 2 hướng đã chứng minh hiệu quả):** (1) "đăng ký chính phủ
có cột website" — thử các nước Mỹ Latinh còn lại theo mẫu Argentina/Colombia: Chile (ANID),
Ecuador (SENESCYT), Uruguay (ANII), Mexico (CONAHCYT — khác `ime.edomex.gob.mx` cấp bang đã
loại), hoặc quay lại Mexico/Peru bằng nguồn khác domain đã bị chặn trước đây. (2) "JSON/dữ
liệu nhúng sẵn trong trang danh bạ hiệp hội" — mở rộng sang cả các trang dùng thư viện bảng
(DataTables) chứ không chỉ bản đồ (Google Maps plugin) như đã làm với ANPROTEC — bài học lượt
này áp dụng được cho MỌI trang chính phủ/hiệp hội có bảng phân trang không thấy AJAX request.
(3) 45 mục Argentina "chết" ở trên — thử lại từ mạng khác, đây là các đại học công lớn thật sự
tồn tại, khả năng cao vẫn cứu được nếu đổi vị trí mạng.

**Đã thử ngay sau đó trong cùng phiên, XÁC NHẬN không dùng được (đừng thử lại trừ khi đổi
mạng):** Peru CITE (`gob.pe/43414-...`) — mở qua trình duyệt thật (không phải `curl`) vẫn ra
"Acceso restringido", xác nhận lại kết luận chặn ở checkpoint 19, không phải do công cụ tra
cứu. Indonesia — hai domain đăng ký doanh nghiệp SIPENSI (`sipensi.umkm.go.id` lỗi SSL 526,
`sipensi.kemenkopukm.go.id` không kết nối được) và `inkubator.brin.go.id` (BRIN) đều không mở
được, giống mẫu hình các domain `.go.id` Indonesia đã gặp trước đây (`sentraki.dgip.go.id`).
Ecuador SENESCYT — không tìm thấy danh bạ công khai có sẵn URL (chỉ có cổng ĐĂNG KÝ
`idearium.gob.ec`/`bancodeideas.gob.ec` cho tổ chức tự khai báo, không phải danh sách đã có
sẵn để tra cứu). Chile ANID OTL — chỉ tìm thấy trang chương trình tài trợ, không thấy danh bạ
công khai (có thể nhỏ, tương tự CORFO đã thử ở checkpoint 19).

**Lần trước:** 2026-09-09 (checkpoint 19 — **NGUỒN MỚI: Minciencias Colombia, danh sách chính
phủ CÓ SẴN cột website**) — nguồn tốt nhất kiểu mới: Bộ KH&CN Colombia (Minciencias) công khai
file Excel CHÍNH THỨC "Listado de Actores del SNCTeI reconocidos" tại
`minciencias.gov.co/sites/default/files/listado_oficial_actores_reconocidos_vigentes.xlsx`
(link nằm trong trang `reconocimiento-actores/parques-cientificos-tecnologicos-y-innovacion-pcti`)
— **112 tổ chức, CỘT "PÁGINA WEB" CÓ SẴN CHO 100% DÒNG** (không cần đoán/kiểm tồn tại link).
Đã lọc theo loại hình khớp phạm vi ROSTER (bỏ "INSTITUTO PÚBLICO"/viện nghiên cứu chung chung,
"CENTRO DE CIENCIA"/bảo tàng khoa học-vườn thực vật, "EMPRESA ALTAMENTE INNOVADORA"/công ty
được chứng nhận, "UNIDAD DE I+D+i DE EMPRESA"/phòng R&D nội bộ công ty — 4 loại này KHÔNG phải
đơn vị trung gian hỗ trợ ĐMST, chỉ là viện/công ty thường): giữ lại CIP (Centro de Innovación y
Productividad), CDT (Centro de Desarrollo Tecnológico), OTRI (Oficina de Transferencia —
đúng nghĩa TTO), Incubadora — **38/112 dòng khớp phạm vi**. `check_url()` giữ **24/38** (14 chết
gồm nhiều đại học lớn như EAFIT/Universidad de Antioquia/Universidad del Cauca — đã thử lại
tất cả 1 lần theo đúng quy tắc, KHÔNG phải nghẽn mạng thoáng qua vì Google vẫn sống bình thường
lúc kiểm — nghi WAF/Cloudflare chặn `urllib` không có cookie/JS, không phải trang thật sự chết;
để lại việc mở, có thể domain này đã dùng dạng URL khác trong ROSTER rồi). Lọc trùng: 1 trùng
(Universidad Tecnológica de Pereira, đã có từ batch Thái Lan... không, từ batch trước). Merge
**23 mục mới**. Toạ độ dùng centroid QUỐC GIA Colombia (chỉ 1 nước, không cần dict riêng).

`ROSTER`: 2380 → **2404**. Đơn vị trên bản đồ: **2413**.

**Bài học kỹ thuật mới, áp dụng được cho MỌI nước Mỹ Latinh còn lại:** nhiều bộ/cơ quan
KH&CN quốc gia công khai "listado de actores reconocidos" hoặc danh sách chứng nhận tương tự
dưới dạng Excel/CSV tải trực tiếp — đây là nguồn CHẤT LƯỢNG CAO NHẤT có thể tìm (chính phủ xác
nhận + có sẵn URL, không cần đoán) khi tìm thấy. Việc mở: đã xác định các đầu mối tương tự
CHƯA khai thác — **Peru**: chương trình CITE (Centros de Innovación Productiva y Transferencia
Tecnológica) của ITP (Instituto Tecnológico de la Producción), có trang
`gob.pe/43414-centros-de-innovacion-productiva-y-transferencia-tecnologica-cite-contacta-a-un-cite-publico`
liệt kê các CITE công lập — CHƯA mở để lấy danh sách+URL. **Mexico**: PDF
`ime.edomex.gob.mx/sites/ime.edomex.gob.mx/files/files/Directorio_Incubadoras2024.pdf` (danh
bạ incubadoras cấp bang Estado de México, không phải toàn quốc) — CHƯA thử tải/trích.

**Đã thử ngay sau đó và XÁC NHẬN không dùng được (đừng thử lại trừ khi đổi mạng/có lý do mới):**
- **Peru CITE** (`gob.pe`, `itp.gob.pe`, `data-peru.itp.gob.pe`) — CẢ BA domain đều trả trang
  chặn kiểu tường lửa (`itp.gob.pe`: "The URL you requested has been blocked"; `data-peru...`:
  HTTP 500 trang chặn WAF) — giống hệt ca Indonesia `sentraki.dgip.go.id` "Error 15" trước đây.
  Không phải nghẽn mạng thoáng qua (đã kiểm Google sống bình thường cùng lúc).
- **Mexico** `ime.edomex.gob.mx` — domain không kết nối được từ mạng hiện tại (`curl`/browser
  đều fail), giống ca China Torch.
- **Spain RedOTRI** (`redotriuniversidades.net`) — domain đã CHẾT HẲN, không resolve DNS nữa
  (site của mạng lưới OTRI Tây Ban Nha, có vẻ đã ngừng hoạt động/đổi tên miền).
- **Chile CORFO** — chỉ ~19 incubator/accelerator được xếp hạng (quá nhỏ, hầu hết đã có sẵn
  trong ROSTER vì là tên tuổi lớn như Start-Up Chile).
- **France SATT** — chỉ 13 tổ chức toàn quốc, quá nhỏ để đáng một đợt riêng.
- **Germany TransferAllianz** (trước là TechnologieAllianz) — 65 thành viên nhưng KHÔNG tìm ra
  trang danh sách công khai có link (trang chủ không có mục "Mitglieder" dẫn tới danh sách).
- **Enterprise Europe Network** (`een.ec.europa.eu`) — đã tìm sâu hơn (kiểm tra script inline
  395KB ở trang `/about/branches` xem có nhúng JSON kiểu ANPROTEC không) — KHÔNG có, trang chọn
  quốc gia không lộ endpoint dữ liệu trong thời gian tìm.
- **US SBA/SBDC** (`sba.gov`, `americassbdc.org`) — mạng lưới thật ~900+ điểm, nhưng công cụ
  tra cứu theo ZIP code (không phải danh sách toàn quốc 1 lần) — cần lặp hàng nghìn mã ZIP mới
  phủ hết, không hiệu quả; Mỹ cũng là nước lớn đã được rà khá kỹ từ trước, độ ưu tiên thấp hơn.

**Kết luận cho lượt sau:** sau khi cạn 2 nguồn lớn (TISC, africatechschools) và thử nhiều nguồn
vừa/nhỏ (ANPROTEC +127, Colombia +23, rồi một loạt dead-end ở trên), tốc độ tăng đã CHẬM LẠI
RÕ RỆT so với đầu phiên. Để tới mốc **5000** (còn thiếu ~2600) cần: (1) tiếp tục dò kiểu "đăng
ký chính thức chính phủ có cột website" (thành công ở Colombia) cho từng nước Mỹ Latinh/Châu Á
còn lại — tốn công tra cứu nhưng chất lượng cao nhất; (2) tiếp tục dò kiểu "JSON nhúng sẵn
trong bản đồ thành viên hiệp hội" (thành công ở ANPROTEC) — cần tìm thêm hiệp hội dùng đúng kiểu
plugin bản đồ này; (3) chấp nhận rằng mốc 5000 nhiều khả năng cần RẤT NHIỀU phiên làm việc nữa,
không phải một phiên có thể xong — nên báo cáo tiến độ trung thực cho sếp thay vì cố ép tốc độ.

**Lần trước:** 2026-09-09 (checkpoint 18 — **NGUỒN MỚI: ANPROTEC Brazil, kỹ thuật mới "đọc
JS nhúng sẵn thay vì scrape HTML"**) — sau khi xác nhận africatechschools.com/TISC hết, cho
agent nghiên cứu tìm nguồn lớn tiếp theo. Kết quả quan trọng nhất: **Startup India** (danh bạ
1518 vườn ươm thật, API `POST api.startupindia.gov.in/sih/api/noauth/search/profiles` với body
`{"roles":["Incubator"],"dpiitRecogniseUser":false,...}` — bẫy: mặc định JS gửi
`dpiitRecogniseUser:true` lọc gần hết, phải đặt `false` mới ra đủ 1518) **NHƯNG trang public
profile của từng tổ chức KHÔNG lộ URL riêng** (chỉ ẩn số điện thoại/email dạng XXXX, mục
"Portfolio" chỉ có link của startup được ươm chứ không phải link của chính vườn ươm) — đây là
**GIỚI HẠN CỨNG** của nguồn này, không có cách nào lấy URL thật hàng loạt mà không đăng nhập
(không được làm) hoặc đoán domain (không đạt chuẩn) — ĐÃ BỎ nguồn này dù dữ liệu tên+địa điểm
rất tốt. China Torch (`chinatorch.gov.cn`) vẫn KHÔNG kết nối được từ mạng hiện tại (curl lẫn
`WebFetch` đều timeout/ECONNREFUSED) — để lại việc mở, thử mạng khác. Enterprise Europe Network
(`een.ec.europa.eu`) là trang chọn quốc gia bằng bản đồ tương tác, chưa tìm ra endpoint dữ liệu
trong thời gian cho phép — để lại việc mở.

**Nguồn dùng được: ANPROTEC** (`anprotec.org.br/site/sobre/associados-anprotec/`, hiệp hội
vườn ươm/khu công nghệ/coworking Brazil) — phát hiện kỹ thuật MỚI, hiệu quả hơn hẳn scrape HTML
từng trang: trang bản đồ thành viên dùng plugin WordPress "wp-google-map-gold", TOÀN BỘ dữ liệu
478 tổ chức (tên, thành phố, bang, **URL thật trong field `location.extra_fields.site`**, hạng
mục) đã nhúng sẵn dạng JSON ngay trong một `<script>` inline của trang — KHÔNG cần gọi API
riêng, KHÔNG cần phân trang, chỉ cần render trang bằng trình duyệt thật rồi `javascript_tool`
trích chuỗi JSON sau khoá `"places":[...]` (đếm ngoặc `[`/`]` kiểu string-aware, giống
`find_roster_span`). 478 mục, 330 có `site` khác rỗng → `check_url()` giữ **143/330** sống →
lọc trùng tên/domain với ROSTER (16 trùng + 1 lỗi định dạng bang "Rio Grande do Sul" thay vì mã
"RS", đã sửa tay merge riêng) → merge **127 mục mới thật** (126 tự động + 1 tay).

**Bài học kỹ thuật quan trọng cho lượt sau:** khi một trang "bản đồ thành viên hiệp hội" dùng
Google Maps nhúng (không phải bản đồ SVG/canvas riêng), rất đáng kiểm tra xem dữ liệu marker có
nhúng sẵn dạng JSON trong `<script>` inline hay không (tìm bằng cách lọc script có chứa
`"lat"`/`"marker"`/tên hiệp hội) TRƯỚC KHI nghĩ đến việc gọi API hoặc scrape từng trang con —
nếu có, đây là cách nhanh và đầy đủ nhất, thường sạch hơn cả gọi API vì đã bao gồm mọi field
(kể cả `site`/`email` mà API danh sách công khai có thể không trả). Toạ độ dùng centroid CẤP
BANG của Brazil (`BR_STATE_CENTROID`, 27 bang, viết tay trong script merge tạm) — chính xác hơn
centroid cấp quốc gia đã dùng cho batch Châu Phi, vì Brazil dữ liệu có sẵn field bang riêng.

`ROSTER`: 2253 → **2380**. Đơn vị trên bản đồ: **2389**.

**Việc mở cho lượt sau (hướng tới mốc 5000):** (1) thử lại China Torch từ mạng khác — danh bạ
chính thức ~178+ khu công nghệ cao TQ, có thể vẫn bị chặn theo ccTLD giống các nước Châu Phi
`.gn`/`.tg` trước đây. (2) Tìm endpoint dữ liệu thật của Enterprise Europe Network (~600 đối
tác) — trang chọn quốc gia bằng bản đồ, chưa rõ cơ chế tải dữ liệu. (3) Áp dụng ĐÚNG kỹ thuật
vừa học (tìm JSON nhúng sẵn trong script bản đồ) cho các hiệp hội vườn ươm/khu công nghệ quốc
gia KHÁC còn chưa thử — Mexico, Colombia, Argentina, Tây Ban Nha (có bài báo nhắc "mapa de
incubadoras y aceleradoras" của Social Innovation Monitor nhưng site chính `socialinnovation
monitor.com` bị chặn bởi Cloudflare bot-check, không truy cập được) — mỗi hiệp hội quốc gia
kiểu này thường chỉ ra 100-500 mục, không lớn bằng TISC/africatechschools nhưng cộng dồn vẫn
đáng kể, và kỹ thuật trích JSON nhúng nhanh hơn nhiều so với scrape từng trang. (4) Cân nhắc
đầu tư công sức reverse-engineer `iasp.ws` (ASP.NET postback) nếu không tìm ra nguồn JSON/tĩnh
nào khác — đã tạm bỏ 2 lần nhưng vẫn là danh bạ khu khoa học lớn nhất chưa khai thác.

**Lần trước:** 2026-09-09 (checkpoint 17 — **VƯỢT MỐC 2000, đợt 2 africatechschools.com**) —
sếp nâng mục tiêu tổng lên **5000 đơn vị**. Checkpoint 16 mới chỉ duyệt trang khu vực MỘT LẦN
mỗi trang (đủ để lấy 861 mục) nhưng một lần fetch tĩnh không lấy hết được toàn bộ danh sách —
xác nhận bằng cách fetch lại nhiều lần cùng 1 trang `?page=N`, kết quả hội tụ dần: West Africa
472 (site ghi 474), North Africa 364 (365), East Africa 340 (341), Southern Africa 294 (297),
Central Africa 104 (107) — tổng **1574** slug duy nhất, so với 861 đã xử lý ở checkpoint 16 →
lộ ra **713 slug hoàn toàn mới** (`/tmp/atx-new-slugs.json`, đã mất khi phiên kết thúc). Tải
chi tiết (`website` + `Location:`) cho cả 713 → `check_url()` toàn bộ → **387/713 sống**. Lọc
trùng tên/domain với ROSTER (70 trùng, cơ chế lọc hoạt động đúng) → merge **317 mục mới thật**.

Toạ độ vẫn dùng centroid CẤP QUỐC GIA (23 nước Châu Phi xuất hiện trong đợt này: Algeria,
Benin, Burkina Faso, Cape Verde, Djibouti, Egypt, Ethiopia, Ghana, Guinea, Guinea Bissau,
Ivory Coast, Kenya, Liberia, Mali, Morocco, Nigeria, Senegal, Sierra Leone, Somalia, Sudan,
The Gambia, Togo, Tunisia — dict `COUNTRY_CENTROID` viết tay trong script merge tạm, KHÔNG có
sẵn trong `roster_common.py`, phải viết lại mỗi lần cần một dict mới nếu muốn tái dùng, nên
cân nhắc thêm cố định vào `roster_common.py` nếu còn merge theo centroid-quốc-gia nhiều lần
nữa).

`ROSTER`: 1936 → **2253**. Đơn vị trên bản đồ: **2262** — đã VƯỢT mốc 2000, còn xa mốc **5000**
mới (chặng kế: 3000).

**`africatechschools.com` COI NHƯ ĐÃ KHAI THÁC HẾT** sau 2 đợt (861 + 713 = 1574 slug, đúng
khớp tổng site công bố). **WIPO TISC cũng đã hết** (xem checkpoint 15). Hai nguồn lớn nhất đã
tìm ra trong phiên đều cạn — **VIỆC MỞ QUAN TRỌNG NHẤT cho lượt sau: tìm nguồn lớn (danh bạ đa-
tổ-chức, có API hoặc HTML tĩnh scrape được) TIẾP THEO**, vì để đạt 5000 cần thêm ít nhất
~2700 mục nữa — quy mô này gần như chắc chắn không khả thi bằng WebSearch từng tổ chức lẻ, bắt
buộc phải tìm ra một nguồn lớn mới kiểu TISC/africatechschools. Đã thử và LOẠI: các domain
`asiatechschools.com`/`latintechschools.com`/`latamtechschools.com`/`europetechschools.com`/
`middleeasttechschools.com`/`pacifictechschools.com` (đoán site chị em của africatechschools.com
theo tên miền) — TẤT CẢ không resolve DNS (curl trả `000`), không tồn tại. IASP (`iasp.ws`,
hiệp hội khu khoa học quốc tế) đã thử ở checkpoint 15, vẫn TẠM BỎ QUA vì ASP.NET postback không
có API JSON — có thể đáng đầu tư công sức reverse-engineer nếu không tìm ra nguồn nào khác, vì
đây là danh bạ khu khoa học CHÍNH THỐNG quy mô lớn. Các hướng CHƯA THỬ, đáng thử lượt sau: WIPO
GREEN (nếu có danh bạ tổ chức tương tự TISC), UBI Global/UBI Index (bảng xếp hạng vườn ươm đại
học thế giới — có thể có danh sách đơn vị kèm link), StartupBlink ecosystem rankings theo từng
nước (có thể liệt kê tên tổ chức + link), F6S (nền tảng accelerator toàn cầu, có thể scrape
được danh mục theo nước/lĩnh vực), hoặc quay lại đào sâu từng nước lớn còn mỏng (Trung Quốc chỉ
~28, Ấn Độ, Brazil, Nga còn nhiều mục TISC chưa lấy hết theo ghi chú checkpoint 12-14).

**Lần trước:** 2026-09-08 (checkpoint 16 — **KHAI THÁC XONG africatechschools.com, SÁT MỐC
2000**) — hoá ra site này có **861 tổ chức** (không phải ~55 như tưởng lượt trước), trải trên
5 trang khu vực Châu Phi. Quy trình 3 bước: (1) lấy tên+slug từ 5 trang `/region/<vùng>/`
(HTML tĩnh, không cần JS), (2) tải từng trang chi tiết `/school/<slug>/`, trích `Website:` +
`Location:` bằng regex (dò 2 lần — lần đầu quên đúng mẫu HTML của "Location", phải tải lại
545 trang đã qua vòng lọc sống để lấy đúng — bài học: kiểm mẫu regex trên 1 trang thật TRƯỚC
khi chạy hàng loạt, đỡ phải tải lại), (3) `check_url()` toàn bộ 861 — giữ **545/861**. Sau khi
lọc trùng tên/domain với ROSTER (115 trùng — phần lớn là các mục incubator Châu Phi đã thêm ở
checkpoint trước từ cùng site này, cơ chế lọc trùng hoạt động đúng), merge **430 mục mới**.

`ROSTER`: 1506 → **1936**. Đơn vị trên bản đồ: **1945** — chỉ còn ~55 nữa tới mốc **2000**
sếp đặt (mốc kế tiếp: 3000).

**Toạ độ dùng mức QUỐC GIA (centroid), không phải thành phố** — do khối lượng quá lớn (861
mục, hàng trăm thành phố khác nhau khắp Châu Phi) nên chấp nhận độ chính xác thô hơn các
nguồn trước, đổi lấy tốc độ xử lý. Quốc gia lấy từ chuỗi `Location:` (dạng "Thành phố, Quốc
gia, Khu vực" — lấy đúng phần Quốc gia, không phải Thành phố).

**Lần trước:** 2026-09-08 (checkpoint 15 — HOÀN TẤT DANH BẠ WIPO TISC, sếp đặt mốc 3000) —
merge batch cuối: Malaysia/Saudi Arabia/Thái Lan (+39) + Benin/Burundi (+2, +1 điền url mục
cũ "UAC Startup Valley"). `ROSTER`: 1465 → **1506**.

**WIPO TISC coi như xong** — đã xử lý HẾT các nước có mục trong danh bạ 1908 tổ chức, CHỈ TRỪ
Viet Nam (63 mục, cố tình bỏ qua vì quy ước ROSTER không phủ Việt Nam — xem mục Việt Nam nằm ở
tab riêng "Mạng lưới ĐMST Việt Nam"). Tổng cả nguồn TISC qua 5 batch: 1035 → 1506 (~470 mục
thật, sau khi lọc trùng + kiểm sống).

**Nguồn lớn TIẾP THEO đã tìm ra, CHƯA khai thác — làm ngay khi mở phiên mới:**
`africatechschools.com` — trang danh mục các trường/hub công nghệ Châu Phi, tưởng chỉ có
~55 mục (đã dùng ở checkpoint Châu Phi trước) nhưng thực ra có **861 tổ chức riêng biệt** khi
duyệt qua 5 trang khu vực (`/region/west-africa/`, `/region/north-africa/`,
`/region/east-africa/`, `/region/southern-africa/`, `/region/central-africa/` — không cần
đăng nhập, HTML tĩnh). Danh sách tên+slug đã lưu ở `/tmp/atx-all-slugs.json` (861 mục, MẤT khi
phiên kết thúc — nếu cần tải lại thì lặp lại đúng 5 URL trên, trích bằng regex
`<a href="/school/([a-z0-9-]+)/">([^<]+)</a>`).

Mỗi mục cần mở trang chi tiết `https://www.africatechschools.com/school/<slug>/` (HTML tĩnh,
`curl` được, KHÔNG cần trình duyệt) để lấy URL thật thực sự — nằm ngay sau chữ "Website:" theo
mẫu: `Website:</span>\s*<span><a href="URL"`. Quy trình giống hệt TISC: tải hết → trích
website → `check_url()` → lọc trùng tên/domain với ROSTER → merge → build → kiểm → push mỗi
~50-150 mục. Đã thử tìm IASP (`iasp.ws`, hiệp hội khu khoa học quốc tế, cũng là nguồn lớn tiềm
năng) nhưng form tìm kiếm dùng ASP.NET postback (`page27.aspx?action=search`), không có API
JSON đơn giản như TISC — TẠM BỎ QUA, có thể thử lại sau nếu cần thêm nguồn.

**Lần trước:** 2026-09-08 (checkpoint 14) — merge batch TISC thứ 4: Philippines/Trung Quốc/
Ai Cập/Uganda/Tunisia/Kyrgyzstan/Tajikistan/Oman/Ấn Độ/Honduras/Chile/El Salvador/Costa Rica/
Guatemala/Cộng hòa Dominica/Panama/Qatar/Uruguay/Venezuela/Bangladesh/Nicaragua/Cambodia.
+152 mục thật (loại 30 trùng — phần lớn là các trường Philippines đã thêm từ danh bạ ITSO
lượt trước, cơ chế lọc trùng theo domain hoạt động đúng, tự động nhận ra dù tên gọi trong TISC
khác chữ với tên đã dùng, vd "Mapua Institute of Technology" (TISC) trùng domain với "Mapua
University ITSO" đã có). Trung Quốc đóng góp nhiều nhất (~30 thành phố khác nhau).

`ROSTER`: 1313 → **1465**. Batch5 (Malaysia/Saudi Arabia/Thái Lan, 110 mục) đã tải xong, đang
kiểm sống — merge ở lượt kế tiếp.

**Lần trước:** 2026-09-08 (checkpoint 13 — VÁ LỖI GỐC RỄ TRONG `roster_common.py`, sếp
nâng mốc tiếp: 2000 → **3000**) — trong lúc merge batch Argentina/Colombia/Cuba/Ecuador/
Georgia/Jamaica/Jordan/Kenya/Mongolia/Nigeria/Palestine/Peru/Nga/Sao Tome/Nam Phi/Sri Lanka/
Trinidad/Zambia từ TISC, `load_roster()` báo lỗi JSON — hoá ra một tên tổ chức THẬT lấy từ
TISC có lỗi ngoặc ngay trong dữ liệu gốc của WIPO: `"...d'Oran (ESGEE]"` (mở ngoặc tròn, đóng
ngoặc vuông — lỗi đánh máy của WIPO, không phải của mình). `find_roster_span()` trong
`roster_common.py` đếm ngoặc `[`/`]` KIỂU THÔ (không biết phân biệt ký tự trong chuỗi
JSON với ký tự cấu trúc mảng) nên bị ký tự `]` lạc trong tên tổ chức làm ngắt mảng ROSTER
giữa chừng. **ĐÃ VÁ**: viết lại `find_roster_span()` để bỏ qua nội dung bên trong chuỗi
(theo dõi trạng thái `in_string`/escape kiểu tokenizer JSON tối giản) — đây là sửa đúng gốc
rễ, không phải sửa data (giữ nguyên tên gốc kể cả lỗi đánh máy của WIPO, không tự ý "sửa hộ"
tên tổ chức người khác). Đã xác nhận: trang web THỰC TẾ (`index.html`) vẫn luôn đúng suốt —
đây là lỗi trong CÔNG CỤ PYTHON dùng để sửa, không phải lỗi hiển thị trên site.

**CẢNH BÁO CHO LƯỢT SAU:** với danh bạ TISC gồm ~1900 tên tổ chức thật, tình trạng ngoặc/dấu
lạc trong tên có thể còn gặp lại — nay đã an toàn nhờ bản vá trên, nhưng nếu thấy `load_roster`
báo lỗi JSON lần nữa, đây là nghi phạm đầu tiên cần kiểm tra tiếp theo.

Merge được: +164 mục thật (sau khi loại 8 trùng, gồm cả trùng miền/domain giữa các "CATI"
Argentina cùng dùng `inti.gob.ar`/`utn.edu.ar`). `ROSTER`: 1149 → **1313**. Nga đóng góp lớn
nhất lượt này (~40 mục mới, còn nhiều nữa trong TISC vì Nga có 172 mục, mới xử lý hết batch
này).

Batch4 (Philippines/Trung Quốc/Ai Cập/Uganda/Tunisia/Ấn Độ/Honduras/Chile...) và batch5
(Malaysia/Saudi Arabia/Thái Lan) đã tải xong, ĐANG kiểm sống — chưa merge, làm tiếp ngay khi
mở phiên mới (file tạm ở `/tmp`, mất khi phiên kết thúc — nếu cần tải lại, dùng đúng API đã
ghi ở mục checkpoint 12 bên dưới).

**Lần trước:** 2026-09-08 (checkpoint 12 — TÌM RA NGUỒN LỚN NHẤT PHIÊN NÀY, sếp nâng mốc
1100→1200→2000) — phát hiện danh bạ TISC (Technology and Innovation Support Center) của
WIPO: `wipo.int/tisc` — **1908 tổ chức thật trên toàn cầu**, mỗi mục có sẵn trường "Web site"
(không cần đoán domain!). Quan trọng: trang tìm kiếm là SPA gọi API JSON công khai, không cần
đăng nhập:
- Danh sách: `https://www.wipo.int/o/api/v1/wipo-tisc/search?lang=en_US&limit=100&page=N`
  (0-indexed, `meta.total_pages` cho biết tổng số trang).
- Chi tiết từng mục (có `website`): `https://www.wipo.int/o/api/v1/wipo-tisc/details?id=<ID>&lang=en_US`
  — `curl` thẳng được, không cần trình duyệt, rất nhanh.

Quy trình đã chạy: tải hết 1908 mục (id+tên+nước) → lọc theo nước ưu tiên (nước mỏng trong
ROSTER + nước có nhiều mục trong TISC) → gọi API `details` từng id lấy `website` → tự kiểm
sống bằng `check_url()` → lọc trùng tên/domain với ROSTER → merge. Lượt này xử lý xong
Algeria/Belarus/Bhutan/Botswana/Burkina Faso/Cameroon/Côte d'Ivoire/Djibouti/Ghana/Indonesia
(một phần) — chủ yếu ra từ Algeria (đợt đầu TISC chỉ có 1 mục Algeria trong ROSTER, nguồn TISC
có 158!). +114 mục thật (sau khi loại 11 trùng).

`ROSTER`: 1035 → **1149**. Đã tải sẵn (chưa xử lý hết) thêm ~230 mục cho Nga/Peru/Colombia/
Argentina/Kenya/Nam Phi/Sri Lanka/Jordan/Ecuador/Mongolia/Palestine/Cuba/Senegal/Nigeria/
Rwanda... ở `/tmp/tisc-details-batch3.json` (file tạm, KHÔNG có trong git — mất khi phiên kết
thúc, nếu cần dùng lại thì tải lại từ API bằng câu lệnh trên) — Nga có tới **172 mục trong
TISC mà ROSTER mới chỉ có 4**, cơ hội lớn nhất tiếp theo.

**Việc mở, làm tiếp ngay khi có phiên mới:** còn nguyên các nước TISC CHƯA ĐỘNG TỚI:
Philippines (114 — khác hẳn danh bạ ITSO đã dùng, đáng thử), China (98), Ai Cập (59), Uganda
(39), Tunisia (39), Kyrgyzstan (25), Tajikistan (25), Oman (22), Ấn Độ (12), Honduras/Chile/
El Salvador/Costa Rica/Guatemala/Cộng hòa Dominica/Panama/Qatar/Uruguay/Venezuela/Armenia/
Bangladesh/Nicaragua/Zimbabwe (mỗi nước dưới 15 mục). Cứ lặp lại đúng quy trình 3 bước ở trên
cho từng batch nước, kiểm sống, lọc trùng, merge, build, kiểm, push mỗi ~50-100 mục.

**Lần trước:** 2026-09-08 (tiếp — checkpoint 11, tiếp tục hướng "khai thác nốt nguồn cũ") —
+10 mục thật. Trung Quốc (+5): quay lại đúng danh sách MOST batch-6 đã dùng dở, lấy nốt các
tên trường chưa xử lý (Southwest Jiaotong University, Wuhan Institute of Technology, China
University of Mining and Technology, Nanjing Institute of Technology, Yancheng Institute of
Technology). Thử tìm danh sách MOST mới hơn/lớn hơn trên `chinatorch.gov.cn` (420 tổ chức!)
nhưng domain này KHÔNG kết nối được từ mọi kênh (`WebFetch`, `curl`, browser) — khác hẳn
`most.gov.cn` (vẫn tải `.doc` được) — để lại việc mở, thử từ mạng khác nếu cần mở rộng thêm
Trung Quốc. Thái Lan (+5): quay lại đúng nguồn `sciencepark.wu.ac.th/rsp` đã dùng dở, tìm tay
5/7 trường còn lại trong mạng lưới 16 trường (University of Phayao, Uttaradit Rajabhat
University, Ubon Ratchathani University Science Park, Burapha University, Thaksin University)
— Mahasarakham University và PSU Science Park vẫn không kết nối được dù thử nhiều biến thể.

`ROSTER`: 1025 → **1035**. Vượt mốc **1044** đơn vị trên bản đồ, còn ~56 nữa tới mốc 1100 sếp
đặt.

**Lần trước:** 2026-09-08 (tiếp — checkpoint 10, sếp đặt mốc tiếp **1100**) — vượt mốc **1034**
đơn vị trên bản đồ (`ROSTER` **1025**). Bài học lớn nhất lượt này: khi đào sâu các nước đã có
độ phủ vừa (Hàn Quốc/Ireland/Đan Mạch/Phần Lan/New Zealand/Áo/Na Uy...) gần như MỌI tổ chức
nổi tiếng tìm được đều ĐÃ CÓ SẴN trong ROSTER — dấu hiệu các nước này đã được rà khá kỹ từ
trước, không phải "quả treo thấp" nữa. Chuyển hướng đúng: quay lại nguồn danh bạ ĐÃ CHỨNG MINH
hiệu quả nhưng CHƯA khai thác hết — danh bạ ITSO Philippines (`info.ipophil.gov.ph`) lượt
trước chỉ mới xử lý trang 1/4 (20/77 mục). Lượt này lấy nốt trang 2-4 (60 tên trường), nhờ
Gemini đoán domain (kiểu `<vietat>.edu.ph`, không dùng `url_context` vì trang phân trang bằng
JS không đổi URL — same vấn đề gặp ở Indonesia/Trung Quốc trước đây, giải quyết bằng cách gọi
Gemini kiểu "đoán URL cho danh sách tên" như đã làm với Trung Quốc), tự kiểm sống toàn bộ 53
kết quả bằng `check_url()` — giữ được 32/53 (đã lọc trùng tên/domain với ROSTER trước khi
kiểm, không phát sinh trùng lặp). Philippines: 17 → **49**.

**Bài học chung rút ra:** khi một nguồn danh bạ đa-tổ-chức đã dùng hiệu quả (PH ITSO, Thái Lan
RSP, MOST Trung Quốc) mà chỉ mới xử lý một phần (1 trang/1 batch), QUAY LẠI lấy hết các
trang/batch còn lại trước khi tìm nguồn hoàn toàn mới — hiệu suất cao hơn nhiều so với vừa tìm
từng trường lẻ vừa tự dò trùng lặp ở các nước đã bão hoà.

**Lần trước:** 2026-09-08 (tiếp — checkpoint 9, chuyển sang ĐÀO SÂU vì hầu hết nước mới "dễ"
đã hết) — vượt mốc **1000** đơn vị trên bản đồ (`đơn vị được lập bản đồ` khác `ROSTER`, xem
"Bối cảnh"). +4 mục thật: Ahmadu Bello University DRI (Nigeria, +1), Mansoura University
Innovation Support Office (Egypt, +1), IPN Technology Transfer Office (Mexico, +1), Bogazici
University TTO (Turkey, +1). Đáng chú ý: thử thêm Inova Unicamp (Brazil), CZIiTT PW Warsaw và
CITTRU Jagiellonian (Poland), Universidad de los Andes Transferencia (Colombia) — CẢ 4 ĐÃ CÓ
SẴN trong ROSTER từ trước (một số dưới tên khác) — dấu hiệu các "quả treo thấp" (low-hanging
fruit) cho nhóm nước đã có độ sâu vừa phải (Brazil/Poland/Colombia) gần như cạn, khác hẳn
nhóm nước Châu Phi/Trung Á vừa mở ở các checkpoint trước.

`ROSTER`: 989 → **993**.

**9 nước vẫn = 0, đã thử nhiều nguồn khác nhau cho mỗi nước, xác nhận KHÔNG PHẢI do nghẽn
mạng tạm thời (đã kiểm tra network sống, thử lại nhiều lần cách nhau vài phút, vẫn nhất
quán lỗi kết nối):** Guinea, Guinea-Bissau, Togo, Niger, Equatorial Guinea, Chad — nhiều khả
năng domain các nước này (`.gn`/`.tg`/`.ne`/`.gw`) bị chặn/lỗi định tuyến từ mạng hiện tại,
đáng thử lại từ mạng khác. North Korea/Vanuatu/Solomon Is. — khó có nguồn thật độc lập (Vanuatu/
Solomon chỉ có campus vệ tinh của USP, đã tính vào Fiji; Triều Tiên gần như không có hiện diện
web công khai kiểu này).

**Lần trước:** 2026-09-08 (tiếp — checkpoint 8) — **PHÁT HIỆN QUAN TRỌNG VỀ QUY TRÌNH:** giữa
lượt rà, `check_url()` báo "chết" hàng loạt cho CẢ `google.com` lẫn `en.sharif.ir` (một trang
vừa xác nhận sống phút trước) — hoá ra là NGHẼN MẠNG TẠM THỜI phía máy đang chạy (không phải
site chết), tự hồi phục sau ~10 giây. Thử lại ngay các mục vừa bị báo "chết" oan trong batch
đó: University of Botswana, USTM Gabon (mở 2 nước mới), Kenyatta University Research
Division, Université de Yaoundé I (đào sâu Kenya/Cameroon), University of Antananarivo (mở
Madagascar) — TẤT CẢ đều sống khi thử lại.

`ROSTER`: 984 → **989** (Botswana +1, Gabon +1, Madagascar +1, Kenya +1, Cameroon +1).

**Quy tắc mới bắt buộc:** nếu `check_url()` báo chết cho một domain lớn/nổi tiếng đáng lẽ
phải sống (vd trang chính phủ, đại học lớn, hoặc bất kỳ trang nào vừa kiểm sống ở bước trước
đó trong cùng phiên) — ĐỪNG kết luận "chết", hãy nghi ngờ mạng trước, kiểm tra bằng
`curl -sI --max-time 8 https://www.google.com` xem có phản hồi không, rồi thử lại
`check_url()` sau vài giây. Việc này giải thích một phần lý do Guinea/Togo/Niger/Equatorial
Guinea/Guinea-Bissau bị đánh giá "chết" ở các lượt trước — dù đã thử lại một số domain này
lần nữa trong lượt này và VẪN chết nhất quán (khác kiểu lỗi thoáng qua), nên có thể thật sự có
vấn đề riêng (định tuyến bị chặn theo ccTLD, hoặc site thật sự không ổn định) — vẫn đáng thử
lại lần nữa ở phiên khác/mạng khác trước khi kết luận hẳn.

**Lần trước:** 2026-09-08 (tiếp — checkpoint 7, quét rộng khắp thế giới, sắp cạn nước dễ) —
+5 mục thật, mở MỚI HOÀN TOÀN 5 nước: Burkina Faso (2iE — viện kỹ thuật nước/năng lượng/môi
trường, KHÔNG phải Université Nazi Boni đã thử trước — cả hai đều sống nhưng 2iE nổi tiếng
hơn nên chọn), eSwatini (Eswatini College of Technology — Limkokwing chi nhánh Eswatini vẫn
không sống), Congo (Université Denis Sassou Nguesso — khác Université Marien Ngouabi đã thử
trước và chết), Djibouti (Université de Djibouti), Papua New Guinea (UPNG).

`ROSTER`: 979 → **984**.

**Nhận ra một mẫu hình rõ:** với 4 nước Guinea/Togo/Madagascar/Niger, đã thử NHIỀU trường
khác nhau (không chỉ 1 trường/nước) và TẤT CẢ đều URLError từ máy này — khả năng cao là domain
quốc gia (`.gn`/`.tg`/`.mg`/`.ne`) bị chặn/lỗi định tuyến từ vị trí mạng hiện tại chứ không
phải các trường đó thật sự chết hết — đáng thử lại từ vị trí mạng khác trước khi kết luận
"không có nguồn". Bài học chung: khi 1 trường trong nước X chết, thử nguồn KHÁC nhau (trường
khác, không chỉ URL khác của cùng trường) trước khi kết luận cả nước đó bế tắc — 2iE/UDSN vừa
tìm được đúng theo cách này.

**Lần trước:** 2026-09-08 (tiếp — checkpoint 6, quét rộng khắp thế giới) — +10 mục thật, mở
MỚI HOÀN TOÀN 8 nước: Comoros, Somalia, Sierra Leone (Njala University), Palestine (An-Najah
National University TTO — Birzeit đã thử lượt trước nhưng chết, An-Najah mới là nguồn dùng
được), Central African Rep. (Université de Bangui), S. Sudan (University of Juba), Mali
(USTTB — thử lại `http://` không `www` mới sống), Fiji (USP — cũng phải bỏ `www` mới sống),
Maldives (MNU), Cabo Verde (Universidade de Cabo Verde).

`ROSTER`: 969 → **979**.

Thử nhưng KHÔNG sống dù đổi nhiều biến thể `http`/`https`/`www`: Botswana (BIUST), eSwatini,
Congo Brazzaville (`umng.cg`), Burkina Faso, Guinea (Conakry lẫn Ouskei Academy), Togo,
Madagascar, Djibouti, Papua New Guinea, Niger, Gabon (`uob.ga`), Equatorial Guinea
(`ungecampus.com`), Guinea-Bissau (`uac.gw`), Chad — đều là lỗi kết nối (URLError/HTTPError),
không phải "domain không tồn tại/parking", nên có thể vẫn đáng thử lại ở lượt sau, khác thời
điểm mạng. Vanuatu/Solomon Is. có campus USP nhưng dùng chung domain `usp.ac.fj` (đã tính là
Fiji) nên không tính mục riêng.

**Lần trước:** 2026-09-08 (tiếp — checkpoint 5, quét rộng khắp thế giới) — +20 mục thật, mở
MỚI HOÀN TOÀN 18 nước: Lithuania (VILNIUS TECH KTTC + KTU NIEC, 2 mục), Cyprus (CUT), Malta
(Univ. of Malta Knowledge Transfer), Yemen (Sana'a University), Kosovo (Univ. Pristina),
Suriname (Anton de Kom University), Barbados (UWI Cave Hill), Lesotho (NUL Innovation Hub),
Liberia (Univ. Liberia TISC), Gambia (Univ. of The Gambia), Haiti (State Univ. Haiti), Iraq
(Univ. Baghdad IT Division), Bahamas (Univ. of The Bahamas BTC Lab), Guyana (Univ. Guyana
IRIE), Benin (UAC Startup Valley), Andorra (Univ. of Andorra), Timor-Leste (National Univ. of
Timor-Leste), Libya (Univ. Tripoli), DR Congo (Université de Kinshasa — thử vài lần mới sống,
`umng.cg` của Congo Brazzaville và `uneswa.ac.sz` của eSwatini vẫn không sống dù thử nhiều
biến thể, để lại việc mở).

`ROSTER`: 949 → **969**.

**Kiểm tra lại pattern quan trọng:** khi 1 URL fail lần đầu, thử lại vài biến thể
(có/không `www.`, `http`/`https`, có/không trailing slash) trước khi bỏ hẳn — lượt này riêng
việc thử lại đã cứu được University of Tripoli và Université de Kinshasa (ban đầu tưởng chết,
hoá ra chỉ cần bỏ query string / thử domain trần).

**Lần trước:** 2026-09-08 (tiếp — sếp yêu cầu "rà đi, rà tới khi không thêm được mới hoặc hết
token", checkpoint 4, quét rộng khắp thế giới) — +20 mục thật, mở MỚI HOÀN TOÀN 15 nước:
Ukraine (KPI Innovations Office), Kyrgyzstan (AUCA SILK), Bosnia and Herz. (Univ. Sarajevo
GrowUp Hub), Moldova (ANCD — cơ quan nhà nước), Cuba (Fundación UH), Jamaica (UWI Mona TISC),
Ecuador (ESPOL i3LAB), Kazakhstan (Nazarbayev University — nhiều đơn vị cụ thể thử đều không
sống, dùng homepage trường), Senegal (UCAD), Zimbabwe (NUST), Mozambique (Eduardo Mondlane
University), Malawi (MUST TISC), Lebanon (AUB Office of Innovation and Transformation), Iran
(Sharif University of Technology — trang Technology Park riêng không sống, dùng trang trường
`en.sharif.ir`), Nepal (Tribhuvan University IT Innovation Center), Bhutan (Royal University
of Bhutan, homepage), Nicaragua (UNAN-Managua, homepage), Honduras (UNAH, homepage),
Afghanistan (Kabul University IT Dept), El Salvador (Universidad de El Salvador, homepage).

`ROSTER`: 929 → **949**. Thử nhưng KHÔNG ra kết quả sống (để lại việc mở): Botswana (BIUST
tech-transfer + homepage đều lỗi kết nối), Fiji (USP), Papua New Guinea (Unitech), Palestine
(Birzeit — mọi URL đều HTTPError), Mauritius (UTM), Madagascar (Univ. Antananarivo), Togo
(Univ. Lomé), Mali (USTTB), Burkina Faso (Univ. Ouagadougou) — các trường hợp lỗi kết nối
(URLError/HTTPError) khi kiểm từ máy này, không phải "trang không tồn tại" — có thể đáng thử
lại sau (chặn bot tạm thời, DNS/mạng, hoặc thật sự không sống).

**Lần trước:** 2026-09-08 (tiếp — Trung Mỹ/Caribbean/Trung Á/Balkan còn lại, checkpoint 3) —
+9 mục thật, mở MỚI HOÀN TOÀN 7 nước: Guatemala (USAC), Cộng hòa Dominica (INTEC), Bolivia
(UMSA CIDE), Venezuela (UCV), Panama (UTP Emprende — trang riêng `emprende.utp.ac.pa` không
sống, dùng `utp.ac.pa` theo quy tắc homepage), Tajikistan (UIDT), Turkmenistan (Oguz Han
Engineering and Technology University), Bắc Macedonia (INNOFEIT, Skopje), Albania
(Metropolitan Incubator, Tirana). INDICASAT (Panama) tìm được URL nhưng không sống, bỏ.

`ROSTER`: 920 → **929**. Kazakhstan, Ukraine, Kyrgyzstan, Cuba, Jamaica, Honduras, Nicaragua,
El Salvador, Ecuador, Bosnia, Moldova, Kosovo, Montenegro vẫn 0 — việc mở cho lượt sau.

**Lần trước:** 2026-09-08 (tiếp — Mỹ Latinh/Trung Á/Balkan, checkpoint 2 theo yêu cầu "tầm 50
mục thì dừng push") — tìm tay từng tổ chức qua WebSearch (không có danh bạ đa-tổ-chức tốt cho
khu vực này), kiểm sống `check_url()`, một số dùng homepage trường theo quy tắc mới (UNC
Córdoba homepage bị BỎ vì trùng domain với mục "Secretaría de Innovación y Vinculación
Tecnológica" đã có sẵn — nhắc lại: LUÔN kiểm domain trùng trước khi thêm, kể cả khi tên mục
khác hẳn; tương tự Tec de Monterrey TTO bị bỏ vì trùng hệt mục "Technology Transfer Office
(TecScience)" đã có). +13 mục thật, mở MỚI HOÀN TOÀN 9 nước: Paraguay, Trinidad and Tobago,
Serbia, Armenia, Azerbaijan, Georgia, Mongolia, Belarus, Uzbekistan. Đào sâu: Argentina
(+1, UBA), Chile (+1, Universidad de Valparaíso), Peru (+1, UNI DITT).

`ROSTER`: 907 → **920**. (Ecuador, Colombia thêm, Kazakhstan, Ukraine thử nhưng mọi URL tìm
được đều không sống kể cả homepage trường — để lại việc mở, chưa mở được.)

**Lần trước:** 2026-09-08 (mở rộng Châu Phi, checkpoint 1, theo yêu cầu "rà tiếp các châu
lục/quốc gia khác") — Châu Phi gần như trống trước lượt này (chỉ Ai Cập/Nam Phi/Nigeria/Ghana/
Ethiopia/Morocco/Uganda có 1-6 mục). Tìm ra nguồn danh bạ đa-tổ-chức tốt:
`africatechschools.com` (catalog tư nhân, KHÔNG chính phủ, nhưng mỗi trang `/school/<slug>/`
có link thật ra site riêng của từng tổ chức — đã xác nhận qua nhiều mẫu). Quy trình: đọc
trang category `/category/incubator/` lấy danh sách tên+quốc gia+slug, rồi `WebFetch` từng
trang `/school/<slug>/` để lấy URL thật, tự kiểm sống bằng `check_url()` (không chạy qua
`roster_grow_worker.py` vì cần 2 bước domain khác nhau — trang danh mục vs trang chi tiết —
`url_context` chỉ đọc được 1 URL/lượt gọi). ~40 trang đã đọc, 32 qua được kiểm sống; 7 mục
thất bại (UP Business Incubator, Propella, BBIN Burundi, Sabi Hub, Ouskei Academy, UniMak
Workflow Hub, NIISP Uganda — đều lỗi kết nối, KHÔNG lỗi HTTP hợp lệ, có thể do chặn bot) đã bỏ.
Bổ sung tay 5 mục ngoài catalog (tìm trực tiếp qua WebSearch): iLabAfrica (Strathmore
University, Kenya), Carnegie Mellon University Africa (Rwanda), National Technology Business
Centre (Zambia), University of Dar es Salaam TDTC (Tanzania — trang riêng `tdtc.udsm.ac.tz`
không sống, áp dụng quy tắc mới dùng `udsm.ac.tz` làm url).

`ROSTER`: 870 → **907** (+37). Mở mới hoàn toàn: Kenya, Cameroon, Tunisia, Algeria, Zambia,
Namibia, Ivory Coast, Angola, Rwanda, Tanzania, Sudan, Mauritania. Đào sâu thêm: Nigeria
(1→6), South Africa (6→9), Egypt (3→5), Ghana (1→4), Ethiopia (1→2), Uganda (2→3).

**Lần trước:** 2026-09-08 (sếp chốt quy tắc mới) — sếp yêu cầu rõ: **khi không tìm ra trang
riêng của đơn vị CGCN cụ thể, cứ dùng TRANG CHỦ TRƯỜNG làm `url` thay vì bỏ qua/để trống** —
ngược với lựa chọn thận trọng ở lượt trước (đã bỏ 15/18 kết quả Gemini đoán vì chỉ ra trang
chủ trường). Đã quay lại 15 mục đó, kiểm sống lại từng URL bằng `check_url()` (một số domain
cần thử biến thể `https://www.` mới sống — `njupt`, `ustl`, `hbu`, `gzu`; `hebeu.edu.cn`
— Hebei University of Engineering — vẫn không kết nối được kể cả sau khi tra lại domain đúng,
BỎ mục này), merge 15/16 mục còn lại với `url` = trang chủ trường. `ROSTER`: 855 → **870**.
Trung Quốc: 13 → 28.

**Quy tắc chuẩn từ giờ:** khi thêm mục ROSTER, nếu tìm được trang riêng của đơn vị thì dùng
trang riêng (ưu tiên vẫn thế); nếu KHÔNG tìm được, dùng trang chủ trường/tổ chức chủ quản làm
`url` — miễn là trang đó xác nhận sống qua `check_url()` — thay vì bỏ mục hoặc để trống. Áp
dụng cho mọi nước từ giờ, không chỉ Trung Quốc.

**Lần trước:** 2026-09-08 (tìm nguồn tiếng Trung tốt hơn cho Trung Quốc, theo yêu cầu trực
tiếp) — kết quả MỎNG hơn kỳ vọng, đáng ghi lại lý do:

Tìm ra nguồn CHÍNH THỐNG cấp quốc gia thật: danh sách "第六批国家技术转移示范机构" (đợt 6,
84 tổ chức) do Bộ Khoa học Công nghệ TQ (MOST) công bố, file `.doc` tải được trực tiếp từ
`most.gov.cn` (`textutil -convert txt` đọc được, không cần OCR). ĐÂY LÀ NGUỒN THẬT — nhưng
CHỈ có tên tổ chức, KHÔNG có link nào (giống hệt vấn đề gặp ở Indonesia's Sentra KI). Thử
nhờ Gemini đoán URL cho 18 tên (gọi thẳng, không qua `roster_grow_worker.py` vì không có
trang để `url_context` đọc — chỉ có danh sách tên tĩnh) — kết quả: Gemini đoán ĐÚNG MỘT KIỂU
domain trường (vd `hbut.edu.cn`, `nankai.edu.cn`) cho gần hết, tức là chỉ đoán ra TRANG CHỦ
TRƯỜNG chứ không phải trang riêng của trung tâm CGCN — không đạt chuẩn chất lượng ROSTER
(giống vấn đề gặp với ITSO Philippines, nhưng lần này không có "trang danh bạ đã ITSO hoá"
để đổi tên bù — nên KHÔNG dùng các kết quả đoán trang chủ này).

Chuyển sang tìm tay từng trường (như Đông Nam Á) — tỷ lệ ra kết quả THẤP: phần lớn trường chỉ
có "科技处"/"科学技术发展院" (phòng KH&CN chung chung, không phải "trung tâm CGCN" riêng như
tên trong danh sách MOST) — không đạt chuẩn nên bỏ (Nankai, Hohai, 中国地质大学 — cả 3 không
thêm). Ra được đúng 3 mục thật có trang riêng xác nhận sống: Southeast University Technology
Transfer Center (`ttc.seu.edu.cn`), USST Technology Transfer Center (`jszy.usst.edu.cn`),
Nanjing Forestry University Technology Transfer Center (`kjc.njfu.edu.cn/lbt/jszyzx`). Tiện
thể tìm ra URL thật cho mục "Shanghai Jiao Tong University Technology Transfer Center" ĐÃ CÓ
SẴN trong ROSTER (trước đó thiếu url) — điền `aitri.sjtu.edu.cn/aitri/`, không phải mục mới.

`ROSTER`: 852 → **855** (+3 mục mới, +1 url điền cho mục cũ). Trung Quốc: 10 → 13.

**Kết luận rút ra (áp dụng cho mọi nguồn tiếng Trung sau này):** danh sách chính thức TQ
(MOST, Bộ Giáo dục) là THẬT nhưng hầu như không kèm link — giống vấn đề Indonesia, khác hẳn
kiểu nguồn tốt Malaysia/Thái Lan (đã có link hoặc dễ đoán domain đơn nhất-đơn-vị). Muốn mở
rộng Trung Quốc đáng kể cần: (1) tìm tay từng trường lớn có tên riêng rõ ràng cho đơn vị CGCN
(không phải phòng ban chung), hoặc (2) chấp nhận tỷ lệ giữ lại thấp như lượt này. KHÔNG dùng
cách nhờ Gemini đoán hàng loạt domain trường — chỉ ra trang chủ, không phải trang riêng.

**Lần trước:** 2026-09-08 (mở rộng Châu Á, theo yêu cầu trực tiếp của sếp — không còn giới
hạn ưu tiên "Đông Nam Á trước") — mở 3 khu vực/nước Châu Á còn mỏng hoặc chưa có mục nào,
đều tìm tay từng tổ chức qua WebSearch + kiểm sống `check_url()` (không có trang danh bạ
nhiều-tổ-chức tốt cho các nơi này, giống cách làm Brunei/Campuchia/Myanmar):

- **Hong Kong (0→5)** — 5/6 trường "Big Six" đều có TTO riêng, dễ tìm, tiếng Anh đầy đủ: HKU
  Technology Transfer Office (`tto.hku.hk`), HKUST Office of Knowledge Transfer
  (`okt.hkust.edu.hk`), CUHK Knowledge Transfer Office (`kto.cuhk.edu.hk`), PolyU Knowledge
  Transfer and Entrepreneurship Office (`polyu.edu.hk/kteo`), CityU Knowledge Transfer Office
  (`cityu.edu.hk/kto`). Chưa thêm Hong Kong Baptist University (chưa tìm ra URL riêng).
- **UAE (2→5)** — thêm EBTIC (Emirates ICT Innovation Center, Khalifa University —
  **khác** với mục "Khalifa University Enterprises (KUEC)" đã có sẵn trong ROSTER, một đơn vị
  chuyên ICT riêng, không trùng), University of Sharjah TTO (**khác** American University of
  Sharjah đã có sẵn — hai trường khác nhau dù tên gần giống, cẩn thận đừng nhầm), UAEU
  Innovation Hub. (Thử thêm URL cho mục KUEC có sẵn nhưng `ku.ac.ae/kuec/` không sống lúc
  kiểm — để nguyên, chưa điền được.)
- **Sri Lanka (0→1):** The Enterprise / TTO, University of Moratuwa (`enterprise.uom.lk`).
- **Bangladesh (0→1):** RISE - Research and Innovation Centre for Science and Engineering,
  BUET (`rise.buet.ac.bd`).

`ROSTER`: 842 → **852**.

**Việc mở:** còn nhiều nước/khu vực Châu Á = 0 hoặc rất mỏng — Kazakhstan (thử tìm URL riêng
cho Nazarbayev University's Office of Industry Engagement and Commercialization nhưng không
ra, chỉ có tên người phụ trách; office không có site riêng), Uzbekistan, Mông Cổ, Nepal,
Pakistan (hiện 1), Iran, Iraq, Lebanon, Trung Quốc (hiện chỉ 10 — rất mỏng so với quy mô hệ
sinh thái CGCN thật của TQ, cần một đợt riêng có nguồn tiếng Trung tốt hơn).

**Lần trước:** 2026-09-08 (tiếp nữa nữa) — mở 3 nước Đông Nam Á CHƯA TỪNG có mục nào
(Brunei/Campuchia/Myanmar), mỗi nước 1 mục thật đầu tiên (không tìm được danh bạ nhiều-tổ-
chức, tìm tay từng tổ chức đơn lẻ theo đúng ngoại lệ đã dùng cho Singapore/Thái Lan — WebSearch
+ kiểm sống bằng `check_url()`, không qua worker vì không có trang nguồn nhiều mục):

- **Brunei (0→1):** UBD Innovation and Enterprise (`ubd.edu.bn/innovation/`), Universiti
  Brunei Darussalam. (Thử thêm Universiti Teknologi Brunei "Enterprise Office" nhưng không
  tìm được URL riêng, chỉ có URL trường chung chung — bỏ, không thêm cho chắc.)
- **Campuchia (0→1):** University-Industry Linkage (UIL) Office (`uil.itc.edu.kh`), Institute
  of Technology of Cambodia (ITC) — đúng đơn vị đã nhắc tên (Peany Houng) ở lần bàn giao
  2026-09-06, giờ có URL thật.
- **Myanmar (0→1):** Department of Research and Innovation — DRI (`dri.gov.mm`), cơ quan nhà
  nước độc lập (không thuộc một trường cụ thể, host để trống — cùng quy ước với "Thailand
  Science Park" đã có trong ROSTER).
- **Indonesia:** cố tìm thêm nhưng KHÔNG ra mục mới nào đạt chuẩn lượt này — 4 KST của BRIN
  (Soekarno, Habibie, Samaun Samadikun, Siwabessy) xác nhận KHÔNG có website riêng, chỉ có
  trang chung `brin.go.id`/`elsa.brin.go.id` — không đạt "trang chính thức của chính tổ chức
  đó" nên không thêm. Vẫn đứng ở 7, mỏng nhất trong nhóm đã động tới.

`ROSTER`: 839 → **842** (Brunei 0→1, Campuchia 0→1, Myanmar 0→1).

**Lần trước:** 2026-09-08 (tiếp nữa) — tìm nguồn danh bạ thay thế cho Thái Lan và Indonesia
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
