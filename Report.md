BÁO CÁO BÀI TẬP LỚN: THIẾT KẾ VÀ PHÂN TÍCH BỘ LỌC SỐ CHO TÍN HIỆU ÂM THANH

TRƯỜNG ĐẠI HỌC BÁCH KHOA HÀ NỘI
VIỆN ĐIỆN TỬ - VIỄN THÔNG


--------------------------------------------------------------------------------


Thông tin sinh viên:

* Họ và tên: Đồng Thiên Trang
* MSSV: 20102350
* Lớp: Điện tử Viễn thông 10 – K55
* Mã lớp thí nghiệm: 625106
* Giảng viên hướng dẫn: Giảng viên Cao cấp chuyên ngành DSP


--------------------------------------------------------------------------------


1. TÓM TẮT (ABSTRACT)

Trong lĩnh vực xử lý tín hiệu âm thanh hiện đại, bộ lọc số (Digital Filter) đóng vai trò là hạt nhân điều khiển chất lượng và đặc tính phổ của tín hiệu. Sự chuyển dịch từ các hệ thống tương tự (analog) cồng kềnh sang các hệ thống số linh hoạt đòi hỏi sự hiểu biết sâu sắc về các cấu trúc lọc FIR và IIR. Báo cáo này trình bày quy trình thiết kế, mô phỏng và phân tích các loại bộ lọc số tối ưu thông qua công cụ MATLAB, đồng thời liên hệ trực tiếp với kiến trúc phần cứng chuyên dụng TMS320C50 của Texas Instruments.

Nội dung báo cáo tập trung vào việc hiện thực hóa các bài toán lọc nhiễu, bảo toàn pha tuyến tính cho âm thanh Hi-Fi và tối ưu hóa tài nguyên tính toán. Kết quả nghiên cứu khẳng định rằng việc làm chủ các thuật toán như Parks-McClellan hay Biến đổi song tuyến (Bilinear Transformation) không chỉ dừng lại ở lý thuyết mà còn là kỹ năng then chốt trong việc triển khai các hệ thống DSP thời gian thực trong kỷ nguyên Công nghiệp 4.0.


--------------------------------------------------------------------------------


2. CHƯƠNG 1: GIỚI THIỆU TỔNG QUAN

Sự chuyển dịch từ kỹ thuật tương tự sang kỹ thuật số trong ngành âm thanh không chỉ là sự thay đổi về mặt công nghệ mà còn là sự tối ưu hóa về độ chính xác và tính lặp lại. Các hệ thống số cho phép xử lý những thuật toán phức tạp mà mạch analog không thể thực hiện hiệu quả do sai số linh kiện và nhiễu nhiệt.

Kiến trúc DSP chuyên dụng:
Trái tim của các hệ thống này là bộ xử lý tín hiệu số (DSP), tiêu biểu là dòng chip TMS320C50. Đây là dòng DSP 16-bit điểm tĩnh (fixed-point) thế hệ thứ ba, phát triển dựa trên kiến trúc của TMS320C10. Khác với CPU thông thường, TMS320C50 sử dụng kiến trúc Harvard cải tiến cho phép truy cập dữ liệu và lệnh song song, tối ưu hóa cho phép toán Nhân và Cộng (MAC - Multiply-Accumulate). Chip đạt tốc độ 50 MIPS (triệu lệnh trên giây), vượt trội hoàn toàn so với mức 8 MIPS của thế hệ đầu, cho phép xử lý âm thanh thời gian thực với độ trễ cực thấp.

Ứng dụng trong xử lý âm thanh:

* Lọc nhiễu đơn tần: Loại bỏ nhiễu điện lưới 50Hz/60Hz bằng bộ lọc Notch (chắn dải).
* Audio Hi-Fi: Sử dụng bộ lọc FIR pha tuyến tính để tránh méo dạng tín hiệu trong các hệ thống thu âm chất lượng cao.
* Nhận dạng tiếng nói: Tiền xử lý tín hiệu trong các thiết bị di động và viễn thông.

Mục tiêu kỹ thuật: Làm chủ các phương pháp thiết kế bộ lọc trên MATLAB và hiểu rõ cơ chế vận hành của phần cứng DSP Lab-Volt để ứng dụng vào thực tế sản xuất.


--------------------------------------------------------------------------------


3. CHƯƠNG 2: CƠ SỞ LÝ THUYẾT VỀ TÍN HIỆU VÀ HỆ THỐNG

2.1. Mô hình toán học và Thao tác tín hiệu

Hệ thống Tuyến tính Bất biến (LTI) rời rạc được mô tả qua phương trình sai phân: y(n) = \sum_{i=0}^{M} b_i x(n-i) - \sum_{j=1}^{N} a_j y(n-j) Trong thực tế lập trình MATLAB, trước khi xử lý, tín hiệu cần được thao tác qua các hàm bổ trợ như sigshift (dịch dãy), sigfold (gấp dãy), và sigadd (cộng dãy). Việc tính toán năng lượng tín hiệu được thực hiện qua hàm tự dựng energy(x,n) với công thức E_x = \sum |x(n)|^2.

2.2. Biến đổi Z và Phân tích miền tần số

Biến đổi Z chuyển đổi phương trình sai phân sang hàm truyền đạt H(z) = \frac{B(z)}{A(z)}. Để tìm biến đổi Z ngược cho các dãy nhân quả, chúng ta sử dụng phương pháp khai triển phân thức đơn giản thông qua hàm residuez để xác định các thặng dư (residues) và điểm cực (poles). X(z) = \sum_{k=1}^{N} \frac{R_k}{1 - p_k z^{-1}} + C

2.3. Phân loại bộ lọc lý tưởng

Dựa trên đáp ứng tần số H(e^{j\omega}), bộ lọc được chia thành:

1. Low-pass (Thông thấp): Giữ lại dải tần thấp (âm bass).
2. High-pass (Thông cao): Loại bỏ tiếng ù, giữ lại âm treble.
3. Band-pass (Thông dải): Chọn lọc dải tần tiếng nói (300Hz - 3.4kHz).
4. Band-stop (Chắn dải): Loại bỏ nhiễu 50Hz.


--------------------------------------------------------------------------------


4. CHƯƠNG 3: THIẾT KẾ BỘ LỌC CÓ ĐÁP ỨNG XUNG HỮU HẠN (FIR)

Bộ lọc FIR luôn ổn định và có khả năng đạt đặc tính pha tuyến tính, điều tối quan trọng trong âm thanh chuyên nghiệp để bảo toàn cấu trúc thời gian của sóng âm.

3.1. Phân loại cấu trúc FIR (Type 1-4)

Dựa trên tính đối xứng của đáp ứng xung h(n) và bậc bộ lọc M, ta có 4 loại:

* Type 1: M chẵn, h(n) đối xứng. Phù hợp cho mọi loại bộ lọc.
* Type 2: M lẻ, h(n) đối xứng. Không dùng làm High-pass do H(\pi) = 0.
* Type 3 & 4: h(n) phản đối xứng. Thường dùng cho các bộ dịch pha 90^\circ (Hilbert transform). Trong MATLAB, các hàm Hr_Type1 đến Hr_Type4 được sử dụng để tính toán đáp ứng biên độ biên độ thực H_r(\omega).

3.2. Phương pháp Thiết kế

* Phương pháp Cửa sổ (Windowing): Sử dụng cửa sổ Hamming để giảm hiện tượng Gibbs. Bậc M được tính từ độ rộng dải quá độ \Delta\omega. Ví dụ: M = \lceil 6.6\pi / \Delta\omega \rceil.
* Phương pháp Parks-McClellan: Sử dụng thuật toán lặp firpm để tối ưu hóa sai số Chebyshev. Phương pháp này cho phép đạt được bậc bộ lọc nhỏ nhất với độ gợn sóng dải thông \delta_1 và độ suy giảm dải chắn \delta_2 đồng nhất (equiripple).


--------------------------------------------------------------------------------


5. CHƯƠNG 4: THIẾT KẾ BỘ LỌC CÓ ĐÁP ỨNG XUNG VÔ HẠN (IIR)

Bộ lọc IIR có cấu trúc đệ quy, cho phép đạt được độ dốc dải thông lớn với bậc bộ lọc thấp, rất hiệu quả trên các chip DSP điểm tĩnh như TMS320C50.

4.1. Chuyển đổi từ Analog sang Digital

* Biến đổi song tuyến (Bilinear): Ánh xạ miền s sang miền z qua công thức s = \frac{2}{T} \frac{1-z^{-1}}{1+z^{-1}}. Phương pháp này khắc phục được hiện tượng trùm phổ (aliasing) nhờ việc nén toàn bộ trục tần số tương tự vào khoảng (-\pi, \pi).
* Bất biến xung (Impulse Invariant): Bảo toàn đáp ứng xung thời gian nhưng dễ bị nhiễu do hiện tượng trùm phổ nếu tín hiệu không có băng thông giới hạn.

4.2. Ánh xạ tần số (Frequency Mapping)

Để thiết kế bộ lọc High-pass hay Band-pass, ta bắt đầu từ bộ lọc Low-pass chuẩn hóa, sau đó sử dụng hàm zmapping.m để thực hiện đổi biến số độc lập trong miền Z, chuyển đổi băng tần mục tiêu một cách chính xác.


--------------------------------------------------------------------------------


6. CHƯƠNG 5: THIẾT KẾ VÀ MÔ PHỎNG TRÊN MATLAB

5.1. Bài toán thiết kế thực tế

Thiết kế bộ lọc thông thấp cho âm thanh với F_s = 44.1 kHz. Thông số chuẩn hóa: \omega_p = 0.2\pi, \omega_s = 0.3\pi. Tính toán tần số vật lý: f_p = \frac{\omega_p \cdot F_s}{2\pi} = \frac{0.2\pi \cdot 44100}{2\pi} = 4.41 kHz. f_s = \frac{0.3\pi \cdot 44100}{2\pi} = 6.615 kHz.

5.2. Triển khai Code và Phân tích

Sử dụng Chebyshev Type I kết hợp Biến đổi song tuyến:

Fs = 44100; T = 1/Fs;
OmegaP = (2/T)*tan(0.2*pi/2);
OmegaS = (2/T)*tan(0.3*pi/2);
[cs, ds] = afd_chb1(OmegaP, OmegaS, 1, 15); % Rp=1dB, As=15dB
[b, a] = bilinear(cs, ds, Fs);
zplane(b, a); % Phân tích tính ổn định


Phân tích đồ thị:

1. Z-plane: Các điểm cực (poles) của bộ lọc IIR nằm hoàn toàn bên trong đường tròn đơn vị (|z| < 1), xác nhận hệ thống ổn định.
2. Magnitude Response: Đạt độ suy giảm tối thiểu 15dB tại dải chắn.
3. Group Delay: Đối với IIR, trễ nhóm không hằng số, gây ra sự sai lệch pha nhẹ giữa các thành phần tần số khác nhau.


--------------------------------------------------------------------------------


7. CHƯƠNG 6: ỨNG DỤNG TRÊN PHẦN CỨNG LAB-VOLT DSP

Hệ thống thí nghiệm Lab-Volt cung cấp môi trường thực tế để kiểm chứng thuật toán trên chip TMS320C50.

6.1. Thành phần hệ thống

* FACET Base Unit: Cung cấp nguồn và hạ tầng kết nối.
* TM320C5x DSK: Chứa chip DSP chủ và bộ tạo dao động ngoài 40MHz (chia đôi thành 20MHz clock nội bộ).
* CODEC (AIC10): Thành phần quan trọng nhất bao gồm:
  * Anti-aliasing Filter: Lọc bỏ các thành phần tần số cao hơn F_s/2 trước khi A/D.
  * A/D & D/A Converter: Chuyển đổi mức điện áp sang mã 16-bit và ngược lại.
  * Post-filter: Làm mượt tín hiệu sau khi tái cấu trúc.

6.2. Quy trình thực nghiệm

Tín hiệu từ micro đi qua Microphone Pre-amplifier để khuếch đại, sau đó vào DSP qua CODEC. Sử dụng môi trường C5x VDE (Visual Development Environment) để nạp file .dsk. Trong bài thí nghiệm ex1_1, việc thay đổi chuyển mạch DIP8 và nhấn nút ngắt (INT#) cho phép điều chỉnh thời gian trễ của hiệu ứng tiếng vọng (echo), minh họa khả năng xử lý thời gian thực của chip.


--------------------------------------------------------------------------------


8. CHƯƠNG 7: SO SÁNH HIỆU NĂNG VÀ ĐÁNH GIÁ KỸ THUẬT

Tiêu chí	Bộ lọc FIR (Parks-McClellan)	Bộ lọc IIR (Bilinear Chebyshev)
Độ phức tạp	Bậc cao (M > 40), cần nhiều MAC.	Bậc thấp (M < 10), tiết kiệm MAC.
Pha	Pha tuyến tính tuyệt đối.	Pha phi tuyến, gây méo thời gian.
Độ ổn định	Luôn ổn định.	Cần kiểm soát vị trí điểm cực.
Ứng dụng	Âm thanh Hi-Fi, xử lý ảnh.	Viễn thông, lọc nhiễu 50Hz.

Biện luận chuyên sâu: Trong các thiết kế dấu phẩy tĩnh 16-bit như TMS320C50, IIR được ưu tiên nhờ hiệu quả tính toán vượt trội (MIPS thấp hơn). Tuy nhiên, FIR là bắt buộc khi cần bảo toàn độ trung thực của âm thanh, tránh hiện tượng lệch pha làm biến dạng cảm thụ thính giác.


--------------------------------------------------------------------------------


9. CHƯƠNG 8: KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN

Báo cáo đã hoàn thành trọn vẹn mục tiêu thiết kế và phân tích bộ lọc số. Chúng ta đã chứng minh được sức mạnh của bộ xử lý TMS320C50 với kiến trúc chuyên biệt cho MAC và khả năng mô phỏng linh hoạt của MATLAB.

Hướng phát triển:

1. Triển khai bộ lọc thích nghi (Adaptive Filter) sử dụng thuật toán LMS để khử tiếng vọng chủ động.
2. Tối ưu hóa thuật toán cho các dòng DSP 32-bit dấu phẩy động (Floating-point) của TI để xử lý âm thanh đa kênh.


--------------------------------------------------------------------------------


10. TÀI LIỆU THAM KHẢO

1. Oppenheim, A. V., & Schafer, R. W. - Digital Signal Processing, Prentice Hall.
2. Proakis, J. G., & Manolakis, D. G. - Digital Signal Processing: Principles, Algorithms, and Applications.
3. Texas Instruments - TMS320C5x User Guide.
4. Lab-Volt Ltd. - Digital Signal Processing Training System Manual.
5. Viện Điện tử - Viễn thông, Bách Khoa Hà Nội - Báo cáo thí nghiệm Xử lý số tín hiệu.
