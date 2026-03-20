# PHÂN TÍCH INPUT, LÝ DO CHỌN BỘ LỌC VÀ TÍNH TOÁN THAM SỐ

## 1. Phân tích tín hiệu input

### 1.1. Bài toán low-pass audio
Trong đề tài, tín hiệu được xét với tần số lấy mẫu:

$$F_s = 44.1\text{ kHz}$$

Các thông số thiết kế:
- $\omega_p = 0.2\pi$
- $\omega_s = 0.3\pi$

Đổi sang tần số vật lý:

$$f_p = \frac{\omega_p F_s}{2\pi} = 4410\text{ Hz}$$

$$f_s = \frac{\omega_s F_s}{2\pi} = 6615\text{ Hz}$$

### Nhận xét
- Dải thông mong muốn nằm dưới khoảng 4.41 kHz.
- Dải chắn bắt đầu từ 6.615 kHz.
- Khoảng từ 4.41 kHz đến 6.615 kHz là dải chuyển tiếp.
- Điều này phù hợp với bài toán làm mượt hoặc loại bỏ thành phần tần cao không mong muốn trong âm thanh.

### 1.2. Bài toán notch 50 Hz
Input demo trong code gồm:
- tín hiệu hữu ích: sin 440 Hz
- nhiễu điện lưới: sin 50 Hz
- nhiễu Gaussian nhỏ

### Nhận xét
Đây là dạng nhiễu hẹp băng, tập trung quanh đúng 50 Hz. Vì vậy dùng notch filter là chính xác hơn so với low-pass hoặc high-pass.

---

## 2. Lý do chọn bộ lọc và bậc lọc

## 2.1. FIR Hamming
### Vì sao chọn
FIR phù hợp khi cần pha tuyến tính. Trong âm thanh, pha tuyến tính giúp các thành phần tần số không bị lệch thời gian quá khác nhau, từ đó hạn chế méo dạng sóng.

### Vì sao bậc cao
Phương pháp cửa sổ Hamming dễ dùng nhưng không tối ưu tuyệt đối. Do đó muốn đáp ứng đủ sắc cạnh thì phải tăng bậc.

### Công thức bậc

$$M = \left\lceil \frac{6.6\pi}{\Delta \omega} \right\rceil$$

Với:

$$\Delta \omega = 0.3\pi - 0.2\pi = 0.1\pi$$

Suy ra:

$$M = \left\lceil \frac{6.6\pi}{0.1\pi} \right\rceil = \lceil 66 \rceil = 66$$

Đây cũng chính là giá trị code đang dùng.

---

## 2.2. FIR Parks-McClellan
### Vì sao chọn
Vẫn là FIR nên vẫn giữ được ưu điểm pha tuyến tính, nhưng dùng thuật toán tối ưu equiripple để giảm số hệ số.

### Vì sao bậc nhỏ hơn
Thuật toán Parks-McClellan tối ưu ripple giữa các dải theo chuẩn Chebyshev nên thường đạt yêu cầu với bậc thấp hơn phương pháp cửa sổ.

### Ý nghĩa thực tế
- giảm số phép nhân-cộng
- thuận lợi khi cần bộ lọc FIR gọn hơn
- vẫn thích hợp cho audio nếu ưu tiên pha

---

## 2.3. IIR Chebyshev Type I
### Vì sao chọn
IIR phù hợp khi ưu tiên hiệu quả tính toán. Trong báo cáo có liên hệ tới DSP fixed-point như TMS320C50, nên bộ lọc IIR là lựa chọn hợp lý vì bậc nhỏ.

### Vì sao chọn Chebyshev Type I
Chebyshev Type I cho dải thông có ripple nhỏ nhưng đạt sườn lọc dốc hơn Butterworth với cùng bậc.

### Vì sao bậc chỉ là 4
Với yêu cầu:
- ripple dải thông $R_p = 1$ dB
- suy giảm dải chắn $R_s = 15$ dB

Hàm `cheb1ord()` tính được bậc tối thiểu:

$$N = 4$$

Điều này cho thấy IIR tiết kiệm tài nguyên hơn FIR rất rõ.

---

## 2.4. Notch filter 50 Hz
### Vì sao chọn
Nhiễu đầu vào chỉ tập trung mạnh quanh 50 Hz. Nếu dùng low-pass hoặc high-pass sẽ loại cả phần tín hiệu hữu ích không cần thiết.

### Vì sao notch là hợp lý nhất
Notch filter chỉ chặn dải rất hẹp quanh tần số nhiễu, do đó giữ được phần còn lại của phổ tốt hơn.

---

## 3. Tính toán các tham số bộ lọc

## 3.1. Chuyển từ tần số chuẩn hóa sang tần số vật lý

$$f = \frac{\omega F_s}{2\pi}$$

- Với $\omega_p = 0.2\pi$:

$$f_p = 4410\text{ Hz}$$

- Với $\omega_s = 0.3\pi$:

$$f_s = 6615\text{ Hz}$$

---

## 3.2. Pre-warp cho bilinear transform
Do phép biến đổi song tuyến gây méo trục tần số, cần pre-warp:

$$\Omega = \frac{2}{T}\tan\left(\frac{\omega}{2}\right)$$

Với $T = 1/F_s$:

- $\Omega_p \approx 28657.92\text{ rad/s}$
- $\Omega_s \approx 44940.14\text{ rad/s}$

### Ý nghĩa
Đây là các tham số tương tự tương đương trước khi ánh xạ sang miền số.

---

## 3.3. Tham số FIR Parks-McClellan
Code sử dụng:
- ripple dải thông: 0.5 dB
- suy giảm dải chắn: 40 dB

Các giá trị này được đổi sang biên độ tuyến tính trước khi đưa vào `remez()` để cân trọng số giữa dải thông và dải chắn.

### Ý nghĩa
- ripple nhỏ giúp giữ độ phẳng dải thông
- suy giảm lớn giúp chặn tần số ngoài dải tốt hơn

---

## 3.4. Tham số notch
Code dùng:
- tần số notch: 50 Hz
- hệ số chất lượng `Q = 30`

### Ý nghĩa của `Q`
- `Q` lớn: dải chắn hẹp hơn
- `Q` nhỏ: dải chắn rộng hơn

Ở đây chọn `Q = 30` để chặn đúng vùng 50 Hz mà không làm mất nhiều thành phần lân cận.

---

## 4. So sánh ngắn gọn

| Loại lọc | Lý do chọn | Ưu điểm | Nhược điểm | Bậc lọc |
|---|---|---|---|---|
| FIR Hamming | cần pha tuyến tính | dễ hiểu, ổn định | bậc cao | 66 |
| FIR Parks-McClellan | cần FIR nhưng gọn hơn | ít hệ số hơn | thiết kế phức tạp hơn | khoảng 20 |
| IIR Chebyshev I | cần tiết kiệm tính toán | bậc thấp, sườn dốc | pha phi tuyến | 4 |
| Notch 50 Hz | nhiễu tập trung tại 50 Hz | loại nhiễu hẹp băng tốt | chỉ hợp khi biết rõ tần số nhiễu | rất hẹp quanh 50 Hz |

---

## 5. Kết luận

Ba yêu cầu chính có thể kết luận như sau:

1. **Phân tích input** cho thấy bài toán gồm cả lọc thông thấp tổng quát và lọc nhiễu 50 Hz hẹp băng.
2. **Lý do chọn bộ lọc** phụ thuộc mục tiêu: bảo toàn pha thì chọn FIR, tiết kiệm tính toán thì chọn IIR, khử nhiễu đơn tần thì chọn Notch.
3. **Tính toán tham số bộ lọc** được thực hiện nhất quán từ thông số chuẩn hóa, đổi sang Hz, rồi đổi tiếp sang miền analog khi cần cho bilinear transform.

Tài liệu này liên kết trực tiếp với code trong [modules/fir_filters.py](modules/fir_filters.py), [modules/iir_filters.py](modules/iir_filters.py) và [modules/applications.py](modules/applications.py).
