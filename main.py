"""Điểm khởi chạy chính của Ứng dụng Quản lý Phòng máy tính (main.py)

Dự án: Quản lý phòng máy tính 12 vị trí (3 hàng x 4 cột).
Luồng khởi động:
1. Khởi tạo database (init_db) nếu chưa tồn tại.
2. Kiểm tra cấu trúc bảng sinh_vien và xep_cho.
3. Đảm bảo dữ liệu sinh viên demo tối thiểu 100 sinh viên đã được tạo (seed_students).
4. Khởi chạy giao diện chính Tkinter (MainWindow).
5. Đọc trạng thái chỗ ngồi hiện tại trực tiếp từ SQLite (không reset dữ liệu cũ).
"""

import sys

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

import tkinter as tk
from database import init_db, get_seat_stats, DB_NAME
from tao_du_lieu_demo import seed_students
from ui.main_window import MainWindow


def main():
    """Hàm khởi động chính của ứng dụng."""
    print("=" * 65)
    print(" HỆ THỐNG QUẢN LÝ PHÒNG MÁY TÍNH - 12 VỊ TRÍ (SQLITE)")
    print("=" * 65)
    
    # 1. Khởi tạo cơ sở dữ liệu SQLite
    try:
        init_db(DB_NAME)
        print("[+] Bước 1: Khởi tạo/kiểm tra cấu trúc cơ sở dữ liệu SQLite thành công.")
    except Exception as e:
        print(f"[-] LỖI KHỞI TẠO CSDL: {e}")
        sys.exit(1)
        
    # 2. Đảm bảo nạp dữ liệu sinh viên demo (chạy lặp an toàn không duplicate)
    try:
        total_students = seed_students(100, DB_NAME)
        print(f"[+] Bước 2: Kiểm tra dữ liệu demo: {total_students} hồ sơ sinh viên đã sẵn sàng.")
    except Exception as e:
        print(f"[-] LỖI SINH DỮ LIỆU DEMO: {e}")
        sys.exit(1)
        
    # 3. Đọc số liệu hiện tại từ SQLite
    stats = get_seat_stats(DB_NAME)
    print(f"[*] Trạng thái phòng máy hiện tại: {stats['used']}/{stats['total']} vị trí đang sử dụng.")
    
    # 4. Khởi động giao diện Tkinter
    print("[+] Bước 3: Đang khởi chạy Giao diện Người dùng Tkinter...")
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()
    print("[*] Ứng dụng đã đóng. Dữ liệu phòng máy được lưu an toàn trong SQLite.")


if __name__ == "__main__":
    main()
