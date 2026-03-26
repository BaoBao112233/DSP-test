"""
thiet_ke_fir.py – Thiết kế bộ lọc FIR theo hai phương pháp:
  1. Phương pháp cửa sổ Hamming: đơn giản, bậc lớn
  2. Phương pháp Parks-McClellan (Remez): equiripple, bậc nhỏ hơn

Cả hai tạo ra bộ lọc pha tuyến tính (linear phase) –
ánh xạ các tần số qua bộ lọc với cùng độ trễ thời gian, không gây méo pha.
"""

from __future__ import annotations  # Hỗ trợ type hint mới trên Python cũ

import numpy as np             # Tính toán số mảng
import matplotlib.pyplot as plt   # Vẽ biểu đồ
import matplotlib.gridspec as gridspec  # Chia lưới subplot linh hoạt hơn plt.subplots
from scipy.signal import firwin, freqz, remez
# firwin : thiết kế FIR bằng phương pháp cửa sổ
# freqz  : tính đáp ứng tần số H(e^{jω})
# remez  : thuật toán Parks-McClellan equiripple

# Import tiện ích đồ thị
from .cau_hinh_do_thi import COLORS, tao_duong_dan_luu, hoan_thien_bieu_do


def thiet_ke_fir_hamming(wp_rad: float, ws_rad: float) -> np.ndarray:
    """
    Thiết kế bộ lọc FIR low-pass bằng cửa sổ Hamming.

    Tham số:
        wp_rad: Mép dải thông (rad/mẫu).
        ws_rad: Mép dải chặn (rad/mẫu).

    Trả về:
        h: Mảng hệ số bộ lọc FIR (impulse response).
    """
    delta_w = ws_rad - wp_rad  # Bề rộng dải chuyển tiếp
    # Bậc bộ lọc theo công thức Harris: M = ceil(6.6π / Δω)
    order = int(np.ceil(6.6 * np.pi / delta_w))
    if order % 2 != 0:  # FIR Type I cần bậc chẵn để đối xứng
        order += 1
    cutoff = (wp_rad + ws_rad) / 2  # Tần số cắt nằm giữa hai mép
    # firwin tạo các hệ số bộ lọc, chuẩn hóa cutoff về [0, 1]
    coefficients = firwin(order + 1, cutoff / np.pi, window="hamming")
    print(f"  [Hamming] Bậc M = {order},  ωc = {cutoff / np.pi:.4f}π  ({len(coefficients)} hệ số)")
    return coefficients


def thiet_ke_fir_pm(wp_rad: float, ws_rad: float, delta1_db: float = 0.5, delta2_db: float = 40.0) -> np.ndarray:
    """
    Thiết kế bộ lọc FIR bằng thuật toán Parks-McClellan (Remez equiripple).

    Phương pháp này tối thiểu hóa sai số cực đại (minimax) giữa các dải,
    cho bậc nhỏ hơn Hamming với cùng đặc tả.

    Tham số:
        wp_rad, ws_rad: Mép dải thông/dải chặn (rad/mẫu).
        delta1_db:     Ripple cho phép trong dải thông (dB).
        delta2_db:     Suy giảm tối thiểu trong dải chặn (dB).
    """
    # Chuyển ripple từ dB sang đơn vị tuyệt đối
    delta1 = (10 ** (delta1_db / 20) - 1) / (10 ** (delta1_db / 20) + 1)
    delta2 = 10 ** (-delta2_db / 20)
    delta  = min(delta1, delta2)  # Lấy ngưỡng khắt hơn trong hai dải

    transition = ws_rad - wp_rad  # Bề rộng dải chuyển tiếp
    # Công thức Herrmann (1973): D = (-20*log10(δ) - 13) / 14.6
    d_value = (-20 * np.log10(delta) - 13) / 14.6
    order   = int(np.ceil(d_value / transition * np.pi))
    if order % 2 != 0:
        order += 1

    # Cấu hình các dải cho remez: [0, wp, ws, 1] và giá trị đích [1, 0]
    bands   = [0, wp_rad / np.pi, ws_rad / np.pi, 1.0]  # Mọi giá trị đã chuẩn hóa [0, 1]
    desired = [1, 0]          # Dải thông = 1, dải chặn = 0
    weight  = [delta2 / delta1, 1]  # Trọng số tương đối giữa hai dải
    coefficients = remez(order + 1, bands, desired, weight=weight, fs=2.0)
    print(f"  [P-McClellan] Bậc M = {order},  {len(coefficients)} hệ số")
    return coefficients


def ve_dap_ung_fir(
    h_hamming: np.ndarray,
    h_pm: np.ndarray,
    fs: float = 44100.0,
    show_plots: bool = True,
    save_path: str | None = None,
):
    """
    Vẽ và so sánh đáp ứng biên độ + pha của hai bộ lọc FIR.

    Tham số:
        h_hamming: Hệ số FIR Hamming.
        h_pm:      Hệ số FIR Parks-McClellan.
        fs:        Tần số lấy mẫu để quy đổi trục tần số ra Hz.
        show_plots, save_path: Xem hoan_thien_bieu_do().
    """
    # Tạo layout 2x2 bằng GridSpec để kiểm soát tỷ lệ subplot
    fig  = plt.figure(figsize=(13, 10), tight_layout=True)
    fig.suptitle("Chương 3 – Bộ lọc FIR: Hamming vs Parks-McClellan", fontsize=13, color=COLORS[4])
    grid = gridspec.GridSpec(2, 2)  # 2 hàng × 2 cột

    for index, (coefficients, label, color) in enumerate([
        (h_hamming, "Hamming",          COLORS[0]),
        (h_pm,      "Parks-McClellan",  COLORS[1]),
    ]):
        # Tính đáp ứng tần số với 4096 điểm tần số → đường cong mượt
        w, response = freqz(coefficients, worN=4096, fs=fs)

        # Hàng trên: đáp ứng biên độ (dB)
        ax_mag = fig.add_subplot(grid[0, index])
        # 20*log10(|H|): chuyển sang thang dB, +1e-12 tránh log(0)
        ax_mag.plot(w / 1e3, 20 * np.log10(np.abs(response) + 1e-12), color=color)
        ax_mag.set_title(f"Magnitude – {label}")
        ax_mag.set_xlabel("Tần số (kHz)")
        ax_mag.set_ylabel("Biên độ (dB)")
        ax_mag.set_ylim(-80, 5)  # Giới hạn trục Y để thấy rõ dải chặn
        ax_mag.axhline(-40, color=COLORS[2], linestyle="--", linewidth=1, label="−40 dB")
        ax_mag.legend(facecolor="#2a2a3e")
        ax_mag.grid(True)

        # Hàng dưới: đáp ứng pha (độ)
        ax_phase = fig.add_subplot(grid[1, index])
        # np.unwrap: bỏ cuộn 2π để đồ thị pha liên tục (không nhảy cóc)
        ax_phase.plot(w / 1e3, np.unwrap(np.angle(response)) * 180 / np.pi, color=color)
        ax_phase.set_title(f"Pha – {label}")
        ax_phase.set_xlabel("Tần số (kHz)")
        ax_phase.set_ylabel("Góc pha (độ)")
        ax_phase.grid(True)

    hoan_thien_bieu_do(fig, show_plots, save_path=save_path)


def demo_bo_loc_fir(fs: float = 44100.0, show_plots: bool = True, save_dir: str | None = None):
    """
    Demo Chương 4: Thiết kế bộ lọc FIR – so sánh Hamming và Parks-McClellan.

    Chạy cả hai thiết kế với cùng đặc tả và vẽ kết quả để so sánh.
    Lưu 05_fir_hamming_vs_pm.png nếu có save_dir.
    """
    print("\n" + "=" * 60)
    print("CHƯƠNG 3: THIẾT KẾ BỘ LỌC FIR")
    print("=" * 60)
    # Tần số mép dải thông và dải chặn (rad/mẫu)
    wp = 0.2 * np.pi  # ωp = 0.2π  ≈ 4.41 kHz @ fs=44100
    ws = 0.3 * np.pi  # ωs = 0.3π  ≈ 6.615 kHz @ fs=44100

    fp      = wp * fs / (2 * np.pi)  # Quy đổi sang Hz để in
    fs_edge = ws * fs / (2 * np.pi)
    print(f"  Fs = {fs} Hz,  fp = {fp:.1f} Hz,  fs_edge = {fs_edge:.1f} Hz")

    h_hamming = thiet_ke_fir_hamming(wp, ws)  # Thiết kế theo cửa sổ Hamming
    h_pm      = thiet_ke_fir_pm(wp, ws)       # Thiết kế theo Parks-McClellan
    # FIR với h đối xứng (Type I) đảm bảo pha tuyến tính chính xác
    print("  Pha tuyến tính (Hamming) : ✔  (FIR với h đối xứng – Type 1)")
    ve_dap_ung_fir(
        h_hamming,
        h_pm,
        fs=fs,
        show_plots=show_plots,
        save_path=tao_duong_dan_luu(save_dir, "05_fir_hamming_vs_pm.png"),
    )
    return {"h_hamming": h_hamming, "h_pm": h_pm, "wp": wp, "ws": ws, "fs": fs}
