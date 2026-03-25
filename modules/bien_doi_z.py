from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import residuez

from .cau_hinh_do_thi import COLORS, build_save_path, finalize_figure


def zplane(
    b: np.ndarray,
    a: np.ndarray,
    title: str = "Z-Plane",
    show_plots: bool = True,
    save_path: str | None = None,
):
    zeros_z = np.roots(b)
    poles_z = np.roots(a)

    fig, ax = plt.subplots(figsize=(6, 6), tight_layout=True)
    fig.suptitle(title, fontsize=12, color=COLORS[4])

    theta = np.linspace(0, 2 * np.pi, 360)
    ax.plot(np.cos(theta), np.sin(theta), color="#6c7086", linewidth=1, label="Unit Circle")
    ax.axhline(0, color="#6c7086", linewidth=0.8)
    ax.axvline(0, color="#6c7086", linewidth=0.8)
    ax.scatter(zeros_z.real, zeros_z.imag, marker="o", s=100, facecolors="none", edgecolors=COLORS[1], linewidths=2, label=f"Zeros ({len(zeros_z)})")
    ax.scatter(poles_z.real, poles_z.imag, marker="x", s=100, color=COLORS[2], linewidths=2, label=f"Poles ({len(poles_z)})")
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.set_aspect("equal")
    ax.set_xlabel("Re(z)")
    ax.set_ylabel("Im(z)")
    ax.legend(facecolor="#2a2a3e")
    ax.grid(True)
    finalize_figure(fig, show_plots, save_path=save_path)

    stable = np.all(np.abs(poles_z) < 1.0)
    print(f"  Ổn định ({title}): {'✔ CÓ (tất cả cực nằm trong vòng tròn đơn vị)' if stable else '✘ KHÔNG'}")
    return zeros_z, poles_z


def demo_z_transform(show_plots: bool = True, save_dir: str | None = None):
    print("\n" + "=" * 60)
    print("CHƯƠNG 2: BIẾN ĐỔI Z – PHÂN TÍCH H(z)")
    print("=" * 60)

    b = np.array([1.0, 1.0])
    a = np.array([1.0, -0.5, 0.25])
    residues, poles, constant = residuez(b, a)

    print("  Hệ số phân tử  b:", b)
    print("  Hệ số mẫu số   a:", a)
    print(f"  Thặng dư  R = {residues}")
    print(f"  Cực       P = {poles}")
    print(f"  Hằng số   C = {constant}")

    zplane(
        b,
        a,
        title="Z-Plane – H(z) = (1+z⁻¹)/(1−0.5z⁻¹+0.25z⁻²)",
        show_plots=show_plots,
        save_path=build_save_path(save_dir, "04_zplane_hz.png"),
    )
    return {"b": b, "a": a, "residues": residues, "poles": poles, "constant": constant}
