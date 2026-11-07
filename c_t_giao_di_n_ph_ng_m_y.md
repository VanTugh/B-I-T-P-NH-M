# ĐẶC TẢ GIAO DIỆN (UI/UX SPECIFICATION)

**Dự án:** Xây dựng ứng dụng xếp chỗ và tra cứu sinh viên trong phòng máy  
**Môn học:** Lập trình Python nâng cao

---

## 1. Tổng quan thiết kế (Overview)
Tài liệu này mô tả chi tiết các thành phần giao diện người dùng (UI) và luồng tương tác (UX) cho ứng dụng quản lý phòng máy. Ứng dụng được thiết kế dạng Desktop App (khuyến nghị sử dụng **Tkinter** hoặc **PyQt5**) với giao diện trực quan, chia thành các khu vực chức năng rõ ràng.

## 2. Bố cục màn hình (Layout)
Cửa sổ chính của ứng dụng nên được chia thành 2 phần (Panels) chính để tối ưu hóa không gian hiển thị:
*   **Panel Trái (Khu vực Sơ đồ):** Chiếm khoảng 60% chiều rộng, hiển thị sơ đồ 12 chỗ ngồi trực quan.
*   **Panel Phải (Khu vực Thao tác):** Chiếm 40% chiều rộng, chứa các trường nhập liệu, nút bấm chức năng và thông báo trạng thái/bộ đếm.

---

## 3. Chi tiết các thành phần giao diện (UI Components)

### 3.1. Khu vực Sơ đồ phòng máy
Bao gồm 12 nút bấm (Button) được sắp xếp theo dạng lưới (Grid) với 3 hàng (A, B, C) và 4 cột (1, 2, 3, 4).

| Trạng thái | Màu sắc (Gợi ý) | Hiển thị Text | Hành động khi click |
| :--- | :--- | :--- | :--- |
| **Trống** | Xanh lá nhạt (Light Green) | Ví dụ: `A1 - Trống` | Chọn ghế để thực hiện "Xếp chỗ" |
| **Đã có người** | Xám hoặc Đỏ nhạt (Light Coral) | Ví dụ: `A2 - SV001` | Chọn ghế để thực hiện "Trả chỗ" |

### 3.2. Khu vực Thao tác & Bộ đếm

| Thành phần | Loại Widget | Mô tả chi tiết |
| :--- | :--- | :--- |
| **Ghế đang chọn** | Label | Hiển thị mã ghế người dùng vừa click bên sơ đồ (VD: "Đang chọn: A2"). Mặc định: "Chưa chọn". |
| **Mã sinh viên** | Entry (Textbox) | Ô nhập liệu để nhập mã sinh viên (VD: SV001). Cần bắt sự kiện Enter để tra cứu nhanh. |
| **Xếp chỗ** | Button | Nút bấm để gán mã sinh viên vào ghế đang chọn. Màu sắc: Xanh dương (Blue). |
| **Trả chỗ** | Button | Nút bấm để hủy chỗ ngồi của ghế đang chọn. Màu sắc: Cam hoặc Đỏ (Orange/Red). |
| **Tra cứu** | Button | Nút bấm để tìm kiếm thông tin theo mã sinh viên. Màu sắc: Xám nhạt. |
| **Thông báo/Kết quả**| Label (Multiline) | Vùng text hiển thị họ tên sinh viên sau khi tra cứu, hoặc hiển thị lỗi (VD: "Mã SV không tồn tại"). Chữ màu đỏ nếu là lỗi, xanh nếu thành công. |
| **Bộ đếm** | Label | Hiển thị góc dưới cùng: "Số chỗ đã sử dụng: X/12" (VD: 1/12). |

---

## 4. Luồng tương tác người dùng (User Flows)

### 4.1. Luồng Xếp chỗ
1. Người dùng click vào một nút ghế có trạng thái "Trống" trên sơ đồ.
2. Nhãn "Ghế đang chọn" cập nhật mã ghế (VD: *A2*).
3. Người dùng nhập `SV001` vào ô Mã sinh viên.
4. Người dùng bấm **"Xếp chỗ"**.
5. Hệ thống kiểm tra hợp lệ (DB). Nếu thành công:
   * Nút A2 đổi màu, text đổi thành `A2 - SV001`.
   * Bộ đếm tăng lên (VD: *1/12*).
   * Xóa trắng ô nhập liệu và hiển thị thông báo thành công.
6. Nếu thất bại, giữ nguyên mọi thứ và báo lỗi tại vùng Thông báo.

### 4.2. Luồng Tra cứu & Trả chỗ

**Tra cứu:**
*   Nhập `SV100` -> Bấm **"Tra cứu"**.
*   Hiển thị thông báo: "Họ tên: Sinh viên 100 - Đang ngồi: A2" hoặc "Chưa được xếp chỗ".

**Trả chỗ:**
*   *Cách 1:* Click trực tiếp vào ghế `A2 - SV001` trên sơ đồ -> Bấm **"Trả chỗ"**.
*   *Cách 2 (Optional):* Nhập mã `SV100` -> Bấm **Trả chỗ**.
*   *Kết quả:* Nút A2 trở về màu xanh (Trống), text thành `A2 - Trống`, bộ đếm giảm xuống tương ứng.

---

## 5. Danh sách thông báo lỗi (Error Messages)
*   **Lỗi chọn ghế:** "Vui lòng chọn một chỗ ngồi trên sơ đồ!"
*   **Lỗi khi xếp chỗ (Ghế đã có người):** "Chỗ A2 đã có người ngồi!"
*   **Lỗi khi xếp chỗ (SV đã có chỗ):** "Sinh viên SV100 đã được xếp ở một vị trí khác!"
*   **Lỗi dữ liệu SV:** "Mã sinh viên không tồn tại trong cơ sở dữ liệu!"