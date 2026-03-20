from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import freqz, group_delay

from .plot_config import COLORS, build_save_path, finalize_figure


def compare_fir_iir(
    h_fir: np.ndarray,
    b_iir: np.ndarray,
    a_iir: np.ndarray,
    fs: float = 44100.0,
    show_plots: bool = True,
    save_dir: str | None = None,
):
    print("\n" + "=" * 60)
    print("CHƯƠNG 7: SO SÁNH FIR (Parks-McClellan) vs IIR (Chebyshev)")
    print("=" * 60)
    print(f"  Số hệ số FIR : {len(h_fir)}")
    print(f"  Số hệ số IIR : b={len(b_iir)}, a={len(a_iir)}")
    print("  FIR pha tuyến tính   : ✔")
    print("  IIR pha phi tuyến    : ✔ (xem đồ thị Group Delay)")

    w_fir, response_fir = freqz(h_fir, worN=8192, fs=fs)
    w_iir, response_iir = freqz(b_iir, a_iir, worN=8192, fs=fs)
    w_gd_fir, gd_fir = group_delay((h_fir, [1.0]), w=8192, fs=fs)
    w_gd_iir, gd_iir = group_delay((b_iir, a_iir), w=8192, fs=fs)

    fig, axes = plt.subplots(1, 2, figsize=(13, 5), tight_layout=True)
    fig.suptitle("Chương 7 – So sánh FIR vs IIR", fontsize=13, color=COLORS[4])

    axes[0].plot(w_fir / 1e3, 20 * np.log10(np.abs(response_fir) + 1e-12), color=COLORS[0], label=f"FIR Parks-McClellan ({len(h_fir)} hệ số)")
    axes[0].plot(w_iir / 1e3, 20 * np.log10(np.abs(response_iir) + 1e-12), color=COLORS[2], label=f"IIR Chebyshev ({len(b_iir)} hệ số)")
    axes[0].set_title("Đáp ứng biên độ")
    axes[0].set_xlabel("Tần số (kHz)")
    axes[0].set_ylabel("Biên độ (dB)")
    axes[0].set_ylim(-80, 5)
    axes[0].legend(facecolor="#2a2a3e")
    axes[0].grid(True)

    upper = max(gd_fir.max(), min(gd_iir.max(), gd_fir.max() * 5)) * 1.1
    axes[1].plot(w_gd_fir / 1e3, gd_fir, color=COLORS[0], label="FIR (pha tuyến tính → hằng số)")
    axes[1].plot(w_gd_iir / 1e3, gd_iir, color=COLORS[2], label="IIR (pha phi tuyến → biến đổi)")
    axes[1].set_title("Group Delay (Trễ nhóm)")
    axes[1].set_xlabel("Tần số (kHz)")
    axes[1].set_ylabel("Mẫu (samples)")
    axes[1].set_ylim(0, upper)
    axes[1].legend(facecolor="#2a2a3e")
    axes[1].grid(True)

    finalize_figure(
        fig,
        show_plots,
        save_path=build_save_path(save_dir, "07_fir_vs_iir_compare.png"),
    )
    return {"gd_fir_max": float(gd_fir.max()), "gd_iir_max": float(gd_iir.max())}
