from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt

from .cau_hinh_do_thi import COLORS, build_save_path, finalize_figure


def generate_original_signal(time_axis: np.ndarray) -> np.ndarray:
    """Tạo tín hiệu gốc liên tục giả lập gồm nhiều thành phần sin."""
    return (
        0.8 * np.sin(2 * np.pi * 440 * time_axis)
        + 0.35 * np.sin(2 * np.pi * 1000 * time_axis)
        + 0.2 * np.sin(2 * np.pi * 3000 * time_axis)
    )


def sample_signal(fs: float = 44100.0, duration: float = 0.01):
    """Lấy mẫu đều tín hiệu theo công thức x[n] = x(nTs)."""
    ts = 1.0 / fs
    continuous_fs = fs * 40

    t_cont = np.linspace(0, duration, int(duration * continuous_fs), endpoint=False)
    t_disc = np.arange(0, duration, ts)

    x_cont = generate_original_signal(t_cont)
    x_disc = generate_original_signal(t_disc)

    return {
        "fs": fs,
        "ts": ts,
        "duration": duration,
        "t_cont": t_cont,
        "t_disc": t_disc,
        "x_cont": x_cont,
        "x_disc": x_disc,
        "f_max": 3000.0,
        "continuous_fs": continuous_fs,
    }


def analyze_nyquist(fs: float, f_max: float) -> dict:
    nyquist = fs / 2
    satisfied = fs >= 2 * f_max
    return {
        "fs": fs,
        "f_max": f_max,
        "nyquist": nyquist,
        "required_min_fs": 2 * f_max,
        "satisfied": satisfied,
    }


def compute_spectrum(x: np.ndarray, fs: float) -> tuple[np.ndarray, np.ndarray]:
    spectrum = np.abs(np.fft.rfft(x))
    freq_axis = np.fft.rfftfreq(len(x), d=1.0 / fs)
    return freq_axis, spectrum


def alias_frequency(f_signal: float, fs: float) -> float:
    """Tính tần số alias rơi về dải [0, Fs/2]."""
    return abs(((f_signal + fs / 2) % fs) - fs / 2)


def demo_sampling(show_plots: bool = True, fs: float = 44100.0, duration: float = 0.01, save_dir: str | None = None):
    sampled = sample_signal(fs=fs, duration=duration)
    nyquist_info = analyze_nyquist(sampled["fs"], sampled["f_max"])
    undersampled_fs = 4000.0
    undersampled = sample_signal(fs=undersampled_fs, duration=duration)
    undersampled_nyquist = analyze_nyquist(undersampled_fs, sampled["f_max"])
    aliased_3000 = alias_frequency(3000.0, undersampled_fs)

    print("\n" + "=" * 60)
    print("MÔ PHỎNG TÍN HIỆU GỐC VÀ QUÁ TRÌNH RỜI RẠC HÓA")
    print("=" * 60)
    print("  Phương pháp rời rạc hóa: lấy mẫu đều theo thời gian")
    print(f"  Công thức: x[n] = x(nTs), với Ts = 1/Fs = {sampled['ts']:.8f} s")
    print("  Tín hiệu gốc gồm 3 thành phần: 440 Hz, 1000 Hz, 3000 Hz")
    print(f"  Tần số thành phần lớn nhất f_max = {sampled['f_max']:.1f} Hz")
    print(f"  Tần số lấy mẫu Fs = {sampled['fs']:.1f} Hz")
    print(f"  Tần số Nyquist Fs/2 = {nyquist_info['nyquist']:.1f} Hz")
    print(f"  Điều kiện Nyquist-Shannon yêu cầu Fs >= {nyquist_info['required_min_fs']:.1f} Hz")
    print(f"  Kết luận: {'✔ THỎA MÃN' if nyquist_info['satisfied'] else '✘ KHÔNG THỎA MÃN'}")
    print("  Giải thích: vì 44.1 kHz lớn hơn rất nhiều so với 2 * 3 kHz = 6 kHz nên việc lấy mẫu không gây aliasing cho tín hiệu mô phỏng này.")
    print(f"  So sánh phản ví dụ: nếu lấy mẫu với Fs = {undersampled_fs:.1f} Hz thì Nyquist chỉ còn {undersampled_nyquist['nyquist']:.1f} Hz.")
    print(f"  Khi đó thành phần 3000 Hz sẽ bị alias về khoảng {aliased_3000:.1f} Hz => ✘ không thỏa Nyquist-Shannon.")

    fig, axes = plt.subplots(2, 1, figsize=(12, 8), tight_layout=True)
    fig.suptitle("Tín hiệu gốc và tín hiệu sau rời rạc hóa", fontsize=13, color=COLORS[4])

    axes[0].plot(sampled["t_cont"] * 1e3, sampled["x_cont"], color=COLORS[0])
    axes[0].set_title("Tín hiệu gốc mô phỏng trong miền thời gian liên tục")
    axes[0].set_xlabel("Thời gian (ms)")
    axes[0].set_ylabel("Biên độ")
    axes[0].grid(True)

    axes[1].plot(sampled["t_cont"] * 1e3, sampled["x_cont"], color=COLORS[5], alpha=0.55, label="Tín hiệu gốc")
    markerline, stemlines, baseline = axes[1].stem(sampled["t_disc"] * 1e3, sampled["x_disc"], linefmt=COLORS[2], markerfmt="o", basefmt="white")
    plt.setp(stemlines, linewidth=1.1)
    plt.setp(markerline, markersize=4)
    axes[1].set_title("Gộp hình: tín hiệu gốc + tín hiệu sau lấy mẫu rời rạc")
    axes[1].set_xlabel("Thời gian (ms)")
    axes[1].set_ylabel("Biên độ")
    axes[1].legend(["Tín hiệu gốc", "Mẫu rời rạc"], facecolor="#2a2a3e")
    axes[1].grid(True)

    finalize_figure(
        fig,
        show_plots,
        save_path=build_save_path(save_dir, "01_sampling_time_domain.png"),
    )

    freq_good, spec_good = compute_spectrum(sampled["x_disc"], sampled["fs"])
    freq_bad, spec_bad = compute_spectrum(undersampled["x_disc"], undersampled_fs)

    fig_fft, axes_fft = plt.subplots(2, 1, figsize=(12, 8), tight_layout=True)
    fig_fft.suptitle("So sánh phổ FFT: lấy mẫu đúng và sai Nyquist", fontsize=13, color=COLORS[4])

    axes_fft[0].plot(freq_good, spec_good, color=COLORS[1])
    axes_fft[0].set_xlim(0, 5000)
    axes_fft[0].set_title("FFT khi Fs = 44.1 kHz (thỏa Nyquist)")
    axes_fft[0].set_xlabel("Tần số (Hz)")
    axes_fft[0].set_ylabel("Biên độ phổ")
    axes_fft[0].axvline(440, color=COLORS[2], linestyle="--", linewidth=1)
    axes_fft[0].axvline(1000, color=COLORS[2], linestyle="--", linewidth=1)
    axes_fft[0].axvline(3000, color=COLORS[2], linestyle="--", linewidth=1)
    axes_fft[0].grid(True)

    axes_fft[1].plot(freq_bad, spec_bad, color=COLORS[3])
    axes_fft[1].set_xlim(0, 2000)
    axes_fft[1].set_title("FFT khi Fs = 4 kHz (không thỏa Nyquist, xuất hiện aliasing)")
    axes_fft[1].set_xlabel("Tần số (Hz)")
    axes_fft[1].set_ylabel("Biên độ phổ")
    axes_fft[1].axvline(aliased_3000, color=COLORS[2], linestyle="--", linewidth=1, label=f"Alias của 3000 Hz -> {aliased_3000:.0f} Hz")
    axes_fft[1].legend(facecolor="#2a2a3e")
    axes_fft[1].grid(True)

    finalize_figure(
        fig_fft,
        show_plots,
        save_path=build_save_path(save_dir, "02_sampling_fft_aliasing.png"),
    )
    return {
        "sampled": sampled,
        "nyquist": nyquist_info,
        "undersampled": undersampled,
        "undersampled_nyquist": undersampled_nyquist,
        "aliased_3000": aliased_3000,
    }
