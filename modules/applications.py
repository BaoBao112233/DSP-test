from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.signal import freqz

from .plot_config import COLORS, build_save_path, finalize_figure
from .signal_ops import energy


def design_notch_50hz(fs: float = 44100.0, q: float = 30.0):
    return signal.iirnotch(50.0, q, fs=fs)


def demo_notch(fs: float = 44100.0, show_plots: bool = True, save_dir: str | None = None):
    print("\n" + "=" * 60)
    print("BỔ SUNG: BỘ LỌC NOTCH 50Hz – LOẠI BỎ NHIỄU ĐIỆN LƯỚI")
    print("=" * 60)

    duration = 0.5
    time = np.linspace(0, duration, int(fs * duration), endpoint=False)
    rng = np.random.default_rng(42)
    clean = np.sin(2 * np.pi * 440 * time)
    hum = 0.6 * np.sin(2 * np.pi * 50 * time)
    noisy = clean + hum + 0.05 * rng.standard_normal(len(time))

    b_notch, a_notch = design_notch_50hz(fs)
    filtered = signal.lfilter(b_notch, a_notch, noisy)

    snr_before = 10 * np.log10(energy(clean) / energy(noisy - clean))
    snr_after = 10 * np.log10(energy(clean) / energy(filtered - clean))
    print(f"  SNR trước lọc : {snr_before:.2f} dB")
    print(f"  SNR sau lọc   : {snr_after:.2f} dB")

    w, response = freqz(b_notch, a_notch, worN=8192, fs=fs)
    sample_count = min(2000, len(time))

    fig, axes = plt.subplots(2, 2, figsize=(13, 8), tight_layout=True)
    fig.suptitle("Bổ sung – Bộ lọc Notch 50Hz", fontsize=13, color=COLORS[4])

    axes[0, 0].plot(time[:sample_count] * 1e3, noisy[:sample_count], color=COLORS[2], linewidth=0.8)
    axes[0, 0].set_title("Tín hiệu nhiễu (440Hz + 50Hz)")
    axes[0, 0].set_xlabel("Thời gian (ms)")
    axes[0, 0].set_ylabel("Biên độ")
    axes[0, 0].grid(True)

    axes[0, 1].plot(time[:sample_count] * 1e3, filtered[:sample_count], color=COLORS[1], linewidth=0.8)
    axes[0, 1].set_title("Tín hiệu sau lọc Notch")
    axes[0, 1].set_xlabel("Thời gian (ms)")
    axes[0, 1].set_ylabel("Biên độ")
    axes[0, 1].grid(True)

    freq_axis = np.fft.rfftfreq(len(time), 1 / fs)
    axes[1, 0].plot(freq_axis, np.abs(np.fft.rfft(noisy)), color=COLORS[2], linewidth=0.8, label="Trước")
    axes[1, 0].plot(freq_axis, np.abs(np.fft.rfft(filtered)), color=COLORS[1], linewidth=0.8, label="Sau")
    axes[1, 0].set_xlim(0, 600)
    axes[1, 0].set_title("Phổ biên độ (0–600 Hz)")
    axes[1, 0].set_xlabel("Tần số (Hz)")
    axes[1, 0].set_ylabel("|FFT|")
    axes[1, 0].legend(facecolor="#2a2a3e")
    axes[1, 0].grid(True)

    axes[1, 1].plot(w, 20 * np.log10(np.abs(response) + 1e-12), color=COLORS[4])
    axes[1, 1].set_xlim(0, 500)
    axes[1, 1].set_ylim(-60, 5)
    axes[1, 1].axvline(50, color=COLORS[2], linestyle="--", label="50 Hz")
    axes[1, 1].set_title("Đáp ứng biên độ Notch Filter")
    axes[1, 1].set_xlabel("Tần số (Hz)")
    axes[1, 1].set_ylabel("Biên độ (dB)")
    axes[1, 1].legend(facecolor="#2a2a3e")
    axes[1, 1].grid(True)

    finalize_figure(
        fig,
        show_plots,
        save_path=build_save_path(save_dir, "08_notch_50hz.png"),
    )
    return {"b": b_notch, "a": a_notch, "snr_before": snr_before, "snr_after": snr_after}


def simulate_echo(x: np.ndarray, fs: float, delay_ms: float = 200.0, decay: float = 0.5) -> np.ndarray:
    delay_samples = int(delay_ms * fs / 1000)
    padded = np.zeros(delay_samples)
    delayed = np.concatenate([padded, x[:-delay_samples]])
    return x + decay * delayed


def demo_echo(fs: float = 8000.0, show_plots: bool = True, save_dir: str | None = None):
    print("\n" + "=" * 60)
    print("BỔ SUNG: MÔ PHỎNG ECHO – LAB-VOLT TMS320C50 ex1_1")
    print("=" * 60)

    duration = 1.0
    time = np.linspace(0, duration, int(fs * duration), endpoint=False)
    x = np.zeros(len(time))
    x[100:200] = np.hanning(100)
    x[400:600] = 0.7 * np.hanning(200)

    delays = [(100, COLORS[0]), (200, COLORS[1]), (400, COLORS[3])]
    for delay_ms, _ in delays:
        print(f"  delay={delay_ms}ms: D = {int(delay_ms * fs / 1000)} mẫu")

    fig, axes = plt.subplots(3, 1, figsize=(11, 8), tight_layout=True)
    fig.suptitle("Bổ sung – Mô phỏng Echo (Lab-Volt TMS320C50)", fontsize=13, color=COLORS[4])

    axes[0].plot(time, x, color=COLORS[5], linewidth=0.9)
    axes[0].set_title("Tín hiệu gốc x(n)")
    axes[0].set_ylabel("Biên độ")
    axes[0].grid(True)

    for index, (delay_ms, color) in enumerate([(100, COLORS[0]), (400, COLORS[3])], start=1):
        y = simulate_echo(x, fs, delay_ms=delay_ms)
        axes[index].plot(time, y, color=color, linewidth=0.9)
        axes[index].set_title(f"Echo với delay = {delay_ms} ms (D={int(delay_ms * fs / 1000)} mẫu)")
        axes[index].set_ylabel("Biên độ")
        axes[index].grid(True)

    axes[-1].set_xlabel("Thời gian (giây)")
    finalize_figure(
        fig,
        show_plots,
        save_path=build_save_path(save_dir, "09_echo_demo.png"),
    )
    return {"x": x, "time": time}
