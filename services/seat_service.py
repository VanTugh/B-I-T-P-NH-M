"""Module 3: Nghiệp vụ Quản lý Chỗ ngồi (services/seat_service.py)

Dự án: Quản lý phòng máy tính 12 vị trí (3 hàng x 4 cột).
Trách nhiệm:
- Xếp sinh viên vào vị trí máy tính chỉ định (assign_seat).
- Trả vị trí máy tính (release_seat).
- Kiểm tra toàn diện các điều kiện ràng buộc nghiệp vụ và tính toàn vẹn CSDL.
- Quản lý vòng đời connection và cursor chặt chẽ bằng khối try/finally, giải phóng tài nguyên.
"""

import sqlite3
from typing import Tuple
from database import get_connection, VALID_SEATS, DB_NAME


def assign_seat(ma_cho: str, ma_sv: str, db_name: str = DB_NAME) -> Tuple[bool, str]:
    """Xếp sinh viên vào vị trí máy tính trong phòng máy.
    
    Điều kiện hợp lệ:
    1. Vị trí phải hợp lệ (nằm trong danh sách 12 chỗ A1-A4, B1-B4, C1-C4).
    2. Mã sinh viên không được để trống và phải tồn tại trong bảng sinh_vien.
    3. Vị trí ma_cho chưa có sinh viên khác ngồi.
    4. Sinh viên ma_sv chưa được xếp ở vị trí máy khác.
    
    Args:
        ma_cho: Mã vị trí máy (ví dụ: 'A2').
        ma_sv: Mã sinh viên (ví dụ: 'SV100').
        db_name: Tên cơ sở dữ liệu SQLite.
        
    Returns:
        Tuple[bool, str]: 
        - bool: True nếu xếp chỗ thành công, False nếu thất bại.
        - str: Thông báo chi tiết kết quả hoặc nguyên nhân lỗi.
    """
    # Chuẩn hóa dữ liệu đầu vào: bỏ khoảng trắng và chuyển chữ hoa
    ma_cho = ma_cho.strip().upper() if ma_cho else ""
    ma_sv = ma_sv.strip().upper() if ma_sv else ""
    
    # 1. Kiểm tra vị trí có hợp lệ trong 12 chỗ hay không
    if ma_cho not in VALID_SEATS:
        return False, f"Vị trí '{ma_cho}' không hợp lệ! Chỉ chấp nhận từ A1 đến C4."
        
    # 2. Kiểm tra mã sinh viên không được rỗng
    if not ma_sv:
        return False, "Mã sinh viên không được để trống!"

    with get_connection(db_name) as conn:
        cursor = conn.cursor()
        try:
            # 3. Kiểm tra mã sinh viên có tồn tại trong hệ thống hồ sơ hay không
            cursor.execute("SELECT ho_ten FROM sinh_vien WHERE ma_sv = ?;", (ma_sv,))
            student = cursor.fetchone()
            if not student:
                return False, f"Sinh viên có mã '{ma_sv}' không tồn tại trong hệ thống!"
                
            ho_ten = student["ho_ten"]
            
            # 4. Kiểm tra vị trí máy đã có người ngồi hay chưa
            cursor.execute("SELECT ma_sv FROM xep_cho WHERE ma_cho = ?;", (ma_cho,))
            seat_occupied = cursor.fetchone()
            if seat_occupied:
                return False, f"Vị trí '{ma_cho}' đã có người ngồi (Sinh viên: {seat_occupied['ma_sv']})!"
                
            # 5. Kiểm tra sinh viên đã được xếp ở vị trí khác hay chưa
            cursor.execute("SELECT ma_cho FROM xep_cho WHERE ma_sv = ?;", (ma_sv,))
            student_assigned = cursor.fetchone()
            if student_assigned:
                return False, f"Sinh viên '{ma_sv}' ({ho_ten}) đã được xếp tại vị trí '{student_assigned['ma_cho']}' rồi!"
                
            # 6. Thỏa mãn toàn bộ điều kiện: Thực hiện lưu bản ghi xếp chỗ
            cursor.execute(
                "INSERT INTO xep_cho (ma_cho, ma_sv) VALUES (?, ?);",
                (ma_cho, ma_sv)
            )
            return True, f"Xếp chỗ thành công! Sinh viên {ma_sv} ({ho_ten}) vào vị trí {ma_cho}."
        except sqlite3.IntegrityError as e:
            conn.rollback()
            return False, f"Lỗi toàn vẹn dữ liệu SQLite: {str(e)}"
        except Exception as e:
            conn.rollback()
            return False, f"Lỗi hệ thống khi xếp chỗ: {str(e)}"
        finally:
            cursor.close()


def release_seat(ma_cho: str, db_name: str = DB_NAME) -> Tuple[bool, str]:
    """Trả lại vị trí máy tính trong phòng máy.
    
    Yêu cầu:
    - Chỉ xóa bản ghi trong bảng xep_cho.
    - TUYỆT ĐỐI KHÔNG xóa thông tin sinh viên trong bảng sinh_vien.
    - Không cho phép trả vị trí đang trống.
    
    Args:
        ma_cho: Mã vị trí máy cần trả (ví dụ: 'A2').
        db_name: Tên cơ sở dữ liệu SQLite.
        
    Returns:
        Tuple[bool, str]:
        - bool: True nếu trả chỗ thành công, False nếu thất bại.
        - str: Thông điệp kết quả.
    """
    ma_cho = ma_cho.strip().upper() if ma_cho else ""
    
    # 1. Kiểm tra vị trí có hợp lệ trong 12 chỗ hay không
    if ma_cho not in VALID_SEATS:
        return False, f"Vị trí '{ma_cho}' không hợp lệ!"
        
    with get_connection(db_name) as conn:
        cursor = conn.cursor()
        try:
            # 2. Kiểm tra vị trí có đang được sử dụng hay không
            cursor.execute("SELECT ma_sv FROM xep_cho WHERE ma_cho = ?;", (ma_cho,))
            record = cursor.fetchone()
            if not record:
                return False, f"Vị trí '{ma_cho}' hiện đang trống, không thể thực hiện trả chỗ!"
                
            ma_sv_released = record["ma_sv"]
            
            # 3. Xóa bản ghi trong bảng xep_cho
            cursor.execute("DELETE FROM xep_cho WHERE ma_cho = ?;", (ma_cho,))
            return True, f"Trả chỗ thành công! Vị trí {ma_cho} (trước đó là SV {ma_sv_released}) hiện đã trống."
        except Exception as e:
            conn.rollback()
            return False, f"Lỗi hệ thống khi trả chỗ: {str(e)}"
        finally:
            cursor.close()
