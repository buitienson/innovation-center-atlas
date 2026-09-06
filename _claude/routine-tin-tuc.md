# Routine tự động: thêm tin + nguồn tài trợ/cuộc thi ĐMST cho Innovation Center Atlas

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

Mục tiêu: mỗi lượt chạy làm **hai việc độc lập** trên `src/atlas.html`, rồi
build + commit + push chung một lượt lên live:

- **(A) Tin tức** — tìm tin đổi mới sáng tạo/KHCN có thật, gần đây, thêm vào
  mảng `NEWS`.
- **(B) Fund/Hackathon** — tìm cơ hội tài trợ/cuộc thi/hackathon/thông báo đề
  xuất nhiệm vụ KHCN&ĐMST **đang mở** (hạn nộp còn ở tương lai, hoặc chưa công
  bố hạn), thêm vào mảng `FUNDING`.

Đây là **routine tự động, không có ai xác nhận từng bước** — ưu tiên an toàn
hơn đầy đủ: không có tin/cơ hội nào đủ tin cậy thì bỏ qua phần đó (hoặc bỏ qua
cả lượt chạy), đừng cố nhét nội dung yếu cho đủ số lượng. Hai việc A và B độc
lập nhau — có thể một lượt chạy chỉ thêm tin mà không thêm cơ hội tài trợ nào,
hoặc ngược lại, hoặc cả hai, hoặc không thêm gì cả.

### Phần A — Tin tức (mảng `NEWS`)

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
   - **Không có tin nào đủ tin cậy/đủ mới hôm nay → bỏ qua Phần A**, chuyển
     sang Phần B. Đây là kết quả bình thường, không phải lỗi.
4. **Viết mỗi tin đúng khuôn** (khớp các item đã có trong `NEWS`):
   ```js
   {date:'YYYY-MM-DD', source:'Tên nguồn', url:'link bài gốc', image:'link ảnh og:image (nếu có)',
     title:{vi:'...', en:'...'},
     summary:{vi:'1-2 câu, có số liệu/mốc cụ thể nếu bài gốc có', en:'...'}}
   ```
   - `date` = ngày đăng bài gốc, không phải ngày routine chạy.
   - `title` và `summary` phải có cả `vi` lẫn `en`, dịch sát nghĩa.
   - `image`: lấy thẻ `<meta property="og:image">` (hoặc `twitter:image`) của chính
     bài gốc (`curl -sL --compressed -A "Mozilla/5.0 ..." <url> | grep -o '<meta[^>]*og:image[^>]*>'`
     là cách nhanh nhất). Đây là ảnh do chính trang nguồn công bố để người khác
     dẫn lại — không phải ảnh tự ý lấy. **Không thấy og:image thật thì bỏ trống
     field này, đừng chèn ảnh khác/ảnh đại diện chung.** URL ảnh có ký tự `&`
     thì giữ nguyên trong chuỗi JS bình thường — hàm render tự escape khi ghép
     HTML, không cần escape tay.
   - Không cần chèn đúng thứ tự ngày — trang tự sort giảm dần khi render.
5. **Chèn phần tử mới vào mảng `NEWS`** (giữ nguyên toàn bộ tin cũ — mảng chỉ
   lớn dần theo thời gian).

### Phần B — Fund/Hackathon (mảng `FUNDING`)

6. **Đọc mảng `FUNDING` hiện có** trong `src/atlas.html` (tìm `var FUNDING = [`)
   — biết đã có mục nào rồi (so theo `url`/`id`, không thêm trùng một thông báo
   đã có dù diễn đạt khác).
7. **Tìm cơ hội tài trợ/cuộc thi/hackathon/đề xuất nhiệm vụ KHCN&ĐMST đang mở**
   hoặc mới công bố — **ưu tiên rõ rệt cho Việt Nam trước, quốc tế sau**:
   - Việt Nam, cấp Nhà nước/Bộ/Ngành/Tỉnh/Thành (ưu tiên cao nhất): cổng thông
     tin điện tử Bộ Khoa học và Công nghệ (mst.gov.vn — hoặc tên bộ mới nếu đã
     đổi), NAFOSTED (nafosted.gov.vn), Quỹ Đổi mới công nghệ quốc gia (NATIF),
     Sở KH&CN các tỉnh/thành lớn (Hà Nội, TP.HCM, Đà Nẵng...) — tìm thông báo
     tuyển chọn/đặt hàng/tài trợ nhiệm vụ KHCN&ĐMST.
   - Việt Nam, cuộc thi/hackathon khởi nghiệp ĐMST: Techfest, các cuộc thi cấp
     trường/thành phố, SIHUB, các chương trình của Bộ GD&ĐT...
   - Quốc tế: một số ít cơ hội lớn, có mở cho Việt Nam tham gia hoặc liên quan
     ĐMST đại học (MIT Solve, VinFuture, các hackathon/competition có deadline
     rõ ràng...).
   - **Mỗi mục phải có link nguồn thật** (WebSearch/WebFetch xác minh còn sống)
     — không bịa link. **Không xác minh được hạn nộp chính xác thì để
     `deadline: null`** (trang tự hiện "xem hạn tại trang chính thức") — tuyệt
     đối không đoán/bịa một ngày cụ thể.
   - Chỉ thêm mục còn actionable: hạn nộp chưa qua (so với ngày chạy routine,
     dùng lệnh `date`), hoặc chưa công bố hạn nhưng thông báo còn hiệu lực. Mục
     đã đóng hạn từ trước thì bỏ qua, không thêm vào (khác với tin tức — mảng
     `FUNDING` này chỉ để hiển thị cơ hội **đang mở**, mục đã đóng để lâu chỉ
     làm loãng danh sách).
8. **Chọn tối đa ~2-3 mục mỗi lượt chạy**, ưu tiên mục có ý nghĩa với ĐMST đại
   học/nghiên cứu.
   - **Không tìm được mục nào đủ tin cậy/còn mở hôm nay → bỏ qua Phần B**, đây
     là kết quả bình thường, không phải lỗi. Phần lớn các lượt chạy dự kiến sẽ
     không thêm gì ở Phần B vì thông báo loại này ra không thường xuyên như tin
     tức — đừng cố nhét cho đủ số lượng.
9. **Viết mỗi mục đúng khuôn** (khớp các item đã có trong `FUNDING`):
   ```js
   {id:'slug-duy-nhat', type:'hackathon'|'competition'|'fund'|'rfp', deadline:'YYYY-MM-DD'|null,
     title:{vi:'...', en:'...'},
     org:{vi:'...', en:'...'},
     theme:{vi:'...', en:'...'},           // tuỳ chọn — bỏ field nếu không rõ
     location:{vi:'...', en:'...'},        // tuỳ chọn
     prize:{vi:'...', en:'...'},           // tuỳ chọn — giá trị tài trợ/giải thưởng
     note:{vi:'...', en:'...'},            // tuỳ chọn — sự thật khách quan bổ sung
     url:'link trang chính thức/thông báo gốc'}
   ```
   - `type`: `hackathon` (hackathon), `competition` (cuộc thi khởi nghiệp),
     `fund` (quỹ tài trợ), `rfp` (đề xuất/đặt hàng/tuyển chọn nhiệm vụ KHCN&ĐMST).
   - `id`: slug ngắn, duy nhất trong mảng, không dấu, dùng `-` nối từ.
   - Field nào không xác minh được thì **bỏ hẳn field đó** (đừng để chuỗi rỗng
     hay đoán đại) — hàm render đã tự bỏ qua field thiếu.
10. **Chèn phần tử mới vào mảng `FUNDING`** (giữ nguyên toàn bộ mục cũ).

### Chung — build, commit, push

11. **Build + kiểm** — đúng quy trình ở `CLAUDE.md` mục "Quy trình sửa":
    - `python3 build.py`
    - kiểm `node --check` trên script inline (>10000 ký tự) + đếm cân bằng thẻ
      div/section trước khi commit.
    - **Nếu cả Phần A lẫn Phần B đều không có gì để thêm → dừng ở đây, không
      sửa gì, không commit gì cả.**
12. **Commit + push thẳng lên `main`** (đã được chủ dự án xác nhận trước khi
    dựng routine này — 2026-09-05, mở rộng sang Phần B ngày 2026-09-06 — không
    cần hỏi lại mỗi lượt). Message dạng:
    `Add N tin + M cơ hội tài trợ/ĐMST (routine tự động, YYYY-MM-DD)` (bỏ phần
    nào bằng 0 khỏi message).
13. **Cập nhật `CLAUDE.md` mục "Lần cuối"** trong cùng commit — ghi đè, không
    nối — liệt kê tiêu đề các tin/mục vừa thêm ở cả hai phần (phần nào không có
    gì thì không cần nhắc), ghi rõ đây là lượt chạy tự động kèm ngày giờ chạy.

## Ràng buộc nội dung — nhắc lại từ `CLAUDE.md`

- Không bịa tin, không bịa link, không bịa số liệu, **không bịa hạn nộp** —
  không xác minh được hạn của một cơ hội tài trợ/cuộc thi thì để `deadline:
  null`, đừng đoán một ngày "nghe hợp lý".
- Không đưa bình luận về quy trình/độ tin cậy lên trang công khai (không viết
  "chưa xác minh", "kết quả tìm kiếm diện rộng" vào `title`/`summary`/`note`
  hiển thị cho người đọc).
- Việc pre-authorize `git push` thẳng lên `main` **CHỈ áp dụng cho đúng việc
  thêm tin/cơ hội theo khuôn ở trên** (sửa mảng `NEWS` và/hoặc mảng `FUNDING`
  + dòng "Lần cuối" trong `CLAUDE.md`). Bất kỳ thay đổi nào khác (sửa
  `src/atlas.html` ngoài hai mảng đó, sửa `build.py`, xoá mục cũ trong `NEWS`
  hay `FUNDING`...) thì KHÔNG tự ý làm.
- Không publish lại Artifact claude.ai trong routine tự động này (Artifact là
  bản xem/sửa nhanh, chủ dự án tự đồng bộ tay khi cần) — chỉ cần GitHub Pages
  (qua `index.html`) là "live" đối với routine này.

---
**Vị trí canonical:** `Innovation-Center-Atlas/_claude/routine-tin-tuc.md` (nằm
trong chính repo, để cloud routine clone về là đọc được ngay). Sửa tại đây.
