# Routine tự động: thêm tin ĐMST cho Innovation Center Atlas

> File này là **nguồn canonical** cho việc tự động tìm & thêm tin — cả khi chạy
> local (skill `atlas-tin-tuc` trên máy Sơn) lẫn khi chạy như một **cloud
> routine theo lịch** (agent chỉ clone repo này, không có gì khác — bắt đầu từ
> con số 0, phải tự đọc hết file này để biết làm gì).

## Bối cảnh (agent chưa biết gì thì đọc đoạn này trước)

Đây là repo của trang tham khảo cá nhân **Innovation Center Atlas**
(`github.com/buitienson/innovation-center-atlas`), deploy qua GitHub Pages ở
nhánh `main`. Cấu trúc:

- `src/atlas.html` — file nguồn để sửa (fragment HTML/CSS/JS gộp).
- `build.py` — bọc `src/atlas.html` thành `index.html` (bản deploy, generated,
  KHÔNG sửa tay file này).
- `CLAUDE.md` — mô tả đầy đủ dự án + quy trình sửa + ranh giới nội dung.

**Đọc `CLAUDE.md` trong repo này trước** để hiểu quy trình build/publish và các
ràng buộc nội dung chung của trang, rồi mới làm các bước dưới.

## Việc cần làm

Mục tiêu: tìm tin đổi mới sáng tạo/KHCN có thật, gần đây, thêm vào mảng `NEWS`
trong `src/atlas.html`, rồi build + commit + push lên live. Đây là **routine tự
động, không có ai xác nhận từng bước** — ưu tiên an toàn hơn đầy đủ: không có
tin đủ tin cậy thì bỏ qua lượt chạy, đừng cố nhét tin yếu cho đủ số lượng.

1. **Đọc mảng `NEWS` hiện có** trong `src/atlas.html` (tìm `var NEWS = [`) —
   biết đã có tin nào rồi (tránh trùng, dù diễn đạt khác), tin mới nhất đang
   dừng ở ngày nào.
2. **Tìm tin ĐMST/KHCN có thật, gần đây** (ưu tiên trong ~7-14 ngày gần nhất
   tính từ hôm nay — dùng lệnh `date` để biết chính xác hôm nay là ngày nào,
   đừng suy đoán từ ngày huấn luyện) — cả trong nước lẫn quốc tế:
   - VN: báo chính thống (Nhân Dân, Chính phủ, TTXVN, Tiền Phong/Sinh Viên Việt
     Nam, Giáo dục & Thời đại, VnExpress...).
   - Quốc tế: trang tin chính chủ của đại học/viện (university/enterprise
     innovation office, MIT News...) hoặc báo lớn (TIME, Reuters, TechCrunch,
     Nikkei...).
   - **Mỗi tin phải có link nguồn thật** (dùng WebSearch/WebFetch để xác minh
     link còn sống và đúng nội dung) — không bịa link, không bịa số liệu,
     không suy diễn thêm chi tiết ngoài bài gốc.
3. **Chọn tối đa ~3 tin mỗi lượt chạy** (chạy hàng ngày, không cần nhồi nhiều),
   ưu tiên tin có ý nghĩa với ĐMST đại học/trung tâm nghiên cứu, bỏ tin PR
   thuần tuý không nội dung thật.
   - **Không có tin nào đủ tin cậy/đủ mới hôm nay → dừng ở đây, không sửa gì,
     không commit gì cả.** Đây là kết quả bình thường, không phải lỗi.
4. **Viết mỗi tin đúng khuôn** (khớp các item đã có trong `NEWS`):
   ```js
   {date:'YYYY-MM-DD', source:'Tên nguồn', url:'link bài gốc',
     title:{vi:'...', en:'...'},
     summary:{vi:'1-2 câu, có số liệu/mốc cụ thể nếu bài gốc có', en:'...'}}
   ```
   - `date` = ngày đăng bài gốc, không phải ngày routine chạy.
   - `title` và `summary` phải có cả `vi` lẫn `en`, dịch sát nghĩa.
   - Không cần chèn đúng thứ tự ngày — trang tự sort giảm dần khi render.
5. **Chèn phần tử mới vào mảng `NEWS`** (giữ nguyên toàn bộ tin cũ — mảng chỉ
   lớn dần theo thời gian).
6. **Build + kiểm** — đúng quy trình ở `CLAUDE.md` mục "Quy trình sửa":
   - `python3 build.py`
   - kiểm `node --check` trên script inline (>10000 ký tự) + đếm cân bằng thẻ
     div/section trước khi commit.
7. **Commit + push thẳng lên `main`** (đã được chủ dự án xác nhận trước khi
   dựng routine này — 2026-09-05 — không cần hỏi lại mỗi lượt). Message dạng:
   `Add N tin ĐMST (routine tự động, YYYY-MM-DD)`.
8. **Cập nhật `CLAUDE.md` mục "Lần cuối"** trong cùng commit — ghi đè, không
   nối — liệt kê tiêu đề các tin vừa thêm, ghi rõ đây là lượt chạy tự động kèm
   ngày giờ chạy.

## Ràng buộc nội dung — nhắc lại từ `CLAUDE.md`

- Không bịa tin, không bịa link, không bịa số liệu.
- Không đưa bình luận về quy trình/độ tin cậy lên trang công khai (không viết
  "chưa xác minh", "kết quả tìm kiếm diện rộng" vào `title`/`summary` hiển thị
  cho người đọc).
- Việc pre-authorize `git push` thẳng lên `main` **CHỈ áp dụng cho đúng việc
  thêm tin theo khuôn ở trên** (sửa mảng `NEWS` + dòng "Lần cuối" trong
  `CLAUDE.md`). Bất kỳ thay đổi nào khác (sửa `src/atlas.html` ngoài mảng
  `NEWS`, sửa `build.py`, xoá tin cũ...) thì KHÔNG tự ý làm.
- Không publish lại Artifact claude.ai trong routine tự động này (Artifact là
  bản xem/sửa nhanh, chủ dự án tự đồng bộ tay khi cần) — chỉ cần GitHub Pages
  (qua `index.html`) là "live" đối với routine này.

---
**Vị trí canonical:** `Innovation-Center-Atlas/_claude/routine-tin-tuc.md` (nằm
trong chính repo, để cloud routine clone về là đọc được ngay). Sửa tại đây.
