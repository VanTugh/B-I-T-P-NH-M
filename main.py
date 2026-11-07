import os
import sqlite3
import tkinter as tk
from tkinter import font as tkfont

from tao_du_lieu_demo import DB_PATH, khoi_tao_du_lieu

DANH_SACH_CHO = [
    f"{hang}{cot}" for hang in ("A", "B", "C") for cot in range(1, 5)
]

# Bảng màu theo đặc tả giao diện (UI/UX Specification)
MAU_TRONG = "#b9f6ca"         # Xanh lá nhạt (Light Green)
MAU_TRONG_ACTIVE = "#69f0ae"
MAU_CO_NGUOI = "#ff8a80"      # Đỏ nhạt (Light Coral)
MAU_CO_NGUOI_ACTIVE = "#ff5252"
MAU_VIEN_CHON = "#0d47a1"     # Viền xanh đậm nổi bật khi ghế đang được chọn


class MainWindow:
    """Cửa sổ chính của Ứng dụng xếp chỗ và tra cứu sinh viên phòng máy."""

    def __init__(self, root: tk.Tk, db_path: str = DB_PATH) -> None:
        self.root = root
        self.db_path = db_path
        self.ghe_dang_chon: str | None = None
        self.nut_ghe: dict[str, tk.Button] = {}
        self.trang_thai_ghe: dict[str, str | None] = {
            ma_cho: None for ma_cho in DANH_SACH_CHO
        }

        # Đảm bảo CSDL và 100 sinh viên mẫu đã sẵn sàng trước khi nạp giao diện
        khoi_tao_du_lieu(self.db_path)

        self._thiet_lap_cua_so()
        self._xay_dung_giao_dien()
        self.load_data_to_gui()

    def _ket_noi_db(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

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

        # Khung chứa 12 nút ghế dạng lưới 3x4
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
                    command=lambda m=ma_cho: self.chon_ghe(m),
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
        # Bắt sự kiện phím Enter để tra cứu nhanh theo đặc tả
        self.entry_ma_sv.bind("<Return>", lambda _event: self.tra_cuu())

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
            command=self.xep_cho,
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
            command=self.tra_cho,
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
            command=self.tra_cuu,
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
    # CÁC HÀM XỬ LÝ SỰ KIỆN VÀ LOGIC DATABASE
    # =========================================================================

    def hien_thi_thong_bao(self, noi_dung: str, la_loi: bool = False) -> None:
        """Cập nhật vùng thông báo với màu đỏ nếu là lỗi, màu xanh nếu thành công."""
        if la_loi:
            self.lbl_thong_bao.config(
                text=noi_dung, fg="#c62828", bg="#ffebee"
            )
        else:
            self.lbl_thong_bao.config(
                text=noi_dung, fg="#1b5e20", bg="#e8f5e9"
            )

    def load_data_to_gui(self) -> None:
        """
        Truy vấn bảng xep_cho từ SQLite và cập nhật trạng thái 12 nút ghế
        cùng bộ đếm sử dụng.
        """
        conn = self._ket_noi_db()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT ma_cho, ma_sv FROM xep_cho")
            du_lieu = dict(cursor.fetchall())
        finally:
            conn.close()

        for ma_cho in DANH_SACH_CHO:
            ma_sv = du_lieu.get(ma_cho)
            self.trang_thai_ghe[ma_cho] = ma_sv
            btn = self.nut_ghe[ma_cho]
            dang_chon = ma_cho == self.ghe_dang_chon

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

        so_cho_da_dung = len(du_lieu)
        self.lbl_bo_dem.config(
            text=f"Số chỗ đã sử dụng: {so_cho_da_dung}/12"
        )

    def chon_ghe(self, ma_cho: str) -> None:
        """Sự kiện khi người dùng click vào một nút ghế trên sơ đồ."""
        self.ghe_dang_chon = ma_cho
        self.lbl_ghe_dang_chon.config(text=f"Đang chọn: {ma_cho}")
        self.load_data_to_gui()

        ma_sv_dang_ngoi = self.trang_thai_ghe.get(ma_cho)
        if ma_sv_dang_ngoi:
            ho_ten = self._lay_ho_ten_sv(ma_sv_dang_ngoi) or ""
            self.hien_thi_thong_bao(
                f"Đã chọn ghế {ma_cho} (Đang có: {ma_sv_dang_ngoi} - {ho_ten}).\n"
                f"Bấm [Trả chỗ] nếu muốn hủy chỗ ngồi này.",
                la_loi=False,
            )
        else:
            self.hien_thi_thong_bao(
                f"Đã chọn ghế {ma_cho} (Trống).\n"
                f"Nhập mã sinh viên và bấm [Xếp chỗ] để gán vị trí.",
                la_loi=False,
            )

    def _lay_ho_ten_sv(self, ma_sv: str) -> str | None:
        conn = self._ket_noi_db()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT ho_ten FROM sinh_vien WHERE ma_sv = ?", (ma_sv,)
            )
            row = cursor.fetchone()
            return row[0] if row else None
        finally:
            conn.close()

    def xep_cho(self) -> None:
        """Xử lý chức năng [Xếp chỗ] với đầy đủ 3 bước kiểm tra hợp lệ (Validate)."""
        # Kiểm tra đã chọn ghế chưa
        if not self.ghe_dang_chon:
            self.hien_thi_thong_bao(
                "Vui lòng chọn một chỗ ngồi trên sơ đồ!", la_loi=True
            )
            return

        ma_cho = self.ghe_dang_chon
        ma_sv = self.entry_ma_sv.get().strip().upper()

        if not ma_sv:
            self.hien_thi_thong_bao(
                "Vui lòng nhập mã sinh viên!", la_loi=True
            )
            return

        conn = self._ket_noi_db()
        try:
            cursor = conn.cursor()

            # Validate 1: Kiểm tra chỗ được chọn có đang trống không
            cursor.execute(
                "SELECT ma_sv FROM xep_cho WHERE ma_cho = ?", (ma_cho,)
            )
            if cursor.fetchone() is not None:
                self.hien_thi_thong_bao(
                    f"Chỗ {ma_cho} đã có người ngồi!", la_loi=True
                )
                return

            # Validate 2: Kiểm tra mã SV có tồn tại trong bảng sinh_vien không
            cursor.execute(
                "SELECT ho_ten FROM sinh_vien WHERE ma_sv = ?", (ma_sv,)
            )
            sv_row = cursor.fetchone()
            if sv_row is None:
                self.hien_thi_thong_bao(
                    "Mã sinh viên không tồn tại trong cơ sở dữ liệu!",
                    la_loi=True,
                )
                return

            ho_ten = sv_row[0]

            # Validate 3: Thêm vào bảng xep_cho và bắt lỗi UNIQUE (IntegrityError)
            try:
                cursor.execute(
                    "INSERT INTO xep_cho (ma_cho, ma_sv) VALUES (?, ?)",
                    (ma_cho, ma_sv),
                )
                conn.commit()
            except sqlite3.IntegrityError:
                self.hien_thi_thong_bao(
                    f"Sinh viên {ma_sv} đã được xếp ở một vị trí khác!",
                    la_loi=True,
                )
                return

        finally:
            conn.close()

        # Cập nhật lại giao diện, xóa trắng ô nhập và thông báo thành công
        self.load_data_to_gui()
        self.entry_ma_sv.delete(0, tk.END)
        self.hien_thi_thong_bao(
            f"Xếp chỗ thành công!\nHọ tên: {ho_ten} ({ma_sv}) - Đang ngồi: {ma_cho}",
            la_loi=False,
        )

    def tra_cho(self) -> None:
        """
        Xử lý chức năng [Trả chỗ]:
        - Cách 1: Chọn trực tiếp ghế đang có người trên sơ đồ -> bấm [Trả chỗ].
        - Cách 2 (Optional): Nhập mã SV vào ô nhập liệu -> bấm [Trả chỗ].
        """
        ma_sv_nhap = self.entry_ma_sv.get().strip().upper()

        conn = self._ket_noi_db()
        try:
            cursor = conn.cursor()

            # Ưu tiên Cách 1: Trả chỗ theo ghế đang chọn trên sơ đồ nếu ghế đó có người
            if self.ghe_dang_chon:
                cursor.execute(
                    "SELECT ma_sv FROM xep_cho WHERE ma_cho = ?",
                    (self.ghe_dang_chon,),
                )
                row = cursor.fetchone()
                if row is not None:
                    ma_cho_xoa = self.ghe_dang_chon
                    ma_sv_xoa = row[0]
                    cursor.execute(
                        "DELETE FROM xep_cho WHERE ma_cho = ?", (ma_cho_xoa,)
                    )
                    conn.commit()
                    self.load_data_to_gui()
                    self.hien_thi_thong_bao(
                        f"Đã trả chỗ {ma_cho_xoa} (Sinh viên {ma_sv_xoa}) thành công!",
                        la_loi=False,
                    )
                    return

            # Hỗ trợ Cách 2: Trả chỗ theo mã sinh viên nhập trong ô Entry
            if ma_sv_nhap:
                cursor.execute(
                    "SELECT ma_cho FROM xep_cho WHERE ma_sv = ?",
                    (ma_sv_nhap,),
                )
                row_sv = cursor.fetchone()
                if row_sv is not None:
                    ma_cho_xoa = row_sv[0]
                    cursor.execute(
                        "DELETE FROM xep_cho WHERE ma_cho = ?", (ma_cho_xoa,)
                    )
                    conn.commit()
                    self.load_data_to_gui()
                    self.entry_ma_sv.delete(0, tk.END)
                    self.hien_thi_thong_bao(
                        f"Đã trả chỗ {ma_cho_xoa} của sinh viên {ma_sv_nhap} thành công!",
                        la_loi=False,
                    )
                    return

            # Nếu không rơi vào 2 trường hợp trên, báo lỗi cụ thể
            if not self.ghe_dang_chon and not ma_sv_nhap:
                self.hien_thi_thong_bao(
                    "Vui lòng chọn một chỗ ngồi trên sơ đồ!", la_loi=True
                )
            elif self.ghe_dang_chon:
                self.hien_thi_thong_bao(
                    f"Chỗ {self.ghe_dang_chon} hiện đang trống, không thể trả chỗ!",
                    la_loi=True,
                )
            else:
                self.hien_thi_thong_bao(
                    f"Sinh viên {ma_sv_nhap} hiện chưa được xếp chỗ!",
                    la_loi=True,
                )
        finally:
            conn.close()

    def tra_cuu(self) -> None:
        """
        Xử lý chức năng [Tra cứu] bằng câu lệnh LEFT JOIN giữa sinh_vien và xep_cho.
        """
        ma_sv = self.entry_ma_sv.get().strip().upper()
        if not ma_sv:
            self.hien_thi_thong_bao(
                "Vui lòng nhập mã sinh viên cần tra cứu!", la_loi=True
            )
            return

        conn = self._ket_noi_db()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT s.ho_ten, x.ma_cho
                FROM sinh_vien s
                LEFT JOIN xep_cho x ON s.ma_sv = x.ma_sv
                WHERE s.ma_sv = ?
                """,
                (ma_sv,),
            )
            row = cursor.fetchone()
        finally:
            conn.close()

        if row is None:
            self.hien_thi_thong_bao(
                "Mã sinh viên không tồn tại trong cơ sở dữ liệu!", la_loi=True
            )
            return

        ho_ten, ma_cho = row
        if ma_cho:
            self.ghe_dang_chon = ma_cho
            self.lbl_ghe_dang_chon.config(text=f"Đang chọn: {ma_cho}")
            self.load_data_to_gui()
            self.hien_thi_thong_bao(
                f"Họ tên: {ho_ten} - Đang ngồi: {ma_cho}", la_loi=False
            )
        else:
            self.hien_thi_thong_bao(
                f"Họ tên: {ho_ten} - Chưa được xếp chỗ", la_loi=False
            )


if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()
