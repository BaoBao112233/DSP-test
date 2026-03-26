"""
thiet_ke_iir.py – Thiết kế bộ lọc IIR bằng phương pháp bilinear transform.

Quy trình:
  1. Pre-warp tần số thiết kế từ miền rời rạc sang miền liên tục
  2. Thiết kế bộ lọc analog Chebyshev Type I (SciPy cheb1ord + cheby1)
  3. Biến đổi bilinear để chuyển về bộ lọc số H(z)

Ưu điểm: bậc rất thấp so với FIR (cùng đặc tả).
Nhược điểm: pha phi tuyến → group delay không đều.
"""

from __future__ import annotations  # Hỗ trợ type hint mới trên Python cũ

import numpy as np             # Tính toán số mảng
import matplotlib.pyplot as plt   # Vẽ biểu đồ
from scipy import signal         # cheb1ord: tính bậc tối thiểu Chebyshev
from scipy.signal import cheby1, freqz, group_delay
# cheby1     : sinh hệ số bộ lọc Chebyshev Type I
# freqz      : tính đáp ứng tần số H(e^{jω})
# group_delay: tính trễ nhóm τ(ω) = -dφ/dω

# Import tiện ích đồ thị
from .cau_hinh_do_thi import COLORS, tao_duong_dan_luu, hoan_thien_bieu_do


def thiet_ke_iir_bilinear(wp_rad: float, ws_rad: float, rp_db: float, rs_db: float, fs: float):
    """
    Thiết kế bộ lọc IIR low-pass Chebyshev Type I bằng bilinear transform.

    Tham số:
        wp_rad: Mép dải thông (rad/mẫu).
        ws_rad: Mép dải chặn (rad/mẫu).
        rp_db:  Ripple tối đa cho phép trong dải thông (dB).
        rs_db:  Suy giảm tối thiểu trong dải chặn (dB).
        fs:     Tần số lấy mẫu (Hz).

    Trả về:
        (b, a, order, omega_p, omega_s)
    """
    sampling_period = 1.0 / fs  # Chu kỳ lấy mẫu T = 1/fs

    # Pre-warp: Ω = (2/T) * tan(ω/2) – bù hiệu ứng co/giãn tần số của bilinear
    omega_p = (2 / sampling_period) * np.tan(wp_rad / 2)   # Ωp analog (rad/s)
    omega_s = (2 / sampling_period) * np.tan(ws_rad / 2)   # Ωs analog (rad/s)
    print(f"  Pre-warp: ΩP = {omega_p:.2f} rad/s,  ΩS = {omega_s:.2f} rad/s")

    # Tính bậc tối thiểu N và tần số -3dB critical cho Chebyshev Type I
    # cheb1ord nhận tần số chuẩn hóa [0, 1] → chia cho π
    order, critical = signal.cheb1ord(wp_rad / np.pi, ws_rad / np.pi, rp_db, rs_db)
    print(f"  Bậc Chebyshev Type I : N = {order}")

    # cheby1: sinh hệ số b, a của bộ lọc số từ đặc tả Chebyshev
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
    """
    Vẽ 4 đồ thị đáp ứng của bộ lọc IIR: biên độ, pha, group delay, mặt phẳng Z.

    Tham số:
        b, a:   Hệ số bộ lọc.
        fs:     Tần số lấy mẫu để quy đổi trục tần số.
        title:  Tiêu đề figure.
        show_plots, save_path: Xem hoan_thien_bieu_do().
    """
    # Tính đáp ứng tần số với 8192 điểm → đường cong rất mượt
    w, response = freqz(b, a, worN=8192, fs=fs)
    # Group delay: τ(ω) = -dφ/dω – chỉ số bất đối xứng pha theo tần số
    w_gd, gd = group_delay((b, a), w=8192, fs=fs)

    fig, axes = plt.subplots(2, 2, figsize=(13, 9), tight_layout=True)
    fig.suptitle(f"Chương 4 – {title}", fontsize=13, color=COLORS[4])

    # [0,0] Đáp ứng biên độ (dB)
    axes[0, 0].plot(w / 1e3, 20 * np.log10(np.abs(response) + 1e-12), color=COLORS[0])
    axes[0, 0].set_title("Đáp ứng biên độ")
    axes[0, 0].set_xlabel("Tần số (kHz)")
    axes[0, 0].set_ylabel("Biên độ (dB)")
    axes[0, 0].set_ylim(-80, 5)
    axes[0, 0].axhline(-3, color=COLORS[2], linestyle="--", label="−3 dB")  # Điểm cắt -3dB
    axes[0, 0].legend(facecolor="#2a2a3e")
    axes[0, 0].grid(True)

    # [0,1] Đáp ứng pha (độ, đã unwrap)
    axes[0, 1].plot(w / 1e3, np.unwrap(np.angle(response)) * 180 / np.pi, color=COLORS[1])
    axes[0, 1].set_title("Đáp ứng pha")
    axes[0, 1].set_xlabel("Tần số (kHz)")
    axes[0, 1].set_ylabel("Pha (độ)")
    axes[0, 1].grid(True)

    # [1,0] Group delay – IIR phi tuyến → đường không nằm ngang
    axes[1, 0].plot(w_gd / 1e3, gd, color=COLORS[3])
    axes[1, 0].set_title("Group Delay (Trễ nhóm)")
    axes[1, 0].set_xlabel("Tần số (kHz)")
    axes[1, 0].set_ylabel("Mẫu (samples)")
    axes[1, 0].set_ylim(0, None)  # Không cắt âm
    axes[1, 0].grid(True)

    # [1,1] Mặt phẳng Z nội tuyền (inline, không dùng ve_mat_phang_z riêng)
    zeros_z = np.roots(b)  # Nghiệm tử số
    poles_z = np.roots(a)  # Nghiệm mẫu số
    theta = np.linspace(0, 2 * np.pi, 360)
    axes[1, 1].plot(np.cos(theta), np.sin(theta), color="#6c7086", linewidth=1)
    axes[1, 1].axhline(0, color="#6c7086", linewidth=0.5)
    axes[1, 1].axvline(0, color="#6c7086", linewidth=0.5)
    axes[1, 1].scatter(zeros_z.real, zeros_z.imag, marker="o", s=80,
                       facecolors="none", edgecolors=COLORS[1], linewidths=2, label="Zeros")
    axes[1, 1].scatter(poles_z.real, poles_z.imag, marker="x", s=80,
                       color=COLORS[2], linewidths=2, label="Poles")
    axes[1, 1].set_xlim(-1.5, 1.5)
    axes[1, 1].set_ylim(-1.5, 1.5)
    axes[1, 1].set_aspect("equal")
    axes[1, 1].set_title("Mặt phẳng Z")
    axes[1, 1].legend(facecolor="#2a2a3e")
    axes[1, 1].grid(True)

    # Kiểm tra ổn định: tất cả cực nằm bên trong |z| = 1
    stable = np.all(np.abs(poles_z) < 1.0)
    print(f"  Ổn định: {'✔ CÓ' if stable else '✘ KHÔNG'} (max|pole| = {np.max(np.abs(poles_z)):.4f})")
    hoan_thien_bieu_do(fig, show_plots, save_path=save_path)
    return stable


def demo_bo_loc_iir(fs: float = 44100.0, show_plots: bool = True, save_dir: str | None = None):
    """
    Demo Chương 5: Thiết kế bộ lọc IIR Chebyshev Type I bằng bilinear transform.

    Dùng cùng đặc tả wp, ws như FIR để so sánh sau này (Chương 7).
    Lưu 06_iir_response.png nếu có save_dir.
    """
    print("\n" + "=" * 60)
    print("CHƯƠNG 4 & 5: THIẾT KẾ BỘ LỌC IIR – BILINEAR CHEBYSHEV TYPE I")
    print("=" * 60)
    wp = 0.2 * np.pi   # Mép dải thông (rad/mẫu)
    ws = 0.3 * np.pi   # Mép dải chặn (rad/mẫu)
    rp = 1.0           # Ripple dải thông: 1 dB
    rs = 15.0          # Suy giảm dải chặn: 15 dB

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
