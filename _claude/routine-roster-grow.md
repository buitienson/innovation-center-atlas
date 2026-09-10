# Routine tự động: mở rộng ROSTER bằng Gemini (`url_context`)

> File này là **nguồn canonical** cho routine mở rộng danh mục mở rộng
> (`ROSTER` trong `src/atlas.html`) — chạy như một **cloud routine theo lịch**
> (agent chỉ clone repo này, bắt đầu từ con số 0, phải tự đọc hết file này).
> Đây là routine **tách riêng** khỏi `_claude/routine-tin-tuc.md` (Tin tức +
> Fund/Hackathon) — uỷ quyền tự động `git push` ở routine đó KHÔNG áp dụng
> cho routine này; routine này có uỷ quyền riêng, xác nhận ngày 2026-09-06
> (xem `CLAUDE.md` mục "## Lịch sử tăng trưởng ROSTER").

> ⚠️ **CHƯA TẠO CLOUD ROUTINE.** Cơ chế đã kiểm chứng hoạt động đúng (xem
> "Tình trạng hiện tại"), nhưng hàng đợi (`roster-grow-queue.md`) mới có mô tả
> nguồn dạng văn bản, chưa có URL cụ thể cho từng mục — cần bổ sung URL nguồn
> trước khi chạy tự động hằng ngày (xem việc cần làm tiếp ở cuối mục này).

## Tình trạng hiện tại (2026-09-07) — đã tìm ra cách dùng Gemini KHÔNG cần billing

**Lịch sử ngắn gọn (chi tiết đầy đủ ở lịch sử git của file này):** bản đầu
dùng công cụ Google Search grounding (`tools:[{"google_search":{}}]`) —
kiểm tra tay phát hiện key/project hiện có bị **429 RESOURCE_EXHAUSTED ngay
lập tức** trên tính năng này (trong khi gọi Gemini bình thường vẫn chạy tốt),
khả năng do Google cắt hạn mức miễn phí 50-80% từ 12/2025 và/hoặc cần bật
billing mới có hạn mức grounding. Bật billing sẽ xoá hạn mức miễn phí khác
của project nên không muốn làm ngay.

**Tìm ra hướng khác, đã kiểm chứng hoạt động đúng:** Gemini có công cụ riêng
**`url_context`** (`tools:[{"url_context":{}}]`) — cho Gemini đọc trực tiếp
MỘT (hoặc vài) URL cụ thể được giao sẵn, khác với `google_search` (tự tìm
kiếm mở). Test tay nhiều lần: `url_context` **không hề bị 429** trên cùng
key — quota hoàn toàn riêng, còn dùng được ngay, không cần billing.

Đánh đổi: `url_context` cần được GIAO SẴN URL nguồn cụ thể (không tự tìm kiếm
mở như `google_search`) — nên hàng đợi (`roster-grow-queue.md`) cần có URL
nguồn thật cho mỗi mục, không chỉ mô tả bằng lời như bản đầu.

**Đã test end-to-end thật với nguồn Malaysia** (`itma.my/tech-transfer-in-
malaysia/`, một trang liệt kê TTO các đại học Malaysia không kèm link riêng
từng đơn vị): Gemini đọc trang, tự nhận diện ~22-23 tổ chức, và vì trang gốc
không có link riêng nên phải **ước lượng URL** dựa trên tên viện/trường —
khoảng 40-50% ước lượng đúng (vd `icc.utm.my`, `umcie.um.edu.my` — đúng),
40-50% sai (vd `psp.upm.edu.my`, `cic.usm.my` — tên miền không tồn tại, DNS
lỗi). **Bước kiểm tra sống bằng HTTP thật của `roster_grow_worker.py` bắt
đúng và loại sạch mọi URL sai** — không có mục nào lọt qua với URL không tồn
tại. Đây chính là lưới an toàn hoạt động đúng như thiết kế, không phải lỗi:
tỷ lệ giữ lại mỗi lượt chạy sẽ thấp hơn số Gemini đề xuất, nhưng mọi mục giữ
lại đều đã xác minh sống thật.

Đã cập nhật `roster_grow_worker.py`: dùng `url_context` thay `google_search`,
cho phép Gemini ước lượng URL khi trang nguồn không có link riêng (không còn
bắt buộc để trống), vẫn giữ nguyên lưới an toàn liveness-check + dedup +
giới hạn 15 mục/lượt. Script tự chẩn đoán khi gặp lỗi hạn mức (429/503): thử
thêm 1 lệnh gọi không kèm tool để phân biệt "chỉ `url_context` bị chặn" với
"cả key hết hạn mức".

**Cập nhật 2026-09-08 (lượt sau) — false-positive thứ 4, vá trong
`roster_grow_worker.py` (không phải `roster_common.py`):** khi trang nguồn
liệt kê nhiều tổ chức nhưng KHÔNG có link riêng cho từng tổ chức (thử với
`sentraki.dgip.go.id/kampus` và `enterprisesg.gov.sg/.../coi-directory`),
Gemini không phải lúc nào cũng "ước lượng URL hợp lý" như system instruction
yêu cầu — nhiều lần nó điền thẳng URL = CHÍNH trang nguồn đã giao. Trang
nguồn luôn "sống" nên lọt qua `check_url()` (hàm đó không biết gì về nguồn,
chỉ kiểm sống/parking/redirect). Đã vá bằng một điều kiện hẹp trong
`roster_grow_worker.py`: so `domain_of(candidate.url)` với domain của từng
`--source-urls` đã giao, loại nếu trùng. **Hệ quả cho việc chọn nguồn:** nguồn
kiểu trang danh bạ CÓ SẴN link riêng từng tổ chức trong HTML (kiểu `itma.my`
— dù không link cũng còn được vì Gemini ước lượng domain từ tên) vẫn dùng
tốt; nguồn kiểu bảng/thẻ không có `<a href>` riêng (site chính phủ dùng JS
render bảng) có tỷ lệ giữ lại rất thấp hoặc bằng 0 với cách làm hiện tại —
cân nhắc nguồn khác hoặc chấp nhận tỷ lệ giữ lại thấp.

### Việc cần làm tiếp trước khi tạo cloud routine

1. Bổ sung URL nguồn thật cho các mục trong `roster-grow-queue.md` (hiện chỉ
   có mô tả bằng lời) — mỗi mục cần 1-3 URL cụ thể (trang danh bạ hiệp hội,
   trang Wikipedia liệt kê, trang chính phủ...). Có thể làm dần, không cần
   xong hết mới bắt đầu chạy — routine chỉ cần URL cho mục `[pending]` kế
   tiếp tại thời điểm chạy.
2. Chạy tay thêm vài lượt để có cảm giác về tỷ lệ giữ lại thực tế trước khi
   để chạy tự động không giám sát hằng ngày.
3. Tạo cloud routine (skill `schedule`) khi đã sẵn sàng — nhập `GEMINI_API_KEY`
   vào ô secret lúc tạo.

## Bối cảnh

`ROSTER` (~786 mục tính đến 2026-09-06) là danh mục các trung tâm CGCN/ĐMST
đại học trên thế giới, tự thu thập từ nguồn công khai — **không phải một cuộc
điều tra đầy đủ**. Một số khu vực (Đông Nam Á, Châu Phi, Trung Đông, Trung Á)
rất mỏng so với thực tế. Mục tiêu routine này: mở rộng dần, có kiểm soát, ưu
tiên chi phí thấp — chạy trên hạn mức miễn phí của Gemini (không tốn token
Claude cho việc tìm kiếm hàng loạt), **dừng khi hết hạn mức ngày đó**, và
**không bao giờ thêm một mục không có nguồn thật**.

**Vì sao không dùng skill `gemini-delegate` dùng chung ở Brain:** script của
skill đó (`gemini_worker.py`) gọi Gemini kiểu text-in/text-out thuần tuý,
không có khả năng duyệt web — dùng cho việc "tìm tổ chức có thật" sẽ khiến
Gemini bịa tên/URL nghe hợp lý từ dữ liệu huấn luyện. Routine này dùng script
riêng `_claude/tools/roster_grow_worker.py`, dùng công cụ **`url_context`**
của Gemini API để Gemini đọc thật các trang nguồn được giao sẵn, cộng thêm
một lớp kiểm tra sống từng URL bằng HTTP trước khi tin (bắt buộc, vì Gemini
có thể ước lượng sai URL của tổ chức khi trang nguồn không có link riêng).

## Việc cần làm mỗi lượt chạy

1. **Đọc `_claude/roster-grow-queue.md`** — tìm mục `[pending]` **đầu tiên**
   theo thứ tự từ trên xuống, lấy cả mô tả lẫn URL nguồn đã gán cho mục đó.
   Không còn mục `[pending]` nào, hoặc mục kế tiếp chưa có URL nguồn → dừng ở
   đây, không sửa gì, không commit gì cả (kết quả bình thường, không phải lỗi).
2. **Chạy worker** cho đúng mục đó:
   ```bash
   export GEMINI_API_KEY="<lấy từ biến môi trường routine, không bao giờ ghi ra file>"
   python3 _claude/tools/roster_grow_worker.py \
     --queue-item "<mô tả ngắn mục pending, để ghi log>" \
     --source-urls "<URL nguồn 1>" "<URL nguồn 2 nếu có>" \
     --roster-html src/atlas.html \
     --output /tmp/roster-candidates.json \
     --max-new 15
   ```
   - **Exit code 2** (hết hạn mức Gemini cả 3 model) → dừng ở đây, không sửa
     gì, không commit gì. Bình thường, thử lại vào lượt chạy sau (ngày mai).
     KHÔNG lùi lại đánh dấu mục pending là lỗi — mục đó vẫn giữ nguyên
     `[pending]` để lượt chạy kế tiếp thử lại từ đầu.
   - **Exit code 1** (lỗi thật — sai tham số, JSON không parse được sau khi
     đã thử) → dừng, không sửa gì, không commit gì. Đây là trường hợp đáng
     xem lại thủ công (không tự sửa code, không tự đoán cách khắc phục).
   - **Exit code 0** → đọc `/tmp/roster-candidates.json`. Có thể là mảng rỗng
     (Gemini không tìm ra tổ chức nào đạt tiêu chuẩn cho nguồn đó) — vẫn hợp
     lệ, đánh dấu mục đó `[done]` với số mục thêm = 0, không cần thêm gì vào
     `ROSTER`.
3. **Merge kết quả vào `ROSTER`** (nếu có): với mỗi phần tử trong
   `candidates.json`, chèn một dòng mới vào cuối mảng `ROSTER` trong
   `src/atlas.html`, theo đúng khuôn 6 trường hiện có:
   ```js
   ["<name>","<host>","<country>","<url>",<lat>,<lng>]
   ```
   - `host` rỗng (`""`) nếu tổ chức độc lập, không thuộc một trường cụ thể.
   - `lat`/`lng` lấy nguyên từ candidate (Gemini tự ước lượng toạ độ thành
     phố — chỉ để định vị gần đúng trên bản đồ, không phải claim cần chính
     xác tuyệt đối, đúng tinh thần `rosterCaveat` đã có trên trang).
   - Field `grounded` và `source_queue_item` trong candidate là thông tin nội
     bộ cho worker/routine — **không đưa vào `ROSTER`** (schema `ROSTER` chỉ
     có đúng 6 trường như trên).
   - Giữ nguyên toàn bộ mục cũ trong `ROSTER` — mảng chỉ lớn dần.
4. **Cập nhật `_claude/roster-grow-queue.md`**: đổi `[pending]` thành `[done]`
   cho mục vừa xử lý, điền "Ngày xử lý" (ngày chạy routine, dùng lệnh `date`)
   và "Số mục thêm" (số phần tử đã merge ở bước 3, kể cả 0).
5. **Build + kiểm** — đúng quy trình ở `CLAUDE.md` mục "Quy trình sửa":
   - `python3 build.py`
   - kiểm `node --check` trên script inline (>10000 ký tự) + đếm cân bằng thẻ
     div/section trước khi commit.
6. **Commit + push thẳng lên `main`** (uỷ quyền riêng cho routine này, xác
   nhận 2026-09-06 — không cần hỏi lại mỗi lượt). Message dạng:
   `Grow roster: <mô tả ngắn mục vừa xử lý> (+N mục, routine tự động, YYYY-MM-DD)`.
7. **Cập nhật `CLAUDE.md` mục "## Lịch sử tăng trưởng ROSTER"** trong cùng
   commit — **NỐI TIẾP, KHÔNG BAO GIỜ ghi đè/xoá**: đổi khối "**Lần cuối:**"
   hiện có (checkpoint N) thành "**Lần trước:**" (giữ nguyên nội dung), rồi
   thêm khối "**Lần cuối:**" MỚI (checkpoint N+1) lên đầu, nêu mục vừa xử lý +
   số lượng thêm được, ghi rõ đây là lượt chạy tự động kèm ngày giờ chạy. Đây
   là lịch sử tích luỹ qua hàng chục checkpoint (nguồn đã thử/loại) — xoá mất
   là mất công sức nhiều phiên, không phải chỉ 1 dòng trạng thái.

   **CẢNH BÁO — sự cố thật đã xảy ra 2026-09-10 do đúng câu chữ "ghi đè, không
   nối" từng viết ở đây (đã sửa lại như trên):** `CLAUDE.md` còn 1 mục KHÁC,
   RIÊNG BIỆT, tên "## Routine tin tức / fund-hackathon — trạng thái lần chạy
   gần nhất" (của `_claude/routine-tin-tuc.md`) — mục đó MỚI thực sự dùng quy
   ước ghi đè. Cả 2 mục đều có dòng bắt đầu bằng "**Lần cuối:**" — một agent
   chạy routine tin tức từng match nhầm dòng "Lần cuối" của MỤC NÀY (ROSTER)
   rồi ghi đè mất hơn 3000 dòng lịch sử 47 checkpoint, phải khôi phục từ git.
   **Khi sửa mục này, chỉ động vào nội dung bên trong heading "## Lịch sử
   tăng trưởng ROSTER" — tuyệt đối không chạm mục tin tức phía trên nó.**

## Ràng buộc nội dung — nhắc lại, áp dụng nghiêm ngặt hơn routine tin tức

- **Không bao giờ thêm một mục không qua được kiểm tra URL sống** của worker
  (worker đã tự làm việc này — routine không tự ý bỏ qua bước này hay tự thêm
  tay một mục worker đã loại).
- Không tự sửa `roster_grow_worker.py` để "linh hoạt hơn" khi gặp lỗi — báo
  dừng đúng như worker chỉ định (xem exit code ở bước 2).
- Không publish lại Artifact claude.ai trong routine tự động này (giống
  routine tin tức) — chỉ cần GitHub Pages (qua `index.html`) là "live".
- Mỗi lượt chạy **chỉ xử lý đúng 1 mục hàng đợi** — không tự ý gộp nhiều mục
  một lượt dù còn thời gian/hạn mức, để mỗi commit nhỏ, dễ soát lại nếu cần.

## Theo dõi chi phí

`roster_grow_worker.py` tự ghi token mỗi lần gọi vào
`_claude/tools/usage.log` (cạnh script, không commit lên git — thêm vào
`.gitignore` nếu chưa có).

---
**Vị trí canonical:** `Innovation-Center-Atlas/_claude/routine-roster-grow.md`.
Sửa tại đây. Hàng đợi nguồn ở `_claude/roster-grow-queue.md`, script ở
`_claude/tools/roster_grow_worker.py`.
