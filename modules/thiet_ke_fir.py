from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from scipy.signal import firwin, freqz, remez

from .cau_hinh_do_thi import COLORS, build_save_path, finalize_figure


def design_fir_hamming(wp_rad: float, ws_rad: float) -> np.ndarray:
    delta_w = ws_rad - wp_rad
    order = int(np.ceil(6.6 * np.pi / delta_w))
    if order % 2 != 0:
        order += 1
    cutoff = (wp_rad + ws_rad) / 2
    coefficients = firwin(order + 1, cutoff / np.pi, window="hamming")
    print(f"  [Hamming] Bậc M = {order},  ωc = {cutoff / np.pi:.4f}π  ({len(coefficients)} hệ số)")
    return coefficients


def design_fir_pm(wp_rad: float, ws_rad: float, delta1_db: float = 0.5, delta2_db: float = 40.0) -> np.ndarray:
    delta1 = (10 ** (delta1_db / 20) - 1) / (10 ** (delta1_db / 20) + 1)
    delta2 = 10 ** (-delta2_db / 20)
    delta = min(delta1, delta2)
    transition = ws_rad - wp_rad
    d_value = (-20 * np.log10(delta) - 13) / 14.6
    order = int(np.ceil(d_value / transition * np.pi))
    if order % 2 != 0:
        order += 1

    bands = [0, wp_rad / np.pi, ws_rad / np.pi, 1.0]
    desired = [1, 0]
    weight = [delta2 / delta1, 1]
    coefficients = remez(order + 1, bands, desired, weight=weight, fs=2.0)
    print(f"  [P-McClellan] Bậc M = {order},  {len(coefficients)} hệ số")
    return coefficients


def plot_fir_response(
    h_hamming: np.ndarray,
    h_pm: np.ndarray,
    fs: float = 44100.0,
    show_plots: bool = True,
    save_path: str | None = None,
):
    fig = plt.figure(figsize=(13, 10), tight_layout=True)
    fig.suptitle("Chương 3 – Bộ lọc FIR: Hamming vs Parks-McClellan", fontsize=13, color=COLORS[4])
    grid = gridspec.GridSpec(2, 2)

    for index, (coefficients, label, color) in enumerate([
        (h_hamming, "Hamming", COLORS[0]),
        (h_pm, "Parks-McClellan", COLORS[1]),
    ]):
        w, response = freqz(coefficients, worN=4096, fs=fs)

        ax_mag = fig.add_subplot(grid[0, index])
        ax_mag.plot(w / 1e3, 20 * np.log10(np.abs(response) + 1e-12), color=color)
        ax_mag.set_title(f"Magnitude – {label}")
        ax_mag.set_xlabel("Tần số (kHz)")
        ax_mag.set_ylabel("Biên độ (dB)")
        ax_mag.set_ylim(-80, 5)
        ax_mag.axhline(-40, color=COLORS[2], linestyle="--", linewidth=1, label="−40 dB")
        ax_mag.legend(facecolor="#2a2a3e")
        ax_mag.grid(True)

        ax_phase = fig.add_subplot(grid[1, index])
        ax_phase.plot(w / 1e3, np.unwrap(np.angle(response)) * 180 / np.pi, color=color)
        ax_phase.set_title(f"Pha – {label}")
        ax_phase.set_xlabel("Tần số (kHz)")
        ax_phase.set_ylabel("Góc pha (độ)")
        ax_phase.grid(True)

    finalize_figure(fig, show_plots, save_path=save_path)


def demo_fir(fs: float = 44100.0, show_plots: bool = True, save_dir: str | None = None):
    print("\n" + "=" * 60)
    print("CHƯƠNG 3: THIẾT KẾ BỘ LỌC FIR")
    print("=" * 60)
    wp = 0.2 * np.pi
    ws = 0.3 * np.pi

    fp = wp * fs / (2 * np.pi)
    fs_edge = ws * fs / (2 * np.pi)
    print(f"  Fs = {fs} Hz,  fp = {fp:.1f} Hz,  fs_edge = {fs_edge:.1f} Hz")

    h_hamming = design_fir_hamming(wp, ws)
    h_pm = design_fir_pm(wp, ws)
    print("  Pha tuyến tính (Hamming) : ✔  (FIR với h đối xứng – Type 1)")
    plot_fir_response(
        h_hamming,
        h_pm,
        fs=fs,
        show_plots=show_plots,
        save_path=build_save_path(save_dir, "05_fir_hamming_vs_pm.png"),
    )
    return {"h_hamming": h_hamming, "h_pm": h_pm, "wp": wp, "ws": ws, "fs": fs}
