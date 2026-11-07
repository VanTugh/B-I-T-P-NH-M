# HƯỚNG DẪN CÁC BƯỚC THỰC HIỆN DỰ ÁN (STEP-BY-STEP GUIDE)

Tài liệu này chia dự án thành 4 bước (Phases) chính. Nhóm có thể dựa vào đây để lập trình tuần tự hoặc chia việc cho từng người làm song song.

## Bước 1: Khởi tạo Cơ sở dữ liệu và Dữ liệu mẫu (Phụ trách: Thành viên 1)

**Mục tiêu:** Tạo file `phong_may.db` và viết script sinh dữ liệu tự động.

1. **Tạo file `tao_du_lieu_demo.py`:**
   * Sử dụng thư viện `sqlite3` kết nối đến file `phong_may.db`.
   * Chạy lệnh `CREATE TABLE IF NOT EXISTS sinh_vien (...)` để tạo bảng sinh viên (khóa chính `ma_sv`).
   * Chạy lệnh `CREATE TABLE IF NOT EXISTS xep_cho (...)` để tạo bảng xếp chỗ (khóa chính `ma_cho`, khóa ngoại `ma_sv` với ràng buộc `UNIQUE`).
2. **Sinh 100 hồ sơ:**
   * Dùng vòng lặp `for i in range(1, 101):`.
   * Tạo chuỗi định dạng: Mã là `SV{i:03}` (ra SV001, SV002...), Tên là `Sinh viên {i:03}`.
   * Dùng câu lệnh `INSERT OR IGNORE INTO sinh_vien...` (hoặc kiểm tra `SELECT` trước khi `INSERT`) để đảm bảo chạy code 2 lần không bị lỗi trùng lặp.
   * `commit()` và đóng kết nối.

## Bước 2: Xây dựng Bộ khung Giao diện GUI (Phụ trách: Thành viên 2)

**Mục tiêu:** Vẽ toàn bộ nút bấm, ô nhập liệu bằng thư viện Tkinter (hoặc PyQt). Tạm thời chưa cần gắn logic database.

1. **Tạo cửa sổ chính (`MainWindow`):**
   * Khởi tạo `tk.Tk()`, thiết lập tiêu đề và kích thước.
   * Chia cửa sổ làm 2 phần: Frame Trái (Sơ đồ) và Frame Phải (Điều khiển).
2. **Vẽ sơ đồ phòng máy (Frame Trái):**
   * Tạo một Dictionary hoặc List lưu 12 mã chỗ: `['A1', 'A2', 'A3', 'A4', 'B1', ... 'C4']`.
   * Dùng 2 vòng lặp lồng nhau (hàng từ 0-2, cột từ 0-3) kết hợp phương thức `.grid(row, column)` để tạo 12 đối tượng `tk.Button`.
   * Gắn một lệnh `command` mặc định để in ra mã chỗ khi click (VD: `print("Đang chọn A1")`).
3. **Vẽ khu vực Điều khiển (Frame Phải):**
   * Label hiển thị "Ghế đang chọn: ...".
   * Entry (`tk.Entry`) để nhập mã sinh viên.
   * Các Button: "Xếp chỗ", "Trả chỗ", "Tra cứu".
   * Label (hoặc Text) để hiển thị thông báo trạng thái/lỗi.
   * Label hiển thị Bộ đếm góc dưới (VD: `0/12`).

## Bước 3: Ghép nối Logic và Database (Phụ trách: Thành viên 3 / Code chung)

**Mục tiêu:** Xử lý sự kiện click nút và tương tác với DB.

1. **Viết hàm Load dữ liệu ban đầu (`load_data_to_gui`):**
   * Khi mở app, `SELECT * FROM xep_cho`.
   * Duyệt qua 12 nút giao diện: Nếu `ma_cho` có trong kết quả trả về, đổi chữ trên nút thành `<Mã chỗ> - <Mã SV>`, đổi màu thành Đỏ/Xám. Nếu không, đổi thành `<Mã chỗ> - Trống`, đổi màu Xanh.
   * Đếm số bản ghi trả về và cập nhật biến bộ đếm (VD: `count/12`).
2. **Viết logic "Xếp chỗ":**
   * Lấy mã ghế đang chọn và mã SV từ ô nhập liệu.
   * **Validate 1:** Kiểm tra chỗ đã chọn có text "Trống" không. Nếu không, báo lỗi "Chỗ đã có người".
   * **Validate 2:** Query `SELECT * FROM sinh_vien WHERE ma_sv=?` để kiểm tra SV có tồn tại không. Nếu không, báo lỗi.
   * **Insert DB:** `INSERT INTO xep_cho(ma_cho, ma_sv) VALUES (?, ?)`.
   * **Bắt lỗi UNIQUE:** Bọc lệnh Insert trong `try... except sqlite3.IntegrityError:` để bắt lỗi SV đã có chỗ khác.
   * Cập nhật lại giao diện (gọi lại hàm ở bước 1).
3. **Viết logic "Trả chỗ":**
   * Lấy mã ghế đang chọn.
   * `DELETE FROM xep_cho WHERE ma_cho = ?`.
   * Cập nhật lại giao diện và trừ bộ đếm.
4. **Viết logic "Tra cứu":**
   * Lấy mã SV từ ô nhập liệu.
   * Dùng câu lệnh `LEFT JOIN`: `SELECT s.ho_ten, x.ma_cho FROM sinh_vien s LEFT JOIN xep_cho x ON s.ma_sv = x.ma_sv WHERE s.ma_sv = ?`.
   * In kết quả ra Label thông báo.

## Bước 4: Chạy Kịch bản Kiểm thử & Đóng gói (Làm chung)

1. Ghép toàn bộ code thành file chạy chính (VD: `main_app.py`).
2. Từng người chạy các Test Case được giao trong file PDF (Tạo dữ liệu 2 lần, Xếp SV100 vào A2, Xếp lỗi, Mở/đóng app...).
3. Tạo file Bảng phân công (`bang_phan_cong.docx/txt`) ghi rõ ai code module nào, test case nào.
4. Nén toàn bộ (Code + DB + Word) và nộp bài.