"""Kiểm thử đơn vị cho Module Cơ sở dữ liệu (tests/test_database.py)

Kiểm tra:
- Khởi tạo bảng CSDL.
- Kiểm tra PRAGMA foreign_keys = ON.
- Ràng buộc PRIMARY KEY, FOREIGN KEY, UNIQUE.
- Hàm get_seat_map() và get_seat_stats().
- Đảm bảo giải phóng tài nguyên connection và cursor sau mỗi ca kiểm thử.
"""

import os
import unittest
import sqlite3
from database import get_connection, init_db, get_seat_map, get_seat_stats, VALID_SEATS

TEST_DB = "test_database_module.db"


class TestDatabaseModule(unittest.TestCase):
    def setUp(self):
        """Khởi tạo môi trường CSDL sạch cho mỗi ca kiểm thử."""
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)
        init_db(TEST_DB)

    def tearDown(self):
        """Dọn dẹp tệp CSDL sau khi kiểm thử."""
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)

    def test_foreign_keys_enabled(self):
        """Kiểm tra PRAGMA foreign_keys bắt buộc phải được kích hoạt."""
        with get_connection(TEST_DB) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("PRAGMA foreign_keys;")
                fk_status = cursor.fetchone()[0]
            finally:
                cursor.close()
        self.assertEqual(fk_status, 1, "Tính năng khóa ngoại chưa được bật!")

    def test_insert_nonexistent_student_raises_fk_error(self):
        """Chèn bản ghi vào xep_cho với mã SV không tồn tại bắt buộc phải ném lỗi IntegrityError."""
        with self.assertRaises(sqlite3.IntegrityError):
            with get_connection(TEST_DB) as conn:
                cursor = conn.cursor()
                try:
                    cursor.execute("INSERT INTO xep_cho (ma_cho, ma_sv) VALUES ('A1', 'SV999');")
                finally:
                    cursor.close()

    def test_duplicate_student_in_xep_cho_raises_unique_error(self):
        """Ràng buộc UNIQUE: Một sinh viên không thể xếp 2 vị trí máy khác nhau."""
        with get_connection(TEST_DB) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO sinh_vien (ma_sv, ho_ten) VALUES ('SV001', 'Sinh viên 001');")
                cursor.execute("INSERT INTO xep_cho (ma_cho, ma_sv) VALUES ('A1', 'SV001');")
            finally:
                cursor.close()
        
        # Thử xếp tiếp vào B1 -> Bắt buộc lỗi UNIQUE
        with self.assertRaises(sqlite3.IntegrityError):
            with get_connection(TEST_DB) as conn:
                cursor = conn.cursor()
                try:
                    cursor.execute("INSERT INTO xep_cho (ma_cho, ma_sv) VALUES ('B1', 'SV001');")
                finally:
                    cursor.close()

    def test_duplicate_seat_raises_pk_error(self):
        """Ràng buộc PRIMARY KEY: Một vị trí máy không thể có 2 sinh viên."""
        with get_connection(TEST_DB) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO sinh_vien (ma_sv, ho_ten) VALUES ('SV001', 'Sinh viên 001');")
                cursor.execute("INSERT INTO sinh_vien (ma_sv, ho_ten) VALUES ('SV002', 'Sinh viên 002');")
                cursor.execute("INSERT INTO xep_cho (ma_cho, ma_sv) VALUES ('A1', 'SV001');")
            finally:
                cursor.close()
        
        # Thử xếp SV002 vào cùng vị trí A1 -> Bắt buộc lỗi PRIMARY KEY
        with self.assertRaises(sqlite3.IntegrityError):
            with get_connection(TEST_DB) as conn:
                cursor = conn.cursor()
                try:
                    cursor.execute("INSERT INTO xep_cho (ma_cho, ma_sv) VALUES ('A1', 'SV002');")
                finally:
                    cursor.close()

    def test_get_seat_map_structure(self):
        """Kiểm tra get_seat_map() trả về đủ 12 vị trí máy từ A1 đến C4."""
        seat_map = get_seat_map(TEST_DB)
        self.assertEqual(len(seat_map), 12)
        for seat in VALID_SEATS:
            self.assertIn(seat, seat_map)
            self.assertIsNone(seat_map[seat])

    def test_get_seat_stats_initial(self):
        """Kiểm tra số liệu thống kê ban đầu khi phòng máy trống."""
        stats = get_seat_stats(TEST_DB)
        self.assertEqual(stats["total"], 12)
        self.assertEqual(stats["used"], 0)
        self.assertEqual(stats["available"], 12)
        self.assertEqual(stats["usage_rate"], 0.0)


if __name__ == "__main__":
    unittest.main()
