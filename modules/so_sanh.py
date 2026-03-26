"""
so_sanh.py – So sánh trực quan bộ lọc FIR và IIR trên cùng một biểu đồ.

Mục đích: giúp người đọc thấy rõ sự đánh đổi giữa FIR và IIR:
  - FIR: pha tuyến tính → group delay phẳng (hằng số)
  - IIR: bậc thấp hơn nhưng pha phi tuyến → group delay biến đổi theo tần số
"""

from __future__ import annotations  # Hỗ trợ type hint mới trên Python cũ

import numpy as np             # Tính toán số mảng
import matplotlib.pyplot as plt   # Vẽ biểu đồ
from scipy.signal import freqz, group_delay
# freqz      : tính đáp ứng tần số H(e^{jω})
# group_delay: τ(ω) = -dφ/dω (trễ nhóm theo tần số)

# Import tiện ích đồ thị
from .cau_hinh_do_thi import COLORS, tao_duong_dan_luu, hoan_thien_bieu_do


def so_sanh_fir_iir(
    h_fir: np.ndarray,
    b_iir: np.ndarray,
    a_iir: np.ndarray,
    fs: float = 44100.0,
    show_plots: bool = True,
    save_dir: str | None = None,
):
    """
    So sánh đáp ứng biên độ và group delay của FIR vs IIR.

    Tham số:
        h_fir:           Hệ số bộ lọc FIR (mảng 1-D, a = [1]).
        b_iir, a_iir:   Hệ số tử/mẫu của bộ lọc IIR.
        fs:              Tần số lấy mẫu (Hz).
        show_plots, save_dir: Xem hoan_thien_bieu_do().
    """
    print("\n" + "=" * 60)
    print("CHƯƠNG 7: SO SÁNH FIR (Parks-McClellan) vs IIR (Chebyshev)")
    print("=" * 60)
    print(f"  Số hệ số FIR : {len(h_fir)}")
    print(f"  Số hệ số IIR : b={len(b_iir)}, a={len(a_iir)}")
    print("  FIR pha tuyến tính   : ✔")
    print("  IIR pha phi tuyến    : ✔ (xem đồ thị Group Delay)")

    # Tính đáp ứng tần số với 8192 điểm để đường cong mượt
    w_fir, response_fir = freqz(h_fir,      worN=8192, fs=fs)
    w_iir, response_iir = freqz(b_iir, a_iir, worN=8192, fs=fs)

    # Group delay của FIR: [1.0] là a-coefficient của FIR (IIR thuần túy = not IIR)
    w_gd_fir, gd_fir = group_delay((h_fir,  [1.0]),     w=8192, fs=fs)
    w_gd_iir, gd_iir = group_delay((b_iir, a_iir),       w=8192, fs=fs)

    fig, axes = plt.subplots(1, 2, figsize=(13, 5), tight_layout=True)
    fig.suptitle("Chương 7 – So sánh FIR vs IIR", fontsize=13, color=COLORS[4])

    # Subplot trái: biên độ dB – cả hai nên có đặc tả giống nhau
    axes[0].plot(w_fir / 1e3, 20 * np.log10(np.abs(response_fir) + 1e-12),
                 color=COLORS[0], label=f"FIR Parks-McClellan ({len(h_fir)} hệ số)")
    axes[0].plot(w_iir / 1e3, 20 * np.log10(np.abs(response_iir) + 1e-12),
                 color=COLORS[2], label=f"IIR Chebyshev ({len(b_iir)} hệ số)")
    axes[0].set_title("Đáp ứng biên độ")
    axes[0].set_xlabel("Tần số (kHz)")
    axes[0].set_ylabel("Biên độ (dB)")
    axes[0].set_ylim(-80, 5)
    axes[0].legend(facecolor="#2a2a3e")
    axes[0].grid(True)

    # Subplot phải: group delay – FIR nằm ngang, IIR biến đổi
    # Giới hạn trục Y để IIR outlier không che khuất FIR
    upper = max(gd_fir.max(), min(gd_iir.max(), gd_fir.max() * 5)) * 1.1
    axes[1].plot(w_gd_fir / 1e3, gd_fir, color=COLORS[0], label="FIR (pha tuyến tính → hằng số)")
    axes[1].plot(w_gd_iir / 1e3, gd_iir, color=COLORS[2], label="IIR (pha phi tuyến → biến đổi)")
    axes[1].set_title("Group Delay (Trễ nhóm)")
    axes[1].set_xlabel("Tần số (kHz)")
    axes[1].set_ylabel("Mẫu (samples)")
    axes[1].set_ylim(0, upper)
    axes[1].legend(facecolor="#2a2a3e")
    axes[1].grid(True)

    hoan_thien_bieu_do(
        fig,
        show_plots,
        save_path=tao_duong_dan_luu(save_dir, "07_fir_vs_iir_compare.png"),
    )
    return {"gd_fir_max": float(gd_fir.max()), "gd_iir_max": float(gd_iir.max())}
