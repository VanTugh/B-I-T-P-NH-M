import sqlite3
from tao_du_lieu_demo import DB_PATH, khoi_tao_du_lieu


class PhongMayModel:
    """
    Model (M trong MVC): Chịu trách nhiệm tương tác trực tiếp với cơ sở dữ liệu
    SQLite (phong_may.db) gồm 2 bảng 'sinh_vien' và 'xep_cho'.
    """

    def __init__(self, db_path: str = DB_PATH) -> None:
        self.db_path = db_path
        # Đảm bảo CSDL và 100 hồ sơ mẫu đã được khởi tạo
        khoi_tao_du_lieu(self.db_path)

    def _ket_noi(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def lay_danh_sach_xep_cho(self) -> dict[str, str]:
        """Lấy toàn bộ dữ liệu xếp chỗ hiện tại dưới dạng {ma_cho: ma_sv}."""
        conn = self._ket_noi()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT ma_cho, ma_sv FROM xep_cho")
            return dict(cursor.fetchall())
        finally:
            conn.close()

    def lay_sv_tai_ghe(self, ma_cho: str) -> str | None:
        """Kiểm tra ghế ma_cho đang có sinh viên nào ngồi (trả về None nếu trống)."""
        conn = self._ket_noi()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT ma_sv FROM xep_cho WHERE ma_cho = ?", (ma_cho,)
            )
            row = cursor.fetchone()
            return row[0] if row else None
        finally:
            conn.close()

    def lay_ghe_cua_sv(self, ma_sv: str) -> str | None:
        """Kiểm tra sinh viên ma_sv đang ngồi ở ghế nào (trả về None nếu chưa xếp)."""
        conn = self._ket_noi()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT ma_cho FROM xep_cho WHERE ma_sv = ?", (ma_sv,)
            )
            row = cursor.fetchone()
            return row[0] if row else None
        finally:
            conn.close()

    def lay_ho_ten_sv(self, ma_sv: str) -> str | None:
        """Lấy họ tên sinh viên từ bảng sinh_vien (trả về None nếu không tồn tại)."""
        conn = self._ket_noi()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT ho_ten FROM sinh_vien WHERE ma_sv = ?", (ma_sv,)
            )
            row = cursor.fetchone()
            return row[0] if row else None
        finally:
            conn.close()

    def them_xep_cho(self, ma_cho: str, ma_sv: str) -> None:
        """
        Thêm bản ghi xếp chỗ mới vào bảng xep_cho.
        Ném ngoại lệ sqlite3.IntegrityError nếu vi phạm ràng buộc UNIQUE hoặc PK.
        """
        conn = self._ket_noi()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO xep_cho (ma_cho, ma_sv) VALUES (?, ?)",
                (ma_cho, ma_sv),
            )
            conn.commit()
        finally:
            conn.close()

    def xoa_xep_cho(self, ma_cho: str) -> bool:
        """Xóa bản ghi xếp chỗ theo mã ghế. Trả về True nếu xóa thành công."""
        conn = self._ket_noi()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM xep_cho WHERE ma_cho = ?", (ma_cho,)
            )
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()

    def tra_cuu_sinh_vien(self, ma_sv: str) -> tuple[str, str | None] | None:
        """
        Tra cứu thông tin sinh viên và chỗ ngồi bằng LEFT JOIN.
        Trả về (ho_ten, ma_cho) hoặc None nếu mã SV không tồn tại.
        """
        conn = self._ket_noi()
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
            return (row[0], row[1]) if row else None
        finally:
            conn.close()
