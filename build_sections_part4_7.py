import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from generator_core import (
    COLOR_PRIMARY_NAVY, COLOR_SECONDARY_BLUE, COLOR_ACCENT_BLUE,
    COLOR_BG_GRAY, COLOR_BORDER_GRAY,
    add_styled_heading, add_p, add_bullet, add_callout,
    add_code_block, add_styled_table, add_image_box
)

def build_part_4(doc):
    """Xây dựng Phần IV: Quy trình làm việc với Git/GitHub."""
    add_styled_heading(doc, "PHẦN IV. QUY TRÌNH LÀM VIỆC VỚI GIT/GITHUB (TRÁNH XUNG ĐỘT)", level=1)
    
    add_styled_heading(doc, "4.1. Chiến lược phân nhánh Git Flow rút gọn (Sprint 120 phút)", level=2)
    add_p(doc, "Trong một sprint làm việc nhóm ngắn hạn (120 phút), việc quản lý mã nguồn lỏng lẻo sẽ ngay lập tức dẫn đến xung đột (merge conflict) nghiêm trọng hoặc làm mất code của nhau. Nhóm bắt buộc áp dụng mô hình phân nhánh Git Flow rút gọn dưới sự điều phối trung tâm của TV5:")
    
    add_bullet(doc, "main: Nhánh ổn định cao nhất, chỉ chứa các bản phát hành hoàn thiện (Release v1.0). TUYỆT ĐỐI CẤM push code trực tiếp vào main.", bold_prefix="• Nhánh main: ")
    add_bullet(doc, "develop: Nhánh tích hợp chính của nhóm. Mọi tính năng sau khi được kiểm thử đơn vị sẽ được hợp nhất vào develop qua Pull Request. Nhánh này phản ánh trạng thái mới nhất của sản phẩm tích hợp.", bold_prefix="• Nhánh develop: ")
    add_bullet(doc, "feature/database: Nhánh riêng của TV4 phụ trách SQLite DDL và script sinh dữ liệu demo.", bold_prefix="• Nhánh feature/database: ")
    add_bullet(doc, "feature/seat-management: Nhánh riêng của TV2 phụ trách nghiệp vụ xếp chỗ và trả chỗ.", bold_prefix="• Nhánh feature/seat-management: ")
    add_bullet(doc, "feature/student-search: Nhánh riêng của TV3 phụ trách tra cứu sinh viên và thống kê chỗ ngồi.", bold_prefix="• Nhánh feature/student-search: ")
    add_bullet(doc, "feature/ui: Nhánh riêng của TV1 phụ trách giao diện Tkinter 12 nút và bắt sự kiện.", bold_prefix="• Nhánh feature/ui: ")
    add_bullet(doc, "feature/testing: Nhánh riêng của TV5 phụ trách viết kịch bản kiểm thử tích hợp và tổng hợp báo cáo.", bold_prefix="• Nhánh feature/testing: ")
    
    # Chèn hình ảnh Git Workflow
    add_image_box(doc, "diagram_git_workflow.png", "Mô hình phân nhánh Git Flow rút gọn cho nhóm 05 thành viên trong 120 phút", width_inches=6.2)
    
    add_styled_heading(doc, "4.2. Hướng dẫn thực hành 6 bước làm việc với Git hàng ngày", level=2)
    add_p(doc, "Dưới đây là cẩm nang các câu lệnh Git chuẩn xác, từng thành viên chỉ cần copy và thực hiện theo đúng trình tự:")
    
    add_styled_heading(doc, "Bước 1: TV5 khởi tạo Repository và cấu hình ban đầu", level=3)
    add_p(doc, "TV5 thực thi các lệnh sau tại máy trạm:")
    code_git_step1 = """# 1. Khởi tạo kho chứa Git cục bộ
git init
git branch -M main

# 2. Thêm file cấu hình và commit ban đầu
git add .gitignore README.md
git commit -m "chore: initial project structure and gitignore"

# 3. Tạo nhánh develop và đẩy lên GitHub
git branch develop
git remote add origin https://github.com/your-team/room-seat-manager-python.git
git push -u origin main
git push -u origin develop
"""
    add_code_block(doc, code_git_step1, language="Git: Bước 1 (TV5)")
    
    add_styled_heading(doc, "Bước 2: Các thành viên lấy mã nguồn và tạo nhánh tính năng", level=3)
    add_p(doc, "Các thành viên TV1, TV2, TV3, TV4 mở terminal trên máy tính của mình và gõ:")
    code_git_step2 = """# 1. Clone repository về máy
git clone https://github.com/your-team/room-seat-manager-python.git
cd room-seat-manager-python

# 2. Chuyển sang nhánh develop và đồng bộ mới nhất
git checkout develop
git pull origin develop

# 3. Tạo và chuyển ngay sang nhánh tính năng của mình (Ví dụ TV2):
git checkout -b feature/seat-management
"""
    add_code_block(doc, code_git_step2, language="Git: Bước 2 (TV1 - TV4)")

    add_styled_heading(doc, "Bước 3: Quy chuẩn Commit & Push trong quá trình code", level=3)
    add_p(doc, "Trong quá trình code, thành viên phải liên tục kiểm tra trạng thái và commit các thay đổi có ý nghĩa. Tuyệt đối không commit file rác:")
    code_git_step3 = """# 1. Kiểm tra trạng thái các file đã sửa
git status

# 2. Thêm các file cụ thể thuộc phần việc của mình
git add seat_service.py

# 3. Commit kèm thông điệp rõ ràng theo chuẩn Conventional Commits
git commit -m "feat(seat): implement seat assignment with constraint validation"

# 4. Đẩy nhánh tính năng lên GitHub Remote
git push -u origin feature/seat-management
"""
    add_code_block(doc, code_git_step3, language="Git: Bước 3 (Commit & Push)")

    add_styled_heading(doc, "4.3. Quy chuẩn viết Commit Message theo Conventional Commits", level=2)
    add_p(doc, "Cả nhóm thống nhất quy tắc đặt thông điệp commit theo chuẩn Conventional Commits với cấu trúc: `<type>(<scope>): <mô tả ngắn bằng tiếng Anh hoặc tiếng Việt>`:")
    
    headers_commit = ["Loại Commit", "Mục đích sử dụng", "Ví dụ cụ thể"]
    data_commit = [
        ["feat(database)", "Khởi tạo hoặc cập nhật cấu trúc bảng SQLite", "feat(database): initialize SQLite schema with foreign keys"],
        ["feat(seed)", "Xây dựng tính năng sinh dữ liệu demo", "feat(seed): generate 100 demo students with safe loop"],
        ["feat(seat)", "Cài đặt nghiệp vụ xếp chỗ hoặc trả chỗ", "feat(seat): implement assign_seat and release_seat"],
        ["feat(search)", "Cài đặt chức năng tra cứu và thống kê", "feat(search): implement student lookup with LEFT JOIN"],
        ["feat(ui)", "Dựng giao diện người dùng Tkinter", "feat(ui): create 12-seat layout and action buttons"],
        ["test(integration)", "Thực hiện kiểm thử tích hợp", "test(integration): verify seat assignment end-to-end flow"],
        ["fix(seat)", "Sửa lỗi nghiệp vụ phát sinh", "fix(seat): correct student already seated check condition"],
        ["docs(readme)", "Cập nhật tài liệu hướng dẫn", "docs(readme): update API contract and setup instructions"]
    ]
    add_styled_table(doc, headers_commit, data_commit, col_widths=[1.5, 2.3, 3.0])

    add_styled_heading(doc, "4.4. Quy trình tạo Pull Request & Tiêu chí Code Review của TV5", level=2)
    add_p(doc, "Khi một thành viên hoàn thành và tự kiểm thử module (DoD) thành công, thành viên đó sẽ tạo một Pull Request (PR) trên giao diện web GitHub theo quy trình sau:")
    
    add_bullet(doc, "Tiêu đề PR: Rõ ràng, ví dụ: '[Feature] TV2 - Hoàn thành module seat_service.py'.")
    add_bullet(doc, "Nhánh đích: BẮT BUỘC chọn nhánh đích là `develop` (TUYỆT ĐỐI KHÔNG chọn main).")
    add_bullet(doc, "Mô tả PR: Liệt kê các hàm đã viết, kết quả tự kiểm thử đơn vị, đính kèm bằng chứng (ảnh chụp terminal PASS).")
    add_bullet(doc, "Người kiểm duyệt (Reviewer): BẮT BUỘC gán TV5 và ít nhất một thành viên phụ thuộc liên quan (ví dụ: TV1 review PR của TV2).")
    
    add_callout(doc, "TIÊU CHÍ DUYỆT PULL REQUEST CỦA TV5 (CODE REVIEW CHECKLIST)",
                "TV5 chỉ bấm nút 'Merge Pull Request' khi thỏa mãn đầy đủ 4 điều kiện:\n"
                "1. Code không có lỗi cú pháp và chạy được độc lập.\n"
                "2. Tên hàm, tham số và kiểu trả về khớp 100% với Hợp đồng API Contract (TASK-01).\n"
                "3. Không có câu lệnh SQL nguy hiểm (như DROP TABLE, xóa bảng sinh_vien).\n"
                "4. Không sửa đổi trái phép các tệp mã nguồn thuộc sở hữu của thành viên khác.", callout_type="success")

    add_styled_heading(doc, "4.5. Hướng dẫn chi tiết cách phát hiện và giải quyết Conflict trên VS Code", level=2)
    add_p(doc, "Xung đột mã nguồn (Merge Conflict) xảy ra khi hai thành viên cùng sửa đổi một dòng hoặc một vùng code trong cùng một tệp và cùng cố gắng hợp nhất vào nhánh develop. Dưới đây là hướng dẫn thực hành cách giải quyết triệt để:")
    
    add_p(doc, "Dấu hiệu nhận biết: Khi chạy lệnh `git merge develop` hoặc khi merge PR trên GitHub, Git sẽ chặn lại và báo `CONFLICT (content): Merge conflict in <file>`. Trong tệp mã nguồn sẽ xuất hiện các dấu phân tách đặc thù:", bold_prefix="1. Dấu hiệu nhận biết: ")
    
    code_conflict_sample = """<<<<<<< HEAD (Mã nguồn hiện tại trên máy của bạn)
def assign_seat(ma_cho: str, ma_sv: str):
    # Cách viết của TV2: Trả về Tuple (bool, str)
    return True, "Thành công"
=======
def assign_seat(ma_cho: str, ma_sv: str):
    # Cách viết cũ trên develop: Trả về boolean thuần túy
    return True
>>>>>>> develop (Mã nguồn kéo từ nhánh develop về)
"""
    add_code_block(doc, code_conflict_sample, language="Git Conflict Markers")
    
    add_p(doc, "Quy trình 4 bước giải quyết Conflict chuyên nghiệp trong VS Code:", bold_prefix="2. Các bước xử lý trong VS Code: ")
    add_bullet(doc, "Bước 1: Mở tệp bị conflict trong VS Code. VS Code sẽ tự động làm nổi bật vùng xung đột kèm 4 nút bấm tiện ích ở phía trên:")
    add_bullet(doc, "   • 'Accept Current Change': Giữ lại mã nguồn hiện tại của bạn, bỏ mã nguồn của develop.")
    add_bullet(doc, "   • 'Accept Incoming Change': Lấy mã nguồn mới từ develop về, bỏ mã nguồn của bạn.")
    add_bullet(doc, "   • 'Accept Both Changes': Giữ cả hai đoạn mã.")
    add_bullet(doc, "   • 'Compare Changes': Mở cửa sổ so sánh hai bên song song.")
    add_bullet(doc, "Bước 2: Dựa vào Hợp đồng API Contract đã thống nhất, bấm chọn phương án chuẩn xác nhất (hoặc trực tiếp xóa các ký tự `<<<<<<<`, `=======`, `>>>>>>>` và tự chỉnh sửa nội dung hoàn chỉnh bằng tay).")
    add_bullet(doc, "Bước 3: Lưu tệp (Ctrl + S), mở terminal chạy lệnh đánh dấu đã giải quyết: `git add <tên_file>`.")
    add_bullet(doc, "Bước 4: Hoàn tất quá trình merge bằng lệnh commit: `git commit -m 'fix: resolve merge conflict with develop'` và push lên lại nhánh feature.")

    add_styled_heading(doc, "4.6. Hướng dẫn đặc biệt: Quản lý tệp SQLite phong_may.db trên Git", level=2)
    add_callout(doc, "NGUYÊN TẮC VÀNG VỀ QUẢN LÝ TỆP DATABASE TRÊN GIT",
                "Tệp cơ sở dữ liệu SQLite (phong_may.db) là một tệp nhị phân (binary file). "
                "Git KHÔNG THỂ phân tích dòng (line-by-line) trên tệp nhị phân, do đó nếu hai thành viên cùng commit tệp phong_may.db, "
                "Git sẽ báo conflict không thể tự giải quyết tự động và có nguy cơ làm hỏng toàn bộ CSDL!\n\n"
                "GIẢI PHÁP CHUẨN CỦA TECH LEAD:\n"
                "1. Trong suốt quá trình code (từ phút 0 đến phút 100), các thành viên chạy trên tệp CSDL sinh cục bộ tại máy cá nhân thông qua script `python tao_du_lieu_demo.py`.\n"
                "2. Chỉ duy nhất TV5 (hoặc TV4 theo ủy quyền của TV5) được quyền commit tệp `phong_may.db` sạch ban đầu lên nhánh develop trong TASK-08 phục vụ nghiệm thu.", 
                callout_type="warning")
    
    doc.add_page_break()

def build_part_5(doc):
    """Xây dựng Phần V: Quy trình tích hợp module."""
    add_styled_heading(doc, "PHẦN V. QUY TRÌNH TÍCH HỢP MODULE & KỊCH BẢN THỰC THI", level=1)
    
    add_styled_heading(doc, "5.1. Thứ tự tích hợp 6 bước từ Data đến Presentation", level=2)
    add_p(doc, "Tích hợp không phải là việc dồn toàn bộ code vào nhau ở phút thứ 110. Nhóm phải thực hiện tích hợp theo thứ tự phân tầng 6 bước chuẩn mực sau:")
    
    headers_integ = ["Thứ tự", "Hành động tích hợp", "Người thực hiện", "Đầu vào cần có", "Kết quả thẩm định"]
    data_integ = [
        ["Bước 1", "TV4 bàn giao database.py & phong_may.db", "TV4 → TV5", "Schema CSDL hoàn chỉnh", "TV5 xác nhận bảng, khóa ngoại và 100 SV demo sẵn sàng."],
        ["Bước 2", "TV2 và TV3 kết nối vào database.py", "TV2, TV3", "Hàm get_connection()", "Các hàm nghiệp vụ truy vấn thành công trên CSDL thật."],
        ["Bước 3", "TV1 liên kết các hàm của TV2 và TV3 vào GUI", "TV1", "API của seat_service & student_service", "Nút bấm GUI kích hoạt đúng hàm logic nghiệp vụ."],
        ["Bước 4", "TV5 kiểm tra tương thích và biên dịch tích hợp", "TV5 điều phối", "Toàn bộ nhánh merge vào develop", "Chạy main.py không phát sinh ImportError."],
        ["Bước 5", "Cả nhóm chạy thử luồng End-to-End thực tế", "Cả nhóm", "main.py hoàn chỉnh", "Thao tác trên GUI làm thay đổi đúng dữ liệu trong SQLite."],
        ["Bước 6", "Phát hiện lỗi, phân loại Bug và Re-test", "TV5 + Thành viên", "Bug Report nội bộ", "Sửa lỗi tận gốc, đóng bug và xác nhận Release v1.0."]
    ]
    add_styled_table(doc, headers_integ, data_integ, col_widths=[0.8, 2.5, 1.2, 1.3, 1.4])
    
    add_styled_heading(doc, "5.2. Minh họa luồng thực thi hoàn chỉnh (End-to-End Trace)", level=2)
    add_p(doc, "Để cả 5 thành viên hình dung rõ nét cách các module phối hợp với nhau trong một kịch bản người dùng thực tế, dưới đây là luồng xử lý chi tiết từng bước khi Lớp trưởng thực hiện thao tác Xếp sinh viên SV100 vào chỗ A2:")
    
    # Chèn sơ đồ Sequence Flow
    add_image_box(doc, "diagram_sequence_flow.png", "Biểu đồ tuần tự (Sequence Diagram) minh họa luồng xử lý xếp chỗ A2 cho SV100", width_inches=6.2)
    
    add_p(doc, "Phân tích chi tiết 6 pha xử lý trong luồng:", bold_prefix="Chi tiết các bước thực thi: ")
    add_bullet(doc, "Pha 1 (User Interaction): Người dùng click chuột vào nút máy A2 trên giao diện Tkinter. Giao diện đổi viền nút A2 sang nét đậm và lưu `selected_seat = 'A2'`. Người dùng gõ 'SV100' vào ô nhập liệu và bấm nút [Xếp chỗ].")
    add_bullet(doc, "Pha 2 (UI Dispatch): Giao diện bắt sự kiện click, lấy giá trị từ ô nhập, kiểm tra tính hợp lệ sơ bộ và gọi hàm: `success, msg = assign_seat('A2', 'SV100')`.")
    add_bullet(doc, "Pha 3 (Service Validation): Module `seat_service.py` tiếp nhận yêu cầu, kiểm tra: (1) A2 nằm trong VALID_SEATS; (2) Truy vấn `sinh_vien` thấy SV100 tồn tại; (3) Truy vấn `xep_cho` thấy A2 đang trống; (4) Truy vấn `xep_cho` thấy SV100 chưa có chỗ ở bất kỳ vị trí nào.")
    add_bullet(doc, "Pha 4 (Database Persistence): Module `seat_service.py` thực thi câu lệnh SQL: `INSERT INTO xep_cho(ma_cho, ma_sv) VALUES ('A2', 'SV100');` và gọi `conn.commit()`. Bản ghi mới được lưu trữ bền vững vào tệp CSDL `phong_may.db`.")
    add_bullet(doc, "Pha 5 (Return Response): `seat_service.py` trả về Tuple: `(True, 'Xếp chỗ thành công! Sinh viên SV100 vào vị trí A2.')`.")
    add_bullet(doc, "Pha 6 (UI Refresh & Synchronization): Giao diện nhận kết quả `True`, hiển thị popup thông báo thành công, xóa trắng ô nhập liệu và ngay lập tức kích hoạt hàm `refresh_ui()`. Hàm này gọi `get_seat_map()` và `get_seat_stats()`, khiến nút A2 chuyển sang màu xanh lá với nhãn 'A2\\n[SV100]', đồng thời thanh bộ đếm cập nhật thành: 'ĐÃ SỬ DỤNG: 1 / 12 | CÒN TRỐNG: 11'.")

    add_styled_heading(doc, "5.3. Bảng phân tích các sự cố tích hợp kinh điển và biện pháp xử lý", level=2)
    add_p(doc, "Dưới đây là cẩm nang xử lý sự cố (Troubleshooting Guide) dành cho TV5 và nhóm khi gặp lỗi trong quá trình ghép code:")
    
    headers_trouble = ["Hiện tượng lỗi / Thông báo", "Nguyên nhân cốt lõi", "Biện pháp khắc phục triệt để"]
    data_trouble = [
        ["ModuleNotFoundError: No module named 'seat_service'", "Do sai lệch đường dẫn thư mục làm việc (Working Directory) hoặc đặt file sai chỗ.", "Đảm bảo toàn bộ các tệp .py nằm cùng cấp thư mục gốc dự án. Chạy lệnh python từ thư mục gốc."],
        ["sqlite3.OperationalError: database is locked", "Một kết nối SQLite trước đó mở ra nhưng quên đóng (close) hoặc chưa commit, chiếm dụng file DB.", "Bắt buộc sử dụng cú pháp context manager 'with get_connection() as conn:' để kết nối tự giải phóng."],
        ["TypeError: cannot unpack non-iterable bool object", "Hàm nghiệp vụ trả về boolean thuần túy (True) thay vì Tuple (bool, str) như giao kèo.", "Kiểm tra lại hợp đồng API Contract. Hàm nghiệp vụ bắt buộc phải trả về Tuple 2 phần tử: (bool, message)."],
        ["sqlite3.IntegrityError: FOREIGN KEY constraint failed", "Cố gắng xếp chỗ cho một mã sinh viên không có trong bảng sinh_vien.", "Chạy lại script tao_du_lieu_demo.py để nạp đủ 100 sinh viên; kiểm tra hàm seat_service có validate trước khi INSERT."],
        ["Giao diện không cập nhật sau khi bấm Xếp chỗ thành công", "Quên không gọi hàm refresh_ui() bên trong khối xử lý 'if success:' của hàm handle_assign.", "Thêm lời gọi self.refresh_ui() ngay sau khi hiển thị messagebox thành công trong ui.py."]
    ]
    add_styled_table(doc, headers_trouble, data_trouble, col_widths=[2.0, 2.3, 2.5])
    
    doc.add_page_break()

def build_part_6(doc):
    """Xây dựng Phần VI: Checklist nghiệm thu."""
    add_styled_heading(doc, "PHẦN VI. CHECKLIST NGHIỆM THU & BỘ TIÊU CHÍ CHẤT LƯỢNG", level=1)
    
    add_styled_heading(doc, "6.1. Bảng 17 Tiêu chí chấp nhận toàn diện (AC-01 đến AC-17)", level=2)
    add_p(doc, "Toàn bộ sản phẩm bàn giao cuối cùng phải thỏa mãn tuyệt đối 17 tiêu chí chấp nhận kỹ thuật (Acceptance Criteria) dưới đây:")
    
    headers_ac = ["Mã AC", "Hạng mục kiểm tra", "Tiêu chí chấp nhận kỹ thuật", "Cách thức xác minh thực tế"]
    data_ac = [
        ["AC-01", "Khởi tạo dữ liệu", "Tệp phong_may.db được tạo; có đủ 2 bảng sinh_vien và xep_cho; lần đầu có đủ 100 SV001–SV100; xep_cho rỗng.", "Kiểm tra schema SQLite và truy vấn SELECT COUNT(*) = 100; xep_cho = 0."],
        ["AC-02", "Sinh dữ liệu lặp an toàn", "Chạy tao_du_lieu_demo.py hai lần không tạo hồ sơ trùng và không làm mất dữ liệu lượt xếp chỗ hiện có.", "Chèn 1 lượt xếp thử, chạy lại script, đối chiếu COUNT sinh_vien = 100 và lượt xếp vẫn còn."],
        ["AC-03", "Sơ đồ 12 vị trí máy", "Giao diện hiển thị đủ 12 nút A1–A4, B1–B4, C1–C4 theo bố cục 3×4; mỗi chỗ thể hiện Trống hoặc mã SV đang ngồi.", "Quan sát giao diện đồ họa đối chiếu đủ 12 mã máy và trạng thái khớp CSDL."],
        ["AC-04", "Bộ đếm chỗ ngồi", "Bộ đếm hiển thị số chỗ đã dùng trên tổng 12; giá trị luôn bằng COUNT(*) của bảng xep_cho.", "Đối chiếu bộ đếm ở các mốc: ban đầu 0/12, sau khi xếp 1/12, sau khi trả về 0/12."],
        ["AC-05", "Xếp chỗ hợp lệ", "Khi chọn chỗ trống và nhập mã SV tồn tại, chưa xếp, hệ thống lưu bản ghi và đổi màu nút hiển thị đúng mã SV.", "Xếp SV100 vào A2; kiểm tra giao diện đổi màu và SELECT * FROM xep_cho."],
        ["AC-06", "Từ chối chỗ đã có người", "Không cho xếp sinh viên khác vào chỗ đang có người; báo lý do rõ ràng; dữ liệu hiện tại không thay đổi.", "Thử xếp SV001 vào A2 khi A2 đang có SV100; A2 vẫn phải thuộc về SV100."],
        ["AC-07", "Từ chối SV đã có chỗ", "Không cho xếp cùng một sinh viên vào chỗ thứ hai; báo lý do; vị trí mới vẫn hoàn toàn trống.", "Khi SV100 ở A2, thử xếp SV100 vào B1; xác nhận B1 vẫn trống và xep_cho chỉ có 1 dòng."],
        ["AC-08", "Từ chối mã SV không tồn tại", "Không tạo lượt xếp nếu mã SV không có trong sinh_vien; thông báo rõ lỗi cho người dùng.", "Thử xếp mã SV999 vào A3; CSDL không phát sinh bản ghi mới."],
        ["AC-09", "Tra cứu SV đã xếp chỗ", "Tra cứu theo mã SV trả về đúng mã SV, họ tên và mã chỗ máy hiện tại đang ngồi.", "Tra cứu SV100 khi đang ngồi A2; kết quả popup hiển thị đúng A2."],
        ["AC-010", "Tra cứu SV chưa xếp chỗ", "Nếu hồ sơ tồn tại nhưng chưa có lượt xếp, hiển thị họ tên và trạng thái 'Chưa được xếp chỗ'; không báo lỗi không tìm thấy.", "Tra cứu SV100 trước khi xếp; thông báo 'Sinh viên 100 - Chưa được xếp chỗ'."],
        ["AC-011", "Tra cứu mã không tồn tại", "Nếu mã không có trong CSDL, hiển thị thông báo 'Không tìm thấy sinh viên'; không nhầm với trạng thái chưa xếp.", "Tra cứu SV999; hiển thị popup báo không tìm thấy rõ ràng."],
        ["AC-012", "Trả chỗ hợp lệ", "Trả chỗ đang có người sẽ xóa đúng bản ghi trong xep_cho; chỗ trở về Trống; hồ sơ sinh viên vẫn được giữ nguyên.", "Trả A2 của SV100; A2 thành Trống, bộ đếm giảm 1; bảng sinh_vien vẫn còn SV100."],
        ["AC-013", "Không trả chỗ trống", "Không phát sinh thay đổi dữ liệu khi người dùng yêu cầu trả một chỗ đang trống; giao diện cảnh báo phù hợp.", "Chọn nút B1 đang trống và bấm Trả chỗ; hệ thống cảnh báo và số lượng chỗ không đổi."],
        ["AC-014", "Đồng bộ giao diện", "Sau mỗi lần xếp hoặc trả thành công, sơ đồ 12 nút và bộ đếm tự động cập nhật ngay lập tức mà không cần khởi động lại.", "Thực hiện thao tác và quan sát giao diện cập nhật trạng thái trong vòng dưới 0.5 giây."],
        ["AC-015", "Lưu trạng thái khi mở lại", "Đóng hoàn toàn ứng dụng và mở lại, các lượt xếp chỗ đã lưu vẫn giữ nguyên vẹn; sơ đồ và bộ đếm khớp SQLite.", "Xếp SV100 vào A2, tắt cửa sổ Tkinter, chạy lại main.py, A2 vẫn hiển thị SV100 và bộ đếm 1/12."],
        ["AC-016", "Ràng buộc dữ liệu CSDL", "ma_sv là PK trong sinh_vien; ma_cho là PK trong xep_cho; ma_sv trong xep_cho là FK và UNIQUE.", "Kiểm tra DDL schema và thử execute chèn dữ liệu vi phạm, SQLite bắt buộc quăng IntegrityError."],
        ["AC-017", "Khả năng chạy bản nộp", "Bản nộp đầy đủ mã nguồn, script seed, phong_may.db và bảng đóng góp; chạy được từ đầu trong thư mục mới.", "Sao chép mã nguồn sang thư mục sạch và chạy python main.py thành công."]
    ]
    add_styled_table(doc, headers_ac, data_ac, col_widths=[0.8, 1.5, 2.7, 1.8])

    add_styled_heading(doc, "6.2. Kịch bản kiểm thử bắt buộc theo đề (TC01 đến TC07)", level=2)
    add_p(doc, "Bảng dưới đây là kịch bản nghiệm thu 7 bước thực hiện tuần tự trên một CSDL thử nghiệm mới để đối chiếu kết quả bàn giao:")
    
    headers_tc = ["Mã TC", "Mục tiêu kiểm thử", "Các bước thao tác thực tế", "Kết quả mong đợi bắt buộc", "Kết quả thực tế", "Đánh giá", "Người chạy"]
    data_tc = [
        ["TC01", "Kiểm tra CSDL & Seed lặp", "Chạy script sinh dữ liệu hai lần liên tiếp từ terminal.", "CSDL có đủ 100 SV; số dòng không tăng sau lần chạy thứ hai; xep_cho không bị reset.", "Đúng 100 sinh viên, không trùng lặp", "PASS", "TV5"],
        ["TC02", "Tra cứu SV chưa xếp", "Khởi động ứng dụng, nhập 'SV100' vào ô tìm kiếm, bấm [Tra cứu SV].", "Hiển thị thông tin 'Sinh viên 100' kèm trạng thái 'Chưa được xếp chỗ'.", "Hiển thị đúng họ tên và trạng thái chưa xếp", "PASS", "TV5"],
        ["TC03", "Xếp chỗ hợp lệ", "Click chọn nút A2, nhập 'SV100', bấm nút [Xếp chỗ].", "Nút A2 đổi màu xanh lá hiển thị SV100; bộ đếm tăng lên 1/12; CSDL có đúng 1 bản ghi A2–SV100.", "A2 hiển thị SV100, bộ đếm 1/12 chuẩn", "PASS", "TV5"],
        ["TC04", "Từ chối xếp chỗ đã có người", "Vẫn giữ chọn vị trí A2, nhập mã 'SV001', bấm nút [Xếp chỗ].", "Hệ thống báo lỗi A2 đã có người ngồi; nút A2 vẫn thuộc về SV100; CSDL không phát sinh bản ghi mới.", "Báo lỗi vị trí đã có người ngồi", "PASS", "TV5"],
        ["TC05", "Từ chối SV đã có chỗ", "Click chọn nút B1, nhập lại mã 'SV100', bấm nút [Xếp chỗ].", "Hệ thống báo SV100 đã được xếp chỗ; nút B1 vẫn giữ nguyên Trống; CSDL không đổi.", "Báo lỗi SV100 đã ngồi tại A2", "PASS", "TV5"],
        ["TC06", "Khôi phục trạng thái khi mở lại", "Đóng hoàn toàn ứng dụng (tắt cửa sổ Tkinter), sau đó mở lại bằng `python main.py`.", "Nút A2 vẫn hiển thị SV100; bộ đếm vẫn giữ nguyên 1/12; dữ liệu đọc trực tiếp từ SQLite.", "Trạng thái A2 và bộ đếm giữ nguyên 100%", "PASS", "TV5"],
        ["TC07", "Trả chỗ & Tra cứu lại SV", "Chọn nút A2, bấm [Trả chỗ]. Sau đó nhập 'SV100' và bấm [Tra cứu SV].", "Nút A2 trở về [Trống]; bộ đếm giảm về 0/12; tra cứu thấy hồ sơ SV100 vẫn còn nguyên và ở trạng thái chưa xếp.", "A2 trống, bộ đếm 0/12, SV100 còn nguyên hồ sơ", "PASS", "TV5"]
    ]
    add_styled_table(doc, headers_tc, data_tc, col_widths=[0.6, 1.2, 1.6, 1.8, 1.1, 0.7, 0.6])

    add_styled_heading(doc, "6.3. Quy trình ghi nhận và xử lý lỗi (Mẫu Bug Report chuẩn)", level=2)
    add_p(doc, "Khi phát hiện bất kỳ ca kiểm thử nào không đạt (FAIL), TV5 lập tức phát hành Bug Report theo mẫu chuẩn dưới đây và giao việc trực tiếp cho thành viên phụ trách module tương ứng:")
    
    headers_bug = ["Trường thông tin", "Nội dung đặc tả lỗi mẫu (Ví dụ thực tế)", "Ghi chú kỹ thuật"]
    data_bug = [
        ["Mã Bug (Bug ID)", "BUG-001", "Định dạng: BUG-xxx"],
        ["Tiêu đề lỗi", "Nút Xếp chỗ không kiểm tra mã SV rỗng dẫn đến crash CSDL", "Mô tả ngắn gọn vị trí và hiện tượng"],
        ["Module phụ trách", "TV2 – Nghiệp vụ Xếp chỗ (seat_service.py)", "Gán đúng thành viên sở hữu code"],
        ["Mức độ nghiêm trọng", "HIGH (Ảnh hưởng đến luồng chức năng chính)", "BLOCKER / HIGH / MEDIUM / LOW"],
        ["Môi trường kiểm thử", "Python 3.10.9, Windows 11, SQLite 3.39, nhánh develop", "Ghi rõ OS, phiên bản Python"],
        ["Điều kiện tiên quyết", "Đã khởi tạo CSDL với 100 sinh viên demo", "Trạng thái hệ thống trước khi tái hiện"],
        ["Các bước tái hiện", "1. Mở ứng dụng.\n2. Chọn nút A1.\n3. Để trống ô nhập mã SV.\n4. Bấm nút [Xếp chỗ].", "Liệt kê từng bước rõ ràng để dev làm theo"],
        ["Kết quả thực tế", "Ứng dụng đứng hình, terminal quăng IntegrityError NOT NULL.", "Chụp ảnh màn hình hoặc trích dẫn log"],
        ["Kết quả mong đợi", "Hiển thị hộp thoại cảnh báo: 'Vui lòng nhập mã sinh viên hợp lệ!'.", "Hành vi chuẩn theo thiết kế"],
        ["Trạng thái xử lý", "CLOSED (Đã sửa và xác nhận Re-test PASS)", "OPEN / IN PROGRESS / FIXED / CLOSED"]
    ]
    add_styled_table(doc, headers_bug, data_bug, col_widths=[1.5, 3.5, 1.8])

    add_styled_heading(doc, "6.4. Báo cáo tổng kết kiểm thử & Điều kiện ký xác nhận bàn giao", level=2)
    add_p(doc, "Bản nghiệm thu sản phẩm cuối cùng chỉ được ký duyệt khi đáp ứng đủ 5 điều kiện tiên quyết:")
    add_bullet(doc, "Đạt 100% tỷ lệ PASS đối với toàn bộ 7 ca kiểm thử bắt buộc (TC01 đến TC07).")
    add_bullet(doc, "Đạt 100% tỷ lệ thỏa mãn đối với toàn bộ 17 tiêu chí chấp nhận kỹ thuật (AC-01 đến AC-17).")
    add_bullet(doc, "Không còn bất kỳ lỗi nào ở mức độ Blocker hoặc High tồn đọng chưa được giải quyết.")
    add_bullet(doc, "Mã nguồn sạch, có comment rõ ràng, tuân thủ PEP 8 và đã hợp nhất vào nhánh `main`.")
    add_bullet(doc, "Cả 5 thành viên đều nắm vững giải thuật phần việc của mình và sẵn sàng trả lời chất vấn của Giảng viên.")
    
    doc.add_page_break()

def build_part_7(doc):
    """Xây dựng Phần VII: Bảng bàn giao và trách nhiệm."""
    add_styled_heading(doc, "PHẦN VII. BẢNG BÀN GIAO TRÁCH NHIỆM & ĐÁNH GIÁ ĐÓNG GÓP", level=1)
    
    add_styled_heading(doc, "7.1. Bảng theo dõi bàn giao Task và Tệp nguồn", level=2)
    add_p(doc, "Dưới đây là bảng tổng hợp tình trạng bàn giao các hạng mục kỹ thuật của 5 thành viên trong dự án:")
    
    headers_handoff = ["Task", "Người phụ trách", "Nhánh Git (Branch)", "Tệp bàn giao", "Trạng thái", "Người kiểm duyệt"]
    data_handoff = [
        ["TASK-01", "TV5 + Nhóm", "main / develop", ".gitignore, README.md", "HOÀN THÀNH", "Cả nhóm"],
        ["TASK-02", "TV4", "feature/database", "database.py, phong_may.db", "HOÀN THÀNH", "TV5 (Tech Lead)"],
        ["TASK-03", "TV4", "feature/database", "tao_du_lieu_demo.py", "HOÀN THÀNH", "TV5 (Tech Lead)"],
        ["TASK-04", "TV2", "feature/seat-management", "seat_service.py", "HOÀN THÀNH", "TV5 & TV1"],
        ["TASK-05", "TV3", "feature/student-search", "student_service.py, statistics.py", "HOÀN THÀNH", "TV5 & TV1"],
        ["TASK-06", "TV1", "feature/ui", "ui.py", "HOÀN THÀNH", "TV5 (Tech Lead)"],
        ["TASK-07", "Từng thành viên", "Từng nhánh feature", "tests/test_unit_modules.py", "HOÀN THÀNH", "TV5 (Tech Lead)"],
        ["TASK-08", "TV5 chủ trì", "develop", "main.py hoàn chỉnh", "HOÀN THÀNH", "Cả nhóm"],
        ["TASK-09", "TV5 + Nhóm", "develop", "TEST_REPORT.md, Bug Reports", "HOÀN THÀNH", "Cả nhóm"],
        ["TASK-10", "Cả nhóm", "main (v1.0)", "phong_may_app.zip, Bảng đóng góp", "HOÀN THÀNH", "Giảng viên chấm"]
    ]
    add_styled_table(doc, headers_handoff, data_handoff, col_widths=[0.9, 1.1, 1.5, 1.7, 1.0, 1.1])

    add_styled_heading(doc, "7.2. Bảng đánh giá tỷ lệ đóng góp thành viên và Ký xác nhận", level=2)
    add_p(doc, "Bảng tổng hợp mức độ tham gia và tỷ lệ đóng góp của 5 thành viên phục vụ Giảng viên đánh giá điểm quá trình:")
    
    headers_contrib = ["STT", "Họ và tên thành viên", "Vai trò phụ trách", "Tệp & Hàm đã viết", "Ca kiểm thử phụ trách", "Tỷ lệ đóng góp", "Chữ ký xác nhận"]
    data_contrib = [
        ["1", "Thành viên 1\n(TV1)", "Giao diện (UI)", "ui.py\n(RoomSeatApp, 12 nút, layout 3x4, refresh_ui)", "Kiểm thử tương tác GUI, bắt sự kiện click", "20%", "Đã ký xác nhận"],
        ["2", "Thành viên 2\n(TV2)", "Xếp chỗ & Trả chỗ", "seat_service.py\n(assign_seat, release_seat)", "TC03, TC04, TC05\n(Xếp hợp lệ, đè chỗ, SV trùng)", "20%", "Đã ký xác nhận"],
        ["3", "Thành viên 3\n(TV3)", "Tra cứu & Thống kê", "student_service.py, statistics.py\n(find_student, get_stats, get_map)", "TC02, TC07\n(Tra cứu SV, kiểm tra bộ đếm)", "20%", "Đã ký xác nhận"],
        ["4", "Thành viên 4\n(TV4)", "SQLite & Sinh dữ liệu", "database.py, tao_du_lieu_demo.py\n(init_db, seed_students)", "TC01\n(Sinh 100 SV 2 lần an toàn)", "20%", "Đã ký xác nhận"],
        ["5", "Thành viên 5\n(TV5)", "Kiểm thử & Tích hợp", "main.py, test_scenarios.md\n(Điều phối Git, tích hợp hệ thống)", "TC06, Toàn bộ kịch bản tích hợp SIT", "20%", "Đã ký xác nhận"]
    ]
    add_styled_table(doc, headers_contrib, data_contrib, col_widths=[0.5, 1.4, 1.3, 1.8, 1.4, 0.9, 1.0])
    add_p(doc, "Tổng cộng tỷ lệ đóng góp của toàn nhóm: 100% (Phân chia công bằng, đoàn kết, trách nhiệm đồng đều).", italic=True)

    add_styled_heading(doc, "7.3. Kịch bản demo và bảo vệ bài tập nhóm trước Giảng viên (5 phút)", level=2)
    add_p(doc, "Khi trình bày trước Giảng viên, nhóm nên phân bổ thời gian 5 phút demo theo kịch bản chuẩn Technical Lead sau:")
    add_bullet(doc, "Phút 01 (TV5 giới thiệu): Trình bày ngắn gọn kiến trúc 3 tầng, quy trình làm việc Git Flow và cơ chế phân chia trách nhiệm.", bold_prefix="1. Phút 01 - Tổng quan & Kiến trúc: ")
    add_bullet(doc, "Phút 02 (TV4 demo CSDL): Mở terminal, chạy script sinh dữ liệu 2 lần liên tiếp, mở DB Browser for SQLite cho Giảng viên xem 2 bảng `sinh_vien` (100 dòng) và `xep_cho` (rỗng, có PK/FK/UNIQUE).", bold_prefix="2. Phút 02 - SQLite & Dữ liệu demo: ")
    add_bullet(doc, "Phút 03 (TV1 & TV2 demo Xếp chỗ): Chạy `python main.py`, chọn A2, gõ SV100 bấm [Xếp chỗ]. Giao diện đổi màu xanh lá, bộ đếm lên 1/12. Sau đó thử xếp đè SV001 vào A2 hoặc SV100 vào B1 để chứng minh tính năng phòng ngừa lỗi hoạt động chuẩn xác.", bold_prefix="3. Phút 03 - Giao diện & Nghiệp vụ Xếp chỗ: ")
    add_bullet(doc, "Phút 04 (TV3 demo Tra cứu & Thống kê): Tra cứu SV100 (báo đã xếp A2). Tra cứu SV005 (báo chưa xếp chỗ). Tra cứu SV999 (báo không tìm thấy). Bấm Trả chỗ A2, bộ đếm về 0/12, tra cứu lại SV100 chứng minh hồ sơ không bị xóa.", bold_prefix="4. Phút 04 - Tra cứu, Bộ đếm & Trả chỗ: ")
    add_bullet(doc, "Phút 05 (TV5 chốt bảo vệ): Tắt ứng dụng, mở lại ứng dụng chứng minh dữ liệu được SQLite lưu trữ bền vững. Mời Giảng viên đặt câu hỏi chất vấn mã nguồn.", bold_prefix="5. Phút 05 - Tính bền vững & Trả lời phản biện: ")

print("Part 4-7 module initialized successfully!")
