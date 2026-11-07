import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from generator_core import (
    COLOR_PRIMARY_NAVY, COLOR_SECONDARY_BLUE, COLOR_ACCENT_BLUE,
    COLOR_BG_GRAY, COLOR_BORDER_GRAY,
    add_styled_heading, add_p, add_bullet, add_callout,
    add_code_block, add_styled_table, add_image_box
)

def build_part_3(doc):
    """Xây dựng Phần III: Hướng dẫn chi tiết từng Task (TASK-01 đến TASK-10)."""
    add_styled_heading(doc, "PHẦN III. HƯỚNG DẪN CHI TIẾT TỪNG TASK (TASK-01 ĐẾN TASK-10)", level=1)
    add_p(doc, "Đây là phần tài liệu quan trọng nhất. Mỗi Task dưới đây được đặc tả theo đúng chuẩn 10 mục kỹ thuật chi tiết. Sinh viên có thể mở VS Code và làm theo từng bước để hoàn thành sản phẩm một cách chuẩn xác.")
    
    # -------------------------------------------------------------------------
    # TASK-01
    # -------------------------------------------------------------------------
    add_styled_heading(doc, "TASK-01: Khởi tạo GitHub Repository, Cấu trúc Thư mục và Hợp đồng Giao diện", level=2)
    
    add_p(doc, "Khởi tạo môi trường phát triển chung trên GitHub, tạo nhánh develop, thiết lập tệp .gitignore chuẩn Python, cấu trúc thư mục rỗng và văn bản Hợp đồng giao diện (API Contract) để toàn bộ 5 thành viên tuân theo.", bold_prefix="1. Mục tiêu Task: ")
    add_p(doc, "TV5 (Kiểm thử & Tích hợp) chủ trì; Cả nhóm (TV1, TV2, TV3, TV4) phối hợp rà soát và thống nhất.", bold_prefix="2. Người chịu trách nhiệm: ")
    add_p(doc, "Nhóm đã đọc kỹ đề bài và hiểu rõ 12 chỗ ngồi, SQLite, các module dự kiến.", bold_prefix="3. Điều kiện đầu vào: ")
    
    add_p(doc, "TV5 thực hiện các bước sau trên máy tính và GitHub:", bold_prefix="4. Các bước thực hiện theo thứ tự: ")
    add_bullet(doc, "Bước 1: Mở trình duyệt, truy cập GitHub và tạo một Repository mới với tên `room-seat-manager-python` (để chế độ Public hoặc Private và add 4 thành viên làm Collaborator).")
    add_bullet(doc, "Bước 2: Mở VS Code trên máy cục bộ, mở thư mục dự án và khởi tạo Git bằng lệnh `git init`.")
    add_bullet(doc, "Bước 3: Tạo tệp `.gitignore` chuẩn Python để bỏ qua `__pycache__/`, `*.pyc`, `.vscode/` và môi trường ảo.")
    add_bullet(doc, "Bước 4: Tạo cấu trúc thư mục và các tệp mã nguồn rỗng (.py) theo danh sách thống nhất.")
    add_bullet(doc, "Bước 5: Tạo tệp `README.md` mô tả dự án và bảng Hợp đồng API Contract.")
    add_bullet(doc, "Bước 6: Commit lần đầu vào nhánh `main`, sau đó tạo nhánh `develop` và đẩy cả hai nhánh lên GitHub Remote.")
    add_bullet(doc, "Bước 7: Thông báo đường dẫn GitHub Repo cho 4 thành viên trong nhóm clone về máy.")
    
    add_p(doc, ".gitignore, README.md, database.py, tao_du_lieu_demo.py, seat_service.py, student_service.py, statistics.py, ui.py, main.py, tests/test_scenarios.md.", bold_prefix="5. Tệp cần tạo hoặc chỉnh sửa: ")
    
    add_p(doc, "Mã nguồn tệp `.gitignore` chuẩn cho dự án Python SQLite:", bold_prefix="6. Hướng dẫn code hoặc thuật toán cần triển khai: ")
    code_gitignore = """# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C# / VS Code
.vscode/
.idea/

# Virtual Environments
venv/
env/
ENV/

# OS generated files
Thumbs.db
ehthumbs.db
Desktop.ini
.DS_Store

# Temporary files
*.tmp
*.bak
"""
    add_code_block(doc, code_gitignore, language="Tệp .gitignore")
    
    add_p(doc, "Bảng Hợp đồng Giao diện Hàm (API Contract) cố định bắt buộc:", bold_prefix="Bảng Hợp đồng API: ")
    headers_api = ["Module", "Tên hàm", "Tham số đầu vào", "Kiểu dữ liệu trả về", "Ý nghĩa nghiệp vụ"]
    data_api = [
        ["database.py", "get_connection()", "db_name: str = 'phong_may.db'", "sqlite3.Connection", "Tạo kết nối CSDL, bật PRAGMA foreign_keys = ON"],
        ["database.py", "init_db()", "db_name: str = 'phong_may.db'", "None", "Tạo 2 bảng nếu chưa có, không làm mất dữ liệu cũ"],
        ["tao_du_lieu_demo.py", "seed_students()", "n: int = 100", "int (số lượng SV)", "Chèn SV001–SV100 bằng INSERT OR IGNORE"],
        ["seat_service.py", "assign_seat()", "ma_cho: str, ma_sv: str", "Tuple[bool, str]", "Xếp SV vào chỗ; trả về (True/False, thông báo)"],
        ["seat_service.py", "release_seat()", "ma_cho: str", "Tuple[bool, str]", "Trả chỗ; chỉ xóa xep_cho, giữ nguyên sinh_vien"],
        ["student_service.py", "find_student()", "ma_sv: str", "Optional[Dict[str, Any]]", "Tra cứu SV: trả Dict (nếu có) hoặc None (nếu không có)"],
        ["statistics.py", "get_seat_stats()", "Không", "Tuple[int, int, int]", "Trả về bộ 3 giá trị: (used, total=12, available)"],
        ["statistics.py", "get_seat_map()", "Không", "Dict[str, Optional[str]]", "Trả về Dict 12 chỗ { 'A1': None/ma_sv, ..., 'C4': ... }"]
    ]
    add_styled_table(doc, headers_api, data_api, col_widths=[1.3, 1.3, 1.4, 1.3, 1.5])
    
    add_p(doc, "Toàn bộ các module trong hệ thống.", bold_prefix="7. Các module liên quan: ")
    add_p(doc, "GitHub Repository hoạt động, nhánh develop có cấu trúc thư mục sạch và bảng API Contract.", bold_prefix="8. Kết quả đầu ra cần bàn giao: ")
    add_callout(doc, "DoD của TASK-01", 
                "Tất cả 4 thành viên (TV1, TV2, TV3, TV4) clone được repo về máy cục bộ, chuyển sang nhánh develop và nhìn thấy đầy đủ các tệp rỗng cùng README.md.", callout_type="success")
    add_p(doc, "Các thành viên chạy `git status` và `git branch -a` trên máy cá nhân để xác nhận nhánh `develop` đã sẵn sàng.", bold_prefix="10. Cách tự kiểm thử Task: ")
    
    # -------------------------------------------------------------------------
    # TASK-02
    # -------------------------------------------------------------------------
    add_styled_heading(doc, "TASK-02: Thiết kế SQLite Schema và Module Kết Nối Database (database.py)", level=2)
    
    add_p(doc, "Thiết kế cấu trúc 2 bảng sinh_vien và xep_cho, đảm bảo đầy đủ khóa chính, khóa ngoại, ràng buộc duy nhất (UNIQUE) và hàm quản lý kết nối tự động bật kiểm tra khóa ngoại.", bold_prefix="1. Mục tiêu Task: ")
    add_p(doc, "TV4 (SQLite & Sinh dữ liệu) phụ trách chính; TV5 kiểm tra và duyệt PR.", bold_prefix="2. Người chịu trách nhiệm: ")
    add_p(doc, "TASK-01 đã hoàn thành; TV4 đã tạo nhánh `feature/database` từ `develop`.", bold_prefix="3. Điều kiện đầu vào: ")
    
    add_p(doc, "TV4 triển khai các bước trong file `database.py`:", bold_prefix="4. Các bước thực hiện theo thứ tự: ")
    add_bullet(doc, "Bước 1: Tạo hàm `get_connection(db_name='phong_may.db')` sử dụng thư viện `sqlite3`.")
    add_bullet(doc, "Bước 2: Cấu hình `conn.row_factory = sqlite3.Row` để cho phép truy cập dữ liệu theo tên cột như Dict.")
    add_bullet(doc, "Bước 3: Thực thi câu lệnh `PRAGMA foreign_keys = ON;` ngay sau khi mở kết nối (Đây là yêu cầu bắt buộc của SQLite vì mặc định tính năng khóa ngoại bị tắt).")
    add_bullet(doc, "Bước 4: Tạo hàm `init_db(db_name='phong_may.db')` chứa câu lệnh DDL định nghĩa bảng `sinh_vien` và `xep_cho`.")
    add_bullet(doc, "Bước 5: Sử dụng `CREATE TABLE IF NOT EXISTS` để không làm mất dữ liệu khi ứng dụng khởi động lại. TUYỆT ĐỐI KHÔNG dùng lệnh `DROP TABLE`.")
    add_bullet(doc, "Bước 6: Thiết lập đúng các ràng buộc: `ma_sv` là PRIMARY KEY trong `sinh_vien`; `ma_cho` là PRIMARY KEY trong `xep_cho`; `ma_sv` trong `xep_cho` có ràng buộc UNIQUE và FOREIGN KEY tham chiếu tới `sinh_vien(ma_sv)`.")
    
    add_p(doc, "database.py (tạo mới và hoàn thiện).", bold_prefix="5. Tệp cần tạo hoặc chỉnh sửa: ")
    
    add_p(doc, "Mã nguồn hoàn chỉnh chuẩn Senior cho `database.py`:", bold_prefix="6. Hướng dẫn code hoặc thuật toán cần triển khai: ")
    code_db = """# database.py
import sqlite3
from typing import Optional

DB_NAME = "phong_may.db"

def get_connection(db_name: str = DB_NAME) -> sqlite3.Connection:
    \"\"\"
    Tạo và cấu hình kết nối tới SQLite Database.
    YÊU CẦU BẮT BUỘC: 
    - Bật PRAGMA foreign_keys = ON để kích hoạt kiểm tra toàn vẹn khóa ngoại.
    - Cấu hình row_factory = sqlite3.Row để truy cập dữ liệu theo tên cột.
    \"\"\"
    conn = sqlite3.connect(db_name)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def init_db(db_name: str = DB_NAME) -> None:
    \"\"\"
    Khởi tạo cấu trúc các bảng CSDL nếu chưa tồn tại.
    TUYỆT ĐỐI KHÔNG DÙNG DROP TABLE vì sẽ làm mất dữ liệu khi mở lại ứng dụng.
    \"\"\"
    with get_connection(db_name) as conn:
        cursor = conn.cursor()
        
        # 1. Bảng hồ sơ sinh viên
        cursor.execute(\"\"\"
            CREATE TABLE IF NOT EXISTS sinh_vien (
                ma_sv TEXT PRIMARY KEY,
                ho_ten TEXT NOT NULL
            );
        \"\"\")
        
        # 2. Bảng xếp chỗ phòng máy (12 chỗ)
        # ma_cho: Khóa chính (A1-C4)
        # ma_sv: Khóa ngoại tham chiếu sinh_vien, có ràng buộc UNIQUE để mỗi SV chỉ ngồi 1 chỗ
        cursor.execute(\"\"\"
            CREATE TABLE IF NOT EXISTS xep_cho (
                ma_cho TEXT PRIMARY KEY,
                ma_sv TEXT UNIQUE NOT NULL,
                FOREIGN KEY (ma_sv) REFERENCES sinh_vien(ma_sv)
            );
        \"\"\")
        
        conn.commit()

if __name__ == "__main__":
    init_db()
    print("[*] Khởi tạo cơ sở dữ liệu phong_may.db thành công với đầy đủ ràng buộc PK, FK, UNIQUE!")
"""
    add_code_block(doc, code_db, language="Python: database.py")
    
    add_p(doc, "Tất cả các module nghiệp vụ (seat_service, student_service, statistics, tao_du_lieu_demo).", bold_prefix="7. Các module liên quan: ")
    add_p(doc, "Tệp database.py hoàn chỉnh, tệp CSDL phong_may.db được tạo tự động với đúng schema.", bold_prefix="8. Kết quả đầu ra cần bàn giao: ")
    add_callout(doc, "DoD của TASK-02", 
                "Chạy `python database.py` không phát sinh lỗi; tệp phong_may.db xuất hiện; thử chèn bản ghi vi phạm khóa ngoại hoặc vi phạm UNIQUE thì SQLite báo lỗi IntegrityError.", callout_type="success")
    
    add_p(doc, "Tự kiểm thử bằng script ngắn kiểm tra ràng buộc khóa ngoại và UNIQUE:", bold_prefix="10. Cách tự kiểm thử Task: ")
    code_test_db = """# Tự kiểm thử nhanh tính năng khóa ngoại
import sqlite3
from database import get_connection, init_db

init_db("test_db.db")
conn = get_connection("test_db.db")
try:
    # Chèn vào xep_cho mã SV999 chưa tồn tại -> Bắt buộc phải quăng lỗi!
    conn.execute("INSERT INTO xep_cho(ma_cho, ma_sv) VALUES ('A1', 'SV999');")
    print("[-] THẤT BẠI: Khóa ngoại chưa được kích hoạt!")
except sqlite3.IntegrityError:
    print("[+] THÀNH CÔNG: SQLite đã chặn chèn sinh viên không tồn tại (FK hoạt động tốt)!")
finally:
    conn.close()
"""
    add_code_block(doc, code_test_db, language="Python: Self-test database.py")

    # -------------------------------------------------------------------------
    # TASK-03
    # -------------------------------------------------------------------------
    add_styled_heading(doc, "TASK-03: Xây dựng Script Sinh Dữ Liệu 100 Sinh Viên Demo An Toàn (tao_du_lieu_demo.py)", level=2)
    
    add_p(doc, "Xây dựng kịch bản tự động sinh tối thiểu 100 sinh viên từ SV001 đến SV100. Đảm bảo chạy nhiều lần không bị nhân đôi dữ liệu và không làm mất các lượt xếp chỗ đang có trong bảng xep_cho.", bold_prefix="1. Mục tiêu Task: ")
    add_p(doc, "TV4 (SQLite & Sinh dữ liệu) phụ trách chính; TV5 kiểm thử nghiệm thu.", bold_prefix="2. Người chịu trách nhiệm: ")
    add_p(doc, "TASK-02 đã hoàn thành, tệp database.py đã sẵn sàng kết nối.", bold_prefix="3. Điều kiện đầu vào: ")
    
    add_p(doc, "TV4 triển khai các bước trong file `tao_du_lieu_demo.py`:", bold_prefix="4. Các bước thực hiện theo thứ tự: ")
    add_bullet(doc, "Bước 1: Import hàm `get_connection` và `init_db` từ `database.py`.")
    add_bullet(doc, "Bước 2: Viết hàm `seed_students(n=100, db_name='phong_may.db')`.")
    add_bullet(doc, "Bước 3: Gọi `init_db(db_name)` ở đầu hàm để đảm bảo bảng CSDL luôn tồn tại trước khi chèn.")
    add_bullet(doc, "Bước 4: Sử dụng vòng lặp `for i in range(1, n + 1)` để tạo mã sinh viên dạng `f'SV{i:03d}'` và họ tên dạng `f'Sinh viên {i:03d}'`.")
    add_bullet(doc, "Bước 5: Sử dụng câu lệnh `INSERT OR IGNORE INTO sinh_vien (ma_sv, ho_ten) VALUES (?, ?);`.")
    add_bullet(doc, "Bước 6: Thực hiện `conn.commit()` sau vòng lặp và thực hiện truy vấn `SELECT COUNT(*) FROM sinh_vien` để trả về tổng số lượng hồ sơ hiện có.")
    
    add_p(doc, "tao_du_lieu_demo.py (tạo mới).", bold_prefix="5. Tệp cần tạo hoặc chỉnh sửa: ")
    
    add_p(doc, "Mã nguồn hoàn chỉnh chuẩn Senior cho `tao_du_lieu_demo.py`:", bold_prefix="6. Hướng dẫn code hoặc thuật toán cần triển khai: ")
    code_seed = """# tao_du_lieu_demo.py
import sqlite3
from database import get_connection, init_db

def seed_students(n: int = 100, db_name: str = "phong_may.db") -> int:
    \"\"\"
    Sinh danh sách n sinh viên demo từ SV001 đến SV100.
    NGUYÊN TẮC QUAN TRỌNG:
    - Sử dụng INSERT OR IGNORE để chạy script nhiều lần không tạo bản ghi trùng lặp.
    - Không xóa hoặc làm ảnh hưởng đến dữ liệu đang xếp chỗ trong bảng xep_cho.
    \"\"\"
    # Đảm bảo bảng CSDL đã được khởi tạo
    init_db(db_name)
    
    with get_connection(db_name) as conn:
        cursor = conn.cursor()
        
        # Chèn danh sách 100 sinh viên bằng vòng lặp
        for i in range(1, n + 1):
            ma_sv = f"SV{i:03d}"
            ho_ten = f"Sinh viên {i:03d}"
            cursor.execute(
                "INSERT OR IGNORE INTO sinh_vien (ma_sv, ho_ten) VALUES (?, ?);",
                (ma_sv, ho_ten)
            )
            
        conn.commit()
        
        # Lấy tổng số lượng sinh viên thực tế trong CSDL
        cursor.execute("SELECT COUNT(*) FROM sinh_vien;")
        total_students = cursor.fetchone()[0]
        return total_students

if __name__ == "__main__":
    print("[*] Đang khởi chạy script sinh dữ liệu demo...")
    count = seed_students(100)
    print(f"[+] Hoàn tất! Số lượng hồ sơ sinh viên hiện có trong CSDL: {count}")
"""
    add_code_block(doc, code_seed, language="Python: tao_du_lieu_demo.py")
    
    add_p(doc, "database.py, student_service.py.", bold_prefix="7. Các module liên quan: ")
    add_p(doc, "Tệp tao_du_lieu_demo.py chạy độc lập được từ terminal, CSDL có đủ 100 sinh viên.", bold_prefix="8. Kết quả đầu ra cần bàn giao: ")
    add_callout(doc, "DoD của TASK-03", 
                "Chạy lệnh `python tao_du_lieu_demo.py` hai lần liên tiếp. Lần 1: báo 100 sinh viên. Lần 2: vẫn báo đúng 100 sinh viên (không tăng lên 200). "
                "Nếu đã có 1 bản ghi xếp chỗ trước đó, bản ghi xếp chỗ vẫn còn nguyên vẹn.", callout_type="success")
    
    add_p(doc, "Chạy lệnh kiểm thử idempotency từ PowerShell:", bold_prefix="10. Cách tự kiểm thử Task: ")
    code_test_seed = """# Chạy lần 1
python tao_du_lieu_demo.py
# Chèn thử 1 lượt xếp chỗ mẫu
python -c "import sqlite3; conn=sqlite3.connect('phong_may.db'); conn.execute('INSERT OR IGNORE INTO xep_cho VALUES (\'A1\', \'SV001\')'); conn.commit()"
# Chạy lần 2
python tao_du_lieu_demo.py
# Kiểm tra lại số lượng SV và lượt xếp chỗ A1
python -c "import sqlite3; conn=sqlite3.connect('phong_may.db'); print('SV count:', conn.execute('SELECT COUNT(*) FROM sinh_vien').fetchone()[0]); print('Lượt A1:', conn.execute('SELECT * FROM xep_cho WHERE ma_cho=\'A1\'').fetchone())"
"""
    add_code_block(doc, code_test_seed, language="Shell / Bash")

    # -------------------------------------------------------------------------
    # TASK-04
    # -------------------------------------------------------------------------
    add_styled_heading(doc, "TASK-04: Xây dựng Module Nghiệp Vụ Xếp Chỗ và Trả Chỗ (seat_service.py)", level=2)
    
    add_p(doc, "Xây dựng 2 hàm nghiệp vụ cốt lõi assign_seat() và release_seat() tuân thủ đầy đủ các quy tắc nghiệp vụ của đề bài: kiểm tra chỗ hợp lệ, kiểm tra mã SV, chống xếp trùng chỗ, chống SV ngồi 2 chỗ, trả chỗ không xóa sinh viên và xử lý ngoại lệ SQLite.", bold_prefix="1. Mục tiêu Task: ")
    add_p(doc, "TV2 (Xếp chỗ & Trả chỗ) phụ trách chính; TV4 hỗ trợ câu lệnh SQL, TV5 review PR.", bold_prefix="2. Người chịu trách nhiệm: ")
    add_p(doc, "TASK-02 đã hoàn thành; nhánh `feature/seat-management` đã được tạo từ `develop`.", bold_prefix="3. Điều kiện đầu vào: ")
    
    add_p(doc, "TV2 triển khai chi tiết các bước trong file `seat_service.py`:", bold_prefix="4. Các bước thực hiện theo thứ tự: ")
    add_bullet(doc, "Bước 1: Khai báo danh sách 12 mã chỗ hợp lệ `VALID_SEATS = ['A1'..'A4', 'B1'..'B4', 'C1'..'C4']`.")
    add_bullet(doc, "Bước 2: Xây dựng hàm `assign_seat(ma_cho, ma_sv)` với 5 bước kiểm tra tuần tự:\n"
                    "  + Kiểm tra mã chỗ có nằm trong VALID_SEATS hay không (chống nhập sai A5, D1).\n"
                    "  + Kiểm tra mã sinh viên có rỗng hay không.\n"
                    "  + Kiểm tra mã sinh viên có tồn tại trong bảng `sinh_vien` hay không (nếu không -> báo lỗi).\n"
                    "  + Kiểm tra chỗ `ma_cho` đã có sinh viên nào ngồi chưa trong bảng `xep_cho` (nếu có -> báo lỗi kèm mã SV đang ngồi).\n"
                    "  + Kiểm tra sinh viên `ma_sv` đã được xếp ở chỗ nào khác chưa trong bảng `xep_cho` (nếu có -> báo lỗi kèm mã chỗ cũ).\n"
                    "  + Nếu tất cả hợp lệ: thực hiện lệnh `INSERT INTO xep_cho(ma_cho, ma_sv) VALUES (?, ?)`, commit và trả về `(True, 'Thông báo thành công')`.")
    add_bullet(doc, "Bước 3: Đặt khối lệnh `try...except sqlite3.IntegrityError` bao quanh câu lệnh INSERT để phòng ngừa xung đột đồng thời.")
    add_bullet(doc, "Bước 4: Xây dựng hàm `release_seat(ma_cho)` với các bước:\n"
                    "  + Kiểm tra mã chỗ có nằm trong VALID_SEATS hay không.\n"
                    "  + Kiểm tra chỗ có đang được sử dụng trong `xep_cho` hay không. Nếu chỗ đang trống -> trả về `(False, 'Chỗ đang trống, không thể trả chỗ')`.\n"
                    "  + Nếu có người: thực thi `DELETE FROM xep_cho WHERE ma_cho = ?;` và commit.\n"
                    "  + TUYỆT ĐỐI KHÔNG thực hiện bất kỳ lệnh DELETE nào trên bảng `sinh_vien`.\n"
                    "  + Trả về `(True, 'Trả chỗ thành công')`.")
    
    add_p(doc, "seat_service.py (tạo mới và hoàn thiện).", bold_prefix="5. Tệp cần tạo hoặc chỉnh sửa: ")
    
    add_p(doc, "Mã nguồn chuẩn Senior cho `seat_service.py`:", bold_prefix="6. Hướng dẫn code hoặc thuật toán cần triển khai: ")
    code_seat = """# seat_service.py
import sqlite3
from typing import Tuple
from database import get_connection

# Danh sách 12 vị trí máy cố định trong phòng thực hành 3 hàng x 4 cột
VALID_SEATS = [
    "A1", "A2", "A3", "A4",
    "B1", "B2", "B3", "B4",
    "C1", "C2", "C3", "C4"
]

def assign_seat(ma_cho: str, ma_sv: str, db_name: str = "phong_may.db") -> Tuple[bool, str]:
    \"\"\"
    Xếp một sinh viên vào vị trí máy chỉ định.
    Trả về Tuple: (Thành_công_hay_không, Thông_điệp_kết_quả)
    \"\"\"
    # Chuẩn hóa dữ liệu đầu vào
    ma_cho = ma_cho.strip().upper() if ma_cho else ""
    ma_sv = ma_sv.strip().upper() if ma_sv else ""
    
    # 1. Kiểm tra mã chỗ hợp lệ
    if ma_cho not in VALID_SEATS:
        return False, f"Mã chỗ '{ma_cho}' không hợp lệ! Vui lòng chọn từ A1-A4, B1-B4, C1-C4."
        
    # 2. Kiểm tra mã sinh viên không rỗng
    if not ma_sv:
        return False, "Vui lòng nhập mã sinh viên hợp lệ!"

    with get_connection(db_name) as conn:
        cursor = conn.cursor()
        
        # 3. Kiểm tra mã sinh viên có tồn tại trong hệ thống hồ sơ không
        cursor.execute("SELECT ho_ten FROM sinh_vien WHERE ma_sv = ?;", (ma_sv,))
        student = cursor.fetchone()
        if not student:
            return False, f"Mã sinh viên '{ma_sv}' không tồn tại trong danh sách hồ sơ!"
            
        ho_ten = student["ho_ten"]
        
        # 4. Kiểm tra chỗ ngồi đã có người chiếm giữ hay chưa
        cursor.execute("SELECT ma_sv FROM xep_cho WHERE ma_cho = ?;", (ma_cho,))
        seat_occupied = cursor.fetchone()
        if seat_occupied:
            return False, f"Vị trí '{ma_cho}' đã có người ngồi (Sinh viên {seat_occupied['ma_sv']})!"
            
        # 5. Kiểm tra sinh viên đã được xếp chỗ ở vị trí khác hay chưa
        cursor.execute("SELECT ma_cho FROM xep_cho WHERE ma_sv = ?;", (ma_sv,))
        student_seated = cursor.fetchone()
        if student_seated:
            return False, f"Sinh viên '{ma_sv}' ({ho_ten}) đã được xếp tại chỗ '{student_seated['ma_cho']}' rồi!"
            
        # 6. Đạt tất cả điều kiện: Thực hiện lưu bản ghi xếp chỗ
        try:
            cursor.execute(
                "INSERT INTO xep_cho (ma_cho, ma_sv) VALUES (?, ?);",
                (ma_cho, ma_sv)
            )
            conn.commit()
            return True, f"Xếp chỗ thành công! Sinh viên {ma_sv} ({ho_ten}) vào vị trí {ma_cho}."
        except sqlite3.IntegrityError as e:
            return False, f"Lỗi toàn vẹn dữ liệu SQLite: {str(e)}"
        except Exception as e:
            return False, f"Lỗi hệ thống ngoài dự kiến: {str(e)}"

def release_seat(ma_cho: str, db_name: str = "phong_may.db") -> Tuple[bool, str]:
    \"\"\"
    Trả lại chỗ ngồi đã xếp.
    QUY TẮC CỐT LÕI:
    - Chỉ xóa bản ghi trong bảng xep_cho.
    - TUYỆT ĐỐI KHÔNG xóa hồ sơ sinh viên trong bảng sinh_vien.
    \"\"\"
    ma_cho = ma_cho.strip().upper() if ma_cho else ""
    
    if ma_cho not in VALID_SEATS:
        return False, f"Mã chỗ '{ma_cho}' không hợp lệ!"
        
    with get_connection(db_name) as conn:
        cursor = conn.cursor()
        
        # 1. Kiểm tra chỗ có đang có người ngồi hay không
        cursor.execute("SELECT ma_sv FROM xep_cho WHERE ma_cho = ?;", (ma_cho,))
        record = cursor.fetchone()
        if not record:
            return False, f"Vị trí '{ma_cho}' hiện đang trống, không thể thực hiện thao tác trả chỗ!"
            
        ma_sv_released = record["ma_sv"]
        
        # 2. Xóa bản ghi xếp chỗ
        cursor.execute("DELETE FROM xep_cho WHERE ma_cho = ?;", (ma_cho,))
        conn.commit()
        return True, f"Trả chỗ thành công! Vị trí {ma_cho} (trước đó là SV {ma_sv_released}) hiện đã trống."
"""
    add_code_block(doc, code_seat, language="Python: seat_service.py")
    
    add_p(doc, "database.py, ui.py.", bold_prefix="7. Các module liên quan: ")
    add_p(doc, "Tệp seat_service.py hoàn chỉnh, đáp ứng mọi quy tắc nghiệp vụ xếp và trả chỗ.", bold_prefix="8. Kết quả đầu ra cần bàn giao: ")
    add_callout(doc, "DoD của TASK-04", 
                "Hàm assign_seat từ chối: (1) SV không tồn tại; (2) Chỗ đã có người; (3) SV đã ngồi chỗ khác. "
                "Hàm release_seat từ chối trả chỗ trống; khi trả chỗ có người thì chỉ xóa bảng xep_cho, kiểm tra bảng sinh_vien hồ sơ SV vẫn còn nguyên.", callout_type="success")
    
    add_p(doc, "Tự kiểm thử qua script kiểm tra đầy đủ các kịch bản biên:", bold_prefix="10. Cách tự kiểm thử Task: ")
    code_test_seat = """# Tự kiểm thử nghiệp vụ seat_service.py
from database import init_db
from tao_du_lieu_demo import seed_students
from seat_service import assign_seat, release_seat

init_db("test_run.db")
seed_students(100, "test_run.db")

# 1. Xếp hợp lệ
ok, msg = assign_seat("A2", "SV100", "test_run.db")
print("Case 1 (Xếp A2 - SV100):", ok, "|", msg)

# 2. Xếp đè chỗ đã có người
ok, msg = assign_seat("A2", "SV001", "test_run.db")
print("Case 2 (Đè SV001 vào A2):", not ok, "|", msg)

# 3. Xếp SV đã có chỗ sang chỗ khác
ok, msg = assign_seat("B1", "SV100", "test_run.db")
print("Case 3 (SV100 sang B1):", not ok, "|", msg)

# 4. Trả chỗ hợp lệ
ok, msg = release_seat("A2", "test_run.db")
print("Case 4 (Trả A2):", ok, "|", msg)

# 5. Trả chỗ trống
ok, msg = release_seat("A2", "test_run.db")
print("Case 5 (Trả lại A2 trống):", not ok, "|", msg)
"""
    add_code_block(doc, code_test_seat, language="Python: Self-test seat_service.py")

    # -------------------------------------------------------------------------
    # TASK-05
    # -------------------------------------------------------------------------
    add_styled_heading(doc, "TASK-05: Xây dựng Module Tra Cứu Sinh Viên và Thống Kê Chỗ Ngồi (student_service.py, statistics.py)", level=2)
    
    add_p(doc, "Xây dựng chức năng tra cứu sinh viên (sử dụng LEFT JOIN để phân biệt rõ 3 trạng thái: đã xếp chỗ, chưa xếp chỗ, không tồn tại) và các hàm thống kê số chỗ đã dùng, còn trống cùng ma trận trạng thái 12 vị trí.", bold_prefix="1. Mục tiêu Task: ")
    add_p(doc, "TV3 (Tra cứu & Thống kê) phụ trách chính; TV4 hỗ trợ câu lệnh JOIN, TV5 review PR.", bold_prefix="2. Người chịu trách nhiệm: ")
    add_p(doc, "TASK-02 đã hoàn thành; nhánh `feature/student-search` đã được tạo từ `develop`.", bold_prefix="3. Điều kiện đầu vào: ")
    
    add_p(doc, "TV3 triển khai các bước thực hiện trên 2 tệp mã nguồn:", bold_prefix="4. Các bước thực hiện theo thứ tự: ")
    add_bullet(doc, "Bước 1: Mở tệp `student_service.py`, xây dựng hàm `find_student(ma_sv, db_name='phong_may.db')`.")
    add_bullet(doc, "Bước 2: Viết câu lệnh SQL sử dụng mệnh đề `LEFT JOIN` giữa bảng `sinh_vien` (sv) và `xep_cho` (xc) theo điều kiện `sv.ma_sv = xc.ma_sv`.")
    add_bullet(doc, "Bước 3: Xử lý logic 3 trạng thái của kết quả tra cứu:\n"
                    "  + Nếu `cursor.fetchone()` trả về `None`: Sinh viên không có trong bảng sinh_vien -> Hàm trả về `None`.\n"
                    "  + Nếu có bản ghi và `xc.ma_cho is None`: Sinh viên tồn tại nhưng chưa có bản ghi xếp chỗ -> Hàm trả về Dict `{'ma_sv': ..., 'ho_ten': ..., 'ma_cho': None}`.\n"
                    "  + Nếu có bản ghi và `xc.ma_cho is not None`: Sinh viên đã được xếp chỗ -> Hàm trả về Dict `{'ma_sv': ..., 'ho_ten': ..., 'ma_cho': row['ma_cho']}`.")
    add_bullet(doc, "Bước 4: Mở tệp `statistics.py`, xây dựng hàm `get_seat_stats(db_name='phong_may.db')`:\n"
                    "  + Thực thi `SELECT COUNT(*) FROM xep_cho;` để lấy `used`.\n"
                    "  + Tổng số máy `total = 12`.\n"
                    "  + Số máy trống `available = total - used`.\n"
                    "  + Trả về Tuple `(used, total, available)`.")
    add_bullet(doc, "Bước 5: Xây dựng hàm `get_seat_map(db_name='phong_may.db')`:\n"
                    "  + Khởi tạo dict gồm 12 key từ A1 đến C4 với giá trị mặc định là `None`.\n"
                    "  + Truy vấn `SELECT ma_cho, ma_sv FROM xep_cho;` và cập nhật mã sinh viên vào đúng key tương ứng.\n"
                    "  + Trả về dict hoàn chỉnh để giao diện Tkinter render.")
    
    add_p(doc, "student_service.py, statistics.py (tạo mới và hoàn thiện cả 2 tệp).", bold_prefix="5. Tệp cần tạo hoặc chỉnh sửa: ")
    
    add_p(doc, "Mã nguồn chuẩn Senior cho `student_service.py` và `statistics.py`:", bold_prefix="6. Hướng dẫn code hoặc thuật toán cần triển khai: ")
    code_student = """# student_service.py
import sqlite3
from typing import Optional, Dict, Any
from database import get_connection

def find_student(ma_sv: str, db_name: str = "phong_may.db") -> Optional[Dict[str, Any]]:
    \"\"\"
    Tra cứu thông tin hồ sơ và vị trí chỗ ngồi của sinh viên.
    QUY TẮC PHÂN BIỆT 3 TRẠNG THÁI:
    1. Trả về None: Không tìm thấy sinh viên trong hệ thống CSDL.
    2. Trả về {'ma_sv': ..., 'ho_ten': ..., 'ma_cho': None}: SV tồn tại nhưng CHƯA xếp chỗ.
    3. Trả về {'ma_sv': ..., 'ho_ten': ..., 'ma_cho': 'A2'}: SV tồn tại và ĐÃ được xếp chỗ.
    \"\"\"
    ma_sv = ma_sv.strip().upper() if ma_sv else ""
    if not ma_sv:
        return None
        
    with get_connection(db_name) as conn:
        cursor = conn.cursor()
        
        # Dùng LEFT JOIN để lấy đầy đủ hồ sơ dù SV chưa được xếp chỗ
        query = \"\"\"
            SELECT sv.ma_sv, sv.ho_ten, xc.ma_cho
            FROM sinh_vien sv
            LEFT JOIN xep_cho xc ON sv.ma_sv = xc.ma_sv
            WHERE sv.ma_sv = ?;
        \"\"\"
        cursor.execute(query, (ma_sv,))
        row = cursor.fetchone()
        
        if not row:
            return None  # Trường hợp 1: Mã SV không tồn tại
            
        return {
            "ma_sv": row["ma_sv"],
            "ho_ten": row["ho_ten"],
            "ma_cho": row["ma_cho"]  # Sẽ là None nếu chưa xếp, hoặc chuỗi 'A2' nếu đã xếp
        }
"""
    add_code_block(doc, code_student, language="Python: student_service.py")
    
    code_stats = """# statistics.py
import sqlite3
from typing import Tuple, Dict, Optional
from database import get_connection
from seat_service import VALID_SEATS

TOTAL_ROOM_SEATS = 12

def get_seat_stats(db_name: str = "phong_may.db") -> Tuple[int, int, int]:
    \"\"\"
    Thống kê số lượng máy tính trong phòng thực hành.
    Trả về bộ ba (Tuple): (used, total, available)
    - used: Số chỗ đang có sinh viên sử dụng (COUNT từ bảng xep_cho).
    - total: Tổng số chỗ ngồi cố định (12).
    - available: Số chỗ còn trống (total - used).
    \"\"\"
    with get_connection(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM xep_cho;")
        used = cursor.fetchone()[0]
        total = TOTAL_ROOM_SEATS
        available = total - used
        return used, total, available

def get_seat_map(db_name: str = "phong_may.db") -> Dict[str, Optional[str]]:
    \"\"\"
    Lấy sơ đồ ma trận trạng thái hiện tại của toàn bộ 12 vị trí máy.
    Trả về Dict: {'A1': None, 'A2': 'SV100', ..., 'C4': None}
    - None biểu thị chỗ đang trống.
    - Chuỗi mã sinh viên biểu thị chỗ đã có người ngồi.
    \"\"\"
    # Khởi tạo bản đồ 12 vị trí ban đầu đều trống
    seat_map: Dict[str, Optional[str]] = {seat: None for seat in VALID_SEATS}
    
    with get_connection(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT ma_cho, ma_sv FROM xep_cho;")
        records = cursor.fetchall()
        for row in records:
            seat_map[row["ma_cho"]] = row["ma_sv"]
            
    return seat_map
"""
    add_code_block(doc, code_stats, language="Python: statistics.py")
    
    add_p(doc, "database.py, seat_service.py, ui.py.", bold_prefix="7. Các module liên quan: ")
    add_p(doc, "Hai tệp student_service.py và statistics.py hoàn chỉnh, đúng kiểu dữ liệu cam kết.", bold_prefix="8. Kết quả đầu ra cần bàn giao: ")
    add_callout(doc, "DoD của TASK-05", 
                "Tra cứu SV999 trả về None (không báo nhầm là chưa xếp chỗ). "
                "Tra cứu SV100 khi chưa xếp trả về dict với ma_cho=None. "
                "Hàm get_seat_stats luôn trả về đúng số lượng dòng của bảng xep_cho và tổng luôn là 12.", callout_type="success")
    
    add_p(doc, "Tự kiểm thử module tra cứu và thống kê:", bold_prefix="10. Cách tự kiểm thử Task: ")
    code_test_search = """# Tự kiểm thử student_service & statistics
from database import init_db
from tao_du_lieu_demo import seed_students
from seat_service import assign_seat
from student_service import find_student
from statistics import get_seat_stats, get_seat_map

init_db("test_stat.db")
seed_students(100, "test_stat.db")

# 1. Tìm SV chưa tồn tại
res_none = find_student("SV999", "test_stat.db")
print("Test SV999 (Expect None):", res_none is None)

# 2. Tìm SV chưa xếp chỗ
res_unseated = find_student("SV100", "test_stat.db")
print("Test SV100 chưa xếp (Expect ma_cho is None):", res_unseated["ma_cho"] is None)

# 3. Xếp SV100 vào A2 và kiểm tra lại
assign_seat("A2", "SV100", "test_stat.db")
res_seated = find_student("SV100", "test_stat.db")
print("Test SV100 đã xếp A2:", res_seated["ma_cho"] == "A2")

# 4. Kiểm tra stats
used, total, avail = get_seat_stats("test_stat.db")
print(f"Stats: used={used}/12, avail={avail} (Expect used=1, avail=11)")
"""
    add_code_block(doc, code_test_search, language="Python: Self-test search & stats")

    # -------------------------------------------------------------------------
    # TASK-06
    # -------------------------------------------------------------------------
    add_styled_heading(doc, "TASK-06: Xây dựng Giao Diện Người Dùng Tkinter 12 Chỗ Ngồi (ui.py, main.py)", level=2)
    
    add_p(doc, "Xây dựng toàn bộ giao diện đồ họa người dùng bằng thư viện chuẩn Tkinter với lưới 12 nút máy tính (3 hàng × 4 cột), ô nhập liệu mã sinh viên, 3 nút chức năng, nhãn bộ đếm và cơ chế cập nhật tự động sau mỗi thao tác thành công. Tuyệt đối không nhúng SQL vào giao diện.", bold_prefix="1. Mục tiêu Task: ")
    add_p(doc, "TV1 (Giao diện) phụ trách chính; TV5 hỗ trợ tích hợp, TV2 và TV3 hỗ trợ kết nối hàm.", bold_prefix="2. Người chịu trách nhiệm: ")
    add_p(doc, "TASK-01 đã hoàn thành; API Contract đã thống nhất; nhánh `feature/ui` đã được tạo từ `develop`.", bold_prefix="3. Điều kiện đầu vào: ")
    
    add_p(doc, "TV1 triển khai các bước xây dựng giao diện trong `ui.py`:", bold_prefix="4. Các bước thực hiện theo thứ tự: ")
    add_bullet(doc, "Bước 1: Khởi tạo lớp ứng dụng `RoomSeatApp` kế thừa từ `tk.Tk` hoặc sử dụng cửa sổ gốc `root` với kích thước 800×650, tiêu đề chuyên nghiệp.")
    add_bullet(doc, "Bước 2: Tạo khu vực Header chứa tiêu đề ứng dụng và nhãn bộ đếm chỗ ngồi (Đã dùng: X / 12 | Còn trống: Y).")
    add_bullet(doc, "Bước 3: Tạo khu vực Sơ đồ phòng máy (Frame trung tâm) chứa 12 nút máy tính theo ma trận 3 hàng × 4 cột (Hàng A: A1–A4; Hàng B: B1–B4; Hàng C: C1–C4).")
    add_bullet(doc, "Bước 4: Cấu hình màu sắc trực quan: Chỗ trống hiển thị màu xanh nhạt (#E8EEF5) với nhãn 'A1\\n[Trống]'; Chỗ đã có người hiển thị màu xanh lá (#C8E6C9) với nhãn 'A2\\n[SV100]'. Nút được click chọn sẽ được viền đậm hoặc đổi màu để nhận diện.")
    add_bullet(doc, "Bước 5: Tạo biến lưu trữ chỗ ngồi hiện tại `self.selected_seat = None` và hàm `select_seat(seat_code)` bắt sự kiện khi click vào nút.")
    add_bullet(doc, "Bước 6: Tạo khu vực Nhập liệu & Thao tác (Frame dưới) gồm: Nhãn 'Mã sinh viên:', Ô nhập liệu `tk.Entry` và 3 nút bấm nổi bật: [Xếp chỗ], [Tra cứu sinh viên], [Trả chỗ].")
    add_bullet(doc, "Bước 7: Tạo khu vực Footer hiển thị nhãn trạng thái (Status Bar) để hiển thị thông báo kết quả thao tác.")
    add_bullet(doc, "Bước 8: Viết các hàm xử lý sự kiện: `handle_assign()`, `handle_search()`, `handle_release()` gọi trực tiếp các hàm nghiệp vụ của TV2 và TV3.")
    add_bullet(doc, "Bước 9: Viết hàm `refresh_ui()` gọi `get_seat_map()` và `get_seat_stats()` để cập nhật lại màu sắc 12 nút và bộ đếm ngay lập tức sau mỗi thao tác thành công hoặc khi mở ứng dụng.")
    
    add_p(doc, "ui.py (tạo mới và hoàn thiện toàn bộ GUI Tkinter).", bold_prefix="5. Tệp cần tạo hoặc chỉnh sửa: ")
    
    # Chèn sơ đồ ma trận chỗ ngồi
    add_image_box(doc, "diagram_seat_matrix.png", "Minh họa bố cục giao diện 12 chỗ ngồi (3 hàng × 4 cột) và bộ đếm", width_inches=5.8)
    
    add_p(doc, "Mã nguồn Tkinter hoàn chỉnh, thiết kế hướng đối tượng chuẩn Senior cho `ui.py`:", bold_prefix="6. Hướng dẫn code hoặc thuật toán cần triển khai: ")
    code_ui = """# ui.py
import tkinter as tk
from tkinter import messagebox
from typing import Optional, Dict

# Import trực tiếp các dịch vụ nghiệp vụ theo đúng hợp đồng API Contract
from seat_service import assign_seat, release_seat, VALID_SEATS
from student_service import find_student
from statistics import get_seat_stats, get_seat_map

class RoomSeatApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("HỆ THỐNG QUẢN LÝ XẾP CHỖ PHÒNG MÁY - 12 VỊ TRÍ")
        self.root.geometry("820x660")
        self.root.resizable(False, False)
        self.root.configure(bg="#F4F6F9")
        
        self.selected_seat: Optional[str] = None
        self.seat_buttons: Dict[str, tk.Button] = {}
        
        self._build_header()
        self._build_seat_matrix()
        self._build_control_panel()
        self._build_status_bar()
        
        # Tải dữ liệu ban đầu từ SQLite
        self.refresh_ui()

    def _build_header(self):
        \"\"\"Xây dựng tiêu đề ứng dụng và thanh thống kê bộ đếm.\"\"\"
        header_frame = tk.Frame(self.root, bg="#1B365D", height=80)
        header_frame.pack(fill=tk.X, side=tk.TOP)
        
        title_lbl = tk.Label(
            header_frame, text="QUẢN LÝ XẾP CHỖ PHÒNG THỰC HÀNH MÁY TÍNH",
            font=("Arial", 15, "bold"), fg="#FFFFFF", bg="#1B365D"
        )
        title_lbl.pack(pady=(12, 4))
        
        self.stats_lbl = tk.Label(
            header_frame, text="Đang tải dữ liệu bộ đếm...",
            font=("Arial", 10, "bold"), fg="#E8EEF5", bg="#1B365D"
        )
        self.stats_lbl.pack(pady=(0, 10))

    def _build_seat_matrix(self):
        \"\"\"Xây dựng lưới 12 chỗ ngồi bố trí 3 hàng x 4 cột.\"\"\"
        matrix_frame = tk.LabelFrame(
            self.root, text=" SƠ ĐỒ PHÒNG MÁY (12 CHỖ NGỒI - BẤM ĐỂ CHỌN) ",
            font=("Arial", 11, "bold"), fg="#1B365D", bg="#FFFFFF",
            padx=20, pady=15, relief=tk.GROOVE
        )
        matrix_frame.pack(padx=25, pady=15, fill=tk.BOTH, expand=True)
        
        rows = ["A", "B", "C"]
        cols = [1, 2, 3, 4]
        
        for r_idx, row_name in enumerate(rows):
            for c_idx, col_num in enumerate(cols):
                seat_code = f"{row_name}{col_num}"
                btn = tk.Button(
                    matrix_frame, text=f"{seat_code}\\n[Trống]",
                    font=("Arial", 10, "bold"), width=13, height=3,
                    relief=tk.RAISED, cursor="hand2",
                    command=lambda s=seat_code: self.on_seat_clicked(s)
                )
                btn.grid(row=r_idx, column=c_idx, padx=12, pady=10)
                self.seat_buttons[seat_code] = btn

    def _build_control_panel(self):
        \"\"\"Xây dựng cụm nút bấm và ô nhập liệu mã sinh viên.\"\"\"
        ctrl_frame = tk.Frame(self.root, bg="#F4F6F9")
        ctrl_frame.pack(padx=25, pady=5, fill=tk.X)
        
        # Ô hiển thị chỗ đang chọn & Ô nhập mã SV
        input_frame = tk.Frame(ctrl_frame, bg="#F4F6F9")
        input_frame.pack(side=tk.TOP, pady=5)
        
        self.selected_info_lbl = tk.Label(
            input_frame, text="Vị trí chọn: [Chưa chọn]",
            font=("Arial", 10, "bold"), fg="#2E75B6", bg="#F4F6F9", width=22, anchor="w"
        )
        self.selected_info_lbl.pack(side=tk.LEFT, padx=5)
        
        lbl_sv = tk.Label(input_frame, text="Mã sinh viên:", font=("Arial", 10, "bold"), bg="#F4F6F9")
        lbl_sv.pack(side=tk.LEFT, padx=(15, 5))
        
        self.entry_sv = tk.Entry(input_frame, font=("Arial", 11, "bold"), width=14, justify="center")
        self.entry_sv.pack(side=tk.LEFT, padx=5)
        
        # Cụm nút hành động
        btn_frame = tk.Frame(ctrl_frame, bg="#F4F6F9")
        btn_frame.pack(side=tk.TOP, pady=8)
        
        btn_assign = tk.Button(
            btn_frame, text="✓ XẾP CHỖ", font=("Arial", 10, "bold"),
            bg="#28A745", fg="#FFFFFF", width=14, height=1, cursor="hand2",
            command=self.handle_assign
        )
        btn_assign.pack(side=tk.LEFT, padx=8)
        
        btn_search = tk.Button(
            btn_frame, text="🔍 TRA CỨU SV", font=("Arial", 10, "bold"),
            bg="#2E75B6", fg="#FFFFFF", width=14, height=1, cursor="hand2",
            command=self.handle_search
        )
        btn_search.pack(side=tk.LEFT, padx=8)
        
        btn_release = tk.Button(
            btn_frame, text="✕ TRẢ CHỖ", font=("Arial", 10, "bold"),
            bg="#D32F2F", fg="#FFFFFF", width=14, height=1, cursor="hand2",
            command=self.handle_release
        )
        btn_release.pack(side=tk.LEFT, padx=8)

    def _build_status_bar(self):
        \"\"\"Thanh thông báo trạng thái phía đáy ứng dụng.\"\"\"
        self.status_bar = tk.Label(
            self.root, text="Hệ thống sẵn sàng phục vụ.",
            font=("Arial", 9, "italic"), fg="#333333", bg="#E8EEF5",
            anchor="w", padx=10, relief=tk.SUNKEN, height=2
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def on_seat_clicked(self, seat_code: str):
        \"\"\"Xử lý sự kiện khi người dùng click vào một nút chỗ ngồi.\"\"\"
        self.selected_seat = seat_code
        self.selected_info_lbl.config(text=f"Vị trí chọn: [{seat_code}]")
        self.status_bar.config(text=f"Đã chọn vị trí máy {seat_code}. Hãy nhập mã sinh viên để xếp hoặc bấm Trả chỗ.")
        
        # Cập nhật viền nổi bật cho nút đang chọn
        for s_code, btn in self.seat_buttons.items():
            if s_code == seat_code:
                btn.config(relief=tk.SOLID, bd=3)
            else:
                btn.config(relief=tk.RAISED, bd=1)

    def handle_assign(self):
        \"\"\"Bắt sự kiện nút Xếp chỗ và gọi seat_service.assign_seat.\"\"\"
        if not self.selected_seat:
            messagebox.showwarning("Cảnh báo", "Vui lòng click chọn một vị trí máy trên sơ đồ trước khi xếp chỗ!")
            return
            
        ma_sv = self.entry_sv.get().strip().upper()
        if not ma_sv:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập mã sinh viên (ví dụ: SV100)!")
            self.entry_sv.focus()
            return
            
        success, message = assign_seat(self.selected_seat, ma_sv)
        if success:
            messagebox.showinfo("Thành công", message)
            self.entry_sv.delete(0, tk.END)
            self.refresh_ui()
            self.status_bar.config(text=message, fg="#155724")
        else:
            messagebox.showerror("Thất bại", message)
            self.status_bar.config(text=f"Lỗi: {message}", fg="#721c24")

    def handle_release(self):
        \"\"\"Bắt sự kiện nút Trả chỗ và gọi seat_service.release_seat.\"\"\"
        if not self.selected_seat:
            messagebox.showwarning("Cảnh báo", "Vui lòng click chọn vị trí máy cần trả trên sơ đồ!")
            return
            
        confirm = messagebox.askyesno("Xác nhận", f"Bạn có chắc chắn muốn trả lại vị trí máy {self.selected_seat}?")
        if not confirm:
            return
            
        success, message = release_seat(self.selected_seat)
        if success:
            messagebox.showinfo("Thành công", message)
            self.refresh_ui()
            self.status_bar.config(text=message, fg="#155724")
        else:
            messagebox.showwarning("Không thể trả chỗ", message)
            self.status_bar.config(text=f"Cảnh báo: {message}", fg="#856404")

    def handle_search(self):
        \"\"\"Bắt sự kiện nút Tra cứu và gọi student_service.find_student.\"\"\"
        ma_sv = self.entry_sv.get().strip().upper()
        if not ma_sv:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập mã sinh viên cần tra cứu!")
            self.entry_sv.focus()
            return
            
        student_info = find_student(ma_sv)
        if student_info is None:
            messagebox.showerror("Không tìm thấy", f"Không tìm thấy sinh viên có mã '{ma_sv}' trong hệ thống!")
            self.status_bar.config(text=f"Không tìm thấy sinh viên {ma_sv}.", fg="#721c24")
        else:
            ho_ten = student_info["ho_ten"]
            ma_cho = student_info["ma_cho"]
            
            if ma_cho:
                msg = f"Sinh viên: {ho_ten} ({ma_sv})\\nTrạng thái: ĐÃ XẾP CHỖ tại vị trí [{ma_cho}]."
                messagebox.showinfo("Kết quả tra cứu", msg)
                # Tự động chọn vị trí chỗ ngồi trên giao diện để người dùng dễ quan sát
                self.on_seat_clicked(ma_cho)
            else:
                msg = f"Sinh viên: {ho_ten} ({ma_sv})\\nTrạng thái: CHƯA ĐƯỢC XẾP CHỖ."
                messagebox.showinfo("Kết quả tra cứu", msg)
                
            self.status_bar.config(text=msg.replace("\\n", " | "), fg="#004085")

    def refresh_ui(self):
        \"\"\"Đồng bộ lại toàn bộ 12 nút và bộ đếm từ SQLite Database.\"\"\"
        # 1. Cập nhật bộ đếm
        used, total, avail = get_seat_stats()
        self.stats_lbl.config(
            text=f"TỔNG SỐ CHỖ: {total}   |   ĐÃ SỬ DỤNG: {used} / {total}   |   CÒN TRỐNG: {avail}"
        )
        
        # 2. Cập nhật trạng thái và màu sắc 12 nút
        seat_map = get_seat_map()
        for seat_code, ma_sv in seat_map.items():
            btn = self.seat_buttons.get(seat_code)
            if btn:
                if ma_sv:
                    # Chỗ đã có sinh viên
                    btn.config(
                        text=f"{seat_code}\\n[{ma_sv}]",
                        bg="#C8E6C9", fg="#1B5E20"  # Nền xanh lá nhạt, chữ đậm
                    )
                else:
                    # Chỗ còn trống
                    btn.config(
                        text=f"{seat_code}\\n[Trống]",
                        bg="#E8EEF5", fg="#1B365D"  # Nền xanh nhạt, chữ navy
                    )

if __name__ == "__main__":
    root = tk.Tk()
    app = RoomSeatApp(root)
    root.mainloop()
"""
    add_code_block(doc, code_ui, language="Python: ui.py")
    
    add_p(doc, "seat_service.py, student_service.py, statistics.py, main.py.", bold_prefix="7. Các module liên quan: ")
    add_p(doc, "Tệp ui.py chạy mượt mà, đầy đủ 12 nút, ô nhập liệu, thông báo và cơ chế cập nhật tự động.", bold_prefix="8. Kết quả đầu ra cần bàn giao: ")
    add_callout(doc, "DoD của TASK-06", 
                "Chạy `python ui.py` cửa sổ hiện lên đúng 820x660; 12 nút bố trí 3x4 đúng vị trí A1-C4; "
                "chọn chỗ hiển thị viền đậm; xếp/trả chỗ tự động cập nhật màu nút và bộ đếm.", callout_type="success")
    
    add_p(doc, "Chạy trực tiếp `python ui.py` từ terminal, thao tác thử nghiệm click vào từng nút chỗ ngồi và bấm các nút chức năng để kiểm tra phản hồi giao diện.", bold_prefix="10. Cách tự kiểm thử Task: ")

    # -------------------------------------------------------------------------
    # TASK-07
    # -------------------------------------------------------------------------
    add_styled_heading(doc, "TASK-07: Kiểm Thử Đơn Vị Độc Lập Từng Module (Unit / Self-Testing)", level=2)
    
    add_p(doc, "Mỗi thành viên tự chạy kịch bản kiểm thử độc lập cho module mình phụ trách trên môi trường CSDL thử nghiệm để đảm bảo không có lỗi cú pháp, lỗi logic hoặc lỗi kiểu dữ liệu trước khi gửi Pull Request.", bold_prefix="1. Mục tiêu Task: ")
    add_p(doc, "Toàn bộ 4 thành viên (TV1, TV2, TV3, TV4) tự thực hiện; TV5 giám sát và xác nhận kết quả.", bold_prefix="2. Người chịu trách nhiệm: ")
    add_p(doc, "Các Task từ TASK-02 đến TASK-06 đã hoàn thành mã nguồn độc lập.", bold_prefix="3. Điều kiện đầu vào: ")
    
    add_p(doc, "Quy trình kiểm thử đơn vị cho từng thành viên:", bold_prefix="4. Các bước thực hiện theo thứ tự: ")
    add_bullet(doc, "TV4 tự kiểm thử: Chạy `tao_du_lieu_demo.py` hai lần liên tiếp trên tệp CSDL mới, kiểm tra `SELECT COUNT(*)` luôn bằng 100.")
    add_bullet(doc, "TV2 tự kiểm thử: Viết script gọi `assign_seat` với 4 ca biên (hợp lệ, chỗ có người, SV có chỗ, SV không tồn tại) và `release_seat` (chỗ có người, chỗ trống).")
    add_bullet(doc, "TV3 tự kiểm thử: Viết script gọi `find_student` với 3 ca (SV không tồn tại -> None; SV chưa xếp -> dict ma_cho=None; SV đã xếp -> dict ma_cho có giá trị) và kiểm tra `get_seat_stats`, `get_seat_map`.")
    add_bullet(doc, "TV1 tự kiểm thử: Chạy giao diện `ui.py` độc lập với CSDL test, click thử 12 nút, nhập dữ liệu và quan sát thông báo.")
    add_bullet(doc, "Báo cáo kết quả PASS cho TV5 trước khi tạo Pull Request.")
    
    add_p(doc, "tests/test_unit_modules.py, tệp nhật ký kiểm thử nội bộ.", bold_prefix="5. Tệp cần tạo hoặc chỉnh sửa: ")
    
    add_p(doc, "Script kiểm thử đơn vị tổng hợp chạy tự động toàn bộ module lõi:", bold_prefix="6. Hướng dẫn code hoặc thuật toán cần triển khai: ")
    code_unit = """# tests/test_unit_modules.py
import os
import sqlite3
from database import init_db, get_connection
from tao_du_lieu_demo import seed_students
from seat_service import assign_seat, release_seat
from student_service import find_student
from statistics import get_seat_stats, get_seat_map

TEST_DB = "test_unit.db"

def run_all_unit_tests():
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)
        
    print("=== BẮT ĐẦU KIỂM THỬ ĐƠN VỊ TỪNG MODULE ===")
    
    # 1. Test TV4: Database & Seed
    init_db(TEST_DB)
    count1 = seed_students(100, TEST_DB)
    count2 = seed_students(100, TEST_DB)
    assert count1 == 100 and count2 == 100, "LỖI: Seed data không an toàn!"
    print("[PASS] Module TV4: Seed 100 SV an toàn lặp 2 lần.")
    
    # 2. Test TV3: Tra cứu SV trước khi xếp
    sv100 = find_student("SV100", TEST_DB)
    assert sv100 is not None and sv100["ma_cho"] is None, "LỖI: Trạng thái SV chưa xếp!"
    sv999 = find_student("SV999", TEST_DB)
    assert sv999 is None, "LỖI: Mã SV không tồn tại phải trả về None!"
    print("[PASS] Module TV3: Tra cứu chính xác SV chưa xếp và SV không tồn tại.")
    
    # 3. Test TV2: Xếp chỗ hợp lệ & vi phạm
    ok, _ = assign_seat("A2", "SV100", TEST_DB)
    assert ok, "LỖI: Xếp A2 cho SV100 thất bại!"
    ok, _ = assign_seat("A2", "SV001", TEST_DB)
    assert not ok, "LỖI: Cho phép xếp đè chỗ đã có người!"
    ok, _ = assign_seat("B1", "SV100", TEST_DB)
    assert not ok, "LỖI: Cho phép SV100 ngồi 2 chỗ!"
    print("[PASS] Module TV2: Xếp chỗ bắt đúng 3 trường hợp ràng buộc.")
    
    # 4. Test TV3: Stats & Map sau khi xếp
    used, total, avail = get_seat_stats(TEST_DB)
    assert used == 1 and total == 12 and avail == 11, "LỖI: Bộ đếm tính toán sai!"
    seat_map = get_seat_map(TEST_DB)
    assert seat_map["A2"] == "SV100" and seat_map["B1"] is None, "LỖI: Seat map sai!"
    print("[PASS] Module TV3: Thống kê bộ đếm 1/12 và bản đồ 12 vị trí chính xác.")
    
    # 5. Test TV2: Trả chỗ
    ok, _ = release_seat("A2", TEST_DB)
    assert ok, "LỖI: Trả chỗ A2 thất bại!"
    sv100_after = find_student("SV100", TEST_DB)
    assert sv100_after is not None, "LỖI NGHIÊM TRỌNG: Trả chỗ đã làm mất hồ sơ sinh viên!"
    print("[PASS] Module TV2: Trả chỗ thành công, bảo toàn hồ sơ sinh viên.")
    
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)
    print("=== TẤT CẢ CÁC MODULE ĐỀU ĐẠT TIÊU CHUẨN UNIT TEST ===")

if __name__ == "__main__":
    run_all_unit_tests()
"""
    add_code_block(doc, code_unit, language="Python: tests/test_unit_modules.py")
    
    add_p(doc, "Toàn bộ các module trong hệ thống.", bold_prefix="7. Các module liên quan: ")
    add_p(doc, "Báo cáo kiểm thử đơn vị thành công cho cả 4 module lõi.", bold_prefix="8. Kết quả đầu ra cần bàn giao: ")
    add_callout(doc, "DoD của TASK-07", 
                "Tất cả các khẳng định (assert) trong `test_unit_modules.py` đều vượt qua không có Exception nào. "
                "TV5 xác nhận cho phép tạo Pull Request vào nhánh develop.", callout_type="success")
    add_p(doc, "Chạy lệnh `python tests/test_unit_modules.py` và quan sát 5 thông báo [PASS] xuất hiện trên console.", bold_prefix="10. Cách tự kiểm thử Task: ")

    # -------------------------------------------------------------------------
    # TASK-08
    # -------------------------------------------------------------------------
    add_styled_heading(doc, "TASK-08: Tích Hợp Các Module Vào Luồng Ứng Dụng Hoàn Chỉnh (main.py)", level=2)
    
    add_p(doc, "Tích hợp toàn bộ các nhánh tính năng vào nhánh develop, giải quyết xung đột import nếu có và hoàn thiện tệp điểm khởi chạy main.py để ứng dụng tự động kiểm tra, khởi tạo CSDL, nạp sinh viên demo và mở giao diện Tkinter.", bold_prefix="1. Mục tiêu Task: ")
    add_p(doc, "TV5 (Kiểm thử & Tích hợp) chủ trì; Cả nhóm hỗ trợ rà soát mã nguồn.", bold_prefix="2. Người chịu trách nhiệm: ")
    add_p(doc, "TASK-07 đã pass toàn bộ; tất cả Pull Request của TV1, TV2, TV3, TV4 đã được merge vào `develop`.", bold_prefix="3. Điều kiện đầu vào: ")
    
    add_p(doc, "TV5 thực hiện các bước tích hợp:", bold_prefix="4. Các bước thực hiện theo thứ tự: ")
    add_bullet(doc, "Bước 1: Trên máy TV5, chuyển sang nhánh `develop` và chạy `git pull origin develop` để lấy toàn bộ mã nguồn mới nhất.")
    add_bullet(doc, "Bước 2: Mở tệp `main.py`, thiết lập hàm `main()` điều phối khởi động.")
    add_bullet(doc, "Bước 3: Gọi `init_db()` để tạo bảng SQLite.")
    add_bullet(doc, "Bước 4: Gọi `seed_students(100)` để đảm bảo CSDL có sẵn 100 sinh viên demo nếu là lần chạy đầu tiên.")
    add_bullet(doc, "Bước 5: Khởi tạo cửa sổ `root = tk.Tk()`, khởi tạo đối tượng `RoomSeatApp(root)` và gọi `root.mainloop()`.")
    add_bullet(doc, "Bước 6: Chạy thử `python main.py` và kiểm tra toàn bộ luồng hoạt động thông suốt từ GUI đến Database.")
    
    add_p(doc, "main.py (hoàn thiện).", bold_prefix="5. Tệp cần tạo hoặc chỉnh sửa: ")
    
    add_p(doc, "Mã nguồn hoàn chỉnh cho tệp khởi chạy trung tâm `main.py`:", bold_prefix="6. Hướng dẫn code hoặc thuật toán cần triển khai: ")
    code_main = """# main.py
\"\"\"
ĐIỂM KHỞI CHẠY CHÍNH CỦA ỨNG DỤNG QUẢN LÝ XẾP CHỖ PHÒNG MÁY (12 CHỖ)
Thành viên phụ trách tích hợp: TV5 - Kiểm thử & Tích hợp
\"\"\"
import sys
import tkinter as tk
from database import init_db
from tao_du_lieu_demo import seed_students
from ui import RoomSeatApp

def main():
    print("[*] Đang khởi động Hệ thống Quản lý Xếp chỗ Phòng máy...")
    
    # 1. Khởi tạo cấu trúc bảng SQLite (nếu chưa có)
    try:
        init_db("phong_may.db")
        print("[+] Khởi tạo cấu trúc CSDL phong_may.db thành công.")
    except Exception as e:
        print(f"[-] LỖI KHỞI TẠO CSDL: {e}")
        sys.exit(1)
        
    # 2. Đảm bảo nạp dữ liệu 100 sinh viên demo
    try:
        total_sv = seed_students(100, "phong_may.db")
        print(f"[+] Đồng bộ dữ liệu demo thành công! Tổng số hồ sơ SV: {total_sv}")
    except Exception as e:
        print(f"[-] LỖI NẠP DỮ LIỆU DEMO: {e}")
        sys.exit(1)
        
    # 3. Khởi chạy giao diện người dùng Tkinter
    print("[*] Đang khởi động Giao diện Đồ họa Tkinter...")
    root = tk.Tk()
    app = RoomSeatApp(root)
    root.mainloop()
    print("[*] Ứng dụng đã đóng an toàn. Toàn bộ trạng thái đã được lưu trong SQLite.")

if __name__ == "__main__":
    main()
"""
    add_code_block(doc, code_main, language="Python: main.py")
    
    add_p(doc, "Tất cả các module trong dự án (database, seed, seat, student, stats, ui).", bold_prefix="7. Các module liên quan: ")
    add_p(doc, "Tệp main.py hoàn chỉnh, khởi chạy ứng dụng mượt mà chỉ với một câu lệnh `python main.py`.", bold_prefix="8. Kết quả đầu ra cần bàn giao: ")
    add_callout(doc, "DoD của TASK-08", 
                "Chạy `python main.py` trong thư mục sạch; CSDL phong_may.db tự sinh; 100 sinh viên tự nạp; "
                "giao diện Tkinter hiện lên với 12 nút; không có bất kỳ thông báo lỗi nào trên terminal console.", callout_type="success")
    add_p(doc, "Chạy lệnh `python main.py` từ dòng lệnh và kiểm tra các log thông báo hiển thị tuần tự từ bước 1 đến bước 3.", bold_prefix="10. Cách tự kiểm thử Task: ")

    # -------------------------------------------------------------------------
    # TASK-09
    # -------------------------------------------------------------------------
    add_styled_heading(doc, "TASK-09: Kiểm Thử Tích Hợp Hệ Thống (SIT) và Xử Lý Lỗi Phát Sinh", level=2)
    
    add_p(doc, "Thực hiện kiểm thử toàn diện kịch bản tích hợp từ đầu đến cuối (End-to-End) theo đúng 7 ca kiểm thử bắt buộc (TC01 đến TC07) của đề bài, kiểm tra tính toàn vẹn dữ liệu SQLite và khả năng phục hồi trạng thái khi đóng/mở lại ứng dụng.", bold_prefix="1. Mục tiêu Task: ")
    add_p(doc, "TV5 chủ trì kiểm thử; Toàn bộ thành viên sẵn sàng tiếp nhận Bug Report và sửa lỗi.", bold_prefix="2. Người chịu trách nhiệm: ")
    add_p(doc, "TASK-08 đã hoàn thành; tệp main.py đã tích hợp thành công trên nhánh `develop`.", bold_prefix="3. Điều kiện đầu vào: ")
    
    add_p(doc, "Các bước tiến hành kiểm thử tích hợp:", bold_prefix="4. Các bước thực hiện theo thứ tự: ")
    add_bullet(doc, "Bước 1: Chuẩn bị môi trường CSDL sạch (xóa tệp phong_may.db cũ nếu cần kiểm tra luồng từ đầu).")
    add_bullet(doc, "Bước 2: Mở tệp `tests/test_scenarios.md` (hoặc bảng checklist) để ghi chép.")
    add_bullet(doc, "Bước 3: Chạy ứng dụng bằng lệnh `python main.py`.")
    add_bullet(doc, "Bước 4: Thực hiện tuần tự 7 ca kiểm thử bắt buộc: TC01 (Seed 2 lần), TC02 (Tra cứu SV100), TC03 (Xếp SV100 vào A2), TC04 (Xếp SV001 vào A2), TC05 (Xếp SV100 vào B1), TC06 (Đóng và mở lại ứng dụng), TC07 (Trả chỗ A2 rồi tra cứu lại SV100).")
    add_bullet(doc, "Bước 5: Với mỗi ca, đối chiếu kết quả trên giao diện và kiểm tra trực tiếp dữ liệu trong bảng `xep_cho` của SQLite.")
    add_bullet(doc, "Bước 6: Nếu phát hiện lỗi (FAIL): TV5 tạo Bug Report, gán cho thành viên phụ trách module đó sửa ngay lập tức, sau đó re-test lại.")
    
    add_p(doc, "tests/test_scenarios.md, TEST_REPORT.md.", bold_prefix="5. Tệp cần tạo hoặc chỉnh sửa: ")
    add_p(doc, "Thuật toán kiểm thử đối sánh 2 lớp: Luôn kiểm tra song song (1) Phản hồi trên giao diện người dùng và (2) Bản ghi thực tế trong CSDL SQLite.", bold_prefix="6. Hướng dẫn code hoặc thuật toán cần triển khai: ")
    add_p(doc, "Toàn bộ hệ thống.", bold_prefix="7. Các module liên quan: ")
    add_p(doc, "Báo cáo kiểm thử tích hợp đầy đủ 7/7 ca PASS, không còn bất kỳ lỗi Blocker hay High nào tồn đọng.", bold_prefix="8. Kết quả đầu ra cần bàn giao: ")
    add_callout(doc, "DoD của TASK-09", 
                "Tất cả 7 ca kiểm thử bắt buộc TC01–TC07 đều đạt kết quả PASS trên bản tích hợp; "
                "đặc biệt ca TC06 (đóng mở lại giữ nguyên trạng thái) và TC07 (trả chỗ không mất sinh viên) hoạt động hoàn hảo 100%.", callout_type="success")
    add_p(doc, "Thực hiện toàn bộ kịch bản kiểm thử theo đúng trình tự mô tả chi tiết tại Phần VI của tài liệu này.", bold_prefix="10. Cách tự kiểm thử Task: ")

    # -------------------------------------------------------------------------
    # TASK-10
    # -------------------------------------------------------------------------
    add_styled_heading(doc, "TASK-10: Hoàn Thiện Tài Liệu, Đóng Gói Sản Phẩm và Chuẩn Bị Nghiệm Thu", level=2)
    
    add_p(doc, "Hợp nhất nhánh develop vào main, gắn thẻ phiên bản release v1.0, dọn dẹp các tệp tạm/rác, hoàn thiện Bảng đóng góp của 5 thành viên và kiểm tra chạy thử trong một thư mục hoàn toàn mới trước khi nộp bài.", bold_prefix="1. Mục tiêu Task: ")
    add_p(doc, "Cả nhóm 05 thành viên cùng thực hiện; TV5 điều phối đóng gói.", bold_prefix="2. Người chịu trách nhiệm: ")
    add_p(doc, "TASK-09 đã PASS 100% tất cả các ca kiểm thử.", bold_prefix="3. Điều kiện đầu vào: ")
    
    add_p(doc, "Các bước đóng gói và hoàn tất bài nộp:", bold_prefix="4. Các bước thực hiện theo thứ tự: ")
    add_bullet(doc, "Bước 1: TV5 tạo Pull Request hợp nhất nhánh `develop` vào nhánh `main`, đặt tên là `Release v1.0 - Bài tập nhóm hoàn chỉnh`.")
    add_bullet(doc, "Bước 2: Các thành viên rà soát lại mã nguồn lần cuối, bảo đảm giữ nguyên các comment giải thích thuật toán, tuân thủ PEP 8.")
    add_bullet(doc, "Bước 3: Xóa sạch các thư mục rác `__pycache__`, file `.tmp`, file log thử nghiệm.")
    add_bullet(doc, "Bước 4: Điền đầy đủ thông tin Họ tên, Mã sinh viên, Phần việc phụ trách và Tỷ lệ % đóng góp vào Bảng đóng góp thành viên.")
    add_bullet(doc, "Bước 5: Thử nghiệm 'Clean Directory Test': Sao chép toàn bộ thư mục bài nộp sang một vị trí khác (hoặc máy tính khác), mở terminal và gõ `python main.py` xem ứng dụng có chạy ngay lập tức hay không.")
    add_bullet(doc, "Bước 6: Đóng gói tệp nén `.zip` (hoặc nộp link GitHub theo quy định của Giảng viên) và chuẩn bị slide/kịch bản demo 5 phút.")
    
    add_p(doc, "README.md, Bảng đóng góp thành viên, phong_may_app.zip.", bold_prefix="5. Tệp cần tạo hoặc chỉnh sửa: ")
    add_p(doc, "Quy tắc kiểm tra bản nộp sạch (Smoke test trên thư mục cô lập).", bold_prefix="6. Hướng dẫn code hoặc thuật toán cần triển khai: ")
    add_p(doc, "Toàn bộ dự án.", bold_prefix="7. Các module liên quan: ")
    add_p(doc, "Bộ mã nguồn hoàn chỉnh chạy được ngay, tệp CSDL phong_may.db, script sinh dữ liệu, tài liệu báo cáo và bảng đóng góp.", bold_prefix="8. Kết quả đầu ra cần bàn giao: ")
    add_callout(doc, "DoD của TASK-10", 
                "Sản phẩm cuối cùng đáp ứng đầy đủ 7 tiêu chí đánh giá của Giảng viên: "
                "(1) Chạy được ứng dụng; (2) Không nhân đôi dữ liệu demo; (3) Xếp/trả chỗ đúng luật; (4) Tra cứu phân biệt 3 trạng thái; "
                "(5) Sơ đồ & bộ đếm chuẩn SQLite; (6) Mở lại giữ trạng thái; (7) Cả 5 thành viên đều sẵn sàng giải thích code của mình.", callout_type="success")
    add_p(doc, "Kiểm tra danh mục tệp nộp bài đảm bảo không thiếu bất kỳ tệp nào trong cấu trúc chuẩn.", bold_prefix="10. Cách tự kiểm thử Task: ")
    
    doc.add_page_break()

print("Part 3 module initialized successfully!")
