"""
ung_dung.py – Các ứng dụng thực tế của bộ lọc số trong xử lý âm thanh:
  1. Bộ lọc Notch 50 Hz: loại bỏ nhiễu điện lưới
  2. Mô phỏng hiệu ứng Echo (Lab-Volt TMS320C50 ex1_1)

Đây là phần "ứng dụng" cuối của báo cáo, minh họa DSP giải
quyết các bài toán thực tế như thế nào.
"""

from __future__ import annotations  # Hỗ trợ type hint mới trên Python cũ

import numpy as np             # Tính toán số mảng
import matplotlib.pyplot as plt   # Vẽ biểu đồ
from scipy import signal         # signal.iirnotch, signal.lfilter
from scipy.signal import freqz   # Tính đáp ứng tần số bộ lọc notch

# Import tiện ích đồ thị và năng lượng
from .cau_hinh_do_thi import COLORS, tao_duong_dan_luu, hoan_thien_bieu_do
from .thaotac_tin_hieu import nang_luong  # Để tính SNR trước/sau lọc


def thiet_ke_notch_50hz(fs: float = 44100.0, q: float = 30.0):
    """
    Thiết kế bộ lọc notch IIR loại bỏ hẹp tần số 50 Hz.

    Tham số:
        fs: Tần số lấy mẫu (Hz).
        q:  Hệ số Q (quality factor) – Q càng cao, dải chặn càng hẹp.
            Q=30 → dải chặn chỉ ~1.67 Hz quanh 50 Hz, giữ gần như toàn bộ phổ còn lại.

    Trả về:
        (b, a): Hệ số bộ lọc notch IIR bậc 2.
    """
    # iirnotch(f0, Q, fs): sinh bộ lọc notch tập trung tại f0 Hz với hệ số chất Q
    return signal.iirnotch(50.0, q, fs=fs)


def demo_bo_loc_notch(fs: float = 44100.0, show_plots: bool = True, save_dir: str | None = None):
    """
    Demo bộ lọc Notch 50 Hz: tạo tín hiệu bẩn rồi lọc và so sánh SNR.

    Tín hiệu:
      - clean:   sin 440 Hz (âm La4 chuẩn)
      - hum:     sin 50 Hz biên độ 0.6 (nhiễu điện lưới)
      - noisy:   clean + hum + noise Gaussian nhỏ

    Đánh giá: SNR (dB) trước và sau lọc.
    Lưu 08_notch_50hz.png nếu có save_dir.
    """
    print("\n" + "=" * 60)
    print("BỔ SUNG: BỘ LỌC NOTCH 50Hz – LOẠI BỎ NHIỄU ĐIỆN LƯỚI")
    print("=" * 60)

    # --- Tạo tín hiệu thử ---
    duration = 0.5  # 500 ms đủ để thấy nhiễu 50 Hz
    time = np.linspace(0, duration, int(fs * duration), endpoint=False)
    rng = np.random.default_rng(42)  # Random seed cố định để tái lập

    clean  = np.sin(2 * np.pi * 440  * time)              # Tín hiệu hữu ích
    hum    = 0.6 * np.sin(2 * np.pi * 50   * time)        # Nhiễu hum 50 Hz
    noisy  = clean + hum + 0.05 * rng.standard_normal(len(time))  # Tín hiệu bẩn

    # --- Lọc notch ---
    b_notch, a_notch = thiet_ke_notch_50hz(fs)
    # lfilter: áp dụng bộ lọc IIR theo thứ tự nhân quả (causal), bắt đầu từ đầu
    filtered = signal.lfilter(b_notch, a_notch, noisy)

    # --- Tính SNR (dB): E_hữu_ích / E_nhiễu ---
    snr_before = 10 * np.log10(nang_luong(clean) / nang_luong(noisy   - clean))
    snr_after  = 10 * np.log10(nang_luong(clean) / nang_luong(filtered - clean))
    print(f"  SNR trước lọc : {snr_before:.2f} dB")
    print(f"  SNR sau lọc   : {snr_after:.2f} dB")

    # --- Tính đáp ứng tần số của bộ lọc notch ---
    w, response    = freqz(b_notch, a_notch, worN=8192, fs=fs)
    sample_count   = min(2000, len(time))  # Chỉ vẽ 2000 mẫu đầu để rõ hơn

    fig, axes = plt.subplots(2, 2, figsize=(13, 8), tight_layout=True)
    fig.suptitle("Bổ sung – Bộ lọc Notch 50Hz", fontsize=13, color=COLORS[4])

    # [0,0] Tín hiệu nhiễu trước lọc
    axes[0, 0].plot(time[:sample_count] * 1e3, noisy[:sample_count], color=COLORS[2], linewidth=0.8)
    axes[0, 0].set_title("Tín hiệu nhiễu (440Hz + 50Hz)")
    axes[0, 0].set_xlabel("Thời gian (ms)")
    axes[0, 0].set_ylabel("Biên độ")
    axes[0, 0].grid(True)

    # [0,1] Tín hiệu sau lọc – tiếng hum phải biến mất
    axes[0, 1].plot(time[:sample_count] * 1e3, filtered[:sample_count], color=COLORS[1], linewidth=0.8)
    axes[0, 1].set_title("Tín hiệu sau lọc Notch")
    axes[0, 1].set_xlabel("Thời gian (ms)")
    axes[0, 1].set_ylabel("Biên độ")
    axes[0, 1].grid(True)

    # [1,0] Phổ FFT trước/sau lọc trên cùng biểu đồ
    freq_axis = np.fft.rfftfreq(len(time), 1 / fs)
    axes[1, 0].plot(freq_axis, np.abs(np.fft.rfft(noisy)),    color=COLORS[2], linewidth=0.8, label="Trước")
    axes[1, 0].plot(freq_axis, np.abs(np.fft.rfft(filtered)), color=COLORS[1], linewidth=0.8, label="Sau")
    axes[1, 0].set_xlim(0, 600)  # Chỉ xem 0–600 Hz để thấy đỉnh 50 Hz và 440 Hz
    axes[1, 0].set_title("Phổ biên độ (0–600 Hz)")
    axes[1, 0].set_xlabel("Tần số (Hz)")
    axes[1, 0].set_ylabel("|FFT|")
    axes[1, 0].legend(facecolor="#2a2a3e")
    axes[1, 0].grid(True)

    # [1,1] Đáp ứng biên độ của chính bộ lọc notch – nên có hố sâu tại 50 Hz
    axes[1, 1].plot(w, 20 * np.log10(np.abs(response) + 1e-12), color=COLORS[4])
    axes[1, 1].set_xlim(0, 500)
    axes[1, 1].set_ylim(-60, 5)
    axes[1, 1].axvline(50, color=COLORS[2], linestyle="--", label="50 Hz")  # Tần số notch
    axes[1, 1].set_title("Đáp ứng biên độ Notch Filter")
    axes[1, 1].set_xlabel("Tần số (Hz)")
    axes[1, 1].set_ylabel("Biên độ (dB)")
    axes[1, 1].legend(facecolor="#2a2a3e")
    axes[1, 1].grid(True)

    hoan_thien_bieu_do(
        fig,
        show_plots,
        save_path=tao_duong_dan_luu(save_dir, "08_notch_50hz.png"),
    )
    return {"b": b_notch, "a": a_notch, "snr_before": snr_before, "snr_after": snr_after}


def mo_phong_echo(x: np.ndarray, fs: float, delay_ms: float = 200.0, decay: float = 0.5) -> np.ndarray:
    """
    Mô phỏng hiệu ứng echo bằng cách cộng phiên bản trễ có suy giảm:
        y[n] = x[n] + decay * x[n - D]
    trong đó D = delay_ms * fs / 1000 (số mẫu trễ).

    Tham số:
        x:         Tín hiệu đầu vào.
        fs:        Tần số lấy mẫu (Hz).
        delay_ms:  Độ trễ echo (ms).
        decay:     Hệ số suy giảm biên độ của tiếng vọng (0 = không echo, 1 = không suy giảm).

    Trả về:
        y: Tín hiệu có echo.
    """
    delay_samples = int(delay_ms * fs / 1000)  # Đổi ms sang số mẫu nguyên
    padded  = np.zeros(delay_samples)           # D mẫu 0 ở đầu (trễ nhân quả)
    delayed = np.concatenate([padded, x[:-delay_samples]])  # Ghép: [0...0, x[0], x[1], ...]
    return x + decay * delayed  # Cộng tín hiệu gốc với tiếng vọng suy giảm


def demo_hieu_ung_echo(fs: float = 8000.0, show_plots: bool = True, save_dir: str | None = None):
    """
    Demo hiệu ứng Echo – tham khảo Lab-Volt TMS320C50 ex1_1.

    Tạo tín hiệu xung ngắn, sau đó áp dụng echo với 2 giá trị delay khác nhau
    (100 ms và 400 ms) để thấy tiếng vọng xuất hiện sau tín hiệu gốc.
    Dùng fs = 8000 Hz cho phù hợp với ví dụ gốc của DSP Lab.
    Lưu 09_echo_demo.png nếu có save_dir.
    """
    print("\n" + "=" * 60)
    print("BỔ SUNG: MÔ PHỎNG ECHO – LAB-VOLT TMS320C50 ex1_1")
    print("=" * 60)

    duration = 1.0  # 1 giây audio @ 8 kHz
    time = np.linspace(0, duration, int(fs * duration), endpoint=False)

    # Tạo tín hiệu xung: hai đoạn hanning window ngắn
    x = np.zeros(len(time))
    x[100:200] = np.hanning(100)       # Xung thứ nhất (biên độ 1.0)
    x[400:600] = 0.7 * np.hanning(200) # Xung thứ hai  (biên độ 0.7)

    # In thông tin trễ cho từng cấu hình
    delays = [(100, COLORS[0]), (200, COLORS[1]), (400, COLORS[3])]
    for delay_ms, _ in delays:
        print(f"  delay={delay_ms}ms: D = {int(delay_ms * fs / 1000)} mẫu")

    fig, axes = plt.subplots(3, 1, figsize=(11, 8), tight_layout=True)
    fig.suptitle("Bổ sung – Mô phỏng Echo (Lab-Volt TMS320C50)", fontsize=13, color=COLORS[4])

    # Subplot 1: tín hiệu gốc không có echo
    axes[0].plot(time, x, color=COLORS[5], linewidth=0.9)
    axes[0].set_title("Tín hiệu gốc x(n)")
    axes[0].set_ylabel("Biên độ")
    axes[0].grid(True)

    # Subplot 2 & 3: tín hiệu sau echo với hai độ trễ khác nhau
    for index, (delay_ms, color) in enumerate([(100, COLORS[0]), (400, COLORS[3])], start=1):
        y = mo_phong_echo(x, fs, delay_ms=delay_ms)
        axes[index].plot(time, y, color=color, linewidth=0.9)
        axes[index].set_title(f"Echo với delay = {delay_ms} ms (D={int(delay_ms * fs / 1000)} mẫu)")
        axes[index].set_ylabel("Biên độ")
        axes[index].grid(True)

    axes[-1].set_xlabel("Thời gian (giây)")
    hoan_thien_bieu_do(
        fig,
        show_plots,
        save_path=tao_duong_dan_luu(save_dir, "09_echo_demo.png"),
    )
    return {"x": x, "time": time}
