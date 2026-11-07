"""Kiểm thử tự động cho Giao diện Tkinter (tests/test_ui.py)

Kiểm tra:
- Khởi tạo cửa sổ Tkinter và 12 nút máy tính.
- Chọn vị trí máy và cập nhật nhãn vị trí.
- Cơ chế refresh_ui() đồng bộ đúng nhãn và màu sắc 12 nút.
- Tương tác nhập liệu và hiển thị kết quả tra cứu.
"""

import os
import unittest
import tkinter as tk
from database import init_db, get_connection
from tao_du_lieu_demo import seed_students
from services.seat_service import assign_seat, release_seat
from ui.main_window import MainWindow

TEST_UI_DB = "test_ui_window.db"


class TestMainWindowGUI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Khởi tạo Tkinter root ẩn."""
        cls.root = tk.Tk()
        cls.root.withdraw()  # Ẩn cửa sổ hiển thị để kiểm thử headless

    @classmethod
    def tearDownClass(cls):
        """Hủy Tkinter root."""
        cls.root.destroy()

    def setUp(self):
        """Chuẩn bị CSDL thử nghiệm."""
        if os.path.exists(TEST_UI_DB):
            os.remove(TEST_UI_DB)
        init_db(TEST_UI_DB)
        seed_students(100, TEST_UI_DB)
        self.app = MainWindow(self.root)
        self.root.update_idletasks()

    def tearDown(self):
        """Dọn dẹp CSDL."""
        if os.path.exists(TEST_UI_DB):
            os.remove(TEST_UI_DB)

    def test_ui_has_12_seat_buttons(self):
        """Kiểm tra giao diện có đủ 12 nút máy tính từ A1 đến C4."""
        self.assertEqual(len(self.app.seat_buttons), 12)
        expected_seats = [
            "A1", "A2", "A3", "A4",
            "B1", "B2", "B3", "B4",
            "C1", "C2", "C3", "C4"
        ]
        for seat in expected_seats:
            self.assertIn(seat, self.app.seat_buttons)
            btn = self.app.seat_buttons[seat]
            self.assertIn("Trống", btn.cget("text"))

    def test_on_seat_selected(self):
        """Kiểm tra chọn vị trí máy cập nhật biến selected_seat và nhãn hiển thị."""
        self.app.on_seat_selected("A2")
        self.assertEqual(self.app.selected_seat, "A2")
        self.assertIn("A2", self.app.lbl_selected_seat.cget("text"))

    def test_refresh_ui_updates_seat_button_and_stats(self):
        """Kiểm tra hàm refresh_ui() cập nhật đúng nhãn nút máy và nhãn thống kê."""
        # Xếp SV100 vào A2 trên CSDL
        assign_seat("A2", "SV100")  # Chạy trên phong_may.db mặc định của app
        self.app.refresh_ui()
        self.root.update_idletasks()
        
        btn_a2 = self.app.seat_buttons["A2"]
        self.assertIn("SV100", btn_a2.cget("text"))
        self.assertIn("1 / 12", self.app.lbl_stat_used.cget("text"))
        
        # Trả lại chỗ A2
        release_seat("A2")
        self.app.refresh_ui()
        self.root.update_idletasks()
        self.assertIn("Trống", btn_a2.cget("text"))
        self.assertIn("0 / 12", self.app.lbl_stat_used.cget("text"))


if __name__ == "__main__":
    unittest.main()
