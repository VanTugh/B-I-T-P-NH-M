import os
import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

# --- COLOR PALETTE ---
COLOR_PRIMARY_NAVY = "1B365D"   # #1B365D - Navy chính
COLOR_SECONDARY_BLUE = "2E75B6" # #2E75B6 - Xanh dương tiêu đề phụ
COLOR_ACCENT_BLUE = "E8EEF5"    # #E8EEF5 - Nền xanh nhạt
COLOR_BG_GRAY = "F4F6F9"        # #F4F6F9 - Nền code / bảng zebra
COLOR_BORDER_GRAY = "D0D7DE"    # #D0D7DE - Viền mảnh
COLOR_TEXT_DARK = "262626"      # #262626 - Chữ chính
COLOR_SUCCESS_GREEN = "28A745"  # #28A745 - Xanh lá thành công
COLOR_ALERT_RED = "D32F2F"      # #D32F2F - Đỏ cảnh báo

# --- STYLING HELPERS ---

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Thiết lập padding cho cell trong bảng (đơn vị: dxa = 1/20 pt)."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_cell_shading(cell, color_hex):
    """Tô màu nền cho cell."""
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    tcPr.append(shd)

def set_cell_borders(cell, top="none", bottom="none", left="none", right="none", 
                     color="D0D7DE", sz="4"):
    """Thiết lập viền tùy chỉnh cho cell."""
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(f'''
        <w:tcBorders {nsdecls("w")}>
            <w:top w:val="{top}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:left w:val="{left}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:bottom w:val="{bottom}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:right w:val="{right}" w:sz="{sz}" w:space="0" w:color="{color}"/>
        </w:tcBorders>
    ''')
    tcPr.append(borders)

def add_header_footer(doc):
    """Cấu hình Header và Footer chuyên nghiệp cho tài liệu."""
    section = doc.sections[0]
    section.different_first_page_header_footer = True
    section.top_margin = Inches(0.8)
    section.bottom_margin = Inches(0.8)
    section.left_margin = Inches(0.8)
    section.right_margin = Inches(0.8)
    
    # Header cho các trang sau
    header = section.header
    hp = header.paragraphs[0]
    hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    hrun = hp.add_run("HƯỚNG DẪN TRIỂN KHAI TASK – PYTHON NÂNG CAO | TECH LEAD SPECIFICATION")
    hrun.font.name = "Arial"
    hrun.font.size = Pt(8.5)
    hrun.font.color.rgb = RGBColor(100, 110, 120)
    
    # Footer cho các trang sau
    footer = section.footer
    fp = footer.paragraphs[0]
    fp.alignment = WD_ALIGN_PARAGRAPH.LEFT
    frun1 = fp.add_run("Dự án: Quản lý Phòng máy (12 chỗ) | Nhóm 05 Thành viên – Sprint 120 phút")
    frun1.font.name = "Arial"
    frun1.font.size = Pt(8.5)
    frun1.font.color.rgb = RGBColor(100, 110, 120)
    
    # Thêm tab và số trang
    frun_tab = fp.add_run("\t\tTrang ")
    frun_tab.font.name = "Arial"
    frun_tab.font.size = Pt(8.5)
    frun_tab.font.color.rgb = RGBColor(100, 110, 120)
    
    # XML Page Number
    fldSimple = OxmlElement('w:fldSimple')
    fldSimple.set(qn('w:instr'), 'PAGE')
    fp._p.append(fldSimple)

def add_styled_heading(doc, text, level):
    """Thêm tiêu đề theo chuẩn font Arial và màu xanh thương hiệu."""
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.font.name = "Arial"
    run.bold = True
    
    if level == 1:
        run.font.size = Pt(16)
        run.font.color.rgb = RGBColor(27, 54, 93)  # #1B365D
        p.paragraph_format.space_before = Pt(16)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        
        # Thêm đường gạch chân mỏng trang nhã dưới Heading 1
        pBdr = parse_xml(f'''
            <w:pBdr {nsdecls("w")}>
                <w:bottom w:val="single" w:sz="12" w:space="4" w:color="{COLOR_PRIMARY_NAVY}"/>
            </w:pBdr>
        ''')
        p._p.get_or_add_pPr().append(pBdr)
        
    elif level == 2:
        run.font.size = Pt(13)
        run.font.color.rgb = RGBColor(46, 117, 182)  # #2E75B6
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
    elif level == 3:
        run.font.size = Pt(11)
        run.font.color.rgb = RGBColor(27, 54, 93)
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.keep_with_next = True
    return p

def add_p(doc, text, bold_prefix="", italic=False):
    """Thêm đoạn văn chuẩn font Arial 10pt."""
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(4)
    
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = "Arial"
        r_pre.font.size = Pt(10)
        r_pre.bold = True
        r_pre.font.color.rgb = RGBColor(27, 54, 93)
        
    run = p.add_run(text)
    run.font.name = "Arial"
    run.font.size = Pt(10)
    run.font.color.rgb = RGBColor(38, 38, 38)
    run.italic = italic
    return p

def add_bullet(doc, text, bold_prefix=""):
    """Thêm bullet point chuẩn."""
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.left_indent = Inches(0.25)
    
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = "Arial"
        r_pre.font.size = Pt(10)
        r_pre.bold = True
        r_pre.font.color.rgb = RGBColor(27, 54, 93)
        
    run = p.add_run(text)
    run.font.name = "Arial"
    run.font.size = Pt(10)
    run.font.color.rgb = RGBColor(38, 38, 38)
    return p

def add_callout(doc, title, text, callout_type="info"):
    """Thêm hộp ghi chú / cảnh báo chuyên nghiệp."""
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    
    cell = table.cell(0, 0)
    cell.width = Inches(6.8)
    set_cell_margins(cell, top=120, bottom=120, left=180, right=180)
    
    if callout_type == "warning":
        border_color = COLOR_ALERT_RED
        bg_color = "FFF5F5"
        prefix = f"⚠️ [CẢNH BÁO / LƯU Ý KỸ THUẬT]: {title}"
        text_color = RGBColor(180, 40, 40)
    elif callout_type == "success":
        border_color = COLOR_SUCCESS_GREEN
        bg_color = "F0FFF4"
        prefix = f"✅ [TIÊU CHUẨN HOÀN THÀNH - DoD]: {title}"
        text_color = RGBColor(30, 120, 50)
    else:
        border_color = COLOR_PRIMARY_NAVY
        bg_color = COLOR_ACCENT_BLUE
        prefix = f"ℹ️ [LƯU Ý QUAN TRỌNG TỪ TECH LEAD]: {title}"
        text_color = RGBColor(27, 54, 93)
        
    set_cell_borders(cell, left="single", color=border_color, sz="36")
    set_cell_shading(cell, bg_color)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    
    r_title = p.add_run(prefix + "\n")
    r_title.font.name = "Arial"
    r_title.font.size = Pt(9.5)
    r_title.bold = True
    r_title.font.color.rgb = text_color
    
    r_text = p.add_run(text)
    r_text.font.name = "Arial"
    r_text.font.size = Pt(9.5)
    r_text.font.color.rgb = RGBColor(40, 40, 40)
    
    # Khoảng cách sau bảng
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def add_code_block(doc, code_str, language="Python / Shell"):
    """Thêm khung hiển thị code chuẩn Monospace Consolas."""
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    
    cell = table.cell(0, 0)
    cell.width = Inches(6.8)
    set_cell_margins(cell, top=100, bottom=100, left=150, right=150)
    set_cell_borders(cell, top="single", bottom="single", left="single", right="single", color=COLOR_BORDER_GRAY, sz="4")
    set_cell_shading(cell, COLOR_BG_GRAY)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.05
    
    # Header language
    r_lang = p.add_run(f"# --- {language} ---\n")
    r_lang.font.name = "Consolas"
    r_lang.font.size = Pt(8.5)
    r_lang.bold = True
    r_lang.font.color.rgb = RGBColor(100, 110, 120)
    
    r_code = p.add_run(code_str.strip())
    r_code.font.name = "Consolas"
    r_code.font.size = Pt(9.0)
    r_code.font.color.rgb = RGBColor(30, 35, 42)
    
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def add_styled_table(doc, headers, data, col_widths=None):
    """Tạo bảng dữ liệu đẹp với header màu Navy và dòng xen kẽ."""
    table = doc.add_table(rows=len(data) + 1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    
    # Thiết lập lặp header khi qua trang
    header_tr = table.rows[0]._tr.get_or_add_trPr()
    header_tr.append(OxmlElement('w:tblHeader'))
    
    # Định dạng Header Row
    for col_idx, header_text in enumerate(headers):
        cell = table.cell(0, col_idx)
        if col_widths and col_idx < len(col_widths):
            cell.width = Inches(col_widths[col_idx])
        set_cell_margins(cell, top=120, bottom=120, left=140, right=140)
        set_cell_shading(cell, COLOR_PRIMARY_NAVY)
        set_cell_borders(cell, top="single", bottom="single", left="single", right="single", color="122540", sz="6")
        
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        run = p.add_run(header_text)
        run.font.name = "Arial"
        run.font.size = Pt(9.5)
        run.bold = True
        run.font.color.rgb = RGBColor(255, 255, 255)
        
    # Định dạng Data Rows
    for row_idx, row_data in enumerate(data):
        row = table.rows[row_idx + 1]
        
        # Ngăn row bị cắt ngang trang
        trPr = row._tr.get_or_add_trPr()
        trPr.append(OxmlElement('w:cantSplit'))
        
        bg_col = "FFFFFF" if row_idx % 2 == 0 else COLOR_BG_GRAY
        for col_idx, val in enumerate(row_data):
            cell = row.cells[col_idx]
            if col_widths and col_idx < len(col_widths):
                cell.width = Inches(col_widths[col_idx])
            set_cell_margins(cell, top=100, bottom=100, left=140, right=140)
            set_cell_shading(cell, bg_col)
            set_cell_borders(cell, top="single", bottom="single", left="single", right="single", color=COLOR_BORDER_GRAY, sz="4")
            
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(1)
            p.paragraph_format.line_spacing = 1.1
            
            # Căn giữa nếu là mã/ID hoặc ngắn
            if len(str(val)) <= 8 and (col_idx == 0 or "TC" in str(val) or "AC" in str(val) or "TV" in str(val) or "PASS" in str(val)):
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                
            run = p.add_run(str(val))
            run.font.name = "Arial"
            run.font.size = Pt(9.0)
            run.font.color.rgb = RGBColor(38, 38, 38)
            
            if "PASS" in str(val):
                run.bold = True
                run.font.color.rgb = RGBColor(40, 167, 69)
            elif "FAIL" in str(val):
                run.bold = True
                run.font.color.rgb = RGBColor(220, 53, 69)
                
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def add_image_box(doc, img_path, caption, width_inches=6.2):
    """Chèn hình ảnh sơ đồ kèm chú thích chuẩn."""
    if os.path.exists(img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(8)
        p_img.paragraph_format.space_after = Pt(2)
        run_img = p_img.add_run()
        run_img.add_picture(img_path, width=Inches(width_inches))
        
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(2)
        p_cap.paragraph_format.space_after = Pt(8)
        run_cap = p_cap.add_run(f"Hình: {caption}")
        run_cap.font.name = "Arial"
        run_cap.font.size = Pt(8.5)
        run_cap.italic = True
        run_cap.font.color.rgb = RGBColor(100, 110, 120)

print("Style helpers initialized successfully!")
