"""Module 5: Giao diện Người dùng Đồ họa Tkinter (ui/main_window.py)

Dự án: Quản lý phòng máy tính 12 vị trí (3 hàng x 4 cột).
Trách nhiệm:
- Xây dựng cửa sổ chính ứng dụng quản lý phòng máy bằng Tkinter.
- Hiển thị sơ đồ 12 vị trí trực quan (3 hàng x 4 cột), phân biệt màu sắc Chỗ trống và Đã có người.
- Khu vực thao tác: Xếp chỗ, Trả chỗ, Tra cứu sinh viên.
- Khu vực thống kê: Tổng số, Đã dùng, Còn trống, Tỷ lệ sử dụng (%).
- Tự động cập nhật giao diện sau mỗi thao tác thành công.
- Tách biệt hoàn toàn tầng giao diện và logic cơ sở dữ liệu.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, Dict

# Import các hàm nghiệp vụ từ tầng services và database
from database import get_seat_map, get_seat_stats, VALID_SEATS
from services.seat_service import assign_seat, release_seat
from services.student_service import find_student


class MainWindow:
    """Lớp điều khiển giao diện chính của ứng dụng Quản lý Phòng máy."""
    
    # Bảng màu giao diện chuẩn
    COLOR_BG = "#F4F6F9"
    COLOR_PRIMARY = "#1B365D"       # Xanh Navy
    COLOR_SECONDARY = "#2E75B6"     # Xanh dương
    COLOR_EMPTY_SEAT = "#E8EEF5"    # Nền chỗ trống
    COLOR_EMPTY_TEXT = "#1B365D"    # Chữ chỗ trống
    COLOR_OCCUPIED_SEAT = "#C8E6C9" # Nền chỗ đã có người
    COLOR_OCCUPIED_TEXT = "#1B5E20" # Chữ chỗ đã có người
    COLOR_SELECTED_SEAT = "#FFF59D" # Nền chỗ đang chọn (Vàng nhạt nổi bật)
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("HỆ THỐNG QUẢN LÝ PHÒNG MÁY TÍNH (12 VỊ TRÍ - SQLITE)")
        self.root.geometry("860x700")
        self.root.minsize(820, 680)
        self.root.configure(bg=self.COLOR_BG)
        
        # Biến trạng thái giao diện
        self.selected_seat: Optional[str] = None
        self.seat_buttons: Dict[str, tk.Button] = {}
        
        # Xây dựng các khối giao diện
        self._create_header()
        self._create_main_content()
        self._create_status_bar()
        
        # Nạp trạng thái ban đầu từ SQLite
        self.refresh_ui()

    def _create_header(self):
        """Tạo thanh tiêu đề phía trên."""
        header_frame = tk.Frame(self.root, bg=self.COLOR_PRIMARY, height=75)
        header_frame.pack(fill=tk.X, side=tk.TOP)
        
        title_label = tk.Label(
            header_frame,
            text="HỆ THỐNG QUẢN LÝ XẾP CHỖ PHÒNG MÁY TÍNH",
            font=("Arial", 15, "bold"),
            fg="#FFFFFF",
            bg=self.COLOR_PRIMARY
        )
        title_label.pack(pady=(10, 2))
        
        subtitle_label = tk.Label(
            header_frame,
            text="Phòng máy 12 vị trí (3 hàng × 4 cột) | Cơ sở dữ liệu SQLite",
            font=("Arial", 9, "italic"),
            fg="#CFD8DC",
            bg=self.COLOR_PRIMARY
        )
        subtitle_label.pack(pady=(0, 10))

    def _create_main_content(self):
        """Tạo khung chứa nội dung chính."""
        container = tk.Frame(self.root, bg=self.COLOR_BG)
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # 1. Khu vực sơ đồ 12 vị trí máy (Phía trên)
        self._create_seat_map_section(container)
        
        # 2. Khung chia đôi phía dưới: Trái là Thao tác, Phải là Thống kê & Tra cứu
        bottom_frame = tk.Frame(container, bg=self.COLOR_BG)
        bottom_frame.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
        
        # Khung bên trái: Xếp chỗ & Trả chỗ
        self._create_action_section(bottom_frame)
        
        # Khung bên phải: Tra cứu & Thống kê
        self._create_info_section(bottom_frame)

    def _create_seat_map_section(self, parent):
        """A. Sơ đồ phòng máy 12 vị trí (3 hàng x 4 cột)."""
        map_group = tk.LabelFrame(
            parent,
            text=" SƠ ĐỒ 12 VỊ TRÍ PHÒNG MÁY (Click vào nút để chọn vị trí) ",
            font=("Arial", 10, "bold"),
            fg=self.COLOR_PRIMARY,
            bg="#FFFFFF",
            padx=15,
            pady=10,
            relief=tk.GROOVE
        )
        map_group.pack(fill=tk.X, pady=(0, 10))
        
        # Bố cục 3 hàng (A, B, C) x 4 cột (1, 2, 3, 4)
        rows = ["A", "B", "C"]
        cols = [1, 2, 3, 4]
        
        for r_idx, row_name in enumerate(rows):
            # Nhãn hàng (Hàng A, Hàng B, Hàng C)
            row_label = tk.Label(
                map_group,
                text=f"Hàng {row_name}",
                font=("Arial", 10, "bold"),
                fg=self.COLOR_SECONDARY,
                bg="#FFFFFF",
                width=8,
                anchor="w"
            )
            row_label.grid(row=r_idx, column=0, padx=(5, 10), pady=6)
            
            for c_idx, col_num in enumerate(cols):
                seat_code = f"{row_name}{col_num}"
                btn = tk.Button(
                    map_group,
                    text=f"{seat_code} - Trống",
                    font=("Arial", 10, "bold"),
                    width=14,
                    height=2,
                    relief=tk.RAISED,
                    bd=2,
                    cursor="hand2",
                    command=lambda s=seat_code: self.on_seat_selected(s)
                )
                btn.grid(row=r_idx, column=c_idx + 1, padx=8, pady=6)
                self.seat_buttons[seat_code] = btn

    def _create_action_section(self, parent):
        """B & C. Khu vực Xếp chỗ và Trả chỗ."""
        action_group = tk.LabelFrame(
            parent,
            text=" QUẢN LÝ XẾP CHỖ & TRẢ CHỖ ",
            font=("Arial", 10, "bold"),
            fg=self.COLOR_PRIMARY,
            bg="#FFFFFF",
            padx=15,
            pady=12,
            relief=tk.GROOVE
        )
        action_group.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Dòng 1: Hiển thị vị trí máy đang chọn
        seat_display_frame = tk.Frame(action_group, bg="#FFFFFF")
        seat_display_frame.pack(fill=tk.X, pady=(0, 8))
        
        tk.Label(
            seat_display_frame,
            text="Vị trí đã chọn:",
            font=("Arial", 10, "bold"),
            bg="#FFFFFF",
            width=14,
            anchor="w"
        ).pack(side=tk.LEFT)
        
        self.lbl_selected_seat = tk.Label(
            seat_display_frame,
            text="[Chưa chọn]",
            font=("Arial", 11, "bold"),
            fg="#D32F2F",
            bg="#FFFFFF",
            anchor="w"
        )
        self.lbl_selected_seat.pack(side=tk.LEFT, padx=5)
        
        # Dòng 2: Ô nhập mã sinh viên để xếp chỗ
        sv_input_frame = tk.Frame(action_group, bg="#FFFFFF")
        sv_input_frame.pack(fill=tk.X, pady=8)
        
        tk.Label(
            sv_input_frame,
            text="Mã sinh viên:",
            font=("Arial", 10, "bold"),
            bg="#FFFFFF",
            width=14,
            anchor="w"
        ).pack(side=tk.LEFT)
        
        self.entry_assign_sv = tk.Entry(
            sv_input_frame,
            font=("Arial", 11),
            width=18,
            relief=tk.SOLID,
            bd=1
        )
        self.entry_assign_sv.pack(side=tk.LEFT, padx=5)
        self.entry_assign_sv.bind("<Return>", lambda event: self.handle_assign())
        
        tk.Label(
            sv_input_frame,
            text="(Ví dụ: SV100)",
            font=("Arial", 8, "italic"),
            fg="#78909C",
            bg="#FFFFFF"
        ).pack(side=tk.LEFT, padx=5)
        
        # Dòng 3: Cụm nút Xếp chỗ và Trả chỗ
        btn_frame = tk.Frame(action_group, bg="#FFFFFF")
        btn_frame.pack(fill=tk.X, pady=(15, 5))
        
        btn_assign = tk.Button(
            btn_frame,
            text="✓ XẾP CHỖ",
            font=("Arial", 10, "bold"),
            bg="#2E7D32",
            fg="#FFFFFF",
            activebackground="#1B5E20",
            activeforeground="#FFFFFF",
            width=12,
            height=2,
            cursor="hand2",
            command=self.handle_assign
        )
        btn_assign.pack(side=tk.LEFT, padx=(0, 10))
        
        btn_release = tk.Button(
            btn_frame,
            text="✕ TRẢ CHỖ",
            font=("Arial", 10, "bold"),
            bg="#C62828",
            fg="#FFFFFF",
            activebackground="#B71C1C",
            activeforeground="#FFFFFF",
            width=12,
            height=2,
            cursor="hand2",
            command=self.handle_release
        )
        btn_release.pack(side=tk.LEFT)

    def _create_info_section(self, parent):
        """D & E. Khu vực Tra cứu sinh viên và Thống kê phòng máy."""
        info_frame = tk.Frame(parent, bg=self.COLOR_BG)
        info_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Khung Tra cứu sinh viên
        search_group = tk.LabelFrame(
            info_frame,
            text=" TRA CỨU SINH VIÊN ",
            font=("Arial", 10, "bold"),
            fg=self.COLOR_PRIMARY,
            bg="#FFFFFF",
            padx=12,
            pady=8,
            relief=tk.GROOVE
        )
        search_group.pack(fill=tk.X, pady=(0, 10))
        
        search_input_frame = tk.Frame(search_group, bg="#FFFFFF")
        search_input_frame.pack(fill=tk.X, pady=4)
        
        tk.Label(
            search_input_frame,
            text="Mã sinh viên:",
            font=("Arial", 10),
            bg="#FFFFFF"
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        self.entry_search_sv = tk.Entry(
            search_input_frame,
            font=("Arial", 10),
            width=12,
            relief=tk.SOLID,
            bd=1
        )
        self.entry_search_sv.pack(side=tk.LEFT, padx=5)
        self.entry_search_sv.bind("<Return>", lambda event: self.handle_search())
        
        btn_search = tk.Button(
            search_input_frame,
            text="🔍 Tra cứu",
            font=("Arial", 9, "bold"),
            bg=self.COLOR_SECONDARY,
            fg="#FFFFFF",
            cursor="hand2",
            command=self.handle_search
        )
        btn_search.pack(side=tk.LEFT, padx=5)
        
        self.lbl_search_result = tk.Label(
            search_group,
            text="Nhập mã sinh viên và bấm 'Tra cứu' để xem thông tin.",
            font=("Arial", 9),
            fg="#546E7A",
            bg="#ECEFF1",
            anchor="w",
            padx=8,
            pady=6,
            relief=tk.SUNKEN
        )
        self.lbl_search_result.pack(fill=tk.X, pady=(6, 2))
        
        # Khung Thống kê phòng máy
        stats_group = tk.LabelFrame(
            info_frame,
            text=" THỐNG KÊ PHÒNG MÁY ",
            font=("Arial", 10, "bold"),
            fg=self.COLOR_PRIMARY,
            bg="#FFFFFF",
            padx=12,
            pady=8,
            relief=tk.GROOVE
        )
        stats_group.pack(fill=tk.BOTH, expand=True)
        
        self.lbl_stat_total = tk.Label(stats_group, text="• Tổng số vị trí: 12", font=("Arial", 9, "bold"), bg="#FFFFFF", anchor="w")
        self.lbl_stat_total.pack(fill=tk.X, pady=2)
        
        self.lbl_stat_used = tk.Label(stats_group, text="• Đã sử dụng: 0 / 12", font=("Arial", 9, "bold"), fg="#D32F2F", bg="#FFFFFF", anchor="w")
        self.lbl_stat_used.pack(fill=tk.X, pady=2)
        
        self.lbl_stat_avail = tk.Label(stats_group, text="• Còn trống: 12 / 12", font=("Arial", 9, "bold"), fg="#2E7D32", bg="#FFFFFF", anchor="w")
        self.lbl_stat_avail.pack(fill=tk.X, pady=2)
        
        self.lbl_stat_rate = tk.Label(stats_group, text="• Tỷ lệ sử dụng: 0.0%", font=("Arial", 9, "bold"), fg=self.COLOR_SECONDARY, bg="#FFFFFF", anchor="w")
        self.lbl_stat_rate.pack(fill=tk.X, pady=2)

    def _create_status_bar(self):
        """Tạo thanh thông báo trạng thái dưới cùng."""
        self.status_bar = tk.Label(
            self.root,
            text="Hệ thống đã sẵn sàng.",
            font=("Arial", 9, "italic"),
            fg="#37474F",
            bg="#CFD8DC",
            anchor="w",
            padx=12,
            pady=4,
            relief=tk.SUNKEN
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    # -------------------------------------------------------------------------
    # XỬ LÝ SỰ KIỆN GIAO DIỆN
    # -------------------------------------------------------------------------

    def on_seat_selected(self, seat_code: str):
        """Xử lý sự kiện khi người dùng click vào một vị trí máy trên sơ đồ."""
        self.selected_seat = seat_code
        self.lbl_selected_seat.config(text=f"[{seat_code}]", fg=self.COLOR_PRIMARY)
        self.status_bar.config(
            text=f"Đã chọn vị trí máy {seat_code}. Nhập mã sinh viên để xếp hoặc bấm 'Trả chỗ'.",
            fg="#1565C0"
        )
        self._highlight_selected_button(seat_code)

    def _highlight_selected_button(self, seat_code: str):
        """Làm nổi bật viền của nút đang được chọn."""
        seat_map = get_seat_map()
        for code, btn in self.seat_buttons.items():
            ma_sv = seat_map.get(code)
            if code == seat_code:
                btn.config(relief=tk.SOLID, bd=3)
            else:
                btn.config(relief=tk.RAISED, bd=2)

    def handle_assign(self):
        """Xử lý sự kiện bấm nút [Xếp chỗ]."""
        # Kiểm tra người dùng đã chọn vị trí máy chưa
        if not self.selected_seat:
            messagebox.showwarning("Cảnh báo", "Vui lòng click chọn một vị trí máy trên sơ đồ trước khi xếp chỗ!")
            return
            
        ma_sv = self.entry_assign_sv.get().strip().upper()
        if not ma_sv:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập mã sinh viên (ví dụ: SV100)!")
            self.entry_assign_sv.focus()
            return
            
        # Gọi tầng nghiệp vụ seat_service
        success, message = assign_seat(self.selected_seat, ma_sv)
        
        if success:
            messagebox.showinfo("Thành công", message)
            self.entry_assign_sv.delete(0, tk.END)
            self.refresh_ui()
            self.status_bar.config(text=f"✓ {message}", fg="#1B5E20")
        else:
            messagebox.showerror("Không thể xếp chỗ", message)
            self.status_bar.config(text=f"✕ Lỗi: {message}", fg="#B71C1C")

    def handle_release(self):
        """Xử lý sự kiện bấm nút [Trả chỗ]."""
        if not self.selected_seat:
            messagebox.showwarning("Cảnh báo", "Vui lòng click chọn vị trí máy cần trả trên sơ đồ!")
            return
            
        # Xác nhận trước khi thực hiện trả chỗ
        confirm = messagebox.askyesno(
            "Xác nhận trả chỗ",
            f"Bạn có chắc chắn muốn giải phóng vị trí máy {self.selected_seat}?"
        )
        if not confirm:
            return
            
        # Gọi tầng nghiệp vụ seat_service
        success, message = release_seat(self.selected_seat)
        
        if success:
            messagebox.showinfo("Thành công", message)
            self.refresh_ui()
            self.status_bar.config(text=f"✓ {message}", fg="#1B5E20")
        else:
            messagebox.showwarning("Không thể trả chỗ", message)
            self.status_bar.config(text=f"✕ Cảnh báo: {message}", fg="#E65100")

    def handle_search(self):
        """Xử lý sự kiện bấm nút [Tra cứu] sinh viên."""
        ma_sv = self.entry_search_sv.get().strip().upper()
        if not ma_sv:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập mã sinh viên cần tra cứu!")
            self.entry_search_sv.focus()
            return
            
        # Gọi tầng nghiệp vụ student_service
        result = find_student(ma_sv)
        
        if result is None:
            text = f"Không tìm thấy sinh viên có mã '{ma_sv}' trong hệ thống."
            self.lbl_search_result.config(text=text, fg="#B71C1C", bg="#FFEBEE")
            self.status_bar.config(text=f"✕ {text}", fg="#B71C1C")
        else:
            ho_ten = result["ho_ten"]
            ma_cho = result["ma_cho"]
            
            if ma_cho:
                text = f"Sinh viên: {ho_ten} ({ma_sv})\n→ ĐÃ XẾP CHỖ tại vị trí: [{ma_cho}]"
                self.lbl_search_result.config(text=text, fg="#1B5E20", bg="#E8F5E9")
                self.status_bar.config(text=f"✓ Sinh viên {ma_sv} đang ngồi tại {ma_cho}.", fg="#1B5E20")
                # Tự động chọn và làm nổi bật vị trí máy tìm thấy trên sơ đồ
                self.on_seat_selected(ma_cho)
            else:
                text = f"Sinh viên: {ho_ten} ({ma_sv})\n→ Trạng thái: CHƯA ĐƯỢC XẾP CHỖ"
                self.lbl_search_result.config(text=text, fg="#0D47A1", bg="#E3F2FD")
                self.status_bar.config(text=f"ℹ Sinh viên {ma_sv} chưa được xếp chỗ.", fg="#0D47A1")

    def refresh_ui(self):
        """Đồng bộ trạng thái toàn bộ 12 vị trí máy và số liệu thống kê từ SQLite."""
        # 1. Cập nhật 12 nút máy tính
        seat_map = get_seat_map()
        for seat_code, ma_sv in seat_map.items():
            btn = self.seat_buttons.get(seat_code)
            if not btn:
                continue
                
            if ma_sv:
                # Vị trí đã có sinh viên ngồi
                btn.config(
                    text=f"{seat_code} - {ma_sv}",
                    bg=self.COLOR_OCCUPIED_SEAT,
                    fg=self.COLOR_OCCUPIED_TEXT
                )
            else:
                # Vị trí còn trống
                btn.config(
                    text=f"{seat_code} - Trống",
                    bg=self.COLOR_EMPTY_SEAT,
                    fg=self.COLOR_EMPTY_TEXT
                )
                
        # Duy trì viền nút đang chọn nếu có
        if self.selected_seat:
            self._highlight_selected_button(self.selected_seat)
            
        # 2. Cập nhật số liệu thống kê
        stats = get_seat_stats()
        self.lbl_stat_total.config(text=f"• Tổng số vị trí: {stats['total']}")
        self.lbl_stat_used.config(text=f"• Đã sử dụng: {stats['used']} / {stats['total']}")
        self.lbl_stat_avail.config(text=f"• Còn trống: {stats['available']} / {stats['total']}")
        self.lbl_stat_rate.config(text=f"• Tỷ lệ sử dụng: {stats['usage_rate']}%")
