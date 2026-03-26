"""
bo_loc_am_thanh_so.py – Điểm vào chính (entry point) của toàn bộ chương trình.

Cách chạy:
    python bo_loc_am_thanh_so.py                         # Hiển thị tất cả biểu đồ
    python bo_loc_am_thanh_so.py --no-plots              # Chạy không mở biểu đồ (headless)
    python bo_loc_am_thanh_so.py --save-plots-dir imgaes/v3  # Lưu biểu đồ ra thư mục
"""

from __future__ import annotations  # Cho phép dùng cú pháp type-hint mới trên Python cũ

import argparse  # Thư viện chuẩn để phân tích tham số dòng lệnh (CLI)

from modules import chay_toan_bo  # Import hàm điều phối chính từ package modules


def phan_tich_tham_so() -> argparse.Namespace:
    """
    Phân tích tham số dòng lệnh mà người dùng truyền vào khi chạy script.

    Trả về:
        argparse.Namespace: object chứa giá trị các tham số đã phân tích.
            - no_plots (bool): True nếu người dùng truyền --no-plots
            - save_plots_dir (str | None): đường dẫn thư mục lưu ảnh, hoặc None
    """
    # Tạo parser với mô tả ngắn gọn hiển thị khi dùng --help
    parser = argparse.ArgumentParser(
        description="Mô phỏng xử lý tín hiệu âm thanh theo tài liệu MATLAB bằng Python.",
    )

    # Tham số cờ (flag): nếu có --no-plots thì args.no_plots = True
    # Dùng khi chạy trên server không có GUI hoặc khi chạy CI/CD pipeline
    parser.add_argument(
        "--no-plots",
        action="store_true",  # Không cần giá trị đi kèm, chỉ cần có mặt là True
        help="Không hiển thị biểu đồ matplotlib, phù hợp khi chạy kiểm thử hoặc debug headless.",
    )

    # Tham số chuỗi tùy chọn: nếu không truyền thì mặc định là None (không lưu)
    parser.add_argument(
        "--save-plots-dir",
        type=str,  # Giá trị nhận vào là chuỗi ký tự (đường dẫn thư mục)
        default=None,  # Mặc định: không lưu ảnh
        help="Thư mục lưu toàn bộ ảnh biểu đồ (ví dụ: imgaes/v3).",
    )

    return parser.parse_args()  # Thực hiện phân tích và trả về Namespace


def main() -> None:
    """
    Hàm chính: đọc tham số CLI rồi khởi động toàn bộ chuỗi mô phỏng.
    """
    args = phan_tich_tham_so()  # Lấy tham số từ dòng lệnh

    # Gọi hàm chạy toàn bộ mô phỏng:
    #   show_plots = True nếu KHÔNG có cờ --no-plots (nghĩa là muốn xem biểu đồ)
    #   save_dir   = đường dẫn thư mục lưu ảnh hoặc None
    chay_toan_bo(show_plots=not args.no_plots, save_dir=args.save_plots_dir)


# Chỉ chạy main() khi script được thực thi trực tiếp,
# không chạy nếu file được import từ module khác
if __name__ == "__main__":
    main()
