"""Kiểm thử chuyên sâu vòng đời Connection và Cursor SQLite (tests/test_connection_lifecycle.py)

Dự án: Quản lý phòng máy tính 12 vị trí (3 hàng x 4 cột).
Mục đích kiểm thử:
1. Xác nhận get_connection() giải phóng hoàn toàn connection (gọi close()) khi kết thúc khối with.
2. Xác nhận cơ chế commit tự động khi thành công và rollback khi gặp ngoại lệ.
3. Kiểm tra kiểm chứng Mock (unittest.mock.patch) đối với sqlite3.connect().
4. Kiểm tra Windows File Lock: Mở DB, thực thi truy vấn, thoát khối with, và xóa file ngay lập tức.
   Trên Windows, nếu connection bị rò rỉ (leak), os.remove() sẽ ném WinError 32 (file lock).
   Nếu xóa file thành công chứng minh connection đã được đóng 100%.
5. Kiểm tra chịu tải liên tục (Stress Test): Thực hiện 50 lần xếp/trả chỗ và 100 lần tra cứu liên tiếp
   để chứng minh không xảy ra lỗi "database is locked" hay rò rỉ tài nguyên.
"""

import os
import sys
import unittest
from unittest.mock import MagicMock, patch
import sqlite3

# Đảm bảo in ký tự Unicode không bị lỗi bảng mã trên console Windows
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from database import init_db, get_connection, get_seat_map, get_seat_stats
from tao_du_lieu_demo import seed_students
from services.seat_service import assign_seat, release_seat
from services.student_service import find_student, get_room_statistics


TEST_LIFECYCLE_DB = "test_lifecycle_leak.db"
TEST_STRESS_DB = "test_stress_leak.db"


class TestConnectionLifecycle(unittest.TestCase):
    """Kiểm thử vòng đời SQLite Connection và Cursor."""

    def tearDown(self):
        """Dọn dẹp file thử nghiệm nếu còn tồn tại."""
        for db_file in [TEST_LIFECYCLE_DB, TEST_STRESS_DB]:
            if os.path.exists(db_file):
                try:
                    os.remove(db_file)
                except PermissionError:
                    pass

    def test_mock_connection_lifecycle_success(self):
        """Kiểm chứng Mock: get_connection() tự động commit() và close() khi thành công."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor

        with patch("sqlite3.connect", return_value=mock_conn) as mock_connect:
            with get_connection("mock_db.db") as conn:
                self.assertEqual(conn, mock_conn)
                mock_cursor.execute("SELECT 1")

            # Kiểm tra: PRAGMA foreign_keys = ON phải được gọi
            mock_conn.execute.assert_called_with("PRAGMA foreign_keys = ON;")
            # Kiểm tra: commit() phải được gọi khi thoát bình thường
            mock_conn.commit.assert_called_once()
            # Kiểm tra: close() phải luôn được gọi khi kết thúc context
            mock_conn.close.assert_called_once()
            # Kiểm tra: rollback() KHÔNG được gọi khi thành công
            mock_conn.rollback.assert_not_called()

    def test_mock_connection_lifecycle_exception_rollback(self):
        """Kiểm chứng Mock: get_connection() tự động rollback() và close() khi có ngoại lệ."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor

        with patch("sqlite3.connect", return_value=mock_conn) as mock_connect:
            with self.assertRaises(RuntimeError):
                with get_connection("mock_db.db") as conn:
                    raise RuntimeError("Lỗi mô phỏng trong nghiệp vụ")

            # Kiểm tra: rollback() phải được gọi khi có ngoại lệ
            mock_conn.rollback.assert_called_once()
            # Kiểm tra: close() vẫn phải được gọi trong finally
            mock_conn.close.assert_called_once()
            # Kiểm tra: commit() KHÔNG được gọi khi có lỗi
            mock_conn.commit.assert_not_called()

    def test_real_windows_file_lock_release(self):
        """Kiểm tra thực tế Windows File Lock: Connection đóng hoàn toàn cho phép xóa file tức thì.
        
        Trên hệ điều hành Windows, SQLite giữ khóa độc quyền (file handle) trên tệp .db.
        Nếu connection bị rò rỉ (chưa gọi conn.close()), lệnh os.remove(db_file)
        chắc chắn sẽ ném ngoại lệ PermissionError: [WinError 32].
        """
        if os.path.exists(TEST_LIFECYCLE_DB):
            os.remove(TEST_LIFECYCLE_DB)

        # 1. Khởi tạo DB
        init_db(TEST_LIFECYCLE_DB)
        seed_students(10, TEST_LIFECYCLE_DB)

        # 2. Sử dụng get_connection thực hiện truy vấn
        with get_connection(TEST_LIFECYCLE_DB) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("SELECT COUNT(*) FROM sinh_vien")
                count = cursor.fetchone()[0]
                self.assertEqual(count, 10)
            finally:
                cursor.close()

        # 3. Ngay sau khi thoát khỏi khối with, connection phải đã được đóng
        # Thử xóa file ngay lập tức - nếu connection chưa đóng, dòng này sẽ văng PermissionError
        try:
            os.remove(TEST_LIFECYCLE_DB)
            file_deleted = True
        except PermissionError:
            file_deleted = False

        self.assertTrue(
            file_deleted,
            "LỖI CONNECTION LEAK: Không thể xóa file DB trên Windows vì connection chưa được đóng!"
        )

    def test_cursor_explicit_close(self):
        """Kiểm tra con trỏ cursor được đóng sau khi sử dụng trong get_connection."""
        if os.path.exists(TEST_LIFECYCLE_DB):
            os.remove(TEST_LIFECYCLE_DB)

        init_db(TEST_LIFECYCLE_DB)
        with get_connection(TEST_LIFECYCLE_DB) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("SELECT 1")
            finally:
                cursor.close()
            # Khi cursor đã đóng, gọi execute lại sẽ gây lỗi ProgrammingError trong sqlite3
            with self.assertRaises(sqlite3.ProgrammingError):
                cursor.execute("SELECT 2")

    def test_stress_consecutive_assign_release_no_leak_or_lock(self):
        """Stress Test: 50 chu kỳ xếp chỗ và trả chỗ liên tiếp không bị khóa DB hay rò rỉ connection."""
        if os.path.exists(TEST_STRESS_DB):
            os.remove(TEST_STRESS_DB)

        init_db(TEST_STRESS_DB)
        seed_students(50, TEST_STRESS_DB)

        # Chạy 50 chu kỳ liên tục: Xếp SV001 vào A1 -> Trả chỗ A1
        for i in range(1, 51):
            sv_id = f"SV{i:03d}"
            # Xếp chỗ
            ok_assign, msg_assign = assign_seat("A1", sv_id, TEST_STRESS_DB)
            self.assertTrue(ok_assign, f"Lỗi ở vòng {i} khi xếp chỗ: {msg_assign}")

            # Kiểm tra trạng thái sơ đồ
            smap = get_seat_map(TEST_STRESS_DB)
            self.assertEqual(smap["A1"], sv_id)

            # Trả chỗ
            ok_rel, msg_rel = release_seat("A1", TEST_STRESS_DB)
            self.assertTrue(ok_rel, f"Lỗi ở vòng {i} khi trả chỗ: {msg_rel}")

            # Kiểm tra lại sơ đồ
            smap = get_seat_map(TEST_STRESS_DB)
            self.assertIsNone(smap["A1"])

        # Kiểm tra thống kê cuối cùng
        stats = get_room_statistics(TEST_STRESS_DB)
        self.assertEqual(stats["used"], 0)
        self.assertEqual(stats["available"], 12)

        # Xóa file DB thành công xác nhận không có connection nào bị treo sau 50 chu kỳ
        os.remove(TEST_STRESS_DB)
        self.assertFalse(os.path.exists(TEST_STRESS_DB))

    def test_stress_consecutive_queries_no_leak(self):
        """Stress Test: 100 lần tra cứu sinh viên liên tiếp giải phóng tài nguyên triệt để."""
        if os.path.exists(TEST_STRESS_DB):
            os.remove(TEST_STRESS_DB)

        init_db(TEST_STRESS_DB)
        seed_students(100, TEST_STRESS_DB)

        for i in range(1, 101):
            sv_id = f"SV{i:03d}"
            info = find_student(sv_id, TEST_STRESS_DB)
            self.assertIsNotNone(info)
            self.assertEqual(info["ma_sv"], sv_id)

        # Tra cứu 20 mã không tồn tại
        for i in range(101, 121):
            sv_id = f"SV{i:03d}"
            info = find_student(sv_id, TEST_STRESS_DB)
            self.assertIsNone(info)

        # Đóng và xóa file ngay lập tức
        os.remove(TEST_STRESS_DB)
        self.assertFalse(os.path.exists(TEST_STRESS_DB))


if __name__ == "__main__":
    unittest.main()
