from __future__ import annotations

import warnings

from .ung_dung import demo_echo, demo_notch
from .so_sanh import compare_fir_iir
from .phan_tich_thiet_ke import run_design_analysis
from .thiet_ke_fir import demo_fir
from .thiet_ke_iir import demo_iir
from .cau_hinh_do_thi import apply_plot_style
from .demo_lay_mau import demo_sampling
from .thaotac_tin_hieu import demo_signal_ops
from .bien_doi_z import demo_z_transform

warnings.filterwarnings("ignore")


def run_all(show_plots: bool = True, save_dir: str | None = None):
    apply_plot_style()

    print("╔══════════════════════════════════════════════════════════╗")
    print("║  THIẾT KẾ & PHÂN TÍCH BỘ LỌC SỐ CHO TÍN HIỆU ÂM THANH ║")
    print("║  Python / SciPy – Mô phỏng MATLAB                       ║")
    print("╚══════════════════════════════════════════════════════════╝")

    sampling_result = demo_sampling(show_plots=show_plots, save_dir=save_dir)
    analysis_result = run_design_analysis()
    signal_ops_result = demo_signal_ops(show_plots=show_plots, save_dir=save_dir)
    z_result = demo_z_transform(show_plots=show_plots, save_dir=save_dir)
    fir_result = demo_fir(show_plots=show_plots, save_dir=save_dir)
    iir_result = demo_iir(show_plots=show_plots, save_dir=save_dir)
    comparison_result = compare_fir_iir(
        fir_result["h_pm"],
        iir_result["b"],
        iir_result["a"],
        fs=fir_result["fs"],
        show_plots=show_plots,
        save_dir=save_dir,
    )
    notch_result = demo_notch(show_plots=show_plots, save_dir=save_dir)
    echo_result = demo_echo(show_plots=show_plots, save_dir=save_dir)

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
