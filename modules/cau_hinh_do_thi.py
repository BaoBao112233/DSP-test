"""
cau_hinh_do_thi.py – Cấu hình chung cho toàn bộ biểu đồ trong dự án.

Module này không phụ thuộc vào module nào khác trong package –
đây là module nền mà tất cả module khác import từ đây.
Dự án sử dụng theme tối Catppuccin Mocha để biểu đồ trông chuyên nghiệp.
"""

from __future__ import annotations  # Hỗ trợ type hint mới trên Python cũ

from pathlib import Path  # Thư viện xử lý đường dẫn file theo kiểu hướng đối tượng

import matplotlib.pyplot as plt  # Thư viện vẽ biểu đồ chính của dự án

# ---------------------------------------------------------------------------
# Bảng màu Catppuccin Mocha – 6 màu sáng dùng trên nền tối
# Thứ tự: Xanh lam, Xanh lá, Đỏ, Cam, Tím, Cyan
# ---------------------------------------------------------------------------
COLORS = ["#89b4fa", "#a6e3a1", "#f38ba8", "#fab387", "#cba6f7", "#89dceb"]


def ap_dung_style_do_thi() -> None:
    """
    Áp dụng theme tối Catppuccin Mocha lên toàn bộ biểu đồ Matplotlib.

    Hàm này cần được gọi đúng MỘT LẦN trước khi vẽ bất kỳ biểu đồ nào.
    Nó thay đổi rcParams toàn cục nên áp dụng cho mọi figure sau đó.
    """
    plt.rcParams.update({
        "figure.facecolor": "#1e1e2e",   # Màu nền ngoài cùng của figure
        "axes.facecolor":   "#2a2a3e",   # Màu nền vùng vẽ đồ thị (axes)
        "axes.edgecolor":   "#cdd6f4",   # Màu viền khung axes
        "axes.labelcolor":  "#cdd6f4",   # Màu chữ nhãn trục X/Y
        "xtick.color":      "#cdd6f4",   # Màu vạch gạch và chữ số trục X
        "ytick.color":      "#cdd6f4",   # Màu vạch gạch và chữ số trục Y
        "text.color":       "#cdd6f4",   # Màu mặc định cho tất cả văn bản
        "grid.color":       "#45475a",   # Màu lưới nền (grid)
        "grid.linestyle":   "--",         # Kiểu nét lưới: nét đứt
        "grid.alpha":       0.5,          # Độ trong suốt lưới (50%)
        "lines.linewidth":  1.8,          # Độ dày đường mặc định
        "font.size":        10,           # Cỡ chữ mặc định (points)
    })


def tao_duong_dan_luu(save_dir: str | None, filename: str) -> str | None:
    """
    Tạo đường dẫn đầy đủ để lưu file ảnh biểu đồ.

    Tham số:
        save_dir: Thư mục gốc để lưu. Nếu là None thì không lưu.
        filename: Tên file PNG (ví dụ: '01_sampling_time_domain.png').

    Trả về:
        str: Đường dẫn đầy đủ tới file PNG sẽ lưu.
        None: Nếu save_dir không được cung cấp.
    """
    if not save_dir:  # Nếu người dùng không chỉ định thư mục – bỏ qua việc lưu
        return None
    output_dir = Path(save_dir)              # Đổi chuỗi thành đối tượng Path
    output_dir.mkdir(parents=True, exist_ok=True)  # Tự tạo thư mục nếu chưa có
    return str(output_dir / filename)        # Nối thư mục + tên file thành chuỗi


def hoan_thien_bieu_do(fig, show_plots: bool, save_path: str | None = None) -> None:
    """
    Hoàn thiện biểu đồ: lưu ra file (nếu có) và hiển thị hoặc đóng.

    Tham số:
        fig:        Đối tượng Figure của Matplotlib cần xử lý.
        show_plots: True = mở cửa sổ đồ thị; False = đóng và giải phóng bộ nhớ.
        save_path:  Đường dẫn để lưu file PNG, hoặc None nếu không lưu.
    """
    if save_path:  # Chỉ lưu khi có đường dẫn hợp lệ
        # Dùng dpi=220 để ảnh đủ sắc nét khi in / nhúng vào báo cáo
        # bbox_inches='tight' cắt lề trắng dư xung quanh figure
        fig.savefig(save_path, dpi=220, bbox_inches="tight")
    if show_plots:  # Hiển thị giao diện đồ thị tương tác
        plt.show()
    else:           # Không hiển thị – giải phóng bộ nhớ tránh rò rỉ
        plt.close(fig)
