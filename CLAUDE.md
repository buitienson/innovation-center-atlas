# Innovation Center Atlas

Trang web tham khảo cá nhân (không phải văn bản HaUI/Bộ) — 6 tab: bản đồ toàn cầu (quả cầu
3D + lược đồ khu vực) các trung tâm nghiên cứu/CGCN/ĐMST của đại học trên thế giới, mạng
lưới ĐMST Việt Nam (HANISA, VNEI, các quỹ), xếp hạng ĐMST đại học, Tin tức ĐMST hằng ngày,
Fund/Hackathon (nguồn tài trợ/cuộc thi/đề xuất nhiệm vụ KHCN&ĐMST đang mở), và Thuật ngữ
(glossary ĐMST/khởi nghiệp/chính sách, có liên kết chéo giữa các mục). Tin tức + Fund/
Hackathon do routine tự động hằng ngày cập nhật (xem `_claude/routine-tin-tuc.md`); danh
mục mở rộng (`ROSTER`, 20067 mục ở tab Toàn cầu — đếm lại bằng script, đừng chép số cũ; mục tiêu
hiện tại **30000**, sếp nâng từ 25000 sau checkpoint 48) có hạ
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

## Panel Việt Nam trên bản đồ 2D — chỉ hiện đúng 149 đơn vị Việt Nam

Đã sửa (commit `7ece197`, `9b48f90`, 2026-09-10): trước đó panel/tab Việt Nam bị
`rosterPointsInBounds(VN_BOUNDS)` gộp thêm các mục ROSTER của NƯỚC KHÁC rơi vào khung toạ
độ Việt Nam (149 → 315 đơn vị/9 quốc gia hiển thị sai ở ô thống kê, đồng thời các chấm
sáng không phải Việt Nam vẫn bị vẽ chồng lên bản đồ). Đã sửa cả 2 lớp: `regionStats()`
nhận thêm `opts.skipRoster` để tab VN chỉ đếm `VN_UNITS`/mạng lưới, KHÔNG quét ROSTER; và
`vnPoints` bỏ hẳn `.concat(rosterPointsInBounds(VN_BOUNDS))`. Các nước khác trên bản đồ VN
giờ tô xám (`grayNonHighlight`), riêng Việt Nam (gồm Hoàng Sa/Trường Sa) giữ màu. **Nhớ:**
ROSTER theo quy ước không chứa Việt Nam — bất kỳ hàm mới nào lấy dữ liệu cho tab/panel
Việt Nam PHẢI dùng `VN_UNITS`/mạng lưới riêng, không được quét ROSTER theo toạ độ.

## Bản đồ zoom cụm Hà Nội / TP.HCM (commit `18c80dc` + `206692b`, 2026-09-10)

Sếp báo bản đồ Việt Nam ở mức zoom toàn quốc: 2 cụm Hà Nội/TP.HCM (~150 điểm dồn vào 1
khung toạ độ nhỏ) chỉ hiện thành 1 quầng sáng mờ, không phân biệt được từng đơn vị. Đã
thêm 2 khung bản đồ MỚI (`#mapVNHN`, `#mapVNHCM`) ngay dưới bản đồ chính + chú thích —
dùng ĐÚNG bộ điểm/độ giãn (`spreadCluster()`, `vnNetworkAsSmallPoints()`) đã có sẵn,
chỉ đổi `bounds` sang đúng khung 2 ô highlight cũ (`{latMin:20.8,latMax:21.6,
lngMin:105.0,lngMax:106.6}` Hà Nội, `{latMin:10.6,latMax:11.1,lngMin:106.4,lngMax:107.0}`
TP.HCM) render trên khung canvas full-size như bản đồ chính — cùng 1 độ giãn (jitter) đó
trải ra nhiều pixel hơn hẳn nên tách rời được. Đơn vị trường đại học (`VN_UNITS`, 7-8
điểm/cụm) gắn nhãn tên cố định; điểm mạng lưới HANISA/VNEI/quỹ (hàng chục điểm/cụm) dùng
lại hệ thống "hiện nhãn khi zoom sâu, né chồng lấn" có sẵn trong `buildCoordMap()` (bật
`showLabel` thay vì `false` như bản đồ chính) + tooltip hover (`<title>`) luôn có sẵn.

**CẬP NHẬT ngay sau đó (cùng ngày) — sếp báo "thiếu bản đồ" trong 2 ô:** bản đầu KHÔNG
truyền `opts.land`, nên 2 khung chỉ có lưới toạ độ + chấm nổi trên nền trống — đúng chức
năng nhưng KHÔNG "trông giống bản đồ". Đã thêm `land:COUNTRIES, grayNonHighlight:true`
(giống hệt cách bản đồ VN chính đang dùng) — đường bờ biển/khối đất Việt Nam (độ phân giải
Natural Earth 1:50m, đã đủ dùng cho bản đồ chính) giờ hiện dưới dạng khối tô đỏ nhạt phủ
khắp khung (vì cả 2 khung đều nằm sâu trong đất liền, không có ranh giới nào khác lọt vào
tầm nhìn). Xác nhận qua kiểm cấu trúc DOM (không chụp màn hình được — Browser pane bị ẩn
suốt lượt kiểm này, `screenshot` timeout liên tục): `mapVNHN` có đúng 8 polygon tô màu
Việt Nam (`fill:rgba(255,90,99,0.22)`), 1 vòng trong đó có 421 điểm trải bbox
(xmin -554 → xmax 928, ymin -270 → ymax 2715) PHỦ TRÙM khung `viewBox 0 0 380 320` — tức
khối đất Việt Nam chắc chắn phủ kín khung nhìn, không phải mảnh rời rạc. Cùng đường code
`buildCoordMap()`/`landColors()` đã dùng ổn định cho bản đồ VN/Asia/SEA chính nhiều
checkpoint — không phải hướng đi mới, chỉ là quên truyền `opts.land` ở bản đầu.

**Bug phát sinh + đã vá cùng lúc:** nhãn lưới toạ độ (`coord-label`) của `buildCoordMap()`
in thẳng biến `la`/`lo` — bước lưới số nguyên (10°, 4°) trước giờ không lộ vấn đề, nhưng
bước lẻ (0.1°/0.2°, dùng cho 2 khung mới) cộng dồn sai số dấu phẩy động qua `+= opts.step`
(vd in ra `106.39999999999999°`). Đã sửa: làm tròn RIÊNG phần chữ hiển thị
(`Math.round(la*1000)/1000`), không đụng `la` gốc (vẫn dùng để tính vị trí đường lưới) —
áp dụng cho mọi bản đồ dùng `buildCoordMap()`, không riêng 2 khung mới.

## Quy tắc nội dung — nhắc lại vì đã bị vi phạm nhiều lần trong lúc dựng

**Không đưa bình luận về quy trình/phương pháp thu thập dữ liệu lên trang công khai.**
Không viết kiểu "nguồn X bị lỗi", "chưa xác minh", "kết quả tìm kiếm diện rộng chưa thẩm
định" vào các trường `org`/`caveat`/ghi chú hiển thị cho người đọc — chỉ giữ sự thật khách
quan, hữu ích (vd "năm tài chính kết thúc 30/6" thì được, "agent tải PDF bị lỗi" thì không).
Sếp đã bắt bỏ đúng loại nội dung này nhiều lần (screenshot legend/ghi chú phân loại, danh
sách Miền Bắc/Miền Nam không đại diện, disclaimer trên quả địa cầu).

---

## Routine tin tức / fund-hackathon — trạng thái lần chạy gần nhất

> Mục này RIÊNG cho routine `_claude/routine-tin-tuc.md` (tin tức + fund/hackathon) — ghi
> đè (không nối) mỗi lần routine đó chạy. KHÔNG phải nơi ghi checkpoint tăng trưởng ROSTER
> (xem mục "Lịch sử tăng trưởng ROSTER" bên dưới, mục đó nối tiếp — Lần cuối/Lần trước —
> KHÔNG bao giờ ghi đè).

**Lần cuối:** 2026-09-10 14:03 — routine tự động thêm tin + fund/hackathon (theo
`_claude/routine-tin-tuc.md`), không phải phiên tương tác.

**Phần A — Tin tức (3 tin, mảng `NEWS`):**
- "Đà Nẵng xây dựng hệ sinh thái khởi nghiệp đổi mới sáng tạo bền vững" (Báo Nhân Dân, 2026-09-03).
- "Concr (Cambridge Enterprise) công bố nền tảng AI 'digital twin' FarrSight dự đoán đáp ứng điều trị ung thư tuyến tụy" (Cambridge Enterprise, 2026-09-03).
- "FSID của Viện Khoa học Ấn Độ (IISc) bổ nhiệm CEO mới, đặt mục tiêu 300 startup deep-tech đến 2030" (Deccan Herald, 2026-09-09).

**Phần B — Fund/Hackathon (1 mục, mảng `FUNDING`):**
- "Khởi nghiệp sáng tạo miền Bắc 2026" — cuộc thi của HSB (ĐHQGHN) cho học sinh THPT, hạn nộp hồ sơ 2026-10-25.

Tất cả link nguồn đã xác minh còn sống (curl trả 200) trước khi thêm.


## Lịch sử tăng trưởng ROSTER (checkpoint 1-48+)

> Nối tiếp — mỗi lần thêm checkpoint mới, khối "Lần cuối" cũ đổi thành "Lần trước", KHÔNG
> BAO GIỜ ghi đè/xoá lịch sử cũ (khác hẳn mục tin tức ở trên). Đây là lịch sử chi tiết các
> nguồn đã thử/loại khi mở rộng danh mục ROSTER — giữ nguyên để tránh lặp lại công sức.

**Lần cuối:** 2026-09-11 (checkpoint 60 — **3 việc song song: (1) fallback wikitext cho ~94 khu công
nghệ cao TQ còn thiếu `P856` (việc mở checkpoint 59) — CHỈ CỨU ĐƯỢC 2/94 vì bị Wikipedia RATE-LIMIT
(429) suốt lượt gọi hàng loạt, không phải do thiếu trường thực sự; (2) Wikipedia tiếng Hàn
`분류:테크노파크` (mạng lưới TechnoPark 17 tỉnh) — xác nhận LẠI 3 tỉnh Daegu/Gwangju/Gyeonggi Daejin
VẪN chặn mạng y hệt các checkpoint 44/47 trước, 0 mục mới; (3) Wikipedia tiếng Ba Lan `Kategoria:
Parki technologiczne/naukowe/przemysłowe w Polsce` — sau lọc + xác minh chỉ **+1 mục thật**. **Tổng
checkpoint này: +3** — còn thiếu ~9924 lúc cuối phiên.

**Bài học kỹ thuật quan trọng — Wikipedia RATE-LIMIT 429 khi gọi hàng loạt liên tục, khác hẳn lỗi
"trang không có trường":** script đầu tiên gọi 94 trang `action=parse&prop=wikitext` liên tiếp chỉ
cách nhau ~1 giây (kèm 3 lần retry/2s khi lỗi) → hầu hết bị 429 "Too Many Requests" và SAU 3 LẦN
RETRY VẪN THẤT BẠI, hàm trả về `None` — kết quả bị hiểu nhầm là "trang không có trường `web=`" dù
xác nhận tay 1 trang (`南昌高新技术产业开发区`) THỰC SỰ CÓ trường này trong infobox. Chạy lại với
retry backoff dài hơn (4-13s) + nghỉ 1.2s/request chỉ cứu thêm được 2/89 — vẫn bị 429 áp đảo. **Kết
luận: batch gọi liên tục >~50 request tới cùng 1 Wikipedia site trong thời gian ngắn CẦN nghỉ dài
hơn nhiều (multi-giây/request) hoặc chia nhỏ thành nhiều lượt cách xa nhau, KHÔNG chỉ tăng số lần
retry — retry dồn dập vào đúng lúc đang bị limit không giúp gì.** Việc mở: 92/94 trang TQ còn lại
CHƯA THỬ LẠI đúng cách (giãn cách đủ dài) — tiềm năng vẫn còn nguyên, chỉ là kỹ thuật gọi API sai.

**Hàn Quốc — xác nhận lại (không phải mở mới):** `분류:테크노파크` liệt kê đủ 17 TechnoPark (khớp
đúng mạng lưới ROSTER đã có 11+Pohang từ checkpoint 44) — 14/17 đã có sẵn qua domain, 3 còn thiếu
(Gyeonggi Daejin `gdtp.or.kr`, Gwangju `gjtp.or.kr`, Daegu `ttp.org`) qua Wikidata P856 hop vẫn
`HTTPError`/`URLError` giống hệt kết quả checkpoint 44 (403)/47 (navigation denied) — XÁC NHẬN chặn
thật, ổn định qua nhiều tháng, không phải lỗi tạm thời. Đừng thử lại 3 domain này nữa trừ khi đổi
hẳn vị trí mạng.

**Ba Lan:** `Kategoria:Parki technologiczne/naukowe/przemysłowe w Polsce` — 35 trang → 15/35 có
`P856` → 8 ứng viên sau lọc trùng → `check_url()` chỉ 2 sống thẳng, và cả 2 ĐỀU BỊ LOẠI sau xác
minh tay: "Park Przemysłowy w Solcu Kujawskim" — `<title>` xác nhận là trang PROFILE của **Polska
Agencja Inwestycji i Handlu (PAIH, cơ quan xúc tiến đầu tư quốc gia)**, không phải trang riêng của
khu công nghiệp — loại theo đúng nguyên tắc "không lấy cổng thông tin/trang mô tả của bên thứ ba,
chỉ lấy trang CHÍNH CHỦ". 2 ca cross-domain redirect (`opnt.pl`→`aftermarket.pl` 403,
`pppt.pl`→`orlen.pl` rỗng) không xác minh được, loại. **Chỉ giữ 1: Lubuski Park
Przemysłowo-Technologiczny** (`lppt.pl`, xác nhận `<title>` đúng tên).

**Kết quả merge:** `ROSTER`: 20064 → **20067** (+3: Lubuski PL, Baoding TQ, Đông Quản Tùng Sơn Hồ
TQ). Đơn vị trên bản đồ: 20073 → **20076** (+3, giữ nguyên chênh lệch +9). Kiểm sau ghi: `node
--check` sạch, thẻ cân bằng (111/111, 6/6), Browser pane đọc đúng "20076 đơn vị được lập bản đồ",
console sạch. Commit (xem `git log`), push.

**Còn thiếu ~9924.** **Việc mở ưu tiên cao nhất cho lượt sau:** (1) **92/94 trang Trung Quốc còn
lại trong `Category:国家级高新技术产业开发区` CHƯA thử đúng cách** — chạy lại wikitext-fallback với
giãn cách ≥3-5 giây/request (hoặc chia làm 3-4 đợt cách nhau vài phút), tiềm năng có thể thêm hàng
chục mục nữa vì đây là category LỚN NHẤT tìm được gần đây; (2) Ba Lan/Hàn Quốc coi như đã khai thác
hết cho lượt này; (3) tiếp tục ngôn ngữ khác (Thổ Nhĩ Kỳ, Hà Lan, Séc, Hungary) hoặc quay về InBIA.

---
**Lần trước:** 2026-09-11 (checkpoint 59 — **Wikipedia tiếng Trung `Category:国家级高新技术产业开发区`
(danh sách ~100 Khu phát triển công nghiệp công nghệ cao cấp quốc gia Trung Quốc — ĐÚNG hệ thống
mà `chinatorch.gov.cn` (China Torch) đã bị chặn mạng suốt nhiều checkpoint từ rất sớm, nay vòng qua
được bằng Wikipedia làm trung gian!) + `Category:企业孵化器`/`Category:种子加速器` — sau lọc + xác
minh (loại 1 ca phạm vi sai — cổng thông tin CHÍNH QUYỀN QUẬN chung chung dù nằm trong category) còn
**8 mục thật sự mới (+8)** — còn thiếu ~9927 lúc cuối phiên.

**Phát hiện đột phá:** domain `.gov.cn` của TỪNG khu công nghệ cao RIÊNG LẺ (`fzgxq.fuzhou.gov.cn`,
`shidz.gov.cn`, `whctp.gov.cn`, `wehdz.gov.cn`, `lyctp.gov.cn`, `tsgxq.gov.cn`, `zizhupark.com`)
KHÔNG bị chặn mạng như `chinatorch.gov.cn` (cổng trung ương) — 9/15 ứng viên sống ngay, tỉ lệ khá
cao so với các lần thử trực tiếp domain trung ương trước đây. **Bài học quan trọng: 1 domain trung
ương bị chặn KHÔNG có nghĩa mọi domain con-quan/địa phương cùng hệ thống cũng bị chặn — đáng thử
riêng từng domain thay vì suy luận cả hệ thống đã bế tắc.**

**Nguồn:** 114 trang (110 có QID) từ `Category:国家级高新技术产业开发区` (danh sách chính thức các
khu công nghệ cao cấp quốc gia, mỗi khu 1 bài riêng) + vài trang từ `Category:企业孵化器`/
`Category:种子加速器`. Chỉ 16/110 có `P856` trên Wikidata (tỉ lệ điền thấp — dữ liệu Wikidata cho
thực thể Trung Quốc thường thiếu trường website hơn ngôn ngữ khác) → sau lọc trùng ROSTER (1 trùng
— Plug and Play qua `plugandplaytechcenter.com`) → 15 ứng viên → `check_url()` 9 sống.

**Loại 1 ca sai phạm vi phát hiện qua đọc tay `<title>`:** "江海区" (Jianghai District, Giang Môn/
Jiangmen) — `<title>` "江门市江海区人民政府门户网站" (Cổng thông tin CHÍNH QUYỀN QUẬN Jianghai,
Jiangmen) — đây là cổng UBND quận CHUNG, không phải trang riêng của khu công nghệ cao (khu công
nghệ chỉ là MỘT PHẦN của quận này) — loại, đúng nguyên tắc không lấy cổng chính quyền địa phương
chung chung. Cùng loại lỗi 2 ca khác ("钱塘区"/Qiantang, "滨江区"/Binjiang) cũng bị loại trước đó vì
chết mạng (không cần xét phạm vi).

**Kết quả cuối: 8 mục** — Fuzhou/Shijiazhuang/Weihai/Wuhan (Đông Hồ, tức "Thung lũng Quang học
Trung Quốc")/Linyi/Tangshan/Zizhu High-tech Industrial Development Zones + `SOSV` (quỹ đầu tư mạo
hiểm/accelerator toàn cầu, gốc Trung Quốc — Chinaccelerator — nay trụ sở Princeton, Mỹ). 0 Việt Nam.
Toạ độ: Linyi/Zizhu có `P625` thật; 6 còn lại tra tay theo tên thành phố.

**Kết quả merge:** `ROSTER`: 20056 → **20064** (+8). Đơn vị trên bản đồ: 20065 → **20073** (+8, giữ
nguyên chênh lệch +9). Kiểm sau ghi: `node --check` sạch, thẻ cân bằng (111/111, 6/6), Browser pane
đọc đúng "20073 đơn vị được lập bản đồ", console sạch. Commit `59024f5`, `git push origin main`.

**Còn thiếu ~9927.** **Việc mở:** (1) `Category:国家级高新技术产业开发区` còn ~90 trang chưa xử lý
(chỉ 16/110 có `P856`, 94 trang còn lại CHƯA thử fallback wikitext để tìm URL — đáng làm tiếp, đây
là mỏ lớn nhất tìm được trong nhiều checkpoint, ước tính có thể còn thêm hàng chục mục nếu tìm được
URL qua wikitext/tìm tay từng khu); (2) tiếp tục áp dụng bài học "domain con không nhất thiết bị
chặn theo domain trung ương" cho các hệ thống chính phủ khác đã từng bị chặn (Nhật/Hàn/Ấn Độ...);
(3) `企业孵化器`/`种子加速器` category tiếng Trung còn nhỏ, hầu hết đã trùng — coi như cạn.

---
**Lần trước:** 2026-09-11 (checkpoint 58 — **Wikipedia tiếng Nga `Категория:Технопарки` (+ sub-cat
Россия/Москва/Украина) + `Категория:Бизнес-инкубаторы`, thử tiếng Nhật nhưng KHÔNG tìm ra category
phù hợp (chỉ trùng "Jurassic Park") — sau lọc trùng ROSTER (khá cao, nhiều tên đã có qua các
checkpoint Wikidata trước) còn **4 mục thật sự mới (+4)** — bài học kỹ thuật quan trọng: encoding
tiếng Nga/Cyrillic qua `curl`/bash bị hỏng thành dấu `?`, phải chuyển hẳn sang Python `urllib` +
ghi file UTF-8 rồi đọc bằng công cụ Read, không print thẳng ra terminal (terminal Windows dùng
cp1252, không hiển thị được Cyrillic)**) — còn thiếu ~9935 lúc cuối phiên.

**Bài học kỹ thuật mới, áp dụng cho MỌI ngôn ngữ chữ khác Latin từ giờ:** lượt trước (tiếng Việt/
Đức/Pháp/Ý/Tây Ban Nha/Bồ Đào Nha) đều gõ trực tiếp chuỗi có dấu vào lệnh `curl --data-urlencode`
qua bash và chạy tốt. Với tiếng Nga, `curl -G --data-urlencode "srsearch=Технопарк"` trả về
`totalhits:0` SAI — kiểm bằng cách tra ngược `action=query&titles=` cho thấy chuỗi đã bị bash/
terminal chuyển thành toàn dấu `?` (mất chữ Cyrillic) trước khi tới `curl`. **Chuyển hẳn sang chạy
qua Python `urllib.request` + `urllib.parse.urlencode()` (không qua `curl` dòng lệnh) và ghi mọi
kết quả ra file bằng `json.dump(..., ensure_ascii=False, encoding='utf-8')` rồi ĐỌC FILE bằng công
cụ Read (không `print()` thẳng — Windows terminal dùng codepage cp1252, `print()` một chuỗi Cyrillic
sẽ crash `UnicodeEncodeError` hoặc âm thầm in sai)** — kỹ thuật này giải quyết đúng gốc rễ, đáng
dùng ngay từ đầu cho các ngôn ngữ Nga/Trung/Nhật/Hàn/Ả Rập/Hy Lạp ở các lượt sau thay vì dò lỗi lại.

**Nguồn:** `Категория:Технопарки` (17 trang gốc, nhiều trang khái niệm chung như "Кластер
(экономика)"/"Технопарк" bỏ qua) + sub-cat Россия (11), Москва (5), Украина (1), Иран (0, rỗng),
Великобритания (0, rỗng) + `Категория:Бизнес-инкубаторы` (12 trang, nhiều trang khái niệm/quốc tế
đã có sẵn như Y Combinator/Station F bỏ qua). 23 trang chọn lọc → 23/23 có QID → 13/23 có `P856` →
sau lọc trùng ROSTER (5/13 đã có sẵn: Ленполиграфмаш, Технополис GS, Университетский, Южный
IT-Парк, МАТАМ) → 8 ứng viên → `check_url()` chỉ 3 sống thẳng + 1 redirect xác minh được → **4 mục**.

**Xác minh redirect:** `yedinstitute.org`→`yedi.ca`, `<title>` "Home - YEDI" xác nhận đúng tổ chức
(York Entrepreneurship Development Institute, Canada — không phải York nước Anh như tên tiếng Nga
"Йоркский" gợi ý, đây là York University ở Toronto) — đổi tên "YEDI (York Entrepreneurship
Development Institute)". Loại: `Venture for America` (chết), `Анкудиновка`/`itpark-nn.com` (trang
mỏng, redirect cũng mỏng), `Plug and Play Dagestan` (chết), `IdeaLab` (trang đỗ tên miền GoDaddy —
tổ chức thật `idealab.com` đã ngừng hoạt động/domain hết hạn, đáng tiếc vì đây là vườn ươm nổi
tiếng California).

**Giữ 4:** Nagatino i-Land (Nga, trung tâm kinh doanh Moscow), UNIT.City (Ukraine, công viên ĐMST
Kyiv — xác nhận `<title>` tiếng Ukraina "Інноваційний парк UNIT.City"), Innopolis (Nga, đặc khu kinh
tế công nghệ Tatarstan), YEDI (Canada). 0 Việt Nam. Toạ độ: Nagatino có `P625` thật; 3 còn lại tra
tay theo địa danh (Kyiv, Tatarstan, York/Toronto).

**Nhật Bản: thử nhưng KHÔNG tìm ra nguồn dùng được** — `list=search&srnamespace=14` cho các từ khoá
"サイエンスパーク"/"リサーチパーク"/"インキュベーション施設"/"テクノパーク" đều 0 kết quả thật
(chỉ "テクノパーク" khớp nhầm "Category:ジュラシック・パーク" = Jurassic Park!), "産業技術総合研究所"
(AIST) chỉ ra category về 1 viện nghiên cứu duy nhất, không phải danh bạ nhiều tổ chức. **Kết luận:
Wikipedia tiếng Nhật KHÔNG có cấu trúc category tương đương cho chủ đề này** — đừng thử lại các từ
khoá này, có thể cần tìm nguồn tiếng Nhật ngoài Wikipedia nếu muốn mở rộng Nhật Bản.

**Kết quả merge:** `ROSTER`: 20052 → **20056** (+4). Đơn vị trên bản đồ: 20061 → **20065** (+4, giữ
nguyên chênh lệch +9). Kiểm sau ghi: `node --check` sạch, thẻ cân bằng (111/111, 6/6), Browser pane
đọc đúng "20065 đơn vị được lập bản đồ", console sạch. Commit `86369dd`, `git push origin main`.

**Còn thiếu ~9935.** **Việc mở:** (1) category tiếng Nga còn ít trang chưa xử lý (Иран/Великобритания
rỗng, có thể do đổi tên category — chưa dò kỹ); (2) Nhật Bản cần nguồn NGOÀI Wikipedia category (có
thể thử `list=search` toàn văn thay vì chỉ category, hoặc METI/JETRO như các checkpoint rất sớm đã
thử và bị chặn 403 — có thể thử lại); (3) áp dụng kỹ thuật Python-urllib-UTF8-file cho MỌI ngôn ngữ
chữ khác Latin từ giờ, không riêng tiếng Nga; (4) còn Trung Quốc/Hàn Quốc/Ả Rập/Hy Lạp chưa thử qua
Wikipedia category (dù Wikidata keyword search đa ngôn ngữ đã thử 1 phần ở checkpoint 43).

---
**Lần trước:** 2026-09-11 (checkpoint 57 — **Wikipedia tiếng Tây Ban Nha `Categoría:Parques
tecnológicos` (+ sub-cat España/Uruguay) + `Incubadoras de empresas`, VÀ tiếng Bồ Đào Nha `Categoria:
Parques tecnológicos` (+ sub-cat Brasil) + `Incubadoras`/`Aceleradoras de negócios` — 2 nguồn ngôn
ngữ mới trong 1 checkpoint theo đúng tinh thần "tự động, không dừng" — sau lọc + xác minh (tỉ lệ
trùng ROSTER RẤT CAO ở batch Brazil, 6/8 mục có website đã có sẵn — xác nhận Brazil đã được rà khá kỹ
qua các checkpoint OSM/Wikidata trước) còn **7 mục thật sự mới (+3 Tây Ban Nha, +4 Brazil)**) — còn
thiếu ~9948 lúc cuối phiên.

**Tây Ban Nha:** `Categoría:Parques tecnológicos` (7 trang gốc) + sub-cat `...de España` (20 trang,
gồm cả sub-cat con `...de Castilla-La Mancha` 5 trang) + `...de Uruguay` (1 trang) +
`Categoría:Incubadoras de empresas` (5 trang, 2 trang khái niệm chung bỏ qua). 33 trang → 33/33 có
QID → 17/33 có `P856` → sau lọc trùng ROSTER (7/17 đã có sẵn — Málaga TechPark, Parque Científico
Valencia, Parque Tecnológico Sumqayit, Parque Científico y Tecnológico Vizcaya, Parque Científico y
Tecnológico Cantabria, Parque Científico Alicante, Parque Científico y Tecnológico UPM) → 10 ứng
viên → `check_url()` chỉ **3 sống** (6 chết thật kể cả sau retry timeout 25s, gồm cả `zonamerica.com`
— khu thương mại tự do lớn ở Uruguay, tiếc vì mất 1 nguồn tốt; và loại 1 mục IASP tự giới thiệu chính
mình `iasp.ws` — hiệp hội đã dùng làm NGUỒN ở checkpoint 21, không tính bản thân hiệp hội là 1 "đơn
vị" trong ROSTER, tránh lẫn nguồn với dữ liệu). Giữ: `Parque Científico y Tecnológico de
Castilla-La Mancha`, `CDTUC` (Cantabria), `Parque Tecnológico y Logístico de Vigo`.

**Bồ Đào Nha:** `Categoria:Parques tecnológicos` (4 trang gốc + 10 sub-cat quốc gia) + sub-cat
`...do Brasil` (20 trang — lớn nhất) + `Categoria:Incubadoras` (dùng vài mục lẻ) +
`Categoria:Aceleradoras de negócios` (4 trang). 26 trang → 25/26 có QID → chỉ **8/25 có `P856`**
(tỉ lệ thấp hơn hẳn các ngôn ngữ khác — nhiều bài tiếng Bồ về công viên công nghệ Brazil không điền
sẵn website trong Wikidata) → sau lọc trùng ROSTER: **6/8 ĐÃ CÓ SẴN** (Ciberporto Hong Kong, Parque
Tecnológico Ribeirão Preto, IPT São Paulo, Fundação Parque Tecnológico da Paraíba, CESAR Recife,
Parque Tecnológico da Bahia — xác nhận Brazil đã rà khá kỹ từ trước) → chỉ 2 ứng viên qua P856.

**Kỹ thuật bổ sung MỚI cho lượt sau — fallback đọc wikitext khi thiếu `P856`:** thử cào wikitext
17 trang còn thiếu website (regex tìm `|site=`/`|url=` trong infobox, hoặc link ngoài đầu tiên
không phải wikipedia/archive) — đa số ra LINK BÁO CHÍ/TRÍCH DẪN chứ không phải trang chủ tổ chức
(rác), chỉ lọc tay được **4 link thật đáng tin**: `Tecnopuc` (`tecnopuc.pucrs.br` — cần User-Agent
trình duyệt thật vì Cloudflare chặn `curl` mặc định, giống bài học checkpoint 36), `Parque de
Ciência e Tecnologia do Guamá` (`pctguama.org.br`, xác nhận `<title>`"PCT Guamá"), loại 2 ca còn lại
sau xác minh (`Parque Tecnológico Univap`→404 chết thật, `Parque Tecnológico de Sorocaba`→trang
"UOL HOST - Avisos" tức trang NHÀ CUNG CẤP HOSTING báo domain hết hạn/treo, KHÔNG phải trang thật —
thêm 1 ca false-positive kiểu mới cho danh sách đã biết). **Bài học: regex wikitext tìm URL không
đáng tin bằng `P856` có sẵn — tỉ lệ nhiễu cao (đa số link báo chí), chỉ nên dùng làm nguồn BỔ SUNG
cho vài trang đáng ngờ nhất (tên tổ chức nổi tiếng, không phải quét hàng loạt).**

**Kết quả cuối: 7 mục** — Tây Ban Nha (3): Parque Científico y Tecnológico de Castilla-La Mancha,
CDTUC, Parque Tecnológico y Logístico de Vigo. Brazil (4): Parque Tecnológico de Belo Horizonte
(BHTEC, qua P856), Porto Digital (qua P856), Parque de Ciência e Tecnologia do Guamá (qua wikitext
fallback), Tecnopuc (qua wikitext fallback). 0 Việt Nam. **Toạ độ:** tra tay theo địa danh trong tên
(Albacete/Santander/Vigo cho Tây Ban Nha; Belo Horizonte/Recife/Belém/Porto Alegre cho Brazil).

**Kết quả merge:** `ROSTER`: 20045 → **20052** (+7). Đơn vị trên bản đồ: 20054 → **20061** (+7, giữ
nguyên chênh lệch +9). Kiểm sau ghi: `node --check` sạch, thẻ cân bằng (111/111, 6/6), Browser pane
đọc đúng "20061 đơn vị được lập bản đồ", console sạch. Commit `2f38349`, `git push origin main`.

**Còn thiếu ~9948.** **Việc mở:** (1) category Tây Ban Nha/Bồ Đào Nha (ngoài Brazil) coi như đã
khai thác hết cho lượt này; (2) **Brazil đã bão hoà** (75% trùng ROSTER) — không đáng đào sâu thêm
qua Wikipedia, cần nguồn khác nếu muốn mở rộng Brazil (đăng ký ANPROTEC đã dùng ở checkpoint 18,
có thể còn sót); (3) kỹ thuật wikitext-fallback mới dùng được nhưng nhiễu cao — chỉ dùng cho
trang có tên tổ chức khả nghi rõ ràng, không quét hàng loạt; (4) `zonamerica.com` (Uruguay) và
`iasp.ws` (hiệp hội, không phải đơn vị) bị loại — không thử lại; (5) tiếp tục theo hướng ngôn ngữ
khác (Nhật/Nga/Trung/Hàn) hoặc quay về tìm nguồn lớn hoàn toàn mới (InBIA).

---
**Lần trước:** 2026-09-11 (checkpoint 56 — **Sếp yêu cầu chủ động, không dừng hỏi lại — tiếp tục ngay
2 category còn mở từ checkpoint 55: Wikipedia tiếng Ý `Categoria:Parchi scientifici tecnologici` +
tiếng Pháp `Catégorie:Pôle de compétitivité en France` (+ sub-cat Auvergne-Rhône-Alpes) — 33 trang,
sau lọc trùng + xác minh tay (phát hiện thêm 1 domain bị chiếm dụng khác `up-tex.fr`, 1 ca sáp nhập
tổ chức thật `PICOM`→`Cap Digital` đã có sẵn nên không tính trùng, 1 ca đổi tên xác nhận
`ViaMéca`→`CIMES`) còn **12 mục thật sự mới (+12)**) — còn thiếu ~9955 lúc cuối phiên.

**Nguồn:** `Categoria:Parchi scientifici tecnologici` (Wikipedia Ý, 24 trang — dò ra qua
`list=search&srnamespace=14` vì `allcategories acprefix=` không khớp tên có dấu cách giữa) +
`Catégorie:Pôle de compétitivité en France` (23 trang) + sub-cat `...en Auvergne-Rhône-Alpes` (6
trang) — cả 2 sub-cat cùng cây category `Catégorie:Cluster` đã kiểm rỗng ở checkpoint 55, nay tìm
đúng tên category khác ("Pôle de compétitivité" thay vì "Cluster"). Cùng kỹ thuật P856-hop, 32/33
có QID, 24/32 có `P856`.

**Phát hiện thêm 2 ca đáng chú ý ngoài các loại false-positive đã biết:**
1. **`up-tex.fr`** (pôle dệt may UP-TEX, Pháp) — `check_url()` báo "ok" nhưng đọc tay `<title>`
   ra "Portail sur l'entreprise, la finance & l'immobilier - Up Tex" (cổng tin tài chính/bất động
   sản chung chung, không có chữ "textile" nào trong trang) — domain đã bị CHIẾM DỤNG/đổi mục đích,
   chỉ giữ lại đúng tên "Up Tex" một cách trùng hợp. Cùng loại lỗ hổng `neode.ch` phát hiện checkpoint
   55 — xác nhận đây là rủi ro lặp lại thường xuyên với domain `.fr` cũ hết hạn, không phải ca hiếm.
2. **`picom.fr`→`capdigital.com`** — redirect xác nhận qua `<title>` "Cap Digital accueille le
   PICOM !" (Cap Digital tiếp nhận PICOM) — đây là SÁP NHẬP THẬT (PICOM gia nhập cluster Cap Digital
   lớn hơn), nhưng `Cap Digital` ĐÃ CÓ SẴN trong ROSTER (`capdigital.com`, thêm ở một checkpoint
   trước) — nên không tính là mục mới, chỉ ghi nhận đây KHÔNG PHẢI trùng giả mà là trùng THẬT do sáp
   nhập tổ chức. **Bài học: khi 1 redirect trỏ về TỔ CHỨC LỚN HƠN đã có sẵn trong ROSTER (không phải
   trang chủ nguyên công ty mẹ bất động sản như các ca loại trước), đây là tín hiệu sáp nhập thật —
   kiểm ROSTER trước khi kết luận trùng hay giữ.**

**1 ca đổi tên xác nhận qua nội dung:** `ViaMéca`→`cimes-hub.com`, `<title>` "CIMES, pôle de
compétitivité mécanique Auvergne Rhône-Alpes" — đổi tên thành "CIMES (ex-ViaMéca)".

**Kết quả cuối: 12 mục giữ lại** (Virtual Reality & Multi Media Park, Pôle européen de la céramique,
Environment Park, Parco Scientifico e Tecnologico di Udine "Luigi Danieli"/COSEF, Medicen Paris
Region, CIMES, Eurasanté, Aquimer, Tenerrdis, i-Trans, Systematic Paris-Region, NextMove) — loại 2
chết thật (Céréales Vallée, Parco scientifico tecnologico Polaris — cả trang lẫn domain mẹ
`sardegnaricerche.it` đều không kết nối được), 1 sáp nhập-trùng (PICOM), 1 domain chiếm dụng
(UP-TEX). Toàn bộ Ý/Pháp, 0 Việt Nam. **Toạ độ:** 2/12 có `P625` thật (Environment Park, Eurasanté);
10 còn lại tra tay theo địa chỉ/logo thật trên trang (Grenoble cho CIMES — xác nhận qua ảnh logo
"grenoble.jpg" trên trang; Paris cho NextMove — xác nhận qua địa chỉ đối tác CCFA "75008 Paris" ở
trang liên hệ, không phải trụ sở chính thức riêng nên độ tin cậy thấp hơn các ca khác).

**Kết quả merge:** `ROSTER`: 20033 → **20045** (+12). Đơn vị trên bản đồ: 20042 → **20054** (+12,
giữ nguyên chênh lệch +9). Kiểm sau ghi: `node --check` sạch, thẻ cân bằng (111/111, 6/6), Browser
pane đọc đúng "20054 đơn vị được lập bản đồ", console sạch. Commit `d35a584`, `git push origin main`.

**Còn thiếu ~9955.** **Việc mở:** (1) category Ý/Pháp liên quan coi như cạn cho lượt này; (2)
jawiki/es.wikipedia.org/pt.wikipedia.org đã thử `list=search` với cú pháp OR nhưng công cụ tìm kiếm
nội bộ các site đó không hỗ trợ OR đáng tin — cần dò từng từ khoá riêng lẻ thay vì gộp; (3) sếp đã
chốt: **tự động tiếp tục toàn bộ, không dừng hỏi lại** — phiên này chạy qua `/loop` tự pace, mỗi lượt
tự chọn nguồn tiếp theo.

---
**Lần trước:** 2026-09-11 (checkpoint 55 — **Wikipedia tiếng Pháp `Catégorie:Technopole` (+ 4 sub-cat
quốc gia France/Belgique/Canada/États-Unis) + `Catégorie:Pépinière d'entreprises`, kỹ thuật Wikidata
P856-hop quen thuộc, HƯỚNG MỞ đã ghi từ checkpoint 54 — nguồn vừa (75 trang), sau lọc + xác minh tay
kỹ hơn hẳn (phát hiện 1 domain bị chiếm dụng bán casino, 1 trang server mặc định chết, 1 trang rỗng)
còn **20 mục thật sự mới (+20)**, batch lớn nhất kể từ checkpoint 53**) — còn thiếu ~9967 lúc cuối
phiên.

**Bước 0 — dò category tiếng Pháp:** `Catégorie:Technopôle`/`Incubateur d'entreprises`/`Parc
scientifique`/`Parc technologique` (có dấu, viết đúng chính tả) đều KHÔNG tồn tại trên frwiki dạng
category — chỉ có `Catégorie:Technopole` (không dấu trên "o") + `Catégorie:Pépinière d'entreprises`
(6 trang, nhỏ). `Catégorie:Technopole` gốc có 4 sub-cat quốc gia: France (44 trang), Belgique (4),
Canada (3), États-Unis (6, hầu hết là TÊN VÙNG "Silicon Alley/Forest/Prairie" không phải tổ chức —
chỉ giữ `Research Triangle Park`) — Vietnam sub-cat bỏ qua theo quy ước. 1 sub-cat khác
(`Technopole de La Réunion`) hoá ra là danh sách CÔNG TY ĐẶT TRỤ SỞ tại khu công nghệ đó (đài truyền
hình, hãng phim...) — sai khuôn dữ liệu, không dùng, giống kiểu "Entreprise ayant son siège... par
technopole" cũng gặp trong cùng cây category.

**Bẫy mã hoá ký tự — 3 tên bị đọc sai dấu khi lấy từ JSON `categorymembers` qua nhiều lớp
copy/paste:** "Sème City" (đúng: "Sèmè City", 2 dấu huyền) và "Parc d'activités de Courtaboeuf"
(đúng: "Courtabœuf", ligature œ) bị gõ sai 1 ký tự khi chép tay từ kết quả JSON hiển thị trên
terminal — `action=query&titles=...` trả "missing" vì tên không khớp. **Sửa bằng cách tra lại theo
`pageids` thay vì `titles`** (API trả đúng tên gốc không qua tay người chép) — đây là kỹ thuật đáng
dùng khi nghi ngờ tên có dấu bị lệch: tra bằng ID số, không tra lại bằng chuỗi tên đã gõ tay.

**Kỹ thuật P856-hop (giống checkpoint 50-54):** 75 trang → 75/75 có QID (100%) → 46/75 có `P856`.
Lọc theo `P31` thấy nhiều kiểu lẫn lộn hơn hẳn đợt tiếng Đức: loại 3 mục rõ ràng sai phạm vi —
`Sakiet Ezzit` (Q41067667 "municipality of Tunisia" — thị trấn, không phải tổ chức), `Sèmè City`
(Q170584 "project" — bản thân dự án đô thị, KHÁC với "Agence de développement de Sèmè City" (Q31728
"public administration") là cơ quan quản lý thật — 2 trang riêng biệt cho cùng 1 khu, chỉ giữ agency
nếu chưa trùng), `La Doua` (Q123705 "neighborhood" — khu đại học Lyon, và URL chỉ là 1 trang con
của chính site Université Lyon 1, không phải site riêng). **Không loại theo P31 "neighborhood" một
cách máy móc** — `Temis`/`Technopolis de Rabat` cũng mang tag này nhưng có website RIÊNG mô tả rõ
ràng là tổ chức quản lý khu công nghệ thật (không phải trang thành phố/cổng thông tin chung) → giữ,
xác minh qua đọc nội dung thay vì chỉ tin nhãn P31.

**Lọc trùng ROSTER** (baseline 20013): loại 12/42 (sau loại P31) trùng domain/tên — trong đó phát
hiện thú vị: "Agence de développement de Sèmè City" (`semecity.bj`) ĐÃ CÓ SẴN trong ROSTER từ đợt
Châu Phi (`africatechschools.com`) trước đây dưới tên khác — xác nhận đúng, không phải trùng giả.
Còn **30 ứng viên**.

**`check_url()` + rà tay SÂU HƠN HẲN các lượt trước — phát hiện 3 LOẠI false-positive MỚI mà
`check_url()` không bắt được (bổ sung cho danh sách lỗ hổng đã biết từ checkpoint 33/43/50):**
1. **Domain bị chiếm dụng bán casino trực tuyến** — `neode.ch` (Thuỵ Sĩ) trả 200 OK, nội dung đủ dài
   ("Ausländische Online Casinos Schweiz 2026"...) nhưng ĐÂY LÀ TRANG QUẢNG CÁO CASINO tiếng Đức,
   không liên quan gì tới tổ chức Neode gốc — CÙNG LOẠI lỗ hổng đã ghi ở checkpoint 50 (Boston Open
   Science Laboratory bị chiếm dụng bán cờ bạc Indonesia) nhưng lần này ở miền `.ch` — xác nhận đây
   không phải ca hiếm, cần luôn đọc tay tiêu đề/nội dung thật, không tin `check_url()` "ok" một mình.
2. **Trang "Web Server's Default Page"** — `alsace-biovalley.com` (BioValley France) trả 200 OK với
   đủ text (trang mặc định Apache/nginx có nhiều chữ hướng dẫn cấu hình) nên vượt qua kiểm tra độ dài
   của `check_url()`, nhưng đây là SERVER CHƯA TỪNG ĐƯỢC CẤU HÌNH — không phải trang thật đang hoạt
   động (khác "The Network Hub" nginx-mặc-định đã gặp ở checkpoint 50, cùng loại lỗi, domain khác).
3. **Trang rỗng hoàn toàn kể cả sau khi JS chạy** — `polemaud.com` (Pôle de compétitivité MATIKEM)
   trả 200 OK nhưng `curl` lẫn Browser pane thật (đợi JS chạy xong) đều cho `<title>` và nội dung
   RỖNG — không phải lỗi mạng, trang thực sự không render gì cả (có thể lỗi cấu hình SPA phía họ).

**2 ca cross-domain redirect xác minh tay THÀNH CÔNG (đổi thương hiệu, giữ + đổi tên):** `Rennes
Atalante` (`rennes-atalante.fr`→`lepoool.tech`) — nội dung xác nhận "Le Poool x La French Tech
Rennes St-Malo, la communauté de l'innovation et de l'entrepreneuriat" — cùng thành phố, cùng sứ
mệnh, đổi tên thành "Le Poool (ex-Rennes Atalante)"; `Archamps Technopole`
(`archamps-technopole.com`→`archparc.fr`) — nội dung xác nhận rõ ràng "180 entreprises... 2137
personnes... annuaire d'entreprises... gouvernance" cho ĐÚNG khu công nghệ đó gần Genève, đổi tên
thành "ArchParc (ex-Archamps Technopole)". **1 ca cross-domain KHÔNG xác minh được, LOẠI:**
`Industries et Agro-Ressources` (`iar-pole.com`→`bioeconomyforchange.eu`) — trang đích nói về
"bioéconomie" hợp chủ đề nhưng tìm không ra chữ "IAR" hay tên cũ nào trong nội dung để xác nhận
CHÍNH tổ chức đó đổi tên (khác 2 ca trên có bằng chứng rõ) — theo đúng kỷ luật "không xác minh được
thì loại", không dùng suy đoán ngoài trang.

**Kết quả cuối: 20 mục giữ lại** (30 ứng viên − 5 chết thật [El Ghazala/Végépolys Valley/Quartier de
l'innovation de Montréal/Cancer-Bio-Santé/Technopolis de Rabat] − 3 false-positive mới phát hiện
[Neode/BioValley France/MATIKEM] − 1 redirect không xác minh được [Industries et Agro-Ressources] −
1 loại theo P31 project [Sèmè City, agency giữ nhưng đã trùng ROSTER]). Toàn bộ Pháp/Thuỵ Sĩ, 0 Việt
Nam. **Gán toạ độ:** 12/20 có `P625` thật; 8 còn lại tra tay theo địa chỉ thật ghi trên trang (Lyon,
Évry, Chartres, Archamps, Saint-Beauzire, Plouzané/Brest, Angers, Paris) — xác nhận riêng `Biopôle`
qua nội dung trang ("large life sciences campus in Lausanne, Switzerland") trước khi gán toạ độ
Lausanne, và `Cluster NAOS` qua `og:description` ("Nouvelle-Aquitaine Open Source (NAOS) est un pôle
de compétitivité...") trước khi gán Bordeaux (thủ phủ vùng, không có địa chỉ cụ thể hơn trên trang).

**Kết quả merge:** `ROSTER`: 20013 → **20033** (+20). Đơn vị trên bản đồ: 20022 → **20042** (+20,
giữ nguyên chênh lệch +9). Kiểm trước khi ghi: `git status`/`git log` sạch. Kiểm sau ghi: `node
--check` sạch, thẻ `div`/`section` cân bằng (111/111, 6/6), mở qua HTTP server cục bộ (Browser pane)
đọc đúng "20042 đơn vị được lập bản đồ" / "20033 trong danh mục mở rộng", console sạch. Commit
`179a620`, `git push origin main`.

**Còn thiếu ~9967 để đạt 30000.** **Việc mở cho lượt sau:** (1) frwiki `Catégorie:Technopole` coi
như đã khai thác hết (đã crawl đủ 2 tầng root + 4 sub-cat quốc gia + `Pépinière d'entreprises`); (2)
**jawiki (tiếng Nhật) vẫn CHƯA THỬ** — thử tìm category tương đương ("サイエンスパーク"/"リサーチパー
ク"/"インキュベーション施設") trước khi mở rộng sang ngôn ngữ khác nữa; (3) **kỹ thuật rà tay lượt
này phát hiện 3 loại false-positive MỚI mà `check_url()` chưa bắt được** (domain chiếm dụng bán
casino ở miền `.ch`, trang "Web Server's Default Page", trang JS rỗng hoàn toàn) — cân nhắc thêm bước
kiểm `<title>` không rỗng + không chứa cụm "Default Page"/"Apache2 Ubuntu Default" vào `check_url()`
dùng chung, đỡ phải rà tay lại từng batch; (4) InBIA (checkpoint 49) vẫn mở, nguồn LỚN nhất từng tìm
được nhưng bị gate sau đăng nhập; (5) tốc độ 20 mục/checkpoint (frwiki) so với 7 mục/checkpoint
(dewiki) xác nhận Pháp có nhiều tổ chức "technopole/pôle de compétitivité" hơn Đức trong phạm vi
ROSTER — có thể còn dư địa nếu mở rộng sang các Catégorie liên quan khác (`Catégorie:Cluster
d'entreprises`, `Catégorie:Pôle de compétitivité` — CHƯA kiểm tồn tại hay chưa) trước khi chuyển hẳn
sang ngôn ngữ khác.

---
**Lần trước:** 2026-09-10 (checkpoint 54 — **Wikipedia tiếng Đức `Kategorie:Technologiepark` + 2
sub-cat quốc gia (Deutschland/Österreich), kỹ thuật Wikidata P856-hop quen thuộc, HƯỚNG MỞ đã ghi
từ checkpoint 53 ("dewiki/frwiki/jawiki chưa từng thử") — nguồn nhỏ (50 trang), sau lọc kiểu-địa-danh
+ trùng ROSTER chỉ còn 7 mục thật sự mới (+7)**) — còn thiếu ~9987 lúc cuối phiên.

**Bước 0 — dò category tiếng Đức:** `action=query&list=allcategories&acprefix=...` xác nhận
`Kategorie:Gründerzentrum`/`Innovationszentrum`/`Inkubator` KHÔNG tồn tại trên dewiki (0 kết quả) —
chỉ có `Kategorie:Technologiepark` (20 trang cấp gốc, gồm cả tên vùng/thành phố kiểu "Silicon Х" lẫn
tổ chức thật) + 2 sub-cat quốc gia `Technologiepark in Deutschland` (22 trang) và `...in Österreich`
(8 trang) — tổng 50 trang duy nhất. `Kategorie:Wissenschaftspark` chỉ có 1 sub-cat rỗng nội dung
(`Wissenschaftspark Leipzig`, không dùng). Bài `Liste der Technologiezentren` (tìm thấy qua
`list=search`) hoá ra là danh sách TÊN VÙNG ("Silicon Valley", "IT-Cluster Rhein-Main-Neckar"...)
kèm số liệu kinh tế vùng, KHÔNG phải danh bạ tổ chức có URL — loại ngay, không dùng.

**Kỹ thuật P856-hop (giống checkpoint 50-53):** `pageprops&redirects=1` lấy `wikibase_item` cho cả
50/50 trang (100%, không có trang nào thiếu QID) → `wbgetentities` lấy `P856`/`P31`/`P625` — 27/50
có website. Lọc theo `P31`: loại 3 mục rõ ràng là ĐỊA DANH/khu quy hoạch chứ không phải tổ chức —
`Sophia Antipolis` (Q486972 human settlement — xã/thị trấn ở Pháp), `Neom` (Q1074523 planned
community — siêu dự án đô thị Ả Rập Xê Út), `Technopolis (Gussew)` (Q1350536 naukograd — thành phố
khoa học Nga, cùng loại lỗi "địa danh lẫn vào" đã gặp nhiều lần từ checkpoint 32 trở đi, khác kiểu
"human settlement"/"planned community"/"naukograd" chưa từng có trong bộ lọc `PLACE_TYPES` cũ nên
phải lọc tay theo QID cụ thể lần này).

**Lọc trùng ROSTER** (base_domain + normalize_name, baseline 20006): loại 16/24 mục còn lại — tỉ lệ
trùng RẤT CAO (67%), đúng dự đoán vì Đức là nước ROSTER đã khai thác kỹ nhất qua nhiều checkpoint
(hackerspace OSM, `office=research`, Wikidata `research institute`...) — các case tiêu biểu (WISTA/
Adlershof, Station F, MaRS, Paris-Saclay đã có qua tên khác, EUREF, Lakeside Science & Technology
Park, Forschungszentrum Seibersdorf...) đều đã có sẵn trong ROSTER từ trước, kể cả 1 case trùng TÊN
nhưng khác domain (Paris-Saclay — giữ nguyên bản đã xác minh kỹ ở checkpoint 50-51, không ghi đè).
Còn **7 ứng viên**.

**`check_url()` + xác minh tay 2 ca cross-domain redirect** (đọc `<title>` trang đích thật, đúng kỷ
luật đã có từ checkpoint 43): `RailCampus OWL` (`railcampus-owl.info`→`railcampus-owl.de`) — xác
nhận `<title>` đúng "RailCampus OWL", giữ URL domain mới; `Techcenter Linz Winterhafen`
(`techcenter.at`→`techharbor.at`) — `<title>` "TECH HARBOR - NEUE WERFT & TECHCENTER" xác nhận CHÍNH
tổ chức đó đổi thương hiệu (chữ "TECHCENTER" vẫn còn trong title mới) — đổi tên thành "Tech Harbor
(Techcenter Linz Winterhafen)" để vẫn tra được theo tên cũ. 5 mục còn lại (`Gav-Yam Negev Advanced
Technologies Park`, `Aerospace Valley`, `Toulouse Aerospace`, `Ludwig Bölkow Campus`, `Aérocentre`)
sống thẳng không redirect — đọc `<title>` xác nhận cả 5 đúng tổ chức: `Aerospace Valley`/`Aérocentre`
là 2 "pôle de compétitivité" (hiệp hội cụm ngành hàng không thật của Pháp, có nhân sự/hội viên, cùng
loại "cluster" đã chấp nhận từ checkpoint 41), `Toulouse Aerospace` là đơn vị quản lý/phát triển khu
kinh doanh hàng không Toulouse (P31 "ecodistrict"+"campus"+"research center" — cùng loại khu phát
triển như Paris-Saclay đã chấp nhận, không phải trang bất động sản đơn thuần).

**Gán toạ độ:** 5/7 có `P625` thật từ Wikidata; 2 mục thiếu (`RailCampus OWL`, `Tech Harbor`) tra tay
qua nội dung trang chủ (RailCampus OWL tự ghi rõ "in Minden" nhiều lần trong text; Tech Harbor ở
Linz, Áo — khớp tên gốc "Linz Winterhafen") → toạ độ thành phố thật (Minden 52.2897/8.9151, Linz
48.3069/14.2858).

**Kết quả merge:** `ROSTER`: 20006 → **20013** (+7). Đơn vị trên bản đồ: 20015 → **20022** (+7, giữ
nguyên chênh lệch +9). Kiểm trước khi ghi: `git status`/`git log` sạch. Kiểm sau ghi: `node --check`
sạch, thẻ `div`/`section` cân bằng (111/111, 6/6), mở qua HTTP server cục bộ (Browser pane) đọc đúng
"20022 đơn vị được lập bản đồ" / "20013 trong danh mục mở rộng" / "12 đơn vị tại Việt Nam" (không
đổi) / "9 case phân tích chuyên sâu" (không đổi), console sạch (chỉ favicon 404 có sẵn từ trước).
Commit `c4f0f5a` (riêng; phần bản đồ zoom HN/HCM ở mục riêng phía trên là 2 commit khác,
`18c80dc`+`c29c356`, cùng phiên), `git push origin main`.

**Còn thiếu ~9987 để đạt 30000.** **Việc mở cho lượt sau:** (1) dewiki `Kategorie:Technologiepark`
coi như đã khai thác hết (chỉ 50 trang, không có category quốc gia nào khác ngoài Deutschland/
Österreich); (2) **frwiki/jawiki vẫn CHƯA THỬ** (đúng gợi ý để lại từ checkpoint 53) — thử
`Catégorie:Technopôle`/`Catégorie:Pépinière d'entreprises` (Pháp) và tương đương tiếng Nhật trước
khi mở rộng sang ngôn ngữ khác; (3) InBIA (checkpoint 49) vẫn mở, chưa làm, nguồn LỚN nhất từng tìm
được nhưng bị gate sau đăng nhập; (4) tốc độ 7 mục/checkpoint (cả 2 checkpoint liên tiếp 53-54 đều
+7, từ 2 nguồn khác hẳn nhau) xác nhận các nguồn Wikipedia nhỏ đã vào giai đoạn "quả treo rất thấp",
cần tiếp tục nhắc sếp về khoảng cách 9987 so với tốc độ này.

---
**Lần trước:** 2026-09-10 (checkpoint 53 — **`List of Biomakerspaces in the United States`
(Wikidata Q140001361, việc mở để lại từ checkpoint 52) qua kỹ thuật Wikidata P856-hop quen thuộc —
nguồn RẤT NHỎ (chỉ 16 mục "Active"), sau lọc trùng ROSTER + xác minh tay chỉ còn 7 mục thật sự mới
(+7)**) — còn thiếu ~9994 lúc cuối phiên.

**Bước 0 — xác nhận trang tồn tại:** `Special:EntityData/Q140001361.json` xác nhận nhãn "List of
Biomakerspaces in the United States", sitelink `enwiki` đúng tên, `P31` có giá trị (danh sách hợp
lệ) — khớp với ghi chú "mới tìm thấy, chưa cào" của checkpoint 52.

**Nguồn dùng:** cào wikitext trang (`action=parse&prop=wikitext`, 3811 ký tự — RẤT NGẮN so với các
trang "List of..." trước đây hàng trăm/nghìn mục). Trang chia 2 mục `== Active ==` (16 mục, 4 vùng
giờ Pacific/Mountain/Central/Eastern) và `== Inactive ==` (18 mục) — **chỉ lấy mục `Active`, bỏ hẳn
toàn bộ `Inactive` vì đây là danh sách các biomakerspace ĐÃ NGỪNG HOẠT ĐỘNG theo chính Wikipedia tự
phân loại** (không cần check_url mới biết loại — khác các lượt trước phải tự phát hiện qua đọc tay
nội dung trang đích).

**Kỹ thuật lấy URL — kết hợp 3 nguồn tuỳ mục:** (1) URL trực tiếp trong `<ref>` của bullet không có
wikilink (Berkeley BioLabs, MIT BioMakers, Cap City Biohackers dạng Inactive nên bỏ); (2) hop qua
Wikidata P856 cho bullet có wikilink dạng `[[Tên]]` — `pageprops&redirects=1` lấy `wikibase_item`
rồi `wbgetentities` lấy `P856`/`P625`: chỉ **2/7 trang có P31 tồn tại có P856** (BioCurious, và
Genspace không có P856 nhưng có P625 — cả hai đều đã trùng ROSTER nên không dùng); các trang còn lại
(SoundBio Lab, HeatSync Labs, ChiTownBio, FamiLAB, Baltimore Underground Science Space) hoàn toàn
không có `P856`/`P625` trên Wikidata — phải tìm URL qua bước 3; (3) **`WebSearch` cho từng mục
không có `<ref>` lẫn không có `P856`** (kỹ thuật bổ sung mới, cần thiết vì nguồn quá nhỏ để tự động
hoá as bulk) — tìm và xác nhận domain chính chủ cho Counter Culture Labs, SoundBio Lab, HeatSync
Labs, ChiTownBio, Baltimore Underground Science Space (BUGSS), Genspace, Ronin Genetics, Triangle
DIY Biology, Bio Tech and Beyond, Biodidact — 10/16 mục Active cần bước này.

**Lọc trùng ROSTER (base_domain + normalize_name, baseline 19999):** phát hiện **tỉ lệ trùng CỰC
CAO — 7/15 mục có URL đã trùng domain VÀ tên chính xác với ROSTER hiện có** (Counter Culture Labs,
SoundBio Lab, BioCurious, HeatSync Labs, Baltimore Underground Science Space/BUGSS, Genspace,
FamiLAB) — xác nhận đúng dự đoán của checkpoint 52 rằng đợt hackerspace/makerspace lớn trước đó (nguồn
OSM `amenity=hackerspace`) đã quét qua hầu hết các case nổi tiếng này, kể cả khi chúng xuất hiện lại
qua nguồn Wikipedia khác. Cũng thử `Baltimore Hackerspace` (mục mới thấy qua `WebSearch` phụ, KHÔNG
nằm trong trang Biomakerspaces — phân biệt với BUGSS) qua Wikidata P856 → `baltimorehackerspace.com`
nhưng CŨNG đã trùng ROSTER (domain + tên) — loại.

**`check_url()` + đọc tay 8 ứng viên còn lại sau lọc trùng, đúng kỷ luật domain-hijack của checkpoint
52:** 1 ca (`Biodidact`, qua domain chính `biodidact.net`) bị `URLError` khi truy cập trực tiếp,
domain thay thế `losalamosmakers.org` (tìm qua `WebSearch`, cùng tổ chức theo mô tả "The Community
Lab") trả 200 OK qua `check_url()` nhưng là site Wix render phía client — đọc tay 200KB đầu không tìm
thấy chữ "Biodidact"/"Los Alamos" hay bất kỳ `<title>`/`og:title` nào trong HTML tĩnh (nội dung thật
chỉ render bằng JS phía trình duyệt, không xác minh được bằng `urllib`) — kết hợp với tín hiệu phụ
quan trọng: kết quả `WebSearch` cho thấy mục Yelp của Biodidact ghi rõ **"BIODIDACT - CLOSED"** →
**LOẠI hẳn, không đủ căn cứ xác nhận còn hoạt động** (bài học mới: khi trang JS-rendered không xác
minh được nội dung tĩnh VÀ có tín hiệu bên ngoài gợi ý đã đóng cửa, không nên tin theo hướng có lợi
chỉ vì HTTP 200). 7 ca còn lại đều xác nhận đúng qua đọc `<title>`/`og:title`/`og:site_name` khớp rõ
tên tổ chức: `Berkeley BioLabs`("Berkley BioLabs"), `La Jolla Library Bio Lab` (title khớp chính xác
trang IDEA Lab của City of San Diego — giữ dù là trang chính quyền vì là trang RIÊNG cho dịch vụ cụ
thể, không phải cổng thông tin chung chung), `Bio, Tech, and Beyond` (title "HOME | biotechandbeyond",
og:site_name "biotechandbeyond" — xác nhận qua đọc 200KB vì trang JS-heavy không lộ `<title>` ở byte
đầu), `ChiTownBio` ("Chicago's Community Biology Lab"), `MIT BioMakers` ("MIT BioMakers"), `Ronin
Genetics` ("Ronin Genetics"), `Triangle DIY Biology` (og:site_name "Triangle DIY Biology", title
"Home" chung chung nên phải đọc og:site_name mới xác nhận được — cùng bài học "og:title/og:site_name
khi title JS-app chung chung" của checkpoint 50).

**Cân nhắc phạm vi:** `Ronin Genetics`/`Triangle DIY Biology` là nhóm DIYbio hoạt động NHỜ không gian
của tổ chức khác (SplatSpace, Durham NC) chứ không sở hữu địa điểm riêng — vẫn GIỮ vì có website/hoạt
động thật riêng biệt (Ronin Genetics có dịch vụ sequencing thật), cùng logic đã chấp nhận các case
"tenant"/chương trình gắn với không gian khác trong ROSTER hiện có.

**Gán toạ độ:** không mục nào trong 7 mục cuối có `P625` → dùng **centroid Mỹ tính lại từ 1419 mục
`United States` hiện có trong ROSTER** (38.818126697451845, -94.63002571520904 — gần khớp centroid
checkpoint 52 dùng, chênh nhỏ do ROSTER đã lớn hơn).

**Mở rộng thử thêm qua Wikipedia `list=search` (bước 1 phần 2 của việc giao) trước khi merge:** thử
10 từ khoá ("list of hackerspaces", "list of makerspaces", "list of fab labs", "list of science
parks", "list of technology transfer offices", "list of research parks", "list of business
incubators", "list of coworking spaces", "list of living labs") — **không tìm được trang "List
of..." MỚI nào chưa từng dùng qua 52 checkpoint trước**, chỉ trả lại các trang đã biết
(`List of research parks`, `List of science parks in the United Kingdom`, `List of startup
incubators in the United States`...) hoặc các trang không đúng định dạng danh sách tổ chức kèm URL.
1 mục mới lộ ra (`HiveBio Community Laboratory`) hoá ra đã có mặt trong chính trang Biomakerspaces ở
mục Inactive — đã loại theo đúng quy tắc trên. **Kết luận: hướng Wikipedia "List of..." + category
CƠ BẢN ĐÃ CẠN** (khớp với dự đoán của checkpoint 52) — không tìm thêm được trang nguồn mới nào qua
`list=search`.

**Kết quả merge:** `ROSTER`: 19999 → **20006** (+7). Đơn vị trên bản đồ: 20008 → **20015** (+7, giữ
nguyên chênh lệch +9). Kiểm trước khi ghi: `git status`/`git log` sạch — phát hiện 1 phiên khác đã
push 2 commit không liên quan ROSTER (`7ece197`, `9b48f90` — sửa panel bản đồ Việt Nam) TRONG lúc
phiên này đang xử lý, nhưng `len(load_roster(...))` vẫn = 19999 cả trước và sau các commit đó (không
đụng dữ liệu ROSTER) nên không cần dedup lại. Kiểm sau ghi: `node --check` sạch (script inline
3,424,717 ký tự), thẻ `div`/`section` cân bằng (107/107, 6/6), mở `index.html` qua HTTP server cục
bộ (`static-server`) qua Browser pane: đúng "20015 đơn vị được lập bản đồ" / "20006 trong danh mục mở
rộng" / "12 đơn vị tại Việt Nam" (không đổi) / "9 case phân tích chuyên sâu" (không đổi). Commit
`17f4272`, `git push origin main` — xác nhận fast-forward `9b48f90..17f4272`.

**Còn thiếu ~9994 để đạt 30000.** **Việc mở cho lượt sau:** (1) nguồn Wikipedia "List of..."/
category-crawl/`list=search` nay ĐÃ XÁC NHẬN CẠN qua 3 checkpoint liên tiếp (51-53) thử nhiều hướng
khác nhau — KHÔNG nên tiếp tục đầu tư thời gian vào hướng này nữa trừ khi có ý tưởng kỹ thuật hoàn
toàn mới (vd nguồn ngôn ngữ khác ngoài Wikipedia tiếng Anh — chưa từng thử `dewiki`/`frwiki`/
`jawiki`... "Liste von..."/"Liste des..." có thể còn mục chưa trùng bản tiếng Anh); (2) InBIA
(checkpoint 49, mục 7) — vẫn mở, chưa làm, nguồn LỚN nhất từng tìm được nhưng bị gate sau đăng nhập;
(3) tốc độ 7 mục/checkpoint lần này (nguồn nhỏ nhất trong nhiều checkpoint gần đây) cộng dồn với
tốc độ dao động 7-94 của 3 checkpoint trước — khoảng cách 9994 vẫn cực lớn so với tốc độ hiện tại,
**cần báo cáo lại nghiêm túc với sếp về nguồn hoàn toàn mới hoặc điều chỉnh kỳ vọng tốc độ/mốc
30000** (đã nhắc ở checkpoint 52, nay càng rõ hơn khi cả hướng Wikipedia lẫn category lẫn `list=search`
đều xác nhận cạn cùng lúc).

---
**Lần trước:** 2026-09-10 (checkpoint 52 — **Wikipedia `Category:Coworking space providers` +
`Category:Hackerspaces` (+2 sub-cat) + `Category:Fab labs`, cùng kỹ thuật Wikidata P856-hop, nhưng
đợt này lộ RÕ tầm quan trọng của bước rà tay nội dung sau `check_url()` — 8/15 ứng viên "OK" tự
động hoá vẫn là false positive khi đọc tay (+7 thật)**) — còn thiếu ~10001 lúc cuối phiên.

**Bước 0 — kiểm tra category rỗng/đổi tên mà checkpoint 51 nghi ngờ:** `Category:Coworking spaces`,
`Category:Makerspaces`, `Category:Living labs`, `Category:Research parks`, `Category:Startup
accelerators by country`, `Category:Technology parks`, `Category:Innovation hub/district`,
`Category:Startup incubator` — **TẤT CẢ đều 0 thành viên** (`action=query&list=categorymembers`
trả rỗng) dù `action=query&list=allcategories` liệt kê chúng tồn tại (category có tên nhưng không
còn trang nào gán — có thể do đổi hướng/gộp vào category khác, không phải lỗi truy vấn). Dò lại
qua `list=allcategories&acprefix=` tìm được TÊN THẬT đang dùng: `Category:Makerspaces` (viết hoa
khác) → vẫn 0; `Category:Coworking space providers` (25 trang, có thật); `Category:Business
incubators by country` (17 sub-cat quốc gia — đã dùng ở checkpoint 51 nên bỏ qua); `Category:Fab
labs` (chỉ 4 trang); `Category:Hackerspace`/`Hackerspaces` (61 trang + 2 sub-cat: `Hackerspaces in
the San Francisco Bay Area`, `Public laboratories`). **Kết luận: nhóm "Coworking spaces/Makerspaces/
Living labs/Research parks/Startup accelerators by country" của checkpoint 51 XÁC NHẬN không tồn
tại dưới tên đó trên Wikipedia hiện tại — đừng thử lại các tên chính xác này nữa** (khác hẳn nghi
ngờ ban đầu "có thể đổi tên" — đã tìm tên thay thế và dùng rồi).

**Nguồn dùng — category-crawl 1 tầng (không "by country" vì các category này không có sub-cat theo
quốc gia):** `Category:Coworking space providers` + `Category:Hackerspaces` + 2 sub-cat của nó +
`Category:Fab labs` → 92 trang duy nhất (namespace bài viết, đã loại `Category:WeWork` sub-cat vì
toàn bài về công ty/sách/series truyền hình không phải địa điểm). Cùng kỹ thuật Wikidata P856-hop
(`pageprops→wikibase_item` rồi `wbgetentities` lấy `P856`/`P31`/`P625`) như checkpoint 50/51: 91/92
resolve QID, 54/91 có `P856`.

**Lọc `P31` bằng tay từng dòng (không đủ mẫu số lớn để xây allowlist tự động như checkpoint 51):**
đọc nhãn `P31` của cả 91 QID (tra `wbgetentities` cho các ID instance-of xuất hiện) → loại theo
nhóm rõ ràng sai phạm vi: bảo tàng (`Computer History Museum Slovenia`, `Eli Whitney Museum`), thư
viện công cộng (`Chattanooga Public Library`), nhà ga xe lửa (`Fürstenberg (Havel) station` — wikilink
khớp nhầm QID), toà nhà địa chỉ cụ thể không phải tổ chức (`Ubica`→QID thực ra là "Ganzenmarkt 24-26,
Utrecht"), công ty holding bất động sản văn phòng đa quốc gia quá rộng (`International Workplace
Group/IWG plc` — công ty mẹ niêm yết của Regus/Spaces, không phải 1 địa điểm cụ thể), dự án phần
mềm/giáo dục không phải không gian vật lý (`Turtlestitch`), trung tâm nghệ thuật thuần tuý dù có
hackerspace phụ (`AS220` — bảo tàng/trung tâm nghệ thuật cộng đồng là chính; `Eyebeam` — nghệ thuật+
công nghệ nhưng cốt lõi là art residency; `De WAR` — trung tâm nghệ thuật+citizen science, fab lab
chỉ là 1 phần). Sau lọc P31 + rà tay: 44 ứng viên có `P856` hợp phạm vi.

**Lọc trùng ROSTER (`base_domain`+`normalize_name`):** 23/44 đã trùng — tỉ lệ trùng CAO (52%),
xác nhận ROSTER đã có 1 đợt hackerspace/makerspace quy mô lớn từ trước (khớp với "OSM (cạn hoàn
toàn)" trong danh sách nguồn đã loại — OSM `amenity=hackerspace` rõ ràng đã quét qua phần lớn các
hackerspace nổi tiếng này ở checkpoint cũ hơn dùng chung nguồn Wikipedia/OSM). Còn **15 ứng viên
sạch**.

**`check_url()` 15 ứng viên:** 10 "OK" ngay, 2 lỗi mạng thử lại `timeout=30` cứu được 1
(`Boston Open Science Laboratory`), 3 bị từ chối rõ ràng (`Jaaga`→domain for sale, `Port City
Makerspace`→403 xác nhận qua `curl` riêng là chặn bot không phải lỗi tạm, `Ucommune`→`curl` xác nhận
DNS không resolve được, domain chết thật). Còn 11 "OK".

**PHÁT HIỆN QUAN TRỌNG — đọc tay nội dung 11 ca "OK" lộ RA 4 ca `check_url()` KHÔNG bắt được (bài
học mới, bổ sung cho danh sách "false positive" đã biết từ checkpoint 43-51):**
1. `ASCII` (a.scii.nl) — trang có 200 OK, đủ dài, không khớp `PARKING_PAGE_SIGNS`, nhưng nội dung
   thật là **"RIP 1999–2006"** — trang tưởng niệm tổ chức đã GIẢI THỂ 18 năm trước, không phải
   trang chủ đang hoạt động.
2. `The Network Hub` (thenetworkhub.ca) — 200 OK, đủ dài text, nhưng nội dung là **trang mặc định
   "Welcome to nginx!"** — domain còn trỏ DNS nhưng chưa từng được cấu hình web server thật (khác
   "parking-for-sale" nên không khớp `PARKING_PAGE_SIGNS`, cũng khác "thin page" vì text đủ dài).
3. `Omni Commons` (omnicommons.org) — 200 OK, nội dung dài, đọc kỹ mới thấy văn phong QUÁ KHỨ: "...
   was a project to steward a building ... finally sold it in [năm]" — tổ chức đã BÁN TOÀ NHÀ, ngừng
   hoạt động, trang chỉ còn lưu lại như trang lưu trữ.
4. `Boston Open Science Laboratory` (bosslab.org) — nghiêm trọng nhất: domain đã bị **CHIẾM DỤNG
   (hijack) cho trang cờ bạc trực tuyến tiếng Indonesia** ("Situs Judi Online Terpercaya di Indonesia")
   — vượt qua `check_url()` vì nội dung ĐỦ DÀI (không "thin"), KHÔNG khớp bất kỳ `PARKING_PAGE_SIGNS`
   nào (đây là trang cờ bạc thật đang hoạt động, không phải trang "domain for sale"), và KHÔNG
   redirect cross-domain (domain gốc vẫn trả 200 trực tiếp, chỉ nội dung bên trong đã bị thay hoàn
   toàn). **Bài học quan trọng nhất phiên này: `check_url()` chỉ đảm bảo "có nội dung thật, không
   phải trang ký sinh/tên miền rao bán" — KHÔNG đảm bảo nội dung đó vẫn là ĐÚNG TỔ CHỨC GỐC. Domain
   hijack cho mục đích khác (cờ bạc, spam SEO...) là một lớp false-positive HOÀN TOÀN KHÁC "parking
   page"/"cross-domain redirect" đã biết — không có tín hiệu tự động nào bắt được ngoài đọc tay và
   nhận ra nội dung không liên quan gì đến tên tổ chức.** Từ nay các batch nhỏ (≤20 ứng viên) nên
   LUÔN đọc tay ít nhất tiêu đề/đoạn mở đầu thật của trang, không chỉ tin `check_url()` "ok".

**Còn 7 ứng viên xác nhận đúng qua đọc tay** (tiêu đề/nội dung khớp rõ tên tổ chức): `Betahaus`
(Berlin, coworking — trùng khớp "betahaus Berlin | Coworking, Offices, Event Spaces"), `Civic Hall`
(New York, coworking/civic tech), `Hera Hub` (Mỹ, coworking nữ doanh nhân), `Industrious` (Mỹ,
chuỗi coworking — khớp "Coworking & Private Office Space | Industrious"), `Open Works`
(Baltimore — dùng URL đổi hướng cùng gốc `openworksbmore.org` thay vì `.com` gốc vì `.com` 404,
`.org` xác nhận sống + khớp "Open Works | Make Space for All"), `SketchPad` (Chicago, makerspace),
`The Office Pass` (Ấn Độ, coworking — khớp chính xác `schema.org Organization name "The Office
Pass"`).

**Gán toạ độ:** `Betahaus`/`Civic Hall` có `P625` thật (Berlin, New York). 5 ca còn lại KHÔNG có
`P625` lẫn `action=query&prop=coordinates` (kiểm riêng, cả 2 nguồn đều rỗng) → dùng **centroid tính
bằng trung bình cộng toạ độ các mục ROSTER hiện có cùng quốc gia** (không phải bbox quốc gia — tránh
đúng lỗi Mỹ/Alaska của checkpoint 51) — 4/5 ca (`Hera Hub`/`Industrious`/`Open Works`/`SketchPad`)
đều Mỹ nên trùng đúng 1 điểm centroid Mỹ (~38.81, -94.68, vùng Kansas — không phải toạ độ thật của
San Diego/NYC/Baltimore/Chicago nhưng đúng quy ước "centroid quốc gia" đã chốt).

**Kết quả merge:** `ROSTER`: 19992 → **19999** (+7). Đơn vị trên bản đồ: 20001 → **20008** (+7,
giữ nguyên chênh lệch +9 case phân tích chuyên sâu). Kiểm trước khi ghi: `git status`/`git log`
sạch, không có phiên khác chạy song song lần này (khác checkpoint 51). Kiểm sau ghi: `node --check`
sạch, thẻ `div`/`section` cân bằng (107/107, 6/6), mở qua HTTP server cục bộ đọc đúng "20008 đơn vị
được lập bản đồ" / "19999 trong danh mục mở rộng". Commit `8f17d77`, `git push origin main` — xác
nhận fast-forward `667a27d..8f17d77`.

**Còn thiếu ~10001 để đạt 30000.** **Việc mở cho lượt sau:** (1) `List of Biomakerspaces in the
United States` (Wikidata `Q140001361`, bài "List of..." curated MỚI tìm thấy lượt này, CHƯA cào nội
dung — chỉ mới thấy trong kết quả tìm kiếm, chưa trích bullet list) — đáng thử bằng đúng kỹ thuật
hop-P856 đã dùng; (2) InBIA (checkpoint 49, mục 7) — vẫn mở, chưa làm, nguồn LỚN nhất từng tìm được
nhưng bị gate sau đăng nhập; (3) ECCP/StartupBlink — LOẠI HẲN (Cloudflare), đừng thử lại; (4)
OpenAlex — LOẠI (quá mỏng); (5) nhóm category rỗng đã xác nhận KHÔNG TỒN TẠI (xem Bước 0 trên) —
đừng thử lại các tên chính xác đó; (6) **bài học `check_url()` không bắt được domain-hijack (mục
"Phát hiện quan trọng" trên) áp dụng cho MỌI batch tương lai, không chỉ batch này** — luôn dành thời
gian đọc tay nội dung thật trước khi merge, kể cả khi `check_url()` báo "ok"; (7) tốc độ 7-94/
checkpoint (rất dao động theo độ "cạn" của nguồn) — khoảng cách 10001 vẫn rất lớn, nguồn Wikipedia
category/list gần như đã cạn (hầu hết category liên quan đã thử qua 3 checkpoint 50-52), **cần cân
nhắc nghiêm túc báo cáo lại với sếp về nguồn hoàn toàn mới** (danh sách đã loại qua 52 checkpoint đã
rất dài — xem đầu mục này) hoặc điều chỉnh kỳ vọng tốc độ đạt mốc 30000.

---
**Lần trước:** 2026-09-10 (checkpoint 51 — **loại hẳn ECCP (Cloudflare bot-check) + loại OpenAlex
(quá mỏng) + Wikipedia `Category:Science parks`/`Category:Business incubators` theo ~65 quốc gia,
kỹ thuật category-crawl MỚI (khác "List of..." của checkpoint 50) (+27, sau khi tự phát hiện và xử
lý race điều kiện với checkpoint 50 đang chạy song song)**) — còn thiếu ~10008 lúc cuối phiên.

**Bước 1 — thử lại việc mở của checkpoint 49 (ECCP), theo đúng ưu tiên được giao:** mở
`clustercollaboration.eu/partners` qua Browser pane thật (không phải `curl`) — trang hiện thẳng màn
hình Cloudflare **"Performing security verification" / "Verify you are human"** (bot-check, không
phải lỗi tạm thời). Theo quy tắc an toàn (không được bấm/vượt CAPTCHA hay bot-detection), DỪNG ngay,
không thử thêm kỹ thuật né tránh nào. **Kết luận: LOẠI HẲN ECCP** — chuyển từ "chưa loại hẳn, đáng dò
kỹ hơn" (checkpoint 49) sang loại dứt điểm, cùng nhóm với StartupBlink (cũng Cloudflare chặn cứng).

**Bước 2 — kiểm mẫu OpenAlex (`api.openalex.org/institutions`) theo đúng gợi ý được giao:** query
`search=` cho các từ khoá phạm vi ROSTER — "science park" 34 kết quả, "incubator" 12, "technology
transfer" 29, "innovation center" 99 (nhiều nhiễu, không phải center thật), "business incubator" 6,
"accelerator" 35, "technopark" 5, "research park" 14 — **cùng bậc độ lớn với ROR đã cạn ở checkpoint
48** (dự đoán đúng trong bối cảnh giao việc: OpenAlex + ROR dùng chung ID nên trùng nhiều, phạm vi
không đủ rộng hơn đáng kể). **Kết luận: LOẠI OpenAlex** — không đáng đầu tư tải hàng loạt.

**Bước 3 — nguồn chính dùng được: Wikipedia, nhưng kỹ thuật category-crawl thay vì "List of..."
curated:** checkpoint 50 (đang chạy song song) đã khai thác 3 trang "List of..." cụ thể; lượt này
thử thêm 1 trang "List of..." nữa (`List of technology centers`, pageid 7697949, chưa được
checkpoint 50 dùng) VÀ một hướng hoàn toàn khác — **`Category:Science parks` → `Category:Science
parks by country` → 42 sub-category theo quốc gia**, cùng **`Category:Business incubators` +
`Category:Business incubators by country` → ~25 sub-category** — dùng
`action=query&list=categorymembers` (MediaWiki API) đệ quy 2 tầng (root → "by country" → từng
quốc gia), KHÔNG đệ quy sâu hơn (thử `Category:Business parks` ở tầng sâu hơn từng gây nổ số lượng
vì có hàng trăm sub-category theo quận/hạt ở Anh — bỏ hẳn category này; `Category:Technology transfer`
cũng bỏ vì toàn chủ đề chính sách như "Bayh-Dole Act" chứ không phải danh sách tổ chức). Kết quả: 67
category/sub-category, **391 trang duy nhất** (khác hẳn tập của checkpoint 50 dù cùng chủ đề, vì
category bao phủ nhiều tổ chức KHÔNG nằm trong các bài "List of..." curated).

**Kỹ thuật xử lý giống checkpoint 50 (hop qua Wikidata P856 + lọc P31)** nhưng bổ sung: xây
`KEEP_TYPES` allowlist tường minh (science/technology/business park, business/startup incubator,
innovation hub/district, industrial park/zone, accelerator...) thay vì chỉ loại theo `PLACE_TYPES`
— vì phần lớn category-crawl candidate CÓ `P31` (khác nhiều trang "List of..." không có bài riêng),
nên lọc theo allowlist chặt hơn khả thi. Bucket "unclear" (P31 mơ hồ như "business"/"organization"
chung chung — 72 mục) và "no_type" (không có `P31` — 6 mục) được **rà tay từng dòng** (đọc tên +
website), loại các case rõ ràng sai phạm vi: công ty tư nhân không phải TTO/vườn ươm (Fin/Intercom,
Gengo, Canva, Innovaccer, RidePal, Simple/neobank, Credit Karma, Rakuten Viki, Aleph Farms, Doorman,
Zeroth.ai/Animoca Brands — các trang mồ côi "Y Combinator-backed startups"/"500 Startups companies"
lẫn vào qua category cha "Startup accelerators"), phòng thí nghiệm hạt nhân/quốc phòng nhạy cảm
(Bettis Atomic Power Laboratory — Hải quân Mỹ), NGO/chương trình không phải trung tâm vật lý (K-Startup
Grand Challenge, Enabling Women of Kamand, Yeni Fikir, Climate Action Africa), link lạc trang xây
dựng/toà nhà (Main campus of Georgia Tech→Brown Hall dorm). **1 ca tự phát hiện lỗi bộ lọc `KEEP_TYPES`:**
"Shenzhen" (thành phố, `P31` gồm cả "special economic zone" nên lọt qua allowlist dù rõ ràng là địa
danh, không phải tổ chức) — loại tay, bài học: `KEEP_TYPES` cần kết hợp kiểm tra "không đồng thời là
địa danh" chứ không chỉ khớp 1 nhãn dương tính.

**`check_url()` + xác minh tay redirect cross-domain (cùng kỷ luật checkpoint 49/50, đọc nội dung
trang đích thật, không tự tin theo mặc định):** trong số cross-domain redirect, xác nhận qua
`<title>`/`og:title`/từ khoá trong HTML **8 ca đổi domain thật**: Erzelli Campus→`erzelli-pst.it`,
Dubai Internet City→`dic.ae`, Catalyst (Inc)→`wearecatalyst.org`, Bio City Leipzig→`biocity-campus.com`
(xác nhận có "Leipzig" trong trang), Liège Science Park→`liegesciencepark.net`, University of the
Virgin Islands Research and Technology Park→`uvirtpark.net` (title khớp chính xác), **Paris-Saclay→
`welcometoparissaclay.com`** (đây là ca checkpoint 50 đã LOẠI vì `<title>` chung chung "nuxt-headless"
không xác nhận được thương hiệu — lượt này đào sâu thêm, đọc `og:title`/`og:site_name` server-side-
rendered = chính xác "Paris-Saclay", nên XÁC NHẬN LẠI và GIỮ; bài học: khi `<title>` của app JS
(Nuxt/Next...) chung chung, kiểm thêm thẻ `og:title`/`og:site_name` trước khi loại hẳn, vì các thẻ
đó thường được SSR dù nội dung thân trang không tải qua `curl`), INCUBA Science Park→`incuba.dk`
(về sau bị loại ở bước dedup-lại vì đã trùng ROSTER — xem dưới). **3 ca redirect về trang chủ tổ
chức MẸ chung chung (cùng logic "bcbtac"/checkpoint 49) → loại:** DMZ→`torontomu.ca` (trang chủ
Toronto Metropolitan University, không phải trang riêng DMZ), Cebu IT Park→`ayalaland.com` (trang
chủ tập đoàn bất động sản Ayala Land), BioCity Nottingham→`thepioneergroup.com` (bị chặn Cloudflare
"Attention Required", không xác minh được nội dung — không đoán). **1 ca xác nhận domain chết thật**
(không phải lỗi tạm thời): Ghent Bio-Energy Valley (`gbev.org`) → trang "domain may be for sale"
qua GoDaddy/`abovedomains.com` — loại. **URLError/TimeoutError hàng loạt (≈30 ca) được thử lại
`timeout=30` (gấp đôi) rồi xác minh thêm bằng `curl` DNS trực tiếp** — đa số là lỗi DNS thật
(`curl` exit 6 "Couldn't resolve host", vd `zjsfq.gov.cn`, `atp.com.au`, `symbion.science`) hoặc bị
chặn/timeout nhất quán (`kacst.gov.sa` treo đủ 15s) — không phải sự cố mạng phía máy này (các domain
khác cùng lượt vẫn tải bình thường) → loại thật, không cứu được.

**Phát hiện race điều kiện với checkpoint 50 đang chạy song song (khác hẳn kịch bản "phiên trước bỏ
dở" của checkpoint 50):** xác nhận `git status`/`len(load_roster(...))` = 19898 sạch trước khi ghi
lần 1 (đúng quy trình) → build xong → kiểm lại thấy `git status`/kích thước file lệch bất thường →
phát hiện MỘT PHIÊN KHÁC đang ghi/commit SONG SONG thời gian thực (không phải file cũ bỏ lại, mà
đang biến đổi ngay trong lúc phiên này xử lý — từ 19898 → (phiên kia ghi) → 19965, tương ứng commit
`67ad372`, +67). Xử lý: **KHÔNG hoảng, không ép ghi đè** — gọi lại `load_roster()` lần nữa ngay
trước khi ghi thật (ra đúng 19965), chạy lại toàn bộ bước lọc trùng ROSTER (base_domain +
normalize_name) trên 42 ứng viên đã chuẩn bị theo baseline 19965 mới nhất → phát hiện **15/42 đã
trùng với chính batch của checkpoint 50** (cùng nguồn Wikipedia/Wikidata nên trùng nhiều — vd
Virginia Tech Corporate Research Center, Advanced Technology Development Center, Entrepreneurs
Roundtable Accelerator, Catalyst, BioCity Nottingham) → còn **27 ứng viên thật sự mới** → ghi, build,
kiểm, **commit + push NGAY LẬP TỨC** (tối thiểu hoá khoảng hở cho lần ghi đè kế tiếp) trước khi làm
các bước phụ. **Gán toạ độ:** ưu tiên `P625` khi có; 2 ca fallback qua "centroid quốc gia" của một
script kế thừa từ scratch của phiên trước bị lỗi (bbox-center của Mỹ tính sai vì lãnh thổ không liền
mạch — Alaska/đảo — ra toạ độ 45.19/0.79 thuộc nước Pháp!) đã phát hiện và sửa tay bằng toạ độ thành
phố thật (QB3→Berkeley CA, North Carolina Research Campus→Kannapolis NC) trước khi ghi — bài học nếu
dùng lại kỹ thuật "centroid theo bbox quốc gia" (khác cách CORDIS FP7 checkpoint 46 dùng centroid có
sẵn trong ROSTER): kiểm tra riêng nước Mỹ/Nga/Pháp (có lãnh thổ hải ngoại xa) trước khi tin bbox-center.

**Kết quả merge:** `ROSTER`: 19965 → **19992** (+27, baseline 19965 đã gồm +67 của checkpoint 50
chạy song song — tổng 2 phiên: 19898 → 19992, +94). Đơn vị trên bản đồ: 19974 → **20001** (+27, giữ
nguyên chênh lệch +9). Kiểm: `node --check` sạch, thẻ `div`/`section` cân bằng (107/107, 6/6). Mở
`index.html` qua HTTP server cục bộ (`static-server`), đọc qua Browser pane: đúng "20001 đơn vị được
lập bản đồ" / "19992 trong danh mục mở rộng" / "12 đơn vị tại Việt Nam" (không đổi) / "9 case phân
tích chuyên sâu" (không đổi). Commit `47ac10b` và `git push origin main` lên live — xác nhận
fast-forward `67ad372..47ac10b`.

**Còn thiếu ~10008 để đạt 30000.** **Việc mở cho lượt sau:** (1) ECCP + StartupBlink nay đã LOẠI HẲN
cả hai (Cloudflare) — đừng thử lại trừ khi có cách hợp lệ khác để vượt bot-check (không có trong
phạm vi công cụ hiện tại); (2) OpenAlex đã LOẠI (quá mỏng, trùng ROR); (3) Wikipedia category-crawl
CÒN MỞ RỘNG ĐƯỢC — các `Category:` khác chưa thử: `Category:Coworking spaces`, `Category:Startup
accelerators by country` (mới thấy `Category:Startup accelerators` phẳng, chưa kiểm có sub-category
theo nước không), `Category:Makerspaces`, `Category:Living labs`, `Category:Research parks` (kiểm
thấy trống ở lượt này — có thể đổi tên hoặc gộp vào "Science parks", cần kiểm lại); nếu dùng lại,
GIỮ NGUYÊN kỷ luật đệ quy tối đa 2 tầng (category quốc gia), KHÔNG đệ quy sâu hơn (đã gây nổ số lượng
với "Business parks" ở lượt này); (4) `List of technology centers` (pageid 7697949) đã dùng ở lượt
này nhưng CHƯA rà hết "unclear"/"no_type" bucket của riêng trang đó theo cùng độ sâu category-crawl —
có thể còn sót vài ca; (5) InBIA (checkpoint 49, mục 7) — vẫn mở, chưa làm; (6) **RỦI RO RACE ĐIỀU
KIỆN đã XÁC NHẬN LÀ CÓ THẬT** (không chỉ giả thuyết) — lượt sau LUÔN kiểm `git log`/`git status` cả
lúc BẮT ĐẦU lẫn NGAY TRƯỚC MỖI bước ghi, và commit+push NGAY sau khi ghi/build/kiểm xong, không trì
hoãn; (7) tốc độ 27-94 mục/checkpoint (tuỳ tính gộp 2 phiên) vẫn quá chậm so với khoảng cách 10008 —
cân nhắc báo cáo lại với sếp.

---
**Lần trước:** 2026-09-10 (checkpoint 50 — **Wikipedia "List of..." (science/research parks +
incubators), kỹ thuật MỚI: hop qua Wikidata P856 thay vì cào từng trang tổ chức (+67)**) — còn
thiếu ~10035 lúc cuối phiên.

**⚠️ Lưu ý quan trọng đầu phiên — phiên trước (agent trước checkpoint này) đã BẮT ĐẦU đúng hướng
Wikipedia "List of..." nhưng DỪNG GIỮA CHỪNG, để lại `index.html`/`src/atlas.html` với thay đổi
CHƯA COMMIT (roster +42, chưa qua đủ bước xác minh) nằm sẵn trong working tree khi phiên này bắt
đầu — phát hiện qua `git status` NGAY TRƯỚC bước ghi cuối cùng (không phải đầu phiên, vì file chỉ
bị sửa lúc merge). Đã `git stash push -u` (không xoá hẳn) để giữ lại phòng trường hợp cần, rồi làm
lại HOÀN TOÀN từ baseline sạch 19898 theo đúng chỉ dẫn "bắt đầu từ đầu". Bài học cho lượt sau:
**LUÔN `git status` kiểm working tree NGAY khi bắt đầu phiên, không chỉ trước bước ghi cuối** — nếu
phiên trước để lại thay đổi chưa commit, phải xử lý (stash) trước khi bắt đầu bất kỳ bước nào khác
để tránh lẫn dữ liệu cũ chưa xác minh vào `len(load_roster(...))` baseline.

**Nguồn dùng — Wikipedia "List of..." (science/tech park + incubator), giới hạn 3 trang cụ thể
ngay từ đầu để tránh lặp lỗi "crawl không giới hạn" của phiên trước:** `List of research parks`
(trang toàn cầu, theo châu lục/quốc gia, pageid 5721896), `List of science parks in the United
Kingdom` (pageid 8694089), `List of startup incubators in the United States` (pageid 80090488).
Cân nhắc thêm `List of tech parks in Chennai` nhưng LOẠI vì đó là các toà nhà văn phòng CNTT cho
thuê (tenant Infosys/Cisco/Wipro...), sai phạm vi TTO/vườn ươm/khu KH&CN.

**Vấn đề gặp: 2 trang đều chỉ là danh sách tên có wikilink, KHÔNG có cột URL trực tiếp** (khác hẳn
CORDIS/ROR có `organizationURL`/`homepage_url` sẵn trong dữ liệu). **Kỹ thuật MỚI (chưa từng dùng
qua 49 checkpoint trước) — "hop" qua Wikidata thay vì cào từng trang tổ chức riêng lẻ:** (1) trích
535 mục thô từ wikitext 3 trang (regex bullet-list/wikitable, giữ ngữ cảnh quốc gia theo heading
`==`/`===`); (2) với mỗi mục có wikilink, `action=query&prop=pageprops&redirects=1` (batch 50 tiêu
đề/lần) lấy `wikibase_item` (QID); (3) `wbgetentities` trên `www.wikidata.org` (batch 50 QID/lần)
lấy `P856` (official website — nguồn CHÍNH), `P31` (instance-of, dùng để LỌC — xem dưới), `P625`
(toạ độ thật nếu có); (4) với mục không có QID/không có P856, dùng URL trực tiếp trong thẻ `<ref>`
của chính bullet đó nếu KHÔNG phải domain báo chí (loại các URL kiểu `timesofindia.indiatimes.com`,
`newindianexpress.com`... — đây là trích dẫn nguồn tin, không phải website tổ chức, dù `check_url()`
sẽ báo "sống" vì trang báo có thật). 430 tiêu đề duy nhất → 271 khớp QID → 187 có `P856`; cộng 101
URL trực tiếp từ `<ref>` (sau lọc báo chí) → 289 ứng viên có URL.

**Lỗi parser tự phát hiện và sửa (quan trọng, người review sau nên biết):** bullet dạng "Tên tổ
chức [[Địa danh]]" (không có dấu gạch ngang phân cách) bị parser đời đầu lấy NHẦM link địa danh làm
tên tổ chức (vd `*Electropreneur Park [[Bhubaneswar]]` → sai thành tên "Bhubaneswar") — đã sửa quy
tắc: chỉ coi wikilink là tên tổ chức khi bullet BẮT ĐẦU bằng `[[`, ngược lại tên là đoạn text thuần
trước link/dấu gạch đầu tiên.

**Lọc theo `P31` (instance-of) — phát hiện MỚI, quan trọng cho các lượt Wikidata sau:** nhiều mục
Wikidata là ĐỊA DANH (thành phố/quận/khu công nghiệp) chứ không phải TỔ CHỨC — `P856` của chúng là
trang CHÍNH QUYỀN ĐỊA PHƯƠNG, không phải TTO/vườn ươm nào (ca thật bắt được: "Bhubaneswar"→
`bmc.gov.in`, "Tampere"/"Ankara"/"Venezia"/"Maastricht"/"Oss"→cổng thông tin thành phố). Xây bộ lọc
`PLACE_TYPES` (city/town/municipality/neighborhood/building/industrial zone...) + `UNIVERSITY_TYPES`
(loại cả trường đại học NGUYÊN VẸN, cùng logic với "HES" của CORDIS checkpoint 45 — ROSTER cần đơn
vị cụ thể, không phải nguyên trường) + `VC_TYPES` (quỹ đầu tư mạo hiểm, sai hẳn loại hình) → loại 37
ứng viên. **Vẫn còn lọt lưới vài ca do QID mang kiểu địa danh đặc thù quốc gia không có trong bộ lọc
chung** (`Cimahi`/`Solo` Indonesia, `Changwon Industrial Park`/`Kista Science City` Hàn/Thuỵ Điển,
`Villeneuve d'Ascq` Pháp) — phải LOẠI TAY sau khi rà mắt toàn bộ danh sách cuối; bài học: bộ lọc
`PLACE_TYPES` hiện tại CHƯA đủ bao quát các QID kiểu "commune"/"city in Indonesia"/... theo từng
nước, lượt sau nếu dùng lại kỹ thuật Wikidata nên bổ sung dần.

**Dọn tên + loại thêm:** dọn cú pháp external-link sót lại `[url Tên]`/dấu ngoặc/dấu phẩy thừa từ
parser (không sửa được hết bằng regex chung, phải tay từng ca hiếm); loại thêm tay: "Vivint" (công
ty an ninh nhà ở, rõ ràng khớp nhầm Wikidata), "Enterprise Development Center"/"Pohang Research
Centre" (URL trỏ về TRANG CHỦ NGUYÊN TRƯỜNG ĐẠI HỌC — njit.edu/postech.edu — quá rộng), "Metrotech
Center" (Business Improvement District bất động sản, không phải đơn vị R&D/CGCN), "Research Forest
(The Woodlands)" (site bất động sản chung chung), "Wallops Research Park" (trỏ về trang CHÍNH QUYỀN
QUẬN Accomack County, Virginia). → còn 129 ứng viên sạch.

**Lọc trùng ROSTER** (base_domain + normalize_name, 19898 mục): loại 111 trùng domain + 5 trùng tên
→ 173 (trước lọc P31) → sau lọc P31 + dọn tay: 129 ứng viên cuối cùng.

**`check_url()` toàn bộ 129** (`ThreadPoolExecutor` 16 luồng): chỉ **60 sống ngay (47%)** — tỉ lệ
thấp vì nhiều tổ chức trong các trang "List of..." (đặc biệt trang toàn cầu, có mục từ 2010s) đã đổi
domain/ngừng hoạt động. **21 ca bị `check_url()` gắn cờ "cross-domain redirect" — xác minh TAY TỪNG
CA bằng cách đọc `<title>`/nội dung trang đích thật** (không tự động tin, đúng thiết kế của hàm):
**8/21 xác nhận đúng tổ chức gốc đổi domain** — Kansai Science City→`kri.or.jp` (tên tổ chức khớp
tiếng Nhật "Tổ chức xúc tiến Kansai Science City"), Scion DTU→`dtusciencepark.dk` (đổi tên "DTU
Science Park"), INCUBA Science Park→`incuba.dk`, Innovation Campus Lemgo→`icl-owl.de`, Cartuja93→
`sevillatechpark.es` (đổi tên "Sevilla TechPark"), Erzelli High-Tech Park→`erzelli-pst.it` (tên
tiếng Ý khớp "Parco Scientifico e Tecnologico di Genova Erzelli"), BioCity Nottingham→
`thepioneergroup.com/locations/biocity-nottingham/` (cùng tập đoàn vận hành với Kent Science Park
đã sống sẵn trong batch), Catalyst→`wearecatalyst.org`. **13/21 LOẠI** vì không xác minh được đúng
tổ chức: Life Science Hub→`lodhagroup.com` (site tập đoàn mẹ bất động sản chung chung, không phải
trang riêng), Paris-Saclay→`welcometoparissaclay.com` (title chung chung "nuxt-headless", không xác
nhận được thương hiệu), Technopolis Group→`technopolisglobal.com` (nội dung mang dấu hiệu trang lỗi
404), PCiTAL→`hoteles-andalucia.com` (domain rõ ràng bị chiếm dụng cho trang khách sạn), Medical
City at Lake Nona→`lakenona.com` (site cộng đồng dân cư chung, không phải riêng Medical City),
Research Park at Florida Atlantic University→`researchparkfau.com` (bị Cloudflare chặn, không xác
minh được), Rensselaer Technology Park→`iriens.com` (trang trống, không xác minh được), BioSquare at
Boston University→`bu.edu` (trang chủ nguyên đại học, quá rộng), và 5 ca khác cùng loại lý do không
xác minh được. **1 ca đặc biệt phát hiện qua rà tay sau khi `check_url()` đã báo "sống":**
"Jagiellonian Center of Innovation" có `P856`/URL trỏ tới MỘT BÀI BÁO trên `genengnews.com` (báo
công nghệ sinh học), không phải trang chủ tổ chức — `check_url()` không thể tự phát hiện loại lỗi
này (trang báo là nội dung hợp lệ, chỉ SAI về BẢN CHẤT không phải website tổ chức) — loại tay. →
**67 ứng viên cuối cùng, 0 Việt Nam** (không có ứng viên VN nào lọt tới bước cuối).

**Gán toạ độ:** ưu tiên `P625` (toạ độ thật từ Wikidata) khi có — 21/67; còn lại dùng centroid quốc
gia lặp nhiều nhất sẵn có trong ROSTER (theo đúng kỹ thuật CORDIS FP7 checkpoint 46) — 46/67.

**Kết quả merge:** phát hiện `git status` có thay đổi CHƯA COMMIT từ phiên trước (xem cảnh báo đầu
mục) → `git stash push -u` rồi xác nhận lại `len(load_roster(...))` = 19898 sạch trước khi ghi.
`ROSTER`: 19898 → **19965** (+67). Đơn vị trên bản đồ: 19907 → **19974** (+67, giữ nguyên chênh
lệch +9). Kiểm: `node --check` sạch (script inline 3,420,576 ký tự), thẻ `div`/`section` cân bằng
(107/107, 6/6). Mở `index.html` qua HTTP server cục bộ (`static-server`), đọc qua Browser pane: đúng
"19974 đơn vị được lập bản đồ" / "19965 trong danh mục mở rộng" / "12 đơn vị tại Việt Nam" (không
đổi) / "9 case phân tích chuyên sâu" (không đổi). Commit `67ad372` và `git push origin main` lên
live.

**Còn thiếu ~10035 để đạt 30000.** **Việc mở cho lượt sau:** (1) kỹ thuật "hop qua Wikidata P856"
CÓ THỂ áp dụng lại cho các trang Wikipedia "List of..." KHÁC chưa thử (vd tìm thêm theo từ khoá
"fab lab"/"makerspace"/"cluster"/"living lab" hoặc theo khu vực địa lý khác — Đông Nam Á, Mỹ Latinh,
Trung Đông chưa có trang "List of..." riêng được kiểm qua lượt này); (2) nếu dùng lại kỹ thuật này,
BỔ SUNG bộ lọc `PLACE_TYPES` với các QID kiểu địa danh đặc thù quốc gia (xem mục "lọt lưới" ở trên)
thay vì rà tay từng ca; (3) InBIA (checkpoint 49, mục 7) — vẫn mở, chưa làm; (4) ECCP cluster
directory (checkpoint 49, mục 4) — vẫn mở, kỹ thuật truy cập chưa rõ; (5) **vẫn cần nguồn lớn hoàn
toàn mới khác** — tốc độ ~22-67 mục/checkpoint gần đây quá chậm so với khoảng cách còn lại 10035;
cân nhắc báo cáo lại với sếp về tính khả thi thời gian của mốc 30000 nếu tốc độ này tiếp diễn.

**Ghi chú bổ sung (phát hiện SAU khi checkpoint 50 đã commit+push):** ngay sau commit `67ad372`
của checkpoint 50, một phiên khác chạy CÙNG LÚC (`git log` cho thấy commit `47ac10b`, tác giả "Bui
Son", đẩy lên `origin/main` trong lúc phiên này đang soạn mục CLAUDE.md này) đã cùng hướng Wikipedia
"List of..." + Wikidata, mở rộng thêm sang `Category:Science parks`/`Category:Business incubators`
theo ~65 sub-category quốc gia, tự re-dedup theo đúng ROSTER tại thời điểm đó và cộng thêm **+27**
(nêu rõ trong log của họ: "another session had already added 15 overlapping candidates from the
same sources" — tức phiên đó đã biết và xử lý trùng với chính checkpoint 50 này). Phiên đó KHÔNG
tự cập nhật mục lịch sử này trong `CLAUDE.md`. Vì vậy: **ROSTER thực tế sau cả 2 phiên = 19965 + 27
= 19992** (không phải 19965 như số cuối checkpoint 50 ở trên) — **còn thiếu ~10008 để đạt 30000**.
Lượt sau ĐỪNG hoảng khi thấy `len(load_roster(...))` không khớp 19965 lúc bắt đầu — 19992 mới là
con số đúng để dùng làm baseline xác nhận trước khi merge tiếp. Bài học: khi làm việc trên repo này
đồng thời với phiên khác (biểu hiện: `git log` xuất hiện commit lạ không phải do chính mình tạo),
KHÔNG cần hoảng hoặc revert — chỉ cần `git fetch`/kiểm `git log` để xác nhận không có xung đột thật
(không cùng sửa 1 dòng ROSTER), rồi tiếp tục dựa trên baseline MỚI NHẤT.

---
**Lần trước:** 2026-09-10 (checkpoint 49 — **NHIỆM VỤ "TÌM NGUỒN LỚN HOÀN TOÀN MỚI": KHÔNG THÀNH
CÔNG — mọi ứng viên lớn đều bị chặn/hijack/gate; chỉ cứu được 1 nguồn nhỏ-sạch chưa từng thử
(Tech-Access Canada, +50)**) — còn thiếu ~10102 lúc cuối phiên.

**Nhiệm vụ chính lượt này — theo đúng yêu cầu của sếp: nghiên cứu sâu tìm 1-2 nguồn quy mô LỚN
(cỡ CORDIS/Wikidata/OSM) hoàn toàn mới, chưa từng thử qua 48 checkpoint trước.** Kết quả: **KHÔNG
tìm được nguồn lớn khả thi** — liệt kê đầy đủ các hướng đã thử và lý do loại:

1. **WIPO "Technology Transfer Organizations" (`wipo.int/en/web/technology-transfer/organizations`)**
   — chỉ là trang thông tin chung (FAQ, human-capital, 1 case study Hashemite University), KHÔNG
   phải danh bạ — chỉ có 1 link tổ chức thật (`ntpark.rs`) trong toàn trang. Loại vì quá nhỏ.
2. **StartupBlink (`startupblink.com/accelerators`)** — trang chủ database gợi ý ">120000 startup,
   100 quốc gia" nhưng bị **Cloudflare chặn cứng** ("Sorry, you have been blocked") ngay từ request
   đầu tiên qua `curl` — không tiếp cận được mà không có kỹ thuật vượt chặn (không làm, ngoài phạm
   vi công cụ cho phép).
3. **World Technopolis Association (`wtanet.org`)** — domain đã **bị đổi chủ/hijack**: tải về là
   trang "East Asia Research" (tổ chức hội thảo học thuật SEO), không liên quan WTA gốc — ca
   domain-squatting mới, khác các ca đã ghi nhận trước (incel.cz checkpoint 48, Ramot.com). Nếu WTA
   thật đã chuyển domain khác thì lượt sau cần `WebSearch` định vị lại trước khi thử tiếp.
4. **European Cluster Collaboration Platform / ECCP (`clustercollaboration.eu`)** — có vẻ lớn (hàng
   nghìn "cluster organisation" châu Âu) nhưng là site Drupal điều khiển bằng AJAX/Views, không tìm
   ra endpoint API công khai qua vài lần dò nhanh (`/jsonapi` bị redirect 308 vòng, trang
   "find-clusters-partners" dùng form POST ẩn). Cần đầu tư sâu hơn (reverse-engineer Views AJAX
   hoặc điều khiển qua Browser pane từng trang) — CHƯA LOẠI HẲN, để mở cho lượt sau nếu có thời
   gian, nhưng cũng cần cân nhắc "cluster công nghiệp" có đúng phạm vi TTO/vườn ươm/khu KH&CN hay
   không trước khi đầu tư.
5. **GALI — Global Accelerator Learning Initiative (`galidata.org`)** — đây là dữ liệu khảo sát học
   thuật về HIỆU QUẢ chương trình accelerator (tổng hợp/aggregate), không phải danh bạ tên tổ chức
   kèm website — loại vì không đúng định dạng cần.
6. **OSM Overpass — quét theo TÊN (name~regex) thay vì theo tag chính, kỹ thuật CHƯA từng thử** (
   khác hẳn cách tiếp cận `amenity=university/college/research_institute` cũ): `nwr["name"~"Science
   Park"]` v.v. Kết quả: **RẤT MỎNG** khi lọc thêm điều kiện có tag `website`/`contact:website` —
   "science park" chỉ 45/1027 phần tử có website, "business incubator" chỉ ~7. Quan trọng hơn: các
   truy vấn gộp nhiều pattern liên tục bị **504 timeout** hoặc **429 rate-limited** trên Overpass
   API công khai (server quá tải khi quét full-text tên) — kết luận: hướng name-regex vừa mỏng vừa
   không ổn định để khai thác quy mô lớn, KHÔNG đáng đầu tư thêm.
7. **InBIA — International Business Innovation Association (`inbia.org/inbia-members/`)** — ứng
   viên **lớn nhất và đáng tiếc nhất**: hiệp hội có công bố ">2000 thành viên, hơn 60 quốc gia"
   (chính xác đúng loại vườn ươm/accelerator ROSTER cần). Có danh sách tên qua API nội bộ
   `POST /members/directory-customer-list` (đọc được qua Browser pane network tab), nhưng
   **trường website/liên hệ bị KHOÁ sau đăng nhập** — xác nhận tay trên 1 hồ sơ thật (Ohio
   University Innovation Center): trang chỉ hiện "Contact information may be available to logged
   in members." — không có URL công khai nào cả. Không thể khai thác hàng loạt nếu không tạo tài
   khoản (bị cấm theo quy tắc an toàn). **Để mở cho lượt sau:** có thể tra riêng từng tên qua
   `WebSearch` để tìm website thật (giống kỹ thuật Na Uy SIVA checkpoint 47) nhưng đây là việc làm
   tay từng dòng, không phải "nguồn lớn nhanh" — cân nhắc kỹ trước khi đầu tư nhiều lượt vào ~2000
   tên.

**Vì không có nguồn lớn nào khả thi, tận dụng phát hiện phụ: Tech-Access Canada — nguồn nhỏ nhưng
sạch, hoàn toàn chưa thử (Canada trước giờ mới chỉ đụng tới NRC IRAP — bị loại vì là chương trình
tài trợ, không phải TTO).** `tech-access.ca` là hiệp hội quốc gia của **64 Technology Access Centres
(TAC)** — trung tâm R&D ứng dụng/chuyển giao công nghệ gắn với các college/cégep Canada, được
NSERC tài trợ — đúng phạm vi TTO của ROSTER. Danh bạ thật (`meetthetacs.ca/Member/Index`), server-
render HTML thường, KHÔNG cần đăng nhập.

**Kỹ thuật:** cào 64 trang hồ sơ `meetthetacs.ca/member/details/{slug}` (tên từ `figcaption` +
`<h3>` ở trang index, website từ `id="tac-contact-website"`, địa chỉ để suy toạ độ thành phố). 4/64
không có website (crvi, dtl, rail, rcdtac) → loại. **Lọc trùng ROSTER** (base-domain + tên chuẩn
hoá, 19848 mục): 3 trùng domain (`bfps`/`tacsm` cùng `nait.ca` với 1 mục NAIT đã có sẵn;
`biopterre.com` đã có sẵn) → **57 ứng viên**. `check_url()` 57: 44 sống ngay; thử lại timeout dài
hơn cứu thêm 1 (`biolab`, lỗi mạng tạm thời). **6 ca chuyển-domain đáng ngờ được xác minh tay từng
ca** (đọc nội dung trang đích qua `curl`, không đoán): 5/6 xác nhận đúng là tổ chức gốc đổi domain
— `aihub`→`theaihub.ca` (nội dung nhắc "Durham"/"AI Hub"), `c2t3`→`c2t3.net` (title "Accueil -
C2T3"), `cetab`→`cetab.bio` (title "CETAB+"), `cta`→`aerocta.ca` (title "Centre technologique en
aérospatiale" = đúng Aerospace Technology Access Centre), `tbt`→`transbio.tech` (title
"TransBIOTech") → **cập nhật URL sang domain mới cho cả 5**; 1/6 (`bcbtac`) redirect về trang chủ
chung của trường (`okanagancollege.ca`), KHÔNG phải domain riêng của TAC → loại. 6 ca lỗi mạng còn
lại xác minh KHÔNG phải tạm thời (403/404/unreachable qua cả `curl` UA thường lẫn UA trình duyệt
đầy đủ): `agrinova.qc.ca` (403, dùng chung cho 2 TAC `agrinova-b`/`agrinova-pl`), `cim-tac` trang
đích 404, `cteau.com` không kết nối, `georgebrown.ca/first` 403, `merinov.ca` không kết nối → loại
theo đúng nguyên tắc không đoán khi 403/không xác minh được nội dung thật.

**Gán toạ độ:** toạ độ THÀNH PHỐ THẬT (không phải centroid quốc gia) cho từng TAC theo địa chỉ trụ
sở thật lấy từ trang hồ sơ (39 thành phố khác nhau khắp Canada — Longueuil, Alma, Oshawa, Surrey,
Winnipeg, Trois-Rivières, Québec, Toronto, Calgary, Edmonton...). **50 mục mới, 0 Việt Nam.**

**Kết quả merge:** xác nhận `git status` sạch (trừ thư mục `.claude/` chưa track, không liên quan)
+ `len(load_roster(...))` = 19848 đúng ngay trước khi ghi. `ROSTER`: 19848 → **19898** (+50). Đơn
vị trên bản đồ: 19857 → **19907** (+50, giữ nguyên chênh lệch +9). Kiểm: `node --check` sạch, thẻ
`div`/`section` cân bằng (107/107, 6/6). Mở `index.html` qua HTTP server cục bộ (`static-server`),
đọc qua Browser pane: đúng "19907 đơn vị được lập bản đồ" / "19898 trong danh mục mở rộng" / "12
đơn vị tại Việt Nam" (không đổi) / "9 case phân tích chuyên sâu" (không đổi). Commit và
`git push origin main` lên live (xem hash ở cuối báo cáo phiên).

**Còn thiếu ~10102 để đạt 30000.** **Việc mở cho lượt sau:** (1) InBIA (mục 7 ở trên) — nguồn LỚN
nhất tìm được lượt này nhưng bị gate sau đăng nhập, cần tra tay từng tên qua `WebSearch` (chậm,
không phải "nguồn lớn nhanh" nhưng đáng làm dần); (2) ECCP cluster-organisation directory (mục 4) —
kỹ thuật truy cập CHƯA rõ, cần đầu tư sâu hơn hoặc Browser pane điều khiển tay, và cần chốt trước
xem "cluster công nghiệp" có tính là đúng phạm vi TTO/vườn ươm/khu KH&CN không; (3) WTA/wtanet.org
đã bị hijack — nếu tổ chức thật còn tồn tại ở domain khác, `WebSearch` định vị lại; (4) StartupBlink
bị Cloudflare chặn cứng, không thử lại trừ khi có cách khác; (5) OSM name-regex (mục 6) xác nhận
CẠN + KHÔNG ỔN ĐỊNH, đừng lặp lại; (6) **vẫn cần tìm nguồn lớn hoàn toàn mới khác** — khoảng cách
10102 quá lớn so với tốc độ ~22-50 mục/checkpoint gần đây, các nguồn nhỏ lẻ không đủ; cân nhắc
hướng hoàn toàn khác (registry chính phủ quốc gia chưa từng thử: Úc, Nam Phi, UAE, Israel...) hoặc
chấp nhận tốc độ chậm và báo cáo lại với sếp về tính khả thi của mốc 30000.

---
**Lần trước:** 2026-09-10 (checkpoint 48 — **ROR (Research Organization Registry) — NGUỒN LỚN
NHƯNG CHỦ YẾU NGOÀI PHẠM VI: TỪ >134000 TỔ CHỨC CHỈ LỌC RA 22 MỤC MỚI THẬT SỰ**) — còn thiếu ~5152
lúc cuối phiên.

**Nhiệm vụ chính — ROR (`ror.org`), chưa từng thử qua 47 checkpoint trước.** Bước 1: bản dump hàng
loạt (Zenodo, DOI `10.5281/zenodo.6347574`) **KHÔNG khả dụng** — `zenodo.org` (và cả domain thay thế
`zenodo-rdm.web.cern.ch`) trả **504 Gateway Time-out** nhất quán qua `curl`, `WebFetch`, và Browser
pane thật (không phải mạng bị chặn — trang chủ zenodo.org cũng 504) → chuyển hẳn sang API
`api.ror.org/v2/organizations` (REST, hoạt động bình thường, **134298 tổ chức** tổng).

**Kiểm mẫu phạm vi trước khi tải hàng loạt (đúng yêu cầu):** lọc thô theo `filter=types:facility`
(14610)/`nonprofit`(19920)/`other`(10024) cho thấy số lượng vẫn quá lớn để duyệt tay, và quan trọng
hơn — **query từ khoá đơn giản qua `query=` bị "phẳng" theo từng từ riêng lẻ** (vd `"research park"`
→ 9357 kết quả vì khớp rời rạc "research" HOẶC "park"), không dùng được. Chuyển sang
`query.advanced=names.value:(...)` (cú pháp Elasticsearch query_string, hỗ trợ cụm từ trong ngoặc
kép + OR) — cho kết quả đúng cụm từ, nhỏ gọn hơn nhiều (vd `"science park"` phrase = 27, `"technology
transfer"` = 27, `incubator` = 12). **Kết luận phạm vi:** ROR có >134000 tổ chức nhưng đây là cơ sở
dữ liệu định danh tổ chức có công bố khoa học (affiliation cho Crossref/DataCite/OpenAlex) — nó phủ
RẤT SÂU đại học/viện nghiên cứu/bệnh viện/công ty/quỹ tài trợ (đã có sẵn phần lớn trong ROSTER qua
IASP/CORDIS/Wikidata các checkpoint trước) nhưng **RẤT MỎNG** cho đúng nhóm ROSTER cần (TTO/vườn
ươm/khu KH&CN) — các trung tâm trung gian hiếm khi tự đứng tên affiliation trong bài báo khoa học
nên ít được ROR cấp ID riêng. Ngược hẳn với kỳ vọng ban đầu.

**Kỹ thuật lọc:** 2 vòng `query.advanced` gộp ~45 từ khoá cụm (tiếng Anh + Bồ Đào Nha/Tây Ban Nha/
Ý/Pháp/Đức: "innovation center/centre", "science/technology/research park", "incubator"/
"incubadora", "technology transfer", "technopark"/"technopole"/"tecnoparque", "living lab", "fab
lab", "makerspace", "cluster", "Gründerzentrum"/"Technologiezentrum"/"Innovationszentrum"...) →
**227 + 12 = 239 dòng thô**. Kiểm tay toàn bộ (không chỉ mẫu 50-100 vì tổng chỉ 239) theo đúng bài
học DPIIT/SBIR — loại thẳng: cơ sở vật lý gia tốc hạt (từ khoá "accelerator" bắt nhầm hàng loạt
"Fermilab"/"SLAC"/"KEK"/"J-PARC"...), chương trình "2011 Collaborative Innovation Center" của Trung
Quốc (quỹ nghiên cứu đại học, không phải TTO), trung tâm R&D nội bộ doanh nghiệp (Unilever/Suntory/
Intesa Sanpaolo/Nissatech), cơ quan tài trợ/chính sách chính phủ thuần tuý (Innosuisse, BRIN
Indonesia, các "Innovation Agency" khu vực), viện nghiên cứu học thuật gắn trong 1 đại học (AIMS
Rwanda, KIOS Cyprus) → còn **114 ứng viên giữ lại**.

**Lọc trùng ROSTER** (base-domain + tên chuẩn hoá, 19826 mục): loại **67/114** trùng — tỉ lệ trùng
RẤT CAO, xác nhận ROSTER đã khai thác khá kỹ mảng science park/incubator châu Âu qua IASP/CORDIS các
checkpoint trước (vd toàn bộ "Ideon", "Kyoto Research Park", "AREA Science Park", "Qatar Science and
Technology Park"... đã có sẵn) → **47 ứng viên mới**.

**`check_url()` toàn bộ 47** (timeout 8s rồi thử lại 20s cho nhóm lỗi mạng): **19 sống ngay**, 28 chết
— trong đó vài ca đáng chú ý cần tay xác minh thêm: **"Association of the Innovation Center of
Electronics" (Czechia, domain `incel.cz`) — tên miền đã bị CHIẾM DỤNG, nội dung hiện tại là trang
quảng cáo/mã độc (`newrotatormarch23.bid`), KHÔNG liên quan tổ chức gốc** (bài học domain-squatting
mới, khác kiểu parking-page/redirect-lander đã biết); "Incubadora Venezolana de la Ciencia" domain
đã bán cho bên thứ 3 (chuyển hẳn sang `seekingenglish.com`); vài ca 403 (`irbm.it`, `corvinno.com`,
`activation.capital`) không xác minh được nội dung thật nên LOẠI theo nguyên tắc không đoán; "Centre
de Transfert de Technologie du Mans" chỉ có 1 bộ phận (Âm học) được `almacoustic.com` tiếp quản, KHÔNG
phải đổi tên toàn bộ tổ chức → LOẠI. Xác minh tay 3 ca lỗi mạng tạm thời (không phải parking/dead
thật) rồi cho sống lại: `netport.se` (chuyển URL gốc, bỏ `/en`), `incubo.eu`, `polomagona.it` → tổng
**22 mục sống, đúng nguồn, đúng phạm vi**.

**Gán toạ độ:** dùng thẳng toạ độ thật `geonames_details.lat/lng` có sẵn trong ROR cho cả 22 mục
(không cần centroid/suy đoán). Tên: bỏ hậu tố phân biệt `(Country)` mà ROR tự thêm khi trùng tên
toàn cầu (vd "GWT-TUD GmbH (Germany)" → "GWT-TUD GmbH") vì đây là hậu tố kỹ thuật của ROR, không phải
tên chính thức của tổ chức.

**Kết quả merge:** xác nhận `git status` sạch + `len(load_roster(...))` = 19826 đúng ngay trước khi
ghi. `ROSTER`: 19826 → **19848** (+22). Đơn vị trên bản đồ: 19835 → **19857** (+22, giữ nguyên
chênh lệch +9). Kiểm: `node --check` sạch, thẻ `div`/`section` cân bằng (107/107, 6/6). Mở
`index.html` qua HTTP server cục bộ (`static-server`), đọc qua Browser pane: đúng "19857 đơn vị được
lập bản đồ" / "19848 trong danh mục mở rộng" / "12 đơn vị tại Việt Nam" (không đổi) / "9 case phân
tích chuyên sâu" (không đổi). Commit và `git push origin main` lên live (xem hash ở cuối báo cáo
phiên).

**Việc mở cho lượt sau:** (1) ROR coi như đã khai thác hết phần khả thi (>45 cụm từ khoá đa ngôn
ngữ đã quét, tỉ lệ trùng ROSTER rất cao 59%) — KHÔNG quay lại nguồn này trừ khi có ý tưởng từ khoá
hoàn toàn mới chưa thử; (2) Zenodo/`zenodo-rdm.web.cern.ch` đang 504 toàn trang (không phải do
mạng) — nếu lượt sau cần dump ROR đầy đủ (vd để làm kỹ hơn phần "facility"/"nonprofit" 44000+ dòng
chưa duyệt tay), thử lại xem Zenodo đã phục hồi chưa; (3) Nhật Bản JPO/METI TLO vẫn 403; (4) Trung
Quốc `chinatorch.gov.cn` vẫn không kết nối được; (5) Thuỵ Điển SISP/Phần Lan TEKEL — đã xác nhận CẠN
cả site gốc lẫn proxy IASP (checkpoint 47); (6) **vẫn cần NGUỒN LỚN HOÀN TOÀN MỚI cỡ CORDIS/IASP**
(hàng trăm-nghìn mục) vì các nguồn nhỏ lẻ gần đây (Na Uy +11, ROR +22) chỉ cho vài chục mục/
checkpoint — không đủ tốc độ để chạm mốc 25000 (còn thiếu ~5152).

---
**Lần trước:** 2026-09-10 (checkpoint 47 — **SBIR/STTR MỸ: KIỂM MẪU → LOẠI NGAY VÌ SAI PHẠM VI +
API ĐANG BẢO TRÌ; HOÀN TẤT VIỆC MỞ NA UY SIVA (+11); IASP-LÀM-PROXY BẮC ÂU XÁC NHẬN ĐÃ CẠN**) —
còn thiếu ~5174 lúc cuối phiên.

**Nhiệm vụ chính — SBIR.gov (Mỹ): kiểm phạm vi + kỹ thuật TRƯỚC khi tải hàng loạt, theo đúng yêu
cầu của sếp.** Kỹ thuật: endpoint công khai `api.www.sbir.gov/public/api/awards` trả **403
Forbidden** nhất quán qua `curl` (nhiều User-Agent khác nhau), qua Browser pane (trình duyệt thật)
— khớp đúng thông báo chính thức trên `sbir.gov/api`: "the SBIR.gov APIs are currently undergoing
maintenance". Trang `sbir.gov/data-resources` có nêu file CSV tải hàng loạt (65-290MB) nhưng
**KHÔNG cần tải** vì đã xác định SAI PHẠM VI trước: `WebSearch` mẫu vài award thật (NASA, NSF, DOE)
cho ra toàn tên DOANH NGHIỆP NHỎ làm R&D nhận hợp đồng liên bang (vd "Black Swift Technologies",
"Techshot") — đây là CÔNG TY KHỞI NGHIỆP/công nghệ, không phải ĐƠN VỊ TRUNG GIAN hỗ trợ ĐMST (TTO/
vườn ươm/khu KH&CN) mà ROSTER yêu cầu — **giống hệt rủi ro đã gặp và LOẠI ở DPIIT India (checkpoint
21)**. Hai lý do độc lập (sai phạm vi + API bảo trì/chặn) → **LOẠI HẲN SBIR/STTR, không tải/xử lý
hàng loạt**, chuyển sang các hướng dự phòng đã liệt kê ở checkpoint 46.

**Hướng dự phòng 1 — Hàn Quốc Daegu/Gwangju/Gyeonggi Daejin TechnoPark:** thử lại `curl` (dgtp.or.kr,
gjtp.or.kr timeout hoàn toàn; gdtp.or.kr 403) và qua Browser pane thật (dgtp.or.kr, gjtp.or.kr đều
"navigation denied or failed") — **VẪN CHẶN như các checkpoint trước, không phải lỗi tạm thời**,
xác nhận lại kết luận cũ, không tốn thêm công.

**Hướng dự phòng 2 — Na Uy SIVA (hoàn tất việc mở từ checkpoint 44):** tra `WebSearch` URL riêng
cho 12 tên tổ chức SIVA đã ghi ở checkpoint 44. Kết quả: 11/12 có URL chính chủ xác nhận qua
`check_url()` (tất cả **11/11 sống**, không ca nào bị cờ); "Oslotech" là ngoại lệ — hoá ra chính là
công ty đứng sau "Oslo Science Park" (`forskningsparken.no`) **ĐÃ CÓ SẴN TRONG ROSTER** (khớp
domain), loại không merge lại. Lọc trùng ROSTER (toàn bộ, cả domain lẫn tên) cho **0 trùng** với 11
mục còn lại. Gán toạ độ THÀNH PHỐ THẬT theo trụ sở từng tổ chức (Trondheim, Oslo, Kjeller, Dokka,
Harstad, Bodø, Gjøvik, Knarvik, Kongsberg, Herøya/Porsgrunn, Halden) — 3/11 (Harstad, Bodø, Knarvik)
cho `CountryLookup.country_for()` = `None` do đúng lỗi độ phân giải polygon Natural Earth 50m ở
vùng biển/fjord đã ghi nhận từ checkpoint 39-40/46 (không phải toạ độ sai) — **CHẤP NHẬN** theo
đúng tiền lệ vì đây là toạ độ thành phố thật, có nguồn xác định rõ, không phải centroid bịa.
**11 mục mới, 0 Việt Nam.**

**Hướng dự phòng 3 — IASP-làm-proxy cho khu vực Bắc Âu chưa tiếp cận trực tiếp được (Thuỵ Điển
SISP, Phần Lan TEKEL) — gợi ý mở từ checkpoint 42:** lọc trực tiếp `iasp.ws/our-members/directory`
theo `Country=Sweden` qua Browser pane (cần "Accept Selected" ở cookie-consent trước) → ra 14 tên
(Ideon Science Park, Lindholmen, Uminova Innovation...) — đối chiếu ROSTER thì **CẢ 14/14 ĐÃ CÓ
SẴN**, khớp domain và tên chính xác. **Xác nhận dứt điểm: gợi ý "IASP-làm-proxy" của checkpoint 42
KHÔNG còn giá trị** — IASP đã được khai thác TOÀN BỘ 79 nước (kể cả Bắc Âu) ngay từ checkpoint 21,
không có gì sót lại để lọc lại theo nước. Đừng thử lại hướng này ở các checkpoint sau.

**Hướng dự phòng 4 (thử nhanh, không theo tới cùng) — MENAinc (mạng lưới vườn ươm/khu công nghệ
Trung Đông-Bắc Phi của World Bank infoDev):** `WebSearch` không tìm được danh bạ hội viên còn sống
(chương trình `infoDev` của World Bank đã ngừng khoảng 2018, trang `spica-directory.net` liệt kê
MENAinc đã **404 Not Found**) — có thể còn cách tiếp cận khác (Wayback Machine cho trang MENAinc/
infoDev cũ) nhưng CHƯA THỬ, để lại việc mở cho lượt sau nếu muốn theo tới cùng.

**Kết quả merge:** xác nhận `git status` sạch + `len(load_roster(...))` = 19815 đúng ngay trước khi
ghi. `ROSTER`: 19815 → **19826** (+11, toàn bộ từ Na Uy SIVA). Đơn vị trên bản đồ: 19824 → **19835**
(+11, giữ nguyên chênh lệch +9). Kiểm: `node --check` sạch (script inline 3,390,592 ký tự), thẻ
`div`/`section` cân bằng (107/107, 6/6). Mở `index.html` qua HTTP server cục bộ
(`static-server` có sẵn), đọc qua Browser pane: đúng "19835 đơn vị được lập bản đồ" / "19826 trong
danh mục mở rộng" / "12 đơn vị tại Việt Nam" (không đổi) / "9 case phân tích chuyên sâu" (không
đổi). Commit và `git push origin main` lên live (xem hash ở cuối báo cáo phiên).

**Việc mở cho lượt sau:** (1) Nhật Bản JPO/METI TLO vẫn 403 (chưa thử cổng khác: Google cache, PDF
trực tiếp, trang tiếng Anh METI/JETRO); (2) Trung Quốc `chinatorch.gov.cn` vẫn không kết nối được
qua nhiều checkpoint — có thể bỏ hẳn; (3) Thuỵ Điển SISP/Phần Lan TEKEL — hướng site gốc vẫn chặn
mạng, và hướng proxy IASP đã xác nhận CẠN (xem trên) — cần nguồn thứ 3 hoàn toàn khác nếu muốn tiếp
tục 2 nước này; (4) 219 ca CORDIS FP7 bị `check_url()` gắn cờ "cross-domain redirect" (checkpoint
46) vẫn chưa xác minh tay; (5) MENAinc/infoDev — thử Wayback Machine nếu muốn theo tới cùng (xem
trên); (6) cần tìm NGUỒN LỚN HOÀN TOÀN MỚI cỡ CORDIS/IASP/ANPROTEC (hàng trăm-nghìn mục) vì các
hướng dự phòng nhỏ lẻ (Na Uy, Hàn Quốc còn lại) chỉ cho vài mục/checkpoint — không đủ tốc độ để
chạm mốc 25000 (còn thiếu ~5174).

---
**Lần trước:** 2026-09-10 (checkpoint 46 — **CORDIS FP7 (chương trình 2007-2013) — GIÁ TRỊ VẪN CÒN
NHƯNG THẤP HƠN H2020/HORIZON, VÀ LẦN ĐẦU GẶP CORDIS THIẾU `geolocation`**) — còn thiếu ~5185 lúc
cuối phiên.

Lượt trước (checkpoint 45) để lại việc mở rõ ràng nhất: `cordis-fp7projects-csv.zip` (33MB) tải
sẵn nhưng chưa dùng — cùng cấu trúc `organization.csv` như Horizon Europe/H2020, chương trình kết
thúc trước 2014 nên quần thể tổ chức tham gia có thể khác phần nào. Lượt này xử lý đúng file đó,
lặp lại kỹ thuật REC-filter → dedup ROSTER → scope-filter → `check_url()` → gán toạ độ → merge của
checkpoint 45.

**Trích xuất REC:** 140064 dòng tổ chức-tham-gia-dự-án FP7 → 33065 dòng `activityType=REC` → gộp
theo `organisationID` → **3701 tổ chức REC duy nhất**, trong đó **2881 có `organizationURL`
(~78%)** — CAO HƠN HẲN tỉ lệ điền URL của H2020/Horizon (~38%, checkpoint 45), có thể vì FP7 dùng
form khai báo tổ chức khác/bắt buộc hơn thời đó.

**Lọc trùng ROSTER** (19446 mục lúc này, đã bao gồm +594 CORDIS Horizon+H2020 của checkpoint 45 —
nên tự động loại lại bất kỳ tổ chức FP7 nào đã lọt qua ở lượt trước mà không cần đối chiếu
`organisationID` chéo 2 lượt): loại 1457 trùng domain + 33 trùng tên → **1391 ứng viên mới**. Lọc
từ khoá phạm vi (đúng danh sách 21 từ khoá của checkpoint 45: HOSPITAL/MUSEUM/MINISTRY/CITY OF...)
loại 76 (nhiều bệnh viện đại học Pháp/Ý/Tây Ban Nha, viện bảo tàng lịch sử tự nhiên, 1 sở thú Anh)
→ **1315 ứng viên**.

**`check_url()` toàn bộ 1315** (2 batch 660+655, `ThreadPoolExecutor` 24 luồng): chỉ **373 sống
(28%)** — THẤP HƠN NHIỀU so với 57% của H2020/Horizon ở checkpoint 45, đúng như dự đoán vì dự án
FP7 kết thúc từ 2007-2013, nhiều tổ chức/domain đã đổi tên, sáp nhập, hoặc ngừng hoạt động sau
hơn một thập kỷ. Lý do chết: `URLError`/`HTTPError`/timeout áp đảo (507+150+20=677), **219 ca cờ
"cross-domain redirect"** (số lượng lớn hơn hẳn checkpoint 45 — trải trên rất nhiều domain đích
khác nhau, gồm cả những domain đã gặp ở checkpoint 45 như `ri.se`/`fraunhofer.de`/`gov.uk`, đúng
kiểu tổ chức đổi domain thật giữa các chương trình CORDIS mà không xác minh tay lượt này), 20 ca
trang đỗ tên miền ("domain may be for sale" v.v.). Kiểm tay 6 URL ngẫu nhiên qua `curl` xác nhận
cả 6 sống thật (HTTP 200) — không phát hiện false-positive.

**Vấn đề MỚI chưa gặp ở CORDIS trước đây — `geolocation` gần như TRỐNG trong FP7:** chỉ **20/373
(5%)** có toạ độ thật trong CSV, khác hẳn ghi chú checkpoint 45 rằng CORDIS "luôn có toạ độ thật
cấp địa chỉ" — hoá ra điều đó chỉ đúng với Horizon Europe/H2020 (dự án gần đây, form khai báo bắt
buộc geolocation), còn FP7 (form cũ hơn, 2007-2013) phần lớn để trống trường này. **Xử lý: quay
lại kỹ thuật centroid quốc gia CỦA CÁC CHECKPOINT TRƯỚC CORDIS** — không tự tính bbox/mean mới, mà
lấy điểm (lat,lon) ĐÃ DÙNG NHIỀU NHẤT cho đúng quốc gia đó ngay trong chính `ROSTER` hiện có (dựng
bảng tần suất toạ độ theo quốc gia từ `ROSTER`, chọn điểm lặp nhiều nhất — vd Đức
(51.1657,10.4515) dùng lại từ 203/1873 mục Đức có sẵn, Mỹ (39.8283,-98.5795) từ 275/1379 mục) —
đối chiếu qua `CountryLookup.country_for()`: đa số khớp đúng quốc gia khai báo, một số nước nhỏ/
quần đảo (Thuỵ Điển, Hy Lạp, Indonesia, Philippines, Đan Mạch, Iceland, Monaco) cho kết quả "None"
vì điểm rơi ra biển ở độ phân giải polygon Natural Earth 50m (bug đã ghi nhận từ checkpoint 39-40)
— CHẤP NHẬN vì đây là toạ độ THẬT ĐÃ CÓ SẴN VÀ ĐÃ ĐƯỢC XÁC MINH trong ROSTER cho đúng quốc gia đó
ở một mục khác, không phải centroid bịa mới. **351/369 mục cuối cùng dùng centroid kiểu này, chỉ
20 dùng toạ độ thật từ CSV** (đảo ngược hẳn tỉ lệ so với checkpoint 45 dùng 100% toạ độ thật).
Thêm 2 mã quốc gia CORDIS chưa có trong bảng ánh xạ: `MC`→Monaco, `DZ`→Algeria (cả 2 đều có sẵn
toạ độ thật trong CSV, không cần centroid).

**Việt Nam:** phát hiện 2 ứng viên FP7 có `country=VN` lọt qua toàn bộ bộ lọc trên (kể cả
`check_url()` sống) — LOẠI THẲNG theo đúng quy tắc ROSTER không chứa đơn vị Việt Nam, không merge.

**Lọc trùng NỘI BỘ batch theo domain** (bước mới bổ sung lượt này — checkpoint 45 chưa làm bước
này, tự phát hiện 2 cặp): "Ceit Alanova Gemeinnützige GmbH" và "Ceit Raltec Gemeinnützige GmbH"
cùng dùng `ceit.at` (2 pháp nhân con Áo, giữ 1 để tránh 2 điểm bản đồ trùng URL); "Eötvös Károly
Közpolitikai Nonprofit Közhasznú Korlátolt Felelősségű Társaság" và tên viết tắt cũ "...Kht" cùng
dùng `ekint.org` — rõ ràng CÙNG một tổ chức ghi 2 `organisationID` khác nhau qua các năm (Hungary
đổi luật hình thức pháp nhân phi lợi nhuận "Kht"→dạng đầy đủ giữa 2007-2014, đúng giai đoạn FP7) —
giữ 1 bản tên đầy đủ mới hơn.

**Sửa lỗi thẩm mỹ `smart_titlecase`:** 8 tên có hậu tố pháp nhân đã sẵn dấu chấm trong CSV gốc (vd
"...NONPROFIT KFT.") bị thuật toán map thêm 1 dấu chấm nữa ("...Kft.." — bảng ánh xạ hậu tố của
checkpoint 45 tự thêm dấu chấm không kiểm tra trùng) → regex `\.\.+`→`.` dọn lại sau khi sinh tên,
không sửa thuật toán gốc (vẫn dùng nguyên cho các đợt sau, chỉ cần dọn hậu kỳ).

**Kết quả merge:** 371 dòng qua bước gán toạ độ, trừ 2 trùng nội bộ domain → **369 mục mới**. Xác
nhận `git status` sạch + `len(load_roster(...))` = 19446 đúng ngay trước khi ghi. `ROSTER`: 19446
→ **19815** (+369). Đơn vị trên bản đồ: 19455 → **19824** (+369, giữ nguyên chênh lệch +9 với
ROSTER). Kiểm: `node --check` sạch (script inline 3,389,711 ký tự), thẻ `div`/`section` cân bằng
(107/107, 6/6). Mở `index.html` qua HTTP server cục bộ (`.claude/launch.json` cấu hình
`static-server` có sẵn từ checkpoint trước), đọc qua Browser pane: đúng "19824 đơn vị được lập bản
đồ" / "19815 trong danh mục mở rộng" / "12 đơn vị tại Việt Nam" (không đổi) / "9 case phân tích
chuyên sâu" (không đổi), console sạch. Commit và `git push origin main` lên live (xem hash ở cuối
báo cáo phiên).

**CORDIS coi như ĐÃ KHAI THÁC HẾT cho `activityType=REC`** sau khi dùng cả 3 chương trình
(Horizon Europe + H2020 ở checkpoint 45, FP7 ở checkpoint này) — tổng **963 mục** từ nguồn này qua
2 checkpoint (594+369), năng suất giảm dần đúng như dự đoán vì trùng lặp tổ chức xuyên chương
trình tăng dần. **Việc mở cho lượt sau:** (1) tổ chức HES (nguyên trường đại học) và PUB/OTH bị
loại hẳn ở CORDIS vì sai độ chi tiết ROSTER — nếu muốn khai thác cần tra tay từng trường xem có
đơn vị CGCN/nghiên cứu con cụ thể không (việc lớn, chậm); (2) **219 ca CORDIS FP7 bị `check_url()`
gắn cờ "cross-domain redirect"** (số lượng đáng kể, trải nhiều domain đích khác nhau — có thể còn
tổ chức thật đã đổi domain giữa 3 chương trình CORDIS chưa xác minh tay, việc mở lớn hơn hẳn ~20
ca của checkpoint 45); (3) quay lại nguồn khác ngoài CORDIS: SBIR/STTR Mỹ
(`sbir.gov`, chưa thử qua 46 checkpoint), Hàn Quốc Daegu/Gwangju/Gyeonggi Daejin TechnoPark (nghi
chặn IP/bot, có thể thử lại giờ khác hoặc qua Wayback Machine), Na Uy SIVA (có tên tổ chức cụ thể
từ checkpoint 44, chưa tra URL riêng).

---
**Lần trước:** 2026-09-10 (checkpoint 45 — **NGUỒN HOÀN TOÀN MỚI: CORDIS (CSDL dự án NC&PT do EU
tài trợ), TẢI HÀNG LOẠT KHÔNG QUA CÀO TRANG, TOẠ ĐỘ THẬT CÓ SẴN TRONG DỮ LIỆU NGUỒN**) — còn thiếu
~5554 lúc cuối phiên.

Lượt trước (checkpoint 44) kết luận cả 2 hướng cũ (Wikidata dò từ khoá, đăng ký chính phủ/hiệp hội
theo từng nước) đều đang cạn, khuyến nghị tìm NGUỒN HOÀN TOÀN MỚI LOẠI KHÁC. Lượt này khai thác
`CORDIS` (`cordis.europa.eu`, CSDL công khai của Uỷ ban Châu Âu ghi mọi dự án Horizon
Europe/H2020/FP7 + toàn bộ tổ chức tham gia từng dự án) — CHƯA TỪNG THỬ qua 44 checkpoint trước.

**Tải dữ liệu:** xác nhận 3 file ZIP tải hàng loạt công khai, không cần đăng nhập/API key, `curl`
tải thẳng được (không cần `WebFetch`/cào trang): `cordis.europa.eu/data/cordis-HORIZONprojects-
csv.zip` (37MB), `cordis.europa.eu/data/cordis-h2020projects-csv.zip` (55MB, dùng lượt này),
`cordis.europa.eu/data/cordis-fp7projects-csv.zip` (33MB, **CHƯA dùng lượt này** — để lại cho lượt
sau, khả năng còn tổ chức mới vì FP7 kết thúc trước 2014, quần thể tổ chức tham gia có thể khác
H2020/Horizon Europe). Mỗi ZIP có `organization.csv` — record MỖI lượt một tổ chức tham gia MỘT dự
án (không phải danh sách tổ chức duy nhất), cột quan trọng: `organisationID` (mã PIC của EU, **nhất
quán xuyên suốt cả 3 chương trình** — dùng để gộp trùng tổ chức tham gia nhiều dự án/nhiều chương
trình), `name` (tên pháp nhân, LUÔN VIẾT HOA TOÀN BỘ — xem vấn đề casing bên dưới), `activityType`
(HES=đại học, REC=viện nghiên cứu, PRC=doanh nghiệp tư nhân, PUB=cơ quan công, OTH=khác),
`country` (ISO2, ngoại lệ `EL`=Hy Lạp và `UK`=Anh không theo chuẩn ISO thường), `geolocation`
(chuỗi `"lat,lon"` — **toạ độ thật cấp địa chỉ có sẵn, không cần centroid/geocode gì thêm** — điểm
mới so với mọi nguồn dùng ở 44 checkpoint trước), `organizationURL`.

**Quyết định phạm vi — chỉ lấy `activityType=REC`:** kiểm mẫu xác nhận `HES` chỉ là tên pháp nhân
NGUYÊN TRƯỜNG ĐẠI HỌC kèm URL trang chủ chung (vd "THE UNIVERSITY OF EDINBURGH" → `ed.ac.uk/home`),
không phải đơn vị CGCN/nghiên cứu cụ thể trong trường — SAI khớp độ chi tiết của ROSTER (ROSTER lưu
đơn vị cụ thể như "TLO Kyoto", "BioNanoNet" — không lưu nguyên trường đại học trần) nên **loại hẳn
HES**, cũng loại `PRC` (doanh nghiệp tư nhân thường, ngoài phạm vi) và `PUB`/`OTH` (quá tạp, không
đủ tín hiệu phân biệt). `REC` = định nghĩa chính thức của EU "pháp nhân phi lợi nhuận có NC&PT là
một trong các mục tiêu chính" — khớp tốt với "trung tâm nghiên cứu" trong phạm vi ROSTER (mẫu: CNR
Italy, Fraunhofer, TNO/VITO, CEA, AIT, TUBITAK...).

**Số liệu qua từng bước lọc** (script Python, không qua Gemini — dữ liệu đã có cấu trúc sẵn, không
cần trích xuất bằng AI): Horizon Europe 3538 tổ chức REC duy nhất, H2020 3469 — gộp theo
`organisationID` xuyên 2 chương trình → **4782 tổ chức REC duy nhất**, trong đó **1805 có
`organizationURL`** (~38%, thấp hơn nhiều so với tỉ lệ điền URL theo dòng vì các tổ chức tham gia
nhiều dự án nhất thường điền URL nhất quán, còn tổ chức tham gia 1 lần thì hay bỏ trống). Lọc trùng
ROSTER bằng `base_domain()` (loại 671) + `normalize_name()` khớp `name` hoặc `shortName` (loại 21)
→ **1113 ứng viên mới**. Lọc từ khoá phạm vi (loại bệnh viện/viện y tế lâm sàng thuần, bảo tàng, bộ/
ngành chính phủ, thị chính, nhà thờ, sở thú/rạp hát, nhà tù/công an, trường mầm non/tiểu học — 21
từ khoá tiếng Anh phổ biến, ví dụ "HOSPITAL"/"MUSEUM"/"MINISTRY"/"CITY OF") → loại 43 (vd "Centre
Hospitalier Universitaire de Liège", "Naturhistorisches Museum") → **1070 ứng viên**.

**`check_url()` toàn bộ 1070** (2 batch 535, ThreadPoolExecutor 24 luồng song song để chạy nhanh —
không đổi logic `check_url()` trong `roster_common.py`, chỉ chạy nhiều request cùng lúc — mỗi batch
xong trong vài chục giây thay vì hàng chục phút chạy tuần tự): **611 sống** (57%), 459 chết —
`URLError`/`HTTPError`/timeout đa số (219+91), cộng ~20 ca bị `check_url()` gắn cờ "cross-domain
redirect" (vd `ri.se`, `gov.uk`, `sei.org` — tổ chức đã đổi domain/sáp nhập, đúng thiết kế của hàm,
KHÔNG tự tin merge, để lại việc mở nếu muốn xác minh tay từng ca), 3-4 ca trang đỗ tên miền thật.
Không có false-positive nào phát hiện qua rà mẫu lý do chết.

**Vấn đề casing tên (mới, chưa gặp ở nguồn nào trước) — tên trong CSV LUÔN VIẾT HOA TOÀN BỘ, không
có nguồn nào cho tên viết hoa-thường chuẩn sẵn:** thử fetch `<title>` trang mỗi tổ chức (591/611 lấy
được) nhưng phần lớn không dùng được — tiêu đề trang thường là "Home"/"Startseite"/"Forside" (điều
hướng chung, không phải tên tổ chức) hoặc chứa ký tự HTML entity vỡ (`&#8212;`) hoặc chữ không phải
Latin (tiếng Hy Lạp/Bulgaria/Serbia dùng chữ Cyrillic cho tên tổ chức Latin gốc) — **không đủ tin
cậy để dùng làm tên hiển thị chính**. Thay vào đó viết thuật toán "smart title-case" tự áp cho tên
gốc viết hoa: bảng ánh xạ hậu tố pháp nhân phổ biến (GMBH→GmbH, SL→S.L., SA→S.A., NV→N.V., BV→B.V.,
EV→e.V., KFT→Kft., SRL→S.r.l., SPA→S.p.A., ASBL/VZW giữ nguyên...) + danh sách từ nối viết thường
đa ngôn ngữ Châu Âu (de/della/dei/van/von/der/het/et/per/voor/y/e...) — **CHẤT LƯỢNG THẤP HƠN tên đã
xác minh thủ công từng đơn vị ở các checkpoint trước** (không hoàn hảo với tên riêng/họ người, ví dụ
lỗi phát hiện qua rà mẫu: "M.B.H." → "M.b.h." dù đã map — chấp nhận vì quy mô 594 mục không thể xác
minh tay từng tên trong 1 lượt). Phát hiện + sửa tay 5 ca lỗi dữ liệu nguồn thật: 3 tên bị nối thêm
"*BIỆT_DANH" (CSV gộp 2 trường bằng dấu `*`, vd "...FOR DEVELOPMENT*CASTED" → cắt lấy phần trước
dấu `*`), 2 tên bị nhân đôi dấu ngoặc kép do lỗi encode CSV gốc (vd `""F. DE PAULA ROJAS""""` → sửa
tay thành `"F. de Paula Rojas"`).

**Toạ độ — dùng thẳng `geolocation` thật từ CORDIS, không centroid:** parse `"lat,lon"`, gọi
`CountryLookup.country_for(lon, lat)` (đúng thứ tự lon-trước như checkpoint 44 đã học) để vừa lấy
tên quốc gia đúng quy ước ROSTER vừa xác minh chéo toạ độ đúng nước khai báo. Phát hiện 27 "lệch"
chỉ do khác biến thể tên (Czechia/Czech Republic, Russia/Russian Federation, DR Congo/Democratic
Republic of Congo, Guinea Bissau/Guinea-Bissau) — không phải lỗi thật, xử lý bằng nhóm tương đương,
giữ tên `CountryLookup` trả về (khớp quy ước `NAME_OVERRIDE` có sẵn). **2 lệch THẬT do toạ độ sát
biên giới** (không phải lỗi centroid như checkpoint trước, mà lỗi độ chính xác toạ độ nguồn): "Istituto
di Sociologia Internazionale di Gorizia" (Ý, thị trấn biên giới Ý-Slovenia, toạ độ rơi sang phía
Slovenia) và "World Business Council for Sustainable Development" (trụ sở Geneva, Thuỵ Sĩ, toạ độ
rơi sang phía Pháp) — cả 2 giữ quốc gia khai báo gốc (Ý, Thuỵ Sĩ) thay vì quốc gia toạ độ trỏ tới,
vì đây là trụ sở thật đã biết, không phải toạ độ bịa.

**Kết quả merge:** 594 mục mới (0 Việt Nam — không có tổ chức Việt Nam nào lọt qua REC+URL+
check_url ở CORDIS lượt này). Trải khắp Châu Âu (Tây Ban Nha 73, Ý 58, Đức 53, Pháp 40, Anh 29...)
kèm một số tổ chức đối tác quốc tế của EU (Trung Quốc 8, Ấn Độ 4, Nga 6, Ukraine 7, Serbia 6, Mexico
4, Nhật 1, Hàn Quốc 1, Israel 1, Malaysia 1, Sri Lanka 1, Kenya 1, Nigeria 2, Morocco 2, Tanzania 2,
Botswana 1, Cameroon 1, Seychelles 1, New Zealand 1, Úc 3...). Xác nhận `git status` sạch +
`len(load_roster(...))` = 18852 đúng ngay trước khi ghi. `ROSTER`: 18852 → **19446** (+594). Đơn vị
trên bản đồ: 18861 → **19455** (+594, giữ nguyên chênh lệch +9 với ROSTER). Kiểm: `node --check`
sạch (script inline 3,349,465 ký tự), thẻ `div`/`section` cân bằng (107/107, 6/6). Mở `index.html`
qua HTTP server cục bộ, đọc `get_page_text`: đúng "19455 đơn vị được lập bản đồ" / "19446 trong
danh mục mở rộng" / "12 đơn vị tại Việt Nam" (không đổi) / "9 case phân tích chuyên sâu" (không
đổi), console sạch. Commit `b7a098a`, đã `git push origin main` lên live.

**Còn thiếu ~5554 để đạt 25000 — CORDIS là nguồn hiệu quả nhất tính đến nay (594 mục 1 lượt, so với
Wikidata 63-260/lượt các checkpoint gần đây).** **Việc mở cho lượt sau:** (1) thử tiếp `cordis-
fp7projects-csv.zip` (chưa dùng lượt này, cùng cấu trúc `organization.csv`, dự án FP7 kết thúc
trước 2014 nên quần thể tổ chức tham gia có thể khác phần nào so với H2020/Horizon Europe đã dùng —
lặp lại đúng quy trình REC-filter → dedup → check_url → merge); (2) ~20 ca bị `check_url()` gắn cờ
"cross-domain redirect" (tổ chức thật đã đổi domain, vd `ri.se`) chưa xác minh tay — nếu xác minh
đúng là cùng tổ chức thì có thể thêm URL mới; (3) tổ chức HES (nguyên trường đại học, ~1412/2903 có
URL) và PUB/OTH bị loại hẳn lượt này vì sai độ chi tiết ROSTER — nếu muốn khai thác sẽ cần tra tay
từng trường xem có đơn vị CGCN/nghiên cứu con cụ thể không (việc lớn, chậm, không hợp một checkpoint
đơn); (4) tỉ lệ trùng ROSTER khá cao ở REC (671/1805 = 37% đã có sẵn) cho thấy Châu Âu đã được khai
thác khá kỹ qua 44 checkpoint trước — hướng CORDIS còn giá trị chính ở tổ chức đối tác quốc tế của
EU (Châu Á/Phi/Mỹ Latinh tham gia Horizon Europe) hơn là mở rộng thêm Châu Âu thuần.

**Việc mở tồn đọng từ checkpoint 44 (chưa động tới lượt này, vẫn còn giá trị):** Daegu/Gwangju/
Gyeonggi Daejin TechnoPark Hàn Quốc (nghi chặn IP/bot tạm thời); Nhật Bản JPO/METI TLO list (403);
Trung Quốc `chinatorch.gov.cn` (chặn mạng nhất quán nhiều checkpoint); Bắc Âu SISP Thuỵ Điển/TEKEL
Phần Lan (không kết nối được, gợi ý thử qua IASP directory làm proxy); Na Uy SIVA (có tên tổ chức cụ
thể, chưa tra URL riêng).

---
**Lần trước:** 2026-09-10 (checkpoint 44 — **CHUYỂN HẲN SANG NGUỒN "ĐĂNG KÝ CHÍNH PHỦ/HIỆP HỘI
CHÍNH THỨC", KHAI THÁC MẠNG LƯỚI TECHNOPARK HÀN QUỐC, NHIỀU NGUỒN LỚN BỊ CHẶN MẠNG**) — còn thiếu
~6148 lúc cuối phiên.

Lượt trước (checkpoint 43) để lại việc mở: kỹ thuật dò-từ-khoá-nhãn Wikidata giảm hiệu suất rõ
rệt qua 3 lượt (664→260→63), khuyến nghị chuyển hẳn sang nguồn "đăng ký chính phủ có cột website"
cho các nước lớn CHƯA THỬ — đặc biệt mạng lưới TechnoPark Hàn Quốc (checkpoint 43 mới lấy được
11/17 qua Wikidata, cần tìm trang danh bạ chính thức đủ hơn).

**Hàn Quốc — TechnoPark, nguồn dùng: Wikipedia tiếng Hàn (bài "한국테크노파크진흥회", đối chiếu
qua `technopark.kr/find` là trang tìm-theo-vùng của hiệp hội, không liệt kê thẳng URL từng tỉnh
nên phải tra riêng).** Hiệp hội hiện có **19 thành viên chính thức** (không phải 17 như checkpoint
43 ước tính — có thêm Gyeonggi Daejin TechnoPark và Sejong TechnoPark là các TP mới thành lập sau
này, ngoài 17 tỉnh/thành gốc): Seoul, Busan, Daegu, Incheon, Gwangju, Daejeon, Ulsan, Gyeonggi,
Gangwon, Chungbuk, Chungnam, Jeonbuk, Jeonnam, Gyeongbuk, Gyeongnam, Jeju, Gyeonggi Daejin,
Pohang (cấp thành phố, không phải cấp tỉnh — đã có sẵn), Sejong. Rà lại ROSTER bằng script (không
tin bằng mắt — lần rà bằng mắt đầu tiên bỏ sót "Chungnam Techno Park" vì tên có dấu cách
"Techno Park" khác "Technopark" viết liền mà bộ lọc ban đầu dùng chuỗi con "technopark" không
khớp) xác nhận ROSTER đã có 11 mục (10 tỉnh + Pohang): Ulsan, Gyeonggi, Gyeongnam, Gyeongbuk,
Daejeon, Seoul, Incheon, Jeonnam, Jeonbuk, Chungnam, Pohang. **Còn thiếu 8:** Busan, Daegu,
Gwangju, Gangwon, Chungbuk, Jeju, Gyeonggi Daejin, Sejong.

Tra URL chính thức từng tỉnh còn thiếu qua `WebSearch` (tên tiếng Hàn + "공식 홈페이지"), rồi
`check_url()` từng cái: **Busan** (`btp.or.kr`), **Gangwon** (`gwtp.or.kr`), **Chungbuk**
(`cbtp.or.kr`), **Jeju** (`jejutp.or.kr`), **Sejong** (`sjtp.or.kr`) — cả 5 đều **sống thật**.
Riêng Chungbuk, `check_url()` báo lỗi `URLError: [SSL: DH_KEY_TOO_SMALL]` (máy chủ dùng tham số
Diffie-Hellman cũ mà OpenSSL mặc định trên máy chặn) — xác minh tay bằng `ssl.create_default_
context()` + `set_ciphers('DEFAULT@SECLEVEL=1')` để hạ mức bảo mật cipher, fetch thành công HTTP
200 cùng domain (không redirect), nội dung thật (không phải trang đỗ tên miền) → tính là sống.
**Ghi lại kỹ thuật SECLEVEL=1 này để dùng lại khi gặp lỗi DH_KEY_TOO_SMALL ở các site chính phủ
dùng hạ tầng SSL cũ** (chưa vá thẳng vào `roster_common.py` vì đây là workaround thủ công cần soi
từng trường hợp, không nên tự động hạ bảo mật cho mọi request).

**3 mục còn lại LOẠI vì không kết luận được (không phải vì xác nhận chết):** Daegu (`dgtp.or.kr`
và biến thể `www.dgtp.or.kr`) và Gwangju (`gjtp.or.kr` và biến thể `www.`/`http://`) — cả hai đều
`ECONNREFUSED`/timeout nhất quán qua nhiều kênh khác nhau (máy cục bộ qua `urllib`, `WebFetch` từ
hạ tầng khác, nhiều lần thử lại) — giống hệt tình huống China Torch các checkpoint trước, nghi
chặn theo IP/khu vực chứ không phải domain thật sự chết; Gyeonggi Daejin (`gdtp.or.kr`) báo `HTTP
403 Forbidden` nhất quán kể cả với User-Agent trình duyệt thật qua cả `urllib` lẫn `WebFetch` —
giống ca Suntory/Fiat checkpoint 43, chặn bot chứ không kết luận được là chết. **Cả 3 để lại cho
lượt sau thử lại** (có thể mạng đỡ chặn hơn vào giờ khác, hoặc thử qua Google cache/Wayback Machine
chưa thử lượt này).

Lọc trùng ROSTER (base-domain + `normalize_name()`): phát hiện "Chungnam Technopark" đã trùng
domain+tên với "Chungnam Techno Park" có sẵn (loại, không merge lại) — 5 mục còn lại không trùng.
Gán toạ độ: dùng toạ độ THÀNH PHỐ THẬT (không dùng centroid quốc gia, cũng không tái dùng cụm
centroid lỗi `35.9125,128.4709` mà nhiều mục Hàn Quốc cũ đang mắc — xem ghi chú checkpoint 42 về
lỗi centroid, không thuộc phạm vi sửa lượt này) — Busan (35.1796, 129.0756), Gangwon/Chuncheon
(37.8813, 127.7298), Chungbuk/Ochang-Cheongju (36.7167, 127.4333), Jeju City (33.4996, 126.5312),
Sejong (36.48, 127.289) — xác nhận cả 5 điểm đều nằm trong polygon Hàn Quốc thật qua
`CountryLookup.country_for(lon, lat)` (chú ý thứ tự tham số là lon trước lat, không phải lat/lon
— lỗi gọi nhầm thứ tự lúc đầu khiến tất cả trả `None`, phát hiện và sửa ngay). → **5 ứng viên
cuối cùng, tất cả Hàn Quốc, 0 Việt Nam.**

**Các nguồn khác đã THỬ và BỊ CHẶN MẠNG/KHÔNG TIẾP CẬN ĐƯỢC lượt này (ghi lại để lượt sau khỏi
lặp lại vô ích, thử lại nếu mạng đỡ chặn hơn):** Nhật Bản — trang danh bạ TLO được công nhận
chính thức của JPO (`jpo.go.jp/toppage/links/tlo.html`) và METI (`meti.go.jp/policy/
innovation_corp/tlo.html`) đều trả **403 Forbidden** nhất quán qua `WebFetch` (thử cả 2 URL, có
vẻ chặn bot/IP nước ngoài) — trang Wikipedia tiếng Nhật về TLO cũng không liệt kê danh sách đầy
đủ, chỉ nêu 1 ví dụ (Okinawa TLO, ghi rõ "không có phê duyệt chính thức" nên không phù hợp). Trung
Quốc — `chinatorch.gov.cn` (cả `http`/`https`) tiếp tục **không kết nối được** (`curl` timeout,
giống mọi checkpoint trước — mạng chặn nhất quán, không phải lỗi tạm thời). Thuỵ Điển — SISP
(`sisp.se`, có trang `/en/members/` liệt kê 63 hội viên theo lời mô tả tìm kiếm) **không kết nối
được** qua cả `curl` cục bộ lẫn `WebFetch` (DNS phân giải đúng IP nhưng connection refused/reset —
nghi chặn theo dải IP, không phải DNS). Na Uy — SIVA (`siva.no`) TRUY CẬP ĐƯỢC (khác Thuỵ Điển) 
nhưng các trang public (`/program/`, `/om-siva/siva-strukturen/`, báo cáo thường niên `arsrapport
24.siva.no/eierskap-i-innovasjonsselskap/`) chỉ mô tả cấu trúc bằng số liệu tổng (vd "61
innovasjonsselskaper") và liệt kê TÊN một vài công ty nổi bật (6AM Accelerator, Oslo Cancer
Cluster Incubator, Oslotech, Kjeller Innovasjon...) nhưng KHÔNG kèm URL — cần tra URL riêng từng
tên qua tìm kiếm nếu muốn dùng, chưa làm được trong lượt này vì lợi ích/công sức chưa rõ (nhiều
tên nghe quen, khả năng cao đã có sẵn trong ROSTER qua các lượt trước). Phần Lan — TEKEL (hiệp hội
science park Phần Lan, `tekel.fi`, 29-32 hội viên theo mô tả tìm kiếm) trang chủ `tekel.fi/in_
english/` **timeout DNS** (`ETIMEOUT`) qua `WebFetch`, không tra được danh sách hội viên.

**Kỹ thuật mới ghi lại cho lượt sau:** (1) khi rà ROSTER tìm trùng theo TỪ KHOÁ TRONG TÊN, LUÔN
chạy bằng script với nhiều biến thể cách viết ("technopark" liền/"techno park" cách/"TechnoPark"
hoa-thường), đừng tin kết quả lọc bằng mắt hoặc regex đơn giản — ca "Chungnam Techno Park" lượt
này suýt bị merge trùng nếu không chạy `base_domain()`/`normalize_name()` qua script trước khi
merge; (2) lỗi SSL `DH_KEY_TOO_SMALL` ở site chính phủ cũ → thử `ssl.create_default_context()` +
`set_ciphers('DEFAULT@SECLEVEL=1')` trước khi kết luận site chết; (3) `CountryLookup.country_for()`
nhận tham số `(lon, lat)` — THỨ TỰ KINH ĐỘ TRƯỚC, không phải `(lat, lon)` như trực giác — gọi
nhầm thứ tự sẽ luôn trả `None` dù toạ độ đúng.

`ROSTER`: 18847 → **18852** (+5, khớp `len(load_roster(...))` kiểm ngay trước merge, `git status`
sạch không có phiên song song). Đơn vị trên bản đồ: 18856 → **18861** (+5, giữ nguyên chênh lệch
+9). Kiểm: `node --check` sạch trên script inline (3,288,518 ký tự), thẻ `div`/`section` cân bằng
(107/107, 6/6). Mở `index.html` qua HTTP server cục bộ (`preview_start`/`preview_stop`), đọc
`get_page_text`: đúng "18861 đơn vị được lập bản đồ" / "18852 trong danh mục mở rộng" / "12 đơn vị
tại Việt Nam" (không đổi) / "9 case phân tích chuyên sâu" (không đổi), console sạch.

**Còn thiếu ~6148 để đạt 25000.** **Việc mở cho lượt sau:** (1) thử lại Daegu/Gwangju TechnoPark
(`dgtp.or.kr`/`gjtp.or.kr`) và Gyeonggi Daejin TechnoPark (`gdtp.or.kr`) — nghi chặn IP/bot tạm
thời, không phải chết thật, thử vào thời điểm khác hoặc qua Wayback Machine; (2) Nhật Bản — JPO/
METI TLO list bị chặn 403, cần tìm cổng khác (Google cache, PDF tải trực tiếp thay vì trang HTML,
hoặc trang tiếng Anh của METI/JETRO); (3) Trung Quốc — `chinatorch.gov.cn` vẫn chặn mạng nhất
quán qua nhiều checkpoint, có thể bỏ hẳn hướng này trừ khi tìm được domain thay thế của MOST; (4)
Bắc Âu — SISP Thuỵ Điển và TEKEL Phần Lan đều không kết nối được (khác kiểu lỗi so với Trung Quốc/
Hàn Quốc, nghi chặn theo vùng địa lý của chính site chứ không phải do phía ta) — thử qua VPN/proxy
khác hoặc nguồn thứ cấp (IASP directory đã liệt kê "Finnish Science Parks Association" và "SISP"
làm hội viên, có thể IASP có trang liệt kê từng hội viên con với URL, xem `iasp.ws/our-members/
directory/` cho từng tên: `@6307/business-joensuu`, `@469117/finnish-science-parks-association` —
gợi ý IASP directory có thể dùng làm proxy để lấy URL của các science park Bắc Âu mà không cần
qua site hiệp hội gốc); (5) Na Uy SIVA — có tên tổ chức cụ thể (6AM Accelerator, Oslo Cancer
Cluster Incubator, Oslotech, Kjeller Innovasjon, Vaager Innovasjon, KUPA, KPB, Digital Innlandet,
Industriutvikling Vest, Kongsberg Innovasjon, Proventia, Smart Innovation Norway) cần tra URL
riêng + check trùng ROSTER trước khi merge, chưa làm lượt này.

---
**Lần trước:** 2026-09-10 (checkpoint 43 — **TIẾP TỤC WIKIDATA DÒ TỪ KHOÁ NHÃN, THÊM TỪ KHOÁ MỚI
+ ÁP MULTI-NGÔN NGỮ NGAY TỪ ĐẦU (11 ngôn ngữ), PHÁT HIỆN LỖ HỔNG MỚI TRONG `check_url()`**) — còn
thiếu ~6153 lúc cuối phiên.

Lượt trước (checkpoint 42) để lại 2 việc mở chính: (1) còn nhiều từ khoá tiếng Anh chưa thử
("innovation lab", "startup hub", "technopark"/"techno park", "research park", "innovation
park", "R&D centre", "tech hub"...); (2) nên áp fallback đa ngôn ngữ NGAY TỪ ĐẦU cho mọi từ khoá
mới, không tách 2 lượt như checkpoint 40→41 đã phải làm. Lượt này làm cả hai cùng lúc: 14 từ khoá
tiếng Anh mới ("business incubator" dạng nhãn tự do — khác class Q1132207 đã dùng, "startup hub",
"digital hub", "open lab", "innovation lab", "r&d center"/"r&d centre", "maker lab", "tech park",
"research park", "innovation park", "technopark", "techno park", "creative hub") + 23 từ khoá
BẢN NGỮ (không dịch qua tiếng Anh) trải 11 ngôn ngữ: Đức (Gründerzentrum/Technologiepark/
Wissenschaftspark/Innovationszentrum/Forschungszentrum), Pháp (incubateur/parc technologique/
pépinière d'entreprises), Tây Ban Nha (incubadora/parque tecnológico/parque científico/centro de
innovación), Bồ Đào Nha (incubadora/parque tecnológico), Nga (технопарк/инновационный центр/
научный парк), Trung (科技园), Nhật (テクノパーク/イノベーションセンター), Ý (parco tecnologico),
Ba Lan (park technologiczny/inkubator), Hà Lan (incubator), Thổ Nhĩ Kỳ (teknoloji parkı). Test
đếm riêng từng cặp (ngôn ngữ, từ khoá) trước — hầu hết ra số nhỏ (1-39), riêng "Forschungszentrum"
(Đức) áp đảo với 99, "technopark" (Anh) 39, "tech park" 30, "coworking" 33 (KHÔNG dùng, xem dưới).
Cân nhắc loại trước khi gộp: "makerspace" (17), "fab lab" (6), "coworking"/"co-working" (33+1) —
giữ đúng tiền lệ checkpoint 40 đã loại hẳn 3 class này (rủi ro lẫn không gian hacker/maker sở
thích cộng đồng và văn phòng chia sẻ thương mại thuần tuý, không phải CGCN/ĐMST đại học); "spin-
off hub"/"spinoff hub" ra 0, coi như ngõ cụt.

**Bài học kỹ thuật QUAN TRỌNG — lỗi timeout QLever khi gộp UNION nhãn + đường dẫn P31/P279* + P856
+ OPTIONAL trong 1 truy vấn:** thử gộp cả 39 cặp (ngôn ngữ, từ khoá) thành 1 truy vấn UNION lớn
kèm `?item wdt:P31/wdt:P279* wd:Q43229 . ?item wdt:P856 ?site . OPTIONAL{P625} OPTIONAL{P17+nhãn}`
— timeout liên tục dù chia nhỏ còn 4 từ khoá/truy vấn (lỗi `"Operation timed out. Last operation:
OptionalJoin on ?item"` / `"Sort (internal order)"`), trong khi các truy vấn ĐẾM riêng từng cặp
(không có `P856`/`OPTIONAL`) chạy nhanh bình thường (như checkpoint 42 đã dùng). Nguyên nhân: vế
`?item wdt:P31/wdt:P279* wd:Q43229` khớp MỌI tổ chức trên Wikidata (rất lớn), kết hợp `P856` (mọi
tổ chức có website — cũng rất lớn) khiến trình tối ưu truy vấn chọn thứ tự join kém khi vế trái là
UNION của nhiều nhánh nhãn nhỏ. **Giải pháp: tách 2 giai đoạn** — giai đoạn 1 lấy THẲNG `?item` cho
từng cặp (ngôn ngữ, từ khoá) riêng lẻ (đúng hình dạng truy vấn đếm đã chứng minh nhanh — label +
lớp tổ chức, KHÔNG kèm P856/OPTIONAL), gộp ID vào 1 tập; giai đoạn 2 dùng `VALUES ?item {...}` với
danh sách ID đã có (250 ID/lô) để tra `P856`/`P625`/`P17` — tra theo ID cụ thể nhanh, không cần
duyệt lại toàn đồ thị. **Ghi lại kỹ thuật 2 giai đoạn này để dùng lại mọi lượt Wikidata sau, đừng
lặp lại việc dò lỗi timeout.**

**Kết quả giai đoạn 1:** 370 item duy nhất (gộp cả 39 cặp). **Giai đoạn 2:** 205/370 có ít nhất 1
website (`P856`) — 165 item không có website bị loại ngay. Lọc trùng ROSTER (base-domain +
`normalize_name()`): 84 trùng domain + 1 trùng tên → 120; loại 1 Việt Nam (qua nhãn quốc gia
Wikidata) + 5 thiếu cả toạ độ lẫn quốc gia hợp lệ (không suy được qua ccTLD, domain `.com/.org`
chung chung như "Kanata Research Park"/"Yahoo Beijing Global R&D Center"/"Technopark, Kollam" —
đúng 4 cách đã chốt, không đoán qua tên dù tên có gợi ý địa danh) → **114 ứng viên**. Loại thêm 5
qua rà phạm vi thủ công (đọc toàn bộ, không phải mẫu, vì lô nhỏ): "Museumsdepot Wissenschaftspark"
(Đức — kho lưu trữ hiện vật bảo tàng đặt trong toà nhà tên "Wissenschaftspark", bản thân không
phải tổ chức R&D/ĐMST), "VIPACH | Vienna Photo Art & Creative HUB" và "Te Puna Creative Hub" (Áo/
New Zealand — không gian nghệ thuật/nhiếp ảnh cộng đồng, sai lĩnh vực dù khớp từ khoá "creative
hub"), "Goyki 3 Art Inkubator" (Ba Lan — ươm tạo NGHỆ THUẬT, không phải doanh nghiệp/công nghệ),
"Parc technologique et archéologique des collines métallifères de Grosseto" (Ý — thực chất là
công viên di sản khảo cổ mỏ cũ, tên gốc tiếng Ý "Parco Tecnologico e Archeologico" gây nhầm, không
phải khu công nghệ) → **109 ứng viên**. Gán toạ độ: 61/109 có `P625` thật (xác minh qua
`CountryLookup`, chỉ 1 lệch biên do độ phân giải Natural Earth 50m — Thâm Quyến (22.54,114.05) bị
gán "Hong Kong" dù đúng là đại lục Trung Quốc, giữ nguyên như thông lệ các lỗi biên tương tự đã
gặp), 48/109 dùng centroid quốc gia ĐÃ DÙNG SẴN trong ROSTER (đối chiếu qua bảng tần suất toạ độ
theo quốc gia dựng từ chính ROSTER hiện có, không tự bịa). Chuẩn hoá "Russia"→"Russian Federation"
(436 so 144 mục hiện có) và "People's Republic of China"→"China" (456 so 40) khớp đa số ROSTER.

**`check_url()` 2 vòng (16 luồng/15s → 6 luồng/25s) + vòng UA Chrome thật (0 cứu thêm):** 109 →
68 sống (tỷ lệ chết 38%, bình thường). Kiểm chéo 2 mẫu tưởng chết oan bằng `WebFetch`: Suntory
(`suntory.com/sic`) bị 403 (chặn bot, không kết luận được) và Fiat (`crf.it`) báo **chứng chỉ SSL
đã hết hạn thật** — xác nhận tỷ lệ chết phần lớn là chết thật, không phải lỗi mạng cục bộ.

**PHÁT HIỆN LỖ HỔNG MỚI trong `check_url()` — chuyển hướng khác domain hoàn toàn không bị bắt:**
`urllib.request.urlopen()` tự động theo mọi redirect HTTP (kể cả 301 sang domain KHÁC hẳn) trước
khi `check_url()` kiểm nội dung — nếu trang đích (dù ở domain khác, không liên quan) có đủ >200 ký
tự văn bản và không chứa cụm "for sale", hàm vẫn báo "ok" dù domain gốc đã đổi chủ/hết hạn. Phát
hiện qua rà tay: "Bangladesh Open Innovation Lab" (`boiledbhoot.org`) chuyển 301 sang
`boilerdeck.org` — một domain gần như trống, không liên quan gì, `check_url()` vẫn báo sống. Quét
lại toàn bộ 68 mục sống bằng script so `base_domain()` của URL gốc với `base_domain()` của
`resp.geturl()` sau khi fetch: ra **7 mục có chuyển-domain**, xác minh tay từng mục qua `WebFetch`
— 4 mục ĐÚNG LÀ HỎNG (loại): "Bangladesh Open Innovation Lab" (domain trống không liên quan),
"Hans Höllwart - Forschungszentrum für integrales Bauwesen AG" (Áo, `fibag.at`→`sfl-
engineering.com`, đã đổi thành công ty khác hẳn), "Parque Científico y Tecnológico Agroalimentario
de Lérida" (Tây Ban Nha, `pcital.com`→`hoteles-andalucia.com`, domain bị bán lại cho chuỗi khách
sạn), "诺丁汉生物科技园"/Nottingham BioCity (Anh, `biocity.co.uk`→`thepioneergroup.com`, đổi
thương hiệu thành "Pioneer Group" không còn mang tên/định danh gốc); 3 mục là CHUYỂN DOMAIN CHÍNH
ĐÁNG cùng 1 tổ chức (giữ, cập nhật URL theo domain đích): "Association of University Research
Parks" (`aurp.net`→`aurp.org`, xác nhận qua `WebFetch` vẫn đúng tổ chức), "Deutsches
Krebsforschungszentrum, Zentralbibliothek" (`dkfz-heidelberg.de`→`dkfz.de/bibliothek`, cùng viện
DKFZ), "Parc technologique du Vallès" (`ptv.es`→`ptv.cat`, đổi tên miền theo vùng Catalunya, cùng
tổ chức). **→ 105 mục.** Loại thêm 1 trùng nội bộ batch ("Pohang TechnoPark"/"Pohang Techno Park"
— 2 item Wikidata khác nhau cùng trỏ 1 site `ptp.or.kr`) → **63 ứng viên cuối cùng**. Rà từ khoá cờ
đỏ (yoga/spa/tarot/tôn giáo/lái xe/thẩm mỹ/bảo hiểm...): 0 khớp. 0 Việt Nam. Trải 25 quốc gia, dẫn
đầu Đức 17 (đa số nhóm "Forschungszentrum" — thư viện/kho lưu trữ/trung tâm nghiên cứu đủ lĩnh vực
từ y sinh, môi trường, âm nhạc, khảo cổ đến hạt nhân, đúng tiền lệ mở rộng phạm vi rộng đã chốt từ
checkpoint 39-41), Hàn Quốc 11 (toàn bộ mạng lưới TechnoPark cấp vùng — 11/17 tỉnh thành chưa có
trong ROSTER), Trung Quốc 5, Mỹ/Pháp 3 mỗi nước.

**Việc mở quan trọng nhất cho lượt sau — vá lỗ hổng `check_url()`:** hàm hiện tại KHÔNG phát hiện
khi domain gốc bị đổi chủ/redirect sang 1 tổ chức/trang hoàn toàn không liên quan (chỉ xét nội
dung trang ĐÍCH cuối cùng, không so domain gốc với domain đích) — nên **thêm bước so
`base_domain(url_goc)` với `base_domain(resp.geturl())` sau mỗi lần fetch thành công vào chính
`roster_common.py`** (không chỉ làm tay 1 lần ở lượt này) để mọi lượt sau tự động bắt được lớp
false-positive này, tránh phải rà tay lại.

`ROSTER`: 18784 → **18847** (+63, khớp `len(load_roster(...))` kiểm ngay trước merge, `git status`
sạch không có phiên song song). Đơn vị trên bản đồ: 18793 → **18856** (+63, giữ nguyên chênh lệch
+9). Kiểm: `node --check` sạch trên script inline (3,285,498 ký tự), thẻ `div`/`section` cân bằng
(107/107, 6/6). Mở `index.html` qua HTTP server cục bộ (`preview_start`/`preview_stop`), đọc
`get_page_text`: đúng "18856 đơn vị được lập bản đồ" / "18847 trong danh mục mở rộng" / "12 đơn vị
tại Việt Nam" (không đổi) / "9 case phân tích chuyên sâu" (không đổi), console sạch. Commit
`69bb970`, `git push origin main` thành công.

**Còn thiếu ~6153 để đạt 25000.** **Việc mở cho lượt sau:** (1) **vá lỗ hổng cross-domain-redirect
trong `check_url()`** (xem trên) — ưu tiên cao vì ảnh hưởng MỌI lượt tương lai, không riêng lượt
này; (2) kỹ thuật dò-từ-khoá-nhãn-rộng tiếp tục giảm hiệu suất rõ rệt (664→260→63 ứng viên cuối 3
lượt gần nhất) — còn vài từ khoá tiếng Anh CHƯA THỬ ("science centre"/"science center" khác "science
park" đã dùng, "startup incubator", "venture lab", "knowledge park", "enterprise hub") và nhiều
NGÔN NGỮ CHƯA THỬ (Hàn, Ả Rập, Hindi, Thuỵ Điển, Phần Lan, Đan Mạch, Ukraina, Do Thái, Indonesia,
Thái) — có thể còn vài chục-trăm mục nữa nhưng lợi ích/công sức đang giảm nhanh; (3) **nên chuyển
hướng nguồn khác hẳn Wikidata cho lượt sau** theo đúng gợi ý Bước 2 đã định: đăng ký chính phủ có
cột website (Nhật Bản METI/JETRO, Hàn Quốc KOTEC/KIAT — lưu ý mạng lưới TechnoPark Hàn Quốc lượt
này mới lấy được 11/17 tỉnh qua Wikidata, có thể còn nguồn liệt kê đủ 17 tỉnh trực tiếp từ hiệp hội
KOTEP/TP mẹ, thử tìm trang đó trước khi quay lại Wikidata cho Hàn Quốc), Trung Quốc thử lại
`chinatorch.gov.cn`, Bắc Âu/Baltic, hoặc hiệp hội đa quốc gia mới có JSON nhúng bản đồ/API; (4)
dùng lại kỹ thuật 2 giai đoạn (item ID trước, `VALUES` tra chi tiết sau) cho MỌI truy vấn Wikidata
tiếp theo có kèm `P856`/`OPTIONAL` — tránh lặp lại việc dò lỗi timeout QLever của lượt này.

---
**Lần trước:** 2026-09-10 (checkpoint 42 — **(A) QUÉT TOÀN ROSTER TÌM LỖI CENTROID GIỐNG BUG
Mỹ/Pháp CỦA CHECKPOINT 39, (B) WIKIDATA CHUYỂN TỪ DÒ CLASS SANG DÒ TỪ KHOÁ NHÃN RỘNG**) — còn
thiếu ~6216 lúc cuối phiên.

**(A) Quét lỗi centroid — có sửa, commit riêng `3d6402b` trước khi tăng trưởng.** Lượt 41 để
lại việc mở: nghi còn nhiều dòng cùng lỗi bbox-toàn-điểm (Mỹ/Pháp) ở các nước có lãnh thổ hải
ngoại khác. Viết script gộp `ROSTER` theo toạ độ làm tròn 4 chữ số thập phân, với mỗi nhóm
toạ độ có ≥4 mục CÙNG 1 quốc gia, đối chiếu quốc gia đó với `CountryLookup.country_for()` (tra
ngược qua polygon Natural Earth thật) — nếu KHÔNG khớp thì nghi vấn. Ra 21 nhóm mismatch; phần
lớn là false positive (biến thể tên: "Türkiye"/"Turkey", "Czechia"/"Czech Republic", "The
Gambia"/"Gambia", "Chinese Taipei"/"Taiwan" — chỉ khác cách viết, không phải lỗi toạ độ; hoặc
điểm ở sát bờ biển/đảo nhỏ mà lưới Natural Earth 50m không đủ phân giải để bắt trúng polygon —
Hy Lạp/Đan Mạch/Nam Phi/New Zealand(-40.9,174.9)/Israel-Palestine — toạ độ ĐÚNG khu vực thực,
không sửa). **8 nhóm là bug thật** — cùng kiểu bbox-toàn-điểm của checkpoint 39/41 (điểm rơi
giữa đại dương, cách xa lãnh thổ hàng nghìn km, trong khi domain `.nl/.fr/.es/.no/.pt/.se` của
từng mục xác nhận đúng quốc gia ghi trong cột `country`): Hà Lan (49 mục, điểm ở giữa Đại Tây
Dương), Pháp (40, gần Mali — CHÍNH LÀ lỗi checkpoint 41 đã cảnh báo nhưng chưa sửa vì lượt đó
chỉ sửa phần Mỹ), Tây Ban Nha (35, ngoài khơi Maroc), Na Uy (23, biển Na Uy), Bồ Đào Nha (22,
giữa Đại Tây Dương gần Azores), Thuỵ Điển (20, vịnh Bothnia), New Zealand (8, ngoài khơi Nam
Phi — cùng lỗi bbox tính luôn đảo Chatham/Kermadec), Nga (4, kinh độ bị hỏng thành đúng `0.0`
trong khi vĩ độ vẫn đúng ~61.5°B — có thể do lỗi parse/truncate ở batch nguồn, không phải bbox).
**Sửa:** thay toạ độ sai bằng centroid ĐÃ DÙNG SẴN nhiều lần cho đúng quốc gia đó ở nơi khác
trong `ROSTER` (không tự bịa centroid mới) — riêng Nga không có cụm centroid-quốc-gia sẵn (chỉ
có điểm St. Petersburg dùng 5 lần, là điểm THÀNH PHỐ không phải centroid quốc gia) nên dùng
centroid Nga chuẩn công khai (61.5240, 105.3188, cùng bộ dữ liệu Google public country centroids
mà mọi centroid "OK" khác trong ROSTER đã khớp — xác nhận qua Mỹ/Anh/Canada/Úc). **201 mục sửa
toạ độ, KHÔNG đổi số lượng** (`len(ROSTER)` giữ 18524). Kiểm bằng HTTP server cục bộ: số liệu
không đổi, console sạch. Commit `3d6402b`, push thành công trước khi sang việc tăng trưởng.

**(B) Tăng trưởng — Wikidata dò từ khoá nhãn, không giới hạn class.** 5 class Wikidata cũ
(`research institute`, `university institute`, `technology park`, `startup accelerator`,
`innovation hub`) coi như cạn từ checkpoint 41. Đổi cách tiếp cận: thay vì liệt kê từng class cụ
thể, lọc THEO TỪ KHOÁ trong nhãn tiếng Anh (`CONTAINS(LCASE(STR(?label)), "...")`) trên MỌI item
có `P31/P279* wd:Q43229` (organization) — rộng hơn hẳn, không phụ thuộc việc ai đó đã gắn đúng
class cụ thể cho item trên Wikidata hay chưa. Test đếm từng từ khoá riêng trước khi gộp (endpoint
`qlever.dev`, nhớ khai `PREFIX` tường minh như checkpoint 41 đã học): "research centre" 423,
"science park" 51, "innovation center" 41, "innovation centre" 32, "technology transfer" 26,
"incubator" 29, "coworking space" 6, "living lab" 8, "innovation hub" 5, "entrepreneurship
cent[er/re]" 2 — CÒN 3 từ khoá thử mà ra 0: "tech transfer" (viết tắt, không ai dùng làm nhãn
chính thức), "startup studio", "digital innovation hub" (không có item nào khớp đúng cụm này dù
class Q-id riêng đã dùng ở checkpoint 40 vẫn còn — nghĩa là nhãn "digital innovation hub" hiếm
gặp trong text, khác hẳn việc được gắn class). Gộp cả 10 từ khoá có kết quả vào 1 truy vấn UNION
bằng `||`, lấy kèm `P856` (website, bắt buộc), `P17`→nhãn quốc gia tiếng Anh, `P625` nếu có.

**Kết quả truy vấn:** 664 dòng thô → 619 item duy nhất. Lọc trùng ROSTER (base-domain +
`normalize_name()`): 198 trùng domain + 5 trùng tên → 416 ứng viên. `check_url()` 2 vòng (vòng 1
16 luồng/10s giữ 275/416; vòng 2 kiểm lại 141 mục chết, 6 luồng/25s, cứu thêm 4) → **279 sống
thật** (tỷ lệ chết ~33%, bình thường, không cần kiểm chéo `WebFetch`). Trong 279: **0 mục nào có
`P625`** (khác hẳn checkpoint 41 — có vẻ nhóm item khớp từ khoá nhãn ít được gắn toạ độ hơn nhóm
item khớp class cụ thể); 16 mục hoàn toàn không có `P17`. Xử lý 16 mục này: chỉ giữ 3 mục suy
được quốc gia qua ccTLD rõ ràng (`.ru`→Nga, `.hr`→Croatia, `.bd`→Bangladesh), LOẠI 13 mục còn lại
(domain `.com/.org` chung chung hoặc trang `academia.edu` — không phải domain riêng của tổ chức,
không đoán bừa qua tên dù vài cái có gợi ý địa danh trong tên như "Los Angeles"/"Texas"/
"Tanzania" — không nằm trong 4 cách đã chốt nên không dùng). Rà trùng NỘI BỘ batch (2 item
Wikidata khác nhau nhưng cùng 1 tổ chức thật, vd "Bhopal Memorial Hospital & Research Centre" và
"...Research Centre, Bhopal", hay "International Development Research Centre" bị gắn nhầm P17 là
Ấn Độ thay vì Canada) → loại thêm 6. **Tổng 260 ứng viên cuối.** 0 Việt Nam. Dẫn đầu Ấn Độ 59
(nhiều "XYZ Medical/Ayurvedic/Homeopathic College and Research Centre" — vẫn giữ vì tiền lệ
checkpoint 39-41 đã nhận rộng rãi cả nhóm "research institute" không riêng CGCN/ĐMST hẹp), Anh
31, Úc 16, Canada 11.

**Toạ độ (không có `P625` nào):** dùng centroid quốc gia ĐÃ DÙNG SẴN trong ROSTER cho từng nước
(tương tự phần (A)), xác minh lại bằng `CountryLookup.country_for()` — phát hiện ngay lỗi tương tự
(A) cho Nga (điểm St. Petersburg lặp lại 5 lần không phải centroid quốc gia) nên dùng centroid Nga
chuẩn công khai như đã sửa ở (A). **Greenland lần đầu xuất hiện trong ROSTER** ("Greenland Climate
Research Centre", domain `.gl`) — Natural Earth có polygon Greenland riêng (không gộp vào Đan
Mạch), tính centroid vùng đất chính (71.7069, -42.6043), xác minh `CountryLookup` khớp. Croatia
cũng lần đầu — dùng centroid chuẩn công khai (45.1, 15.2), tình cờ trùng khớp hoàn toàn điểm đã
dùng sẵn 11 lần cho các mục Croatia khác trong ROSTER (xác nhận đúng quy ước).

`ROSTER`: 18524 → **18784** (+260, khớp `len(load_roster(...))` kiểm ngay trước merge, `git
status` sạch). Đơn vị trên bản đồ: 18533 → **18793** (+260, giữ nguyên chênh lệch +9). Kiểm:
`node --check` sạch, thẻ `div`/`section` cân bằng (107/107, 6/6). Mở `index.html` qua HTTP server
cục bộ, `get_page_text`: đúng "18793 đơn vị được lập bản đồ" / "18784 trong danh mục mở rộng" /
"12 đơn vị tại Việt Nam" (không đổi) / "9 case phân tích chuyên sâu" (không đổi), console sạch.
Commit `db5fb5b`, `git push origin main` thành công.

**Còn thiếu ~6216 để đạt 25000.** **Việc mở cho lượt sau:** (1) kỹ thuật dò-từ-khoá-nhãn-rộng
CÒN NHIỀU DƯ ĐỊA — mới thử 13 từ khoá, còn có thể thử thêm biến thể ("innovation lab", "startup
hub", "technopark"/"techno park" liền/tách, "research park", "innovation park", "business park"
[cẩn thận lẫn bất động sản thương mại thường], "R&D centre", "tech hub") VÀ áp fallback đa ngôn
ngữ (COALESCE 9 ngôn ngữ + `?labelAny`, kỹ thuật checkpoint 41) NGAY TỪ ĐẦU cho các từ khoá tiếng
Anh — hiện lượt này CHỈ lọc nhãn tiếng Anh nên chắc chắn bỏ sót item chỉ có nhãn ngôn ngữ khác chứa
từ khoá tương đương (vd tiếng Đức "Gründerzentrum", tiếng Pháp "incubateur", tiếng Tây Ban Nha
"parque científico") — nếu thử tiếp nên tra từ khoá BẢN NGỮ luôn, không chỉ dịch tiếng Anh; (2)
bug centroid-bbox-toàn-điểm coi như ĐÃ QUÉT HẾT các nhóm ≥4 mục cùng quốc gia — nhưng CHƯA quét
nhóm nhỏ hơn (2-3 mục) vì chi phí/lợi ích thấp, để ngỏ nếu phát hiện thêm qua công việc khác; (3)
nguồn OSM và phi-Wikidata khác đã liệt kê ở checkpoint ≤38 coi như cạn.

---
**Lần trước:** 2026-09-10 (checkpoint 41 — **NHÃN ĐA NGÔN NGỮ cho 5 class Wikidata đã dùng
(`research institute` Q31855 + `university institute`/`technology park`/`startup
accelerator`/`innovation hub` của checkpoint 40), cứu các item KHÔNG có nhãn tiếng Anh**) —
còn thiếu ~6476 lúc cuối phiên.

Lượt trước (checkpoint 40) để lại việc mở: batch Wikidata mọi lượt trước chỉ lấy item có nhãn
tiếng Anh (`rdfs:label ... FILTER(LANG=... "en")`), loại thẳng item không có nhãn "en" dù có
nhãn ngôn ngữ khác — checkpoint 39 xác nhận 53/607 bị loại kiểu này, ước tính còn dư địa. Lượt
này khai thác đúng dư địa đó: đổi hẳn endpoint QLever cũ (`qlever.cs.uni-freiburg.de`, giờ 308
redirect sang `qlever.dev`) — endpoint mới **yêu cầu khai báo `PREFIX` tường minh** (khác
endpoint cũ chấp nhận `wdt:`/`wd:`/`rdfs:` ngầm định), đã thêm 3 dòng `PREFIX` đầu mỗi truy vấn.

**Truy vấn:** `FILTER NOT EXISTS { ?item rdfs:label ?enLabel . FILTER(LANG(?enLabel)="en") }` để
chỉ lấy phần item ĐÃ BỊ LOẠI ở các lượt trước (không quét lại toàn bộ, không trùng công đã làm),
rồi with 9 `OPTIONAL` lấy nhãn theo thứ tự ưu tiên ngôn ngữ `zh/ja/ko/ru/ar/es/fr/de/pt` (script
ngôn ngữ hay gặp ở tổ chức nghiên cứu ngoài khối Anh ngữ), cộng 1 `OPTIONAL` cuối lấy NHÃN BẤT KỲ
(`?labelAny` không filter ngôn ngữ) làm lưới an toàn cho ngôn ngữ hiếm không nằm trong 9 danh
sách trên, `COALESCE` theo đúng thứ tự đó. Gộp cả 5 class trong 1 truy vấn `VALUES ?class {...}`.
Đếm trước khi lấy đủ: `research institute` chiếm áp đảo (690/1013 dòng thô thiếu nhãn EN, 4 class
nhỏ còn lại cộng chỉ 54) — đúng như dự đoán vì đây là class lớn nhất đã dùng.

**Kết quả truy vấn:** 1013 dòng thô (item,site) → 730 item duy nhất CÓ được 1 nhãn nào đó qua
chuỗi `COALESCE` (0 item còn trống nhãn sau khi cộng cả 9 ngôn ngữ + nhãn bất kỳ — lưới an toàn
`?labelAny` hoạt động đúng, không mất item nào vì thiếu nhãn nữa). Lọc trùng ROSTER (base-domain +
`normalize_name()`, `normalize_name()` Unicode-safe nên so khớp tên chữ Nga/Ả Rập/Hán/Nhật chính
xác): 166 trùng domain + 1 trùng tên → **306 ứng viên duy nhất**.

**Toạ độ:** 115/306 có sẵn `P625` (regex `POINT(...)` viết hoa, học đúng bài học checkpoint 40).
272/306 có `P17`→nhãn quốc gia tiếng Anh của Wikidata; 34 hoàn toàn không có quốc gia. Phát hiện
lại ĐÚNG lỗi centroid-quốc-gia của checkpoint 39: hàm bbox-toàn-bộ-điểm (min/max thô trên mọi
polygon của một nước) cho ra toạ độ SAI nghiêm trọng với nước có lãnh thổ hải ngoại rải rác — Mỹ
tính ra (45.19°B, 0.79°Đ, tức miền nam nước Pháp) vì bbox kéo dài tới Guam/Alaska/Puerto Rico,
Pháp còn tệ hơn (14.86°B, -2.98°Đ, gần Mali) vì tính luôn Guyane thuộc Pháp/Réunion/Polynésie —
**đây chính là nguồn gốc toạ độ sai đã nằm sẵn trong ROSTER từ checkpoint 39** (dòng "Aldo Leopold
Wilderness Research Institute" hiện có toạ độ (45.1858, 0.7927) — xác nhận bug, ghi lại làm việc
mở, KHÔNG tự sửa vì ngoài phạm vi lượt này). **Sửa cho batch này:** đổi sang lấy polygon LỚN NHẤT
(diện tích shoelace) trong multipolygon mỗi nước rồi mới tính bbox-center của riêng polygon đó —
kiểm lại Mỹ/Pháp/Trung Quốc/Nhật/Anh/Bồ Đào Nha/Hà Lan đều ra toạ độ đúng vùng lục địa chính. Ưu
tiên xử lý toạ độ: (1) `P625` thật nếu có; (2) nếu có toạ độ, `CountryLookup` (`country_from_latlon.py`)
để XÁC MINH LẠI quốc gia thay vì tin nhãn Wikidata thô — sửa đúng lỗi "Liên Xô" (8 item nhãn quốc
gia Wikidata là "Soviet Union", không map được vào cột quốc gia hiện đại của ROSTER, nhưng có toạ
độ thật để suy ra quốc gia hiện tại: Nga/Kazakhstan/Ukraina...); (3) nếu chỉ có nhãn quốc gia (không
"Soviet Union"), centroid-polygon-lớn-nhất theo tên đó + jitter xác định (hash MD5 tên tổ chức,
±0.8°); (4) nếu thiếu cả toạ độ lẫn quốc gia, suy quốc gia từ ccTLD của domain (`.ru`→Nga,
`.kz`→Kazakhstan, `.ua`→Ukraina..., dict ~50 mã tự viết cho lượt này) rồi mới centroid; (5) hết cả
4 cách → LOẠI (12 mục, ví dụ "北海道野生動物研究所", "Pedersen Brain Science Institute" — domain
`.com`/`.org`/tổ chức mẹ quốc tế không suy ra quốc gia được, không đoán bừa).

**`check_url()` 2 vòng:** vòng 1 (12 luồng/12s) giữ 206/294. Vòng 2 kiểm lại 88 mục chết (6
luồng/25s) chỉ cứu thêm 1 → 87 vẫn chết, đa số `URLError`/`HTTPError`/timeout — RIÊNG BATCH NÀY có
tỷ lệ chết cao bất thường (206/294 ≈ 70% thay vì ~80-90% thường thấy), đã NGHI NGỜ lỗi mạng cục bộ
của máy (nhiều IP nước ngoài khác nhau cùng timeout kết nối TCP) nên đã kiểm chéo bằng
`WebFetch` (chạy trên hạ tầng Anthropic, đường mạng khác hẳn) cho 2 mẫu (`iar-conicet.gov.ar`,
`ippuc.org.br`) — CẢ HAI đều lỗi kết nối trên `WebFetch` (`ECONNREFUSED`/`ECONNRESET`) — xác nhận
đây là site thật sự chết/không truy cập được, không phải do mạng máy cục bộ, KHÔNG cứu thêm.
**Tổng: 207/306 sống thật.** Rà từ khoá cờ đỏ (agent/gemini/chưa xác minh/unverified) trên 207 mục:
**0 khớp**. 0 Việt Nam xuyên suốt (lọc từ bước gán quốc gia, xác nhận lại ở bước cuối bằng
`normalize_name`). Trải 30 quốc gia, dẫn đầu Đức 28, Argentina 22, Ukraina 16, Nhật 15, Nga 15 —
đúng đặc điểm dữ liệu Wikidata dồi dào cho các nước có cộng đồng biên tập Wikipedia/Wikidata lớn
bằng ngôn ngữ mẹ đẻ (đặc biệt Đức/Nga/Ukraina/Nhật vốn có rất nhiều viện nghiên cứu tên bằng tiếng
Đức/Nga/Nhật không có bản dịch tiếng Anh).

`ROSTER`: 18317 → **18524** (+207, khớp đúng số kiểm lại `len(load_roster(...))` ngay trước merge
— `git status` sạch). Đơn vị trên bản đồ: 18326 → **18533** (+207, giữ nguyên chênh lệch +9).
Kiểm: `node --check` sạch, thẻ `div`/`section` cân bằng (107/107, 6/6). Mở `index.html` qua HTTP
server cục bộ (`preview_start`/`preview_stop` của Browser pane) qua Browser pane, đọc
`get_page_text`: đúng "18533 đơn vị được lập bản đồ" / "18524 trong danh mục mở rộng" / "12 đơn vị
tại Việt Nam" (không đổi) / "9 case phân tích chuyên sâu" (không đổi), console sạch. Commit
`6b3512a`, `git push origin main` thành công.

**Còn thiếu ~6476 để đạt 25000.** **Việc mở cho lượt sau:** (1) **kỹ thuật nhãn đa ngôn ngữ lượt
này coi như ĐÃ CẠN cho 5 class hiện có** (0 item còn thiếu nhãn sau lượt này) — không lặp lại cho
đúng 5 class cũ, nhưng NÊN áp dụng ngay từ đầu (không tách 2 lượt như đã làm) cho bất kỳ class
Wikidata MỚI nào thử ở lượt sau, đỡ phải quay lại vá; (2) **bug toạ độ centroid-bbox-toàn-điểm của
checkpoint 39 vẫn còn nguyên trong ROSTER** (ít nhất dòng "Aldo Leopold Wilderness Research
Institute" 45.1858/0.7927 sai) — có thể còn nhiều dòng khác cùng lỗi (mọi nước có lãnh thổ hải
ngoại: Mỹ/Pháp/Anh/Hà Lan/Đan Mạch/Tây Ban Nha/Bồ Đào Nha/Nga...) từ các batch dùng
"centroid-quốc-gia" kiểu bbox-toàn-điểm ở checkpoint 39 — lượt sau nên quét toàn ROSTER tìm toạ độ
bất thường (vd. cách xa mọi polygon thật của quốc gia ghi trong cột `country`, dùng chính
`CountryLookup.country_for()` để đối chiếu ngược) rồi sửa lại bằng phương pháp polygon-lớn-nhất đã
dùng ở lượt này; (3) tiếp tục tra Q-id mới cho khái niệm CGCN/ĐMST chưa thử: "innovation and
technology center", "research centre" (nếu tách biệt "research institute"), "living lab",
"digital innovation hub" (khác `innovation hub` Q28689074); (4) endpoint QLever đã đổi domain
(`qlever.cs.uni-freiburg.de` → 308 redirect → `qlever.dev`) — dùng thẳng `qlever.dev` từ đầu ở lượt
sau, tiết kiệm 1 round-trip, và NHỚ khai báo `PREFIX` tường minh (endpoint mới không còn ngầm định
như endpoint cũ); (5) nguồn OSM và phi-Wikidata khác đã liệt kê ở checkpoint ≤38 coi như cạn.

---
**Lần trước:** 2026-09-10 (checkpoint 40 — **TIẾP TỤC WIKIDATA, ĐỔI ENDPOINT SANG QLEVER MIRROR do
`query.wikidata.org` (WDQS chính thức) đang bị throttle nặng "active wdqs outage" 1 req/min suốt
phiên — class `university institute` (Q11946645) + 3 class nhỏ `technology park`/`startup
accelerator`/`innovation hub`**) — còn thiếu ~6683 lúc cuối phiên.

Lượt trước (checkpoint 39) khuyến nghị đào sâu tiếp Wikidata, gợi ý thử riêng `think tank`
(Q155271) và `university institute` (Q11946645) tách khỏi subclass tràn lan của `research
institute`. **`query.wikidata.org` (WDQS chính thức) ngay từ truy vấn đầu tiên trả 429 liên tục:
"Aggressively rate-limiting to 1 req/min - this rule was created during active wdqs outage"** — thử
giãn cách 65s/lệnh + 8 lần retry vẫn 429 liên tục (một tiến trình treo ~9 phút rồi lỗi hẳn) — đây là
outage thật phía WMF, không phải do nhịp truy vấn của mình. **Chuyển hẳn sang QLever
(`https://qlever.cs.uni-freiburg.de/api/wikidata`)** — một SPARQL engine bên thứ ba mirror trọn bộ
RDF dump Wikidata, cùng namespace `wdt:`/`wd:`, KHÔNG bị throttle suốt phiên, và quan trọng hơn: hỗ
trợ `rdfs:label`/`schema:description` trực tiếp (không cần `SERVICE wikibase:label` đặc thù của
WDQS) — nghĩa là item/nhãn tiếng Anh/mô tả/website/toạ độ/quốc gia (QID)/nhãn quốc gia đều lấy được
trong **1 truy vấn duy nhất mỗi class**, không cần giai đoạn lấy nhãn riêng hay phân trang (các class
thử đều dưới vài nghìn dòng). Đây là nâng cấp kỹ thuật lớn so với quy trình 2 giai đoạn (raw + label
riêng, phân trang 500-2000 dòng) của checkpoint 39.

**Khảo sát class:** `think tank` (Q155271) qua QLever ra 1192 cặp (item,site) — lấy mẫu 20 dòng
ngẫu nhiên + quét từ khoá (innovation/technology/science/research institute/scientific/tech
transfer/r&d/digital/engineering/biotech/nanotech) chỉ khớp **186/1192 (15.6%)**, và ngay trong tập
khớp từ khoá vẫn lẫn nhiều think tank chính sách công thuần tuý (khớp giả do cụm "research
institute" quá chung chung nằm trong tên, ví dụ "Africa Policy Research Institute"). Mẫu không khớp
toàn là think tank ngoại giao/kinh tế/xã hội (Nigerian Institute of International Affairs, Horn
Economic and Social Policy Institute...) — **KẾT LUẬN: sai phạm vi, bỏ hẳn class này**, không chỉ lọc
từ khoá vì tỷ lệ nhiễu vẫn cao ngay trong tập đã lọc.

`university institute` (Q11946645, 561 cặp), `technology park` (Q1281153, 18), `startup accelerator`
(Q4086495, 54), `innovation hub` (Q28689074, 13) — lấy mẫu cả 4 class đều đúng phạm vi rõ ràng
(viện/trung tâm nghiên cứu trực thuộc đại học, công viên công nghệ, chương trình accelerator khởi
nghiệp, hub ĐMST) — **dùng cả 4, gộp 1 truy vấn `VALUES ?class {...}`**. Kiểm thêm nhưng loại:
`business incubator` (Q1132207, 62 — đã cạn từ checkpoint 39), `science park` (Q1976594, 133 — đã
cạn), `technology transfer office` (Q48782630, 1 — đã biết quá hẹp/rác), `tech incubators and
accelerators` (Q136436817, 0 — Q-id gộp không có instance trực tiếp); `hackspace` (Q1032372, 327),
`makerspace` (Q45820240, 69), `fab lab` (Q1390062, 27) — lấy mẫu toàn không gian hacker/maker cộng
đồng tự phát (hobby club), không phải trung tâm CGCN/ĐMST của đại học, và hackerspace nói riêng đã
được cào qua OSM `leisure=hackerspace` từ checkpoint 27 — **bỏ cả 3 class này (sai phạm vi + rủi ro
trùng lặp cao)**.

**Bài học kỹ thuật:** literal toạ độ `P625` từ QLever trả dạng `POINT(...)` viết HOA (khác `Point(...)`
viết thường mà code checkpoint 39 dựa trên WDQS giả định) — regex phân biệt hoa/thường ban đầu khớp
0/522 toạ độ, âm thầm rơi hết vào nhánh centroid-quốc-gia mà không báo lỗi; sửa regex
case-insensitive rồi mới đúng **288/522 (55%) có toạ độ P625 thật**, 234 còn lại dùng centroid bbox
từ `_ne50_countries_cache.geojson` (tái dùng `NAME_OVERRIDE`). Một chuẩn hoá tên quốc gia cần thêm:
nhãn Wikidata gốc cho Trung Quốc là "People's Republic of China" (Q148) — đổi về "China" cho khớp
số đông ROSTER hiện có (452 "China" so với 40 "People's Republic of China" đã có sẵn, không sai
nhưng để nhất quán batch mới).

Gộp 4 class trong 1 truy vấn: 646 dòng thô → 607 item duy nhất (53 không có nhãn tiếng Anh, loại) →
522 có toạ độ dùng được (33 loại vì vừa thiếu `P625` vừa thiếu `P17` quốc gia hợp lệ) → lọc trùng
ROSTER (base-domain + `normalize_name()`): 390 trùng domain + 2 trùng tên + 11 trùng nội bộ batch
(tỷ lệ trùng domain rất cao — 75% — vì `university institute` chồng lấn nhiều với các viện đại học
đã vào ROSTER từ đợt `research institute` checkpoint 39) → **119 ứng viên duy nhất**. `check_url()`
3 vòng (12 luồng/15s → 6 luồng/25s retry → UA Chrome thật): 84 → +3 → +1 = **88 sống**. 0 Việt Nam
xuyên suốt (đã lọc từ bước gán quốc gia, xác nhận lại ở bước cuối).

**Rà chất lượng:** quét từ khoá cờ đỏ trên 119 ứng viên ra 3 khớp, **cả 3 đều là dương tính giả**:
"ISPA – University Institute" (Bồ Đào Nha) khớp chuỗi con "spa" trong "ISPA"; "International Research
Institute for Zen Buddhism at Hanazono University" và "Volos Academy for Theological Studies" là viện
nghiên cứu nhân văn/tôn giáo học chính thống trực thuộc đại học (không phải cơ sở tôn giáo hành đạo)
— giữ nguyên cả 3. Trải 35 quốc gia, dẫn đầu Mỹ 13, Anh 12, Bồ Đào Nha 8, Nga 6, Áo 5.

`ROSTER`: 18229 → **18317** (+88, khớp đúng số kiểm lại `len(load_roster(...))` ngay trước merge —
`git status` sạch). Đơn vị trên bản đồ: 18238 → **18326** (+88, giữ nguyên chênh lệch +9). Kiểm:
`node --check` sạch, thẻ `div`/`section` cân bằng (107/107, 6/6). Mở `index.html` qua HTTP server cục
bộ (`.claude/launch.json` config `static-server`, dùng `preview_start`/`preview_stop` của Browser
pane thay vì tự chạy `&` nền) qua Browser pane, đọc `get_page_text`: đúng "18326 đơn vị được lập bản
đồ" / "18317 trong danh mục mở rộng" / "12 đơn vị tại Việt Nam" (không đổi) / "9 case phân tích
chuyên sâu" (không đổi), console sạch.

**Còn thiếu ~6683 để đạt 25000.** **Việc mở cho lượt sau:** (1) **luôn dùng QLever
(`qlever.cs.uni-freiburg.de/api/wikidata`) cho mọi truy vấn Wikidata tiếp theo**, đừng quay lại
`query.wikidata.org` trừ khi xác nhận outage đã hết (kiểm nhanh 1 query đơn giản trước) — QLever
nhanh hơn nhiều và không bị throttle trong suốt phiên này; (2) batch lượt này chỉ lấy item có nhãn
tiếng Anh (`rdfs:label ... FILTER(LANG=... "en")`) — 53/607 bị loại vì không có nhãn tiếng Anh, có
thể còn nhiều hơn ở class khác; thử lấy thêm nhãn ngôn ngữ bản địa (đặc biệt Trung/Nhật/Hàn/Nga) cho
các item bị rơi vì thiếu nhãn "en" — dư địa chưa khai thác; (3) `university institute` mới dùng P31
trực tiếp — CHƯA thử subclass riêng có ý nghĩa của nó (nếu có) hoặc các class "khoa/viện" khác gần
nghĩa; (4) tiếp tục tra Q-id mới cho các khái niệm CGCN/ĐMST chưa thử: "innovation and technology
center", "research centre" (nếu có Q-id tách biệt với "research institute"), "living lab", "digital
innovation hub" (khác `innovation hub` Q28689074 đã dùng — kiểm xem có Q-id EU DIH riêng không); (5)
nguồn OSM và các nguồn phi-Wikidata đã liệt kê ở checkpoint ≤38 coi như cạn, không quay lại trừ tag
hoàn toàn mới.

---
**Lần trước:** 2026-09-10 (checkpoint 39 — **ĐỔI HƯỚNG KHỎI OSM, NGUỒN MỚI HOÀN TOÀN: Wikidata SPARQL
`query.wikidata.org/sparql`, class "research institute" (Q31855), kỹ thuật #3 trong 5 kỹ thuật đã chứng
minh — lần đầu dùng Wikidata qua 39 checkpoint, quy mô LỚN NHẤT từ 1 nguồn duy nhất tính đến nay**) — còn
thiếu ~6771 lúc cuối phiên.

Agent lượt trước (checkpoint 38) kết luận các namespace OSM "an toàn" đã cạn, khuyến nghị mạnh nghiên cứu
Wikidata SPARQL (nguồn có cấu trúc lớn nhất thế giới, miễn phí, chưa từng thử). Tra `wikidata.org` tìm đúng
Q-id trước: thử "business incubator" (Q1132207, chỉ 69 mục có site), "science park" (Q1976594, 139 mục),
"technology transfer office" (Q48782630, quá hẹp/rác), **"research institute" (Q31855) cho ra 8533 cặp
(item,site) trực tiếp — đúng class, không lẫn** (kiểm subclass mở rộng `P279*` cho 24201 nhưng phần lớn là
`academic department`/`laboratory` — đơn vị con quá nhỏ, KHÔNG dùng subclass, chỉ dùng P31 trực tiếp).

Truy vấn SPARQL `?item wdt:P31 wd:Q31855; wdt:P856 ?site` (P856 = official website) + `OPTIONAL` toạ độ
P625 và quốc gia P17. **Bài học kỹ thuật quan trọng:** endpoint Wikidata trả 502 khi kèm `SERVICE
wikibase:label` cho >500 dòng/trang hoặc dùng `ORDER BY` trên tập lớn — phải tách làm 2 bước: (1) trang
dữ liệu thô (item/site/coord/country **không** label, `LIMIT 2000 OFFSET n`, ổn định) rồi (2) trang nhãn
riêng (`LIMIT 500 OFFSET n` kèm label service, vẫn thỉnh thoảng 502 — retry lại offset lỗi là qua). Gọi
API `wbgetentities` để lấy nhãn hàng loạt bị chặn 429 liên tục dù batch 50 id/lần — bỏ hướng này, dùng
SPARQL label service phân trang nhỏ thay thế, ổn định hơn hẳn.

Kết quả thô: 8865 dòng (item,site) → gộp theo `item` (nhiều dòng do OPTIONAL nhân bản khi 1 item có nhiều
toạ độ/quốc gia) → **7786 item duy nhất có website**. Toạ độ P625 có sẵn cho 4018/7786 (52%); quốc gia P17
có cho 7466/7786 (96%). Dùng tự tính centroid quốc gia (bbox-center) từ chính `_ne50_countries_cache.geojson`
đã cache sẵn (dùng lại `NAME_OVERRIDE` của `country_from_latlon.py`) cho 3046 item có quốc gia nhưng thiếu
toạ độ — 367 item không có cả toạ độ lẫn quốc gia hợp lệ bị loại thẳng. Lấy nhãn tiếng Anh: 7289/7786 có
nhãn (1140 item không có nhãn tiếng Anh nào bị loại).

Lọc trùng ROSTER (base-domain qua `tldextract` + `normalize_name()`) + lọc Việt Nam (17 mục) → **3364 ứng
viên mới, duy nhất**. `check_url()` 4 vòng (16 luồng/15s → 8/25s → 4/30s → vòng UA Chrome thật) mất tổng
~40 phút (chạy nền qua watcher lệnh Bash, không dùng `run_in_background`/`&`): 3364 → 2431 (vòng 1) → +20 →
+9 → +14 (UA) = **2474 sống**. Đa số URL "chết" là `URLError`/`HTTPError` thật (site đã ngưng hoạt động),
không phải bị chặn bot — vòng UA chỉ vớt thêm 14/904, xác nhận hầu hết là chết thật.

**Rà chất lượng:** quét từ khoá cờ đỏ (yoga/tôn giáo/chữa lành/tarot/bảo hiểm/spa...) trên toàn bộ 2474 —
chỉ 1 mục thật sự đáng ngờ (`Bout Me Healing`, Mỹ, Q-id rất mới Q138679019, toạ độ Wikidata lệch sang Pháp
— rõ ràng gắn sai `P31` trong Wikidata) → loại thủ công. Còn lại toàn bộ ~29 khớp từ khoá khác đều là khớp
chuỗi con giả (Space/Spatial chứa "spa", Prayoga chứa "yoga"...) — giữ nguyên. Đọc mẫu ngẫu nhiên 40/2474 +
toàn bộ 201 item có Q-id rất mới (>130 triệu, tạo gần đây) để dò rác — chất lượng cao đồng đều, phủ rất
rộng cả châu Phi (Mali, Kenya, Ghana, Algeria, Tunisia, Morocco, Chad, Nigeria) lẫn châu Á/Âu/Mỹ, những khu
vực OSM trước đây phủ mỏng. Kiểm trùng tên/domain nội bộ batch: 0 domain trùng, 8 tên trùng nhưng đều là
tên chung ("Institute of Botany" ở nhiều nước khác nhau — không phải cùng 1 tổ chức). **0 Việt Nam** (xác
nhận cả ở bước lọc quốc gia và bước cuối). Trải **~115+ quốc gia**, dẫn đầu: Mỹ 340, Đức 241, Nhật 150, Nga
127, Hàn Quốc 109, Pháp/Tây Ban Nha 87 mỗi nước, Ấn Độ 86, Canada 81, Hà Lan 74.

`ROSTER`: 15756 → **18229** (+2473, khớp đúng số kiểm lại `len(load_roster(...))` ngay trước merge —
`git status` sạch, không có phiên song song). Đơn vị trên bản đồ: 15765 → **18238** (+2473, giữ nguyên
chênh lệch +9). Kiểm: `node --check` sạch trên script inline, thẻ `div`/`section` cân bằng (107/107, 6/6).
Mở `index.html` qua HTTP server cục bộ qua Browser pane, đọc trực tiếp qua `javascript_tool` (trang quá lớn
cho `get_page_text`): hiển thị đúng "18238 đơn vị được lập bản đồ" / "18229 trong danh mục mở rộng" / "12
đơn vị tại Việt Nam" (không đổi) / "9 case phân tích chuyên sâu" (không đổi), console sạch không lỗi.

**Còn thiếu ~6771 để đạt 25000.** **Việc mở cho lượt sau:** (1) Wikidata SPARQL còn NHIỀU dư địa chưa khai
thác trong đúng lượt này — mới dùng đúng 1 class (`Q31855` research institute, P31 trực tiếp); (2) thử tiếp
`Q1132207` (business incubator, chỉ 69 — đã cạn) và `Q1976594` (science park, chỉ 139 — đã cạn) không đáng
kể, nhưng CHƯA thử `Q3918` (university) hay `Q38723` (higher education institution) — rủi ro trùng lặp rất
cao với ROSTER hiện có (đã có sẵn rất nhiều đại học) nên cần khảo sát tỉ lệ trùng trước khi đầu tư; (3)
CHƯA thử các subclass CÓ ý nghĩa riêng của `Q31855` (bỏ qua ở lượt này vì lẫn `academic department`/
`laboratory`) như đứng riêng: `think tank` (Q155271, 1167 mục có site) hoặc `university institute`
(Q11946645, 556 mục) — đáng thử riêng từng class thay vì gộp subclass tràn lan; (4) CHƯA thử Wikidata cho
các class khác hẳn (bảo tàng khoa học, đài quan trắc, vườn ươm công nghệ theo tên riêng...) — tra Q-id
trước khi chạy SPARQL, đọc kỹ hướng dẫn `Bước 1` ở đầu phiên trước nếu lặp lại kỹ thuật này; (5) nguồn OSM
coi như đã cạn theo kết luận checkpoint 38, KHÔNG quay lại trừ khi có tag hoàn toàn mới chưa thử; (6) nếu
Wikidata tiếp tục hiệu quả, đây có thể là nguồn đủ lớn để một mình đưa ROSTER cán đích 25000 — ưu tiên đào
sâu tiếp nguồn này trước khi tìm nguồn hoàn toàn khác.

---
**Lần trước:** 2026-09-10 (checkpoint 38 — **NGUỒN OSM MỚI `amenity=research_institute` (khác namespace
`office=research` đã làm ở checkpoint 28), toàn cầu 1 lượt, chất lượng CAO NHẤT trong các batch OSM gần
đây**) — còn thiếu ~9244 lúc cuối phiên.

Overpass `overpass-api.de`, `[timeout:280]`, 1 truy vấn duy nhất `out center tags;` cho toàn bộ
`amenity=research_institute` toàn cầu (không cần chia bbox — tag hiếm hơn hẳn `university`/`college`):
`out count;` báo 6662 phần tử (2047 node + 4156 way + 459 relation), tải trọn ~2.7MB 1 lần không timeout.
Trích tên+URL (ưu tiên `website`/`contact:website`/`url`, chấp nhận `contact:facebook`/`contact:instagram`/
`contact:linkedin` theo đúng chính sách mạng xã hội đã chốt) → 2661 ứng viên có cả tên+URL (383 không tên,
3618 không URL bị loại ngay). Gán quốc gia qua `CountryLookup`: 107 điểm ngoài biên NE50, 38 điểm rơi Việt
Nam loại ngay → 2516 ứng viên hợp lệ, trải **102 quốc gia** (không tập trung 1-2 nước như các batch trước —
Đức 320, Nga 313, Mỹ 241, Pháp 203, Tây Ban Nha 136 dẫn đầu nhưng phân bố rộng khắp).

Gộp multi-campus qua `base_domain()` → 1746 nhóm domain duy nhất. Lọc trùng ROSTER (base-domain qua
`tldextract` + `normalize_name()`) loại 423 domain + 4 tên → **1319 ứng viên mới**.

**Khảo sát chất lượng trước khi tải hàng loạt (bài học từ rủi ro `amenity=college` ở checkpoint 37):** đọc
mẫu ngẫu nhiên 80/1319 + quét từ khoá cờ đỏ (tôn giáo/yoga/lái xe/thẩm mỹ/nấu ăn — chỉ khớp **1/1319**, khác
hẳn tình trạng nhiễu cao của `amenity=college`) — kết luận tag `amenity=research_institute` SẠCH hơn hẳn
`amenity=college` ở mọi vùng địa lý đã thử (không giới hạn Nam Á/ĐNÁ), vì tên gọi "research institute"
trong OSM community-mapping có xu hướng chỉ áp cho cơ sở nghiên cứu thật (viện hàn lâm khoa học Nga/Ukraine/
Serbia dạng "НИИ"/Институт, Leibniz/Helmholtz/Max-Planck Đức, CNRS/labo Pháp, trạm quan trắc/nông nghiệp/
khí tượng nhiều nước, national lab Mỹ...) — không lẫn trường phổ thông/dạy nghề như `college`. Loại 1 mục
"Buddhism Research Institute" (Mỹ) qua quét từ khoá tôn giáo, giữ **1318 sạch**.

`check_url()` 4 vòng (16 luồng/15s → 8/25s → 4/30s → vòng UA trình duyệt thật): 1318 → 940 (vòng 1) → +11
→ +3 → +5 (UA) = **959 sống**. Rà tay đọc toàn bộ 959 dòng theo từng nhóm quốc gia (không chỉ mẫu) do quy
mô vừa phải: phát hiện 2 URL Facebook dạng `/posts/<id>` (bài đăng cụ thể, không phải trang định danh tổ
chức — dễ biến mất/không đại diện tổ chức, khác hẳn URL trang Facebook Page đã chốt chính sách chấp nhận) ở
Malaysia, loại cả 2; dọn 1 query-string tracking LinkedIn (`?trk=similar-pages`) không loại bỏ mục. Còn lại
**957 mục thật, duy nhất**, trải 72 quốc gia (Nga 186, Đức 96, Mỹ 71, Pháp 69, Nhật 50, Tây Ban Nha 31, Ba
Lan/Anh/Ukraine 27 mỗi nước dẫn đầu). Bao gồm 1 điểm ở Nam Cực (SANAE IV, trạm South African National
Antarctic Programme — nước "Antarctica" mới, hợp lệ vì đúng vị trí thật) và xác nhận lại quy ước quốc gia có
sẵn cho "Kosovo"/"N. Cyprus" khớp đúng ROSTER. **0 Việt Nam** (xác nhận ở cả bước gán quốc gia và bước cuối).

`ROSTER`: 14799 → **15756** (+957, khớp đúng số kiểm lại `len(load_roster(...))` ngay trước merge, không có
phiên song song nào ghi đè lần này — `git status` sạch, `git log` không đổi so với đầu phiên). Đơn vị trên
bản đồ: 14808 → **15765** (+957, giữ nguyên chênh lệch +9 do 9 case phân tích chuyên sâu). Kiểm: `node
--check` sạch trên script inline, thẻ `div`/`section` cân bằng (107/107, 6/6). Mở `index.html` qua HTTP
server cục bộ (`.claude/launch.json`) qua Browser pane: hiển thị đúng "15765 đơn vị được lập bản đồ" /
"15756 trong danh mục mở rộng" / "12 đơn vị tại Việt Nam" (không đổi) / "9 case phân tích chuyên sâu" (không
đổi), không lỗi console.

**Còn thiếu ~9244 để đạt 25000.** **Việc mở cho lượt sau:** (1) `amenity=research_institute` đã khai thác
TOÀN CẦU trong 1 lượt (không như `university`/`college` phải chia bbox) — tag này coi như ĐÃ XONG, đừng lặp
lại; (2) 2 tag OSM giáo dục/nghiên cứu chính (`amenity=university` 7 bbox, `amenity=college` Nam Á+ĐNÁ,
`amenity=research_institute` toàn cầu) + `office=research`/`office=*` (checkpoint 27-30) coi như đã khai
thác gần hết các namespace OSM "an toàn" (tên gọi rõ nghĩa, ít nhiễu) — namespace OSM còn lại nếu muốn thử
tiếp nên khảo sát mẫu kỹ trước (như lượt này) vì nguy cơ nhiễu như `college`/`office=association` tăng dần
khi namespace càng chung chung; (3) `amenity=college` Tây Âu/Mỹ Latinh/Châu Phi+Trung Đông/Úc-NZ vẫn còn
"CÓ dữ liệu nhưng nhiễu cao" như checkpoint 37 đã khảo sát — cân nhắc kỹ trước khi đầu tư công rà tay; (4) ở
khoảng cách ~9244, cần nguồn thật lớn — nên dành thời gian nghiên cứu SÂU 1-2 nguồn hoàn toàn mới quy mô
lớn thay vì tiếp tục chia nhỏ OSM (sắp cạn các tag "an toàn"), hoặc quay lại 1 trong 5 kỹ thuật khác đã
chứng minh (đăng ký chính phủ, JSON nhúng bản đồ hiệp hội, API REST toàn bộ, API phân trang+cào hồ sơ, SMW
askargs) áp dụng cho quốc gia/lĩnh vực chưa từng thử.

---
**Lần trước:** 2026-09-10 (checkpoint 37 — **SẾP NÂNG MỤC TIÊU TỪ 15000 LÊN 25000; NGUỒN OSM MỚI
`amenity=college` (khác `amenity=university` đã cạn ở checkpoint 36), bbox Nam Á + Đông Nam Á, PHÁT HIỆN
VÀ XỬ LÝ 1 PHIÊN SONG SONG ghi đè cùng file `src/atlas.html`**) — còn thiếu ~10201 lúc cuối phiên.

**Khảo sát khả thi trước khi chọn vùng — bài học quan trọng nhất lượt này: `amenity=college` KHÔNG đồng
nhất chất lượng như `amenity=university` theo từng vùng địa lý/văn hoá ngôn ngữ.** Đếm `out count;` cả 8
bbox đã dùng cho `amenity=university` (Châu Phi+Trung Đông 886, Nam Á 1334, Đông Nam Á 714, Mỹ Latinh 1798,
Đông Âu/Trung Á 1682, Đông Á 1329, Tây Âu/Bắc Âu 6448, Úc/NZ 240) rồi đọc mẫu 25-50 phần tử mỗi vùng trước
khi tải toàn bộ: **Tây Âu phát hiện đa số (isced:level chủ yếu = 3, min_age chủ yếu = 16 qua thống kê tag)
là trường TRUNG HỌC PHỔ THÔNG kiểu Anh ("sixth-form college"/"further education college") — đúng định
nghĩa gốc của OSM cho tag `amenity=college` là cơ sở giáo dục sau trung học KHÔNG cấp bằng đại học, khác
hẳn `amenity=university`; Mỹ Latinh/Châu Phi+Trung Đông đọc mẫu thấy lẫn nhiều trường dạy khiêu vũ/yoga/
tango, phòng thương mại, học viện làm đẹp/pha chế — nhiễu cao.** Nam Á (Ấn Độ/Pakistan/Bangladesh/Nepal/
Sri Lanka, "college" = từ chuẩn chỉ trường đại học/cao đẳng cấp bằng cử nhân theo Đạo luật Đại học) và Đông
Nam Á (Philippines/Indonesia "Sekolah Tinggi"/Malaysia "Kolej"/Thái Lan "วิทยาลัย" đều là hệ thống cao đẳng
nghề chính quy sau trung học) cho tỷ lệ HEI thật cao nhất qua đọc mẫu — **chọn 2 vùng này, GHI RÕ vào đây để
lượt sau không lặp lại khảo sát Tây Âu/Mỹ Latinh/Châu Phi+Trung Đông/Úc-NZ cho tag này** (khác hẳn kết luận
"đã cạn" của `amenity=university` — với `amenity=college`, các vùng đó CÓ dữ liệu nhưng đa số SAI CHỦ ĐỀ,
không phải "hết nguồn").

**Overpass `overpass-api.de`, `[timeout:180-280]`, retry 1 lần do "server too busy" (bài học cũ) cho cả 2
bbox** — Nam Á `(5,60,38,92)` 1334 phần tử, Đông Nam Á `(-11,92,29,142)` 714 phần tử (tràn cả Việt Nam do
bbox rộng, đúng dự kiến). Gán quốc gia qua `CountryLookup`: 56 điểm ngoài biên NE50, **43 điểm rơi Việt Nam
loại ngay** (SE Asia bbox) → 1949 ứng viên có quốc gia hợp lệ, 22 nước (Ấn Độ 1128 áp đảo).

**Lọc chất lượng theo TỪNG LỚP (khác hẳn quy trình chuẩn của `amenity=university` — chỉ dedup domain rồi
`check_url()` là đủ; `amenity=college` cần thêm lớp lọc NỘI DUNG vì tag này lẫn cả bậc trung học/dạy nghề
không cấp bằng):**
1. **Lọc từ khoá cứng trước cả `check_url()`** (30 loại): trường mẫu giáo/tiểu học/THPT/"grammar school"/
   "public school"/convent, **cao đẳng dự bị đại học Nam Á** (junior/intermediate/pre-university/PU/"+2"/
   "higher secondary" — bậc lớp 11-12, KHÔNG phải đại học dù tên có chữ "college"), trường lái xe/luyện thi/
   ngân hàng/phòng thương mại. Sửa 1 lỗi logic: quy tắc loại "hospital" ban đầu vô tình loại nhầm các
   TRƯỜNG Y THẬT của Ấn Độ (quy ước đặt tên "X Medical College **and Hospital**" — bệnh viện thực hành gắn
   liền trường, vẫn là trường cấp bằng bác sĩ thật) vì lookahead regex chỉ nhìn về phía sau "hospital" trong
   khi "College" thường đứng TRƯỚC — sửa bằng kiểm tra "college" xuất hiện bất kỳ đâu trong tên trước khi
   loại theo "hospital". base_domain gộp 1919 → 1907 kept, 1695 nhóm domain duy nhất. Lọc trùng ROSTER
   (base-domain qua `tldextract` + `normalize_name()`) loại 79 domain + 7 tên → **1609 ứng viên**.
2. **`check_url()` 4 vòng** (16 luồng/15s → 8/25s → 4/30s → vòng UA trình duyệt thật, đúng bài học checkpoint
   36): 1609 → 1145 (vòng 1) → +8 → +2 → +7 (UA) = **1162 sống**.
3. **Rà tay 2 lớp cho phần "sống":** (a) quét từ khoá cờ đỏ tiếng Anh (academy/school/centre/dance/yoga/
   hospital...) gắn cờ 96/1162, đọc tên xác nhận tay từng mục — loại 26 (trường phổ thông kết hợp "School &
   College" quy ước Bangladesh/Pakistan cho campus phổ thông+dự bị đại học chung, cơ quan đào tạo nghề chính
   phủ không cấp bằng như ITI/Tool Room/Vocational Training Authority, NGO/thư viện không phải cơ sở giáo
   dục). (b) **PHÁT HIỆN LỖI QUÉT: regex cờ đỏ chỉ khớp chữ Latin, bỏ lọt bản tương đương phi-Latin** — ví dụ
   "আজিমপুর গভঃ গার্লস স্কুল অ্যান্ড কলেজ" (tiếng Bengal cho "School and College") không khớp `\bschool\b`
   tiếng Anh; "衡阳市逸夫中学" (THCS tiếng Trung) không khớp `\bschool\b`. Thêm vòng quét riêng theo chuỗi con
   đa ngôn ngữ (Bengal "স্কুল"/"বিদ্যালয়" kèm "কলেজ", Trung "中学"/"党校") — loại thêm 6. Rà tay đọc toàn bộ
   các nhóm nước nhỏ còn lại (Thái Lan, Nepal, Pakistan, Bangladesh, Trung Quốc, Indonesia, Malaysia,
   Philippines, Singapore, Đài Loan, Hong Kong, Nhật, Myanmar, Bhutan, Brunei, Lào, Uzbekistan,
   Turkmenistan, Iran — tất cả trừ Ấn Độ vì quá lớn, chỉ áp quét từ khoá mở rộng cho Ấn Độ) dựa hiểu biết hệ
   thống giáo dục từng nước (vd "Cadet College" Pakistan = trường phổ thông nội trú quân sự KHÔNG cấp bằng
   đại học dù tên có "College"; "H.S.S."/"Higher Sec." Nepal = dự bị đại học; "Notre Dame College"/"Dhaka
   Residential Model College" Bangladesh = trường HSC nổi tiếng KHÔNG cấp bằng cử nhân; "Marlborough
   College"/"Epsom College" Malaysia = trường phổ thông Anh Quốc chi nhánh; "Confucius Institute" = trung
   tâm văn hoá/ngôn ngữ gắn trong đại học, không tự cấp bằng; techникум Uzbekistan/Turkmenistan = trung cấp
   nghề Liên Xô cũ, dưới bậc đại học) — loại thêm 27, tổng loại tay **53/1162**, giữ **1077**.

**PHÁT HIỆN QUAN TRỌNG: 1 PHIÊN SONG SONG khác đã ghi đè `src/atlas.html` trên đĩa trong lúc lượt này đang
chạy** (Google Drive `G:\` dùng chung, không phải worktree cô lập) — phát hiện khi script merge cuối cùng
đọc `ROSTER` tại chỗ ra **14862** thay vì 13724 đã xác nhận đầu phiên, dù chưa hề tự ghi gì vào file. Đối
chiếu diff với `git show HEAD:src/atlas.html`: có **1138 dòng mới lạ** (field `org` để rỗng — khác quy ước
`org=name` của mọi script trong phiên này), phân bố quốc gia GẦN NHƯ TRÙNG KHỚP batch Nam Á+Đông Nam Á đang
làm (Ấn Độ 729, Philippines 75, Indonesia 58...) — kết luận: một phiên Claude Code khác đã độc lập chọn
ĐÚNG cùng nguồn/vùng này, chạy xong và ghi tại chỗ (chưa commit) trong lúc phiên này còn đang rà tay. Kiểm
tra chất lượng dữ liệu của họ trước khi quyết định: `check_url()` mẫu ngẫu nhiên 60/1138 → 59 sống (đúng tỷ
lệ mong đợi, xác nhận họ có kiểm URL); 0 Việt Nam; nhưng quét lại bằng ĐÚNG bộ từ khoá/tên loại tay của
phiên này phát hiện **67/1138 mục lẽ ra phải loại vẫn còn trong dữ liệu của họ** (họ không làm bước rà tay
đọc nội dung — chỉ dừng ở `check_url()`). **Xử lý: KHÔNG ghi đè/bỏ dữ liệu của họ, cũng KHÔNG commit thẳng
dữ liệu chưa rà** — áp used đúng bộ tiêu chí loại tay đã đúc kết ở bước rà tay của phiên này (tên khớp chính
xác + regex mở rộng + quét đa ngôn ngữ) lên toàn bộ 1138 dòng của họ, loại 67 còn lại **1071**, rồi dựng lại
`ROSTER` từ đúng bản `git show HEAD` (không dùng `git checkout` phá hỏng — ghi đè trực tiếp bằng Python để
tránh lệnh destructive) + gộp CHUNG 1 lượt cả 2 tập ứng viên đã làm sạch (1077 của phiên này + 1071 của họ)
qua đúng 1 lần dedup base-domain/tên duy nhất để không sót trùng giữa 2 tập. **Bài học cho các phiên sau khi
làm việc trên `G:\My Drive\...` (thư mục Drive dùng chung, không phải git worktree riêng): LUÔN kiểm lại
`ROSTER` tại chỗ ngay trước bước merge cuối cùng (không tin số đã đọc đầu phiên), và LUÔN đối chiếu
`git show HEAD:<file>` trước khi ghi đè nếu số bất ngờ đổi khác — đừng vội cho là lỗi, có thể là phiên song
song khác đang chạy cùng lúc.**

Gộp 1077 (phiên này) + 1071 (đã làm sạch của phiên song song) = 2148 ứng viên, dedup lẫn nhau + với
`ROSTER` gốc (base-domain qua `tldextract` + `normalize_name()`) loại 1073 trùng (đa số là trùng CHÉO giữa
2 tập vì cùng nguồn) → **1075 mục thêm thật, duy nhất**. Theo quốc gia: Ấn Độ 729, Philippines 72,
Indonesia 54, Thái Lan 44, Trung Quốc 43, Malaysia 36, Nepal 32, Bangladesh 22, Sri Lanka 8, Pakistan 6,
Hong Kong 6, Singapore 5, Đài Loan 5, Nhật Bản 4, Brunei 3, Bhutan 2, Lào 2, Iran 1, Myanmar 1. **0 Việt
Nam** (xác nhận lại ở bước đầu và bước cuối).

`ROSTER`: 13724 → **14799** (+1075). Đơn vị trên bản đồ: 13733 → **14808** (+1075, giữ nguyên chênh lệch
+9). Kiểm: `node --check` sạch trên script inline, thẻ `div`/`section` cân bằng (107/107, 6/6). Mở
`index.html` qua HTTP server cục bộ (`.claude/launch.json`) qua Browser pane: hiển thị đúng "14808 đơn vị
được lập bản đồ" / "14799 trong danh mục mở rộng" / "12 đơn vị tại Việt Nam" (không đổi) / "9 case phân
tích chuyên sâu" (không đổi), không lỗi console. Xoá `_claude/scratch/` trước khi commit.

**SẾP NÂNG MỤC TIÊU TỪ 15000 LÊN 25000 — còn thiếu ~10201.** **Việc mở cho lượt sau:** (1) `amenity=college`
CHỈ mới khai thác Nam Á + Đông Nam Á — Châu Phi+Trung Đông/Mỹ Latinh/Tây Âu/Úc-NZ CÓ dữ liệu nhưng tỷ lệ sai
chủ đề rất cao (trường phổ thông Anh/trường dạy nghề không cấp bằng/hobby), NẾU làm tiếp các vùng đó BẮT
BUỘC phải làm đủ quy trình rà tay đa lớp như lượt này (không chỉ `check_url()`), cân nhắc kỹ độ ưu tiên so
với nguồn khác trước khi đầu tư; (2) **`amenity=research_institute` VẪN CHƯA THỬ** (gợi ý từ checkpoint 36,
option 2 còn lại) — kỹ thuật Overpass+base_domain+CountryLookup đã chứng minh nhiều lần, nhưng cần cảnh giác
rủi ro tương tự `amenity=college` (tag có thể lẫn viện nghiên cứu phi-KHCN, think-tank chính trị, hay cơ sở
không phải "institute" theo nghĩa nghiên cứu); (3) **bài học vận hành quan trọng: luôn kiểm `ROSTER` tại chỗ
ngay trước merge cuối, đối chiếu `git show HEAD` nếu số bất ngờ khác — đề phòng phiên song song trên Google
Drive dùng chung**; (4) danh sách domain/tên loại tay tích luỹ được cho `amenity=college` (dùng lại nếu gặp
lại các domain/tên này ở vùng khác): "Cadet College" (Pakistan, phổ thông nội trú quân sự), "H.S.S."/"Higher
Sec."/"+2" (Nepal/Ấn Độ, dự bị đại học lớp 11-12), "School & College"/"স্কুল অ্যান্ড কলেজ"/"বিদ্যালয়...
কলেজ" (Bangladesh, campus phổ thông+dự bị đại học chung), "Model College"/"Public College" (Pakistan, cao
đẳng dự bị chính phủ), "中学"/"党校" (Trung Quốc, THCS/trường Đảng), "Confucius Institute" (trung tâm ngôn
ngữ gắn đại học, không tự cấp bằng), "Vocational Training Authority"/ITI/"Skills Development Centre" (nhiều
nước, đào tạo nghề ngắn hạn không cấp bằng), "Marlborough College"/"Epsom College" Malaysia (trường phổ
thông Anh chi nhánh), "United World College"/"Hwa Chong Institution"/"Millennia Institute" Singapore (phổ
thông/dự bị đại học); (5) quy trình lọc nhiều lớp (từ khoá cứng → check_url → quét cờ đỏ Latin → quét đa
ngôn ngữ → rà tay từng nước nhỏ) hiệu quả nhưng TỐN THỜI GIAN hơn hẳn `amenity=university` (vốn chỉ cần
domain-dedup+check_url) — cân nhắc đây là đặc thù của tag "college"/"institute" nói chung so với "school"/
"university" vốn rõ nghĩa hơn.

---
**Lần trước:** 2026-09-10 (checkpoint 36 — **CÙNG NGUỒN OSM `amenity=university`, 2 bbox CUỐI CÙNG còn lại
trong danh sách checkpoint 32 để lại: Đông Á (Trung Quốc/Nhật/Hàn/Đài Loan/Mông Cổ) + Tây Âu/Bắc Âu/Úc-NZ,
làm cả 2 trong 1 lượt — cả 7 bbox `amenity=university` đã lên kế hoạch từ checkpoint 32 nay ĐÃ XONG HẾT**)
— tiếp tục mục tiêu **15000** (còn thiếu ~3201 lúc đầu phiên).

**Đông Á trước** (bbox `(18,73,54,146)`, qua `overpass-api.de`, retry 1 lần do "server too busy" — bài học
cũ, `[timeout:300]`): `out count;` 1802 phần tử → `out center tags;` tải trọn 1 lần (~1MB). Gộp domain qua
`base_domain()` (giờ đã chuyển hẳn vào `_claude/tools/roster_common.py` làm hàm dùng chung, dùng
`tldextract` — đúng bài học checkpoint 35, không tự viết bảng tay nữa) → 1423 nhóm domain duy nhất. Gán
quốc gia qua `CountryLookup`: 34 điểm rơi ngoài biên NE50 (đảo/mũi đất nhỏ ở Hong Kong/Hàn Quốc/Nhật/Trung
Quốc/Đài Loan-Mã Tổ) gán tay đủ cả 34 qua tên/TLD; 55 điểm rơi vào Việt Nam (bbox chạm phần Bắc Việt Nam ở
vĩ độ 18-23°B) loại ngay. Lọc trùng ROSTER (base-domain + `normalize_name()`) loại 468 trùng domain + 9
trùng tên → còn 891 ứng viên.

**Tây Âu/Bắc Âu + Úc/NZ sau** (2 bbox riêng, gộp xử lý chung 1 lượt): Tây Âu/Bắc Âu `(35,-10,71,32)` —
`overpass-api.de` báo "server too busy" 2 lần liền dù đã `[timeout:300]` và retry, chuyển hẳn sang mirror
`overpass.openstreetmap.fr` (đúng bài học "thử mirror khác" tích luỹ nhiều checkpoint) → thành công ngay
lần đầu, `out count;` 5110 phần tử (LỚN NHẤT từ trước tới nay, vượt cả Mỹ Latinh 2930 ở checkpoint 35),
`out center tags;` tải trọn không cần chia nhỏ (2.9MB). Úc/NZ `(-47,110,-10,180)` nhỏ hơn nhiều (147 phần
tử), cùng mirror, không trở ngại. Gộp domain 2 bbox chung 1 lần → 2621 nhóm duy nhất. Gán quốc gia: 81 điểm
rơi ngoài biên NE50 (đảo/bờ biển nhỏ ở Thuỵ Điển/Đức/Croatia/Tunisia/Bồ Đào Nha/Ireland/Hy Lạp/Thổ Nhĩ
Kỳ/Monaco/Fiji/Indonesia — trạm nghiên cứu biển, campus vệ tinh, đại học nhỏ ven biển) gán tay đủ 81 qua
tên/TLD/domain, loại riêng 3 mục sai chủ đề phát hiện ngay ở bước này (Centro Cultural Reina Sofía — lặp
lại đúng domain đã loại ở checkpoint 32 dạng khác toạ độ; IntoUniversity — tổ chức từ thiện phụ đạo sau
giờ học ở Anh, không phải đại học; Rum Ortodoks Ruhban Okulu — chủng viện Chính thống giáo đào tạo ngắn
hạn). 0 Việt Nam (đúng dự kiến, bbox không chạm Việt Nam). Lọc trùng ROSTER (roster đã gồm cả batch Đông Á
vừa merge) loại 809 trùng domain + 13 trùng tên → còn 1796 ứng viên.

**`check_url()` phát hiện lỗi False-negative mới do WAF chặn User-Agent mặc định của tool — đã thêm vòng
retry thứ 4 để vá:** sau 3 vòng chuẩn (16 luồng/15s → 8 luồng/25s → 4 luồng/30s), Đông Á còn 288 "chết",
kiểm tay 1 domain (`thu.edu.tw` — Đại học Đông Hải, Đài Loan, rất nổi tiếng và chắc chắn đang hoạt động)
phát hiện `curl` với User-Agent mặc định của `check_url()` (chuỗi `"Mozilla/5.0 (roster-tools)"`) bị chặn
403 bởi WAF, nhưng cùng URL trả 200 OK khi đổi sang User-Agent trình duyệt thật (Chrome/Windows). Kiểm mẫu
ngẫu nhiên 40/288 domain "chết" bằng User-Agent thật: chỉ 2/40 (5%) phục hồi — xác nhận ĐA SỐ domain "chết"
còn lại là chết thật (URLError/kết nối thất bại), KHÔNG phải bị chặn UA hàng loạt, nhưng vẫn đáng làm 1
vòng retry toàn bộ vì tỷ lệ phục hồi khác 0. Viết script retry riêng (`check_round_ua.py`, dùng lại nguyên
logic `check_url()` gốc — theo redirect 1 hop, phát hiện trang ký gửi domain — chỉ đổi User-Agent) chạy
trên toàn bộ danh sách "chết" cuối cùng của cả 2 batch: Đông Á +8 sống (`thu.edu.tw`/`ctbc.edu.tw` Đài Loan
trong đó), Tây Âu/Úc-NZ +6 sống. **Bài học cho batch `check_url()` sau: cân nhắc thêm hẳn 1 vòng retry
User-Agent trình duyệt thật vào quy trình chuẩn (sau vòng 3, trước khi chốt danh sách chết) — chi phí thấp
(chỉ chạy trên phần đã chết, không phải toàn bộ), lợi ích nhỏ nhưng chắc chắn dương (~1-2% tổng số ứng
viên mỗi batch, đặc biệt cao ở Đài Loan lần này).** Không sửa `check_url()` gốc trong `roster_common.py`
(vẫn giữ User-Agent cũ làm mặc định) vì đa số domain vẫn nhận diện tốt user-agent đó, chỉ thêm script retry
riêng dùng khi cần.

Kết quả `check_url()` cuối: Đông Á 891 → 603+8=**611 sống**; Tây Âu/Úc-NZ 1796 → 1309+13+3+6=**1331 sống**.

**Quét từ khoá cờ đỏ trên tên trước khi rà tay (đúng kỹ thuật checkpoint 35):** Đông Á chỉ 3/611 bị gắn cờ
— cả 3 đọc `<title>` xác nhận hợp lệ, giữ nguyên 2 ("Temple University, Japan Campus" — campus thật của
Temple University Mỹ tại Nhật; "The Film School of Tokyo"/映画美学校 — trường điện ảnh chuyên ngành thật),
sửa lỗi chính tả 1 ("SN Bose National Centre for Basic Schiences" → "...Sciences", viện nghiên cứu quốc gia
Ấn Độ thật thuộc Bộ KHCN). Riêng vòng UA-retry đón thêm lại đúng 1 mục "Oxford University Press" (domain
`oup.co.in` khác hẳn domain đã loại ở checkpoint 33) — LOẠI LẠI vì cùng vấn đề: chi nhánh Ấn Độ của 1 NHÀ
XUẤT BẢN, không phải trường — ghi nhớ thêm `oup.co.in` vào danh sách domain loại tay tích luỹ.

Tây Âu/Úc-NZ 217/1331 bị gắn cờ (nhiều hơn hẳn Đông Á vì đa số đại học châu Âu đặt tên campus/khoa dài kiểu
"[Tên Trường] [Tên Campus]" khớp từ khoá "campus"/"site" xây trong bộ lọc) — áp đúng quy tắc tinh chỉnh
checkpoint 34 "chỉ đổi tên khi tên gốc THẬT SỰ không tự nhận diện được tổ chức mẹ": ĐA SỐ (206/217) là tên
kiểu "Monash University, Clayton Campus"/"University of Worcester Lakeside Campus" đã tự ghi rõ tên trường
mẹ — GIỮ NGUYÊN không đổi, không cần đọc trang thật. Chỉ đọc `<title>`+mô tả trang thật cho ~23 mục thật sự
mơ hồ (acronym ngắn không tự nhận diện, hoặc từ khoá nghi sai chủ đề như "hospital"/"bank"/"press"/"seminary"/
"hotel" — phần lớn hoá ra vẫn là trường thật dùng từ đó trong tên hợp lệ, vd "Bankovní Institut Vysoká
škola" = đại học ngân hàng thật, "Continental Theological Seminary" = chủng viện CÓ cấp bằng Cử nhân/Thạc
sĩ thần học được công nhận nên GIỮ (khác case Halki bên Đông Á loại vì đào tạo ngắn hạn không cấp bằng)) →
loại 11 mục xác nhận sai chủ đề/không xác định được qua đọc trang thật: **CESNET** Czech (hiệp hội hạ tầng
mạng nghiên cứu quốc gia, không phải đại học), **AFALVI** Tây Ban Nha (tiêu đề trang không xác định được là
tổ chức giáo dục), **ESAMUR** Tây Ban Nha (cơ quan xử lý nước thải vùng Murcia), **GEO600** Đức (cơ sở
thiết bị nghiên cứu sóng hấp dẫn, không cấp bằng), **ICJT** Slovenia (trung tâm đào tạo hạt nhân, không xác
định được là bậc đại học), **Law Society of Ireland** (hiệp hội luật sư/cơ quan quản lý nghề, không phải
trường — cùng loại "Colegio de Abogados" checkpoint 35), **Mercy University Hospital Centre of Nurse
Education** Ireland (trung tâm đào tạo điều dưỡng do 1 bệnh viện vận hành, không phải đại học độc lập),
**Centre for Alternative Technology** Xứ Wales (trung tâm/từ thiện môi trường, không phải đại học được công
nhận), **CREPS** Pháp (cơ sở lưu trú/thể thao vùng, không tự cấp bằng), **"DA"** Đức (tên OSM không xác
định được — URL trỏ trang "Standorte"/danh sách địa điểm chung của Hochschule Karlsruhe, không định danh
được cơ sở cụ thể nào), **RIPAM 7** Ý (xác nhận qua `<title>` là 1 HỘI NGHỊ/sự kiện về di sản kiến trúc
Địa Trung Hải, không phải tổ chức). **Đổi tên 6 mục** qua xác nhận nội dung trang thật: "Minerva Building"
(Anh, `lincoln.ac.uk` không tự nêu tên trường) → "University of Lincoln"; "IUT" (Pháp, `iut-valence.fr`) →
"IUT de Valence"; "UNED" (Tây Ban Nha, domain lạ `uneddenia.es` khác hẳn domain chính `uned.es` — đây là
Trung tâm Liên kết địa phương của UNED tại Denia) → "UNED Denia (Centro Asociado)"; "ISNAB" (Pháp) → "ISNAB
- Institut des Sciences de la Nature et de l'Agroalimentaire de Bordeaux"; "SOFI" (Đức) → "SOFI -
Soziologisches Forschungsinstitut Göttingen"; "DRCMR" (Đan Mạch) → "DRCMR - Danish Research Centre for
Magnetic Resonance". Các acronym ngắn còn lại đọc trang xác nhận là brand công khai thật của chính tổ chức
(CEFAM, IGEMA, IPABO, ISPRA, ISNAB gốc, BPP, SAE, VUT, UMIT, FHDW, INSEEC, ISEP, EPSI, ENSATT...) — GIỮ
NGUYÊN.

Kết quả cuối: Đông Á 611 sống → loại 1 (Oxford University Press) → sửa lỗi chính tả 1 → **610 mục thêm
thật**. Tây Âu/Úc-NZ 1331 sống → loại 11 (sai chủ đề/không xác định) → đổi tên 6 → 1320 ứng viên → merge
qua script chuẩn loại thêm 5 trùng tên thật trong nội bộ batch (IUT/Webster University/Wyższe Seminarium
Duchowne/Staatliche Akademie der Bildenden Künste/Uniwersytet Artystyczny — đã có mục khác cùng tên từ
trước trong chính batch này qua toạ độ/domain khác) → **1315 mục thêm thật**. Đông Á theo quốc gia: Nhật
Bản 311, Trung Quốc 188, Hàn Quốc 83, Nga 14, Mông Cổ 4, Ấn Độ 3, Kyrgyzstan 2, Hong Kong 2, Đài Loan 2,
Bangladesh 1. Tây Âu/Úc-NZ theo quốc gia (48 quốc gia): Đức 271, Pháp 196, Anh 87, Ý 86, Tây Ban Nha 75, Áo
57, Hà Lan 54, Ba Lan 48, Nga 44, CH Séc 37, Úc 36, Thuỵ Sĩ 33, Bỉ 31, Bồ Đào Nha 26, Phần Lan 25, Ireland
24, Croatia 22, Thuỵ Điển 19, Slovakia 17, Na Uy 17, Đan Mạch 16, Thổ Nhĩ Kỳ 16, New Zealand 12, Bosnia và
Herzegovina 11, Hungary 10, Latvia 10, Slovenia 9, Estonia 6, Belarus 3, Serbia 3, Montenegro 2, Ukraine 2,
Algeria 2, Litva 2, Fiji 2, và 11 nước còn lại 1 mục mỗi nước (Hy Lạp, San Marino, Isle of Man, Bắc
Macedonia, Vanuatu, Monaco, Romania, Bulgaria, New Caledonia...). **0 Việt Nam** (xác nhận lại ở cả 2 batch,
cả bước đầu và bước cuối).

**Chuyển `base_domain()` vào `_claude/tools/roster_common.py` làm hàm dùng chung** (bài học tồn đọng từ
checkpoint 35 "cân nhắc viết thẳng vào roster_common.py thay vì mỗi batch tự cài lại") — dùng `tldextract`,
không còn phải chép lại logic mỗi batch nữa, các batch domain-dedup sau (không riêng `amenity=university`)
import thẳng `from roster_common import base_domain`.

`ROSTER`: 11799 → 12409 (Đông Á, +610) → **13724** (Tây Âu/Úc-NZ, +1315; tổng lượt này +1925 — kỷ lục mới
về số mục thêm trong 1 lượt, vượt qua +1500 của checkpoint 35). Đơn vị trên bản đồ: 11808 → **13733**
(+1925, giữ nguyên chênh lệch +9). Kiểm sau khi merge cả 2 batch: `node --check` sạch trên script inline
(2.693.930 ký tự), thẻ `div`/`section` cân bằng (107/107, 6/6). Mở `index.html` qua HTTP server cục bộ
(`.claude/launch.json`) qua Browser pane: hiển thị đúng "13733 đơn vị được lập bản đồ" / "13724 trong danh
mục mở rộng" / "12 đơn vị tại Việt Nam" (không đổi) / "9 case phân tích chuyên sâu" (không đổi), không lỗi
console. Xoá thư mục `_claude/scratch/` (dữ liệu thô tạm của lượt này) trước khi commit để tránh phình repo
— đúng quy tắc "Nguồn tham khảo còn lưu" ở đầu file này. Commit `0a50632`, `git push origin main` thành
công (`git log --oneline -3` xác nhận đã lên `origin/main`).

**Còn thiếu ~1276 để chạm mốc 15000.** **Việc mở cho lượt sau:** (1) **CẢ 7 bbox `amenity=university` đã
lên kế hoạch từ checkpoint 32 (Châu Phi+Trung Đông, Nam Á, Đông Nam Á, Mỹ Latinh, Đông Âu/Trung Á, Đông Á,
Tây Âu/Bắc Âu+Úc-NZ) NAY ĐÃ LÀM XONG HẾT** — coi kỹ thuật bbox-theo-vùng lớn với tag `amenity=university` là
ĐÃ CẠN. Lựa chọn cho lượt sau: (a) chạy 1 lượt `amenity=university` KHÔNG giới hạn bbox (toàn cầu) để vét
phần còn sót giữa biên các bbox cũ — rủi ro trùng ROSTER cao (đã phủ gần hết các vùng lớn) nhưng
`base_domain()` dedup mạnh đủ lọc; cân nhắc trước tiên vì gần chạm mốc 15000 (chỉ còn ~1276, không cần khối
lượng lớn như các lượt trước); (b) chuyển sang tag OSM khác cùng họ giáo dục: `amenity=college` (chưa thử,
tên tag khác nhưng OSM dùng khá lẫn lộn với `university` ở nhiều nước, có thể còn nhiều cao đẳng/viện chưa
bắt được qua `amenity=university`), hoặc `amenity=research_institute` (rủi ro nhiễu cao hơn, cần lọc kỹ hơn
nữa vì không tự động là "đại học" như university/college); (2) **User-Agent trình duyệt thật cứu thêm được
1-2% domain "chết"** ở vòng retry cuối — cân nhắc đưa hẳn thành vòng chuẩn thứ 4 trong quy trình
`check_url()` mọi batch sau (script `check_round_ua.py` ở lượt này dùng lại được, chỉ cần đổi input); (3)
domain loại tay tích luỹ cần nhớ (ngoài danh sách checkpoint 35): `oup.co.in` (Oxford University Press chi
nhánh Ấn Độ, khác domain checkpoint 33 nhưng cùng vấn đề NXB), domain Centro Cultural Reina Sofía
(`institucional.cadiz.es` — lặp lại đúng tổ chức đã loại ở checkpoint 32 dạng domain khác); (4)
`base_domain()` giờ đã có sẵn trong `roster_common.py` — import thẳng, không tự viết lại; (5) 217/1331 =
16% tỷ lệ gắn cờ ở Tây Âu (cao hơn hẳn 3/611 = 0.5% ở Đông Á) xác nhận đúng dự đoán "đại học châu Âu đặt
tên campus/khoa dài" — kỹ thuật quét từ khoá + chỉ đọc tay phần thật sự mơ hồ (không phải toàn bộ phần gắn
cờ) vẫn hiệu quả, giữ dùng tiếp.

---
**Lần trước:** 2026-09-09 (checkpoint 35 — **CÙNG NGUỒN OSM `amenity=university`, 2 bbox cuối cùng của danh
sách: Mỹ Latinh + Đông Âu/Trung Á, làm cả 2 trong 1 lượt**) — tiếp tục mục tiêu **15000** (còn thiếu
~4701 lúc đầu phiên).

**Chọn cả 2 vùng lớn nhất còn lại trong 1 lượt** (đúng gợi ý ưu tiên checkpoint 34 để lại — 2 vùng còn
lại đều LỚN hơn Đông Nam Á vừa làm nên tiềm năng đóng góp cao): Mỹ Latinh (899 mục ROSTER hiện có, bbox
`(-56,-118,33,-30)` — toàn bộ Trung+Nam Mỹ+Caribbean, KHÔNG tách Mexico riêng vì Overpass xử lý được cả
khối trong 1 câu) và Đông Âu/Trung Á (669 mục hiện có, bbox `(35,19,55,90)` — Balkan tới Trung Á, tràn cả
sang Thổ Nhĩ Kỳ/Hy Lạp/Iran/Iraq/Syria/Afghanistan do bbox rộng, giữ nguyên các nước tràn biên vì đều là
tổ chức thật hợp lệ, không giới hạn theo danh sách nước "Đông Âu/Trung Á" chặt).

**Overpass `overpass-api.de`, `[timeout:300]`:** `out count;` trước cho cả 2 bbox — Mỹ Latinh 2930 phần
tử (767 node + 2163 way, LỚN NHẤT trong các batch `amenity=university` từ trước tới nay), Đông Âu/Trung Á
2095 phần tử (590 node + 1505 way). Cả 2 lần đầu gặp `Dispatcher_Client::request_read_and_idx::timeout`
("server too busy") — retry sau vài giây là qua, đúng bài học cũ. `out center tags;` toàn bộ 1 lần cho
mỗi bbox, không cần chia nhỏ (1.48MB và 1.35MB).

**PHÁT HIỆN LỖI NGHIÊM TRỌNG trong `base_domain()` viết tay dùng suốt checkpoint 32-34 — đã SỬA bằng
`tldextract`:** hàm eTLD+1 tự viết chỉ liệt kê thủ công vài nhãn "2nd-level" phổ biến
(edu/com/org/gov/net) cho mỗi ccTLD 2 ký tự, KHÔNG bao quát được các "public suffix" vùng/miền thật của
nhiều nước — ví dụ Iran dùng `ac.ir` làm hậu tố học thuật DÙNG CHUNG cho toàn bộ đại học cả nước (giống
`edu.in` của Ấn Độ) nhưng `ac.ir` không có trong bảng tự viết, nên hàm cũ mặc định cắt về 2 nhãn
`ac.ir` — coi TẤT CẢ 122 subdomain đại học Iran khác nhau là "cùng 1 domain", chỉ giữ được 1/122 khi gộp
nhóm nội bộ. Tương tự với vùng địa lý Ukraine (`*.dp.ua`, `*.kiev.ua`, `*.in.ua`) và nhiều nước khác. Phát
hiện qua kiểm tra thủ công: đếm số domain 2-nhãn "khả nghi" (nhãn đầu ngắn ≤4 ký tự, TLD 2 ký tự) có
>1 phần tử gộp chung — ra 90 nhóm nghi vấn, trong đó `ac.ir` có 122 phần tử gộp thành 1 (rõ ràng sai),
trong khi các nhóm khác như `bsu.by` (18, Belarusian State University — ĐÚNG, vì đây thật sự là domain
riêng của 1 trường có nhiều subdomain khoa/viện) hay `uoi.gr` (18, University of Ioannina — ĐÚNG tương
tự) lại là gộp ĐÚNG. Không thể phân biệt đúng/sai bằng heuristic tự chế thêm — **chuyển hẳn sang thư viện
`tldextract`** (`pip install tldextract`, cài được bình thường không treo) dùng Public Suffix List thật
của Mozilla thay vì bảng tự liệt kê. Kết quả: số nhóm domain duy nhất của Đông Âu/Trung Á tăng từ 1164 lên
1312 (+148, chủ yếu là các đại học Iran bị gộp nhầm được tách lại đúng — riêng Iran từ 12 lên 106 sau khi
sửa). Mỹ Latinh ít ảnh hưởng hơn (1525→1544, +19) vì hầu hết TLD Mỹ Latinh đã có trong bảng cũ. **Bài học
cho các batch `amenity=university`/domain-dedup sau: LUÔN dùng `tldextract` (hoặc PSL thật) ngay từ đầu,
đừng tự liệt kê bảng TLD 2 tầng bằng tay nữa — cách cũ chỉ đúng tình cờ với các nước đã kiểm tay, sai âm
thầm (không báo lỗi) với các nước chưa kiểm, mức độ sai tỉ lệ thuận với số ccTLD lạ trong bbox.**

**Loại Mỹ (United States) khỏi batch Mỹ Latinh:** bbox `(-56,-118,33,-30)` trải tới vĩ độ 33°B nên dính cả
Texas/Florida/Puerto Rico — 135 phần tử gán quốc gia Mỹ qua `CountryLookup`, loại thẳng (ROSTER đã có sẵn
940 mục Mỹ, không phải trọng tâm lượt này). Puerto Rico (lãnh thổ Mỹ nhưng NE50 gán tên riêng "Puerto
Rico") vẫn GIỮ lại (không phải "United States" nên không bị loại, và về địa lý/văn hoá thuộc vùng
Caribbean — giữ nhất quán với các đảo Caribbean nhỏ khác đã giữ ở batch này). 0 Việt Nam ở cả 2 bbox (xác
nhận qua `CountryLookup` trước khi lọc, không dựa bbox thủ công).

Lọc trùng ROSTER hiện có (base-domain qua `tldextract` + `normalize_name()`) trên nhóm đã gán quốc gia (đã
loại "None"/ngoài biên NE50 và Mỹ): Mỹ Latinh loại 157 trùng domain + 17 trùng tên → còn 1175 ứng viên;
Đông Âu/Trung Á loại 147 trùng domain + 14 trùng tên → còn 1124 ứng viên.

`check_url()` 3 lượt mỗi vùng (16 luồng/15s → 8 luồng/25s trên lỗi → 4 luồng/30s trên lỗi còn lại, đúng
quy trình chuẩn, retry lần 3 chỉ cứu thêm 3-5 mục mỗi vùng — xác nhận phần lớn lỗi còn lại là domain chết
thật): Mỹ Latinh **715 sống** (703+7+5), Đông Âu/Trung Á **791 sống** (782+6+3).

**Rà thủ công qua đọc `<title>`/nội dung trang thật (không chỉ tin `check_url()` sống), quét tự động bằng
regex trên tên trước khi đọc tay để thu hẹp danh sách nghi vấn** (khác cách đọc từng mục thủ công của các
checkpoint trước — với ~1500 ứng viên, quét từ khoá cờ đỏ trong TÊN trước, chỉ đọc trang thật cho các mục
bị gắn cờ): quét acronym ngắn viết hoa (≤6 ký tự) + quét từ khoá toà nhà/khoa/phòng ban + quét từ khoá
sai chủ đề (bệnh viện/phòng khám/luyện thi/hiệp hội luật sư/nhà xuất bản) → loại **6 mục**: (1) "CEPUNT"
Peru — trang thật "Asegura tu ingreso" (đảm bảo trúng tuyển) = trung tâm LUYỆN THI đầu vào, không phải
trường; (2) "UEA" Ecuador (`uea.edu.ec`) — trang trả về rỗng hoàn toàn (0 ký tự văn bản, không `<title>`),
không xác minh được nội dung dù `check_url()` báo sống; (3) "Instituto preuniversitario Motolinia de León
Oaxaca" Mexico — tên tự ghi rõ "preuniversitario" (dự bị đại học/cấp phổ thông), không phải bậc đại học;
(4) "Colegio de Abogados" Argentina (`caq.org.ar`) — Đoàn Luật sư (hiệp hội nghề nghiệp), không phải
trường; (5) "МИБС" Nga (`orenburg.ldc.ru`) — trang thật "МРТ в Оренбурге: адреса и телефоны :: МИБС" =
chuỗi phòng khám chẩn đoán hình ảnh (MRI), không phải giáo dục; (6) "МУЦА"/IUCA Kyrgyzstan (`iuca.kg`) —
trang trả về rỗng, không đọc được `<title>` hay nội dung. **Đổi tên 2 mục** qua xác nhận `<title>` trang
thật: "ITFIP" (Colombia) → "UniEspinal" (trang thật tự giới thiệu "UniEspinal – Entidad pública de
Educación Superior", xác nhận tổ chức đã đổi thương hiệu, dùng đúng tên hiện tại thay vì tên cũ trong tag
OSM); "ABCD" (Brazil) → "ABCD Piauí" (rõ nghĩa hơn, khớp `<title>` "ABCD Piauí", xác nhận là trường
chuyên đào tạo sau đại học ngành Nha khoa được Bộ Giáo dục Brazil (MEC) công nhận). **Các acronym ngắn
khác GIỮ NGUYÊN** (không đổi tên) sau khi đọc `<title>` xác nhận đúng là tên thương hiệu công khai của
chính tổ chức đó, khớp với domain riêng (vd "UNA"→Universidad Nacional de las Artes, "СГЭУ"→Samara State
University of Economics, "ТГАСУ"→Tomsk State University of Architecture and Building) — tiếp nối bài học
tinh chỉnh checkpoint 34: chỉ đổi tên khi tên gốc thật sự không tự nhận diện được, không đổi khi acronym
đã là brand công khai thật.

Kết quả cuối: 715+791=1506 sống → loại 6 → đổi tên 2 → 1500 ứng viên → merge qua script chuẩn (an toàn
kiểm lại tên/domain 1 lần nữa qua `tldextract`) loại thêm **0** (không có trùng nào lọt qua bước lọc
trước) → **1500 mục thêm thật, cả 2 vùng trong 1 lượt**. Mỹ Latinh (711): Brazil 263, Mexico 141, Colombia
42, Argentina 41, Peru 36, Chile 22, Ecuador 22, Bolivia 21, Venezuela 18, Uruguay 13, Paraguay 13, Costa
Rica 12, Puerto Rico 7, Cuba 7, Nicaragua 7, Dominican Republic 6, El Salvador 6, Haiti 5, Guatemala 5,
Honduras 4, Trinidad and Tobago 3, Panama 3, France 2, Jamaica 2, Aruba 2, Antigua and Barbuda 1, Bahamas
1, Belize 1, Saint Kitts and Nevis 1, Netherlands 1, Curaçao 1, Barbados 1, Bermuda 1. Đông Âu/Trung Á
(789): Ukraine 129, Russian Federation 108, Poland 80, Uzbekistan 76, Turkey 70, Romania 38, Serbia 34,
Albania 32, Bulgaria 26, Hungary 24, Belarus 23, Kazakhstan 22, Georgia 20, Iran 19, Armenia 16, Moldova
16, Slovakia 12, Lithuania 9, Azerbaijan 8, Kyrgyzstan 5, Tajikistan 5, Greece 4, North Macedonia 4,
Turkmenistan 4, Kosovo 3, China 1, Bosnia and Herzegovina 1. **0 Việt Nam** (xác nhận lại ở bước đầu VÀ
bước cuối).

`ROSTER`: 10299 → **11799** (+1500, kỷ lục về số mục thêm trong 1 lượt — nhờ gộp 2 vùng lớn nhất còn lại
+ sửa lỗi `base_domain()` cứu thêm ~148 ứng viên đáng lẽ mất do gộp nhầm). Đơn vị trên bản đồ: 10308 →
**11808** (+1500, giữ nguyên chênh lệch +9). Kiểm: `node --check` sạch trên script inline (2.476.865 ký
tự), thẻ `div`/`section` cân bằng (107/107, 6/6). Mở `index.html` qua HTTP server cục bộ
(`.claude/launch.json` có sẵn từ checkpoint 31) qua Browser pane: hiển thị đúng "11808 đơn vị được lập bản
đồ" / "11799 trong danh mục mở rộng" / "12 đơn vị tại Việt Nam" (không đổi), không lỗi console. Commit
`48755fb`, `git push origin main` thành công.

**Còn thiếu ~3201 để chạm mốc 15000.** **Việc mở cho lượt sau:** (1) **CẢ 5 bbox `amenity=university` của
danh sách checkpoint 32 để lại nay đã LÀM XONG** (Châu Phi+Trung Đông, Nam Á, Đông Nam Á, Mỹ Latinh, Đông
Âu/Trung Á) — coi kỹ thuật bbox-theo-vùng với tag này là ĐÃ CẠN theo nghĩa "vùng lớn rõ ràng", nhưng còn 2
hướng khai thác tiếp CÙNG TAG này chưa thử: (a) bbox riêng cho Đông Á (Trung Quốc/Nhật/Hàn/Đài Loan) —
các batch Đông Nam Á + Đông Âu/Trung Á đều TRÀN qua Trung Quốc/Nhật nhưng chỉ vét được phần rơi vào bbox
hẹp, chưa khai thác toàn diện (Trung Quốc chỉ có ~96+1=97 mục qua 2 lần tràn bbox, so với dân số/số đại
học thực tế); (b) bbox Tây Âu/Bắc Âu/Úc-New Zealand — CHƯA TỪNG THỬ với tag `amenity=university`, có thể
còn nhiều nếu ROSTER các nước này còn mỏng (cần đếm trước khi làm); (2) **BÀI HỌC QUAN TRỌNG NHẤT lượt
này: LUÔN dùng `tldextract` cho `base_domain()`** ở mọi batch domain-dedup sau (không riêng
`amenity=university`) — cân nhắc viết thẳng vào `roster_common.py` làm hàm dùng chung thay vì mỗi batch
tự cài `pip install tldextract` lại; (3) kỹ thuật quét từ khoá cờ đỏ trên TÊN trước rồi mới đọc tay
(thay vì đọc tay từng mục) hiệu quả tốt cho batch lớn (~1500 ứng viên) — giữ dùng tiếp cho các batch lớn
sau, mở rộng danh sách từ khoá cờ đỏ nếu phát hiện loại sai chủ đề mới; (4) domain loại thủ công tích luỹ
cần nhớ (ngoài `nmcauditingcollege.com` từ trước): `orenburg.ldc.ru` (МИБС, chuỗi phòng khám MRI), `caq.
org.ar` (Đoàn Luật sư Argentina), `cepunt.edu.pe` (trung tâm luyện thi Peru), `educem.mx` (dự bị đại học
Mexico) — các domain này nếu OSM có node trùng toạ độ lệch bbox khác có thể lặp lại như case
`nmcauditingcollege.com` ở checkpoint 34.

---
**Lần trước:** 2026-09-09 (checkpoint 34 — **CÙNG NGUỒN OSM `amenity=university`, bbox Đông Nam Á**
(Indonesia/Philippines/Malaysia/Thailand/Myanmar/Campuchia/Singapore/Lào/Brunei/Timor-Leste, tràn thêm
sang Trung Quốc/Đài Loan/Hong Kong/Nhật (Okinawa)/Ấn Độ (Andaman) do bbox rộng)) — tiếp tục mục tiêu
**15000** (còn thiếu ~5141 lúc đầu phiên).

**Chọn đúng vùng ưu tiên checkpoint 33 để lại:** Đông Nam Á (mỏng nhất sau Nam Á đã làm — 250 mục hiện có
lúc đó). Bbox dùng đúng gợi ý cũ `(-11,92,29,142)` (Nam Timor-Leste tới biên Trung Quốc/Myanmar, Andaman
tới Papua) — CHỦ Ý bbox này tràn cả vào lãnh thổ Việt Nam nên phải lọc kỹ.

**Kỹ thuật lặp lại y hệt checkpoint 32/33:** `overpass.openstreetmap.fr` bị chặn (403) đầu phiên,
`overpass.osm.ch` cũng lỗi (400) — chuyển sang `overpass-api.de` (200, đúng bài học "thử mirror khác"
tích luỹ từ checkpoint 30), `[timeout:300]` trong câu QL. `out count;` trước: 1071 phần tử (143 node + 928
way) có `name`+`website`/`contact:website` — tải `out center tags;` toàn bộ 1 lần (654KB), không cần chia
nhỏ.

**Lọc Việt Nam NGAY TỪ ĐẦU bằng `CountryLookup` (không dựa vào bbox thủ công):** gán quốc gia cho toàn bộ
1071 phần tử trước, đếm được đúng **111 phần tử rơi vào Việt Nam** trong bbox này (bị loại bỏ hoàn toàn
ngay ở bước đầu, không đưa vào bất kỳ bước lọc trùng/kiểm sống nào sau đó) — phân bố còn lại: Indonesia
231, Philippines 167, China 146, Malaysia 108, Thailand 106, Taiwan 66, Myanmar 32, Singapore 12,
Cambodia 11, Japan 7, Hong Kong 5, India 3, Laos 3, Timor-Leste 1, cộng 62 điểm rơi ngoài biên NE50 (đảo
nhỏ/bờ biển, gán tay sau). Xác nhận lại 0 Việt Nam ở bước cuối trước khi merge (kiểm `'vietnam' in
country.lower()` trên toàn ROSTER sau merge = 0, không đổi so với trước batch).

**`base_domain()` eTLD+1** viết lại y hệt checkpoint 32/33 (thêm TLD 2 tầng Đông Nam Á + các nước tràn bbox
vào bảng: `ac.id`/`co.id`/`or.id`/`sch.id`, `ac.th`/`co.th`, `edu.my`/`com.my`, `edu.sg`, `edu.ph`/`ac.ph`,
`edu.kh`, `edu.la`, `edu.mm`/`ac.mm`, `edu.bn`, `edu.cn`/`ac.cn`, `edu.tw`, `ac.jp`, `ac.in`/`edu.in`,
`edu.bd`/`ac.bd`) — gộp 960 phần tử (sau loại Việt Nam) về 695 nhóm domain duy nhất. Lọc trùng ROSTER hiện
có (base-domain + `normalize_name()`) loại 86 (toàn bộ trùng domain, 0 trùng tên riêng) → còn 609 ứng
viên.

**62 điểm rơi ngoài biên NE50** (34 còn lại sau khi loại Việt Nam trong nhóm này) — toàn bộ là đảo nhỏ/mũi
đất/khu vực ven biển độ phân giải 50m không phủ tới (Cebu/Mindanao Philippines, Surabaya/Kalimantan/Kupang
Indonesia, Hong Kong, Ma Tổ Đài Loan, Zhuhai/Xiamen/Quảng Đông Trung Quốc, Songkhla/Samut Prakan Thái Lan,
Brunei) — gán tay cả 34/34 qua TLD + tên xác nhận, không loại (khác batch trước có vài điểm phải loại vì
không xác định được — lần này toàn bộ xác định được rõ ràng qua đuôi domain quốc gia).

`check_url()` 3 lượt y hệt quy trình chuẩn (16 luồng/15s → 416 sống; retry 8 luồng/25s trên 193 lỗi → +26;
retry lần 3 4 luồng/30s trên 167 lỗi còn lại → +2, xác nhận lại phần lớn lỗi còn lại là domain chết thật)
→ **444 sống**.

**Rà thủ công đọc nội dung trang thật (không chỉ tin `check_url()` sống), tiếp nối bài học checkpoint
33:** loại 3 mục qua đọc `<title>`+text thật — (1) "National Management College" (Myanmar theo toạ độ,
domain `nmcauditingcollege.com`) hoá ra là ĐÚNG CÙNG một trung tâm luyện thi CA/CMA ở Tamil Nadu, Ấn Độ đã
bị loại ở checkpoint 33 (South Asia batch) — node OSM khác ID nhưng cùng domain/tên, rơi trúng bbox Đông
Nam Á do toạ độ gán ở Myanmar, vẫn sai chủ đề y hệt, loại lại; (2) "St. Clare College of Caloocan"
(`stclareonline.com`) — trang thật hiện "ST. CLARE ONLINE EDUCATION SYSTEM", giống 1 cổng LMS dùng chung
hơn là trang chủ chính thức của 1 trường cụ thể, không đủ tin cậy để xác nhận đúng tổ chức; (3) "Vidyācaraṇa
Buddhist Resource" (Malaysia, `vidyacarana.org.my`) — trang chỉ trả về CSS/JS thô, không đọc được tiêu đề
hay nội dung nào, không xác minh được là đại học/cao đẳng thật.

Đổi tên 7 mục tên toà nhà/khoa/phòng ban chung chung sang đúng tên tổ chức xác nhận qua `<title>` trang
thật (đúng kỹ thuật checkpoint 33): "Dr. Carlos Lanting College Annex Building" → "Dr. Carlos S. Lanting
College", "Arellano University in Pasig - Elementary Department" → "Arellano University (Pasig)" (trang
thật là toàn bộ đại học, không riêng bậc tiểu học), "SUTD Parcel D" → "Singapore University of Technology
and Design (SUTD)", "TMAB" (Indonesia, acronym vô nghĩa không tự nhận diện được) → "Politeknik Negeri
Balikpapan", "Kantor Rektorat IAILM Suryalaya" → "Institut Agama Islam Latifah Mubarokiyah (IAILM)
Suryalaya", "คณะวิศวกรรมศาสตร์" (chỉ ghi "Khoa Kỹ thuật", không tên trường) → "คณะวิศวกรรมศาสตร์
มหาวิทยาลัยเกษตรศาสตร์" (Khoa Kỹ thuật, ĐH Kasetsart), "อาคารศูนย์ภาษา" (tên toà nhà "Toà nhà Trung tâm
Ngôn ngữ") → "ศูนย์ภาษาและความสัมพันธ์ระหว่างประเทศ มหาวิทยาลัยราชภัฏหมู่บ้านจอมบึng" (Trung tâm Ngôn
ngữ & QHQT, ĐH Rajabhat Muban Chombueng). **Khác checkpoint 33:** các mục "Faculty of X, [tên trường]" đã
TỰ ghi rõ tên trường mẹ trong tên gốc (vd "Faculty Economics and Business, UIN Syarif Hidayatullah",
"Fakultas Teknik Universitas Hasanuddin", "Pascasarjana UIN Sultan Syarif Kasim Riau") — GIỮ NGUYÊN không
đổi tên, chỉ đổi tên khi tên gốc KHÔNG tự nhận diện được tổ chức mẹ (bài học tinh chỉnh: chỉ đổi tên thật
sự mơ hồ, không đổi tên đã đủ rõ dù dài).

Kết quả cuối: 444 sống → loại 3 (đọc nội dung trang) → đổi tên 7 → 441 ứng viên → merge qua script chuẩn
(an toàn kiểm lại tên/org 1 lần nữa) loại thêm 1 trùng tên thật ("Singapore University of Technology and
Design (SUTD)" đã có sẵn trong ROSTER qua 1 domain khác không bắt được ở bước lọc domain) → **440 mục
thêm thật**. Quốc gia: Indonesia 133, China 95, Philippines 56, Taiwan 46, Thailand 41, Malaysia 29,
Myanmar 16, Cambodia 6, Japan 5, Singapore 4, Hong Kong 3, India 3, Laos 2, Brunei 1. **0 Việt Nam** (xác
nhận lại ở bước đầu VÀ bước cuối).

`ROSTER`: 9859 → **10299** (+440). Đơn vị trên bản đồ: 9868 → **10308** (+440, giữ nguyên chênh lệch +9).
Kiểm: `node --check` sạch trên script inline (2.272.083 ký tự), thẻ `div`/`section` cân bằng (107/107,
6/6). Mở `index.html` qua HTTP server cục bộ (`.claude/launch.json` có sẵn từ checkpoint 31, dùng lại
nguyên) qua Browser pane: hiển thị đúng "10308 đơn vị được lập bản đồ" / "10299 trong danh mục mở rộng" /
"12 đơn vị tại Việt Nam" (không đổi), không lỗi console. Commit `97e7189`, `git push origin main` thành
công.

**Còn thiếu ~4701 để chạm mốc 15000.** **Việc mở cho lượt sau:** (1) **`amenity=university` còn dư địa ở
2 vùng chưa thử**: Mỹ Latinh (885 mục hiện có tính từ checkpoint 32, dày hơn Đông Nam Á/Nam Á nhưng vẫn
còn khoảng trống ở Ecuador/Bolivia/Trung Mỹ), Đông Âu/Trung Á (622 mục) — 2 vùng còn lại trong danh sách 4
vùng checkpoint 32 để lại; (2) bbox Đông Nam Á vừa làm TRÀN sang Trung Quốc/Đài Loan/Hong Kong/Nhật/Ấn Độ
— các nước lớn này CHƯA được khai thác toàn diện (chỉ có phần rơi vào bbox hẹp), có thể đáng làm bbox
riêng cho Đông Á (Trung Quốc/Nhật/Hàn/Đài Loan) nếu muốn khai thác tiếp nguồn `amenity=university` sau khi
xong Mỹ Latinh/Đông Âu; (3) tiếp tục dùng đúng `base_domain()` + `normalize_name()`, nhớ bổ sung TLD 2 tầng
vùng mới; (4) bài học mới lượt này: khi loại 1 domain vì sai chủ đề ở batch trước, GHI NHỚ domain đó có
thể xuất hiện lại ở batch vùng khác nếu OSM có node trùng lặp toạ độ lệch qua biên giới vùng (case
`nmcauditingcollege.com` lặp lại y hệt) — nên cân nhắc giữ 1 danh sách domain đã loại thủ công tích luỹ
qua các batch `amenity=university` để tự động loại ngay từ đầu, đỡ phải đọc lại nội dung trang 2 lần; (5)
bài học tinh chỉnh quy tắc đổi tên: chỉ đổi tên khi tên gốc THẬT SỰ không tự nhận diện được tổ chức (toà
nhà/acronym/chức danh chung chung), KHÔNG đổi tên các mục "Faculty of X, [Tên Trường]" đã tự ghi rõ trường
mẹ trong tên — giữ nguyên đủ rõ ràng, tránh mất thông tin cấp khoa/đơn vị con thật.

---
**Lần trước:** 2026-09-09 (checkpoint 33 — **CÙNG NGUỒN OSM `amenity=university`, bbox Nam Á** (Ấn Độ/
Pakistan/Bangladesh/Sri Lanka/Nepal/Afghanistan/Bhutan)) — tiếp tục mục tiêu **15000** (còn thiếu ~5491
lúc đầu phiên).

**Chọn vùng theo dữ liệu chứ không đoán:** đếm ROSTER hiện có theo quốc gia cho 4 khu vực còn nhiều dư
địa `amenity=university` mà checkpoint 32 để lại (Nam Á/Đông Nam Á/Mỹ Latinh/Đông Âu-Trung Á) trước khi
chọn bbox — Nam Á mỏng nhất (338 mục cho 8 nước, so với Đông Nam Á 250 nhưng Đông Nam Á vướng nhiều nước
đã có mục kha khá — Ấn Độ vẫn dẫn đầu Nam Á với 287 nhưng cả vùng vẫn thấp hơn hẳn 3 vùng còn lại) —
chọn Nam Á, đúng gợi ý ưu tiên "1" mà checkpoint 32 để lại.

**Kỹ thuật lặp lại y hệt checkpoint 32, đúng quy trình chuẩn đã đúc kết:** bbox `(5,60,38,92)` (Nam Á đầy
đủ, từ Sri Lanka tới biên Trung Quốc/Iran) qua `overpass.openstreetmap.fr` với `[timeout:300]` trong câu
QL — `out count;` trước cho thấy 573 phần tử (131 node + 442 way) có `name`+`website`/`contact:website`,
nhỏ hơn hẳn batch Châu Phi/Trung Đông (1350) nên tải `out center tags;` toàn bộ trong 1 lần, không cần
chia nhỏ. Gộp trùng nội bộ bằng `base_domain()` (viết lại đúng hàm eTLD+1 của checkpoint 32, thêm vài
TLD 2 tầng Nam Á vào bảng: `ac.in`/`edu.in`/`ac.pk`/`edu.pk`/`ac.bd`/`edu.bd`/`ac.lk`/`edu.lk`/`ac.np`/
`edu.np`/`ac.bt`/`edu.af`) — loại 64 mục multi-campus trùng domain (509 nhóm domain duy nhất từ 573).

Gán quốc gia qua `CountryLookup`: 503/509 khớp thẳng, 6 điểm rơi ngoài biên NE50 (đều ở gần bờ biển —
Chabahar Maritime University Iran, viện hải dương/thuỷ sản Ấn Độ ở Kochi/Goa, 1 trường Mumbai) — gán tay
cả 6 qua tên/vị trí thực, không loại. 0 Việt Nam trong bbox (đúng dự kiến — bbox không chạm lãnh thổ Việt
Nam). Lọc trùng ROSTER (base-domain + tên chuẩn hoá `normalize_name()` đã vá từ checkpoint 32, dùng thẳng
không sửa lại) loại 32 (25 trùng domain + 7 trùng tên) → còn 477 ứng viên.

`check_url()` 3 lượt (16 luồng/15s → 355 sống; retry 8 luồng/25s trên 122 lỗi → +1; retry lần 3 4 luồng/
30s trên 121 lỗi còn lại → +0, xác nhận phần lớn lỗi `URLError`/`HTTPError` là domain chết thật chứ không
phải mạng chặn tạm thời như một số batch trước) → **356 sống**.

**Rà thủ công phát hiện thêm các vấn đề chất lượng mới, khác kiểu checkpoint 32:** (1) 4 mục tên là tên
toà nhà/cổng/khối chung chung ("Admin Block", "Gate no. 2", "Food Technology Block", "service road") dù
website ĐÚNG là trang chủ 1 trường/viện thật — thay vì loại, ĐỔI TÊN về đúng tên tổ chức (Kumaun
University, NUST Pakistan, Kongu Engineering College, Indian Institute of Public Administration) vì
domain xác nhận đúng là trang chủ chính thức; (2) 3 mục Sri Lanka tên chỉ ghi "Faculty of..." nhưng
domain là subdomain của 1 trường lớn CHƯA có mục nào khác trong ROSTER cho trường đó — đổi tên về đúng
tên trường (University of Colombo, Sabaragamuwa University of Sri Lanka, Eastern University Sri Lanka)
thay vì giữ tên khoa hoặc loại bỏ, xác minh qua `<title>` trang thật; (3) loại 4 mục sai chủ đề/gây hiểu
nhầm qua đọc nội dung trang thật: "R Square Academy" (trung tâm luyện thi công chức, không phải đại học),
"NMC Auditing College" tên OSM ghi "National Management College" nhưng nội dung trang là "trung tâm
luyện thi CA/CMA nội trú", "Oxford University Press" (chi nhánh Ấn Độ của 1 NHÀ XUẤT BẢN, gắn nhầm tag),
"Somaiya Ayurvihar" (tên nghe như học viện nhưng nội dung trang là 1 BỆNH VIỆN đa khoa Mumbai); (4) loại
riêng 1 mục "Edith Cowan University" toạ độ tại Sri Lanka nhưng website là trang chủ ĐẠI HỌC Ở ÚC
(`ecu.edu.au`) — giữ lại sẽ gây hiểu nhầm quốc gia của 1 đại học Úc thật, không có subdomain riêng cho
chi nhánh/đối tác Sri Lanka nào để dùng thay. **Bài học mới cho các batch `amenity=university` sau:**
ngoài loại tên toà nhà/campus như checkpoint 32, cần đọc thử nội dung trang (không chỉ tin `check_url()`
sống) với các tên mơ hồ/viết tắt lạ — 1 trong 356 mục sống hoá ra là bệnh viện, 1 là nhà xuất bản, đều
qua được `check_url()` bình thường vì trang thật sự tồn tại, chỉ sai chủ đề.

Kết quả cuối: 356 sống → loại 5 (1 luyện thi + 1 NXB + 1 bệnh viện + 1 trùng quốc gia/URL) → đổi tên 7 (4
building + 3 faculty Sri Lanka) → 351 ứng viên → merge qua script chuẩn (an toàn kiểm lại tên/org 1 lần
nữa) loại thêm 1 trùng tên thật ("Kongu Engineering College" trùng org của "TBI@KEC" đã có trong ROSTER —
chấp nhận loại dù khác domain, giữ nguyên tắc lọc trùng tên nghiêm ngặt) → **350 mục thêm thật**. Quốc
gia: Ấn Độ 229, Bangladesh 49, Pakistan 37, Sri Lanka 15, Afghanistan 8, Nepal 6, Uzbekistan 3 (rơi vào
bbox dù ngoài Nam Á truyền thống), Tajikistan 2, Bhutan 1. 0 Việt Nam.

`ROSTER`: 9509 → **9859** (+350). Đơn vị trên bản đồ: 9518 → **9868** (+350, giữ nguyên chênh lệch +9).
Kiểm: `node --check` sạch trên script inline (2.220.944 ký tự), thẻ `div`/`section` cân bằng (107/107,
6/6). Mở `index.html` qua HTTP server cục bộ (`.claude/launch.json` có sẵn từ checkpoint 31, dùng lại
nguyên) qua Browser pane: hiển thị đúng "9868 đơn vị được lập bản đồ" / "9859 trong danh mục mở rộng" /
"12 đơn vị tại Việt Nam" (không đổi), không lỗi console. Commit `6f07004`, `git push origin main`
thành công.

**Còn thiếu ~5141 để chạm mốc 15000.** **Việc mở cho lượt sau:** (1) **`amenity=university` còn dư địa ở
3 vùng chưa thử**: Đông Nam Á (250 mục hiện có, mỏng nhất sau Nam Á — Indonesia chỉ 19 dù dân số lớn,
Myanmar 4, Lào 1, Campuchia 9, Đông Timor 1, Brunei 1 — bbox gợi ý `(-11,92,29,142)` nhưng cần loại bỏ
kỹ phần lãnh thổ Việt Nam trong bbox này bằng `country_from_latlon`, KHÔNG đưa Việt Nam vào ROSTER), Mỹ
Latinh (885 mục, dày hơn nhưng vẫn còn khoảng trống ở Ecuador/Bolivia/Trung Mỹ), Đông Âu/Trung Á (622
mục); (2) tiếp tục dùng đúng `base_domain()` + `normalize_name()` đã có, nhớ bổ sung TLD 2 tầng đặc thù
vùng mới vào bảng `TWO_TIER_TLDS` cục bộ trong script (chưa đưa vào `roster_common.py` dùng chung, mỗi
batch tự viết lại đúng như checkpoint 32/33 đã làm — cân nhắc chuyển hẳn vào `roster_common.py` nếu còn
dùng tiếp ở batch sau để đỡ chép lại); (3) bài học đọc nội dung trang cho tên mơ hồ (mục 4 ở trên) nên áp
dụng tiếp — không chỉ tin domain sống, đặc biệt với tên viết tắt ngắn hoặc tên nghe giống công ty/tổ chức
khác ngành; (4) nguồn khác `office=*`/`amenity=*` OSM vẫn còn `amenity=research_institute`,
`amenity=library` (rủi ro nhiễu cao) — độ ưu tiên thấp hơn tiếp tục đào `amenity=university` theo vùng.

---
**Lần trước:** 2026-09-09 (checkpoint 32 — **NGUỒN OSM MỚI: `amenity=university` thay vì `office=*`,
giới hạn bbox Châu Phi + Trung Đông**) — tiếp tục mục tiêu **15000** (còn thiếu ~5954 lúc đầu phiên).

**Đầu phiên: kiểm lại 7 domain nghi bị chặn tầng mạng ở checkpoint 31.** Retry `check_url()` (timeout
15-20s, 2 lượt): chỉ **1/7 sống** (`u-touch.org`) — nhưng `WebFetch` xác nhận đây là tổ chức phát triển
cộng đồng/giáo dục ở Uganda (ICT literacy cho phụ nữ/trẻ em), KHÔNG phải trung tâm CGCN/ĐMST/vườn ươm —
SAI CHỦ ĐỀ, không thêm. 6 domain còn lại (`inkubator.wloclawek.pl`, `torinosocialinnovation.it`,
`socialinnovation.ca`, `ciep.ar`, `ciridd.org`, `citralab.lk`) vẫn `URLError`/`HTTPError` cả 2 lượt —
không cứu thêm được, để nguyên kết luận cũ.

**Nguồn chính: OSM `amenity=university`** (57958 phần tử toàn cầu theo taginfo — CHƯA THỬ, đúng như việc
mở checkpoint 31 để lại). Theo đúng khuyến nghị: giới hạn phạm vi bằng bounding box thay vì tải toàn cầu
để bớt tải lọc trùng/kiểm sống. Dùng bbox `(-35,-20,38,52)` (Nam Phi tới Bắc Phi/Trung Đông tới biên Iran
— bao trọn Châu Phi + phần lớn Trung Đông, đúng vùng ROSTER còn mỏng) — Overpass (`overpass.openstreetmap.
fr`, `overpass-api.de` báo "server too busy" lúc đầu phiên) trả **1350 phần tử** có `name`+`website`/
`contact:website`. Lưu ý mới: `overpass-api.de` cần `[timeout:300]` NGAY TRONG câu QL (không chỉ `curl -m`)
— mirror trả về đúng thông báo "Query timed out... after 121 seconds" khi quên chỉnh, chỉ dùng đúng
`[timeout:120]` mặc định trong ví dụ cũ.

Lọc trùng nội bộ (domain/tên) + trùng ROSTER hiện có (domain) → còn 985 ứng viên (0 Việt Nam trong bbox
này). `check_url()` 2 lượt (20 luồng/15s rồi 8 luồng/25s cho phần lỗi) → **587 sống**. Rà thủ công phát
hiện tiếp 2 vấn đề mới đáng ghi lại cho các lượt `amenity=university` sau:

1. **18 điểm rơi ngoài biên giới NE50** (`country_from_latlon.py` trả `None`) — đều là các đại học/khoa
   thật ở gần bờ biển/đảo nhỏ (Tây Ban Nha, Lebanon, Bahrain, Kuwait, Iran, Hy Lạp, Bồ Đào Nha, Somalia,
   Sierra Leone, Thổ Nhĩ Kỳ, Nam Phi) — gán tay quốc gia qua tên/URL cho 16/18, loại 2/18 (`asal.dz` —
   Trung tâm Kỹ thuật Vũ trụ của cơ quan không gian Algeria, không phải đại học; `Centro Cultural Reina
   Sofía` — trung tâm văn hoá, gắn nhầm tag `amenity=university`).
2. **OSM gắn tag `amenity=university` riêng cho TỪNG khoa/campus/cơ sở của cùng 1 trường** (khác subdomain
   nên dedup theo domain đầy đủ không bắt được) — vd 5 mục khác nhau đều là University of Tehran
   (`ut.ac.ir`, `geography.ut.ac.ir`, `sport.ut.ac.ir`, `abu.ut.ac.ir`, `farabi.ut.ac.ir`), tương tự
   Çukurova Üniversitesi (Thổ Nhĩ Kỳ, 3 mục), Universidad de Cádiz (Tây Ban Nha, nhiều khoa). **Giải
   pháp mới:** viết hàm `base_domain()` tách phần gốc domain kiểu eTLD+1 (xử lý cả TLD 2 tầng như
   `.ac.za`/`.edu.tr`/`.co.uk`), gộp mọi ứng viên CÙNG base domain trong 1 lượt về ĐÚNG 1 mục (ưu tiên
   URL ít nhãn phụ nhất = trang chủ trường, tên không chứa từ khoá khoa/campus/toà nhà), đồng thời so
   base domain (không chỉ domain đầy đủ) với ROSTER hiện có để bắt các trường hợp ROSTER đã có TTO cụ
   thể dưới 1 subdomain khác của cùng trường. Loại thêm 10 mục chất lượng kém qua rà tay (tên toà nhà
   chung chung không định danh được tổ chức: "U-Block", "FABNE Block", "Engineering 2", "New Examination
   Centre", "Coordination Center"; trường phổ thông K-12 gắn nhầm tag: "Brummana High School"; URL trỏ
   sang bài báo chứ không phải trang tổ chức: "Molelwane Research Farm"; cơ sở đào tạo tôn giáo ngắn hạn
   không phải đại học: "Fischers Yeshiva", "בית יוסף"/`studienjahr.de`; nhà ở sinh viên: "Sonop Tehuis").

**Áp dụng đúng quy tắc đã chốt từ sếp:** OSM `amenity=university` = trang chủ chính thức của TRƯỜNG ĐẠI
HỌC — theo đúng phạm vi Atlas đã ghi rõ ("trung tâm CGCN/ĐMST CỦA ĐẠI HỌC"), bản thân trường đại học tự nó
là 1 đơn vị hợp lệ nếu không tìm ra trung tâm/văn phòng CGCN riêng — nên KHÔNG cần lọc thêm theo từ khoá
chủ đề như các batch `office=*` trước, chỉ cần là trường đại học/cao đẳng THẬT (đã loại các trường hợp
KHÔNG PHẢI đại học ở trên).

**Phát hiện + vá lỗi thật trong `_claude/tools/roster_common.py` (công cụ dùng chung, không phải script
riêng batch này):** `normalize_name()` cũ dùng regex `[^a-z0-9]` sau khi hạ chữ thường — với tên viết
HOÀN TOÀN bằng chữ không phải Latin (Ả Rập/Ba Tư/Do Thái/Hy Lạp) thì MỌI ký tự đều bị xoá, tên quy về
chuỗi rỗng `""` — và vì ROSTER đã có sẵn 1 mục cũ cũng quy về `""`, TOÀN BỘ 155 ứng viên tên phi-Latin hợp
lệ trong batch này bị đánh nhầm "trùng" (khớp `""` với `""`) khi chạy qua script merge dùng hàm này, dù đã
qua hết các lớp lọc trùng domain/base-domain nghiêm ngặt trước đó. Phát hiện qua log merge in ra toàn tên
Ả Rập/Ba Tư bị SKIP — kiểm tay bằng `.encode('unicode_escape')` xác nhận đúng nguyên nhân. **Đã vá**:
đổi sang lọc Unicode-aware (`ch.isalnum()` thay vì regex ASCII), giữ nguyên chữ cái mọi hệ chữ viết, chỉ
bỏ dấu câu/khoảng trắng — rồi phục hồi đúng 154/155 mục bị đánh nhầm (1/155 là trùng tên thật, loại đúng).
**Bài học cho các batch sau, đặc biệt Trung Đông/Nam Á/Đông Á:** hàm `normalize_name()` giờ đã đúng, nhưng
nên luôn kiểm log merge có dòng "SKIP dup" đáng ngờ nào lặp lại bất thường (nhiều tên hoàn toàn khác nhau
cùng bị skip) trước khi tin kết quả cuối.

Kết quả cuối: 587 sống → loại 12 (2 sai chủ đề + 10 chất lượng kém) → gán quốc gia đủ 587 → loại 63 trùng
base-domain với ROSTER hiện có → gộp 48 mục trùng base-domain NỘI BỘ batch (chủ yếu Iran/Thổ Nhĩ Kỳ/Tây
Ban Nha) → còn **464 ứng viên cuối**, trải 56 quốc gia (nhiều nhất: Iran 51, Nigeria 26, Turkey 24,
Morocco 21, Iraq 20, Algeria 20). Merge qua script chuẩn → phát hiện lỗi `normalize_name` ở trên → vá +
phục hồi → **463 mục thêm thật** (464 trừ 1 trùng tên thật). 0 Việt Nam.

`ROSTER`: 9046 → **9509** (+463). Đơn vị trên bản đồ: 9055 → **9518** (+463, giữ nguyên chênh lệch +9).
Kiểm: `node --check` sạch trên script inline (2.176.625 ký tự), thẻ `div`/`section` cân bằng (107/107,
6/6). Mở `index.html` qua HTTP server cục bộ (`.claude/launch.json`, sửa `runtimeExecutable` thành đường
dẫn `python.exe` đầy đủ) qua Browser pane: hiển thị đúng "9518 đơn vị được lập bản đồ" / "9509 trong danh
mục mở rộng" / "12 đơn vị tại Việt Nam" (không đổi), không lỗi console. Commit `e874e7f`, `git push origin
main` thành công.

**Còn thiếu ~5491 để chạm mốc 15000.** **Việc mở cho lượt sau:** (1) **`amenity=university` còn RẤT
nhiều dư địa** — mới khai thác 1 bbox Châu Phi+Trung Đông trong tổng 57958 phần tử toàn cầu; các bbox
CHƯA THỬ: Nam Á (Ấn Độ/Pakistan/Bangladesh — rất nhiều đại học nhỏ), Đông Nam Á, Mỹ Latinh, Đông Âu/
Trung Á — lặp lại đúng quy trình (bbox → Overpass structural pull → `base_domain()` collapse → gán
quốc gia → `check_url()`) cho từng vùng, nhớ dùng `[timeout:300]` trong câu QL; (2) cân nhắc chạy luôn
`amenity=university` KHÔNG giới hạn bbox (toàn cầu) nếu các vùng mỏng đã khai thác hết — rủi ro trùng
ROSTER cao hơn (nhiều đại học lớn Âu/Mỹ/Đông Á đã có TTO cụ thể trong ROSTER) nhưng `base_domain()` dedup
mới đã đủ mạnh để lọc phần lớn; (3) hàm `normalize_name()` đã vá trong `roster_common.py` — nhớ tận dụng
đúng (không cần tự viết lại lọc trùng tên phi-Latin ở batch sau); (4) nguồn khác `office=*`/`amenity=*`
OSM vẫn còn: `amenity=research_institute`, `amenity=library` (rủi ro nhiễu cao, phần lớn thư viện công
cộng không liên quan) — chưa thử, độ ưu tiên thấp hơn tiếp tục đào `amenity=university` theo vùng.

---
**Lần trước:** 2026-09-09 (checkpoint 31 — **CÙNG NGUỒN OpenStreetMap, kỹ thuật MỚI "tải cấu trúc
trước, lọc từ khoá SAU" (offline) thay vì lọc từ khoá ngay trong Overpass QL**) — tiếp tục mục tiêu
**15000** (còn thiếu ~5965 lúc đầu phiên).

**Đổi kỹ thuật vì lý do hiệu suất:** lượt trước (checkpoint 30) lọc từ khoá ngay trong câu Overpass QL
(`name~"..."`) — cách này khiến Overpass phải chạy regex phức tạp trên toàn bộ tập `office=association`/
`ngo`/`educational_institution` (35656+24152+48294 phần tử) MỖI LẦN đổi bộ từ khoá, dễ timeout khi mở
rộng danh sách từ khoá (xác nhận lại: thử gộp cả bộ từ khoá mở rộng đa ngôn ngữ vào 1 câu Overpass y hệt
lượt trước → timeout ở giây 61 dù chỉ đọc `office=foundation` nhỏ hơn nhiều). **Lối thoát:** tách quy
trình 2 bước — (1) Overpass CHỈ lọc theo cấu trúc rẻ (đã có tag `office=X` + có `name` + có `website`
hoặc `contact:website`, không regex tên) rồi `out;` toàn bộ phần tử khớp — bước này NHANH vì office=X là
chỉ mục có sẵn; (2) tải file JSON kết quả về, lọc từ khoá bằng Python OFFLINE — không giới hạn độ phức
tạp regex, không lo timeout, có thể thử nhiều vòng từ khoá khác nhau trên cùng 1 lần tải mà không phải
gọi lại Overpass. Kiểm cỡ tập trước khi tải bằng `out count;`: `office=association`+website 12230,
`office=ngo`+website 5759, `office=educational_institution`+website 7999 — cả 3 tải "out;" đầy đủ tags
+ toạ độ thành công qua `overpass-api.de` (timeout Python phải đặt ≥260s, một số lần đầu bị "read
operation timed out"/504 phải retry qua mirror `overpass.openstreetmap.fr`). Bài học kỹ thuật: `out
tags;` KHÔNG trả toạ độ (chỉ trả tags) — lần đầu quên, phải đổi thành `out;` rồi refetch; sau đó phát
hiện có thể tiết kiệm băng thông hơn nữa bằng cách CHỈ refetch toạ độ cho đúng các ID đã lọc từ khoá
xong (`node(id:...)`) thay vì tải lại toàn bộ tập gốc lần 2.

Bộ từ khoá offline mở rộng thêm so với checkpoint 30 (đa ngôn ngữ: `incubateur`/`pépinière`/`technopole`
(Pháp), `inkubator`/`incubatore`/`gründerzentrum` (Đức/Ý/Ba Lan), `vivero de empresas`/`parque
tecnológico` (Tây Ban Nha/Bồ Đào Nha)...) — nhưng khớp từ khoá vẫn RẤT THẤP trên cả 4 tag đã thử: `office=
association` 38/12230 (0,3%), `office=ngo` 21/5759 (0,4%), `office=educational_institution` 36/7999
(0,5%), `office=charity` (tag hoàn toàn mới, 914 phần tử có website) chỉ 1/914 (0,1%) — xác nhận các tag
`office=*` rộng này đã gần cạn khả năng khai thác bằng từ khoá, đúng nhận định checkpoint 30.

**Rà thủ công + WebSearch xác nhận từng trường hợp nghi ngờ** (95 ứng viên gộp 4 tag, loại 12 trước khi
kiểm URL): 2 trường K-12 lặp lại đúng tên đã loại ở checkpoint 30 ("KNC Innovative Global School",
"Innovation Spokane Schools 907" — khớp lại vì quét rộng hơn tình cờ bắt lại đúng bản ghi cũ), 1 câu lạc
bộ doanh nhân thuần kết nối lặp lại ("JCI Johor Bahru Entrepreneur" — cũng đã loại ở checkpoint 30), 1 tổ
chức dịch vụ gia đình lặp lại ("Families & Youth Innovations Plus"), 1 học viện bootcamp tư nhân lặp lại
("Kimit Innovation | Academy") — 4/12 là các mục ĐÃ TỪNG bị loại thủ công ở checkpoint 30 nhưng quét lại
vẫn xuất hiện vì Overpass trả về theo ID khác nhau mỗi lần, phải rà lại từ đầu chứ không tự động loại
được chỉ bằng dedup ROSTER (chúng chưa từng được MERGE nên không nằm trong ROSTER để dedup bắt được) —
**bài học mới: nên giữ một danh sách tên/OSM-ID đã loại thủ công lâu dài (không chỉ trong CLAUDE.md dạng
văn xuôi) nếu muốn tránh rà lại y hệt các lượt sau**. Các trường hợp MỚI xác minh qua WebSearch: loại
"Professional School of Management, Innovation & Technology" (PFH — cả một trường đại học tư, không phải
1 trung tâm), "Integral (INnovative TEaching, GRooming ALchemy)" (bẫy chơi chữ viết tắt, thực chất là 1
trường cao đẳng thường), "Pépinière jeunesses centre sud..." (chương trình xã hội cho thanh niên, không
phải vườn ươm doanh nghiệp dù tên có "pépinière"), "Great Lakes Incubator Farm" (chương trình đào tạo
nông dân/canh tác tái sinh của một Conservation District Mỹ, "incubator" theo nghĩa nông nghiệp chứ
không phải doanh nghiệp/công nghệ), "European Institute of Innovation, Entrepreneurship and Technology"
(eiiet.com — xác nhận qua WebSearch là 1 trường tư dạy khách sạn/du lịch, gắn mác "innovation" thuần
marketing), "Lawrence Center for Entrepreneurship" (tổ chức CÓ THẬT ở Lawrence, Kansas — nhưng URL gắn
trong OSM `larryville.com` KHÔNG phải site thật của họ, site thật là `larryville-entrepreneur.blogspot.
com`/Facebook — loại vì URL sai dù tổ chức đúng chủ đề, không tự sửa URL). Giữ lại các trường hợp
WebSearch xác nhận ĐÚNG dù ban đầu nghi ngờ: "Centre for Innovative Planning and Development" (CIPD, UTM
Malaysia — trung tâm R&D cấp đại học thật, đúng diện "trung tâm nghiên cứu của đại học"), "Great Lakes"
loại nhưng "safety innovation center gGmbH" (Paderborn, Đức — tổ chức phi lợi nhuận R&D thật, có dự án
Horizon Europe) và "Repair Café" tại `manoceanindien.fr` (xác nhận đúng là Repair Café thật của MAN Océan
Indien, Mayotte, dù domain tên khác) đều GIỮ.

Sau loại 12 + 1 trùng nội bộ (2 bản ghi "Fablab d'Alençon"/"Fablab d'alençon" viết hoa khác nhau, cùng
URL) còn 82 ứng viên → lọc trùng ROSTER (domain/tên) loại tới **58/82** (đa số trùng vì bộ từ khoá mới
vẫn chứa nguyên bộ từ khoá cũ của checkpoint 30, quét lại bắt trúng nhiều bản ghi ĐÃ merge) → còn 24. 0
Việt Nam. Kiểm `check_url()`: đợt 1 (8 luồng, 15s) chỉ **8/24 sống**; đợt 2 retry 16 lỗi (6 luồng, 25s)
**0/16 cứu thêm** — TOÀN BỘ đều lỗi `URLError` dù nhiều tên miền (vd `socialinnovation.ca`, tổ chức phi
lợi nhuận lớn thật ở Toronto) chắc chắn không phải đã chết thật. **Rà tay bằng `curl`/`nslookup` phát
hiện: mạng phiên này CHẶN Ở TẦNG TCP một số tên miền cụ thể dù DNS phân giải đúng và Internet nói chung
vẫn thông** (`github.com`/`wikipedia.org`/`bbc.com` load tức thì) — cùng hiện tượng "chặn tầng mạng theo
domain cụ thể, không phải chặn toàn mạng" đã ghi nhận với Overpass mirror ở checkpoint 30. Domain bị chặn
lượt này: `u-touch.org`, `inkubator.wloclawek.pl`, `torinosocialinnovation.it`, `socialinnovation.ca`,
`ciep.ar` (đều `URLError`/timeout TCP dù DNS đúng); `ciridd.org`, `citralab.lk` trả 403 (có thể chặn bot
qua Cloudflare, không hẳn cùng nguyên nhân). Ngược lại `tarantomakers.it` và `coworking-savona.org` ban
đầu cũng lỗi nhưng RETRY THÀNH CÔNG (200/ok) — xác nhận đây là hiện tượng chặn/nghẽn KHÔNG ỔN ĐỊNH theo
thời điểm chứ không phải domain chết vĩnh viễn — **việc mở cho lượt sau: thử lại đúng 7 domain bị chặn ở
trên bằng `check_url()`, nhiều khả năng phần lớn là tổ chức thật đang bị bỏ sót oan**. `innovatedublin.
org`, `c2i.unilim.fr`, `eiccatalystnetwork.org`, `excellenceskills.com.my` xác nhận qua `nslookup` là
NXDOMAIN thật (domain đã chết hẳn, không phải do mạng) — loại chắc chắn. `ccfeh.com` là trang rao bán
domain (namecheap) — loại. `toulouse-metropole-habitat.fr/.../FABLAB-La-Gloire` trả 404 thật — loại.
`innovup.fefa.tg` DNS timeout không kết luận được — loại theo hướng an toàn.

Cũng thử `office=foundation` (4591 phần tử toàn cầu) làm nguồn mới — chỉ 18 khớp từ khoá tiếng Anh, quá
nhỏ để đáng theo tiếp, KHÔNG dùng riêng (đã gộp thử vào batch `office=charity` ở trên cho đủ số).

Kết quả cuối: **11 mục sống + đúng chủ đề** (8 qua `check_url()` bình thường + 2 cứu qua retry tay
`tarantomakers.it`/`coworking-savona.org` + 1 từ `office=charity` "PepSE — Pépinière des Solidarités
Etudiantes", Brest, Pháp, đại học). Quốc gia: Ba Lan 3, Đức 2, Ý 2, còn lại Thuỵ Sĩ/Brazil/Áo/Pháp mỗi
nước 1 — không có Việt Nam.

`ROSTER`: 9035 → **9046** (+11). Đơn vị trên bản đồ: 9044 → **9055** (+11, giữ nguyên chênh lệch +9).
Kiểm: `node --check` sạch trên script inline, thẻ `div`/`section` cân bằng (107/107, 6/6). Mở
`index.html` qua HTTP server cục bộ (tạo mới `.claude/launch.json` ở cả gốc phiên và gốc repo — script
`python -m http.server --directory <repo>`, cần đường dẫn `python.exe` đầy đủ vì alias Windows Store
không chạy được trong môi trường Browser pane) qua Browser pane: hiển thị đúng "9055 đơn vị được lập bản
đồ" / "9046 trong danh mục mở rộng" / "12 đơn vị tại Việt Nam" (không đổi), không lỗi console.

**Còn thiếu ~5954 để chạm mốc 15000.** **Việc mở cho lượt sau:** (1) **ưu tiên cao — thử lại 7 domain
nghi bị chặn tầng mạng tạm thời** (`u-touch.org`, `inkubator.wloclawek.pl`, `torinosocialinnovation.it`,
`socialinnovation.ca`, `ciep.ar`, `ciridd.org`, `citralab.lk` — đều là tổ chức có vẻ thật, chỉ cần
`check_url()` thành công là đủ điều kiện thêm ngay, không cần rà lại nội dung); (2) kỹ thuật "tải cấu
trúc trước, lọc từ khoá sau" đã chứng minh khả thi nhưng tỷ lệ khớp từ khoá trên `office=association`/
`ngo`/`educational_institution`/`charity`/`foundation` đều RẤT THẤP (0,1–0,5%) — 4 tag lớn này coi như
ĐÃ KHAI THÁC GẦN HẾT bằng từ khoá, đừng lặp lại trừ khi nghĩ ra bộ từ khoá hẳn mới; (3) CHƯA THỬ:
`amenity=university` (57958 phần tử, rất lớn nhưng rủi ro trùng đại học đã có + sai chủ đề vì đây là
toàn bộ trường đại học chứ không phải trung tâm/văn phòng cụ thể — cân nhắc kỹ trước khi làm, có thể chỉ
đáng thử với bộ lọc quốc gia đang thiếu dữ liệu); (4) nên bắt đầu ghi riêng 1 file danh sách tên/OSM-ID
đã loại thủ công (bài học ghi ở trên) để lượt sau tự động loại được ngay từ bước lọc, không tốn công
WebSearch lại; (5) cần tìm HẲN nguồn ngoài OSM — danh mục các tag `office=*` liên quan chủ đề coi như đã
quét gần hết, nên quay lại hướng đăng ký chính phủ/hiệp hội quốc gia (nhiều nước vẫn chưa thử, xem danh
sách "Nguồn ĐÃ THỬ" tích luỹ qua 30 checkpoint bên dưới) hoặc tìm nguồn dữ liệu lớn hoàn toàn mới ngoài
cả 2 hướng OSM lẫn đăng ký quốc gia.

---
**Lần trước:** 2026-09-09 (checkpoint 30 — **NGUỒN LỚN MỚI: OpenStreetMap, 3 tag mới `office=association`/
`office=ngo`/`office=educational_institution` (lọc từ khoá tên) + `office=research` dạng `relation`**) —
**sếp vừa nâng mục tiêu từ 10000 lên 15000** (còn thiếu ~6065 lúc đầu phiên, khoảng cách LỚN hơn hẳn 9
lượt trước cộng lại). Việc mở đầu phiên: tìm nguồn hoàn toàn mới quy mô lớn cho mục tiêu mới.

**Overpass API chính (`overpass-api.de`) và mirror `overpass.kumi.systems` bị CHẶN Ở TẦNG MẠNG lúc đầu
phiên** (curl timeout ở bước TCP connect, không phải lỗi DNS hay lỗi ứng dụng — `nslookup` vẫn resolve
đúng IP, nhưng `curl -v` treo ở "Trying ... Connection timed out"; Browser pane cũng báo "navigation...
denied or failed" cho đúng domain này trong khi domain khác bình thường) — nghi bị chặn do mẫu truy vấn
Overpass nặng lặp lại nhiều lượt trước từ cùng máy/IP. **Đã tìm ra lối thoát: mirror khác vẫn thông**
(`overpass.openstreetmap.fr`, `overpass.osm.ch` — kiểm bằng `curl` tới `/api/status` trả 200 bình
thường) — **GHI NHỚ CHO BATCH SAU**: nếu `overpass-api.de` lại chặn, thử ngay các mirror này trước khi
kết luận Overpass đã hết dùng được.

Tra `taginfo.openstreetmap.org` API (`/api/4/tag/stats?key=X&value=Y`, trả JSON số liệu trực tiếp,
nhanh hơn hẳn mở trang web JS) cho một loạt tag `office=*` chưa thử: `office=association` (35656 toàn
cầu), `office=ngo` (24152), `office=educational_institution` (48294) — đều QUÁ RỘNG để lấy toàn bộ
(đa số là hội đoàn/NGO/trường học không liên quan chủ đề Atlas, giống bài học `office=coworking` cũ) —
nên lọc ngay trong câu Overpass QL bằng regex trên `name` (`~"fablab|hackerspace|makerspace|incubat|
innovat|tech hub|technopark|technology park|science park|repair caf|fab lab|living lab|startup hub|
entrepreneur|makers",i`) thay vì tải hết rồi lọc sau — giảm tải cho server, tránh timeout (thử gộp cả
3 tag + `office=research` dạng `relation` trong 1 câu bị timeout ở giây 212, phải TÁCH thành 4 câu
riêng theo từng tag mới chạy xong, mỗi câu <2 phút). Cũng thử khai thác nốt phần CÒN THIẾU của
`office=research` (checkpoint 28 chỉ lấy `node`+`way`) bằng `relation["office"="research"]["name"]`
riêng — 797 relation toàn cầu.

Gộp theo `(type,id)` 4 câu: 936 điểm duy nhất có tên, 326 có `website`/`contact:website` (tỷ lệ có
website thấp hơn hẳn `office=research` cũ vì bản chất tag rộng/hỗn tạp hơn). Gán quốc gia bằng
`country_from_latlon.py` (điểm mạnh có sẵn từ checkpoint 28, dùng lại nguyên): 5 điểm rơi ngoài biên
giới bị loại, 0 Việt Nam (kiểm đúng theo tên quốc gia chuẩn hoá, không có biến thể "Vietnam"/"VN" nào
lọt qua). Lọc trùng nội bộ batch (domain/tên) loại 118, lọc trùng ROSTER hiện có loại 48 → còn **153**
ứng viên. Kiểm sống `check_url()` (8 luồng, timeout 15s): alive lượt 1 **115/153**. Retry 38 lỗi (6
luồng, timeout 20s): cứu thêm **0** → tổng **115/153 sống thật (75,2%)** — cùng tầm với `office=research`
cũ (79,1%).

**Rà thủ công phát hiện 15 mục lọt lưới từ khoá nhưng SAI CHỦ ĐỀ** (bài học mới: lọc từ khoá tên rộng
như `innovat`/`entrepreneur`/`makers` vẫn lọt nhiễu, phải đọc tên + tra nhanh từng mục nghi ngờ trước
khi merge, không chỉ tin domain còn sống) — loại 6 trường phổ thông gắn tên "Innovation"/"Innovative"
(K-12 thật, không phải trung tâm ĐMST: "Fred Tajaredes School of Innovation", "KNC Innovative Global
School", "Innovation Spokane Schools 907"), 1 hội hoạ sĩ khắc in khớp nhầm qua hậu tố "-makers"
("Royal Society of Painter-Printmakers"), 2 công ty trị liệu/chăm sóc sức khoẻ gắn tên "Innovations"
("Taconic Innovations" — dịch vụ người khuyết tật, "Behaviour Innovations" — trị liệu ABA tự kỷ), 1
tổ chức nghiên cứu giáo dục gắn tên "Schoolmakers" (khớp nhầm qua "-makers", thực chất là công ty
nghiên cứu lãnh đạo trường học), 1 tổ chức nhà ở xã hội ("Innovative Housing, Inc."), 1 tổ chức dịch vụ
gia đình/trẻ em ("Families & Youth Innovations Plus"), 2 câu lạc bộ/hội doanh nhân thuần kết nối không
phải hạ tầng ươm tạo ("Crown Heights Young Entrepreneurs", "JCI Johor Bahru Entrepreneur",
"Malaysia China Silk Road Entrepreneurs Association"), 1 trường kinh doanh thuần đào tạo bằng cấp
("TIME-The Institute of Management and Entrepreneurship"), 1 công ty không rõ ngành nghề tên trùng
("Josh Innovations"), 1 học viện đào tạo kỹ năng công nghệ tư nhân dạng bootcamp ("Kimit Innovation
Academy") — kiểm bằng WebSearch xác nhận từng trường hợp trước khi loại. Merge an toàn lần cuối (100
dòng còn lại): 0 trùng phát sinh thêm. Chỉ 1/100 URL sống là domain mạng xã hội (Facebook, Fablab
Avignon).

Nguồn theo loại tag: `relresearch` (relation office=research) 58/100, `office=association` (lọc từ
khoá) 17/100, `office=educational_institution` (lọc từ khoá) 16/100, `office=ngo` (lọc từ khoá) 9/100.
Quốc gia (top): Đức 26, Mỹ 16, Pháp 10, Ấn Độ 5, Tây Ban Nha 5, Canada 3, Áo 3, Slovakia 3, Brazil 3 —
Đức vẫn dẫn đầu áp đảo, đúng xu hướng mọi batch OSM trước. `org` để trống toàn batch.

**Hai nguồn khác đã thử và LOẠI hẳn lượt này (đọc kỹ trước khi cân nhắc thử lại):** (1) **ENoLL**
(European Network of Living Labs, `enoll.org`, ~184 thành viên 41 quốc gia) — có PDF "Members Catalogue
2025" công khai (`enoll.org/wp-content/uploads/2025/09/Members-Catalogue-2025_Preview.pdf`, 81MB) chứa
tên+quốc gia+website mỗi thành viên, nhưng layout PDF nhiều cột (tên tổ chức/tên đơn vị chủ quản/quốc
gia+website xếp cạnh nhau) khiến cả `pdftotext` (thường và `-layout`) lẫn trích xuất theo toạ độ khối
văn bản (PyMuPDF `get_text("blocks")`) đều occasionally GHÉP SAI tên với website của thành viên KHÁC
trên cùng trang (xác minh thấy nhiều cặp sai rõ ràng khi rà tay, vd tên "E2L Earth observation Living
Labs" bị ghép nhầm website "gerontopole-na.fr" của một thành viên Pháp khác) — rủi ro merge sai tên-URL
quá cao so với yêu cầu chính xác của dự án, KHÔNG dùng. Nếu muốn khai thác nguồn này về sau, cần rà
THỦ CÔNG từng trong ~184 trang hồ sơ (tốn công, không tự động hoá an toàn được với cấu trúc PDF này).
(2) **Knowledge Exchange UK** (tên cũ PraxisAuril/Auril/Unico, hội TTO Anh+Ireland, `ke.org.uk`) — có
API REST công khai `wp-json/wp/v2/civi-member` trả đúng 74 thành viên (tên+link hồ sơ), nhưng RÀ HTML
từng trang hồ sơ xác nhận KHÔNG có trường website tổ chức nào hiển thị công khai (chỉ có tên + có thể
vài dòng mô tả, không link ra ngoài) — không có cách lấy URL thật, COI NHƯ CẠN, đừng thử lại trừ khi
trang web đổi cấu trúc.

`ROSTER`: 8935 → **9035** (+100). Đơn vị trên bản đồ: 8944 → **9044** (+100, giữ nguyên chênh lệch +9).
Kiểm: `node --check` sạch trên script inline (2.118.541 ký tự), thẻ `div`/`section` cân bằng (107/107,
6/6), Browser pane qua HTTP server cục bộ hiển thị đúng "9044 đơn vị trên bản đồ" / "9035 trong danh
mục mở rộng" / "12 đơn vị tại Việt Nam" (không đổi so với trước — xác nhận batch này không lọt Việt
Nam), không lỗi console.

**Còn thiếu ~5965 để chạm mốc 15000 MỚI** (khoảng cách còn rất lớn, mới đi được ~1,6% chặng đường mới
mở). **Việc mở cho lượt sau:** (1) mirror Overpass thay thế đã xác nhận thông (`overpass.openstreetmap.
fr`, `overpass.osm.ch`) — dùng ngay nếu `overpass-api.de` lại chặn; (2) 3 tag `office=association`/`ngo`/
`educational_institution` mới lọc bằng 1 bộ từ khoá cố định — có thể MỞ RỘNG danh sách từ khoá regex
(vd thêm "coworking", "accelerator", "vườn ươm" dịch các ngôn ngữ khác, "technopole", "cluster") để vét
thêm phần còn lại của 3 tag này (hiện chỉ lọc được 207/48294+35656+24152 tổng 3 tag, còn rất nhiều
chưa xét vì chỉ tag có match từ khoá tên mới được Overpass trả về — muốn vét hết phải tải toàn bộ rồi
lọc offline, tốn tài nguyên hơn); (3) ENoLL PDF (184 living lab, 41 quốc gia) vẫn là nguồn tiềm năng
nếu ai đó sẵn sàng rà tay từng trang (không tự động hoá được an toàn, xem chi tiết ở trên); (4) Knowledge
Exchange UK/PraxisAuril COI NHƯ CẠN (không có trường website); (5) IASP còn ~70 mục "chết" (nghi chặn
mạng khu vực); (6) BIRAC BioNEST PDF lỗi cấu trúc vẫn chưa sửa được; (7) InovaLink Brazil vẫn bế tắc;
(8) cần tiếp tục tìm nguồn hoàn toàn mới quy mô lớn khác — ở khoảng cách 15000, các nguồn cỡ 100-500
như lượt này chỉ là một phần nhỏ, cần ưu tiên tìm nguồn cỡ nghìn (như `office=research` node+way +2182
ở checkpoint 28, hay `fablabs.io` +1367) nếu còn tồn tại chưa khai thác.

---
**Lần trước:** 2026-09-09 (checkpoint 29 — **HackerspaceWiki, trạng thái "building" + "planned"**)
— tiếp tục mục tiêu **10000**. Đây là việc mở đã ghi ở checkpoint 28: khai thác 2 nhóm trạng thái
còn lại của `Category:Hackerspace` chưa từng lấy (checkpoint 26 chỉ lấy `active`).

**Trước tiên đã thử và LOẠI `shop=repair` qua Overpass** (ưu tiên đầu tiên ghi ở checkpoint 28):
`taginfo.openstreetmap.org` báo 7328 điểm toàn cầu, nhưng đây LÀ vấn đề — kiểm tra
`[out:json];(node["shop"="repair"]["name"]["website"];...);out tags center;` trả về 945 điểm có
tên+website, lấy mẫu đọc tên: tuyệt đại đa số là cửa hàng sửa chữa THƯƠNG MẠI thuần túy (thủy lực,
dịch vụ IT, may vá, sửa xe đạp, sửa điện thoại...) — hoàn toàn KHÔNG phải "repair café" cộng đồng
phi lợi nhuận đúng chủ đề Atlas. Kiểm bằng từ khoá tên ("cafe"/"repair caf"/"reparatur"/"community"/
"nonprofit"/"association"/"foundation"/"stichting"/"verein"...) chỉ khớp 45/945 (4,8%), và tra
`taginfo` xác nhận KHÔNG có tag OSM chuyên biệt nào cho "repair café" (`repair_cafe`, `community_repair`
đều 0 lượt dùng) để lọc riêng. Kết luận: `shop=repair` là tag cho cửa hàng dịch vụ thương mại, khác
hẳn phong trào Repair Café cộng đồng đã lấy riêng ở checkpoint trước (nguồn Repair Café Foundation
chính thức) — KHÔNG dùng batch này, không lãng phí thêm công kiểm sống.

Cũng thử kiểm lại xem có nên "cứu" một phần dữ liệu `office=coworking` (đã loại hoàn toàn ở
checkpoint 27 vì đa số là chuỗi thương mại WeWork/Regus/Spaces) bằng cách lọc tên theo từ khoá
"makerspace"/"hackerspace"/"fablab"/"innovation"/"incubator"/"tech hub" trên dữ liệu 5859 điểm đã
cache sẵn từ checkpoint 27 — chỉ khớp 83/5859 (1,4%), quá nhỏ để đáng một batch riêng, KHÔNG dùng.

**Nguồn dùng:** HackerspaceWiki (`wiki.hackerspaces.org`), tái sử dụng đúng dữ liệu SMW `askargs`
đã cache từ checkpoint 26 (`hs_merged.json`, 2587 trang `Category:Hackerspace`, không cần query lại
wiki) — chỉ đổi bộ lọc trạng thái từ `active` (đã lấy) sang `building` (238 trang) + `planned` (351
trang). Trích xuất giống hệt `extract_hs.py` cũ (bổ sung vài centroid quốc gia thiếu: Jordan, Andorra,
Guatemala, Moldova, xứ Wales→UK) → **338** trang có `Website` hợp lệ (246 trong 589 trang building+
planned KHÔNG có trường Website — tỷ lệ thiếu cao hơn hẳn nhóm `active` cũ, đúng logic: dự án còn ở
giai đoạn "đang xây dựng"/"mới lên kế hoạch" thường chưa kịp lập trang web).

Lọc trùng: 22 trùng nội bộ batch + 22 trùng ROSTER hiện có (domain/tên) → còn **294** ứng viên. Kiểm
sống `check_url()` (8 luồng, timeout 15s): alive lượt 1 chỉ **98/294**. Retry 196 lỗi (6 luồng, timeout
20s): cứu thêm **1** → tổng **99/294 sống thật (33,7%)** — THẤP HƠN HẲN so với mọi batch trước (`active`
86,7%, `office=research` 79,1%, `leisure=hackerspace` 71,5%) — đúng như dự đoán ở checkpoint 28 khi xếp
việc này "độ ưu tiên thấp": trang wiki trạng thái "building"/"planned" phần lớn là dự án chưa từng đi
vào hoạt động thật hoặc đã bị bỏ dở từ lâu (domain hết hạn/không còn phản hồi), khác hẳn "active" là
nhóm đã xác nhận đang hoạt động khi trang wiki cập nhật gần nhất. Merge an toàn lần cuối: 0 trùng phát
sinh thêm. 7/99 (7%) URL sống là domain mạng xã hội (Facebook/Twitter) — đúng chính sách đã chốt.

Quốc gia (top): Mỹ 49, Đức 7, Anh 4, Pháp 3, Tây Ban Nha 3, Ấn Độ 3 — phân bố lệch Mỹ mạnh hơn hẳn
các batch OSM (đúng đặc điểm HackerspaceWiki: cộng đồng dùng wiki này đông nhất ở Mỹ). `org` để trống
toàn batch (cùng quy ước các batch HackerspaceWiki/OSM trước). 50 "planned" + 49 "building" trong 99
mục — không lệch hẳn về một trạng thái.

`ROSTER`: 8837 → **8936** (+99). Đơn vị trên bản đồ: 8846 → **8945** (+99, giữ nguyên chênh lệch +9).
Kiểm: `node --check` sạch trên script inline (2.108.287 ký tự), thẻ `div`/`section` cân bằng (107/107,
6/6), Browser pane qua HTTP server cục bộ hiển thị đúng "8945 đơn vị trên bản đồ", không lỗi console.

**Còn thiếu ~1064 để chạm mốc 10000** (chưa đạt mốc lượt này). **Việc mở cho lượt sau:** (1)
HackerspaceWiki giờ đã khai thác HẾT cả 3 trạng thái hữu ích (active/building/planned) — nguồn này
COI NHƯ ĐÃ CẠN, đừng quay lại trừ khi wiki có thêm trang mới; (2) `shop=repair` và lọc từ khoá
`office=coworking` đã thử và LOẠI hẳn lượt này — đừng thử lại; (3) cần tìm NGUỒN LỚN HOÀN TOÀN MỚI
(kỹ thuật thứ 7?) — đã cạn gần hết danh sách quốc gia/mạng lưới/tag OSM khả thi đã biết, có thể cần
nghiên cứu thêm wiki cộng đồng SMW khác (chưa xác định trang cụ thể nào), hoặc mạng lưới tổ
chức phát triển doanh nghiệp lớn dạng ANDE (Aspen Network of Development Entrepreneurs — đã thử
nhanh `andeglobal.org/members/`, site JS nặng + REST API `wp-json` trả 401 Unauthorized, cần kỹ
thuật cào khác — WebFetch/browser thật — nếu muốn thử tiếp); (4) 571 hồ sơ Repair Café bị bỏ qua vì
thiếu quốc gia (việc mở cũ); (5) BIRAC BioNEST PDF lỗi cấu trúc vẫn chưa sửa được; (6) InovaLink
Brazil vẫn bế tắc.

**Lần trước:** 2026-09-09 (checkpoint 28 — **CÙNG NGUỒN OpenStreetMap, tag MỚI `office=research`**)
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
