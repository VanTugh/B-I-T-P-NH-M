# HỆ THỐNG QUẢN LÝ PHÒNG MÁY TÍNH (12 VỊ TRÍ – BỐ CỤC 3×4 – SQLITE)

**Học phần:** Lập trình Python Nâng Cao (Advanced Python Programming)  
**Bài tập nhóm:** Phát triển ứng dụng hỗ trợ Lớp trưởng xếp chỗ, trả chỗ và tra cứu sinh viên phòng máy tính.  
**Phiên bản:** 1.0.0 (Release)  
**Mô hình phát triển:** 3-Tier Layered Architecture (UI – Services – SQLite Database)  

---

## 1. GIỚI THIỆU DỰ ÁN

Hệ thống Quản lý Phòng máy tính là ứng dụng desktop hoàn chỉnh được xây dựng nhằm tin học hóa công tác quản lý phòng thực hành máy tính cho lớp học. Phòng máy được bố trí theo cấu trúc ma trận gồm **12 vị trí máy** (3 hàng × 4 cột).

Ứng dụng hỗ trợ Lớp trưởng quản lý hồ sơ sinh viên (tối thiểu 100 sinh viên demo), xếp sinh viên vào chỗ ngồi, giải phóng vị trí máy, tra cứu thông tin và hiển thị tỷ lệ lấp đầy trực quan trong thời gian thực. Toàn bộ dữ liệu được lưu trữ bền vững trong cơ sở dữ liệu quan hệ **SQLite3** cục bộ, bảo đảm dữ liệu vẫn nguyên vẹn khi tắt và mở lại chương trình.

---

## 2. CÁC CHỨC NĂNG CHÍNH

1. **Hiển thị sơ đồ 12 vị trí máy:**
   - Trực quan hóa 12 máy tính theo đúng bố cục 3 hàng × 4 cột:
     - Hàng A: A1, A2, A3, A4
     - Hàng B: B1, B2, B3, B4
     - Hàng C: C1, C2, C3, C4
   - Phân biệt rõ rệt bằng màu sắc: Chỗ trống hiển thị màu xanh nhạt `[A1 - Trống]`; Chỗ đã có người ngồi hiển thị màu xanh lá đậm `[A2 - SV100]`.
   - Cơ chế highlight viền đậm khi người dùng click chọn vị trí.

2. **Xếp sinh viên vào vị trí (Assign Seat):**
   - Kiểm tra mã sinh viên phải tồn tại trong danh sách hồ sơ.
   - Kiểm tra vị trí máy phải hợp lệ (từ A1 đến C4).
   - Kiểm tra vị trí máy chưa bị ai chiếm giữ (chống xếp đè).
   - Kiểm tra sinh viên chưa được xếp ở bất kỳ vị trí máy nào khác (mỗi sinh viên chỉ ngồi 1 chỗ).
   - Bắt lỗi ngoại lệ toàn vẹn dữ liệu SQLite và thông báo rõ ràng cho người dùng.

3. **Trả vị trí máy (Release Seat):**
   - Chỉ giải phóng vị trí máy đang có người sử dụng.
   - Không cho phép trả vị trí đang trống.
   - Có hộp thoại xác nhận trước khi thực hiện trả chỗ.
   - **Bảo toàn dữ liệu:** Chỉ xóa bản ghi xếp chỗ trong bảng `xep_cho`, tuyệt đối **không xóa** hồ sơ sinh viên trong bảng `sinh_vien`.

4. **Tra cứu sinh viên theo mã (Student Lookup):**
   - Sử dụng kỹ thuật `LEFT JOIN` giữa 2 bảng để phân biệt chuẩn xác 3 trạng thái:
     * *Không tìm thấy:* Sinh viên không có trong cơ sở dữ liệu.
     * *Chưa xếp chỗ:* Sinh viên có hồ sơ nhưng chưa được gán vị trí máy (`ma_cho = None`).
     * *Đã xếp chỗ:* Hiển thị họ tên kèm vị trí máy đang ngồi (ví dụ: `A2`) và tự động làm nổi bật vị trí đó trên sơ đồ.

5. **Thống kê phòng máy thời gian thực (Statistics):**
   - Tổng số vị trí: 12 máy cố định.
   - Số vị trí đã sử dụng: `COUNT(*)` từ bảng `xep_cho`.
   - Số vị trí còn trống: `12 - Đã dùng`.
   - Tỷ lệ sử dụng phòng máy theo phần trăm (`%`).

6. **Lưu trữ dữ liệu bền vững (Persistence):**
   - Mọi thay đổi đều được `COMMIT` tức thì vào CSDL `phong_may.db`.
   - Đóng và mở lại ứng dụng trạng thái sơ đồ và bộ đếm được khôi phục 100%.

7. **Sinh dữ liệu sinh viên demo (Data Seeding):**
   - Tự động sinh tối thiểu 100 sinh viên mẫu (`SV001` đến `SV100`).
   - Sử dụng `INSERT OR IGNORE` bảo đảm chạy nhiều lần không duplicate và không mất dữ liệu xếp chỗ hiện có.

---

## 3. CÔNG NGHỆ SỬ DỤNG

- **Ngôn ngữ:** Python 3.10+
- **Giao diện người dùng (GUI):** Thư viện chuẩn `tkinter` (kết hợp `ttk`, `messagebox`).
- **Cơ sở dữ liệu:** `sqlite3` (kích hoạt `PRAGMA foreign_keys = ON`).
- **Kiểm thử tự động:** Thư viện chuẩn `unittest`.
- **Quản lý mã nguồn:** Git & GitHub (Quy chuẩn phân nhánh Git Flow).

*Dự án ưu tiên 100% thư viện chuẩn đi kèm Python, không yêu cầu cài đặt thêm các framework phức tạp bên ngoài.*

---

## 4. CẤU TRÚC THƯ MỤC DỰ ÁN

```text
Python_Computer_Lab/
│
├── main.py                     # Điểm khởi chạy chính của ứng dụng
├── database.py                 # Module CSDL: kết nối, tạo bảng, map, stats
├── tao_du_lieu_demo.py         # Script sinh tối thiểu 100 sinh viên demo an toàn
├── phong_may.db                # Cơ sở dữ liệu SQLite cục bộ
│
├── services/                   # Tầng xử lý nghiệp vụ (Business Logic Layer)
│   ├── __init__.py
│   ├── seat_service.py         # Nghiệp vụ xếp chỗ và trả chỗ
│   └── student_service.py      # Nghiệp vụ tra cứu sinh viên và thống kê
│
├── ui/                         # Tầng giao diện người dùng (Presentation Layer)
│   ├── __init__.py
│   └── main_window.py          # Lớp MainWindow điều khiển GUI Tkinter 12 nút
│
├── tests/                      # Bộ kiểm thử tự động (Unit & Integration Tests)
│   ├── __init__.py
│   ├── test_database.py        # Kiểm thử module database & ràng buộc CSDL
│   ├── test_seat_service.py    # Kiểm thử nghiệp vụ xếp chỗ và trả chỗ
│   ├── test_student_service.py # Kiểm thử nghiệp vụ tra cứu và thống kê
│   ├── test_ui.py              # Kiểm thử thành phần giao diện Tkinter
│   └── test_scenarios.py       # Kiểm thử 9 kịch bản bắt buộc (TC01 - TC09 + biên)
│
├── requirements.txt            # Thông tin môi trường và thư viện phụ trợ
├── README.md                   # Hướng dẫn chi tiết sử dụng và vận hành dự án
└── .gitignore                  # Cấu hình bỏ qua tệp tạm và CSDL test
```

---

## 5. YÊU CẦU MÔI TRƯỜNG

- Hệ điều hành: Windows 10/11, macOS, hoặc Linux.
- Phiên bản Python: Python 3.10 trở lên.
- Đã cài đặt Git (nếu muốn clone và quản lý mã nguồn).

---

## 6. HƯỚNG DẪN CÀI ĐẶT

1. **Clone repository từ GitHub:**
   ```bash
   git clone https://github.com/VanTugh/B-I-T-P-NH-M.git
   cd B-I-T-P-NH-M
   ```

2. **(Tùy chọn) Khởi tạo và kích hoạt môi trường ảo:**
   - Trên Windows:
     ```powershell
     python -m venv venv
     .\venv\Scripts\activate
     ```
   - Trên Linux / macOS:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Cài đặt thư viện (nếu cần biên soạn tài liệu Word):**
   ```bash
   pip install -r requirements.txt
   ```

---

## 7. HƯỚNG DẪN TẠO DATABASE VÀ DỮ LIỆU DEMO

Bạn có thể chủ động khởi tạo CSDL và sinh 100 sinh viên demo độc lập từ dòng lệnh:

```bash
# 1. Khởi tạo cấu trúc bảng CSDL
python database.py

# 2. Sinh tối thiểu 100 sinh viên demo (SV001 - SV100)
python tao_du_lieu_demo.py
```

*Lưu ý: Bạn có thể chạy lại lệnh `python tao_du_lieu_demo.py` nhiều lần mà không lo trùng lặp dữ liệu hay mất dữ liệu đang xếp chỗ.*

---

## 8. HƯỚNG DẪN CHẠY ỨNG DỤNG

Để khởi động toàn bộ ứng dụng quản lý phòng máy:

```bash
python main.py
```

Khi chạy lệnh này, ứng dụng sẽ tự động:
1. Kiểm tra và khởi tạo CSDL `phong_may.db` nếu chưa có.
2. Tự động kiểm tra và nạp 100 sinh viên demo nếu cơ sở dữ liệu đang rỗng.
3. Nạp trạng thái xếp chỗ hiện tại từ SQLite và mở cửa sổ giao diện Tkinter.

---

## 9. HƯỚNG DẪN CHẠY BỘ KIỂM THỬ (TEST SUITE)

Hệ thống tích hợp bộ kiểm thử toàn diện với **31 test case** tự động, bao phủ 100% các tình huống nghiệp vụ và kịch bản bắt buộc:

### Chạy toàn bộ test suite:
```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

### Chạy riêng từng module test:
```bash
# 1. Kiểm thử kịch bản bắt buộc của đề bài (TC01 đến TC09 + kiểm thử biên):
python -m unittest tests/test_scenarios.py -v

# 2. Kiểm thử CSDL và các ràng buộc khóa ngoại / UNIQUE:
python -m unittest tests/test_database.py -v

# 3. Kiểm thử nghiệp vụ xếp chỗ và trả chỗ:
python -m unittest tests/test_seat_service.py -v

# 4. Kiểm thử tra cứu sinh viên và thống kê:
python -m unittest tests/test_student_service.py -v

# 5. Kiểm thử tương tác giao diện Tkinter:
python -m unittest tests/test_ui.py -v
```

---

## 10. MÔ TẢ CẤU TRÚC DATABASE (SQLITE SCHEMA)

Hệ thống sử dụng cơ sở dữ liệu quan hệ `phong_may.db` gồm 2 bảng chuẩn hóa:

### Bảng 1: `sinh_vien` (Danh sách hồ sơ sinh viên)
| Tên cột | Kiểu dữ liệu | Ràng buộc | Ý nghĩa |
|---|---|---|---|
| `ma_sv` | TEXT | PRIMARY KEY | Mã định danh sinh viên duy nhất (ví dụ: `SV001`, `SV100`) |
| `ho_ten` | TEXT | NOT NULL | Họ và tên sinh viên (ví dụ: `Sinh viên 001`) |

### Bảng 2: `xep_cho` (Xếp chỗ phòng máy tính)
| Tên cột | Kiểu dữ liệu | Ràng buộc | Ý nghĩa |
|---|---|---|---|
| `ma_cho` | TEXT | PRIMARY KEY | Mã vị trí máy tính duy nhất (`A1` đến `C4`) |
| `ma_sv` | TEXT | UNIQUE, NOT NULL, FOREIGN KEY | Mã sinh viên đang ngồi máy, tham chiếu `sinh_vien(ma_sv)` |

### Quy tắc toàn vẹn dữ liệu:
- Luôn bật `PRAGMA foreign_keys = ON;` trên mọi kết nối SQLite.
- `ma_cho` là Khóa chính: Mỗi máy chỉ có tối đa 1 sinh viên.
- `ma_sv` có ràng buộc `UNIQUE`: Mỗi sinh viên chỉ có tối đa 1 máy.
- `ma_sv` là Khóa ngoại: Không thể xếp chỗ cho sinh viên chưa có hồ sơ.
- Vị trí máy chưa có bản ghi trong bảng `xep_cho` được hiểu là vị trí đang **Trống**.

---

## 11. HƯỚNG DẪN SỬ DỤNG CÁC CHỨC NĂNG TRÊN GIAO DIỆN

### 1. Thao tác Xếp chỗ ngồi:
- **Bước 1:** Click chuột vào vị trí máy muốn xếp trên sơ đồ (ví dụ: nút `A2 - Trống`). Vị trí được chọn sẽ có viền nổi bật và hiển thị tại ô `Vị trí đã chọn: [A2]`.
- **Bước 2:** Nhập mã sinh viên vào ô `Mã sinh viên:` (ví dụ: `SV100`).
- **Bước 3:** Bấm nút **[✓ XẾP CHỖ]** (hoặc nhấn phím `Enter`).
- **Kết quả:** Nút `A2` chuyển sang màu xanh lá `A2 - SV100`, ô nhập được xóa trắng, bộ đếm tăng lên `1 / 12`.

### 2. Thao tác Trả chỗ ngồi:
- **Bước 1:** Click chuột vào vị trí máy đang có người muốn trả (ví dụ: nút `A2 - SV100`).
- **Bước 2:** Bấm nút **[✕ TRẢ CHỖ]**.
- **Bước 3:** Hộp thoại xác nhận hiện ra, chọn **Yes** để đồng ý giải phóng vị trí máy.
- **Kết quả:** Nút `A2` trở về màu xanh nhạt `A2 - Trống`, bộ đếm giảm về `0 / 12`. Hồ sơ sinh viên `SV100` vẫn được lưu nguyên vẹn trong hệ thống.

### 3. Thao tác Tra cứu sinh viên:
- **Bước 1:** Nhập mã sinh viên cần tìm vào ô `Mã sinh viên:` trong khu vực **TRA CỨU SINH VIÊN** (ví dụ: `SV100`).
- **Bước 2:** Bấm nút **[🔍 Tra cứu]** (hoặc nhấn phím `Enter`).
- **Kết quả:**
  - Nếu sinh viên đang có chỗ ngồi: Hiển thị họ tên và vị trí máy, đồng thời hệ thống tự động làm nổi bật vị trí đó trên sơ đồ phòng máy.
  - Nếu sinh viên chưa có chỗ: Hiển thị thông báo `Trạng thái: CHƯA ĐƯỢC XẾP CHỖ`.
  - Nếu mã không tồn tại: Báo lỗi `Không tìm thấy sinh viên trong hệ thống`.

---

## 12. DANH SÁCH THÀNH VIÊN VÀ PHÂN CÔNG TRÁCH NHIỆM

| STT | Thành viên | Vai trò phụ trách | Tệp mã nguồn bàn giao | Tỷ lệ đóng góp |
|---|---|---|---|:---:|
| 1 | **TV1** | Giao diện đồ họa (UI) | `ui/main_window.py` | 20% |
| 2 | **TV2** | Nghiệp vụ Xếp chỗ & Trả chỗ | `services/seat_service.py` | 20% |
| 3 | **TV3** | Tra cứu sinh viên & Thống kê | `services/student_service.py` | 20% |
| 4 | **TV4** | Cơ sở dữ liệu SQLite & Seed data | `database.py`, `tao_du_lieu_demo.py` | 20% |
| 5 | **TV5** | Kiểm thử, Tích hợp & Tech Lead | `main.py`, `tests/*`, `README.md` | 20% |

---
*Tài liệu kỹ thuật và mã nguồn hoàn thiện phục vụ đánh giá nghiệm thu học phần Lập trình Python Nâng Cao.*
