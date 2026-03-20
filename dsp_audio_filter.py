"""Điểm vào chính cho mô phỏng DSP âm thanh."""

from __future__ import annotations

import argparse

from modules import run_all


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Mô phỏng xử lý tín hiệu âm thanh theo tài liệu MATLAB bằng Python.",
    )
    parser.add_argument(
        "--no-plots",
        action="store_true",
        help="Không hiển thị biểu đồ matplotlib, phù hợp khi chạy kiểm thử hoặc debug headless.",
    )
    parser.add_argument(
        "--save-plots-dir",
        type=str,
        default=None,
        help="Thư mục lưu toàn bộ ảnh biểu đồ (ví dụ: imgaes/v3).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_all(show_plots=not args.no_plots, save_dir=args.save_plots_dir)


if __name__ == "__main__":
    main()
