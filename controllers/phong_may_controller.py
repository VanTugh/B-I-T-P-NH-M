import sqlite3
from models.phong_may_model import PhongMayModel
from views.phong_may_view import DANH_SACH_CHO, PhongMayView


class PhongMayController:
    """
    Controller (C trong MVC): Điều phối luồng sự kiện giữa PhongMayView và
    PhongMayModel, thực hiện kiểm tra hợp lệ (Validate) và cập nhật giao diện.
    """

    def __init__(self, model: PhongMayModel, view: PhongMayView) -> None:
        self.model = model
        self.view = view
        self.ghe_dang_chon: str | None = None
        self.trang_thai_ghe: dict[str, str | None] = {
            ma_cho: None for ma_cho in DANH_SACH_CHO
        }

        # Gắn các sự kiện trên View vào các phương thức xử lý của Controller
        self.view.gan_su_kien(
            on_chon_ghe=self.chon_ghe,
            on_xep_cho=self.xep_cho,
            on_tra_cho=self.tra_cho,
            on_tra_cuu=self.tra_cuu,
        )

        # Nạp dữ liệu ban đầu từ CSDL lên giao diện
        self.load_data_to_gui()

    def load_data_to_gui(self) -> None:
        """Lấy dữ liệu từ Model và yêu cầu View cập nhật sơ đồ cùng bộ đếm."""
        du_lieu = self.model.lay_danh_sach_xep_cho()
        for ma_cho in DANH_SACH_CHO:
            self.trang_thai_ghe[ma_cho] = du_lieu.get(ma_cho)
        self.view.cap_nhat_so_do(du_lieu, self.ghe_dang_chon)

    def chon_ghe(self, ma_cho: str) -> None:
        """Xử lý khi người dùng click chọn một ghế trên sơ đồ."""
        self.ghe_dang_chon = ma_cho
        self.view.cap_nhat_nhan_ghe_chon(ma_cho)
        self.load_data_to_gui()

        ma_sv_dang_ngoi = self.trang_thai_ghe.get(ma_cho)
        if ma_sv_dang_ngoi:
            ho_ten = self.model.lay_ho_ten_sv(ma_sv_dang_ngoi) or ""
            self.view.hien_thi_thong_bao(
                f"Đã chọn ghế {ma_cho} (Đang có: {ma_sv_dang_ngoi} - {ho_ten}).\n"
                f"Bấm [Trả chỗ] nếu muốn hủy chỗ ngồi này.",
                la_loi=False,
            )
        else:
            self.view.hien_thi_thong_bao(
                f"Đã chọn ghế {ma_cho} (Trống).\n"
                f"Nhập mã sinh viên và bấm [Xếp chỗ] để gán vị trí.",
                la_loi=False,
            )

    def xep_cho(self) -> None:
        """Xử lý chức năng [Xếp chỗ] với đầy đủ 3 bước kiểm tra hợp lệ (Validate)."""
        if not self.ghe_dang_chon:
            self.view.hien_thi_thong_bao(
                "Vui lòng chọn một chỗ ngồi trên sơ đồ!", la_loi=True
            )
            return

        ma_cho = self.ghe_dang_chon
        ma_sv = self.view.lay_ma_sv_nhap()

        if not ma_sv:
            self.view.hien_thi_thong_bao(
                "Vui lòng nhập mã sinh viên!", la_loi=True
            )
            return

        # Validate 1: Kiểm tra ghế được chọn có đang trống không
        if self.model.lay_sv_tai_ghe(ma_cho) is not None:
            self.view.hien_thi_thong_bao(
                f"Chỗ {ma_cho} đã có người ngồi!", la_loi=True
            )
            return

        # Validate 2: Kiểm tra mã SV có tồn tại trong bảng sinh_vien không
        ho_ten = self.model.lay_ho_ten_sv(ma_sv)
        if ho_ten is None:
            self.view.hien_thi_thong_bao(
                "Mã sinh viên không tồn tại trong cơ sở dữ liệu!",
                la_loi=True,
            )
            return

        # Validate 3: Thêm vào bảng xep_cho và bắt lỗi UNIQUE (IntegrityError)
        try:
            self.model.them_xep_cho(ma_cho, ma_sv)
        except sqlite3.IntegrityError:
            self.view.hien_thi_thong_bao(
                f"Sinh viên {ma_sv} đã được xếp ở một vị trí khác!",
                la_loi=True,
            )
            return

        # Cập nhật lại giao diện, xóa trắng ô nhập và thông báo thành công
        self.load_data_to_gui()
        self.view.xoa_o_nhap_sv()
        self.view.hien_thi_thong_bao(
            f"Xếp chỗ thành công!\nHọ tên: {ho_ten} ({ma_sv}) - Đang ngồi: {ma_cho}",
            la_loi=False,
        )

    def tra_cho(self) -> None:
        """
        Xử lý chức năng [Trả chỗ]:
        - Cách 1: Click trực tiếp vào ghế đang có người trên sơ đồ -> bấm [Trả chỗ].
        - Cách 2 (Optional): Nhập mã SV vào ô nhập liệu -> bấm [Trả chỗ].
        """
        ma_sv_nhap = self.view.lay_ma_sv_nhap()

        # Ưu tiên Cách 1: Trả chỗ theo ghế đang chọn trên sơ đồ
        if self.ghe_dang_chon:
            ma_sv_tai_ghe = self.model.lay_sv_tai_ghe(self.ghe_dang_chon)
            if ma_sv_tai_ghe is not None:
                ma_cho_xoa = self.ghe_dang_chon
                self.model.xoa_xep_cho(ma_cho_xoa)
                self.load_data_to_gui()
                self.view.hien_thi_thong_bao(
                    f"Đã trả chỗ {ma_cho_xoa} (Sinh viên {ma_sv_tai_ghe}) thành công!",
                    la_loi=False,
                )
                return

        # Hỗ trợ Cách 2: Trả chỗ theo mã sinh viên nhập trong ô Entry
        if ma_sv_nhap:
            ma_cho_cua_sv = self.model.lay_ghe_cua_sv(ma_sv_nhap)
            if ma_cho_cua_sv is not None:
                self.model.xoa_xep_cho(ma_cho_cua_sv)
                self.load_data_to_gui()
                self.view.xoa_o_nhap_sv()
                self.view.hien_thi_thong_bao(
                    f"Đã trả chỗ {ma_cho_cua_sv} của sinh viên {ma_sv_nhap} thành công!",
                    la_loi=False,
                )
                return

        # Báo lỗi cụ thể nếu không trả chỗ được
        if not self.ghe_dang_chon and not ma_sv_nhap:
            self.view.hien_thi_thong_bao(
                "Vui lòng chọn một chỗ ngồi trên sơ đồ!", la_loi=True
            )
        elif self.ghe_dang_chon:
            self.view.hien_thi_thong_bao(
                f"Chỗ {self.ghe_dang_chon} hiện đang trống, không thể trả chỗ!",
                la_loi=True,
            )
        else:
            self.view.hien_thi_thong_bao(
                f"Sinh viên {ma_sv_nhap} hiện chưa được xếp chỗ!",
                la_loi=True,
            )

    def tra_cuu(self) -> None:
        """Xử lý chức năng [Tra cứu] sinh viên theo mã SV."""
        ma_sv = self.view.lay_ma_sv_nhap()
        if not ma_sv:
            self.view.hien_thi_thong_bao(
                "Vui lòng nhập mã sinh viên cần tra cứu!", la_loi=True
            )
            return

        ket_qua = self.model.tra_cuu_sinh_vien(ma_sv)
        if ket_qua is None:
            self.view.hien_thi_thong_bao(
                "Mã sinh viên không tồn tại trong cơ sở dữ liệu!", la_loi=True
            )
            return

        ho_ten, ma_cho = ket_qua
        if ma_cho:
            self.ghe_dang_chon = ma_cho
            self.view.cap_nhat_nhan_ghe_chon(ma_cho)
            self.load_data_to_gui()
            self.view.hien_thi_thong_bao(
                f"Họ tên: {ho_ten} - Đang ngồi: {ma_cho}", la_loi=False
            )
        else:
            self.view.hien_thi_thong_bao(
                f"Họ tên: {ho_ten} - Chưa được xếp chỗ", la_loi=False
            )
