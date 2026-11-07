"""Module 1: Quản lý Cơ sở dữ liệu SQLite (database.py)

Dự án: Quản lý phòng máy tính 12 vị trí (3 hàng x 4 cột).
Trách nhiệm:
- Quản lý kết nối SQLite3 và cấu hình PRAGMA foreign_keys = ON.
- Khởi tạo bảng sinh_vien và xep_cho với các ràng buộc PK, FK, UNIQUE.
- Cung cấp các hàm truy vấn dùng chung: get_seat_map(), get_seat_stats().
"""

import os
import sys
import sqlite3

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
from typing import Dict, Optional, Tuple, Any

DB_NAME = "phong_may.db"

# 12 vị trí phòng máy cố định (3 hàng x 4 cột)
VALID_SEATS = [
    "A1", "A2", "A3", "A4",
    "B1", "B2", "B3", "B4",
    "C1", "C2", "C3", "C4"
]
TOTAL_SEATS = len(VALID_SEATS)


def get_connection(db_name: str = DB_NAME) -> sqlite3.Connection:
    """Tạo và trả về kết nối SQLite3 đã được kích hoạt kiểm tra khóa ngoại.
    
    Args:
        db_name: Đường dẫn hoặc tên tệp cơ sở dữ liệu.
        
    Returns:
        sqlite3.Connection: Đối tượng kết nối với row_factory = sqlite3.Row.
    """
    conn = sqlite3.connect(db_name)
    conn.row_factory = sqlite3.Row
    # BẮT BUỘC: Bật kiểm tra ràng buộc khóa ngoại trong SQLite
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db(db_name: str = DB_NAME) -> None:
    """Khởi tạo cấu trúc các bảng trong cơ sở dữ liệu nếu chưa tồn tại.
    
    Lưu ý: Sử dụng CREATE TABLE IF NOT EXISTS để không làm mất dữ liệu cũ
    khi khởi động lại ứng dụng.
    
    Args:
        db_name: Tên tệp cơ sở dữ liệu SQLite.
    """
    with get_connection(db_name) as conn:
        cursor = conn.cursor()
        
        # Bảng 1: Danh sách hồ sơ sinh viên
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sinh_vien (
                ma_sv TEXT PRIMARY KEY,
                ho_ten TEXT NOT NULL
            );
        """)
        
        # Bảng 2: Xếp chỗ ngồi trong phòng máy
        # - ma_cho: PRIMARY KEY (mỗi vị trí máy chỉ có 1 bản ghi)
        # - ma_sv: FOREIGN KEY tham chiếu sinh_vien(ma_sv), UNIQUE (mỗi sinh viên chỉ ngồi 1 chỗ)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS xep_cho (
                ma_cho TEXT PRIMARY KEY,
                ma_sv TEXT UNIQUE NOT NULL,
                FOREIGN KEY (ma_sv) REFERENCES sinh_vien(ma_sv)
            );
        """)
        
        conn.commit()


def get_seat_map(db_name: str = DB_NAME) -> Dict[str, Optional[str]]:
    """Lấy bản đồ trạng thái toàn bộ 12 vị trí máy trong phòng máy.
    
    Args:
        db_name: Tên tệp cơ sở dữ liệu SQLite.
        
    Returns:
        Dict[str, Optional[str]]: Từ điển có 12 key từ 'A1' đến 'C4'.
        Giá trị là mã sinh viên (nếu đã có người ngồi) hoặc None (nếu đang trống).
    """
    seat_map: Dict[str, Optional[str]] = {seat: None for seat in VALID_SEATS}
    
    with get_connection(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT ma_cho, ma_sv FROM xep_cho;")
        records = cursor.fetchall()
        for row in records:
            seat_map[row["ma_cho"]] = row["ma_sv"]
            
    return seat_map


def get_seat_stats(db_name: str = DB_NAME) -> Dict[str, Any]:
    """Thống kê chi tiết trạng thái sử dụng phòng máy.
    
    Args:
        db_name: Tên tệp cơ sở dữ liệu SQLite.
        
    Returns:
        Dict[str, Any]: Gồm các trường:
        - 'total': Tổng số vị trí máy (12).
        - 'used': Số vị trí máy đang sử dụng.
        - 'available': Số vị trí máy còn trống.
        - 'usage_rate': Tỷ lệ sử dụng tính theo phần trăm (%).
    """
    with get_connection(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM xep_cho;")
        used = cursor.fetchone()[0]
        
    total = TOTAL_SEATS
    available = total - used
    usage_rate = round((used / total) * 100, 1) if total > 0 else 0.0
    
    return {
        "total": total,
        "used": used,
        "available": available,
        "usage_rate": usage_rate
    }


if __name__ == "__main__":
    init_db()
    stats = get_seat_stats()
    print("[+] Khởi tạo cơ sở dữ liệu thành công.")
    print(f"[*] Thống kê ban đầu: Đã dùng {stats['used']}/{stats['total']}, Còn trống {stats['available']}")
