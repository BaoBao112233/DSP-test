from __future__ import annotations

import matplotlib.pyplot as plt

COLORS = ["#89b4fa", "#a6e3a1", "#f38ba8", "#fab387", "#cba6f7", "#89dceb"]


def apply_plot_style() -> None:
    plt.rcParams.update({
        "figure.facecolor": "#1e1e2e",
        "axes.facecolor": "#2a2a3e",
        "axes.edgecolor": "#cdd6f4",
        "axes.labelcolor": "#cdd6f4",
        "xtick.color": "#cdd6f4",
        "ytick.color": "#cdd6f4",
        "text.color": "#cdd6f4",
        "grid.color": "#45475a",
        "grid.linestyle": "--",
        "grid.alpha": 0.5,
        "lines.linewidth": 1.8,
        "font.size": 10,
    })


def finalize_figure(fig, show_plots: bool) -> None:
    if show_plots:
        plt.show()
    else:
        plt.close(fig)
