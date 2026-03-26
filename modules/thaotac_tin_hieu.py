"""
thaotac_tin_hieu.py – Các phép toán cơ bản trên tín hiệu rời rạc
(Tương ương Chương 1 trong giáo trình DSP / MATLAB).

Bao gồm:
  - dịch tín hiệu (time shift)
  - gấp tín hiệu (time reversal)
  - cộng hai tín hiệu có trục thời gian khác nhau
  - tính năng lượng tín hiệu
  - demo minh họa với biểu đồ stem
"""

from __future__ import annotations  # Hỗ trợ type hint mới trên Python cũ

import numpy as np                   # Thư viện tính toán số mảng
import matplotlib.pyplot as plt      # Thư viện vẽ biểu đồ

# Import các tiện ích đồ thị từ module cấu hình dùng chung
from .cau_hinh_do_thi import COLORS, tao_duong_dan_luu, hoan_thien_bieu_do


def dich_tin_hieu(x: np.ndarray, n: np.ndarray, d: int):
    """
    Dịch tín hiệu x[n] sang phải d mẫu: y[n] = x[n - d].

    Tham số:
        x: Mảng giá trị tín hiệu (biên độ).
        n: Mảng chỉ số thời gian tương ứng với x.
        d: Số mẫu cần dịch (dương = dịch phải, âm = dịch trái).

    Trả về:
        (x_copy, n_new): bản sao giá trị gốc và trục thời gian đã dịch.
    Note: giá trị x không thay đổi, chỉ dịch trục n.
    """
    return x.copy(), n + d  # Copy x tránh sửa mảng gốc; n + d dịch toàn bộ trục


def gap_tin_hieu(x: np.ndarray, n: np.ndarray):
    """
    Gấp (lật ngược) tín hiệu: y[n] = x[-n].

    Tham số:
        x: Mảng giá trị tín hiệu.
        n: Mảng chỉ số thời gian.

    Trả về:
        (x_flipped, n_flipped): giá trị và trục đều được lật ngược.
    """
    return x[::-1].copy(), -n[::-1].copy()
    # x[::-1]   : đảo chiều mảng giá trị
    # -n[::-1]  : đảo chiều mảng chỉ số rồi đổi dấu (phép gấp quanh n=0)


def cong_hai_tin_hieu(x1: np.ndarray, n1: np.ndarray, x2: np.ndarray, n2: np.ndarray):
    """
    Cộng hai dãy tín hiệu có trục thời gian khác nhau.

    Vấn đề: n1 và n2 có thể không cùng phạm vi, nên không thể cộng trực tiếp.
    Giải pháp: mở rộng cả hai thành dãy dài hơn, zero-pad phần còn thiếu.

    Tham số:
        x1, n1: Dãy thứ nhất và trục chỉ số tương ứng.
        x2, n2: Dãy thứ hai và trục chỉ số tương ứng.

    Trả về:
        (y, n_out): Tổng của hai dãy trên trục chung.
    """
    # Xác định phạm vi chỉ số chung bao gồm cả hai dãy
    n_start = min(n1[0], n2[0])   # Chỉ số bắt đầu nhỏ nhất
    n_stop  = max(n1[-1], n2[-1]) # Chỉ số kết thúc lớn nhất
    n_out   = np.arange(n_start, n_stop + 1)  # Trục chung liên tục

    # Khởi tạo hai dãy zero có độ dài bằng trục chung
    y1 = np.zeros(len(n_out))
    y2 = np.zeros(len(n_out))

    # Đặt giá trị từ dãy gốc vào vị trí chính xác trên trục chung
    # offset = n1[0] - n_start: số phần tử zero-pad ở đầu dãy y1
    y1[n1[0] - n_start : n1[-1] - n_start + 1] = x1
    y2[n2[0] - n_start : n2[-1] - n_start + 1] = x2

    return y1 + y2, n_out  # Cộng cùng vị trí trên trục chung


def nang_luong(x: np.ndarray) -> float:
    """
    Tính năng lượng của tín hiệu rời rạc: E = sum(|x[n]|^2).

    Công thức này áp dụng cho cả tín hiệu thực và phức.
    Với tín hiệu thực: |x|^2 = x^2.
    """
    return float(np.sum(np.abs(x) ** 2))
    # np.abs(x): trị tuyệt đối (hỗ trợ số phức)
    # ** 2    : bình phương
    # np.sum  : tổng tất cả phần tử
    # float() : chuyển numpy scalar về float thuần Python


def demo_thaotac_tin_hieu(show_plots: bool = True, save_dir: str | None = None):
    """
    Demo Chương 1: minh họa các phép toán trên tín hiệu rời rạc.

    Tạo tín hiệu mẫu hình tam giác, rồi thực hiện:
      1. Dịch phải 3 mẫu
      2. Gấp quanh n=0
      3. Cộng tín hiệu gốc với tín hiệu gấp
    Vẽ 3 biểu đồ stem song song để so sánh trực quan.
    Lưu 03_signal_ops_discrete.png nếu có save_dir.
    """
    # --- Tạo tín hiệu mẫu ---
    n = np.arange(-5, 6)  # Chỉ số n từ -5 đến 5 (11 mẫu)
    # Tín hiệu x[n]: xung hình tam giác cân qua n=0
    x = np.array([0, 0, 0, 1, 2, 3, 2, 1, 0, 0, 0], dtype=float)

    # --- Thực hiện các phép toán ---
    _, n_shifted = dich_tin_hieu(x, n, 3)       # Dịch phải 3 mẫu
    x_folded, n_folded = gap_tin_hieu(x, n)     # Gấp: x(-n)
    x_added, n_added = cong_hai_tin_hieu(       # Cộng: x(n) + x(-n)
        x, n, x_folded, n_folded
    )

    # --- In kết quả ra console ---
    print("=" * 60)
    print("CHƯƠNG 1: THAO TÁC TÍN HIỆU RỜI RẠC")
    print("=" * 60)
    print(f"  Năng lượng x(n)  : E = {nang_luong(x):.2f}")
    print(f"  Sau dịch  d=3    : n_shift = {n_shifted}")
    print(f"  Sau gấp          : n_fold  = {n_folded}")

    # --- Vẽ 3 biểu đồ stem thể hiện tín hiệu rời rạc ---
    fig, axes = plt.subplots(3, 1, figsize=(10, 7), tight_layout=True)
    fig.suptitle("Chương 1 – Thao tác tín hiệu rời rạc", fontsize=13, color=COLORS[4])

    # Dữ liệu cho 3 subplot: (giá trị, chỉ số, tiêu đề, màu)
    for ax, data in zip(
        axes,
        [
            (x,       n,        "x(n) – Tín hiệu gốc",          COLORS[0]),
            (x,       n_shifted,"x(n-3) – Dịch phải 3 mẫu",    COLORS[1]),
            (x_added, n_added,  "x(n)+x(-n) – Cộng dãy gấp",    COLORS[3]),
        ],
    ):
        samples, index, title, color = data
        # stem: vẽ tín hiệu rời rạc bằng các cột đứng (khác plot liên tục)
        ax.stem(index, samples, linefmt=color, markerfmt="o", basefmt="white")
        ax.set_title(title)
        ax.set_xlabel("n")
        ax.set_ylabel("Biên độ")
        ax.grid(True)

    # Lưu và hiển thị
    hoan_thien_bieu_do(
        fig,
        show_plots,
        save_path=tao_duong_dan_luu(save_dir, "03_signal_ops_discrete.png"),
    )
    # Trả về dict để chay_demo.py có thể tiếp tục sử dụng nếu cần
    return {"x": x, "n": n, "x_added": x_added, "n_added": n_added}
