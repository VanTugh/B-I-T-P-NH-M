from collections.abc import Callable
import tkinter as tk
from tkinter import font as tkfont

DANH_SACH_CHO = [
    f"{hang}{cot}" for hang in ("A", "B", "C") for cot in range(1, 5)
]

# Bảng màu theo đặc tả giao diện (UI/UX Specification)
MAU_TRONG = "#b9f6ca"         # Xanh lá nhạt (Light Green)
MAU_TRONG_ACTIVE = "#69f0ae"
MAU_CO_NGUOI = "#ff8a80"      # Đỏ nhạt (Light Coral)
MAU_CO_NGUOI_ACTIVE = "#ff5252"


class PhongMayView:
    """
    View (V trong MVC): Chịu trách nhiệm hiển thị toàn bộ giao diện Tkinter
    gồm Panel Trái (Sơ đồ 12 ghế 3x4) và Panel Phải (Điều khiển, Thông báo, Bộ đếm).
    """

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.nut_ghe: dict[str, tk.Button] = {}
        self._callback_chon_ghe: Callable[[str], None] | None = None

        self._thiet_lap_cua_so()
        self._xay_dung_giao_dien()

    def _thiet_lap_cua_so(self) -> None:
        self.root.title("Ứng dụng Xếp chỗ và Tra cứu Sinh viên Phòng máy")
        self.root.geometry("920x520")
        self.root.minsize(820, 480)
        self.root.configure(bg="#f5f7fa")

        # Cấu hình tỷ lệ 2 cột: Panel Trái ~60% (weight=3), Panel Phải ~40% (weight=2)
        self.root.columnconfigure(0, weight=3, uniform="panel")
        self.root.columnconfigure(1, weight=2, uniform="panel")
        self.root.rowconfigure(0, weight=1)

    def _xay_dung_giao_dien(self) -> None:
        font_tieu_de = tkfont.Font(family="Segoe UI", size=13, weight="bold")
        font_nut_ghe = tkfont.Font(family="Segoe UI", size=11, weight="bold")
        font_nhan = tkfont.Font(family="Segoe UI", size=10)
        font_nhan_dam = tkfont.Font(family="Segoe UI", size=10, weight="bold")
        font_bo_dem = tkfont.Font(family="Segoe UI", size=11, weight="bold")

        # =====================================================================
        # PANEL TRÁI (Khu vực Sơ đồ phòng máy - 60% chiều rộng)
        # =====================================================================
        self.frame_trai = tk.LabelFrame(
            self.root,
            text=" SƠ ĐỒ PHÒNG MÁY (3 HÀNG x 4 CỘT) ",
            font=font_tieu_de,
            bg="#ffffff",
            fg="#1a237e",
            padx=16,
            pady=16,
            bd=2,
            relief=tk.GROOVE,
        )
        self.frame_trai.grid(
            row=0, column=0, sticky="nsew", padx=(16, 8), pady=16
        )

        frame_luoi_ghe = tk.Frame(self.frame_trai, bg="#ffffff")
        frame_luoi_ghe.pack(expand=True, fill="both")

        cac_hang = ["A", "B", "C"]
        for r in range(3):
            frame_luoi_ghe.rowconfigure(r, weight=1)
            for c in range(4):
                frame_luoi_ghe.columnconfigure(c, weight=1)
                ma_cho = f"{cac_hang[r]}{c + 1}"
                btn = tk.Button(
                    frame_luoi_ghe,
                    text=f"{ma_cho} - Trống",
                    font=font_nut_ghe,
                    bg=MAU_TRONG,
                    activebackground=MAU_TRONG_ACTIVE,
                    fg="#1b5e20",
                    relief=tk.RAISED,
                    bd=2,
                    cursor="hand2",
                    command=lambda m=ma_cho: self._khi_click_ghe(m),
                )
                btn.grid(row=r, column=c, sticky="nsew", padx=8, pady=8)
                self.nut_ghe[ma_cho] = btn

        # Chú thích màu sắc bên dưới sơ đồ
        frame_chu_thich = tk.Frame(self.frame_trai, bg="#ffffff")
        frame_chu_thich.pack(fill="x", pady=(10, 0))

        tk.Label(
            frame_chu_thich,
            text="  Trống  ",
            bg=MAU_TRONG,
            fg="#1b5e20",
            font=font_nhan,
            bd=1,
            relief=tk.SOLID,
        ).pack(side="left", padx=(8, 12))

        tk.Label(
            frame_chu_thich,
            text="  Đã có người  ",
            bg=MAU_CO_NGUOI,
            fg="#b71c1c",
            font=font_nhan,
            bd=1,
            relief=tk.SOLID,
        ).pack(side="left")

        # =====================================================================
        # PANEL PHẢI (Khu vực Thao tác & Bộ đếm - 40% chiều rộng)
        # =====================================================================
        self.frame_phai = tk.LabelFrame(
            self.root,
            text=" BẢNG ĐIỀU KHIỂN & TRA CỨU ",
            font=font_tieu_de,
            bg="#ffffff",
            fg="#1a237e",
            padx=18,
            pady=16,
            bd=2,
            relief=tk.GROOVE,
        )
        self.frame_phai.grid(
            row=0, column=1, sticky="nsew", padx=(8, 16), pady=16
        )

        # 1. Label hiển thị Ghế đang chọn
        self.lbl_ghe_dang_chon = tk.Label(
            self.frame_phai,
            text="Đang chọn: Chưa chọn",
            font=tkfont.Font(family="Segoe UI", size=12, weight="bold"),
            bg="#e8eaf6",
            fg="#1a237e",
            pady=10,
            bd=1,
            relief=tk.SOLID,
        )
        self.lbl_ghe_dang_chon.pack(fill="x", pady=(4, 16))

        # 2. Ô nhập Mã sinh viên
        tk.Label(
            self.frame_phai,
            text="Mã sinh viên (VD: SV001 - SV100):",
            font=font_nhan_dam,
            bg="#ffffff",
            anchor="w",
        ).pack(fill="x")

        self.entry_ma_sv = tk.Entry(
            self.frame_phai,
            font=tkfont.Font(family="Segoe UI", size=12),
            bd=2,
            relief=tk.GROOVE,
        )
        self.entry_ma_sv.pack(fill="x", pady=(6, 16), ipady=5)

        # 3. Cụm các nút chức năng: Xếp chỗ, Trả chỗ, Tra cứu
        frame_nut = tk.Frame(self.frame_phai, bg="#ffffff")
        frame_nut.pack(fill="x", pady=(0, 16))
        frame_nut.columnconfigure(0, weight=1)
        frame_nut.columnconfigure(1, weight=1)
        frame_nut.columnconfigure(2, weight=1)

        self.btn_xep_cho = tk.Button(
            frame_nut,
            text="Xếp chỗ",
            font=font_nhan_dam,
            bg="#1976d2",  # Xanh dương (Blue)
            activebackground="#1565c0",
            fg="#ffffff",
            activeforeground="#ffffff",
            pady=8,
            cursor="hand2",
        )
        self.btn_xep_cho.grid(row=0, column=0, sticky="ew", padx=(0, 6))

        self.btn_tra_cho = tk.Button(
            frame_nut,
            text="Trả chỗ",
            font=font_nhan_dam,
            bg="#e65100",  # Cam/Đỏ (Orange/Red)
            activebackground="#bf360c",
            fg="#ffffff",
            activeforeground="#ffffff",
            pady=8,
            cursor="hand2",
        )
        self.btn_tra_cho.grid(row=0, column=1, sticky="ew", padx=3)

        self.btn_tra_cuu = tk.Button(
            frame_nut,
            text="Tra cứu",
            font=font_nhan_dam,
            bg="#e0e0e0",  # Xám nhạt (Light Gray)
            activebackground="#bdbdbd",
            fg="#212121",
            pady=8,
            cursor="hand2",
        )
        self.btn_tra_cuu.grid(row=0, column=2, sticky="ew", padx=(6, 0))

        # 4. Vùng hiển thị Thông báo / Kết quả (Multiline Label)
        tk.Label(
            self.frame_phai,
            text="Thông báo / Kết quả:",
            font=font_nhan_dam,
            bg="#ffffff",
            anchor="w",
        ).pack(fill="x")

        self.lbl_thong_bao = tk.Label(
            self.frame_phai,
            text="Sẵn sàng. Hãy chọn một ghế trên sơ đồ hoặc nhập mã SV để tra cứu.",
            font=font_nhan,
            bg="#fafafa",
            fg="#1b5e20",
            justify="left",
            anchor="nw",
            wraplength=290,
            padx=10,
            pady=10,
            bd=1,
            relief=tk.SUNKEN,
            height=5,
        )
        self.lbl_thong_bao.pack(fill="both", expand=True, pady=(6, 12))

        # 5. Bộ đếm góc dưới cùng
        self.lbl_bo_dem = tk.Label(
            self.frame_phai,
            text="Số chỗ đã sử dụng: 0/12",
            font=font_bo_dem,
            bg="#e3f2fd",
            fg="#0d47a1",
            pady=8,
            bd=1,
            relief=tk.SOLID,
        )
        self.lbl_bo_dem.pack(fill="x", side="bottom")

    # =========================================================================
    # CÁC PHƯƠNG THỨC GẮN SỰ KIỆN & CẬP NHẬT GIAO DIỆN TỪ CONTROLLER
    # =========================================================================

    def _khi_click_ghe(self, ma_cho: str) -> None:
        if self._callback_chon_ghe:
            self._callback_chon_ghe(ma_cho)

    def gan_su_kien(
        self,
        on_chon_ghe: Callable[[str], None],
        on_xep_cho: Callable[[], None],
        on_tra_cho: Callable[[], None],
        on_tra_cuu: Callable[[], None],
    ) -> None:
        """Gắn các hàm xử lý sự kiện từ Controller vào các nút bấm và ô nhập."""
        self._callback_chon_ghe = on_chon_ghe
        self.btn_xep_cho.config(command=on_xep_cho)
        self.btn_tra_cho.config(command=on_tra_cho)
        self.btn_tra_cuu.config(command=on_tra_cuu)
        self.entry_ma_sv.bind("<Return>", lambda _event: on_tra_cuu())

    def lay_ma_sv_nhap(self) -> str:
        """Lấy chuỗi mã sinh viên người dùng nhập (đã cắt khoảng trắng và viết hoa)."""
        return self.entry_ma_sv.get().strip().upper()

    def xoa_o_nhap_sv(self) -> None:
        """Xóa trắng ô nhập mã sinh viên."""
        self.entry_ma_sv.delete(0, tk.END)

    def cap_nhat_nhan_ghe_chon(self, ma_cho: str | None) -> None:
        """Cập nhật nhãn hiển thị ghế đang chọn."""
        if ma_cho:
            self.lbl_ghe_dang_chon.config(text=f"Đang chọn: {ma_cho}")
        else:
            self.lbl_ghe_dang_chon.config(text="Đang chọn: Chưa chọn")

    def hien_thi_thong_bao(self, noi_dung: str, la_loi: bool = False) -> None:
        """Hiển thị thông báo trạng thái (màu đỏ nếu lỗi, màu xanh nếu thành công)."""
        if la_loi:
            self.lbl_thong_bao.config(
                text=noi_dung, fg="#c62828", bg="#ffebee"
            )
        else:
            self.lbl_thong_bao.config(
                text=noi_dung, fg="#1b5e20", bg="#e8f5e9"
            )

    def cap_nhat_so_do(
        self, du_lieu_xep_cho: dict[str, str], ghe_dang_chon: str | None = None
    ) -> None:
        """Cập nhật trạng thái 12 nút ghế trên sơ đồ và bộ đếm góc dưới."""
        for ma_cho in DANH_SACH_CHO:
            ma_sv = du_lieu_xep_cho.get(ma_cho)
            btn = self.nut_ghe[ma_cho]
            dang_chon = ma_cho == ghe_dang_chon

            if ma_sv:
                btn.config(
                    text=f"{ma_cho} - {ma_sv}",
                    bg=MAU_CO_NGUOI,
                    activebackground=MAU_CO_NGUOI_ACTIVE,
                    fg="#b71c1c",
                    relief=tk.SOLID if dang_chon else tk.RAISED,
                    bd=4 if dang_chon else 2,
                )
            else:
                btn.config(
                    text=f"{ma_cho} - Trống",
                    bg=MAU_TRONG,
                    activebackground=MAU_TRONG_ACTIVE,
                    fg="#1b5e20",
                    relief=tk.SOLID if dang_chon else tk.RAISED,
                    bd=4 if dang_chon else 2,
                )

        so_cho_da_dung = len(du_lieu_xep_cho)
        self.lbl_bo_dem.config(
            text=f"Số chỗ đã sử dụng: {so_cho_da_dung}/12"
        )
