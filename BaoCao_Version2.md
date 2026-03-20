# BÁO CÁO VERSION 2

## 1. Mục tiêu

Tài liệu này mô tả chi tiết cách tổ chức code Python mô phỏng các nội dung DSP trong báo cáo gốc, theo hướng dễ debug, dễ mở rộng và bám sát tư duy MATLAB. Phiên bản 2 tập trung vào 3 mục tiêu:

1. Tách code thành module nhỏ để kiểm thử và sửa lỗi nhanh.
2. Dùng `matplotlib` để hiển thị biểu đồ khi cần phân tích đáp ứng hệ thống.
3. Tài liệu hóa rõ luồng xử lý từ lý thuyết đến code.

---

## 2. Kiến trúc thư mục

```text
DSP-test/
├── dsp_audio_filter.py
├── requirements.txt
├── Repost.md
├── BaoCao_Version2.md
├── GhiNho_100_CauHoi_Dap.md
└── modules/
    ├── __init__.py
    ├── plot_config.py
    ├── signal_ops.py
    ├── z_analysis.py
    ├── fir_filters.py
    ├── iir_filters.py
    ├── applications.py
    ├── comparison.py
    └── demo_runner.py
```

---

## 3. Ý nghĩa từng module

### 3.1 [modules/plot_config.py](modules/plot_config.py)
Chứa cấu hình giao diện cho `matplotlib`:
- Màu nền
- Màu trục
- Màu đường vẽ
- Hàm `apply_plot_style()` để áp dụng style thống nhất
- Hàm `finalize_figure()` để quyết định `plt.show()` hay `plt.close()` khi debug headless

### 3.2 [modules/signal_ops.py](modules/signal_ops.py)
Chứa các thao tác tín hiệu rời rạc cơ bản:
- `sigshift()`
- `sigfold()`
- `sigadd()`
- `energy()`
- `demo_signal_ops()`

Module này dùng để kiểm chứng các phép toán chỉ số rời rạc trước khi đi vào thiết kế bộ lọc.

### 3.3 [modules/z_analysis.py](modules/z_analysis.py)
Chứa phần biến đổi Z và phân tích cực-không:
- `zplane()` để mô phỏng lệnh `zplane()` trong MATLAB
- `demo_z_transform()` để dùng `residuez()` phân tích khai triển phân thức

### 3.4 [modules/fir_filters.py](modules/fir_filters.py)
Chứa thiết kế bộ lọc FIR:
- `design_fir_hamming()`
- `design_fir_pm()`
- `plot_fir_response()`
- `demo_fir()`

Tại đây có thể debug riêng phần FIR mà không ảnh hưởng IIR.

### 3.5 [modules/iir_filters.py](modules/iir_filters.py)
Chứa thiết kế bộ lọc IIR:
- `afd_chb1_bilinear()`
- `plot_iir_response()`
- `demo_iir()`

Module này bám sát ý tưởng trong báo cáo: pre-warping + Chebyshev Type I + kiểm tra ổn định qua cực.

### 3.6 [modules/applications.py](modules/applications.py)
Chứa các bài toán ứng dụng thực tế:
- `design_notch_50hz()`
- `demo_notch()`
- `simulate_echo()`
- `demo_echo()`

Tách riêng module này giúp bổ sung bài toán âm thanh thực tế mà không làm rối phần lý thuyết.

### 3.7 [modules/comparison.py](modules/comparison.py)
So sánh FIR và IIR:
- đáp ứng biên độ
- trễ nhóm
- độ phức tạp hệ số

### 3.8 [modules/demo_runner.py](modules/demo_runner.py)
Đây là module điều phối toàn bộ luồng mô phỏng:
1. áp style biểu đồ
2. gọi demo từng chương
3. gom kết quả trả về

### 3.9 [dsp_audio_filter.py](dsp_audio_filter.py)
File chạy chính rất gọn:
- parse tham số dòng lệnh
- gọi `run_all()`
- hỗ trợ `--no-plots` để debug hoặc chạy trên server không có màn hình

---

## 4. Luồng xử lý tổng thể

### Bước 1: Khởi tạo
Chạy file [dsp_audio_filter.py](dsp_audio_filter.py). File này gọi [modules/demo_runner.py](modules/demo_runner.py).

### Bước 2: Áp dụng style đồ thị
`apply_plot_style()` đảm bảo toàn bộ biểu đồ có cùng phong cách hiển thị.

### Bước 3: Chạy từng khối bài toán
- Khối 1: thao tác tín hiệu rời rạc
- Khối 2: biến đổi Z
- Khối 3: FIR
- Khối 4: IIR
- Khối 5: so sánh FIR/IIR
- Khối 6: notch 50Hz
- Khối 7: echo

### Bước 4: Hiển thị hoặc đóng hình
Nếu chạy bình thường: `show_plots=True` → `matplotlib` hiển thị hình.
Nếu debug/headless: dùng `--no-plots` → hình được đóng ngay sau khi tạo.

---

## 5. Phân tích cách code từng phần

## 5.1 Phần thao tác tín hiệu

### `sigshift(x, n, d)`
Ý nghĩa:
- giữ nguyên biên độ `x`
- chỉ thay đổi trục chỉ số `n + d`

Mục đích:
- mô phỏng phép dịch tín hiệu trong DSP rời rạc

### `sigfold(x, n)`
Ý nghĩa:
- đảo thứ tự mẫu
- đổi dấu trục thời gian

Mục đích:
- mô phỏng phép gấp tín hiệu, thường dùng khi học tích chập và đối xứng

### `sigadd(x1, n1, x2, n2)`
Ý nghĩa:
- căn chỉnh hai trục chỉ số khác nhau
- đưa về cùng miền `n_out`
- cộng từng phần tử

Lưu ý debug:
- đây là nơi dễ sai lệch index nhất
- cần kiểm tra `n_start`, `n_stop`, và lát cắt khi gán vào `y1`, `y2`

---

## 5.2 Phần biến đổi Z

### `residuez(b, a)`
Dùng để phân tích hàm truyền rời rạc dưới dạng tổng các phân thức đơn giản. Điều này tương ứng với nội dung lý thuyết trong báo cáo.

### `zplane(b, a)`
Các bước xử lý:
1. Tìm zero bằng `np.roots(b)`
2. Tìm pole bằng `np.roots(a)`
3. Vẽ vòng tròn đơn vị
4. Vẽ cực và không trên mặt phẳng phức
5. Kiểm tra ổn định bằng điều kiện $|p_k| < 1$

---

## 5.3 Phần FIR

### 5.3.1 FIR Hamming
Trong [modules/fir_filters.py](modules/fir_filters.py), hàm `design_fir_hamming()` tính bậc theo công thức trong báo cáo:

$$M = \left\lceil \frac{6.6\pi}{\Delta \omega} \right\rceil$$

Sau đó:
- nếu `M` lẻ thì tăng lên để được FIR Type-1
- chọn tần số cắt trung bình giữa dải thông và dải chắn
- gọi `firwin()` với cửa sổ Hamming

### 5.3.2 FIR Parks-McClellan
Hàm `design_fir_pm()`:
1. đổi ripple dB sang biên độ tuyến tính
2. ước lượng bậc gần đúng
3. gọi `remez()` để tối ưu equiripple

Ưu điểm:
- số hệ số thấp hơn so với Hamming
- phù hợp khi muốn tiết kiệm phép nhân-cộng

---

## 5.4 Phần IIR

### `afd_chb1_bilinear()`
Các bước:
1. Pre-warp tần số bằng:

$$\Omega = \frac{2}{T} \tan\left(\frac{\omega}{2}\right)$$

2. Dùng `cheb1ord()` xác định bậc nhỏ nhất
3. Dùng `cheby1()` tạo bộ lọc số

Trong MATLAB gốc có dạng `afd_chb1` + `bilinear`. Trong Python, `SciPy` cho phép đi thẳng theo chuẩn digital, nhưng vẫn giữ phần pre-warp để giải thích đúng lý thuyết.

### `plot_iir_response()`
Vẽ 4 nhóm đồ thị:
- Magnitude
- Phase
- Group delay
- Z-plane

Ý nghĩa debug:
- nếu magnitude sai → kiểm tra thông số bậc/tần số cắt
- nếu pole vượt vòng tròn đơn vị → kiểm tra ổn định
- nếu phase méo nhiều → đó là bản chất IIR

---

## 5.5 Phần Notch 50Hz

Mục tiêu:
- loại nhiễu điện lưới 50Hz khỏi tín hiệu âm thanh

Cách làm:
- tạo tín hiệu sạch 440Hz
- cộng nhiễu 50Hz và nhiễu Gaussian nhỏ
- thiết kế `iirnotch(50Hz)`
- lọc bằng `signal.lfilter()`
- so sánh SNR trước và sau lọc

Đây là phần sát với ứng dụng thực tế nhất trong đồ án.

---

## 5.6 Phần Echo

Hàm `simulate_echo()` dùng mô hình:

$$y(n) = x(n) + \alpha x(n-D)$$

với:
- $D$: số mẫu trễ
- $\alpha$: hệ số suy giảm

Ý nghĩa:
- mô phỏng bài thí nghiệm điều chỉnh tiếng vọng trên kit Lab-Volt DSP

---

## 6. Lý do tách module để debug

Phiên bản cũ gom toàn bộ logic vào một file dài. Khi debug sẽ có các nhược điểm:
- khó tìm lỗi do phạm vi file lớn
- khó thử riêng FIR/IIR
- khó tái sử dụng hàm
- khó kiểm tra từng chương độc lập

Phiên bản mới khắc phục bằng cách:
- mỗi chương lớn thành một module riêng
- file chạy chính rất ngắn
- có thể import từng module trong Python shell để thử riêng
- có thể viết test sau này cho từng hàm

Ví dụ debug riêng FIR:
```python
from modules.fir_filters import demo_fir
result = demo_fir(show_plots=False)
print(result["h_pm"])
```

Ví dụ debug riêng Notch:
```python
from modules.applications import demo_notch
demo_notch(show_plots=False)
```

---

## 7. Cách chạy chương trình

### Chạy bình thường
```bash
python dsp_audio_filter.py
```

### Chạy không mở biểu đồ
```bash
python dsp_audio_filter.py --no-plots
```

Phù hợp khi:
- debug trên terminal
- chạy CI/CD
- chạy máy chủ không có giao diện

---

## 8. Kết quả chính

### FIR
- Hamming: bậc lớn hơn nhưng đơn giản
- Parks-McClellan: số hệ số ít hơn, tối ưu hơn

### IIR
- Chebyshev Type I cho bậc nhỏ
- đáp ứng dốc tốt
- pha phi tuyến
- ổn định nếu mọi pole nằm trong vòng tròn đơn vị

### Notch 50Hz
- cải thiện SNR rõ rệt
- cho thấy ứng dụng thực tế của bộ lọc chắn dải

### Echo
- minh họa trực quan bài toán trễ và phản hồi âm thanh

---

## 9. Định hướng mở rộng

1. Thêm chức năng đọc file `.wav` thật bằng `scipy.io.wavfile`
2. Thêm bộ lọc high-pass, band-pass, band-stop tổng quát
3. Thêm LMS adaptive filter để khử vọng
4. Thêm unit test cho từng module
5. Thêm notebook để trình bày trực quan theo từng chương
6. Thêm CLI chọn chế độ chạy từng demo

---

## 10. Kết luận

Phiên bản 2 đã chuyển code sang cấu trúc module rõ ràng, phù hợp cho học tập, báo cáo và debug. `matplotlib` tiếp tục được dùng để minh họa đáp ứng biên độ, pha, trễ nhóm, phổ FFT và Z-plane. Kiến trúc mới giúp bám sát báo cáo gốc nhưng sạch hơn, dễ đọc hơn và thuận lợi hơn khi phát triển tiếp.
