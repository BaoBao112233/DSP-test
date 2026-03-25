from __future__ import annotations

import numpy as np
from scipy import signal


def phan_tich_dau_vao(fs: float = 44100.0):
    wp = 0.2 * np.pi
    ws = 0.3 * np.pi
    fp = wp * fs / (2 * np.pi)
    fs_edge = ws * fs / (2 * np.pi)
    transition_hz = fs_edge - fp

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
    if specs is None:
        specs = phan_tich_dau_vao(fs)
    wp = specs["wp"]
    ws = specs["ws"]
    delta_w = ws - wp

    hamming_order = int(np.ceil(6.6 * np.pi / delta_w))
    if hamming_order % 2 != 0:
        hamming_order += 1

    rp_db = 1.0
    rs_db = 15.0
    iir_order, critical = signal.cheb1ord(wp / np.pi, ws / np.pi, rp_db, rs_db)

    delta1_db = 0.5
    delta2_db = 40.0
    delta1 = (10 ** (delta1_db / 20) - 1) / (10 ** (delta1_db / 20) + 1)
    delta2 = 10 ** (-delta2_db / 20)
    delta = min(delta1, delta2)
    d_value = (-20 * np.log10(delta) - 13) / 14.6
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
        "pm_order": pm_order,
        "iir_order": iir_order,
        "critical": critical,
        "rp_db": rp_db,
        "rs_db": rs_db,
        "delta1_db": delta1_db,
        "delta2_db": delta2_db,
    }


def tinh_tham_so(fs: float = 44100.0):
    wp = 0.2 * np.pi
    ws = 0.3 * np.pi
    t = 1.0 / fs
    omega_p = (2 / t) * np.tan(wp / 2)
    omega_s = (2 / t) * np.tan(ws / 2)
    fp = wp * fs / (2 * np.pi)
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
        "fp": fp,
        "fs_edge": fs_edge,
        "omega_p": omega_p,
        "omega_s": omega_s,
        "nyquist": fs / 2,
    }


def chay_phan_tich_thiet_ke(fs: float = 44100.0):
    input_result = phan_tich_dau_vao(fs)
    choice_result = giai_thich_lua_chon(fs, specs=input_result)
    parameter_result = tinh_tham_so(fs)
    return {
        "input": input_result,
        "choice": choice_result,
        "parameters": parameter_result,
    }
