"""
demo_lay_mau.py – Minh họa quá trình rời rạc hóa (lấy mẫu) và định lý Nyquist-Shannon.

Chương này trả lời: cần lấy mẫu nhanh đến mức nào để khôi phục tín hiệu liên tục?
  - Định lý Nyquist-Shannon: fs >= 2 * f_max
  - Hiện tượng aliasing khi lấy mẫu không đủ nhanh
  - Minh họa bằng tín hiệu 440 Hz + 1000 Hz + 3000 Hz
"""

from __future__ import annotations  # Hỗ trợ type hint mới trên Python cũ

import numpy as np            # Tính toán mảng, FFT
import matplotlib.pyplot as plt  # Vẽ biểu đồ

# Import tiện ích đồ thị từ module cấu hình chung
from .cau_hinh_do_thi import COLORS, tao_duong_dan_luu, hoan_thien_bieu_do


def tao_tin_hieu_goc(time_axis: np.ndarray) -> np.ndarray:
    """
    Tạo tín hiệu giả lập liên tục gồm 3 thành phần sin:
      - 440  Hz (0.8):  mô phỏng âm La chuẩn của đàn guitar
      - 1000 Hz (0.35): thành phần trung tần
      - 3000 Hz (0.2):  thành phần cao tần (f_max), quyết định fs tối thiểu

    Tham số:
        time_axis: Mảng thời gian (s) để tính giá trị tín hiệu.
    """
    return (
        0.8  * np.sin(2 * np.pi * 440  * time_axis)   # Thành phần 440 Hz
        + 0.35 * np.sin(2 * np.pi * 1000 * time_axis)  # Thành phần 1000 Hz
        + 0.2  * np.sin(2 * np.pi * 3000 * time_axis)  # Thành phần 3000 Hz
    )


def lay_mau_tin_hieu(fs: float = 44100.0, duration: float = 0.01):
    """
    Lấy mẫu đều tín hiệu theo công thức x[n] = x(n * Ts).

    Tham số:
        fs:       Tần số lấy mẫu (Hz), mặc định 44100 Hz (chất lượng CD).
        duration: Độ dài đoạn tín hiệu cần lấy (giây).

    Trả về:
        dict chứa tất cả tham số, trục thời gian và giá trị tín hiệu.
    """
    ts = 1.0 / fs          # Chu kỳ lấy mẫu Ts (đơn vị giây)
    continuous_fs = fs * 40  # Độ phân giải giả lập tín hiệu liên tục: gấp 40x fs

    # Trục thời gian dày đặc cho tín hiệu liên tục giả lập
    t_cont = np.linspace(0, duration, int(duration * continuous_fs), endpoint=False)
    # Trục thời gian thưa theo tần số lấy mẫu thực tế
    t_disc = np.arange(0, duration, ts)

    x_cont = tao_tin_hieu_goc(t_cont)  # Tín hiệu liên tục (giả lập)
    x_disc = tao_tin_hieu_goc(t_disc)  # Tín hiệu rời rạc sau lấy mẫu

    return {
        "fs": fs,
        "ts": ts,
        "duration": duration,
        "t_cont": t_cont,
        "t_disc": t_disc,
        "x_cont": x_cont,
        "x_disc": x_disc,
        "f_max": 3000.0,        # Tần số cao nhất trong tín hiệu
        "continuous_fs": continuous_fs,
    }


def kiem_tra_nyquist(fs: float, f_max: float) -> dict:
    """
    Kiểm tra định lý Nyquist-Shannon: fs phải >= 2 * f_max.

    Tham số:
        fs:    Tần số lấy mẫu (Hz).
        f_max: Tần số cao nhất trong tín hiệu cần lưu giữ (Hz).
    """
    nyquist  = fs / 2          # Tần số Nyquist: giới hạn trên có thể biểu diễn được
    satisfied = fs >= 2 * f_max  # Điều kiện cần thỏa
    return {
        "fs":            fs,
        "f_max":         f_max,
        "nyquist":       nyquist,
        "required_min_fs": 2 * f_max,  # Tần số lấy mẫu tối thiểu cần có
        "satisfied":     satisfied,
    }


def tinh_pho(x: np.ndarray, fs: float) -> tuple[np.ndarray, np.ndarray]:
    """
    Tính phổ một phía của tín hiệu rời rạc bằng FFT.

    Dùng rfft thay vì fft vì tín hiệu thực: phổ đối xứng nên chỉ cần nửa một phía.

    Trả về:
        (freq_axis, spectrum): trục tần số (Hz) và biên độ phổ.
    """
    spectrum  = np.abs(np.fft.rfft(x))           # Biến đổi Fourier phía thực
    freq_axis = np.fft.rfftfreq(len(x), d=1.0 / fs)  # Trục tần số tương ứng
    return freq_axis, spectrum


def tan_so_alias(f_signal: float, fs: float) -> float:
    """
    Tính tần số alias rơi về dải [0, fs/2] khi lấy mẫu quá đưa.

    Công thức: ta rơi về (f_signal mod fs) được bằng cách phản chiếu quanh fs/2.
    """
    # ((f_signal + fs/2) % fs) – fs/2: ra kết quả trong (-fs/2, fs/2]
    # abs() để đảm bảo giá trị dương
    return abs(((f_signal + fs / 2) % fs) - fs / 2)


def demo_qua_trinh_lay_mau(show_plots: bool = True, fs: float = 44100.0, duration: float = 0.01, save_dir: str | None = None):
    """
    Demo Chương 2: Quá trình lấy mẫu và định lý Nyquist-Shannon.

    Vẽ 4 biểu đồ:
      - Miền thời gian: tín hiệu liên tục
      - Miền thời gian: gộp tín hiệu liên tục + các mẫu rời rạc
      - Phổ FFT khi fs = 44.1 kHz (thỏa Nyquist)
      - Phổ FFT khi fs = 4 kHz (không thỏa, aliasing xảy ra)
    """
    # --- Lấy mẫu đúng điều kiện Nyquist (fs = 44.1 kHz >> 2*3000 = 6 kHz) ---
    sampled      = lay_mau_tin_hieu(fs=fs, duration=duration)
    nyquist_info = kiem_tra_nyquist(sampled["fs"], sampled["f_max"])

    # --- Phản ví dụ: lấy mẫu quá đưa (undersample) với fs = 4 kHz < 2*3000 Hz ---
    undersampled_fs      = 4000.0
    undersampled         = lay_mau_tin_hieu(fs=undersampled_fs, duration=duration)
    undersampled_nyquist = kiem_tra_nyquist(undersampled_fs, sampled["f_max"])
    aliased_3000 = tan_so_alias(3000.0, undersampled_fs)  # Tần số giả mạo xuất hiện

    # --- In tóm tắt kết quả phân tích ---
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

    # ============================================================
    # Biểu đồ 1: Miền thời gian
    # ============================================================
    fig, axes = plt.subplots(2, 1, figsize=(12, 8), tight_layout=True)
    fig.suptitle("Tín hiệu gốc và tín hiệu sau rời rạc hóa", fontsize=13, color=COLORS[4])

    # Subplot trên: chỉ tín hiệu liên tục
    axes[0].plot(sampled["t_cont"] * 1e3, sampled["x_cont"], color=COLORS[0])
    axes[0].set_title("Tín hiệu gốc mô phỏng trong miền thời gian liên tục")
    axes[0].set_xlabel("Thời gian (ms)")
    axes[0].set_ylabel("Biên độ")
    axes[0].grid(True)

    # Subplot dưới: gộp liên tục + stem rời rạc
    axes[1].plot(sampled["t_cont"] * 1e3, sampled["x_cont"], color=COLORS[5], alpha=0.55, label="Tín hiệu gốc")
    # stem: vẽ tín hiệu rời rạc bằng các thanh đứng
    markerline, stemlines, baseline = axes[1].stem(sampled["t_disc"] * 1e3, sampled["x_disc"], linefmt=COLORS[2], markerfmt="o", basefmt="white")
    plt.setp(stemlines, linewidth=1.1)  # Mỗi thanh stem độ dày 1.1
    plt.setp(markerline, markersize=4)  # Mỗi mẫu có chấm kích thước 4
    axes[1].set_title("Gộp hình: tín hiệu gốc + tín hiệu sau lấy mẫu rời rạc")
    axes[1].set_xlabel("Thời gian (ms)")
    axes[1].set_ylabel("Biên độ")
    axes[1].legend(["Tín hiệu gốc", "Mẫu rời rạc"], facecolor="#2a2a3e")
    axes[1].grid(True)

    hoan_thien_bieu_do(
        fig,
        show_plots,
        save_path=tao_duong_dan_luu(save_dir, "01_sampling_time_domain.png"),
    )

    # ============================================================
    # Biểu đồ 2: Phổ FFT so sánh đúng/sai Nyquist
    # ============================================================
    freq_good, spec_good = tinh_pho(sampled["x_disc"],     sampled["fs"])
    freq_bad,  spec_bad  = tinh_pho(undersampled["x_disc"], undersampled_fs)

    fig_fft, axes_fft = plt.subplots(2, 1, figsize=(12, 8), tight_layout=True)
    fig_fft.suptitle("So sánh phổ FFT: lấy mẫu đúng và sai Nyquist", fontsize=13, color=COLORS[4])

    # Subplot trên: fs thỏa → các đỉnh phổ rõ tại đúng vị trí gốc
    axes_fft[0].plot(freq_good, spec_good, color=COLORS[1])
    axes_fft[0].set_xlim(0, 5000)
    axes_fft[0].set_title("FFT khi Fs = 44.1 kHz (thỏa Nyquist)")
    axes_fft[0].set_xlabel("Tần số (Hz)")
    axes_fft[0].set_ylabel("Biên độ phổ")
    # Đường kẻ dọc đánh dấu vị trí 3 thành phần tần số
    axes_fft[0].axvline(440,  color=COLORS[2], linestyle="--", linewidth=1)
    axes_fft[0].axvline(1000, color=COLORS[2], linestyle="--", linewidth=1)
    axes_fft[0].axvline(3000, color=COLORS[2], linestyle="--", linewidth=1)
    axes_fft[0].grid(True)

    # Subplot dưới: fs không thỏa → xuất hiện đỉnh giả (alias)
    axes_fft[1].plot(freq_bad, spec_bad, color=COLORS[3])
    axes_fft[1].set_xlim(0, 2000)
    axes_fft[1].set_title("FFT khi Fs = 4 kHz (không thỏa Nyquist, xuất hiện aliasing)")
    axes_fft[1].set_xlabel("Tần số (Hz)")
    axes_fft[1].set_ylabel("Biên độ phổ")
    # Đường kẻ dọc chỉ vị trí tần số alias
    axes_fft[1].axvline(aliased_3000, color=COLORS[2], linestyle="--", linewidth=1, label=f"Alias của 3000 Hz -> {aliased_3000:.0f} Hz")
    axes_fft[1].legend(facecolor="#2a2a3e")
    axes_fft[1].grid(True)

    hoan_thien_bieu_do(
        fig_fft,
        show_plots,
        save_path=tao_duong_dan_luu(save_dir, "02_sampling_fft_aliasing.png"),
    )
    # Trả về kết quả để các module khác có thể dùng nếu cần
    return {
        "sampled": sampled,
        "nyquist": nyquist_info,
        "undersampled": undersampled,
        "undersampled_nyquist": undersampled_nyquist,
        "aliased_3000": aliased_3000,
    }
