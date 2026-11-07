"""Bộ kiểm thử kịch bản bắt buộc (TC01 - TC09 + Mở rộng) (tests/test_scenarios.py)

Dự án: Quản lý phòng máy tính 12 vị trí (3 hàng x 4 cột).
Trách nhiệm:
- Trực tiếp chạy và thẩm định toàn bộ 9 ca kiểm thử bắt buộc (TC01 đến TC09).
- Kiểm tra các ca biên: mã SV không tồn tại, vị trí sai, trả chỗ trống, phòng đầy, ràng buộc CSDL.
"""

import os
import sys
import unittest
import sqlite3

# Đảm bảo in ký tự Unicode không bị lỗi bảng mã trên console Windows
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
from database import init_db, get_connection, get_seat_stats, get_seat_map, VALID_SEATS
from tao_du_lieu_demo import seed_students
from services.seat_service import assign_seat, release_seat
from services.student_service import find_student, get_room_statistics

SCENARIOS_DB = "test_scenarios_phong_may.db"


class TestMandatoryScenarios(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Khởi tạo trước toàn bộ kịch bản."""
        if os.path.exists(SCENARIOS_DB):
            os.remove(SCENARIOS_DB)

    @classmethod
    def tearDownClass(cls):
        """Dọn dẹp sau khi chạy toàn bộ kịch bản."""
        if os.path.exists(SCENARIOS_DB):
            os.remove(SCENARIOS_DB)

    def test_01_TC01_seed_first_time(self):
        """TC01: Chạy seed lần đầu -> Có ít nhất 100 sinh viên."""
        total = seed_students(100, SCENARIOS_DB)
        self.assertGreaterEqual(total, 100)
        self.assertEqual(total, 100)
        print("\n[TC01 - PASS] Chạy seed lần đầu thành công: 100 sinh viên.")

    def test_02_TC02_seed_second_time(self):
        """TC02: Chạy seed lần thứ hai -> Không tăng số lượng sinh viên."""
        total_before = seed_students(100, SCENARIOS_DB)
        total_after = seed_students(100, SCENARIOS_DB)
        self.assertEqual(total_before, total_after, "Lỗi: Số lượng sinh viên bị tăng lên!")
        self.assertEqual(total_after, 100)
        print("[TC02 - PASS] Chạy seed lần thứ hai an toàn: Số lượng vẫn là 100 sinh viên.")

    def test_03_TC03_search_sv100_before_assign(self):
        """TC03: Tra cứu SV100 -> Hiển thị đúng thông tin, trạng thái chưa xếp."""
        res = find_student("SV100", SCENARIOS_DB)
        self.assertIsNotNone(res)
        self.assertEqual(res["ma_sv"], "SV100")
        self.assertEqual(res["ho_ten"], "Sinh viên 100")
        self.assertIsNone(res["ma_cho"], "SV100 chưa xếp chỗ thì ma_cho phải là None!")
        print("[TC03 - PASS] Tra cứu SV100 chính xác: Hồ sơ 'Sinh viên 100', trạng thái chưa xếp chỗ.")

    def test_04_TC04_assign_sv100_to_a2(self):
        """TC04: Xếp SV100 vào A2 -> Thành công, thống kê 1/12."""
        success, msg = assign_seat("A2", "SV100", SCENARIOS_DB)
        self.assertTrue(success, f"Xếp SV100 vào A2 thất bại: {msg}")
        
        stats = get_room_statistics(SCENARIOS_DB)
        self.assertEqual(stats["used"], 1)
        self.assertEqual(stats["total"], 12)
        self.assertEqual(stats["available"], 11)
        print("[TC04 - PASS] Xếp SV100 vào A2 thành công. Bộ đếm cập nhật chuẩn: 1/12.")

    def test_05_TC05_assign_sv001_to_a2_rejected(self):
        """TC05: Xếp SV001 vào A2 -> Từ chối vì vị trí A2 đã có người."""
        success, msg = assign_seat("A2", "SV001", SCENARIOS_DB)
        self.assertFalse(success, "Lỗi: Hệ thống cho phép xếp đè vào chỗ đã có người!")
        self.assertIn("đã có người", msg.lower())
        
        # Đảm bảo A2 vẫn thuộc về SV100
        seat_map = get_seat_map(SCENARIOS_DB)
        self.assertEqual(seat_map["A2"], "SV100")
        print("[TC05 - PASS] Từ chối xếp SV001 vào A2 chuẩn xác: Vị trí A2 vẫn thuộc về SV100.")

    def test_06_TC06_assign_sv100_to_b1_rejected(self):
        """TC06: Xếp SV100 vào B1 -> Từ chối vì SV100 đã được xếp ở A2."""
        success, msg = assign_seat("B1", "SV100", SCENARIOS_DB)
        self.assertFalse(success, "Lỗi: Hệ thống cho phép một sinh viên ngồi 2 chỗ!")
        self.assertIn("đã được xếp tại vị trí", msg.lower())
        
        # Đảm bảo B1 vẫn trống
        seat_map = get_seat_map(SCENARIOS_DB)
        self.assertIsNone(seat_map["B1"])
        print("[TC06 - PASS] Từ chối xếp SV100 sang B1 chuẩn xác: SV100 chỉ ngồi 1 chỗ tại A2.")

    def test_07_TC07_persistence_after_restart(self):
        """TC07: Đóng và mở lại ứng dụng -> A2 vẫn có SV100, thống kê 1/12."""
        # Giả lập đóng ứng dụng (không giữ connection) và khởi tạo lại
        init_db(SCENARIOS_DB)
        seed_students(100, SCENARIOS_DB)
        
        stats = get_room_statistics(SCENARIOS_DB)
        seat_map = get_seat_map(SCENARIOS_DB)
        
        self.assertEqual(seat_map["A2"], "SV100", "Lỗi: Mất dữ liệu xếp chỗ A2 sau khi mở lại!")
        self.assertEqual(stats["used"], 1)
        self.assertEqual(stats["total"], 12)
        print("[TC07 - PASS] Đóng và mở lại ứng dụng: Dữ liệu SQLite bền vững, A2 vẫn là SV100, bộ đếm 1/12.")

    def test_08_TC08_release_seat_a2(self):
        """TC08: Trả chỗ A2 -> Thành công, thống kê 0/12."""
        success, msg = release_seat("A2", SCENARIOS_DB)
        self.assertTrue(success, f"Trả chỗ A2 thất bại: {msg}")
        
        stats = get_room_statistics(SCENARIOS_DB)
        seat_map = get_seat_map(SCENARIOS_DB)
        
        self.assertIsNone(seat_map["A2"])
        self.assertEqual(stats["used"], 0)
        self.assertEqual(stats["available"], 12)
        print("[TC08 - PASS] Trả chỗ A2 thành công. Vị trí A2 trở về trống, bộ đếm cập nhật: 0/12.")

    def test_09_TC09_search_sv100_after_release(self):
        """TC09: Tra cứu lại SV100 -> Sinh viên vẫn tồn tại nhưng chưa có vị trí."""
        res = find_student("SV100", SCENARIOS_DB)
        self.assertIsNotNone(res, "LỖI NGHIÊM TRỌNG: Hồ sơ SV100 đã bị xóa khỏi sinh_vien!")
        self.assertEqual(res["ma_sv"], "SV100")
        self.assertEqual(res["ho_ten"], "Sinh viên 100")
        self.assertIsNone(res["ma_cho"], "SV100 sau khi trả chỗ phải có ma_cho = None!")
        print("[TC09 - PASS] Tra cứu lại SV100: Hồ sơ được bảo toàn trọn vẹn, trạng thái trở về chưa xếp chỗ.")

    def test_10_extra_edge_cases(self):
        """Kiểm tra mở rộng: Mã SV không tồn tại, Vị trí máy sai, Trả chỗ trống, Phòng đầy 12/12."""
        # 1. Mã SV không tồn tại
        self.assertIsNone(find_student("SV999", SCENARIOS_DB))
        ok, msg = assign_seat("A1", "SV999", SCENARIOS_DB)
        self.assertFalse(ok)
        
        # 2. Vị trí không hợp lệ
        ok, msg = assign_seat("Z9", "SV001", SCENARIOS_DB)
        self.assertFalse(ok)
        
        # 3. Trả chỗ trống
        ok, msg = release_seat("C4", SCENARIOS_DB)
        self.assertFalse(ok)
        
        # 4. Xếp kín phòng 12 chỗ (A1-A4, B1-B4, C1-C4)
        for i, seat in enumerate(VALID_SEATS, start=1):
            sv = f"SV{i:03d}"
            ok, _ = assign_seat(seat, sv, SCENARIOS_DB)
            self.assertTrue(ok)
            
        stats_full = get_room_statistics(SCENARIOS_DB)
        self.assertEqual(stats_full["used"], 12)
        self.assertEqual(stats_full["available"], 0)
        self.assertEqual(stats_full["usage_rate"], 100.0)
        
        # Thử xếp sinh viên thứ 13 vào bất kỳ chỗ nào -> Bắt buộc từ chối
        ok, msg = assign_seat("A1", "SV013", SCENARIOS_DB)
        self.assertFalse(ok)
        
        # Trả lại 12 chỗ
        for seat in VALID_SEATS:
            release_seat(seat, SCENARIOS_DB)
        self.assertEqual(get_room_statistics(SCENARIOS_DB)["used"], 0)
        print("[TC-EXTRA - PASS] Đạt toàn bộ kiểm thử biên: SV999, Z9, Trả chỗ trống, Phòng đầy 12/12 máy.")


if __name__ == "__main__":
    unittest.main()
