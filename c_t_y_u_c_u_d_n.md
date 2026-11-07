# ĐẶC TẢ YÊU CẦU DỰ ÁN (PROJECT SPECIFICATION)

**Tên dự án:** Ứng dụng xếp chỗ và tra cứu sinh viên phòng máy
**Môn học:** Lập trình Python nâng cao
**Thời gian thực hiện:** 120 phút

---

## 1. Tổng quan hệ thống
Hệ thống là một ứng dụng Desktop (khuyến nghị dùng `Tkinter` hoặc `PyQt`) kết hợp với cơ sở dữ liệu `SQLite`, giúp lớp trưởng dễ dàng quản lý, sắp xếp và tra cứu vị trí ngồi của sinh viên trong một phòng máy tính gồm 12 chỗ (3 hàng x 4 cột).

---

## 2. Đặc tả Cơ sở dữ liệu (Database Specification)

Hệ thống sử dụng SQLite với tệp dữ liệu lưu trữ nội bộ tên là `phong_may.db`.

### 2.1. Cấu trúc bảng
Cơ sở dữ liệu gồm 2 bảng chính:

**Bảng 1: `sinh_vien`**
| Tên cột | Kiểu dữ liệu | Ràng buộc | Mô tả |
| :--- | :--- | :--- | :--- |
| `ma_sv` | TEXT / VARCHAR | Khóa chính (Primary Key) | Mã sinh viên định danh |
| `ho_ten` | TEXT / VARCHAR | Không rỗng (NOT NULL) | Họ và tên sinh viên |

**Bảng 2: `xep_cho`**
| Tên cột | Kiểu dữ liệu | Ràng buộc | Mô tả |
| :--- | :--- | :--- | :--- |
| `ma_cho` | TEXT / VARCHAR | Khóa chính (Primary Key) | Mã ghế (VD: A1, A2, B1...) |
| `ma_sv` | TEXT / VARCHAR | Khóa ngoại (Foreign Key) tham chiếu `sinh_vien(ma_sv)`, Ràng buộc **UNIQUE** | Đảm bảo 1 sinh viên chỉ ngồi 1 chỗ |

### 2.2. Dữ liệu mẫu (`tao_du_lieu_demo.py`)
*   Sử dụng vòng lặp để tạo tự động ít nhất 100 hồ sơ.
*   **Dữ liệu:** Mã từ `SV001` đến `SV100`, Tên tương ứng từ `Sinh viên 001` đến `Sinh viên 100`.
*   **Ràng buộc logic:** 
    *   Trạng thái ban đầu: 12 chỗ đều trống.
    *   Script phải an toàn khi chạy nhiều lần (không tạo ra bản ghi trùng lặp, dùng `INSERT OR IGNORE` hoặc kiểm tra tồn tại).
    *   Bảo toàn lượt xếp chỗ hiện có khi chạy lại script.

---

## 3. Đặc tả Chức năng và Giao diện (UI & Functions)

### 3.1. Hiển thị sơ đồ phòng máy
*   **Giao diện:** 12 nút (Button) bố cục dạng lưới $3 \times 4$. Các hàng A, B, C và cột 1, 2, 3, 4.
*   **Trạng thái nút:** Hiển thị `<Mã chỗ> - Trống` hoặc `<Mã chỗ> - <Mã SV>`.
*   **Bộ đếm:** Hiển thị tổng số chỗ đang được dùng ở dạng phân số (VD: $1/12$).
*   **Bảo toàn trạng thái:** Ứng dụng phải truy vấn SQLite khi khởi động để vẽ lại sơ đồ và cập nhật bộ đếm đúng với dữ liệu lưu ở lần chạy trước.

### 3.2. Chức năng Xếp chỗ
*   **Input:** Chọn một chỗ trên sơ đồ + Nhập mã sinh viên (VD: SV001).
*   **Action:** Bấm nút **[Xếp chỗ]**.
*   **Validate (Kiểm tra hợp lệ):**
    1.  Chỗ được chọn phải đang trống.
    2.  Mã SV phải tồn tại trong bảng `sinh_vien`.
    3.  SV chưa được xếp ở bất kỳ chỗ nào khác (bắt lỗi IntegrityError do ràng buộc UNIQUE).
*   **Output:** Cập nhật DB, đổi text trên nút (thành tên SV), tăng bộ đếm. Báo lỗi chi tiết nếu vi phạm Validate.

### 3.3. Chức năng Tra cứu & Trả chỗ
*   **Tra cứu:**
    *   Input: Nhập mã sinh viên (VD: SV001).
    *   Output: Hiển thị Họ tên và Chỗ đang ngồi (hoặc thông báo chưa xếp chỗ).
*   **Trả chỗ:**
    *   Input: Chọn ghế đang có sinh viên ngồi trên sơ đồ (VD: A2 đang có SV001).
    *   Action: Bấm nút **[Trả chỗ]**.
    *   Output: Xóa bản ghi có `ma_cho = 'A2'` trong bảng `xep_cho`. Cập nhật nút về trạng thái `A2 - Trống`. Giảm bộ đếm.

---

## 4. Kịch bản kiểm thử (Test Cases)

| Kịch bản (Test Case) | Các bước thực hiện | Kết quả mong đợi (Expected Result) |
| :--- | :--- | :--- |
| **TC1: Khởi tạo dữ liệu** | Chạy file `tao_du_lieu_demo.py` 2 lần liên tiếp. | DB có đủ 100 hồ sơ. Số lượng bản ghi không tăng lên (giữ nguyên) ở lần chạy thứ hai. Không báo lỗi crash. |
| **TC2: Xếp chỗ hợp lệ** | Tìm `SV100`, chọn ghế `A2`, bấm [Xếp chỗ]. | Hiển thị đúng họ tên `Sinh viên 100`. Nút A2 đổi thành `A2 - SV100`. Bộ đếm hiện $1/12$. |
| **TC3: Ràng buộc xếp chỗ** | 1. Thử xếp `SV001` vào `A2`.<br>2. Thử xếp `SV100` vào `B1`. | 1. Báo lỗi chỗ đã có người, A2 vẫn là SV100.<br>2. Báo lỗi SV đã có chỗ, B1 vẫn trống. |
| **TC4: Lưu trữ trạng thái** | Đóng ứng dụng hoàn toàn và mở lại. | Giao diện nạp lại dữ liệu: A2 vẫn hiển thị SV100, bộ đếm giữ mức $1/12$. |
| **TC5: Trả chỗ & Cập nhật** | 1. Chọn `A2`, bấm [Trả chỗ].<br>2. Tra cứu lại `SV100`. | Bộ đếm giảm về $0/12$. Trạng thái của SV100 khi tra cứu báo "Chưa được xếp chỗ". |

---

## 5. Phân công & Đóng gói nộp bài

*   **File cần nộp:**
    1.  Mã nguồn chính (`main.py` / `app.py`).
    2.  File tạo dữ liệu (`tao_du_lieu_demo.py`).
    3.  Tệp database (`phong_may.db`).
    4.  Bảng thống kê đóng góp nhóm.
*   **Thuyết trình:** Mỗi thành viên phải chạy code của mình, tự giải thích xử lý lỗi và chạy một Kịch bản kiểm thử (Test case).