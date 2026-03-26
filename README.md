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
  - [bo\_loc\_am\_thanh\_so.py](#bo_loc_am_thanh_so)
  - [modules/chay\_demo.py](#moduleschay_demo)
  - [modules/demo\_lay\_mau.py](#modulesdemo_lay_mau)
  - [modules/phan\_tich\_thiet\_ke.py](#modulesphan_tich_thiet_ke)
  - [modules/thaotac\_tin\_hieu.py](#modulesthaotac_tin_hieu)
  - [modules/bien\_doi\_z.py](#modulesbien_doi_z)
  - [modules/thiet\_ke\_fir.py](#modulesthiet_ke_fir)
  - [modules/thiet\_ke\_iir.py](#modulesthiet_ke_iir)
  - [modules/so\_sanh.py](#modulesso_sanh)
  - [modules/ung\_dung.py](#modulesunq_dung)
  - [modules/cau\_hinh\_do\_thi.py](#modulescau_hinh_do_thi)
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
python -m venv venv

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
├── bo_loc_am_thanh_so.py      # Điểm vào chính (entry point)
├── requirements.txt         # Danh sách thư viện cần thiết
├── modules/
│   ├── __init__.py          # Export chay_toan_bo()
│   ├── chay_demo.py       # Điều phối toàn bộ luồng chạy
│   ├── demo_lay_mau.py     # Chương 1b: Lấy mẫu & định lý Nyquist
│   ├── phan_tich_thiet_ke.py   # Phân tích tín hiệu đầu vào & lựa chọn bộ lọc
│   ├── thaotac_tin_hieu.py        # Chương 1: Thao tác tín hiệu rời rạc
│   ├── bien_doi_z.py        # Chương 2: Biến đổi Z, phân tích H(z)
│   ├── thiet_ke_fir.py       # Chương 3: Thiết kế bộ lọc FIR
│   ├── thiet_ke_iir.py       # Chương 4: Thiết kế bộ lọc IIR
│   ├── so_sanh.py        # Chương 7: So sánh FIR vs IIR
│   ├── ung_dung.py      # Bổ sung: Notch 50Hz & Echo
│   └── cau_hinh_do_thi.py       # Cấu hình giao diện biểu đồ (Catppuccin dark)
└── imgaes/
    └── v3/                  # Thư mục lưu ảnh biểu đồ xuất ra
```

---

## Hướng dẫn sử dụng

### Chạy toàn bộ mô phỏng

Chạy lệnh sau từ thư mục gốc để thực hiện toàn bộ chuỗi mô phỏng và hiển thị tất cả biểu đồ:

```bash
# Câu lệnh chạy gốc
python bo_loc_am_thanh_so.py

# Chỉ chạy tính toán, không mở cửa sổ đồ thị
python bo_loc_am_thanh_so.py --no-plots

# Lưu toàn bộ ảnh biểu đồ vào thư mục imgaes/v3/
python bo_loc_am_thanh_so.py --save-plots-dir imgaes/v3

# Vừa lưu ảnh vừa không hiển thị cửa sổ (phù hợp server/script tự động)
python bo_loc_am_thanh_so.py --no-plots --save-plots-dir imgaes/v3
```


### Các tùy chọn dòng lệnh

| Tùy chọn | Mô tả |
|---|---|
| _(không có)_ | Chạy đầy đủ và hiển thị tất cả biểu đồ |
| `--no-plots` | Chạy không hiển thị biểu đồ (tiện cho CI/CD hoặc môi trường headless) |
| `--save-plots-dir <thư mục>` | Lưu toàn bộ biểu đồ dưới dạng file PNG vào thư mục chỉ định |


---

## Hướng dẫn từng file

### `bo_loc_am_thanh_so.py`

**Điểm vào (entry point) của chương trình.** Phân tích tham số dòng lệnh rồi gọi `chay_toan_bo()` từ package `modules`.

```python
# Dùng trực tiếp trong code khác
from modules import chay_toan_bo
results = chay_toan_bo(show_plots=False, save_dir="output/")
```

Hàm `chay_toan_bo()` trả về một `dict` chứa kết quả của từng phần mô phỏng.

---

### `modules/chay_demo.py`

**Điều phối trung tâm** – gọi lần lượt tất cả các module theo đúng thứ tự, truyền tham số `show_plots` và `save_dir` xuống từng bước. Đây là nơi duy nhất gọi `ap_dung_style_do_thi()` để áp dụng theme tối cho matplotlib trước khi vẽ bất kỳ biểu đồ nào.

Thứ tự thực thi:
1. `demo_qua_trinh_lay_mau` → Lấy mẫu & Nyquist
2. `chay_phan_tich_thiet_ke` → Phân tích tín hiệu đầu vào
3. `demo_thaotac_tin_hieu` → Thao tác tín hiệu rời rạc
4. `demo_phan_tich_z` → Phân tích Z
5. `demo_bo_loc_fir` → Thiết kế FIR
6. `demo_bo_loc_iir` → Thiết kế IIR
7. `so_sanh_fir_iir` → So sánh
8. `demo_bo_loc_notch` → Bộ lọc Notch 50 Hz
9. `demo_hieu_ung_echo` → Hiệu ứng Echo

---

### `modules/demo_lay_mau.py`

**Mô phỏng lấy mẫu tín hiệu và định lý Nyquist.**

Tín hiệu gốc được tạo từ 3 thành phần sin (440 Hz, 1000 Hz, 3000 Hz). Module thực hiện:
- Lấy mẫu tín hiệu liên tục tại tần số `Fs = 44100 Hz`
- Kiểm tra điều kiện Nyquist: `Fs ≥ 2 × f_max`
- Vẽ biểu đồ tín hiệu liên tục so với tín hiệu rời rạc
- Mô phỏng aliasing khi lấy mẫu dưới tần số Nyquist

**Hàm chính:** `demo_qua_trinh_lay_mau(fs, show_plots, save_dir)`

---

### `modules/phan_tich_thiet_ke.py`

**Phân tích bài toán và giải thích lý do lựa chọn bộ lọc.**

- Xác định các thông số tần số: dải thông (`fp = 4410 Hz`), dải chắn (`fs_edge = 6615 Hz`), bề rộng dải chuyển tiếp
- Tính bậc ước lượng cho bộ lọc Hamming và Chebyshev Type I
- In ra bảng so sánh để người dùng hiểu lý do chọn FIR hay IIR trong từng tình huống

**Hàm chính:** `chay_phan_tich_thiet_ke()` — không tạo biểu đồ, chỉ in kết quả phân tích ra terminal.

---

### `modules/thaotac_tin_hieu.py`

**Chương 1 – Thao tác cơ bản trên tín hiệu rời rạc.**

Triển khai các phép toán nền tảng của DSP:

| Hàm | Chức năng |
|---|---|
| `dich_tin_hieu(x, n, d)` | Dịch tín hiệu đi `d` mẫu |
| `gap_tin_hieu(x, n)` | Lấy đối xứng (gấp) tín hiệu quanh n=0 |
| `cong_hai_tin_hieu(x1, n1, x2, n2)` | Cộng hai tín hiệu không cùng trục thời gian |
| `nang_luong(x)` | Tính năng lượng $E = \sum |x[n]|^2$ |

**Hàm demo:** `demo_thaotac_tin_hieu(show_plots, save_dir)` — vẽ biểu đồ 3 tín hiệu: gốc, dịch và cộng.

---

### `modules/bien_doi_z.py`

**Chương 2 – Biến đổi Z và phân tích hàm truyền H(z).**

- Phân tích phân số riêng phần (partial fraction) của H(z) bằng `scipy.signal.residuez`
- Vẽ sơ đồ zero-pole trên mặt phẳng Z (z-plane)
- Kiểm tra tính ổn định: tất cả cực phải nằm trong vòng tròn đơn vị `|z| < 1`
- In kết quả phần dư (residues), cực (poles), và hằng số trực tiếp

**Hàm chính:**
- `ve_mat_phang_z(b, a, title, show_plots, save_path)` — vẽ z-plane và trả về `(zeros, poles)`
- `demo_phan_tich_z(show_plots, save_dir)` — demo với H(z) = (1+z⁻¹)/(1−0.5z⁻¹+0.25z⁻²)

---

### `modules/thiet_ke_fir.py`

**Chương 3 – Thiết kế bộ lọc FIR.**

Thiết kế và so sánh hai phương pháp:

| Phương pháp | Hàm thiết kế | Đặc điểm |
|---|---|---|
| Cửa sổ Hamming | `thiet_ke_fir_hamming(wp, ws)` | Đơn giản, dễ tính bậc theo công thức `M ≈ 6.6π/Δω` |
| Parks-McClellan | `thiet_ke_fir_pm(wp, ws, δ₁_dB, δ₂_dB)` | Tối ưu minimax, bậc thấp hơn cùng đặc tả |

Biểu đồ xuất ra gồm: đáp ứng biên độ (dB), đáp ứng pha, và so sánh hệ số trên cùng một figure.

**Hàm demo:** `demo_bo_loc_fir(show_plots, save_dir)` — trả về `dict` chứa `h_hamming`, `h_pm`, `fs`, `wp`, `ws`.

---

### `modules/thiet_ke_iir.py`

**Chương 4 – Thiết kế bộ lọc IIR Chebyshev Type I.**

- Pre-warping tần số về miền analog bằng biến đổi bilinear: $\Omega = \frac{2}{T}\tan\!\left(\frac{\omega}{2}\right)$
- Xác định bậc tối thiểu N bằng `scipy.signal.cheb1ord`
- Thiết kế bộ lọc thực tế bằng `scipy.signal.cheby1`
- Biểu đồ gồm đáp ứng biên độ, pha, group delay và sơ đồ z-plane

**Hàm chính:**
- `thiet_ke_iir_bilinear(wp, ws, rp_dB, rs_dB, fs)` — trả về `(b, a, order, Ωp, Ωs)`
- `demo_bo_loc_iir(show_plots, save_dir)` — trả về `dict` chứa `b`, `a`, `fs`

---

### `modules/so_sanh.py`

**Chương 7 – So sánh trực tiếp FIR (Parks-McClellan) và IIR (Chebyshev).**

Vẽ 2 biểu đồ cạnh nhau:
1. **Đáp ứng biên độ (dB):** nhấn mạnh sự khác biệt về số hệ số cần thiết
2. **Group Delay:** thể hiện tính pha tuyến tính của FIR (hằng số) và pha phi tuyến của IIR (biến đổi theo tần số)

**Hàm chính:** `so_sanh_fir_iir(h_fir, b_iir, a_iir, fs, show_plots, save_dir)`

---

### `modules/ung_dung.py`

**Ứng dụng thực tế: bộ lọc Notch 50 Hz và hiệu ứng Echo.**

#### Bộ lọc Notch 50 Hz (`demo_bo_loc_notch`)
- Loại bỏ nhiễu điện lưới 50 Hz khỏi tín hiệu âm thanh 440 Hz
- Sử dụng `scipy.signal.iirnotch` với hệ số phẩm chất `Q = 30`
- Tính và in SNR trước/sau lọc
- 4 biểu đồ: tín hiệu nhiễu, tín hiệu đã lọc, đáp ứng pha, đáp ứng biên độ của notch filter

#### Hiệu ứng Echo (`demo_hieu_ung_echo`)
- Mô phỏng echo bằng bộ lọc FIR với delay: `y[n] = x[n] + α·x[n−D]`
- Tham số mặc định: độ trễ `D = 0.1 s`, hệ số suy giảm `α = 0.5`
- Vẽ tín hiệu gốc và tín hiệu echo trong miền thời gian

---

### `modules/cau_hinh_do_thi.py`

**Cấu hình giao diện biểu đồ dùng chung.**

- `ap_dung_style_do_thi()` — áp dụng theme tối (Catppuccin Mocha) cho toàn bộ matplotlib: nền `#1e1e2e`, trục `#2a2a3e`, chữ `#cdd6f4`
- `COLORS` — bảng màu 6 màu sáng trên nền tối: xanh lam, xanh lá, đỏ, cam, tím, cyan
- `tao_duong_dan_luu(save_dir, filename)` — tạo đường dẫn file PNG đầy đủ, tự động tạo thư mục nếu chưa tồn tại
- `hoan_thien_bieu_do(fig, show_plots, save_path)` — lưu file (nếu có `save_path`) rồi hiển thị hoặc đóng figure

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