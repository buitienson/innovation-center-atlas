# Hàng đợi nguồn — routine mở rộng ROSTER

> Canonical cho routine `_claude/routine-roster-grow.md`. Mỗi lượt chạy xử lý
> **đúng 1 mục** còn `[pending]` (theo thứ tự từ trên xuống), gọi
> `roster_grow_worker.py --queue-item "<mô tả mục>"`, merge kết quả đã qua kiểm
> vào `ROSTER`, rồi đánh dấu mục đó `[done]` kèm ngày + số mục thêm được ngay
> tại dòng đó (ghi đè, không xoá mục cũ — giữ lại làm nhật ký tiến độ).
>
> Hết hàng đợi (không còn mục `[pending]`) → hôm đó không làm gì, không phải
> lỗi. Sếp bổ sung thêm mục vào cuối file khi cần.
>
> Số trong ngoặc ở tiêu đề mỗi nhóm là số đơn vị **hiện có** trong `ROSTER` cho
> khu vực/nước đó tính đến 2026-09-06 (đếm bằng cách đọc trực tiếp mảng
> `ROSTER` trong `src/atlas.html`) — dùng để ưu tiên nơi mỏng nhất trước, không
> phải để giới hạn worker (worker luôn tự loại trùng theo tên/domain).

## Đông Nam Á — mỏng nhất, ưu tiên cao nhất

1. [pending] Malaysia (hiện có 4) — TTO/trung tâm ĐMST các đại học công lập lớn ngoài UM/USM/UKM/UTM đã có (thử UPM, UiTM, USIM, UMS...)
   - Ngày xử lý: — · Số mục thêm: —
2. [pending] Thái Lan (hiện có 4) — TTO/trung tâm ĐMST các đại học lớn ngoài Chulalongkorn/Mahidol đã có (thử Chiang Mai, Khon Kaen, Kasetsart, Thammasat, KMUTT)
   - Ngày xử lý: — · Số mục thêm: —
3. [pending] Indonesia (hiện có 3) — TTO/Science Techno Park các đại học lớn (UI, ITB, UGM, IPB, Universitas Airlangga)
   - Ngày xử lý: — · Số mục thêm: —
4. [pending] Philippines (hiện có 3) — Technology Transfer/Innovation Support Office các đại học (UP System, Ateneo, De La Salle, Mapua, UST)
   - Ngày xử lý: — · Số mục thêm: —
5. [pending] Singapore (hiện có 3) — trung tâm CGCN/ĐMST ngoài NUS/BLOCK71 đã có (NTUitive đã có — thử SMU, SUTD, SIT, SUSS)
   - Ngày xử lý: — · Số mục thêm: —
6. [pending] Campuchia, Myanmar, Brunei (hiện có 0) — trung tâm ĐMST/khởi nghiệp đại học nếu có (RUPP, ITC Campuchia; Yangon Technological University; Universiti Brunei Darussalam)
   - Ngày xử lý: — · Số mục thêm: —

## Nam Á (ngoài Ấn Độ — Ấn Độ đã có 145, không cần tìm thêm)

7. [pending] Pakistan (hiện có 1) — TTO các đại học lớn (LUMS, NUST, Karachi, Punjab)
   - Ngày xử lý: — · Số mục thêm: —
8. [pending] Bangladesh, Sri Lanka, Nepal (hiện có 0) — trung tâm ĐMST/CGCN đại học nếu có (BUET, Dhaka; Moratuwa, Colombo; Tribhuvan)
   - Ngày xử lý: — · Số mục thêm: —

## Đông Á (ngoài Nhật Bản — đã có 30, khá đầy đủ)

9. [pending] Trung Quốc (hiện có 10 — rất mỏng so với quy mô hệ thống đại học) — TTO các đại học top ngoài Tsinghua/Peking đã có (thử Fudan, Zhejiang, Shanghai Jiao Tong, USTC)
   - Ngày xử lý: — · Số mục thêm: —
10. [pending] Hàn Quốc (hiện có 7) — TTO/trung tâm CGCN các đại học lớn (KAIST, SNU, Yonsei, POSTECH)
    - Ngày xử lý: — · Số mục thêm: —
11. [pending] Đài Loan (hiện có 5) — TTO các đại học lớn ngoài NTU/NTHU đã có (NCTU/NYCU, NCKU)
    - Ngày xử lý: — · Số mục thêm: —

## Châu Phi — mỏng nhất toàn châu lục

12. [pending] Nam Phi (hiện có 6) — TTO các đại học lớn ngoài Wits/UCT đã có (Stellenbosch, Pretoria, KwaZulu-Natal)
    - Ngày xử lý: — · Số mục thêm: —
13. [pending] Kenya (hiện có 0) — trung tâm ĐMST/CGCN đại học (University of Nairobi, Strathmore, JKUAT)
    - Ngày xử lý: — · Số mục thêm: —
14. [pending] Nigeria (hiện có 1) — TTO đại học ngoài đơn vị đã có (Lagos, Ibadan, Covenant University)
    - Ngày xử lý: — · Số mục thêm: —
15. [pending] Ghana (hiện có 1) — trung tâm ĐMST đại học ngoài đơn vị đã có (KNUST, Legon)
    - Ngày xử lý: — · Số mục thêm: —
16. [pending] Ai Cập (hiện có 3) — TTO đại học ngoài Cairo/AUC đã có (Alexandria, Ain Shams)
    - Ngày xử lý: — · Số mục thêm: —
17. [pending] Morocco, Tunisia, Algeria (hiện có 1, 0, 0) — trung tâm ĐMST đại học nếu có (Mohammed V, Manouba, USTHB)
    - Ngày xử lý: — · Số mục thêm: —
18. [pending] Rwanda, Senegal, Ethiopia, Uganda (hiện có 0, 0, 1, 2) — trung tâm ĐMST đại học nếu có (University of Rwanda, Cheikh Anta Diop, Addis Ababa, Makerere)
    - Ngày xử lý: — · Số mục thêm: —

## Trung Đông

19. [pending] UAE (hiện có 2) — trung tâm ĐMST/CGCN đại học ngoài đơn vị đã có (Khalifa University, AUS, NYU Abu Dhabi)
    - Ngày xử lý: — · Số mục thêm: —
20. [pending] Israel (hiện có 6) — TTO đại học ngoài các case đã có — kiểm kỹ trùng tên vì Israel có các công ty CGCN nổi tiếng riêng lẻ (Yissum/Hebrew Univ, Yeda/Weizmann, Ramot/Tel Aviv có thể đã nằm trong CASES chứ không phải ROSTER)
    - Ngày xử lý: — · Số mục thêm: —
21. [pending] Lebanon, Jordan, Qatar (hiện có 0, 1, 1) — trung tâm ĐMST đại học nếu có (American University of Beirut; Jordan University; Qatar University, HBKU)
    - Ngày xử lý: — · Số mục thêm: —

## Trung Á (hiện có 0)

22. [pending] Kazakhstan, Uzbekistan — trung tâm ĐMST đại học nếu có (Nazarbayev University, National University of Uzbekistan)
    - Ngày xử lý: — · Số mục thêm: —

## Mỹ Latinh (ngoài Brazil 18/Colombia 7/Chile 6/Mexico 4 đã có)

23. [pending] Argentina (hiện có 2) — TTO đại học ngoài đơn vị đã có (UBA, UNLP, UNC)
    - Ngày xử lý: — · Số mục thêm: —
24. [pending] Peru (hiện có 4) — TTO đại học ngoài các đơn vị đã có (PUCP, UNI, UNMSM)
    - Ngày xử lý: — · Số mục thêm: —
25. [pending] Ecuador, Uruguay, Bolivia, Paraguay (hiện có 0, 1, 0, 0) — trung tâm ĐMST đại học nếu có
    - Ngày xử lý: — · Số mục thêm: —
26. [pending] Trung Mỹ: Panama, Guatemala (hiện có 0, 0) — trung tâm ĐMST đại học nếu có (ngoài Costa Rica 3 đã có)
    - Ngày xử lý: — · Số mục thêm: —

## Đông Âu / Balkan (thưa)

27. [pending] Romania (hiện có 1) — TTO đại học ngoài đơn vị đã có (Bucharest, Cluj-Napoca, Iasi)
    - Ngày xử lý: — · Số mục thêm: —
28. [pending] Serbia, Bosnia, Bắc Macedonia, Albania (hiện có 0 mỗi nước) — trung tâm ĐMST đại học vùng Balkan nếu có
    - Ngày xử lý: — · Số mục thêm: —
29. [pending] Ukraine (hiện có 0) — trung tâm ĐMST đại học nếu còn hoạt động công khai (Kyiv, Lviv)
    - Ngày xử lý: — · Số mục thêm: —

## Danh bạ hiệp hội TTO khu vực (hiệu suất cao — nhiều nước một lượt, dễ trùng nên để worker tự lọc)

30. [pending] ASTP-Proton (astp4kt.eu hoặc astp.net) — member directory, ưu tiên hội viên từ các nước Đông Âu/Bắc Âu còn thiếu (Romania, Bulgaria, Slovakia, Croatia, Estonia, Iceland)
    - Ngày xử lý: — · Số mục thêm: —
31. [pending] RedOTT / RedEmprendia (Mỹ Latinh) — danh bạ hội viên, ưu tiên nước ngoài Brazil/Colombia/Chile/Mexico
    - Ngày xử lý: — · Số mục thêm: —
32. [pending] AUTM (autm.net) member directory (Bắc Mỹ) — chỉ các trường/viện chưa có trong roster (dễ trùng vì US/Canada đã khá đầy — worker tự dedupe theo tên/domain)
    - Ngày xử lý: — · Số mục thêm: —
33. [pending] UNITT (unitt.jp) member directory (Nhật) — hội viên ngoài các TLO đã có
    - Ngày xử lý: — · Số mục thêm: —
34. [pending] THETA / KTA network (Australia/NZ) member directory — bổ sung ngoài 11 (Úc) + 6 (NZ) đã có
    - Ngày xử lý: — · Số mục thêm: —

---
**Vị trí canonical:** `Innovation-Center-Atlas/_claude/roster-grow-queue.md`. Sếp
thêm mục mới ở cuối file theo đúng khuôn `[pending] <mô tả> ... - Ngày xử lý: — · Số mục thêm: —`.
