import os
import sys

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import docx
from generator_core import add_header_footer
from build_sections_part1_2 import build_cover_page, build_toc, build_part_1, build_part_2
from build_sections_part3 import build_part_3
from build_sections_part4_7 import build_part_4, build_part_5, build_part_6, build_part_7

OUTPUT_DOCX = "HUONG_DAN_TRIEN_KHAI_TASK_BAI_TAP_PYTHON_NANG_CAO.docx"

def assemble_document():
    print("[*] Đang khởi tạo tài liệu Word (.docx) mới...")
    doc = docx.Document()
    
    print("[*] Đang cấu hình Header, Footer và Canh lề chuẩn A4...")
    add_header_footer(doc)
    
    print("[*] Đang xây dựng Trang bìa (Cover Page)...")
    build_cover_page(doc)
    
    print("[*] Đang xây dựng Mục lục & Danh mục thuật ngữ...")
    build_toc(doc)
    
    print("[*] Đang xây dựng PHẦN I: Tổng quan quy trình & Kiến trúc 3-Tier...")
    build_part_1(doc)
    
    print("[*] Đang xây dựng PHẦN II: Danh sách Task & Thứ tự thực hiện...")
    build_part_2(doc)
    
    print("[*] Đang xây dựng PHẦN III: Hướng dẫn chi tiết từng Task (TASK-01 đến TASK-10)...")
    build_part_3(doc)
    
    print("[*] Đang xây dựng PHẦN IV: Quy trình làm việc với Git/GitHub...")
    build_part_4(doc)
    
    print("[*] Đang xây dựng PHẦN V: Quy trình tích hợp module & Minh họa luồng...")
    build_part_5(doc)
    
    print("[*] Đang xây dựng PHẦN VI: Checklist nghiệm thu & Bộ tiêu chí chất lượng...")
    build_part_6(doc)
    
    print("[*] Đang xây dựng PHẦN VII: Bảng bàn giao trách nhiệm & Đóng góp...")
    build_part_7(doc)
    
    print(f"[*] Đang lưu tệp Word hoàn chỉnh vào: {OUTPUT_DOCX}...")
    doc.save(OUTPUT_DOCX)
    
    file_size = os.path.getsize(OUTPUT_DOCX)
    print(f"[+] THÀNH CÔNG! Đã tạo xong tài liệu: {OUTPUT_DOCX} (Kích thước: {file_size:,} bytes)")

if __name__ == "__main__":
    assemble_document()
