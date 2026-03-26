"""
modules/__init__.py – Khai báo public API của package modules.

Khi người dùng viết: from modules import chay_toan_bo
Python sẽ tìm chay_toan_bo trong file này đầu tiên.
__all__ quy định danh sách tên được export khi dùng: from modules import *
"""

# Import hàm điều phối chính từ file chay_demo.py trong cùng package
from .chay_demo import chay_toan_bo

# Danh sách tên public của package – chỉ export chay_toan_bo ra ngoài
__all__ = ["chay_toan_bo"]
