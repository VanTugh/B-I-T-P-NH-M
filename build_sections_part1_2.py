import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from generator_core import (
    COLOR_PRIMARY_NAVY, COLOR_SECONDARY_BLUE, COLOR_ACCENT_BLUE,
    COLOR_BG_GRAY, COLOR_BORDER_GRAY,
    set_cell_margins, set_cell_shading, set_cell_borders,
    add_styled_heading, add_p, add_bullet, add_callout,
    add_code_block, add_styled_table, add_image_box
)

def build_cover_page(doc):
    """Xây dựng trang bìa chuyên nghiệp, ấn tượng."""
    # Banner top
    p_top = doc.add_paragraph()
    p_top.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_top.paragraph_format.space_before = Pt(10)
    p_top.paragraph_format.space_after = Pt(2)
    r_top1 = p_top.add_run("BÀI TẬP NHÓM HỌC PHẦN: LẬP TRÌNH PYTHON NÂNG CAO\n")
    r_top1.font.name = "Arial"
    r_top1.font.size = Pt(11)
    r_top1.bold = True
    r_top1.font.color.rgb = RGBColor(100, 110, 120)
    
    r_top2 = p_top.add_run("KỸ THUẬT PHÁT TRIỂN ỨNG DỤNG THEO MÔ HÌNH PHÂN TẦNG VÀ LÀM VIỆC NHÓM AGILE/GIT")
    r_top2.font.name = "Arial"
    r_top2.font.size = Pt(9.5)
    r_top2.italic = True
    r_top2.font.color.rgb = RGBColor(120, 130, 140)
    
    # Khoảng trống trang trí
    p_space = doc.add_paragraph()
    p_space.paragraph_format.space_before = Pt(30)
    
    # Tiêu đề chính
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_after = Pt(12)
    r_title = p_title.add_run("HƯỚNG DẪN TRIỂN KHAI TASK\nBÀI TẬP NHÓM PYTHON NÂNG CAO")
    r_title.font.name = "Arial"
    r_title.font.size = Pt(22)
    r_title.bold = True
    r_title.font.color.rgb = RGBColor(27, 54, 93)  # Navy
    
    # Tiêu đề phụ
    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(25)
    r_sub = p_sub.add_run("HỆ THỐNG QUẢN LÝ XẾP CHỖ PHÒNG MÁY TÍNH\n(BỐ CỤC 12 CHỖ – 3 HÀNG × 4 CỘT – CƠ SỞ DỮ LIỆU SQLITE)")
    r_sub.font.name = "Arial"
    r_sub.font.size = Pt(13)
    r_sub.bold = True
    r_sub.font.color.rgb = RGBColor(46, 117, 182)  # Blue
    
    # Badge khung thời gian
    p_badge = doc.add_paragraph()
    p_badge.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_badge.paragraph_format.space_after = Pt(40)
    r_badge = p_badge.add_run("★ SPRINT KỸ THUẬT 120 PHÚT | ĐẶC TẢ KỸ THUẬT & QUY TRÌNH PHỐI HỢP DÀNH CHO 5 THÀNH VIÊN ★")
    r_badge.font.name = "Arial"
    r_badge.font.size = Pt(10)
    r_badge.bold = True
    r_badge.font.color.rgb = RGBColor(27, 54, 93)
    
    # Bảng Metadata
    headers_meta = ["THUỘC TÍNH ĐẶC TẢ", "THÔNG TIN CHI TIẾT DỰ ÁN"]
    data_meta = [
        ["Học phần đào tạo", "Lập trình Python Nâng Cao (Advanced Python Programming)"],
        ["Đề tài thực hiện", "Ứng dụng hỗ trợ Lớp trưởng xếp chỗ, trả chỗ và tra cứu sinh viên phòng máy"],
        ["Kiến trúc hệ thống", "3-Tier Architecture (Tkinter GUI → Service Business Layer → SQLite DB)"],
        ["Quy mô dữ liệu", "Phòng máy 12 chỗ (A1–C4), CSDL tối thiểu 100 hồ sơ sinh viên (SV001–SV100)"],
        ["Vai trò lập tài liệu", "Senior Python Developer kiêm Technical Lead"],
        ["Đối tượng áp dụng", "Nhóm phát triển 05 thành viên (TV1, TV2, TV3, TV4, TV5)"],
        ["Thời gian thực thi", "120 phút (Theo quy định thời gian làm bài chuẩn)"],
        ["Mô hình quản lý mã nguồn", "Git Flow rút gọn trên GitHub (develop branch, feature branches, Pull Request)"],
        ["Phiên bản tài liệu", "Phiên bản 1.0 – Bàn giao chính thức (Official Technical Specification)"]
    ]
    add_styled_table(doc, headers_meta, data_meta, col_widths=[2.3, 4.5])
    
    # Lưu ý bảo mật dưới trang bìa
    p_bot = doc.add_paragraph()
    p_bot.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_bot.paragraph_format.space_before = Pt(30)
    r_bot = p_bot.add_run("TÀI LIỆU KỸ THUẬT NỘI BỘ – YÊU CẦU TOÀN BỘ THÀNH VIÊN TUÂN THỦ NGHIÊM NGẶT HỢP ĐỒNG API VÀ QUY TRÌNH GIT")
    r_bot.font.name = "Arial"
    r_bot.font.size = Pt(8.5)
    r_bot.italic = True
    r_bot.font.color.rgb = RGBColor(120, 130, 140)
    
    # Ngắt trang sau bìa
    doc.add_page_break()

def build_toc(doc):
    """Xây dựng Mục lục và Danh mục thuật ngữ."""
    add_styled_heading(doc, "MỤC LỤC TÀI LIỆU", level=1)
    
    toc_items = [
        ("PHẦN I. TỔNG QUAN QUY TRÌNH TRIỂN KHAI & KIẾN TRÚC HỆ THỐNG", "Trang 3"),
        ("    1.1. Bối cảnh dự án & Mục tiêu tối thượng trong 120 phút", "Trang 3"),
        ("    1.2. Kiến trúc tổng thể 3 tầng (3-Tier Layered Architecture)", "Trang 3"),
        ("    1.3. Phân định trách nhiệm module & Cơ chế giao tiếp liên tầng", "Trang 4"),
        ("    1.4. Năm nguyên tắc kỹ thuật cốt lõi bất khả xâm phạm", "Trang 5"),
        ("PHẦN II. DANH SÁCH TASK VÀ THỨ TỰ THỰC HIỆN", "Trang 6"),
        ("    2.1. Ma trận phân bổ 10 Task kỹ thuật", "Trang 6"),
        ("    2.2. Phân tích luồng thực thi: Tuần tự vs. Song song", "Trang 7"),
        ("    2.3. Sơ đồ luồng phụ thuộc Task (Mermaid & Visual Diagram)", "Trang 8"),
        ("    2.4. Kế hoạch điều phối dòng thời gian Sprint 120 phút", "Trang 9"),
        ("PHẦN III. HƯỚNG DẪN CHI TIẾT TỪNG TASK (TASK-01 ĐẾN TASK-10)", "Trang 10"),
        ("    TASK-01: Khởi tạo GitHub Repository, cấu trúc dự án & API Contract", "Trang 10"),
        ("    TASK-02: Thiết kế SQLite Schema và Module kết nối CSDL (database.py)", "Trang 12"),
        ("    TASK-03: Xây dựng Script sinh dữ liệu 100 sinh viên demo an toàn", "Trang 14"),
        ("    TASK-04: Xây dựng Module nghiệp vụ Xếp chỗ và Trả chỗ (seat_service.py)", "Trang 16"),
        ("    TASK-05: Xây dựng Module Tra cứu sinh viên & Thống kê chỗ ngồi", "Trang 19"),
        ("    TASK-06: Xây dựng Giao diện người dùng Tkinter 12 chỗ (ui.py, main.py)", "Trang 22"),
        ("    TASK-07: Kiểm thử đơn vị độc lập từng module (Unit / Self-Testing)", "Trang 26"),
        ("    TASK-08: Tích hợp các module vào luồng ứng dụng hoàn chỉnh", "Trang 28"),
        ("    TASK-09: Kiểm thử tích hợp hệ thống (SIT) và Xử lý lỗi phát sinh", "Trang 30"),
        ("    TASK-10: Hoàn thiện tài liệu, đóng gói sản phẩm và chuẩn bị nghiệm thu", "Trang 32"),
        ("PHẦN IV. QUY TRÌNH LÀM VIỆC VỚI GIT/GITHUB (TRÁNH XUNG ĐỘT)", "Trang 34"),
        ("    4.1. Chiến lược phân nhánh Git Flow rút gọn", "Trang 34"),
        ("    4.2. Hướng dẫn thực hành 6 bước làm việc với Git hàng ngày", "Trang 35"),
        ("    4.3. Quy chuẩn viết Commit Message theo Conventional Commits", "Trang 36"),
        ("    4.4. Quy trình tạo Pull Request & Tiêu chí Code Review của TV5", "Trang 37"),
        ("    4.5. Hướng dẫn chi tiết cách phát hiện và giải quyết Conflict trên VS Code", "Trang 38"),
        ("    4.6. Hướng dẫn đặc biệt: Quản lý tệp SQLite phong_may.db trên Git", "Trang 40"),
        ("PHẦN V. QUY TRÌNH TÍCH HỢP MODULE & KỊCH BẢN THỰC THI", "Trang 41"),
        ("    5.1. Thứ tự tích hợp 6 bước từ Data đến Presentation", "Trang 41"),
        ("    5.2. Minh họa luồng thực thi hoàn chỉnh (End-to-End Trace)", "Trang 42"),
        ("    5.3. Bảng phân tích các sự cố tích hợp kinh điển và biện pháp xử lý", "Trang 44"),
        ("PHẦN VI. CHECKLIST NGHIỆM THU & BỘ TIÊU CHÍ CHẤT LƯỢNG", "Trang 45"),
        ("    6.1. Bảng 17 Tiêu chí chấp nhận toàn diện (AC-01 đến AC-17)", "Trang 45"),
        ("    6.2. Kịch bản kiểm thử bắt buộc theo đề (TC01 đến TC07)", "Trang 48"),
        ("    6.3. Quy trình ghi nhận và xử lý lỗi (Mẫu Bug Report chuẩn)", "Trang 50"),
        ("    6.4. Báo cáo tổng kết kiểm thử & Điều kiện ký xác nhận bàn giao", "Trang 51"),
        ("PHẦN VII. BẢNG BÀN GIAO TRÁCH NHIỆM & ĐÁNH GIÁ ĐÓNG GÓP", "Trang 52"),
        ("    7.1. Bảng theo dõi bàn giao Task và Tệp nguồn", "Trang 52"),
        ("    7.2. Bảng đánh giá tỷ lệ đóng góp thành viên và Ký xác nhận", "Trang 53"),
        ("    7.3. Kịch bản demo và bảo vệ bài tập nhóm trước Giảng viên", "Trang 54")
    ]
    
    for title, page in toc_items:
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(1)
        p.paragraph_format.space_after = Pt(1)
        p.paragraph_format.line_spacing = 1.15
        
        r1 = p.add_run(title)
        r1.font.name = "Arial"
        r1.font.size = Pt(9.5)
        if "PHẦN" in title:
            r1.bold = True
            r1.font.color.rgb = RGBColor(27, 54, 93)
        else:
            r1.font.color.rgb = RGBColor(60, 60, 60)
            
        r_tab = p.add_run(f"  ...........................................................................................................  {page}")
        r_tab.font.name = "Arial"
        r_tab.font.size = Pt(8.5)
        r_tab.font.color.rgb = RGBColor(150, 150, 150)
        
    add_callout(doc, "BẢNG QUY ƯỚC THUẬT NGỮ KỸ THUẬT VIẾT TẮT",
                "• SoC (Separation of Concerns): Phân tách trách nhiệm giữa các module độc lập.\n"
                "• DDL (Data Definition Language): Ngôn ngữ định nghĩa cấu trúc dữ liệu SQLite (CREATE TABLE, PRIMARY KEY, FOREIGN KEY).\n"
                "• DoD (Definition of Done): Bộ tiêu chí bắt buộc phải thỏa mãn để một Task được xem là hoàn thành.\n"
                "• AC (Acceptance Criteria): Tiêu chí chấp nhận kỹ thuật của bài toán (AC-01 đến AC-17).\n"
                "• TC (Test Case): Ca kiểm thử chức năng theo kịch bản chuẩn (TC01 đến TC07).\n"
                "• PR (Pull Request): Yêu cầu tích hợp nhánh tính năng vào nhánh develop trên GitHub có sự xét duyệt.",
                callout_type="info")
    
    doc.add_page_break()

def build_part_1(doc):
    """Xây dựng Phần I: Tổng quan quy trình triển khai & Kiến trúc hệ thống."""
    add_styled_heading(doc, "PHẦN I. TỔNG QUAN QUY TRÌNH TRIỂN KHAI & KIẾN TRÚC HỆ THỐNG", level=1)
    
    add_styled_heading(doc, "1.1. Bối cảnh dự án & Mục tiêu tối thượng trong 120 phút", level=2)
    add_p(doc, "Bài tập nhóm học phần Lập trình Python Nâng Cao yêu cầu xây dựng một ứng dụng hoàn chỉnh hỗ trợ Lớp trưởng quản lý phòng thực hành máy tính có quy mô 12 chỗ ngồi, bố trí theo cấu trúc ma trận 3 hàng × 4 cột (tương ứng các mã máy: A1–A4, B1–B4, C1–C4). Hệ thống quản lý danh sách sinh viên với tối thiểu 100 hồ sơ (từ SV001 đến SV100) và bắt buộc sử dụng hệ quản trị cơ sở dữ liệu SQLite cục bộ để lưu trữ trạng thái bền vững.")
    add_p(doc, "Mục tiêu tối thượng của nhóm là hoàn thành toàn bộ yêu cầu đề bài trong khung thời gian giới hạn 120 phút. Để đạt được mục tiêu này mà không rơi vào tình trạng 'vỡ trận' khi ghép code ở những phút cuối, toàn bộ 5 thành viên phải làm việc theo một quy chuẩn kỹ thuật thống nhất, chia sẻ cùng một tầm nhìn kiến trúc và tuân thủ tuyệt đối sự điều phối của Technical Lead.")
    
    add_styled_heading(doc, "1.2. Kiến trúc tổng thể 3 tầng (3-Tier Layered Architecture)", level=2)
    add_p(doc, "Thay vì viết code theo kiểu 'Monolithic' (dồn toàn bộ giao diện, câu lệnh SQL và logic xếp chỗ vào một file duy nhất), hệ thống được thiết kế chuẩn mực theo mô hình kiến trúc 3 tầng phân lập (3-Tier Architecture):")
    
    add_bullet(doc, "Tầng giao diện người dùng (Presentation Layer - UI): Bao gồm main.py và ui.py do TV1 phụ trách. Tầng này chịu trách nhiệm hiển thị cửa sổ Tkinter, lưới 12 nút máy tính, ô nhập liệu mã sinh viên, các nút chức năng (Xếp chỗ, Tra cứu, Trả chỗ), nhãn bộ đếm và hiển thị các hộp thoại thông báo. Tầng giao diện TUYỆT ĐỐI KHÔNG chứa câu lệnh SQL nào.", bold_prefix="1. Presentation Layer (UI): ")
    add_bullet(doc, "Tầng xử lý nghiệp vụ (Business Logic / Services Layer): Bao gồm seat_service.py (TV2 phụ trách), student_service.py (TV3 phụ trách) và statistics.py (TV3 phụ trách). Tầng này đóng vai trò là 'bộ não' của ứng dụng, tiếp nhận yêu cầu từ UI, kiểm tra tính hợp lệ dữ liệu, kiểm tra ràng buộc phòng máy và gọi tầng Data để ghi/đọc dữ liệu.", bold_prefix="2. Business Logic Layer (Services): ")
    add_bullet(doc, "Tầng truy cập dữ liệu (Data Access Layer - Database): Bao gồm database.py, tao_du_lieu_demo.py và tệp CSDL phong_may.db do TV4 phụ trách. Tầng này đảm nhận việc tạo kết nối SQLite, bật cơ chế ràng buộc khóa ngoại (PRAGMA foreign_keys = ON), khởi tạo bảng nếu chưa có và sinh dữ liệu demo an toàn.", bold_prefix="3. Data Access Layer (Database): ")
    
    # Chèn sơ đồ kiến trúc
    add_image_box(doc, "diagram_architecture.png", "Kiến trúc phân tầng 3-Tier của Ứng dụng Quản lý Phòng máy 12 chỗ", width_inches=6.2)
    
    add_styled_heading(doc, "1.3. Phân định trách nhiệm module & Cơ chế giao tiếp liên tầng", level=2)
    add_p(doc, "Bảng dưới đây quy định ranh giới trách nhiệm và luồng dữ liệu trao đổi giữa các module:")
    
    headers_resp = ["Tầng / Module", "Người phụ trách", "Tệp mã nguồn", "Trách nhiệm chính", "Giao tiếp đầu vào / đầu ra"]
    data_resp = [
        ["Presentation (UI)", "TV1", "ui.py\nmain.py", "Dựng GUI Tkinter, hiển thị 12 nút, bắt sự kiện click, hiển thị bộ đếm & thông báo.", "Input: Nhập liệu từ User\nOutput: Gọi hàm Service và refresh UI"],
        ["Seat Service", "TV2", "seat_service.py", "Xử lý nghiệp vụ xếp chỗ, trả chỗ, kiểm tra chỗ trống, kiểm tra sinh viên đã xếp chưa.", "Input: ma_cho, ma_sv\nOutput: Tuple (bool, message)"],
        ["Student & Stats", "TV3", "student_service.py\nstatistics.py", "Tra cứu SV (phân biệt 3 trạng thái); Thống kê số chỗ đã dùng, còn trống, lập seat_map 12 vị trí.", "Input: ma_sv\nOutput: Dict SV, Tuple Stats, Dict Seat Map"],
        ["Database Layer", "TV4", "database.py\ntao_du_lieu_demo.py", "Quản lý kết nối SQLite, cấu hình khóa ngoại, tạo bảng DDL, sinh 100 SV demo an toàn.", "Input: Lệnh DDL/DML, số lượng n\nOutput: Connection SQLite, phong_may.db"],
        ["Testing & Int.", "TV5", "tests/\ntest_scenarios.md", "Thiết lập cấu trúc dự án, điều phối Git, viết test case, review PR, tích hợp và nghiệm thu.", "Input: Toàn bộ module của nhóm\nOutput: Test Report, Build ổn định v1.0"]
    ]
    add_styled_table(doc, headers_resp, data_resp, col_widths=[1.2, 0.8, 1.2, 2.1, 1.5])
    
    add_styled_heading(doc, "1.4. Năm nguyên tắc kỹ thuật cốt lõi bất khả xâm phạm", level=2)
    add_p(doc, "Để bảo đảm dự án về đích an toàn, tất cả các thành viên phải khắc cốt ghi tâm 5 nguyên tắc sau:")
    
    add_callout(doc, "NGUYÊN TẮC 1: PHÂN TÁCH TRÁCH NHIỆM TUYỆT ĐỐI (SEPARATION OF CONCERNS)",
                "Không bao giờ viết toàn bộ mã nguồn vào một tệp duy nhất. Mỗi thành viên chỉ làm việc trong tệp mã nguồn được phân công. "
                "Bất kỳ sự can thiệp chéo nào mà không thông qua TV5 đều bị từ chối khi duyệt Pull Request.", callout_type="warning")
                
    add_callout(doc, "NGUYÊN TẮC 2: GIAO DIỆN 'MỎNG' (THIN CLIENT) – CẤM VIẾT SQL TRONG UI",
                "Trong file ui.py của TV1, TUYỆT ĐỐI KHÔNG ĐƯỢC CÓ bất kỳ dòng lệnh 'import sqlite3' hoặc câu lệnh SQL 'SELECT/INSERT/DELETE' nào! "
                "Giao diện chỉ có nhiệm vụ lấy dữ liệu người dùng nhập, gọi hàm của TV2/TV3 và hiển thị kết quả trả về lên màn hình.", callout_type="warning")
                
    add_callout(doc, "NGUYÊN TẮC 3: DÙNG CHUNG MỘT CẤU TRÚC CƠ SỞ DỮ LIỆU DUY NHẤT (SINGLE SCHEMA)",
                "Chỉ có TV4 được quyền thiết kế và chỉnh sửa cấu trúc bảng trong database.py. Các thành viên TV2, TV3 bắt buộc phải truy vấn "
                "dựa trên đúng tên bảng ('sinh_vien', 'xep_cho') và tên cột ('ma_sv', 'ho_ten', 'ma_cho') do TV4 định nghĩa.", callout_type="info")
                
    add_callout(doc, "NGUYÊN TẮC 4: THỐNG NHẤT HỢP ĐỒNG GIAO DIỆN (API CONTRACT FIRST) TRƯỚC KHI CODE",
                "Trước khi viết dòng code logic đầu tiên, toàn bộ nhóm phải thống nhất danh sách hàm, tham số đầu vào và kiểu dữ liệu trả về. "
                "Không một ai được tự ý đổi tên hàm hoặc đổi kiểu trả về (ví dụ: đổi từ Tuple (bool, str) sang boolean thuần túy).", callout_type="info")

    add_callout(doc, "NGUYÊN TẮC 5: LẬP TRÌNH PHÒNG THỦ & CHỐNG SQL INJECTION",
                "Mọi câu lệnh truy vấn SQL trong hệ thống bắt buộc phải dùng tham số hóa dấu hỏi chấm (?, ?). "
                "Tuyệt đối cấm nối chuỗi f-string (ví dụ: f'SELECT * FROM sinh_vien WHERE ma_sv = \"{ma_sv}\"'). "
                "Mọi thao tác ghi dữ liệu phải có try...except bắt sqlite3.IntegrityError để tránh sập ứng dụng.", callout_type="warning")

def build_part_2(doc):
    """Xây dựng Phần II: Danh sách Task và Thứ tự thực hiện."""
    add_styled_heading(doc, "PHẦN II. DANH SÁCH TASK VÀ THỨ TỰ THỰC HIỆN", level=1)
    
    add_styled_heading(doc, "2.1. Ma trận phân bổ 10 Task kỹ thuật", level=2)
    add_p(doc, "Dự án được chia thành 10 Task kỹ thuật rõ ràng, có phân công phụ trách chính, người hỗ trợ/review, điều kiện phụ thuộc và thời lượng dự kiến trong sprint 120 phút:")
    
    headers_task = ["Mã Task", "Tên Task & Nội dung chính", "Người phụ trách", "Phụ thuộc", "Thời lượng", "Loại hình thực thi"]
    data_task = [
        ["TASK-01", "Khởi tạo GitHub Repo, cấu trúc thư mục & API Contract", "TV5 + Cả nhóm", "Không", "15 phút", "Tuần tự (Bắt buộc làm đầu tiên)"],
        ["TASK-02", "Thiết kế SQLite Schema & Module database.py", "TV4 (TV5 review)", "TASK-01", "20 phút", "Tuần tự (Nền tảng cho các Service)"],
        ["TASK-03", "Xây dựng Script sinh dữ liệu demo 100 sinh viên", "TV4 (TV5 review)", "TASK-02", "15 phút", "Song song với TASK-04, 05, 06"],
        ["TASK-04", "Xây dựng Module nghiệp vụ Xếp chỗ và Trả chỗ", "TV2 (TV4 hỗ trợ)", "TASK-02", "35 phút", "Song song với TASK-03, 05, 06"],
        ["TASK-05", "Xây dựng Module Tra cứu sinh viên & Thống kê chỗ", "TV3 (TV4 hỗ trợ)", "TASK-02", "35 phút", "Song song với TASK-03, 04, 06"],
        ["TASK-06", "Xây dựng Giao diện người dùng Tkinter 12 chỗ ngồi", "TV1 (TV5 hỗ trợ)", "TASK-01, API", "45 phút", "Song song (Dựng mockup trước, ráp API sau)"],
        ["TASK-07", "Kiểm thử đơn vị độc lập từng module (Unit Test)", "Từng TV (TV5 soát)", "TASK-03 đến 06", "20 phút", "Song song giữa các thành viên"],
        ["TASK-08", "Tích hợp các module vào luồng ứng dụng hoàn chỉnh", "TV5 chủ trì + Nhóm", "TASK-07", "20 phút", "Tuần tự (Tích hợp tập trung)"],
        ["TASK-09", "Kiểm thử tích hợp hệ thống (SIT) và Sửa lỗi", "TV5 + Thành viên", "TASK-08", "15 phút", "Tuần tự (Chạy kịch bản TC01–TC07)"],
        ["TASK-10", "Hoàn thiện tài liệu, đóng gói sản phẩm & Nghiệm thu", "Cả nhóm", "TASK-09", "10 phút", "Tuần tự (Đóng gói thư mục sạch)"]
    ]
    add_styled_table(doc, headers_task, data_task, col_widths=[0.9, 2.5, 1.2, 1.0, 0.9, 1.3])
    
    add_styled_heading(doc, "2.2. Phân tích luồng thực thi: Tuần tự vs. Song song", level=2)
    add_p(doc, "Trong điều kiện thời gian thi công chỉ có 120 phút, việc hiểu rõ Task nào phải chờ và Task nào có thể triển khai song song là chìa khóa then chốt để nhóm tối ưu hóa năng suất:")
    
    add_bullet(doc, "TASK-01 và TASK-02 bắt buộc phải chạy TUẦN TỰ đầu tiên. Không một ai được phép code nghiệp vụ nếu chưa có cấu trúc dự án và chưa có CSDL SQLite mẫu. Cả nhóm phải dành trọn 15 phút đầu cùng TV5 chốt danh sách hàm.", bold_prefix="1. Giai đoạn thiết lập nền tảng (0–35 phút): ")
    add_bullet(doc, "Sau khi TV4 hoàn thành TASK-02 và đẩy nhánh feature/database lên develop, 4 luồng công việc sẽ chạy HOÀN TOÀN SONG SONG: TV4 sinh 100 sinh viên (TASK-03); TV2 code logic xếp/trả chỗ (TASK-04); TV3 code tra cứu/thống kê (TASK-05); TV1 code giao diện Tkinter và kết nối hàm (TASK-06).", bold_prefix="2. Giai đoạn bứt phá song song (35–65 phút): ")
    add_bullet(doc, "Mỗi thành viên tự chạy script test module của mình (TASK-07). Khi pass toàn bộ, tạo Pull Request vào nhánh develop.", bold_prefix="3. Giai đoạn kiểm thử độc lập (55–75 phút): ")
    add_bullet(doc, "TV5 kéo mã nguồn từ develop, ráp nối thành tệp main.py hoàn chỉnh (TASK-08), chạy kịch bản kiểm thử tích hợp (TASK-09) và hoàn tất hồ sơ nộp bài (TASK-10).", bold_prefix="4. Giai đoạn tích hợp và nghiệm thu (75–120 phút): ")

    add_styled_heading(doc, "2.3. Sơ đồ luồng phụ thuộc Task (Task Dependency Flowchart)", level=2)
    add_p(doc, "Dưới đây là sơ đồ trực quan hóa mối quan hệ phụ thuộc giữa 10 Task kỹ thuật:")
    
    add_image_box(doc, "diagram_task_flow.png", "Sơ đồ luồng phụ thuộc và tiến trình thực thi 10 Task kỹ thuật", width_inches=6.2)
    
    add_p(doc, "Mã nguồn biểu diễn sơ đồ bằng cú pháp Mermaid tiêu chuẩn:")
    mermaid_code = """graph TD
    T01["TASK-01: Setup GitHub & API Contract<br/>(TV5 + Cả nhóm | 0-15m)"] --> T02["TASK-02: SQLite Schema & database.py<br/>(TV4 | 15-35m)"]
    T01 -.->|Thống nhất API| T06["TASK-06: Tkinter UI 12 chỗ<br/>(TV1 | 15-65m)"]
    T02 --> T03["TASK-03: Seed 100 SV Demo<br/>(TV4 | 35-50m)"]
    T02 --> T04["TASK-04: Xếp & Trả chỗ<br/>(TV2 | 25-60m)"]
    T02 --> T05["TASK-05: Tra cứu & Thống kê<br/>(TV3 | 25-60m)"]
    T03 --> T07["TASK-07: Unit Testing từng Module<br/>(Từng TV & TV5 | 55-75m)"]
    T04 --> T07
    T05 --> T07
    T06 --> T07
    T07 --> T08["TASK-08: Tích hợp Module vào main.py<br/>(TV5 chủ trì | 75-95m)"]
    T08 --> T09["TASK-09: Kiểm thử tích hợp SIT<br/>(TV5 & Nhóm | 95-110m)"]
    T09 --> T10["TASK-10: Đóng gói & Nghiệm thu v1.0<br/>(Cả nhóm | 110-120m)"]
    
    classDef startEnd fill:#E8EEF5,stroke:#1B365D,stroke-width:2px;
    classDef parallel fill:#E8F5E9,stroke:#388E3C,stroke-width:1.5px;
    classDef test fill:#FFF9C4,stroke:#FBC02D,stroke-width:1.5px;
    classDef integ fill:#FFCDD2,stroke:#D32F2F,stroke-width:2px;
    class T01,T02 startEnd;
    class T03,T04,T05,T06 parallel;
    class T07 test;
    class T08,T09,T10 integ;"""
    add_code_block(doc, mermaid_code, language="Mermaid Syntax")

    add_styled_heading(doc, "2.4. Kế hoạch điều phối dòng thời gian Sprint 120 phút", level=2)
    add_p(doc, "Nhóm phải bám sát từng mốc thời gian dưới đây. Trưởng nhóm TV5 có trách nhiệm nhắc giờ (time-boxing) cho cả nhóm:")
    
    headers_time = ["Khung thời gian", "Mục tiêu cần đạt của cả nhóm", "Hành động cụ thể của từng thành viên"]
    data_time = [
        ["00 – 10 phút", "Chốt thiết kế & API Contract", "Đọc kỹ đề; thống nhất tên bảng, tên cột, tên hàm, kiểu trả về; tạo repo Git chung."],
        ["10 – 35 phút", "Có CSDL & Khung Module lõi", "TV4 tạo database.py + init_db(); TV1 dựng layout GUI 3x4; TV2/TV3 tạo file service; TV5 soạn test."],
        ["35 – 65 phút", "Hoàn thành code logic độc lập", "TV4 sinh 100 SV; TV2 hoàn tất assign/release; TV3 hoàn tất find/stats; TV1 gắn hàm mock vào GUI."],
        ["65 – 80 phút", "Kiểm thử độc lập & Tạo PR", "Mỗi thành viên tự chạy script test; TV5 review PR và merge các nhánh tính năng vào develop."],
        ["80 – 100 phút", "Ráp nối & Tích hợp hoàn chỉnh", "TV5 chủ trì ghép ui.py + services + database.py; chạy ứng dụng thực tế từ main.py."],
        ["100 – 115 phút", "Kiểm thử toàn diện TC01–TC07", "Chạy lại đủ 7 kịch bản kiểm thử bắt buộc; kiểm tra đóng/mở ứng dụng lưu trạng thái SQLite; sửa bug."],
        ["115 – 120 phút", "Đóng gói & Chuẩn bị bảo vệ", "Dọn dẹp code rác; điền bảng đóng góp; kiểm tra chạy sạch trên thư mục mới; sẵn sàng demo."]
    ]
    add_styled_table(doc, headers_time, data_time, col_widths=[1.3, 2.3, 3.2])
    
    doc.add_page_break()

print("Part 1 & 2 module initialized successfully!")
