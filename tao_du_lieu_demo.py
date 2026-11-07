import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "phong_may.db")


def khoi_tao_du_lieu(db_path: str = DB_PATH) -> tuple[int, int]:
    """
    Khởi tạo cơ sở dữ liệu phong_may.db gồm 2 bảng sinh_vien và xep_cho,
    đồng thời sinh tự động 100 hồ sơ sinh viên (SV001 -> SV100).
    An toàn khi chạy nhiều lần và bảo toàn dữ liệu xếp chỗ hiện có.
    """
    conn = sqlite3.connect(db_path)
    try:
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")

        # 1. Tạo bảng sinh_vien (khóa chính ma_sv)
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS sinh_vien (
                ma_sv TEXT PRIMARY KEY,
                ho_ten TEXT NOT NULL
            )
            """
        )

        # 2. Tạo bảng xep_cho (khóa chính ma_cho, khóa ngoại ma_sv với ràng buộc UNIQUE)
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS xep_cho (
                ma_cho TEXT PRIMARY KEY,
                ma_sv TEXT NOT NULL UNIQUE,
                FOREIGN KEY (ma_sv) REFERENCES sinh_vien(ma_sv)
            )
            """
        )

        # 3. Sinh tự động 100 hồ sơ sinh viên từ SV001 đến SV100
        danh_sach_sv = [
            (f"SV{i:03d}", f"Sinh viên {i:03d}") for i in range(1, 101)
        ]
        cursor.executemany(
            "INSERT OR IGNORE INTO sinh_vien (ma_sv, ho_ten) VALUES (?, ?)",
            danh_sach_sv,
        )

        conn.commit()

        # Kiểm tra tổng số bản ghi sau khi chạy
        cursor.execute("SELECT COUNT(*) FROM sinh_vien")
        so_luong_sv = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM xep_cho")
        so_luong_xep_cho = cursor.fetchone()[0]

        return so_luong_sv, so_luong_xep_cho
    finally:
        conn.close()


if __name__ == "__main__":
    tong_sv, tong_cho = khoi_tao_du_lieu()
    print(f"Khởi tạo cơ sở dữ liệu thành công tại: {DB_PATH}")
    print(f"- Tổng số hồ sơ sinh viên trong bảng 'sinh_vien': {tong_sv}")
    print(f"- Số chỗ đang được xếp trong bảng 'xep_cho' (được bảo toàn): {tong_cho}/12")
