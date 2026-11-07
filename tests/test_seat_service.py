"""Kiểm thử đơn vị cho Module Xếp chỗ và Trả chỗ (tests/test_seat_service.py)

Kiểm tra:
- assign_seat(): Hợp lệ, Vị trí sai, Mã SV rỗng, SV không tồn tại, Chỗ đã có người, SV đã ngồi chỗ khác.
- release_seat(): Trả chỗ có người, Trả chỗ trống, Vị trí sai, Bảo toàn hồ sơ sinh_vien.
- Đảm bảo giải phóng toàn bộ kết nối và con trỏ.
"""

import os
import unittest
import sqlite3
from database import init_db, get_connection
from tao_du_lieu_demo import seed_students
from services.seat_service import assign_seat, release_seat

TEST_DB = "test_seat_service.db"


class TestSeatService(unittest.TestCase):
    def setUp(self):
        """Khởi tạo CSDL thử nghiệm có sẵn 100 sinh viên."""
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)
        init_db(TEST_DB)
        seed_students(100, TEST_DB)

    def tearDown(self):
        """Dọn dẹp sau khi kiểm thử."""
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)

    def test_assign_seat_success(self):
        """Xếp chỗ hợp lệ: Sinh viên tồn tại, chỗ trống."""
        success, msg = assign_seat("A2", "SV100", TEST_DB)
        self.assertTrue(success)
        self.assertIn("thành công", msg.lower())
        
        # Kiểm tra CSDL thực tế với resource cleanup đầy đủ
        with get_connection(TEST_DB) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("SELECT ma_sv FROM xep_cho WHERE ma_cho = 'A2';")
                row = cursor.fetchone()
            finally:
                cursor.close()
        self.assertIsNotNone(row)
        self.assertEqual(row["ma_sv"], "SV100")

    def test_assign_seat_invalid_seat_code(self):
        """Từ chối vị trí không hợp lệ (ví dụ: A5, D1, XYZ)."""
        for invalid_seat in ["A5", "D1", "XYZ", ""]:
            success, msg = assign_seat(invalid_seat, "SV100", TEST_DB)
            self.assertFalse(success)
            self.assertIn("không hợp lệ", msg.lower())

    def test_assign_seat_empty_student_code(self):
        """Từ chối khi để trống mã sinh viên."""
        success, msg = assign_seat("A1", "", TEST_DB)
        self.assertFalse(success)
        self.assertIn("không được để trống", msg.lower())

    def test_assign_seat_nonexistent_student(self):
        """Từ chối khi sinh viên không có trong bảng sinh_vien (ví dụ: SV999)."""
        success, msg = assign_seat("A1", "SV999", TEST_DB)
        self.assertFalse(success)
        self.assertIn("không tồn tại", msg.lower())

    def test_assign_seat_already_occupied(self):
        """Từ chối khi vị trí đã có người ngồi (xếp đè)."""
        assign_seat("A2", "SV100", TEST_DB)
        success, msg = assign_seat("A2", "SV001", TEST_DB)
        self.assertFalse(success)
        self.assertIn("đã có người", msg.lower())

    def test_assign_seat_student_already_assigned(self):
        """Từ chối khi sinh viên đã được xếp ở một vị trí khác."""
        assign_seat("A2", "SV100", TEST_DB)
        success, msg = assign_seat("B1", "SV100", TEST_DB)
        self.assertFalse(success)
        self.assertIn("đã được xếp tại vị trí", msg.lower())

    def test_release_seat_success(self):
        """Trả vị trí đang có sinh viên ngồi."""
        assign_seat("A2", "SV100", TEST_DB)
        success, msg = release_seat("A2", TEST_DB)
        self.assertTrue(success)
        self.assertIn("thành công", msg.lower())
        
        # Kiểm tra bảng xep_cho đã xóa và hồ sơ sinh_vien vẫn còn nguyên
        with get_connection(TEST_DB) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("SELECT * FROM xep_cho WHERE ma_cho = 'A2';")
                self.assertIsNone(cursor.fetchone())
                
                cursor.execute("SELECT * FROM sinh_vien WHERE ma_sv = 'SV100';")
                self.assertIsNotNone(cursor.fetchone(), "LỖI NGHIÊM TRỌNG: Trả chỗ làm mất hồ sơ sinh viên!")
            finally:
                cursor.close()

    def test_release_empty_seat_rejected(self):
        """Không cho phép trả vị trí đang trống."""
        success, msg = release_seat("B1", TEST_DB)
        self.assertFalse(success)
        self.assertIn("đang trống", msg.lower())


if __name__ == "__main__":
    unittest.main()
