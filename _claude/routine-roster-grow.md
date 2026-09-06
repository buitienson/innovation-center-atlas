# Routine tự động: mở rộng ROSTER bằng Gemini (Google Search grounding)

> File này là **nguồn canonical** cho routine mở rộng danh mục mở rộng
> (`ROSTER` trong `src/atlas.html`) — chạy như một **cloud routine theo lịch**
> (agent chỉ clone repo này, bắt đầu từ con số 0, phải tự đọc hết file này).
> Đây là routine **tách riêng** khỏi `_claude/routine-tin-tuc.md` (Tin tức +
> Fund/Hackathon) — uỷ quyền tự động `git push` ở routine đó KHÔNG áp dụng
> cho routine này; routine này có uỷ quyền riêng, xác nhận ngày 2026-09-06
> (xem `CLAUDE.md` mục "Lần cuối").

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
riêng `_claude/tools/roster_grow_worker.py`, có bật **Google Search grounding**
của Gemini API để Gemini thực sự tìm trên web, cộng thêm một lớp kiểm tra sống
từng URL bằng HTTP trước khi tin.

## Việc cần làm mỗi lượt chạy

1. **Đọc `_claude/roster-grow-queue.md`** — tìm mục `[pending]` **đầu tiên**
   theo thứ tự từ trên xuống. Không còn mục `[pending]` nào → dừng ở đây,
   không sửa gì, không commit gì cả (kết quả bình thường, không phải lỗi).
2. **Chạy worker** cho đúng mục đó:
   ```bash
   export GEMINI_API_KEY="<lấy từ biến môi trường routine, không bao giờ ghi ra file>"
   python3 _claude/tools/roster_grow_worker.py \
     --queue-item "<nguyên văn mô tả mục pending>" \
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
7. **Cập nhật `CLAUDE.md` mục "Lần cuối"** trong cùng commit — ghi đè, không
   nối — nêu mục vừa xử lý + số lượng thêm được, ghi rõ đây là lượt chạy tự
   động kèm ngày giờ chạy.

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
