from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt

COLORS = ["#89b4fa", "#a6e3a1", "#f38ba8", "#fab387", "#cba6f7", "#89dceb"]


def ap_dung_style_do_thi() -> None:
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


def tao_duong_dan_luu(save_dir: str | None, filename: str) -> str | None:
    if not save_dir:
        return None
    output_dir = Path(save_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    return str(output_dir / filename)


def hoan_thien_bieu_do(fig, show_plots: bool, save_path: str | None = None) -> None:
    if save_path:
        fig.savefig(save_path, dpi=220, bbox_inches="tight")
    if show_plots:
        plt.show()
    else:
        plt.close(fig)
