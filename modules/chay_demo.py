"""
chay_demo.py – Module điều phối (orchestrator) toàn bộ luồng mô phỏng.

Hàm chay_toan_bo() là điểm vào duy nhất được xuất ra ngoài qua __init__.py.
Nó gọi 9 demo theo thứ tự logic của báo cáo:
  1. Lấy mẫu & Nyquist       (demo_qua_trinh_lay_mau)
  2. Phân tích thiết kế       (chay_phan_tich_thiet_ke)
  3. Thao tác tín hiệu rời rạc (demo_thaotac_tin_hieu)
  4. Biến đổi Z               (demo_phan_tich_z)
  5. Thiết kế FIR             (demo_bo_loc_fir)
  6. Thiết kế IIR             (demo_bo_loc_iir)
  7. So sánh FIR vs IIR       (so_sanh_fir_iir)
  8. Bộ lọc Notch 50 Hz       (demo_bo_loc_notch)
  9. Mô phỏng Echo            (demo_hieu_ung_echo)
"""

from __future__ import annotations  # Hỗ trợ type hint mới trên Python cũ

import warnings  # Tắt cảnh báo SciPy không liên quan khi chạy demo

# Import từng module demo – mỗi module = một chương giáo trình
from .ung_dung import demo_hieu_ung_echo, demo_bo_loc_notch
from .so_sanh import so_sanh_fir_iir
from .phan_tich_thiet_ke import chay_phan_tich_thiet_ke
from .thiet_ke_fir import demo_bo_loc_fir
from .thiet_ke_iir import demo_bo_loc_iir
from .cau_hinh_do_thi import ap_dung_style_do_thi   # Khởi tạo theme đồ thị
from .demo_lay_mau import demo_qua_trinh_lay_mau
from .thaotac_tin_hieu import demo_thaotac_tin_hieu
from .bien_doi_z import demo_phan_tich_z

# Bỏ qua các FutureWarning/DeprecationWarning không liên quan đến logic
warnings.filterwarnings("ignore")


def chay_toan_bo(show_plots: bool = True, save_dir: str | None = None):
    """
    Chạy toàn bộ 9 demo theo thứ tự và trả về dict kết quả.

    Tham số:
        show_plots: True = mở cửa sổ đồ thị tương tác.
        save_dir:   Thư mục lưu file PNG, hoặc None để không lưu.

    Trả về:
        dict chứa kết quả từ tất cả 9 demo để kiểm tra sau.
    """
    # Áp dụng theme Catppuccin Mocha TRƯỚC KHI vẽ bất kỳ biểu đồ nào
    ap_dung_style_do_thi()

    print("╔══════════════════════════════════════════════════════════╗")
    print("║  THIẾT KẾ & PHÂN TÍCH BỘ LỌC SỐ CHO TÍN HIỆU ÂM THANH ║")
    print("║  Python / SciPy – Mô phỏng MATLAB                       ║")
    print("╚══════════════════════════════════════════════════════════╝")

    # --- Chương 1: Lấy mẫu, Định lý Nyquist-Shannon ---
    sampling_result = demo_qua_trinh_lay_mau(show_plots=show_plots, save_dir=save_dir)

    # --- Chương 2: Phân tích thiết kế (chỉ console, không vẽ) ---
    analysis_result = chay_phan_tich_thiet_ke()

    # --- Chương 3: Thao tác tín hiệu rời rạc (dịch, gấp, cộng) ---
    signal_ops_result = demo_thaotac_tin_hieu(show_plots=show_plots, save_dir=save_dir)

    # --- Chương 4: Biến đổi Z, phân tích H(z) ---
    z_result = demo_phan_tich_z(show_plots=show_plots, save_dir=save_dir)

    # --- Chương 5: Thiết kế bộ lọc FIR (Hamming + Parks-McClellan) ---
    fir_result = demo_bo_loc_fir(show_plots=show_plots, save_dir=save_dir)

    # --- Chương 6: Thiết kế bộ lọc IIR (Chebyshev Type I + bilinear) ---
    iir_result = demo_bo_loc_iir(show_plots=show_plots, save_dir=save_dir)

    # --- Chương 7: So sánh FIR vs IIR (dùng kết quả từ 2 chương trên) ---
    comparison_result = so_sanh_fir_iir(
        fir_result["h_pm"],    # FIR Parks-McClellan (bậc nhỏ hơn Hamming)
        iir_result["b"],
        iir_result["a"],
        fs=fir_result["fs"],
        show_plots=show_plots,
        save_dir=save_dir,
    )

    # --- Chương 8 (Bổ sung): Bộ lọc Notch 50 Hz ---
    notch_result = demo_bo_loc_notch(show_plots=show_plots, save_dir=save_dir)

    # --- Chương 9 (Bổ sung): Mô phỏng hiệu ứng Echo ---
    echo_result = demo_hieu_ung_echo(show_plots=show_plots, save_dir=save_dir)

    print("\n✔  Hoàn thành toàn bộ mô phỏng.")
    # Trả về tất cả kết quả để bo_loc_am_thanh_so.py có thể kiểm tra nếu cần
    return {
        "sampling":   sampling_result,
        "analysis":   analysis_result,
        "signal_ops": signal_ops_result,
        "z":          z_result,
        "fir":        fir_result,
        "iir":        iir_result,
        "comparison": comparison_result,
        "notch":      notch_result,
        "echo":       echo_result,
        "save_dir":   save_dir,
    }
