from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt

from .plot_config import COLORS, finalize_figure


def sigshift(x: np.ndarray, n: np.ndarray, d: int):
    return x.copy(), n + d


def sigfold(x: np.ndarray, n: np.ndarray):
    return x[::-1].copy(), -n[::-1].copy()


def sigadd(x1: np.ndarray, n1: np.ndarray, x2: np.ndarray, n2: np.ndarray):
    n_start = min(n1[0], n2[0])
    n_stop = max(n1[-1], n2[-1])
    n_out = np.arange(n_start, n_stop + 1)

    y1 = np.zeros(len(n_out))
    y2 = np.zeros(len(n_out))
    y1[n1[0] - n_start:n1[-1] - n_start + 1] = x1
    y2[n2[0] - n_start:n2[-1] - n_start + 1] = x2
    return y1 + y2, n_out


def energy(x: np.ndarray) -> float:
    return float(np.sum(np.abs(x) ** 2))


def demo_signal_ops(show_plots: bool = True):
    n = np.arange(-5, 6)
    x = np.array([0, 0, 0, 1, 2, 3, 2, 1, 0, 0, 0], dtype=float)

    _, n_shifted = sigshift(x, n, 3)
    x_folded, n_folded = sigfold(x, n)
    x_added, n_added = sigadd(x, n, x_folded, n_folded)

    print("=" * 60)
    print("CHƯƠNG 1: THAO TÁC TÍN HIỆU RỜI RẠC")
    print("=" * 60)
    print(f"  Năng lượng x(n)  : E = {energy(x):.2f}")
    print(f"  Sau dịch  d=3    : n_shift = {n_shifted}")
    print(f"  Sau gấp          : n_fold  = {n_folded}")

    fig, axes = plt.subplots(3, 1, figsize=(10, 7), tight_layout=True)
    fig.suptitle("Chương 1 – Thao tác tín hiệu rời rạc", fontsize=13, color=COLORS[4])

    for ax, data in zip(
        axes,
        [
            (x, n, "x(n) – Tín hiệu gốc", COLORS[0]),
            (x, n_shifted, "x(n-3) – Dịch phải 3 mẫu", COLORS[1]),
            (x_added, n_added, "x(n)+x(-n) – Cộng dãy gấp", COLORS[3]),
        ],
    ):
        samples, index, title, color = data
        ax.stem(index, samples, linefmt=color, markerfmt="o", basefmt="white")
        ax.set_title(title)
        ax.set_xlabel("n")
        ax.set_ylabel("Biên độ")
        ax.grid(True)

    finalize_figure(fig, show_plots)
    return {"x": x, "n": n, "x_added": x_added, "n_added": n_added}
