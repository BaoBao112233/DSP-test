from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.signal import cheby1, freqz, group_delay

from .cau_hinh_do_thi import COLORS, tao_duong_dan_luu, hoan_thien_bieu_do


def thiet_ke_iir_bilinear(wp_rad: float, ws_rad: float, rp_db: float, rs_db: float, fs: float):
    sampling_period = 1.0 / fs
    omega_p = (2 / sampling_period) * np.tan(wp_rad / 2)
    omega_s = (2 / sampling_period) * np.tan(ws_rad / 2)
    print(f"  Pre-warp: ΩP = {omega_p:.2f} rad/s,  ΩS = {omega_s:.2f} rad/s")

    order, critical = signal.cheb1ord(wp_rad / np.pi, ws_rad / np.pi, rp_db, rs_db)
    print(f"  Bậc Chebyshev Type I : N = {order}")
    b, a = cheby1(order, rp_db, critical, btype="low")
    return b, a, order, omega_p, omega_s


def ve_dap_ung_iir(
    b: np.ndarray,
    a: np.ndarray,
    fs: float = 44100.0,
    title: str = "IIR – Chebyshev Type I",
    show_plots: bool = True,
    save_path: str | None = None,
):
    w, response = freqz(b, a, worN=8192, fs=fs)
    w_gd, gd = group_delay((b, a), w=8192, fs=fs)

    fig, axes = plt.subplots(2, 2, figsize=(13, 9), tight_layout=True)
    fig.suptitle(f"Chương 4 – {title}", fontsize=13, color=COLORS[4])

    axes[0, 0].plot(w / 1e3, 20 * np.log10(np.abs(response) + 1e-12), color=COLORS[0])
    axes[0, 0].set_title("Đáp ứng biên độ")
    axes[0, 0].set_xlabel("Tần số (kHz)")
    axes[0, 0].set_ylabel("Biên độ (dB)")
    axes[0, 0].set_ylim(-80, 5)
    axes[0, 0].axhline(-3, color=COLORS[2], linestyle="--", label="−3 dB")
    axes[0, 0].legend(facecolor="#2a2a3e")
    axes[0, 0].grid(True)

    axes[0, 1].plot(w / 1e3, np.unwrap(np.angle(response)) * 180 / np.pi, color=COLORS[1])
    axes[0, 1].set_title("Đáp ứng pha")
    axes[0, 1].set_xlabel("Tần số (kHz)")
    axes[0, 1].set_ylabel("Pha (độ)")
    axes[0, 1].grid(True)

    axes[1, 0].plot(w_gd / 1e3, gd, color=COLORS[3])
    axes[1, 0].set_title("Group Delay (Trễ nhóm)")
    axes[1, 0].set_xlabel("Tần số (kHz)")
    axes[1, 0].set_ylabel("Mẫu (samples)")
    axes[1, 0].set_ylim(0, None)
    axes[1, 0].grid(True)

    zeros_z = np.roots(b)
    poles_z = np.roots(a)
    theta = np.linspace(0, 2 * np.pi, 360)
    axes[1, 1].plot(np.cos(theta), np.sin(theta), color="#6c7086", linewidth=1)
    axes[1, 1].axhline(0, color="#6c7086", linewidth=0.5)
    axes[1, 1].axvline(0, color="#6c7086", linewidth=0.5)
    axes[1, 1].scatter(zeros_z.real, zeros_z.imag, marker="o", s=80, facecolors="none", edgecolors=COLORS[1], linewidths=2, label="Zeros")
    axes[1, 1].scatter(poles_z.real, poles_z.imag, marker="x", s=80, color=COLORS[2], linewidths=2, label="Poles")
    axes[1, 1].set_xlim(-1.5, 1.5)
    axes[1, 1].set_ylim(-1.5, 1.5)
    axes[1, 1].set_aspect("equal")
    axes[1, 1].set_title("Mặt phẳng Z")
    axes[1, 1].legend(facecolor="#2a2a3e")
    axes[1, 1].grid(True)

    stable = np.all(np.abs(poles_z) < 1.0)
    print(f"  Ổn định: {'✔ CÓ' if stable else '✘ KHÔNG'} (max|pole| = {np.max(np.abs(poles_z)):.4f})")
    hoan_thien_bieu_do(fig, show_plots, save_path=save_path)
    return stable


def demo_bo_loc_iir(fs: float = 44100.0, show_plots: bool = True, save_dir: str | None = None):
    print("\n" + "=" * 60)
    print("CHƯƠNG 4 & 5: THIẾT KẾ BỘ LỌC IIR – BILINEAR CHEBYSHEV TYPE I")
    print("=" * 60)
    wp = 0.2 * np.pi
    ws = 0.3 * np.pi
    rp = 1.0
    rs = 15.0

    b, a, order, omega_p, omega_s = thiet_ke_iir_bilinear(wp, ws, rp, rs, fs)
    print(f"  Hệ số b = {np.round(b, 6)}")
    print(f"  Hệ số a = {np.round(a, 6)}")
    stable = ve_dap_ung_iir(
        b,
        a,
        fs=fs,
        title=f"IIR Chebyshev Type I (N={order}), Fs=44.1kHz",
        show_plots=show_plots,
        save_path=tao_duong_dan_luu(save_dir, "06_iir_response.png"),
    )
    return {"b": b, "a": a, "order": order, "omega_p": omega_p, "omega_s": omega_s, "stable": stable, "wp": wp, "ws": ws, "fs": fs}
