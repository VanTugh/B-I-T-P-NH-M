import os
os.environ['MPLCONFIGDIR'] = os.path.join(os.environ.get('TEMP', '.'), 'matplotlib_tmp')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def create_all_diagrams():
    # 1. Architecture Diagram
    fig, ax = plt.subplots(figsize=(8.5, 4.8), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis('off')
    rect1 = patches.FancyBboxPatch((0.5, 4.3), 9, 1.3, boxstyle='round,pad=0.2', facecolor='#E8EEF5', edgecolor='#1B365D', linewidth=2)
    ax.add_patch(rect1)
    ax.text(5, 5.2, 'TẦNG GIAO DIỆN (PRESENTATION LAYER)', ha='center', va='center', fontsize=11, fontweight='bold', color='#1B365D')
    ax.text(5, 4.65, 'main.py  |  ui.py (Tkinter GUI: 12 nút 3x4, Ô nhập liệu SV, Cụm nút thao tác, Bộ đếm x/12)', ha='center', va='center', fontsize=9.5, color='#333333')

    ax.annotate('', xy=(5, 3.8), xytext=(5, 4.2), arrowprops=dict(facecolor='#1B365D', edgecolor='#1B365D', width=2, headwidth=8))

    rect2 = patches.FancyBboxPatch((0.5, 2.3), 9, 1.5, boxstyle='round,pad=0.2', facecolor='#D9E2EC', edgecolor='#2E75B6', linewidth=2)
    ax.add_patch(rect2)
    ax.text(5, 3.45, 'TẦNG NGHIỆP VỤ (BUSINESS LOGIC LAYER / SERVICES)', ha='center', va='center', fontsize=11, fontweight='bold', color='#1B365D')
    ax.text(2.0, 2.75, 'seat_service.py\n(assign_seat, release_seat\nKiểm tra logic & DB)', ha='center', va='center', fontsize=9, bbox=dict(boxstyle='square,pad=0.4', facecolor='#FFFFFF', edgecolor='#2E75B6'))
    ax.text(5.0, 2.75, 'student_service.py\n(find_student\nJOIN phân loại trạng thái)', ha='center', va='center', fontsize=9, bbox=dict(boxstyle='square,pad=0.4', facecolor='#FFFFFF', edgecolor='#2E75B6'))
    ax.text(8.0, 2.75, 'statistics.py\n(get_seat_stats, get_seat_map\nBộ đếm & Ma trận 12 vị trí)', ha='center', va='center', fontsize=9, bbox=dict(boxstyle='square,pad=0.4', facecolor='#FFFFFF', edgecolor='#2E75B6'))

    ax.annotate('', xy=(5, 1.7), xytext=(5, 2.2), arrowprops=dict(facecolor='#1B365D', edgecolor='#1B365D', width=2, headwidth=8))

    rect3 = patches.FancyBboxPatch((0.5, 0.3), 9, 1.3, boxstyle='round,pad=0.2', facecolor='#BCCCDC', edgecolor='#1B365D', linewidth=2)
    ax.add_patch(rect3)
    ax.text(5, 1.25, 'TẦNG DỮ LIỆU (DATA ACCESS LAYER)', ha='center', va='center', fontsize=11, fontweight='bold', color='#1B365D')
    ax.text(5, 0.7, 'database.py (get_connection, init_db)  |  phong_may.db (SQLite)  |  tao_du_lieu_demo.py', ha='center', va='center', fontsize=9.5, color='#1B365D', fontweight='semibold')
    plt.tight_layout()
    plt.savefig('diagram_architecture.png', bbox_inches='tight')
    plt.close()

    # 2. Task Flow Diagram
    fig, ax = plt.subplots(figsize=(9.2, 5.8), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7)
    ax.axis('off')

    def draw_box(x, y, w, h, text, subtext, color, border):
        rect = patches.FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.15', facecolor=color, edgecolor=border, linewidth=1.5)
        ax.add_patch(rect)
        ax.text(x + w/2, y + h/2 + 0.12, text, ha='center', va='center', fontsize=9, fontweight='bold', color='#1B365D')
        ax.text(x + w/2, y + h/2 - 0.18, subtext, ha='center', va='center', fontsize=7.5, color='#444444')

    draw_box(0.3, 5.8, 2.6, 0.85, 'TASK-01: Setup Project', 'TV5 & Nhóm (0-15p)', '#E8EEF5', '#1B365D')
    draw_box(3.7, 5.8, 2.6, 0.85, 'TASK-02: SQLite Schema', 'TV4 (15-35p)', '#D9E2EC', '#2E75B6')

    draw_box(0.2, 3.8, 2.1, 0.85, 'TASK-03: Seed Data', 'TV4 (35-50p)', '#E1F5FE', '#0288D1')
    draw_box(2.6, 3.8, 2.2, 0.85, 'TASK-04: Xếp/Trả chỗ', 'TV2 (25-60p)', '#E8F5E9', '#388E3C')
    draw_box(5.1, 3.8, 2.2, 0.85, 'TASK-05: Tra cứu/Stats', 'TV3 (25-60p)', '#FFF3E0', '#F57C00')
    draw_box(7.6, 3.8, 2.1, 0.85, 'TASK-06: Tkinter UI', 'TV1 (15-65p)', '#F3E5F5', '#7B1FA2')

    draw_box(3.7, 2.1, 2.6, 0.85, 'TASK-07: Unit Testing', 'Từng TV & TV5 (55-75p)', '#FFF9C4', '#FBC02D')
    draw_box(0.3, 0.5, 2.6, 0.85, 'TASK-08: Tích hợp Module', 'TV5 chủ trì (75-95p)', '#D1C4E9', '#512DA8')
    draw_box(3.7, 0.5, 2.6, 0.85, 'TASK-09: Test Tích hợp', 'TV5 & Nhóm (95-110p)', '#FFCDD2', '#D32F2F')
    draw_box(7.1, 0.5, 2.6, 0.85, 'TASK-10: Nghiệm thu', 'Cả nhóm (110-120p)', '#C8E6C9', '#388E3C')

    # Arrows
    ax.annotate('', xy=(3.7, 6.22), xytext=(2.9, 6.22), arrowprops=dict(facecolor='#1B365D', width=1.5, headwidth=6))
    for target_x in [1.25, 3.7, 6.2]:
        ax.annotate('', xy=(target_x, 4.65), xytext=(5.0, 5.8), arrowprops=dict(facecolor='#2E75B6', width=1.2, headwidth=5))
    ax.annotate('', xy=(8.65, 4.65), xytext=(1.6, 5.8), arrowprops=dict(facecolor='#7B1FA2', width=1.2, headwidth=5, linestyle='--'))
    for start_x in [1.25, 3.7, 6.2, 8.65]:
        ax.annotate('', xy=(5.0, 2.95), xytext=(start_x, 3.8), arrowprops=dict(facecolor='#444444', width=1.0, headwidth=5))
    ax.annotate('', xy=(1.6, 1.35), xytext=(5.0, 2.1), arrowprops=dict(facecolor='#1B365D', width=1.5, headwidth=6))
    ax.annotate('', xy=(3.7, 0.92), xytext=(2.9, 0.92), arrowprops=dict(facecolor='#1B365D', width=1.5, headwidth=6))
    ax.annotate('', xy=(7.1, 0.92), xytext=(6.3, 0.92), arrowprops=dict(facecolor='#1B365D', width=1.5, headwidth=6))

    plt.tight_layout()
    plt.savefig('diagram_task_flow.png', bbox_inches='tight')
    plt.close()

    # 3. Seat Matrix
    fig, ax = plt.subplots(figsize=(7.8, 4.3), dpi=300)
    ax.set_xlim(0, 9)
    ax.set_ylim(0, 5.5)
    ax.axis('off')
    ax.text(4.5, 5.0, 'SƠ ĐỒ PHÒNG MÁY 12 VỊ TRÍ (3 HÀNG × 4 CỘT)', ha='center', va='center', fontsize=12, fontweight='bold', color='#1B365D')

    seats = [
        [('A1', 'Trống', '#E8EEF5'), ('A2', 'SV100', '#C8E6C9'), ('A3', 'Trống', '#E8EEF5'), ('A4', 'Trống', '#E8EEF5')],
        [('B1', 'Trống', '#E8EEF5'), ('B2', 'Trống', '#E8EEF5'), ('B3', 'Trống', '#E8EEF5'), ('B4', 'Trống', '#E8EEF5')],
        [('C1', 'Trống', '#E8EEF5'), ('C2', 'Trống', '#E8EEF5'), ('C3', 'Trống', '#E8EEF5'), ('C4', 'Trống', '#E8EEF5')]
    ]

    for row_idx, row in enumerate(seats):
        y = 3.6 - row_idx * 1.3
        for col_idx, (code, status, color) in enumerate(row):
            x = 0.8 + col_idx * 1.9
            border = '#388E3C' if status != 'Trống' else '#1B365D'
            box = patches.FancyBboxPatch((x, y), 1.6, 0.95, boxstyle='round,pad=0.1', facecolor=color, edgecolor=border, linewidth=2)
            ax.add_patch(box)
            ax.text(x + 0.8, y + 0.6, code, ha='center', va='center', fontsize=11, fontweight='bold', color='#1B365D')
            ax.text(x + 0.8, y + 0.28, status, ha='center', va='center', fontsize=9, fontweight='semibold', color='#2E75B6' if status == 'Trống' else '#1B5E20')

    ax.text(4.5, 0.3, 'BỘ ĐẾM TRẠNG THÁI: 1 / 12 Chỗ đã sử dụng (Còn trống: 11 chỗ)', ha='center', va='center', fontsize=10, fontweight='bold', color='#D32F2F', bbox=dict(boxstyle='round,pad=0.3', facecolor='#FFF3E0', edgecolor='#FF9800'))
    plt.tight_layout()
    plt.savefig('diagram_seat_matrix.png', bbox_inches='tight')
    plt.close()

    # 4. Git Workflow
    fig, ax = plt.subplots(figsize=(9.2, 4.6), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.axis('off')
    ax.text(5, 4.6, 'MÔ HÌNH NHÁNH GIT FLOW RÚT GỌN (SPRINT 120 PHÚT)', ha='center', va='center', fontsize=11, fontweight='bold', color='#1B365D')

    ax.plot([0.5, 9.5], [3.8, 3.8], color='#1B365D', linewidth=3, label='main')
    ax.text(0.5, 4.05, 'main (Release v1.0)', fontsize=9.5, fontweight='bold', color='#1B365D')
    ax.scatter([1.0, 9.0], [3.8, 3.8], color='#1B365D', s=120, zorder=5)
    ax.text(1.0, 3.45, 'Init', ha='center', fontsize=8)
    ax.text(9.0, 3.45, 'Release v1.0', ha='center', fontsize=8, fontweight='bold', color='#1B365D')

    ax.plot([1.0, 8.5], [2.4, 2.4], color='#2E75B6', linewidth=2.5, linestyle='-', label='develop')
    ax.text(0.5, 2.4, 'develop', fontsize=9.5, fontweight='bold', color='#2E75B6')
    ax.scatter([1.5, 4.0, 6.0, 8.0], [2.4, 2.4, 2.4, 2.4], color='#2E75B6', s=90, zorder=5)

    ax.annotate('', xy=(1.5, 2.4), xytext=(1.0, 3.8), arrowprops=dict(facecolor='#2E75B6', width=1.5, headwidth=6))

    branches = [
        ('feature/database (TV4)', 1.5, 1.8, 3.8, '#0288D1'),
        ('feature/seat-management (TV2)', 1.0, 3.5, 5.8, '#388E3C'),
        ('feature/student-search (TV3)', 0.5, 3.5, 6.2, '#F57C00'),
        ('feature/ui (TV1)', 0.05, 2.0, 7.8, '#7B1FA2'),
    ]

    for name, y_lvl, start_x, end_x, col in branches:
        ax.plot([start_x, end_x], [y_lvl, y_lvl], color=col, linewidth=2, linestyle=':')
        ax.text(start_x + 0.1, y_lvl + 0.15, name, fontsize=7.5, color=col, fontweight='semibold')
        ax.annotate('', xy=(start_x, y_lvl), xytext=(start_x - 0.3, 2.4), arrowprops=dict(facecolor=col, width=1, headwidth=4))
        ax.annotate('', xy=(end_x + 0.2, 2.4), xytext=(end_x, y_lvl), arrowprops=dict(facecolor=col, width=1, headwidth=4))

    ax.annotate('', xy=(9.0, 3.8), xytext=(8.0, 2.4), arrowprops=dict(facecolor='#1B365D', width=2, headwidth=7))

    plt.tight_layout()
    plt.savefig('diagram_git_workflow.png', bbox_inches='tight')
    plt.close()

    # 5. Sequence Flow
    fig, ax = plt.subplots(figsize=(9.2, 4.8), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis('off')
    ax.text(5, 5.6, 'LUỒNG XỬ LÝ HOÀN CHỈNH KHI XẾP CHỖ (END-TO-END SEQUENCE)', ha='center', va='center', fontsize=11, fontweight='bold', color='#1B365D')

    actors = [
        (1.2, 'Người dùng\n(Lớp trưởng)'),
        (3.6, 'Giao diện\n(ui.py)'),
        (6.3, 'Dịch vụ Nghiệp vụ\n(seat_service.py)'),
        (8.9, 'Cơ sở dữ liệu\n(phong_may.db)')
    ]

    for x, label in actors:
        ax.text(x, 5.0, label, ha='center', va='center', fontsize=8.5, fontweight='bold', bbox=dict(boxstyle='round,pad=0.3', facecolor='#E8EEF5', edgecolor='#1B365D'))
        ax.plot([x, x], [0.4, 4.5], color='#B0BEC5', linestyle='--', linewidth=1.5)

    steps = [
        (1.2, 3.6, 4.1, '1. Chọn A2, nhập "SV100", bấm [Xếp chỗ]', '#1B365D'),
        (3.6, 6.3, 3.4, '2. Gọi assign_seat("A2", "SV100")', '#2E75B6'),
        (6.3, 8.9, 2.7, '3. Kiểm tra logic & INSERT xep_cho', '#00796B'),
        (8.9, 6.3, 2.0, '4. Commit thành công (Trả True, "Thành công")', '#388E3C'),
        (6.3, 3.6, 1.4, '5. Trả kết quả (True, Thông báo)', '#2E75B6'),
        (3.6, 1.2, 0.7, '6. Cập nhật A2="SV100", Bộ đếm 1/12, Báo thành công', '#D32F2F')
    ]

    for x_from, x_to, y, text, col in steps:
        ax.annotate('', xy=(x_to, y), xytext=(x_from, y), arrowprops=dict(facecolor=col, edgecolor=col, width=1.5, headwidth=6))
        mid_x = (x_from + x_to) / 2
        ax.text(mid_x, y + 0.16, text, ha='center', va='center', fontsize=7.5, fontweight='semibold', color=col)

    plt.tight_layout()
    plt.savefig('diagram_sequence_flow.png', bbox_inches='tight')
    plt.close()

    print('All 5 diagrams created successfully!')

if __name__ == '__main__':
    create_all_diagrams()
