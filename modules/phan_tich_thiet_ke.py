"""
phan_tich_thiet_ke.py – Phân tích tham số đầu vào và lý do chọn bộ lọc.

Module này chỉ xuất văn bản ra console (không có biểu đồ),
gồm các bước phân tích kỹ thuật thường được viết trong báo cáo:
  1. Phân tích tín hiệu đầu vào và yêu cầu bộ lọc
  2. Giải thích tại sao chọn từng loại bộ lọc + ước tính bậc
  3. Tính toán tham số pre-warp cho biến đổi bilinear
"""

from __future__ import annotations  # Hỗ trợ type hint mới trên Python cũ

import numpy as np       # Các hàm toán học cơ bản (pi, ceil, log10, tan)
from scipy import signal  # chỉ dùng signal.cheb1ord để ước tính bậc Chebyshev


def phan_tich_dau_vao(fs: float = 44100.0):
    """
    Phân tích tín hiệu đầu vào và xác định yêu cầu tần số của bộ lọc.

    Tham số:
        fs: Tần số lấy mẫu (Hz).

    Trả về:
        dict các tham số tần số biên.
    """
    # Tần số mép dải thông và dải chặn (tần số chuẩn hóa, đơn vị rad/mẫu)
    wp = 0.2 * np.pi  # Mép dải thông: 0.2π rad/mẫu = 0.1 * fs
    ws = 0.3 * np.pi  # Mép dải chặn: 0.3π rad/mẫu = 0.15 * fs

    # Quy đổi sang Hz bằng công thức: f_Hz = (ω_rad * Fs) / (2π)
    fp      = wp * fs / (2 * np.pi)   # Mép dải thông âm thanh (≈ 4.41 kHz)
    fs_edge = ws * fs / (2 * np.pi)  # Mép dải chặn âm thanh (≈ 6.615 kHz)
    transition_hz = fs_edge - fp      # Bề rộng dải chuyển tiếp

    print("\n" + "=" * 60)
    print("PHÂN TÍCH TÍN HIỆU INPUT")
    print("=" * 60)
    print("  1) Input cho bài toán low-pass audio:")
    print(f"     - Tần số lấy mẫu Fs = {fs:.1f} Hz")
    print(f"     - Mép dải thông fp = {fp:.1f} Hz")
    print(f"     - Mép dải chắn fs = {fs_edge:.1f} Hz")
    print(f"     - Bề rộng dải chuyển tiếp = {transition_hz:.1f} Hz")
    print("     - Diễn giải: tín hiệu hữu ích nằm chủ yếu dưới 4.41 kHz, các thành phần trên 6.615 kHz cần bị suy giảm.")
    print("  2) Input cho bài toán notch demo:")
    print("     - Thành phần hữu ích: sin 440 Hz (nốt La4)")
    print("     - Nhiễu hẹp băng: 50 Hz từ điện lưới")
    print("     - Nhiễu ngẫu nhiên: Gaussian biên độ nhỏ")
    print("     - Diễn giải: vì nhiễu tập trung mạnh ở 50 Hz nên bộ lọc notch là lựa chọn hợp lý hơn low-pass thông thường.")

    return {
        "fs": fs,
        "wp": wp,
        "ws": ws,
        "fp": fp,
        "fs_edge": fs_edge,
        "transition_hz": transition_hz,
    }


def giai_thich_lua_chon(fs: float = 44100.0, specs: dict | None = None):
    """
    Giải thích lý do chọn từng loại bộ lọc và ước tính bậc tối thiểu.

    Tham số:
        fs:    Tần số lấy mẫu (Hz).
        specs: Kết quả từ phan_tich_dau_vao(); nếu None sẽ tự gọi.
    """
    if specs is None:
        specs = phan_tich_dau_vao(fs)
    wp      = specs["wp"]
    ws      = specs["ws"]
    delta_w = ws - wp  # Bề rộng dải chuyển tiếp theo rad/mẫu

    # --- FIR Hamming: công thức kinh nghiệm Harris/Kaiser ---
    # M = ceil(6.6 * π / Δω): 6.6 là hằng số của cửa sổ Hamming
    hamming_order = int(np.ceil(6.6 * np.pi / delta_w))
    if hamming_order % 2 != 0:  # Bậc phải chẵn để bộ lọc FIR Type I đối xứng
        hamming_order += 1

    # --- IIR Chebyshev Type I: dùng cheb1ord tính bậc tối thiểu ---
    rp_db = 1.0   # Ripple tối đa trong dải thông: 1 dB
    rs_db = 15.0  # Suy giảm tối thiểu trong dải chặn: 15 dB
    iir_order, critical = signal.cheb1ord(wp / np.pi, ws / np.pi, rp_db, rs_db)
    # wp / np.pi: chuẩn hóa về [0, 1] theo quy ước của SciPy

    # --- FIR Parks-McClellan: công thức Kaiser-Hermann (Herrmann 1973) ---
    delta1_db = 0.5   # Ripple dải thông: 0.5 dB
    delta2_db = 40.0  # Suy giảm dải chặn: 40 dB
    # Chuyển từ dB sang đơn vị tuyết đối
    delta1 = (10 ** (delta1_db / 20) - 1) / (10 ** (delta1_db / 20) + 1)
    delta2 = 10 ** (-delta2_db / 20)
    delta  = min(delta1, delta2)
    # Tham số D (Herrmann): D = (-20*log10(δ) - 13) / 14.6
    d_value  = (-20 * np.log10(delta) - 13) / 14.6
    pm_order = int(np.ceil(d_value / delta_w * np.pi))
    if pm_order % 2 != 0:
        pm_order += 1

    print("\n" + "=" * 60)
    print("LÝ DO CHỌN BỘ LỌC + BẬC LỌC")
    print("=" * 60)
    print("  1) FIR Hamming:")
    print("     - Chọn khi cần pha tuyến tính để hạn chế méo dạng âm thanh.")
    print("     - Bậc lớn hơn vì phương pháp cửa sổ không tối ưu tuyệt đối.")
    print(f"     - Bậc tính theo công thức báo cáo: M = ceil(6.6π/Δω) = {hamming_order}.")
    print("  2) FIR Parks-McClellan:")
    print("     - Chọn khi vẫn cần FIR nhưng muốn ít hệ số hơn.")
    print("     - Thuật toán equiripple tối ưu sai số cực đại giữa các dải.")
    print(f"     - Bậc ước lượng gần đúng: M ≈ {pm_order}.")
    print("  3) IIR Chebyshev Type I:")
    print("     - Chọn khi ưu tiên hiệu quả tính toán trên DSP fixed-point.")
    print("     - Chấp nhận pha phi tuyến để đổi lấy bậc thấp hơn FIR.")
    print(f"     - Với Rp = {rp_db:.1f} dB, Rs = {rs_db:.1f} dB => bậc tối thiểu N = {iir_order}.")
    print("  4) Notch 50 Hz:")
    print("     - Chọn vì nhiễu tập trung quanh đúng một tần số hẹp là 50 Hz.")
    print("     - Không cần low-pass hay high-pass vì sẽ làm mất thêm thành phần hữu ích không cần thiết.")

    return {
        "hamming_order": hamming_order,
        "pm_order":      pm_order,
        "iir_order":     iir_order,
        "critical":      critical,
        "rp_db":         rp_db,
        "rs_db":         rs_db,
        "delta1_db":     delta1_db,
        "delta2_db":     delta2_db,
    }


def tinh_tham_so(fs: float = 44100.0):
    """
    Tính các tham số thiết kế bộ lọc, bao gồm pre-warp biến đổi bilinear.

    Biến đổi bilinear ảnh xạ: s = (2/T) * tan(ω/2), cần pre-warp tần số
    thiết kế để bù tác động nén tần số (warping effect).
    """
    wp = 0.2 * np.pi   # Mép dải thông chuẩn hóa
    ws = 0.3 * np.pi   # Mép dải chặn chuẩn hóa
    t  = 1.0 / fs      # Chu kỳ lấy mẫu T (giây)
    # Pre-warp: biến tần số rời rạc ω sang tần số liên tục Ω tương đương
    # Công thức: Ω = (2/T) * tan(ω/2)  (rad/s)
    omega_p = (2 / t) * np.tan(wp / 2)   # Tần số liên tục dải thông (Ωp)
    omega_s = (2 / t) * np.tan(ws / 2)   # Tần số liên tục dải chặn (Ωs)
    # Quy đổi sang Hz để hiển thị
    fp      = wp * fs / (2 * np.pi)
    fs_edge = ws * fs / (2 * np.pi)

    print("\n" + "=" * 60)
    print("TÍNH TOÁN CÁC THAM SỐ BỘ LỌC")
    print("=" * 60)
    print(f"  - ωp = 0.2π rad/sample => fp = {fp:.1f} Hz")
    print(f"  - ωs = 0.3π rad/sample => fs = {fs_edge:.1f} Hz")
    print(f"  - Pre-warp Ωp = {omega_p:.2f} rad/s")
    print(f"  - Pre-warp Ωs = {omega_s:.2f} rad/s")
    print(f"  - Tần số Nyquist = {fs / 2:.1f} Hz")
    print(f"  - Miền dải thông chuẩn hóa = {wp / np.pi:.2f}")
    print(f"  - Miền dải chắn chuẩn hóa = {ws / np.pi:.2f}")
    print("  - Ý nghĩa: các tham số này là đầu vào trực tiếp cho thiết kế FIR/IIR trong SciPy và MATLAB.")

    return {
        "fp":      fp,
        "fs_edge": fs_edge,
        "omega_p": omega_p,
        "omega_s": omega_s,
        "nyquist": fs / 2,
    }


def chay_phan_tich_thiet_ke(fs: float = 44100.0):
    """
    Chạy toàn bộ phân tích thiết kế theo thứ tự: đầu vào → chọn lựa → tham số.
    Trả về dict chứa kết quả từ cả 3 bước.
    """
    input_result     = phan_tich_dau_vao(fs)                     # Bước 1: phân tích input
    choice_result    = giai_thich_lua_chon(fs, specs=input_result) # Bước 2: chọn lựa
    parameter_result = tinh_tham_so(fs)                          # Bước 3: tính tham số
    return {
        "input":      input_result,
        "choice":     choice_result,
        "parameters": parameter_result,
    }
