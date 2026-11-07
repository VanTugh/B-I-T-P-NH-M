"""Kiểm thử đơn vị cho Module Tra cứu sinh viên và Thống kê (tests/test_student_service.py)

Kiểm tra:
- find_student(): Phân biệt rõ 3 trường hợp:
  1. Mã SV không tồn tại (trả về None).
  2. SV tồn tại nhưng chưa xếp chỗ (ma_cho = None).
  3. SV đã được xếp chỗ (ma_cho có giá trị).
- get_room_statistics(): Số liệu thống kê phòng máy.
"""

import os
import unittest
from database import init_db
from tao_du_lieu_demo import seed_students
from services.seat_service import assign_seat
from services.student_service import find_student, get_room_statistics

TEST_DB = "test_student_service.db"


class TestStudentService(unittest.TestCase):
    def setUp(self):
        """Khởi tạo CSDL thử nghiệm có sẵn 100 sinh viên."""
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)
        init_db(TEST_DB)
        seed_students(100, TEST_DB)

    def tearDown(self):
        """Dọn dẹp tệp thử nghiệm."""
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)

    def test_find_student_nonexistent(self):
        """Tra cứu mã sinh viên không tồn tại -> Bắt buộc trả về None."""
        res = find_student("SV999", TEST_DB)
        self.assertIsNone(res)
        
        res_empty = find_student("", TEST_DB)
        self.assertIsNone(res_empty)

    def test_find_student_not_assigned(self):
        """Sinh viên có tồn tại nhưng chưa được xếp chỗ -> ma_cho = None."""
        res = find_student("SV100", TEST_DB)
        self.assertIsNotNone(res)
        self.assertEqual(res["ma_sv"], "SV100")
        self.assertEqual(res["ho_ten"], "Sinh viên 100")
        self.assertIsNone(res["ma_cho"], "Sinh viên chưa xếp chỗ thì ma_cho phải là None!")

    def test_find_student_assigned(self):
        """Sinh viên đã được xếp chỗ -> ma_cho bằng đúng mã vị trí."""
        assign_seat("A2", "SV100", TEST_DB)
        res = find_student("SV100", TEST_DB)
        self.assertIsNotNone(res)
        self.assertEqual(res["ma_sv"], "SV100")
        self.assertEqual(res["ma_cho"], "A2")

    def test_get_room_statistics(self):
        """Kiểm tra tính toán số liệu thống kê phòng máy."""
        stats_initial = get_room_statistics(TEST_DB)
        self.assertEqual(stats_initial["total"], 12)
        self.assertEqual(stats_initial["used"], 0)
        self.assertEqual(stats_initial["available"], 12)
        self.assertEqual(stats_initial["usage_rate"], 0.0)
        
        # Xếp 1 sinh viên vào vị trí A2
        assign_seat("A2", "SV100", TEST_DB)
        stats_after = get_room_statistics(TEST_DB)
        self.assertEqual(stats_after["used"], 1)
        self.assertEqual(stats_after["available"], 11)
        self.assertAlmostEqual(stats_after["usage_rate"], round(1 / 12 * 100, 1))


if __name__ == "__main__":
    unittest.main()
