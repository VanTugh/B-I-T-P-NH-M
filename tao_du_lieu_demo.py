"""Module 2: Sinh dữ liệu sinh viên demo (tao_du_lieu_demo.py)

Dự án: Quản lý phòng máy tính 12 vị trí (3 hàng x 4 cột).
Trách nhiệm:
- Sinh tối thiểu 100 hồ sơ sinh viên từ SV001 đến SV100.
- Đảm bảo tính an toàn (idempotency): Chạy nhiều lần không làm nhân đôi dữ liệu.
- Không làm mất hoặc xáo trộn các lượt xếp chỗ đang có trong bảng xep_cho.
- Quản lý vòng đời connection và cursor chặt chẽ, đóng tài nguyên trong finally.
- Chạy độc lập được bằng lệnh: python tao_du_lieu_demo.py.
"""

import sys

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from database import get_connection, init_db, DB_NAME


def seed_students(n: int = 100, db_name: str = DB_NAME) -> int:
    """Khởi tạo danh sách n sinh viên demo từ SV001 đến SV100.
    
    Sử dụng câu lệnh 'INSERT OR IGNORE' để nếu sinh viên đã tồn tại thì bỏ qua,
    tránh lỗi duplicate key và không làm tăng số lượng bản ghi.
    
    Args:
        n: Số lượng sinh viên demo cần tạo (mặc định là 100).
        db_name: Tên cơ sở dữ liệu SQLite.
        
    Returns:
        int: Tổng số sinh viên hiện có trong bảng sinh_vien sau khi thực hiện.
    """
    # Đảm bảo bảng CSDL đã được tạo
    init_db(db_name)
    
    with get_connection(db_name) as conn:
        cursor = conn.cursor()
        try:
            # Sử dụng vòng lặp sinh n sinh viên
            for i in range(1, n + 1):
                ma_sv = f"SV{i:03d}"
                ho_ten = f"Sinh viên {i:03d}"
                cursor.execute(
                    "INSERT OR IGNORE INTO sinh_vien (ma_sv, ho_ten) VALUES (?, ?);",
                    (ma_sv, ho_ten)
                )
                
            # Đếm tổng số sinh viên thực tế trong cơ sở dữ liệu
            cursor.execute("SELECT COUNT(*) FROM sinh_vien;")
            total_students = cursor.fetchone()[0]
        finally:
            cursor.close()
            
    return total_students


if __name__ == "__main__":
    print("[*] Đang tiến hành sinh dữ liệu sinh viên demo...")
    total = seed_students(100)
    print(f"[+] Hoàn tất! Tổng số lượng sinh viên hiện có trong CSDL: {total}")
