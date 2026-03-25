# DSP Audio Filter – Mô phỏng Xử lý Tín hiệu Số

Dự án mô phỏng toàn bộ quy trình **thiết kế và phân tích bộ lọc số cho tín hiệu âm thanh** bằng Python/SciPy, tái hiện lại các bài toán thường gặp trong giáo trình DSP sử dụng MATLAB. Bao gồm: lấy mẫu, biến đổi Z, thiết kế bộ lọc FIR/IIR, so sánh hiệu năng, và các ứng dụng thực tế (lọc notch 50 Hz, hiệu ứng echo).

---

## Mục lục

- [Yêu cầu hệ thống](#yêu-cầu-hệ-thống)
- [Cài đặt](#cài-đặt)
- [Cấu trúc dự án](#cấu-trúc-dự-án)
- [Hướng dẫn sử dụng](#hướng-dẫn-sử-dụng)
  - [Chạy toàn bộ mô phỏng](#chạy-toàn-bộ-mô-phỏng)
  - [Các tùy chọn dòng lệnh](#các-tùy-chọn-dòng-lệnh)
- [Hướng dẫn từng file](#hướng-dẫn-từng-file)
  - [dsp\_audio\_filter.py](#dsp_audio_filterpy)
  - [modules/demo\_runner.py](#modulesdemo_runnerpy)
  - [modules/sampling\_demo.py](#modulessampling_demopy)
  - [modules/design\_analysis.py](#modulesdesign_analysispy)
  - [modules/signal\_ops.py](#modulessignal_opspy)
  - [modules/z\_analysis.py](#modulesz_analysispy)
  - [modules/fir\_filters.py](#modulesfir_filterspy)
  - [modules/iir\_filters.py](#modulesiir_filterspy)
  - [modules/comparison.py](#modulescomparisonpy)
  - [modules/applications.py](#modulesapplicationspy)
  - [modules/plot\_config.py](#modulesplot_configpy)
- [Ví dụ kết quả](#ví-dụ-kết-quả)

---

## Yêu cầu hệ thống

| Phần mềm | Phiên bản tối thiểu |
|---|---|
| Python | 3.9+ |
| numpy | 1.24+ |
| scipy | 1.11+ |
| matplotlib | 3.7+ |

> Hệ điều hành: Linux / macOS / Windows đều được hỗ trợ.

---

## Cài đặt

### 1. Clone repository

```bash
git clone https://github.com/<your-username>/DSP-test.git
cd DSP-test
```

### 2. Tạo môi trường ảo (khuyến nghị)

```bash
# Tạo virtual environment
python -m venv .venv

# Kích hoạt (Linux / macOS)
source .venv/bin/activate

# Kích hoạt (Windows)
.venv\Scripts\activate
```

### 3. Cài đặt các thư viện phụ thuộc

```bash
pip install -r requirements.txt
```

Nội dung `requirements.txt`:

```
numpy>=1.24
scipy>=1.11
matplotlib>=3.7
```

### 4. Kiểm tra cài đặt

```bash
python -c "import numpy, scipy, matplotlib; print('OK')"
```

Nếu in ra `OK` là cài đặt thành công.

---

## Cấu trúc dự án

```
DSP-test/
├── dsp_audio_filter.py      # Điểm vào chính (entry point)
├── requirements.txt         # Danh sách thư viện cần thiết
├── modules/
│   ├── __init__.py          # Export run_all()
│   ├── demo_runner.py       # Điều phối toàn bộ luồng chạy
│   ├── sampling_demo.py     # Chương 1b: Lấy mẫu & định lý Nyquist
│   ├── design_analysis.py   # Phân tích tín hiệu đầu vào & lựa chọn bộ lọc
│   ├── signal_ops.py        # Chương 1: Thao tác tín hiệu rời rạc
│   ├── z_analysis.py        # Chương 2: Biến đổi Z, phân tích H(z)
│   ├── fir_filters.py       # Chương 3: Thiết kế bộ lọc FIR
│   ├── iir_filters.py       # Chương 4: Thiết kế bộ lọc IIR
│   ├── comparison.py        # Chương 7: So sánh FIR vs IIR
│   ├── applications.py      # Bổ sung: Notch 50Hz & Echo
│   └── plot_config.py       # Cấu hình giao diện biểu đồ (Catppuccin dark)
└── imgaes/
    └── v3/                  # Thư mục lưu ảnh biểu đồ xuất ra
```

---

## Hướng dẫn sử dụng

### Chạy toàn bộ mô phỏng

Chạy lệnh sau từ thư mục gốc để thực hiện toàn bộ chuỗi mô phỏng và hiển thị tất cả biểu đồ:

```bash
python dsp_audio_filter.py
```

### Các tùy chọn dòng lệnh

| Tùy chọn | Mô tả |
|---|---|
| _(không có)_ | Chạy đầy đủ và hiển thị tất cả biểu đồ |
| `--no-plots` | Chạy không hiển thị biểu đồ (tiện cho CI/CD hoặc môi trường headless) |
| `--save-plots-dir <thư mục>` | Lưu toàn bộ biểu đồ dưới dạng file PNG vào thư mục chỉ định |

**Ví dụ:**

```bash
# Chỉ chạy tính toán, không mở cửa sổ đồ thị
python dsp_audio_filter.py --no-plots

# Lưu toàn bộ ảnh biểu đồ vào thư mục imgaes/v3/
python dsp_audio_filter.py --save-plots-dir imgaes/v3

# Vừa lưu ảnh vừa không hiển thị cửa sổ (phù hợp server/script tự động)
python dsp_audio_filter.py --no-plots --save-plots-dir imgaes/v3
```

---

## Hướng dẫn từng file

### `dsp_audio_filter.py`

**Điểm vào (entry point) của chương trình.** Phân tích tham số dòng lệnh rồi gọi `run_all()` từ package `modules`.

```python
# Dùng trực tiếp trong code khác
from modules import run_all
results = run_all(show_plots=False, save_dir="output/")
```

Hàm `run_all()` trả về một `dict` chứa kết quả của từng phần mô phỏng.

---

### `modules/demo_runner.py`

**Điều phối trung tâm** – gọi lần lượt tất cả các module theo đúng thứ tự, truyền tham số `show_plots` và `save_dir` xuống từng bước. Đây là nơi duy nhất gọi `apply_plot_style()` để áp dụng theme tối cho matplotlib trước khi vẽ bất kỳ biểu đồ nào.

Thứ tự thực thi:
1. `demo_sampling` → Lấy mẫu & Nyquist
2. `run_design_analysis` → Phân tích tín hiệu đầu vào
3. `demo_signal_ops` → Thao tác tín hiệu rời rạc
4. `demo_z_transform` → Phân tích Z
5. `demo_fir` → Thiết kế FIR
6. `demo_iir` → Thiết kế IIR
7. `compare_fir_iir` → So sánh
8. `demo_notch` → Bộ lọc Notch 50 Hz
9. `demo_echo` → Hiệu ứng Echo

---

### `modules/sampling_demo.py`

**Mô phỏng lấy mẫu tín hiệu và định lý Nyquist.**

Tín hiệu gốc được tạo từ 3 thành phần sin (440 Hz, 1000 Hz, 3000 Hz). Module thực hiện:
- Lấy mẫu tín hiệu liên tục tại tần số `Fs = 44100 Hz`
- Kiểm tra điều kiện Nyquist: `Fs ≥ 2 × f_max`
- Vẽ biểu đồ tín hiệu liên tục so với tín hiệu rời rạc
- Mô phỏng aliasing khi lấy mẫu dưới tần số Nyquist

**Hàm chính:** `demo_sampling(fs, show_plots, save_dir)`

---

### `modules/design_analysis.py`

**Phân tích bài toán và giải thích lý do lựa chọn bộ lọc.**

- Xác định các thông số tần số: dải thông (`fp = 4410 Hz`), dải chắn (`fs_edge = 6615 Hz`), bề rộng dải chuyển tiếp
- Tính bậc ước lượng cho bộ lọc Hamming và Chebyshev Type I
- In ra bảng so sánh để người dùng hiểu lý do chọn FIR hay IIR trong từng tình huống

**Hàm chính:** `run_design_analysis()` — không tạo biểu đồ, chỉ in kết quả phân tích ra terminal.

---

### `modules/signal_ops.py`

**Chương 1 – Thao tác cơ bản trên tín hiệu rời rạc.**

Triển khai các phép toán nền tảng của DSP:

| Hàm | Chức năng |
|---|---|
| `sigshift(x, n, d)` | Dịch tín hiệu đi `d` mẫu |
| `sigfold(x, n)` | Lấy đối xứng (gấp) tín hiệu quanh n=0 |
| `sigadd(x1, n1, x2, n2)` | Cộng hai tín hiệu không cùng trục thời gian |
| `energy(x)` | Tính năng lượng $E = \sum |x[n]|^2$ |

**Hàm demo:** `demo_signal_ops(show_plots, save_dir)` — vẽ biểu đồ 3 tín hiệu: gốc, dịch và cộng.

---

### `modules/z_analysis.py`

**Chương 2 – Biến đổi Z và phân tích hàm truyền H(z).**

- Phân tích phân số riêng phần (partial fraction) của H(z) bằng `scipy.signal.residuez`
- Vẽ sơ đồ zero-pole trên mặt phẳng Z (z-plane)
- Kiểm tra tính ổn định: tất cả cực phải nằm trong vòng tròn đơn vị `|z| < 1`
- In kết quả phần dư (residues), cực (poles), và hằng số trực tiếp

**Hàm chính:**
- `zplane(b, a, title, show_plots, save_path)` — vẽ z-plane và trả về `(zeros, poles)`
- `demo_z_transform(show_plots, save_dir)` — demo với H(z) = (1+z⁻¹)/(1−0.5z⁻¹+0.25z⁻²)

---

### `modules/fir_filters.py`

**Chương 3 – Thiết kế bộ lọc FIR.**

Thiết kế và so sánh hai phương pháp:

| Phương pháp | Hàm thiết kế | Đặc điểm |
|---|---|---|
| Cửa sổ Hamming | `design_fir_hamming(wp, ws)` | Đơn giản, dễ tính bậc theo công thức `M ≈ 6.6π/Δω` |
| Parks-McClellan | `design_fir_pm(wp, ws, δ₁_dB, δ₂_dB)` | Tối ưu minimax, bậc thấp hơn cùng đặc tả |

Biểu đồ xuất ra gồm: đáp ứng biên độ (dB), đáp ứng pha, và so sánh hệ số trên cùng một figure.

**Hàm demo:** `demo_fir(show_plots, save_dir)` — trả về `dict` chứa `h_hamming`, `h_pm`, `fs`, `wp`, `ws`.

---

### `modules/iir_filters.py`

**Chương 4 – Thiết kế bộ lọc IIR Chebyshev Type I.**

- Pre-warping tần số về miền analog bằng biến đổi bilinear: $\Omega = \frac{2}{T}\tan\!\left(\frac{\omega}{2}\right)$
- Xác định bậc tối thiểu N bằng `scipy.signal.cheb1ord`
- Thiết kế bộ lọc thực tế bằng `scipy.signal.cheby1`
- Biểu đồ gồm đáp ứng biên độ, pha, group delay và sơ đồ z-plane

**Hàm chính:**
- `afd_chb1_bilinear(wp, ws, rp_dB, rs_dB, fs)` — trả về `(b, a, order, Ωp, Ωs)`
- `demo_iir(show_plots, save_dir)` — trả về `dict` chứa `b`, `a`, `fs`

---

### `modules/comparison.py`

**Chương 7 – So sánh trực tiếp FIR (Parks-McClellan) và IIR (Chebyshev).**

Vẽ 2 biểu đồ cạnh nhau:
1. **Đáp ứng biên độ (dB):** nhấn mạnh sự khác biệt về số hệ số cần thiết
2. **Group Delay:** thể hiện tính pha tuyến tính của FIR (hằng số) và pha phi tuyến của IIR (biến đổi theo tần số)

**Hàm chính:** `compare_fir_iir(h_fir, b_iir, a_iir, fs, show_plots, save_dir)`

---

### `modules/applications.py`

**Ứng dụng thực tế: bộ lọc Notch 50 Hz và hiệu ứng Echo.**

#### Bộ lọc Notch 50 Hz (`demo_notch`)
- Loại bỏ nhiễu điện lưới 50 Hz khỏi tín hiệu âm thanh 440 Hz
- Sử dụng `scipy.signal.iirnotch` với hệ số phẩm chất `Q = 30`
- Tính và in SNR trước/sau lọc
- 4 biểu đồ: tín hiệu nhiễu, tín hiệu đã lọc, đáp ứng pha, đáp ứng biên độ của notch filter

#### Hiệu ứng Echo (`demo_echo`)
- Mô phỏng echo bằng bộ lọc FIR với delay: `y[n] = x[n] + α·x[n−D]`
- Tham số mặc định: độ trễ `D = 0.1 s`, hệ số suy giảm `α = 0.5`
- Vẽ tín hiệu gốc và tín hiệu echo trong miền thời gian

---

### `modules/plot_config.py`

**Cấu hình giao diện biểu đồ dùng chung.**

- `apply_plot_style()` — áp dụng theme tối (Catppuccin Mocha) cho toàn bộ matplotlib: nền `#1e1e2e`, trục `#2a2a3e`, chữ `#cdd6f4`
- `COLORS` — bảng màu 6 màu sáng trên nền tối: xanh lam, xanh lá, đỏ, cam, tím, cyan
- `build_save_path(save_dir, filename)` — tạo đường dẫn file PNG đầy đủ, tự động tạo thư mục nếu chưa tồn tại
- `finalize_figure(fig, show_plots, save_path)` — lưu file (nếu có `save_path`) rồi hiển thị hoặc đóng figure

---

## Ví dụ kết quả

Khi chạy thành công, terminal sẽ in:

```
╔══════════════════════════════════════════════════════════╗
║  THIẾT KẾ & PHÂN TÍCH BỘ LỌC SỐ CHO TÍN HIỆU ÂM THANH ║
║  Python / SciPy – Mô phỏng MATLAB                       ║
╚══════════════════════════════════════════════════════════╝

...

CHƯƠNG 1: THAO TÁC TÍN HIỆU RỜI RẠC
CHƯƠNG 2: BIẾN ĐỔI Z – PHÂN TÍCH H(z)
CHƯƠNG 3: BỘ LỌC FIR – Hamming & Parks-McClellan
CHƯƠNG 4: BỘ LỌC IIR – Chebyshev Type I (Bilinear)
CHƯƠNG 7: SO SÁNH FIR vs IIR
BỔ SUNG: BỘ LỌC NOTCH 50Hz

✔  Hoàn thành toàn bộ mô phỏng.
```

Ảnh biểu đồ (nếu dùng `--save-plots-dir`) được lưu vào thư mục `imgaes/v3/` với định dạng PNG, độ phân giải 220 DPI.