"""
Module kiểm thử tự động (Automated Test Suite) phụ trách bởi Thành viên 5.
Kiểm tra đầy đủ 5 kịch bản kiểm thử (TC1 -> TC5) theo Đặc tả Yêu cầu Dự án.
Cách chạy:
    python -m unittest discover -s tests -v
hoặc:
    python tests/test_phong_may.py
"""

import os
import sqlite3
import sys
import tkinter as tk
import unittest

# Đảm bảo import được các package ở thư mục gốc B-I-T-P-NH-M
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from controllers.phong_may_controller import PhongMayController
from models.phong_may_model import PhongMayModel
from tao_du_lieu_demo import DB_PATH, khoi_tao_du_lieu
from views.phong_may_view import PhongMayView


class TestUngDungPhongMay(unittest.TestCase):
    """Bộ kiểm thử 5 kịch bản (TC1 -> TC5) cho Ứng dụng Xếp chỗ Phòng máy."""

    @classmethod
    def setUpClass(cls) -> None:
        """Khởi tạo CSDL và làm sạch bảng xep_cho trước khi bắt đầu bộ test."""
        khoi_tao_du_lieu(DB_PATH)
        cls._xoa_tat_ca_xep_cho()

    @classmethod
    def tearDownClass(cls) -> None:
        """Đưa bảng xep_cho về trạng thái ban đầu (12 chỗ trống) sau khi test xong."""
        cls._xoa_tat_ca_xep_cho()

    @staticmethod
    def _xoa_tat_ca_xep_cho() -> None:
        conn = sqlite3.connect(DB_PATH)
        try:
            conn.execute("DELETE FROM xep_cho")
            conn.commit()
        finally:
            conn.close()

    def _tao_ung_dung(self) -> tuple[tk.Tk, PhongMayModel, PhongMayView, PhongMayController]:
        root = tk.Tk()
        root.withdraw()  # Ẩn cửa sổ khi chạy kiểm thử tự động
        model = PhongMayModel(DB_PATH)
        view = PhongMayView(root)
        controller = PhongMayController(model=model, view=view)
        return root, model, view, controller

    def test_tc1_khoi_tao_du_lieu_hai_lan_lien_tiep(self) -> None:
        """TC1: Chạy khởi tạo dữ liệu 2 lần liên tiếp, giữ nguyên 100 hồ sơ, không lỗi."""
        so_sv_lan_1, _ = khoi_tao_du_lieu(DB_PATH)
        so_sv_lan_2, _ = khoi_tao_du_lieu(DB_PATH)

        self.assertEqual(so_sv_lan_1, 100)
        self.assertEqual(so_sv_lan_2, 100)

    def test_tc2_xep_cho_hop_le(self) -> None:
        """TC2: Chọn ghế A2, nhập SV100, bấm [Xếp chỗ] -> A2 - SV100, bộ đếm 1/12."""
        self._xoa_tat_ca_xep_cho()
        root, _, view, ctrl = self._tao_ung_dung()
        try:
            ctrl.chon_ghe("A2")
            view.xoa_o_nhap_sv()
            view.entry_ma_sv.insert(0, "SV100")
            ctrl.xep_cho()

            self.assertEqual(view.nut_ghe["A2"].cget("text"), "A2 - SV100")
            self.assertIn("Sinh viên 100", view.lbl_thong_bao.cget("text"))
            self.assertEqual(
                view.lbl_bo_dem.cget("text"), "Số chỗ đã sử dụng: 1/12"
            )
        finally:
            root.destroy()

    def test_tc3_rang_buoc_xep_cho(self) -> None:
        """TC3: Kiểm tra lỗi khi ghế đã có người (A2) và khi SV đã có chỗ khác (SV100 -> B1)."""
        root, _, view, ctrl = self._tao_ung_dung()
        try:
            # 1. Thử xếp SV001 vào A2 (đang có SV100)
            ctrl.chon_ghe("A2")
            view.xoa_o_nhap_sv()
            view.entry_ma_sv.insert(0, "SV001")
            ctrl.xep_cho()

            self.assertEqual(
                view.lbl_thong_bao.cget("text"), "Chỗ A2 đã có người ngồi!"
            )
            self.assertEqual(view.nut_ghe["A2"].cget("text"), "A2 - SV100")

            # 2. Thử xếp SV100 vào B1 (SV100 đã ngồi ở A2)
            ctrl.chon_ghe("B1")
            view.xoa_o_nhap_sv()
            view.entry_ma_sv.insert(0, "SV100")
            ctrl.xep_cho()

            self.assertEqual(
                view.lbl_thong_bao.cget("text"),
                "Sinh viên SV100 đã được xếp ở một vị trí khác!",
            )
            self.assertEqual(view.nut_ghe["B1"].cget("text"), "B1 - Trống")
        finally:
            root.destroy()

    def test_tc4_luu_tru_trang_thai_khi_mo_lai_app(self) -> None:
        """TC4: Đóng ứng dụng hoàn toàn và mở lại -> A2 vẫn là SV100, bộ đếm giữ 1/12."""
        root, _, view, _ = self._tao_ung_dung()
        try:
            self.assertEqual(view.nut_ghe["A2"].cget("text"), "A2 - SV100")
            self.assertEqual(
                view.lbl_bo_dem.cget("text"), "Số chỗ đã sử dụng: 1/12"
            )
        finally:
            root.destroy()

    def test_tc5_tra_cho_va_cap_nhat_tra_cuu(self) -> None:
        """TC5: Chọn A2 bấm [Trả chỗ] -> Bộ đếm về 0/12, tra cứu SV100 báo chưa xếp chỗ."""
        root, _, view, ctrl = self._tao_ung_dung()
        try:
            # 1. Chọn A2 và bấm [Trả chỗ]
            ctrl.chon_ghe("A2")
            ctrl.tra_cho()

            self.assertEqual(view.nut_ghe["A2"].cget("text"), "A2 - Trống")
            self.assertEqual(
                view.lbl_bo_dem.cget("text"), "Số chỗ đã sử dụng: 0/12"
            )

            # 2. Tra cứu lại SV100
            view.xoa_o_nhap_sv()
            view.entry_ma_sv.insert(0, "SV100")
            ctrl.tra_cuu()

            self.assertIn(
                "Chưa được xếp chỗ", view.lbl_thong_bao.cget("text")
            )
        finally:
            root.destroy()


if __name__ == "__main__":
    unittest.main(verbosity=2)
