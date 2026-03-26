"""
bien_doi_z.py – Biến đổi Z và phân tích hàm hệ thống H(z) trong miền z.

Biến đổi Z là công cụ phân tích tín hiệu rời rạc trong miền tần số phức:
  - Vẽ mặt phẳng Z: vị trí cực (poles) và không (zeros)
  - Bộ lọc ổn định khi tất cả cực nằm bên trong vòng tròn đơn vị
  - Phân tích phần phân (partial fraction) để tìm hàm x[n]
"""

from __future__ import annotations  # Hỗ trợ type hint mới trên Python cũ

import numpy as np            # Tính toán số mảng, tìm nghiệm đa thức
import matplotlib.pyplot as plt  # Vẽ biểu đồ mặt phẳng Z
from scipy.signal import residuez  # Hàm phân tích phần phân cho biến đổi Z

# Import tiện ích đồ thị từ module cấu hình chung
from .cau_hinh_do_thi import COLORS, tao_duong_dan_luu, hoan_thien_bieu_do


def ve_mat_phang_z(
    b: np.ndarray,
    a: np.ndarray,
    title: str = "Z-Plane",
    show_plots: bool = True,
    save_path: str | None = None,
):
    """
    Vẽ mặt phẳng Z với vòng tròn đơn vị, cực và không của bộ lọc H(z).

    Tham số:
        b:          Hệ số tử số của H(z).
        a:          Hệ số mẫu số của H(z).
        title:      Tiêu đề biểu đồ.
        show_plots: Hiển thị cửa sổ biểu đồ hay không.
        save_path:  Đường dẫn PNG để lưu, hoặc None.

    Trả về:
        (zeros_z, poles_z): vị trí không và cực trên mặt phẳng số phức.
    """
    zeros_z = np.roots(b)  # Giải đa thức tử số → tìm số 0 (zeros)
    poles_z = np.roots(a)  # Giải đa thức mẫu số → tìm cực (poles)

    fig, ax = plt.subplots(figsize=(6, 6), tight_layout=True)
    fig.suptitle(title, fontsize=12, color=COLORS[4])

    # Vẽ vòng tròn đơn vị: tập hợp {z : |z| = 1} trên mặt phẳng phức
    theta = np.linspace(0, 2 * np.pi, 360)  # 360 góc từ 0 đến 2π
    ax.plot(np.cos(theta), np.sin(theta), color="#6c7086", linewidth=1, label="Unit Circle")

    # Vẽ hai trục tọa độ Re(z) và Im(z)
    ax.axhline(0, color="#6c7086", linewidth=0.8)
    ax.axvline(0, color="#6c7086", linewidth=0.8)

    # Vẽ bằng các ký hiệu chuẩn: 'o' = zero, 'x' = pole
    ax.scatter(zeros_z.real, zeros_z.imag, marker="o", s=100, facecolors="none", edgecolors=COLORS[1], linewidths=2, label=f"Zeros ({len(zeros_z)})")
    ax.scatter(poles_z.real, poles_z.imag, marker="x", s=100, color=COLORS[2], linewidths=2, label=f"Poles ({len(poles_z)})")

    # Giới hạn trục để có khoảng mức ngoài vòng tròn rõ hơn
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.set_aspect("equal")  # Đảm bảo vòng tròn không bị méo thành elip
    ax.set_xlabel("Re(z)")
    ax.set_ylabel("Im(z)")
    ax.legend(facecolor="#2a2a3e")
    ax.grid(True)
    hoan_thien_bieu_do(fig, show_plots, save_path=save_path)

    # Kiểm tra ổn định: bộ lọc ổn định ⟺ tất cả cực nằm bên trong |z| = 1
    stable = np.all(np.abs(poles_z) < 1.0)
    print(f"  Ổn định ({title}): {'✔ CÓ (tất cả cực nằm trong vòng tròn đơn vị)' if stable else '✘ KHÔNG'}")
    return zeros_z, poles_z


def demo_phan_tich_z(show_plots: bool = True, save_dir: str | None = None):
    """
    Demo Chương 3: Biến đổi Z – phân tích hàm hệ thống H(z).

    H(z) = (1 + z^{-1}) / (1 - 0.5 z^{-1} + 0.25 z^{-2})
    Thực hiện phân tích phần phân (partial fraction) để biết
    cách khôi phục h[n] = Z^{-1}[H(z)].
    """
    print("\n" + "=" * 60)
    print("CHƯƠNG 3: BIẾN ĐỔI Z – PHÂN TÍCH H(z)")
    print("=" * 60)

    # Hệ số b (tử số): tương ứng 1 + z^{-1}  → [1, 1]
    b = np.array([1.0, 1.0])
    # Hệ số a (mẫu số): tương ứng 1 - 0.5z^{-1} + 0.25z^{-2}  → [1, -0.5, 0.25]
    a = np.array([1.0, -0.5, 0.25])

    # Phân tích phần phân (partial fraction expansion) của H(z)/z
    # Kết quả: H(z) = R[0]/(1-P[0]z^{-1}) + R[1]/(1-P[1]z^{-1}) + C
    residues, poles, constant = residuez(b, a)

    print("  Hệ số phân tử  b:", b)
    print("  Hệ số mẫu số   a:", a)
    print(f"  Thặng dư  R = {residues}")
    print(f"  Cực       P = {poles}")
    print(f"  Hằng số   C = {constant}")

    # Vẽ mặt phẳng Z và kiểm tra ổn định
    ve_mat_phang_z(
        b,
        a,
        title="Z-Plane – H(z) = (1+z⁻¹)/(1−0.5z⁻¹+0.25z⁻²)",
        show_plots=show_plots,
        save_path=tao_duong_dan_luu(save_dir, "04_zplane_hz.png"),
    )
    return {"b": b, "a": a, "residues": residues, "poles": poles, "constant": constant}
