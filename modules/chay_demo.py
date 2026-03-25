from __future__ import annotations

import warnings

from .ung_dung import demo_hieu_ung_echo, demo_bo_loc_notch
from .so_sanh import so_sanh_fir_iir
from .phan_tich_thiet_ke import chay_phan_tich_thiet_ke
from .thiet_ke_fir import demo_bo_loc_fir
from .thiet_ke_iir import demo_bo_loc_iir
from .cau_hinh_do_thi import ap_dung_style_do_thi
from .demo_lay_mau import demo_qua_trinh_lay_mau
from .thaotac_tin_hieu import demo_thaotac_tin_hieu
from .bien_doi_z import demo_phan_tich_z

warnings.filterwarnings("ignore")


def chay_toan_bo(show_plots: bool = True, save_dir: str | None = None):
    ap_dung_style_do_thi()

    print("╔══════════════════════════════════════════════════════════╗")
    print("║  THIẾT KẾ & PHÂN TÍCH BỘ LỌC SỐ CHO TÍN HIỆU ÂM THANH ║")
    print("║  Python / SciPy – Mô phỏng MATLAB                       ║")
    print("╚══════════════════════════════════════════════════════════╝")

    sampling_result = demo_qua_trinh_lay_mau(show_plots=show_plots, save_dir=save_dir)
    analysis_result = chay_phan_tich_thiet_ke()
    signal_ops_result = demo_thaotac_tin_hieu(show_plots=show_plots, save_dir=save_dir)
    z_result = demo_phan_tich_z(show_plots=show_plots, save_dir=save_dir)
    fir_result = demo_bo_loc_fir(show_plots=show_plots, save_dir=save_dir)
    iir_result = demo_bo_loc_iir(show_plots=show_plots, save_dir=save_dir)
    comparison_result = so_sanh_fir_iir(
        fir_result["h_pm"],
        iir_result["b"],
        iir_result["a"],
        fs=fir_result["fs"],
        show_plots=show_plots,
        save_dir=save_dir,
    )
    notch_result = demo_bo_loc_notch(show_plots=show_plots, save_dir=save_dir)
    echo_result = demo_hieu_ung_echo(show_plots=show_plots, save_dir=save_dir)

    print("\n✔  Hoàn thành toàn bộ mô phỏng.")
    return {
        "sampling": sampling_result,
        "analysis": analysis_result,
        "signal_ops": signal_ops_result,
        "z": z_result,
        "fir": fir_result,
        "iir": iir_result,
        "comparison": comparison_result,
        "notch": notch_result,
        "echo": echo_result,
        "save_dir": save_dir,
    }
