# HƯỚNG DẪN DỰ ÁN – THIẾT KẾ & PHÂN TÍCH BỘ LỌC SỐ CHO TÍN HIỆU ÂM THANH

> **Ngôn ngữ:** Python 3.10+  
> **Thư viện:** NumPy, SciPy, Matplotlib  
> **Cập nhật lần cuối:** 25/03/2026

---

## MỤC LỤC

1. [Cấu trúc thư mục](#1-cấu-trúc-thư-mục)
2. [Tổng quan dự án](#2-tổng-quan-dự-án)
3. [Hướng dẫn chạy chương trình](#3-hướng-dẫn-chạy-chương-trình)
4. [Mô tả chi tiết từng file và các hàm](#4-mô-tả-chi-tiết-từng-file-và-các-hàm)
5. [Sơ đồ phụ thuộc module](#5-sơ-đồ-phụ-thuộc-module)

---

## 1. CẤU TRÚC THƯ MỤC

```
DSP-test/
├── bo_loc_am_thanh_so.py          ← Điểm vào chính (main entry point)
├── requirements.txt               ← Danh sách thư viện
├── HUONG_DAN.md                   ← File hướng dẫn này
│
└── modules/
    ├── __init__.py                ← Khai báo gói & export công khai
    ├── cau_hinh_do_thi.py         ← Cấu hình màu sắc và phong cách biểu đồ
    ├── thaotac_tin_hieu.py        ← Thao tác cơ bản trên tín hiệu rời rạc
    ├── demo_lay_mau.py            ← Mô phỏng lấy mẫu & định lý Nyquist
    ├── bien_doi_z.py              ← Phân tích biến đổi Z, mặt phẳng Z
    ├── phan_tich_thiet_ke.py      ← Phân tích đặc tả & lý do chọn bộ lọc
    ├── thiet_ke_fir.py            ← Thiết kế bộ lọc FIR (Hamming, Parks-McClellan)
    ├── thiet_ke_iir.py            ← Thiết kế bộ lọc IIR (Chebyshev Type I, Bilinear)
    ├── so_sanh.py                 ← So sánh FIR vs IIR (Group Delay, Biên độ)
    ├── ung_dung.py                ← Ứng dụng thực tế: Notch 50Hz, mô phỏng Echo
    └── chay_demo.py               ← Điều phối toàn bộ luồng demo từ chương 1→9
```

---

## 2. TỔNG QUAN DỰ ÁN

Dự án mô phỏng toàn bộ quy trình **Xử lý Tín hiệu Số (DSP)** áp dụng cho tín hiệu âm thanh, bao gồm:

| Chương | Nội dung |
|--------|----------|
| Chương 1 | Thao tác tín hiệu rời rạc: dịch, gấp, cộng |
| Chương 2 | Biến đổi Z, phân rã phân số riêng phần, mặt phẳng Z |
| Chương 3 | Thiết kế bộ lọc FIR: cửa sổ Hamming & thuật toán Parks-McClellan |
| Chương 4 | Thiết kế bộ lọc IIR: Chebyshev Type I qua biến đổi Bilinear |
| Chương 5 | Kiểm tra tính ổn định, mặt phẳng Z của IIR |
| Chương 6 | Phân tích & lựa chọn bộ lọc phù hợp với đặc tả |
| Chương 7 | So sánh FIR vs IIR: Biên độ, Pha, Group Delay |
| Bổ sung | Bộ lọc Notch 50 Hz loại bỏ nhiễu điện lưới |
| Bổ sung | Mô phỏng hiệu ứng Echo theo Lab-Volt TMS320C50 |

---

## 3. HƯỚNG DẪN CHẠY CHƯƠNG TRÌNH

### Cài đặt môi trường

```bash
# Tạo virtual environment (nếu chưa có)
python -m venv .venv
source .venv/bin/activate

# Cài đặt thư viện
pip install -r requirements.txt
```

### Chạy toàn bộ mô phỏng

```bash
# Chạy và hiển thị tất cả biểu đồ
.venv/bin/python bo_loc_am_thanh_so.py

# Chạy không hiển thị biểu đồ (headless / CI)
.venv/bin/python bo_loc_am_thanh_so.py --no-plots

# Chạy và lưu tất cả biểu đồ vào thư mục imgaes/v3/
.venv/bin/python bo_loc_am_thanh_so.py --save-plots-dir imgaes/v3
```

---

## 4. MÔ TẢ CHI TIẾT TỪNG FILE VÀ CÁC HÀM

---

### `bo_loc_am_thanh_so.py` — Điểm vào chính

**Mục đích:** File thực thi chính của toàn bộ dự án. Phân tích tham số dòng lệnh rồi khởi chạy chuỗi demo.

| Hàm | Chữ ký | Mô tả |
|-----|--------|-------|
| `parse_args` | `() → Namespace` | Phân tích tham số dòng lệnh: `--no-plots` và `--save-plots-dir` |
| `main` | `() → None` | Hàm main: gọi `parse_args()` rồi chuyển tham số vào `run_all()` |

---

### `modules/__init__.py` — Khai báo gói

**Mục đích:** Xuất API công khai duy nhất của package `modules`.

| Export | Nguồn | Mô tả |
|--------|-------|-------|
| `run_all` | `chay_demo` | Hàm duy nhất được xuất ra ngoài để chạy toàn bộ |

---

### `modules/cau_hinh_do_thi.py` — Cấu hình biểu đồ

**Mục đích:** Định nghĩa bảng màu tối (Catppuccin Mocha), cấu hình toàn cục cho Matplotlib, và các hàm tiện ích lưu/hiển thị biểu đồ.

| Hàm / Hằng | Chữ ký | Mô tả |
|------------|--------|-------|
| `COLORS` | `list[str]` | Bảng 6 màu hex theo theme Catppuccin Mocha (xanh, xanh lá, đỏ, cam, tím, cyan) |
| `apply_plot_style` | `() → None` | Áp dụng theme tối lên toàn bộ biểu đồ Matplotlib thông qua `rcParams` |
| `build_save_path` | `(save_dir, filename) → str \| None` | Tạo đường dẫn lưu file ảnh; tự tạo thư mục nếu chưa tồn tại; trả về `None` nếu `save_dir` là `None` |
| `finalize_figure` | `(fig, show_plots, save_path) → None` | Lưu biểu đồ ra file nếu có `save_path`, hiển thị hoặc đóng tùy `show_plots` |

---

### `modules/thaotac_tin_hieu.py` — Thao tác tín hiệu rời rạc

**Mục đích:** Cài đặt các phép toán cơ bản trên dãy tín hiệu rời rạc theo ký hiệu MATLAB: dịch, gấp, cộng, tính năng lượng. Tương ứng **Chương 1** của báo cáo.

| Hàm | Chữ ký | Mô tả |
|-----|--------|-------|
| `sigshift` | `(x, n, d) → (x, n+d)` | Dịch dãy tín hiệu `x[n]` sang phải `d` mẫu; trả về bản sao `x` và trục thời gian mới |
| `sigfold` | `(x, n) → (x[-1::-1], -n[-1::-1])` | Gấp (đảo chiều) dãy tín hiệu theo trục $n = 0$; tương đương $x(-n)$ |
| `sigadd` | `(x1, n1, x2, n2) → (y, n_out)` | Cộng hai dãy tín hiệu có thể có miền thời gian khác nhau; tự động căn chỉnh và zero-pad |
| `energy` | `(x) → float` | Tính năng lượng $E = \sum |x[n]|^2$ |
| `demo_signal_ops` | `(show_plots, save_dir) → dict` | Demo tổng hợp: tạo tín hiệu mẫu, thực hiện dịch/gấp/cộng, in kết quả và vẽ 3 biểu đồ stem; lưu `03_signal_ops_discrete.png` |

---

### `modules/demo_lay_mau.py` — Mô phỏng lấy mẫu & định lý Nyquist

**Mục đích:** Mô phỏng quá trình rời rạc hóa tín hiệu liên tục, kiểm tra điều kiện Nyquist-Shannon, minh họa hiện tượng aliasing. Tương ứng phần đầu báo cáo (lấy mẫu).

| Hàm | Chữ ký | Mô tả |
|-----|--------|-------|
| `generate_original_signal` | `(time_axis) → ndarray` | Tạo tín hiệu gốc liên tục giả lập gồm 3 thành phần sin: 440 Hz, 1000 Hz, 3000 Hz với biên độ khác nhau |
| `sample_signal` | `(fs, duration) → dict` | Lấy mẫu đều tín hiệu theo $x[n] = x(nT_s)$; trả về dict chứa trục thời gian liên tục và rời rạc, tín hiệu, và các tham số mô phỏng |
| `analyze_nyquist` | `(fs, f_max) → dict` | Kiểm tra điều kiện Nyquist-Shannon $F_s \geq 2f_{max}$; trả về kết quả `satisfied` cùng tần số Nyquist |
| `compute_spectrum` | `(x, fs) → (freq_axis, spectrum)` | Tính phổ biên độ qua FFT nhanh (rfft); trả về trục tần số và giá trị $|X(f)|$ |
| `alias_frequency` | `(f_signal, fs) → float` | Tính tần số alias khi lấy mẫu sai: ánh xạ tần số thực về miền $[0, F_s/2]$ |
| `demo_sampling` | `(show_plots, fs, duration, save_dir) → dict` | Demo tổng hợp: so sánh lấy mẫu đúng (44.1 kHz) và sai Nyquist (4 kHz); vẽ miền thời gian (`01_sampling_time_domain.png`) và miền tần số (`02_sampling_fft_aliasing.png`) |

---

### `modules/bien_doi_z.py` — Biến đổi Z & mặt phẳng Z

**Mục đích:** Thực hiện phân tích biến đổi Z: phân rã phân số riêng phần, vẽ mặt phẳng Z (zero-pole plot), kiểm tra tính ổn định. Tương ứng **Chương 2**.

| Hàm | Chữ ký | Mô tả |
|-----|--------|-------|
| `zplane` | `(b, a, title, show_plots, save_path) → (zeros, poles)` | Vẽ sơ đồ mặt phẳng Z: vẽ vòng tròn đơn vị, đánh dấu zero (○) và pole (×); in kết luận ổn định; trả về mảng zeros và poles |
| `demo_z_transform` | `(show_plots, save_dir) → dict` | Demo biến đổi Z cho $H(z) = (1+z^{-1})/(1-0.5z^{-1}+0.25z^{-2})$: tính phân rã thặng dư qua `residuez`, vẽ mặt phẳng Z (`04_zplane_hz.png`), in thặng dư R, cực P, hằng số C |

---

### `modules/phan_tich_thiet_ke.py` — Phân tích thiết kế bộ lọc

**Mục đích:** Tính toán đặc tả bộ lọc từ yêu cầu kỹ thuật, giải thích lý do chọn từng loại bộ lọc, tính toán tham số pre-warp cho biến đổi Bilinear. Tương ứng phần phân tích lựa chọn trong báo cáo.

| Hàm | Chữ ký | Mô tả |
|-----|--------|-------|
| `analyze_input_signals` | `(fs) → dict` | Chuyển đổi tần số chuẩn hóa ($\omega_p = 0.2\pi$, $\omega_s = 0.3\pi$) sang Hz thực; tính bề rộng dải chuyển tiếp; in phân tích tín hiệu đầu vào cho bài toán low-pass và notch |
| `explain_filter_choices` | `(fs, specs) → dict` | Tra công thức tính bậc lọc cho cả 3 loại (Hamming, Parks-McClellan, Chebyshev); in giải thích lý do kỹ thuật khi chọn từng loại bộ lọc |
| `calculate_filter_parameters` | `(fs) → dict` | Tính tham số pre-warp bilinear $\Omega_P$, $\Omega_S$; in bảng tóm tắt tần số Nyquist và miền chuẩn hóa |
| `run_design_analysis` | `(fs) → dict` | Hàm tổng hợp: gọi tuần tự `analyze_input_signals` → `explain_filter_choices` → `calculate_filter_parameters`; trả về dict gộp kết quả cả 3 hàm |

---

### `modules/thiet_ke_fir.py` — Thiết kế bộ lọc FIR

**Mục đích:** Thiết kế và phân tích bộ lọc FIR bằng hai phương pháp: cửa sổ Hamming và thuật toán Parks-McClellan (equiripple tối ưu). Tương ứng **Chương 3**.

| Hàm | Chữ ký | Mô tả |
|-----|--------|-------|
| `design_fir_hamming` | `(wp_rad, ws_rad) → ndarray` | Thiết kế FIR bằng cửa sổ Hamming: tính bậc $M = \lceil 6.6\pi/\Delta\omega \rceil$, đặt tần số cắt tại trung điểm dải chuyển tiếp; in bậc và số hệ số |
| `design_fir_pm` | `(wp_rad, ws_rad, delta1_db, delta2_db) → ndarray` | Thiết kế FIR Parks-McClellan (Remez): ước tính bậc theo công thức delta, gọi `remez()` với trọng số ripple; in bậc và số hệ số |
| `plot_fir_response` | `(h_hamming, h_pm, fs, show_plots, save_path) → None` | Vẽ lưới 2×2: biên độ (dB) và pha (độ) cho cả Hamming và Parks-McClellan; lưu `05_fir_hamming_vs_pm.png` |
| `demo_fir` | `(fs, show_plots, save_dir) → dict` | Demo tổng hợp **Chương 3**: thiết kế cả hai bộ lọc FIR, in tham số, gọi `plot_fir_response`; trả về `{h_hamming, h_pm, wp, ws, fs}` |

---

### `modules/thiet_ke_iir.py` — Thiết kế bộ lọc IIR

**Mục đích:** Thiết kế bộ lọc IIR Chebyshev Type I low-pass thông qua biến đổi Bilinear từ miền tương tự sang số. Phân tích đáp ứng tần số, pha, group delay, và mặt phẳng Z. Tương ứng **Chương 4 & 5**.

| Hàm | Chữ ký | Mô tả |
|-----|--------|-------|
| `afd_chb1_bilinear` | `(wp_rad, ws_rad, rp_db, rs_db, fs) → (b, a, order, Ωp, Ωs)` | Thiết kế IIR Chebyshev Type I: thực hiện pre-warp bilinear ($\Omega = \frac{2}{T}\tan(\omega/2)$), xác định bậc tối thiểu qua `cheb1ord`, tổng hợp bộ lọc số qua `cheby1`; in các tham số trung gian |
| `plot_iir_response` | `(b, a, fs, title, show_plots, save_path) → bool` | Vẽ lưới 2×2: biên độ (−3 dB marker), pha mở (unwrapped), group delay, và mặt phẳng Z; kiểm tra ổn định (tất cả cực nằm trong vòng tròn đơn vị); trả về `True/False` ổn định; lưu `06_iir_response.png` |
| `demo_iir` | `(fs, show_plots, save_dir) → dict` | Demo tổng hợp **Chương 4 & 5**: gọi `afd_chb1_bilinear` rồi `plot_iir_response`; trả về `{b, a, order, omega_p, omega_s, stable, wp, ws, fs}` |

---

### `modules/so_sanh.py` — So sánh FIR vs IIR

**Mục đích:** So sánh trực tiếp hiệu năng FIR Parks-McClellan và IIR Chebyshev về biên độ và group delay (trễ nhóm), làm nổi bật ưu/nhược điểm pha tuyến tính vs phi tuyến. Tương ứng **Chương 7**.

| Hàm | Chữ ký | Mô tả |
|-----|--------|-------|
| `compare_fir_iir` | `(h_fir, b_iir, a_iir, fs, show_plots, save_dir) → dict` | Tính `freqz` và `group_delay` cho cả hai bộ lọc; vẽ 2 biểu đồ cạnh nhau: đáp ứng biên độ (dB) và group delay (mẫu); tự động scale trục Y group delay để tránh nhiễu spike IIR; lưu `07_fir_vs_iir_compare.png`; trả về `{gd_fir_max, gd_iir_max}` |

---

### `modules/ung_dung.py` — Ứng dụng thực tế

**Mục đích:** Hai ứng dụng DSP thực tế minh họa tính hữu dụng của các bộ lọc đã thiết kế: loại bỏ nhiễu điện lưới 50 Hz và tạo hiệu ứng echo.

| Hàm | Chữ ký | Mô tả |
|-----|--------|-------|
| `design_notch_50hz` | `(fs, q) → (b, a)` | Thiết kế bộ lọc Notch tại 50 Hz bằng `iirnotch` với hệ số Q xác định độ hẹp dải chắn |
| `demo_notch` | `(fs, show_plots, save_dir) → dict` | Demo **Bổ sung – Notch 50 Hz**: tổng hợp tín hiệu nhiễu (440 Hz + 50 Hz + Gaussian), lọc qua Notch, tính SNR trước/sau, vẽ 4 biểu đồ (tín hiệu, phổ, đáp ứng bộ lọc); lưu `08_notch_50hz.png`; trả về `{b, a, snr_before, snr_after}` |
| `simulate_echo` | `(x, fs, delay_ms, decay) → ndarray` | Mô phỏng echo: $y[n] = x[n] + \alpha \cdot x[n - D]$ với $D$ = số mẫu delay; tương ứng thí nghiệm Lab-Volt TMS320C50 ex1\_1 |
| `demo_echo` | `(fs, show_plots, save_dir) → dict` | Demo **Bổ sung – Echo**: tạo tín hiệu xung ngắn, áp dụng echo với delay 100 ms và 400 ms, vẽ 3 biểu đồ; lưu `09_echo_demo.png`; trả về `{x, time}` |

---

### `modules/chay_demo.py` — Điều phối toàn bộ demo

**Mục đích:** Module trung tâm kết nối và chạy tất cả các chương theo thứ tự, thu thập kết quả và trả về dict tổng hợp.

| Hàm | Chữ ký | Mô tả |
|-----|--------|-------|
| `run_all` | `(show_plots, save_dir) → dict` | Hàm điều phối chính: áp dụng theme biểu đồ, rồi gọi tuần tự 9 demo theo thứ tự (Chương 1→9); kết quả IIR được chuyển sang `compare_fir_iir`; trả về dict tổng hợp với keys: `sampling`, `analysis`, `signal_ops`, `z`, `fir`, `iir`, `comparison`, `notch`, `echo`, `save_dir` |

---

## 5. SƠ ĐỒ PHỤ THUỘC MODULE

```
bo_loc_am_thanh_so.py
        │
        └── modules/__init__.py
                    │
                    └── chay_demo.py  ──────────────────────────────────────┐
                            │                                                │
                ┌───────────┼───────────────────────┐                       │
                │           │                       │                       │
        ung_dung.py    so_sanh.py         phan_tich_thiet_ke.py             │
        demo_lay_mau.py    thiet_ke_fir.py           thiet_ke_iir.py        │
        bien_doi_z.py      thaotac_tin_hieu.py                              │
                │           │                                               │
                └───────────┴──► cau_hinh_do_thi.py ◄────────────────────┘
```

**Chú thích:** `cau_hinh_do_thi.py` là module cơ sở không phụ thuộc module nào khác trong dự án. Tất cả các module khác đều import từ nó.

---

## 6. BẢN ĐỒ ĐỔI TÊN FILE

| Tên cũ (tiếng Anh) | Tên mới (tiếng Việt) | Ghi chú |
|--------------------|----------------------|---------|
| `dsp_audio_filter.py` | `bo_loc_am_thanh_so.py` | Bộ lọc âm thanh số |
| `modules/applications.py` | `modules/ung_dung.py` | Ứng dụng thực tế |
| `modules/comparison.py` | `modules/so_sanh.py` | So sánh FIR/IIR |
| `modules/demo_runner.py` | `modules/chay_demo.py` | Chạy demo |
| `modules/design_analysis.py` | `modules/phan_tich_thiet_ke.py` | Phân tích thiết kế |
| `modules/plot_config.py` | `modules/cau_hinh_do_thi.py` | Cấu hình đồ thị |
| `modules/signal_ops.py` | `modules/thaotac_tin_hieu.py` | Thao tác tín hiệu |
| `modules/sampling_demo.py` | `modules/demo_lay_mau.py` | Demo lấy mẫu |
| `modules/PT_TinHieuGoc.py` | `modules/bien_doi_z.py` | Biến đổi Z |
| `modules/Thietke_Fir.py` | `modules/thiet_ke_fir.py` | Thiết kế FIR |
| `modules/Thietke_IIR.py` | `modules/thiet_ke_iir.py` | Thiết kế IIR |
