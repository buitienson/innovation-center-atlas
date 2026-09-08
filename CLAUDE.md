# Innovation Center Atlas

Trang web tham khảo cá nhân (không phải văn bản HaUI/Bộ) — 6 tab: bản đồ toàn cầu (quả cầu
3D + lược đồ khu vực) các trung tâm nghiên cứu/CGCN/ĐMST của đại học trên thế giới, mạng
lưới ĐMST Việt Nam (HANISA, VNEI, các quỹ), xếp hạng ĐMST đại học, Tin tức ĐMST hằng ngày,
Fund/Hackathon (nguồn tài trợ/cuộc thi/đề xuất nhiệm vụ KHCN&ĐMST đang mở), và Thuật ngữ
(glossary ĐMST/khởi nghiệp/chính sách, có liên kết chéo giữa các mục). Tin tức + Fund/
Hackathon do routine tự động hằng ngày cập nhật (xem `_claude/routine-tin-tuc.md`); danh
mục mở rộng (`ROSTER`, 1936 mục ở tab Toàn cầu — đếm lại bằng script, đừng chép số cũ) có hạ
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
**Lần cuối:** 2026-09-08 (checkpoint 16 — **KHAI THÁC XONG africatechschools.com, SÁT MỐC
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
