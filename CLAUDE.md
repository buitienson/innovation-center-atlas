# Innovation Center Atlas

Trang web tham khảo cá nhân (không phải văn bản HaUI/Bộ) — 6 tab: bản đồ toàn cầu (quả cầu
3D + lược đồ khu vực) các trung tâm nghiên cứu/CGCN/ĐMST của đại học trên thế giới, mạng
lưới ĐMST Việt Nam (HANISA, VNEI, các quỹ), xếp hạng ĐMST đại học, Tin tức ĐMST hằng ngày,
Fund/Hackathon (nguồn tài trợ/cuộc thi/đề xuất nhiệm vụ KHCN&ĐMST đang mở), và Thuật ngữ
(glossary ĐMST/khởi nghiệp/chính sách, có liên kết chéo giữa các mục). Tin tức + Fund/
Hackathon do routine tự động hằng ngày cập nhật (xem `_claude/routine-tin-tuc.md`); danh
mục mở rộng (`ROSTER`, 19848 mục ở tab Toàn cầu — đếm lại bằng script, đừng chép số cũ; mục tiêu
hiện tại **25000**, sếp nâng từ 15000 ở checkpoint 37) có hạ
tầng mở rộng bằng Gemini `url_context` đã chạy tay thành công nhiều lượt (xem
`_claude/routine-roster-grow.md`), **chưa lên cloud routine tự động**; các mục còn lại Sơn
tự sửa tay khi cần.

**Live:** https://buitienson.github.io/innovation-center-atlas/
**Artifact (bản xem/sửa nhanh):** https://claude.ai/code/artifact/175ea757-eca9-4a87-acc8-47981ab5b129
**GitHub:** https://github.com/buitienson/innovation-center-atlas

## Hiệu năng trang — thủ phạm THẬT là bảng danh sách ROSTER, không phải quả cầu 3D

**Bài học quan trọng nhất** (commit `bc8d9ba`, 2026-09-10): sau khi vá quả cầu 3D xuống còn
16 draw call (xem mục dưới), sếp vẫn báo giật — hoá ra nguyên nhân chính không nằm ở quả cầu
mà ở **bảng tìm kiếm ROSTER** (`renderRosterTable()`): khi mở trang, KHÔNG có bộ lọc nào áp
dụng, hàm này dựng nguyên **19848 dòng `<tr>`** (~80000 node DOM) vào `#rosterBody` ngay lúc
tải trang, khiến tổng trang có **155290 node DOM** — gây giật khi mở trang, khi gõ tìm kiếm
(dựng lại toàn bộ bảng mỗi phím gõ, không debounce), và khi cuộn qua bảng khổng lồ đó. Đã sửa:
giới hạn số dòng THỰC SỰ dựng vào DOM ở 300 (`ROSTER_TABLE_MAX`), kèm ghi chú khi bị cắt bớt —
tìm kiếm/lọc vẫn khớp trên TOÀN BỘ ROSTER trong bộ nhớ, chỉ phần vẽ ra DOM bị giới hạn. Đã đo
trực tiếp: tổng DOM node giảm từ 155290 xuống 38002.

**Bài học tổng quát cho lần sau khi ROSTER tiếp tục tăng (hướng 25000+):** khi có báo cáo
"giật/lag" mà đã sửa xong 1 chỗ (vd quả cầu 3D) nhưng vẫn còn — ĐỪNG giả định chỗ vừa sửa
chưa đủ và đào sâu thêm chỉ ở đó; kiểm tra CẢ TRANG bằng `document.querySelectorAll('*').length`
xem tổng DOM node có bất thường không, vì bất kỳ danh sách/bảng nào dựng trực tiếp từ `ROSTER`
mà không giới hạn số dòng (kiểu `rows.map(...).join('')`) đều sẽ tái diễn đúng lỗi này khi
ROSTER đủ lớn — nên rà toàn bộ chỗ nào có `ROSTER.map`/`ROSTER.forEach` sinh HTML trực tiếp,
không chỉ chỗ đã biết.

**CẬP NHẬT (commit `6dc68d1`):** sau khi vá bảng ROSTER ở
trên, sếp VẪN báo giật, lần này kèm phản hồi cụ thể "đốm sáng trên bản đồ 2D chồng lấn nhìn
không ra" — hoá ra 3 **bản đồ 2D Asia/SEA/Việt Nam** (`buildCoordMap()`, gọi qua
`rosterPointsInBounds(bounds)`) mỗi cái vẽ TỪNG mục ROSTER trong vùng thành 1 vòng tròn SVG:
đo được **Asia 4119 điểm (8238 circle), SEA 1250 điểm (2500 circle), VN 313 điểm (626
circle)**. Đây KHÔNG khớp mẫu tìm kiếm `ROSTER.map(...).join('')` ở trên (nó là
`ROSTER.filter().map()` trả về mảng object đưa vào hàm vẽ SVG, không sinh chuỗi HTML trực
tiếp) — bài học: khi rà "chỗ nào dùng ROSTER để render", đừng chỉ tìm theo MẪU CODE cụ thể đã
biết, phải tìm theo Ý NGHĨA (bất kỳ hàm nào lặp qua ROSTER rồi tạo ra DOM/SVG node, bất kể
cú pháp) — `grep` theo tên hàm gọi (`rosterPointsInBounds`, `rosterFiltered`, `ROSTER.filter`)
đáng tin hơn `grep` theo cú pháp `.map(...).join(...)`.

**Lỗi thật tìm được:** cả 3 bản đồ đặt `showLabel:false` cho mọi điểm ROSTER (đúng ý định:
điểm nhỏ không cần nhãn chữ) nhưng nhánh vẽ "điểm nhỏ" (`p.small`) trong `buildCoordMap()`
KHÔNG kiểm tra cờ này (nhánh vẽ "điểm lớn/case tiêu biểu" bên cạnh CÓ kiểm) — nên mỗi điểm vẫn
bị tạo thêm 1 `<text>` VÀ 1 mục trong `pointLabelItems`, mảng này bị hàm `updateMapLabels()`
quét lại **mỗi lần kéo/zoom bản đồ** với thuật toán tránh chồng nhãn gần O(n²) (so từng cặp
nhãn đã đặt) — đây mới là nguyên nhân giật KHI TƯƠNG TÁC với bản đồ 2D, không phải quả cầu.
Đã sửa: thêm đúng điều kiện `if(p.showLabel!==false)` vào nhánh điểm nhỏ (đúng như nhánh kia
đã làm) — `pointLabelItems` giờ gần như rỗng cho các bản đồ này. Đồng thời giảm bán kính điểm
nhỏ (glow 5→2.6, core 2.1→1.1) để đỡ chồng lấn khi có hàng nghìn điểm trong 1 khung SVG cố
định.

**Bài học tổng quát MỚI (quan trọng hơn bài học cũ ở trên):** khi 1 tính năng có "cờ tắt"
(`showLabel:false`, tương tự `visible:false`...) được set nhất quán ở NƠI TẠO DỮ LIỆU nhưng
lại có 2 nhánh code xử lý khác nhau cho cùng loại dữ liệu (ở đây: nhánh "case lớn" và nhánh
"điểm nhỏ") — luôn nghi ngờ 1 trong 2 nhánh QUÊN kiểm tra cờ đó, đặc biệt nếu nhánh đó được
viết sau hoặc thêm dữ liệu (ROSTER) vào sau khi code đã có sẵn cho mục đích khác (case tiêu
biểu). Bug bất đối xứng kiểu này (2 nhánh giống nhau nhưng chỉ 1 nhánh đúng) dễ lọt qua vì mỗi
nhánh nhìn "hợp lý" khi đọc riêng lẻ.

**CẬP NHẬT 2 (commit `0903164`):** sau khi vá bug `showLabel` ở trên, sếp vẫn thấy nặng và yêu
cầu thẳng "tắt hiệu ứng, giảm độ lớn điểm sáng cho đỡ nặng" — mỗi điểm ROSTER nhỏ trên bản đồ
2D trước đó vẽ 2 circle (glow halo + core) và circle core chạy animation CSS `infinite` vĩnh
viễn — với hàng nghìn điểm/bản đồ, đó là hàng nghìn animation SVG chạy đồng thời liên tục,
tốn chi phí style/paint riêng, KHÁC với bug O(n²) label đã vá (2 vấn đề cộng dồn, không phải 1).
Đã sửa: mỗi điểm ROSTER giờ chỉ còn 1 circle tĩnh (r=0.9), không animation — chỉ các điểm case
tiêu biểu (vài chục, không phải hàng nghìn) còn giữ hiệu ứng glow+nhấp nháy. Đo được: circle
Asia giảm từ 8238 xuống 4121, tổng DOM node 32335→26668.

**CẬP NHẬT 3 (commit `5871a83`):** sếp phản hồi "3D mượt rồi, 2D vẫn là gốc giật" — tức 2 lượt
vá trên (label O(n²) + bỏ animation) làm nhẹ đi nhưng chưa hết. Tìm tiếp: `attachPanZoom()`
(dùng chung cho cả 3 bản đồ) áp dụng kéo/zoom bằng cách set THUỘC TÍNH SVG `transform` (không
phải CSS `transform`) trên nhóm nội dung — với hàng nghìn `<circle>` con còn lại (Asia ~4100,
SEA ~1250, VN ~310) dù đã tĩnh không animation, set thuộc tính SVG mỗi khung hình kéo/zoom vẫn
khiến trình duyệt có xu hướng vẽ lại (repaint) toàn bộ hình học bên trong thay vì chỉ dịch
chuyển 1 layer đã dựng sẵn qua compositor — đây là khoảng cách tăng tốc GPU nổi tiếng giữa
thuộc tính SVG và CSS transform. Đã sửa: đổi `apply()` sang set `content.style.transform`
(CSS) thay vì `setAttribute('transform', ...)`, thêm `transform-box:view-box;
transform-origin:0 0` cho `.map-content` để CSS transform dùng đúng cùng hệ toạ độ (gốc ở góc
trên-trái viewBox) như thuộc tính cũ — chỉ đổi CÁCH VẼ, không đổi vị trí hiển thị. Đã kiểm
chứng: kéo chuột 50px di chuyển đúng 1 điểm mẫu (100px, 40px) trên màn hình (đúng tỷ lệ
viewBox/màn hình của bản đồ này), zoom bằng lăn chuột vẫn ra scale/translate đúng tâm.

**Việc mở nếu vẫn còn báo giật sau CẬP NHẬT 3:** sếp từng báo "Use hardware acceleration"
trong Chrome đang TẮT (ảnh chụp mục Settings→System) rồi tự bật lên nhưng CHƯA xác nhận đã
khởi động lại trình duyệt để áp dụng (Chrome yêu cầu restart hẳn, không chỉ bật switch) — nếu
tăng tốc phần cứng thực sự tắt từ đầu, WebGL/canvas/SVG-compositor đều phải chạy bằng renderer
phần mềm (rất chậm), có thể là 1 phần nguyên nhân độc lập với các bug code đã vá — cần hỏi lại
kết quả sau restart ở phiên sau nếu sếp chưa phản hồi.

**CẬP NHẬT 4 — commit `88b8d73` SAI, đã phải lùi lại 1 phần (commit `418a311`):** sau CẬP NHẬT 3,
sếp báo "nhẹ hơn rất nhiều", rồi xin khôi phục glow halo + nhấp nháy cho điểm ROSTER (đã bỏ ở
CẬP NHẬT 2) và tăng độ nhạy zoom. Lúc đó tôi ĐO SAI CÁCH: chỉ bọc `performance.now()` quanh việc
bắn sự kiện `mousemove` rồi đo thời gian JS chạy XONG TRONG HÀM (~2.6ms/lần) và kết luận nhầm là
"vẫn nhẹ" — nhưng phép đo đó CHỈ bắt được thời gian JS đồng bộ của handler, KHÔNG bắt được chi
phí trình duyệt phải LIÊN TỤC đánh giá lại hàng nghìn animation CSS `infinite` MỖI KHUNG HÌNH,
kể cả khi không tương tác gì (animation tự chạy nền, không phụ thuộc sự kiện chuột). Sếp báo
"lại giật lag rồi" ngay sau đó — ĐÚNG, đây là chi phí THẬT, khác hẳn và CỘNG THÊM vào bug
transform-attribute đã vá ở CẬP NHẬT 3, không phải do CẬP NHẬT 3 chưa đủ.

**Đã sửa đúng (commit `418a311`):** giữ lại 2 circle/điểm (glow halo + core, vẫn màu mè, vẫn
8238 circle cho Asia) nhưng bỏ hẳn class `core-glow`/`core-blink` (mang animation `infinite`)
khỏi nhánh điểm ROSTER — chỉ còn few "big" points (case tiêu biểu) còn nhấp nháy. Lần này đo
ĐÚNG chỗ bằng Web Animations API thật: `document.getAnimations().length` — giảm từ ước tính
8000+ xuống còn **6** cho toàn trang, đây mới là con số phản ánh đúng "có bao nhiêu animation
đang chạy liên tục", không phải thời gian 1 lần gọi handler.

**Bài học sửa lại bài học cũ ở trên (bài học cũ SAI, đừng làm theo):** đo `performance.now()`
quanh 1 lần gọi event handler CHỈ chứng minh JS ĐỒNG BỘ trong handler đó rẻ — KHÔNG chứng minh
gì về chi phí RENDER/ANIMATION LIÊN TỤC chạy độc lập với sự kiện (CSS `animation:...infinite`,
`requestAnimationFrame` loop riêng...). Muốn biết có đang "đốt" animation liên tục hay không,
dùng `document.getAnimations().length` (đếm animation đang hoạt động) hoặc đếm số phần tử có
class animation trước/sau khi đổi, ĐỪNG suy ra từ thời gian 1 lệnh gọi hàm.

**CẬP NHẬT 5 (commit `a780a58`) — cân bằng được cả hiệu năng lẫn thẩm mỹ:** sếp xác nhận mượt
hơn hẳn sau CẬP NHẬT 4 nhưng chê 2 điểm: (1) màu điểm ROSTER nhạt/"nhờ nhờ" — đang dùng bảng màu
pastel dùng chung với badge/chip nơi khác (`VN_TYPE_COLORS`...), đã đổi riêng cho các điểm này
sang đúng màu rực của quả cầu 3D (`TYPE_HEX`: `#408CFF`/`#00E0C6`/`#BE5AFF`/`#C8D2E6`); (2) nhớ
hiệu ứng nhấp nháy — sếp tự đề xuất giải pháp hay: "mỗi quốc gia 1 ông nhấp nháy là ông hoành
tráng nhất" thay vì tất cả hoặc không gì cả. Đã làm đúng vậy: `rosterPointsInBounds()` đánh dấu
`blink:true` cho ĐÚNG 1 dòng ROSTER đầu tiên gặp mỗi quốc gia (không xếp hạng gì, chỉ là dòng
đầu tiên theo thứ tự mảng), chỉ dòng đó được gắn class animation. Đo được: Asia còn 38 điểm
nhấp nháy (bằng đúng số quốc gia trong khung, không phải 4119), tổng animation toàn trang 112
(so với 8000+ gây giật ở CẬP NHẬT 4) — **đây là mức cân bằng tốt giữa "có sức sống" và "nhẹ",
nên dùng làm mẫu cho các lần thêm hiệu ứng tương tự sau này khi có nhiều điểm dữ liệu.**

**CẬP NHẬT 6 (commit `3d5a4a3`) — sót Việt Nam:** logic "1 điểm/quốc gia" ở CẬP NHẬT 5 chỉ áp
cho `rosterPointsInBounds()` — nhưng ROSTER theo quy ước KHÔNG có Việt Nam, nên Việt Nam
KHÔNG BAO GIỜ được hàm đó gán `blink`. Trên bản đồ Asia/SEA, Việt Nam hiện diện qua
`vnUnitsAsSmallPoints()` (hàm riêng, tách biệt) — chưa từng được sửa để gắn `blink` — nên Việt
Nam là quốc gia DUY NHẤT không nhấp nháy trong khi mọi nước khác đều có, dễ thấy vì Việt Nam
lại là mạng lưới được đầu tư nhiều dữ liệu nhất. Đã sửa: gắn `blink:true` cho đơn vị đầu tiên
trong mảng `VN_UNITS` khi hàm này chạy. **Bài học:** khi thêm 1 hành vi (`blink`) cho "mỗi
quốc gia/nhóm", phải rà HẾT các hàm sinh điểm cho bản đồ đó (ở đây có 3: `rosterPointsInBounds`,
`vnUnitsAsSmallPoints`, `vnNetworkAsSmallPoints`), không chỉ hàm đầu tiên nghĩ tới — nhất là khi
1 nhóm dữ liệu (Việt Nam) bị loại khỏi nguồn chính (ROSTER) vì lý do khác (quy ước phạm vi) chứ
không phải vì nó kém quan trọng hơn.

## Hiệu năng quả cầu 3D

**Fix thật sự** (commit `f52528d`, 2026-09-10): mỗi loại ROSTER (university/company/network/
other) giờ là **1 `THREE.Points` (point cloud) duy nhất** dựng từ 1 `BufferGeometry`, thay vì
mỗi điểm 1 `THREE.Sprite` riêng — ở quy mô ~20000 điểm, mỗi Sprite là 1 draw call GPU riêng dù
material có dùng chung hay không, nên đây mới là nút thắt thật (không phải số material). Đã đo
trực tiếp trong trình duyệt qua `renderer.info.render.calls`: từ ước tính ~19850+ giảm còn
**16** cho toàn cảnh. Bắt click/hover (raycasting) giờ dùng hàm dùng chung `pickHit()` — hit
vào Points chỉ trả về `index` đỉnh, phải tra ngược qua `userData.rows` của point cloud đó (mảng
song song với buffer vị trí) để lấy đúng dòng ROSTER; đã kiểm chứng qua console (`window.
__pickHit(x,y)`, x/y là NDC -1..1) trả đúng tổ chức thật. Nhấp nháy (opacity/size) giờ tính
theo LOẠI (4 lần/khung hình) vì material dùng chung cho cả point cloud — các case tiêu biểu +
điểm Việt Nam (chỉ ~10 điểm, vẫn là Sprite riêng) vẫn nhấp nháy độc lập từng điểm như cũ.

**2 việc chỉnh thêm ngay sau đó** (commit `b581877`, cùng ngày):
1. **Sếp báo hiệu ứng nhấp nháy xấu** ("sáng lốm đốm chứ không nên cùng sáng cùng tắt") — đúng
   như cảnh báo ở trên: gộp cả loại thành 1 material khiến TOÀN BỘ điểm cùng loại nhấp nháy
   ĐỒNG BỘ, nhìn như "bật/tắt" chứ không tự nhiên. Đã sửa: chia mỗi loại thành
   `ROSTER_PULSE_BUCKETS=24` nhóm nhỏ (gán vòng tròn theo thứ tự duyệt ROSTER — KHÔNG theo địa
   lý, để 2 điểm gần nhau trên bản đồ, vốn hay liền nhau trong mảng vì nhập theo batch quốc
   gia/khu vực, rơi vào 2 nhóm khác nhau, không nhấp nháy cùng lúc), mỗi nhóm 1 material + 1
   pha riêng — vẫn chỉ ~100 draw call (đo được 108), không phải hàng nghìn.
2. **Phát hiện thêm qua đo trực tiếp:** `pickHit()` (raycast vào point cloud) tốn ~1ms/lần gọi
   — trong khi sự kiện `mousemove` có thể bắn ra nhanh hơn thế nhiều khi di chuột qua quả cầu
   (kể cả KHÔNG giữ chuột để xoay), làm nghẽn main thread chỉ vì di chuột qua lại. Đã giới hạn
   `onHover` chạy tối đa 1 lần/50ms — vẫn mượt cho tooltip hover, giảm tải vài lần.

**Bài học cho lượt sau nếu vẫn có báo cáo giật:** đã có TIỀN LỆ 2 lần liên tiếp là fix tưởng đủ
nhưng chưa đủ — **luôn đo bằng số liệu thật** (`renderer.info.render.calls`, `document.
querySelectorAll('*').length`, `performance.now()` quanh hàm nghi ngờ) thay vì chỉ suy luận lý
thuyết rồi coi là xong; nếu sếp báo còn giật sau khi đã đo/sửa 1 chỗ, đó là tín hiệu rất mạnh
rằng còn ít nhất 1 nguyên nhân khác CHƯA được đo tới, không phải bản fix vừa rồi sai.

**Bản fix đầu (commit `6747431`, chỉ gộp material dùng chung theo loại) KHÔNG đủ** — sếp xác
nhận vẫn giật sau khi lên bản đó, vì gộp material chỉ giảm số lần chuyển trạng thái GPU giữa
các draw call, không giảm SỐ LƯỢNG draw call (vẫn ~20000). Bài học: khi thấy hàng chục nghìn
`THREE.Sprite`/`THREE.Mesh` riêng lẻ gây giật, luôn nghĩ tới gộp draw call (Points/InstancedMesh)
trước, đừng dừng ở việc gộp material — 2 việc khác nhau, chỉ gộp material không giải quyết
đúng gốc rễ.

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
**Lần cuối:** 2026-09-10 14:03 — routine tự động thêm tin + fund/hackathon (theo
`_claude/routine-tin-tuc.md`), không phải phiên tương tác.

**Phần A — Tin tức (3 tin, mảng `NEWS`):**
- "Đà Nẵng xây dựng hệ sinh thái khởi nghiệp đổi mới sáng tạo bền vững" (Báo Nhân Dân, 2026-09-03).
- "Concr (Cambridge Enterprise) công bố nền tảng AI 'digital twin' FarrSight dự đoán đáp ứng điều trị ung thư tuyến tụy" (Cambridge Enterprise, 2026-09-03).
- "FSID của Viện Khoa học Ấn Độ (IISc) bổ nhiệm CEO mới, đặt mục tiêu 300 startup deep-tech đến 2030" (Deccan Herald, 2026-09-09).

**Phần B — Fund/Hackathon (1 mục, mảng `FUNDING`):**
- "Khởi nghiệp sáng tạo miền Bắc 2026" — cuộc thi của HSB (ĐHQGHN) cho học sinh THPT, hạn nộp hồ sơ 2026-10-25.

Tất cả link nguồn đã xác minh còn sống (curl trả 200) trước khi thêm.
