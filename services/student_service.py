"""Module 4: Tra cứu Sinh viên và Thống kê Phòng máy (services/student_service.py)

Dự án: Quản lý phòng máy tính 12 vị trí (3 hàng x 4 cột).
Trách nhiệm:
- Tra cứu sinh viên theo mã sinh viên (sử dụng LEFT JOIN để phân biệt rõ 3 trạng thái).
- Cung cấp hàm thống kê số vị trí tổng, đã dùng, còn trống và tỷ lệ sử dụng.
"""

from typing import Optional, Dict, Any
from database import get_connection, get_seat_stats, DB_NAME


def find_student(ma_sv: str, db_name: str = DB_NAME) -> Optional[Dict[str, Any]]:
    """Tra cứu sinh viên theo mã sinh viên.
    
    Phân biệt rõ 3 trường hợp:
    1. Không tìm thấy mã sinh viên trong bảng sinh_vien -> Trả về None.
    2. Sinh viên tồn tại nhưng chưa được xếp chỗ -> Trả về Dict với ma_cho = None.
    3. Sinh viên tồn tại và đã được xếp chỗ -> Trả về Dict với ma_cho là mã vị trí máy (ví dụ: 'A2').
    
    Args:
        ma_sv: Mã sinh viên cần tra cứu (ví dụ: 'SV100').
        db_name: Tên cơ sở dữ liệu SQLite.
        
    Returns:
        Optional[Dict[str, Any]]: Từ điển thông tin sinh viên hoặc None nếu không tồn tại.
        Cấu trúc Dict:
        {
            "ma_sv": "SV100",
            "ho_ten": "Sinh viên 100",
            "ma_cho": "A2" hoặc None
        }
    """
    ma_sv = ma_sv.strip().upper() if ma_sv else ""
    if not ma_sv:
        return None
        
    with get_connection(db_name) as conn:
        cursor = conn.cursor()
        
        # Mệnh đề LEFT JOIN kết hợp bảng sinh_vien và xep_cho
        query = """
            SELECT sv.ma_sv, sv.ho_ten, xc.ma_cho
            FROM sinh_vien sv
            LEFT JOIN xep_cho xc ON sv.ma_sv = xc.ma_sv
            WHERE sv.ma_sv = ?;
        """
        cursor.execute(query, (ma_sv,))
        row = cursor.fetchone()
        
        if not row:
            return None  # Trường hợp 1: Không tồn tại
            
        return {
            "ma_sv": row["ma_sv"],
            "ho_ten": row["ho_ten"],
            "ma_cho": row["ma_cho"]  # None nếu chưa xếp, chuỗi 'A2' nếu đã xếp
        }


def get_room_statistics(db_name: str = DB_NAME) -> Dict[str, Any]:
    """Lấy số liệu thống kê phòng máy phục vụ giao diện và báo cáo.
    
    Args:
        db_name: Tên cơ sở dữ liệu SQLite.
        
    Returns:
        Dict[str, Any]:
        - 'total': 12
        - 'used': số máy đang ngồi
        - 'available': số máy còn trống
        - 'usage_rate': tỷ lệ phần trăm sử dụng (%)
    """
    return get_seat_stats(db_name)
