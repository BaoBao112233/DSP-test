# 100 CÂU HỎI – ĐÁP (CẬP NHẬT THEO CODE VÀ BÁO CÁO MỚI)

Tài liệu này cập nhật theo:

- Code mới có `sampling_demo`, kiểm tra Nyquist, mô phỏng aliasing, xuất ảnh `imgaes/v3`.
- Báo cáo hợp nhất mới: `BaoCao_HopNhat_V1_V2_V3.md`.

Quy ước nhấn mạnh:

- 🔴 **VẤN ĐÁP TRỌNG TÂM**: câu có xác suất cao được hỏi trực tiếp khi bảo vệ.
- Mỗi câu gồm: **Đáp**, **Vì sao**, **Liên kết**.

---

## A. DANH SÁCH 25 CÂU VẤN ĐÁP TRỌNG TÂM (ÔN TRƯỚC)

Các câu nên ưu tiên: **4, 5, 23, 27, 31, 33, 34, 36, 41, 43, 47, 48, 51, 57, 61, 63, 65, 67, 71, 72, 74, 81, 82, 86, 100**.

Lý do: đây là nhóm câu bao phủ đầy đủ chuỗi logic bảo vệ đồ án:
Chuỗi ôn nhanh gồm: lấy mẫu đúng/sai Nyquist; chọn FIR/IIR; tính bậc và tham số; ổn định pole-zero; ứng dụng notch + SNR; kết luận kỹ thuật.

---

## B. 100 CÂU HỎI – ĐÁP CHI TIẾT

### PHẦN 1 — NỀN TẢNG DSP VÀ LẤY MẪU

**Câu 1.** **DSP là gì?**  
**Đáp:** DSP là xử lý số tín hiệu bằng thuật toán trên dữ liệu rời rạc.  
**Vì sao:** Tín hiệu sau số hóa mới xử lý được bằng máy tính.  
**Liên kết:** Nền cho toàn bộ tài liệu.

**Câu 2.** **Tín hiệu âm thanh số là gì?**  
**Đáp:** Tín hiệu analog đã qua lấy mẫu và lượng tử hóa.  
**Vì sao:** Máy tính lưu và xử lý ở dạng số.  
**Liên kết:** Dựa trên câu 1.

**Câu 3.** **`Fs` là gì?**  
**Đáp:** Tần số lấy mẫu, số mẫu/giây.  
**Vì sao:** Quyết định độ phân giải thời gian và giới hạn phổ.  
**Liên kết:** Dẫn đến Nyquist.

**Câu 4.** 🔴 **Định lý Nyquist–Shannon là gì?**  
**Đáp:** Cần $F_s \ge 2f_{max}$.  
**Vì sao:** Nếu thấp hơn sẽ aliasing.  
**Liên kết:** Câu 5, 31, 36.

**Câu 5.** 🔴 **Vì sao với tín hiệu có $f_{max}=3000$ Hz, chọn `Fs=44.1 kHz` là an toàn?**  
**Đáp:** Vì $44100 \gg 2\times3000=6000$ Hz.  
**Vì sao:** Khoảng cách lớn giúp tránh aliasing trong mô phỏng.  
**Liên kết:** Câu 4, 31.

**Câu 6.** **Rời rạc hóa trong code dùng phương pháp gì?**  
**Đáp:** Lấy mẫu đều: $x[n]=x(nT_s)$.  
**Vì sao:** Đây là chuẩn trong DSP.  
**Liên kết:** `modules/sampling_demo.py`.

**Câu 7.** **`Ts` được tính thế nào?**  
**Đáp:** $T_s=1/F_s$.  
**Vì sao:** Định nghĩa nghịch đảo tần số lấy mẫu.  
**Liên kết:** Câu 6.

**Câu 8.** **Tín hiệu gốc mô phỏng gồm những thành phần nào?**  
**Đáp:** 440 Hz, 1000 Hz, 3000 Hz.  
**Vì sao:** Dễ quan sát phổ và kiểm tra Nyquist.  
**Liên kết:** Câu 5.

**Câu 9.** **Alias frequency là gì?**  
**Đáp:** Là tần số sai xuất hiện sau lấy mẫu thiếu.  
**Vì sao:** Thành phần vượt Nyquist bị gấp phổ.  
**Liên kết:** Câu 10.

**Câu 10.** **Trong phản ví dụ `Fs=4 kHz`, thành phần 3 kHz alias về đâu?**  
**Đáp:** Về khoảng 1 kHz.  
**Vì sao:** 3 kHz nằm ngoài Nyquist 2 kHz nên bị gấp.  
**Liên kết:** `alias_frequency()`.

**Câu 11.** **Vì sao cần vẽ cả time-domain và FFT ở phần sampling?**  
**Đáp:** Time-domain cho trực giác mẫu; FFT cho bằng chứng aliasing/phổ.  
**Vì sao:** Hai miền bổ sung nhau.  
**Liên kết:** Hình 01 và 02.

**Câu 12.** **`--no-plots` dùng để làm gì?**  
**Đáp:** Chạy headless, không bật cửa sổ đồ thị.  
**Vì sao:** Thuận tiện debug/CI/server.  
**Liên kết:** CLI chính.

**Câu 13.** **`--save-plots-dir` dùng để làm gì?**  
**Đáp:** Xuất toàn bộ hình ra thư mục chỉ định.  
**Vì sao:** Phục vụ báo cáo và tái lập kết quả.  
**Liên kết:** `imgaes/v3`.

**Câu 14.** **Vì sao bộ ảnh được đánh số 01..09?**  
**Đáp:** Để map thứ tự với luồng phân tích trong báo cáo.  
**Vì sao:** Tránh nhầm khi trích hình.  
**Liên kết:** `BaoCao_HopNhat_V1_V2_V3.md`.

**Câu 15.** **Năng lượng tín hiệu dùng công thức nào?**  
**Đáp:** $E=\sum |x(n)|^2$.  
**Vì sao:** Là chuẩn đo năng lượng rời rạc.  
**Liên kết:** Câu 86 (SNR).

**Câu 16.** **SNR là gì?**  
**Đáp:** Tỷ số năng lượng tín hiệu/nhiễu (dB).  
**Vì sao:** Đánh giá mức “sạch” sau xử lý.  
**Liên kết:** Câu 85–86.

**Câu 17.** **Vì sao 440 Hz thường dùng làm tín hiệu tham chiếu?**  
**Đáp:** Là nốt La chuẩn, dễ nhận diện.  
**Vì sao:** Thuận lợi so sánh trước/sau lọc.  
**Liên kết:** Notch demo.

**Câu 18.** **Khi nào cần anti-aliasing filter trước ADC?**  
**Đáp:** Khi tín hiệu analog có thành phần gần/vượt $F_s/2$.  
**Vì sao:** Lấy mẫu không tự loại nhiễu ngoài dải.  
**Liên kết:** Phần phần cứng DSP.

**Câu 19.** **Phần mềm mô phỏng thay được phần cứng hoàn toàn không?**  
**Đáp:** Không hoàn toàn.  
**Vì sao:** Phần cứng còn có lượng tử hóa, trễ I/O, nhiễu thực.  
**Liên kết:** Chương ứng dụng Lab-Volt.

**Câu 20.** **Mục tiêu chính của khối sampling trong code mới là gì?**  
**Đáp:** Chứng minh đúng/sai Nyquist bằng cả lý thuyết và hình ảnh.  
**Vì sao:** Đây là điểm thường bị hỏi khi vấn đáp.  
**Liên kết:** Câu 4, 10.

---

### PHẦN 2 — THAO TÁC TÍN HIỆU RỜI RẠC VÀ HỆ LTI

**Câu 21.** **`sigshift()` làm gì?**  
**Đáp:** Dịch trục chỉ số của tín hiệu.  
**Vì sao:** Mô phỏng trễ/sớm trong miền rời rạc.  
**Liên kết:** `modules/signal_ops.py`.

**Câu 22.** **`sigfold()` làm gì?**  
**Đáp:** Gấp tín hiệu: $x(n)\to x(-n)$.  
**Vì sao:** Dùng trong phân tích tích chập/đối xứng.  
**Liên kết:** Câu 21.

**Câu 23.** 🔴 **`sigadd()` vì sao dễ sai?**  
**Đáp:** Vì phải căn chỉnh index trước khi cộng.  
**Vì sao:** Lệch `n_start/n_stop` sẽ cộng sai vị trí mẫu.  
**Liên kết:** Debug cơ bản trước khi lọc.

**Câu 24.** **Vì sao dùng `stem` cho tín hiệu rời rạc?**  
**Đáp:** Thể hiện rõ từng mẫu tại từng chỉ số nguyên.  
**Vì sao:** `plot` dễ gây nhầm là liên tục.  
**Liên kết:** Hình 03.

**Câu 25.** **Hệ LTI là gì?**  
**Đáp:** Hệ tuyến tính và bất biến theo thời gian.  
**Vì sao:** Là mô hình chuẩn của đa số bộ lọc số.  
**Liên kết:** Câu 26.

**Câu 26.** **Phương trình sai phân tổng quát có dạng gì?**  
**Đáp:** $y(n)=\sum b_ix(n-i)-\sum a_jy(n-j)$.  
**Vì sao:** Mô tả FIR/IIR theo miền thời gian.  
**Liên kết:** FIR vs IIR.

**Câu 27.** 🔴 **Khác nhau cốt lõi giữa FIR và IIR ở phương trình sai phân?**  
**Đáp:** IIR có hồi tiếp $y(n-j)$, FIR thì không.  
**Vì sao:** Hồi tiếp tạo đáp ứng vô hạn và ảnh hưởng ổn định.  
**Liên kết:** Câu 61–63.

**Câu 28.** **Vì sao cần kiểm tra khối thao tác tín hiệu trước khối lọc?**  
**Đáp:** Vì sai index nền sẽ làm sai mọi kết quả sau.  
**Vì sao:** Lỗi thường lan truyền khó phát hiện.  
**Liên kết:** Câu 23.

**Câu 29.** **`energy()` liên quan gì đến phần ứng dụng notch?**  
**Đáp:** Dùng để tính SNR trước/sau lọc.  
**Vì sao:** Cần số liệu định lượng, không chỉ nhìn đồ thị.  
**Liên kết:** Câu 86.

**Câu 30.** **Ý nghĩa của module hóa ở phần nền DSP?**  
**Đáp:** Có thể test từng khối độc lập.  
**Vì sao:** Giảm chi phí debug và tăng khả năng tái sử dụng.  
**Liên kết:** `demo_runner.py`.

---

### PHẦN 3 — BIẾN ĐỔI Z, POLE-ZERO, ỔN ĐỊNH

**Câu 31.** 🔴 **Hàm truyền đạt rời rạc có dạng nào?**  
**Đáp:** $H(z)=B(z)/A(z)$.  
**Vì sao:** Tử tạo zero, mẫu tạo pole.  
**Liên kết:** Câu 32, 33.

**Câu 32.** **Zero là gì?**  
**Đáp:** Nghiệm của tử số.  
**Vì sao:** Tại đó đáp ứng bằng 0.  
**Liên kết:** Câu 31.

**Câu 33.** 🔴 **Pole là gì và vì sao quan trọng?**  
**Đáp:** Nghiệm của mẫu số; quyết định ổn định và dạng đáp ứng.  
**Vì sao:** Pole gần vòng tròn đơn vị làm hệ nhạy.  
**Liên kết:** Câu 34.

**Câu 34.** 🔴 **Điều kiện ổn định BIBO của hệ rời rạc?**  
**Đáp:** Mọi pole phải có $|p_k|<1$.  
**Vì sao:** Khi đó đáp ứng tự do suy giảm theo thời gian.  
**Liên kết:** Z-plane trong code.

**Câu 35.** **`zplane()` dùng để làm gì?**  
**Đáp:** Vẽ zero, pole và vòng tròn đơn vị.  
**Vì sao:** Kiểm tra ổn định trực quan nhất.  
**Liên kết:** Hình 04.

**Câu 36.** 🔴 **Nếu một pole nằm ngoài vòng tròn đơn vị thì sao?**  
**Đáp:** Hệ mất ổn định.  
**Vì sao:** Đáp ứng tự do tăng theo thời gian.  
**Liên kết:** Câu 34.

**Câu 37.** **`residuez()` cho ta thông tin gì?**  
**Đáp:** Thặng dư, pole, hằng số của khai triển phân thức.  
**Vì sao:** Hỗ trợ hiểu cấu trúc hệ và đáp ứng thời gian.  
**Liên kết:** Câu 31.

**Câu 38.** **Vì sao phải học Z-transform trước IIR?**  
**Đáp:** Vì IIR phụ thuộc mạnh vào vị trí pole.  
**Vì sao:** Không hiểu pole thì khó bảo đảm ổn định.  
**Liên kết:** Câu 63.

**Câu 39.** **Trong demo hiện tại hệ ví dụ Z có ổn định không?**  
**Đáp:** Có, pole nằm trong vòng tròn đơn vị.  
**Vì sao:** Kết quả in ra và hình xác nhận.  
**Liên kết:** Hình 04.

**Câu 40.** **Tại sao nói Z-plane là công cụ vấn đáp “đinh”?**  
**Đáp:** Vì chỉ bằng 1 hình có thể trả lời cả ổn định + đặc tính hệ.  
**Vì sao:** Câu hỏi hội đồng hay đi thẳng vào pole-zero.  
**Liên kết:** 31–36.

---

### PHẦN 4 — PHÂN TÍCH INPUT VÀ THÔNG SỐ THIẾT KẾ

**Câu 41.** 🔴 **Input chính của bài toán low-pass là gì?**  
**Đáp:** Giữ tốt dưới 4.41 kHz, suy giảm mạnh từ 6.615 kHz trở lên.  
**Vì sao:** Từ $\omega_p=0.2\pi$, $\omega_s=0.3\pi$ với $F_s=44.1$ kHz.  
**Liên kết:** Câu 42, 43.

**Câu 42.** **Đổi từ tần số chuẩn hóa sang Hz theo công thức nào?**  
**Đáp:** $f=\omega F_s/(2\pi)$.  
**Vì sao:** Liên hệ giữa miền chuẩn hóa và miền vật lý.  
**Liên kết:** Câu 41.

**Câu 43.** 🔴 **Tính nhanh $f_p$ và $f_s$ từ đề bài?**  
**Đáp:** $f_p=4410$ Hz, $f_s=6615$ Hz.  
**Vì sao:** Thay trực tiếp vào công thức câu 42.  
**Liên kết:** Câu 47.

**Câu 44.** **Dải chuyển tiếp là gì?**  
**Đáp:** Khoảng từ mép dải thông đến mép dải chắn.  
**Vì sao:** Bộ lọc chuyển từ pass sang stop tại đây.  
**Liên kết:** Câu 45.

**Câu 45.** **Dải chuyển tiếp ảnh hưởng gì đến bậc lọc?**  
**Đáp:** Càng hẹp → bậc càng cao.  
**Vì sao:** Cần đáp ứng thay đổi gắt hơn theo tần số.  
**Liên kết:** Câu 48.

**Câu 46.** **`design_analysis` module mới có vai trò gì?**  
**Đáp:** In rõ 3 khối: phân tích input, lý do chọn lọc, tính tham số.  
**Vì sao:** Đúng chuỗi trả lời khi vấn đáp.  
**Liên kết:** `modules/design_analysis.py`.

**Câu 47.** 🔴 **Vì sao FIR Hamming ra bậc 66 trong bài này?**  
**Đáp:** Do $M=\lceil 6.6\pi/\Delta\omega\rceil$ với $\Delta\omega=0.1\pi$.  
**Vì sao:** Đây là công thức xấp xỉ chuẩn cho Hamming.  
**Liên kết:** Câu 48.

**Câu 48.** 🔴 **Tại sao phải làm tròn bậc về dạng phù hợp Type-1?**  
**Đáp:** Để đảm bảo đối xứng và hỗ trợ pha tuyến tính.  
**Vì sao:** FIR Type-1 phù hợp low-pass.  
**Liên kết:** Câu 43, 57.

**Câu 49.** **Trong phần IIR, các thông số `Rp`, `Rs` nghĩa là gì?**  
**Đáp:** Ripple dải thông và suy giảm dải chắn (dB).  
**Vì sao:** Là ràng buộc chất lượng thiết kế.  
**Liên kết:** Câu 67.

**Câu 50.** **Vì sao cần cả số liệu in console và đồ thị?**  
**Đáp:** Console cho số định lượng, đồ thị cho trực quan kiểm chứng.  
**Vì sao:** Hai loại bằng chứng bổ sung nhau.  
**Liên kết:** Toàn pipeline.

---

### PHẦN 5 — FIR: HAMMING & PARKS-MCCLELLAN

**Câu 51.** 🔴 **FIR là gì và ưu điểm lớn nhất là gì?**  
**Đáp:** Bộ lọc đáp ứng hữu hạn; ưu điểm lớn là ổn định và pha tốt.  
**Vì sao:** Không có hồi tiếp nên ổn định cấu trúc.  
**Liên kết:** Câu 61.

**Câu 52.** **Vì sao FIR hợp với âm thanh Hi-Fi?**  
**Đáp:** Vì có thể đạt pha tuyến tính tốt.  
**Vì sao:** Giảm méo dạng sóng theo thời gian.  
**Liên kết:** Câu 43.

**Câu 53.** **Hamming window giải quyết vấn đề gì?**  
**Đáp:** Giảm dao động Gibbs so với cửa sổ chữ nhật.  
**Vì sao:** Làm đáp ứng mượt hơn.  
**Liên kết:** Câu 47.

**Câu 54.** **Parks-McClellan là gì?**  
**Đáp:** Thuật toán thiết kế FIR equiripple tối ưu Chebyshev.  
**Vì sao:** Giảm sai số cực đại theo trọng số dải.  
**Liên kết:** Câu 55, 56.

**Câu 55.** **Trong Python dùng hàm nào cho Parks-McClellan?**  
**Đáp:** `remez()`.  
**Vì sao:** Triển khai chuẩn thuật toán equiripple.  
**Liên kết:** `modules/Thietke_Fir.py`.

**Câu 56.** **`weight` trong `remez` có tác dụng gì?**  
**Đáp:** Ưu tiên sai số giữa passband và stopband.  
**Vì sao:** Điều chỉnh trade-off theo mục tiêu thiết kế.  
**Liên kết:** Câu 54.

**Câu 57.** 🔴 **Vì sao Parks-McClellan trong demo chỉ ~20 bậc còn Hamming 66?**  
**Đáp:** Vì equiripple tối ưu hơn cửa sổ cố định.  
**Vì sao:** Đạt chỉ tiêu với ít hệ số hơn.  
**Liên kết:** Câu 47.

**Câu 58.** **Khi nào chọn Hamming thay vì PM?**  
**Đáp:** Khi cần cách thiết kế đơn giản, dễ giải thích.  
**Vì sao:** PM tối ưu hơn nhưng phức tạp hơn trong trình bày.  
**Liên kết:** Vấn đáp chiến lược.

**Câu 59.** **Khi nào chọn PM thay vì Hamming?**  
**Đáp:** Khi muốn FIR gọn, giảm chi phí tính toán.  
**Vì sao:** Số hệ số thấp hơn rõ rệt.  
**Liên kết:** Câu 57.

**Câu 60.** **Kết luận nhanh phần FIR khi bị hỏi gấp?**  
**Đáp:** FIR cho pha tốt; Hamming dễ triển khai, PM tối ưu hệ số.  
**Vì sao:** Tóm đúng bản chất và trade-off.  
**Liên kết:** 51–59.

---

### PHẦN 6 — IIR CHEBYSHEV TYPE I

**Câu 61.** 🔴 **IIR là gì?**  
**Đáp:** Bộ lọc đáp ứng vô hạn do có hồi tiếp.  
**Vì sao:** Đầu ra phụ thuộc cả đầu ra trước.  
**Liên kết:** Câu 27.

**Câu 62.** **Ưu điểm lớn nhất của IIR trong bài này?**  
**Đáp:** Đạt độ dốc tốt với bậc thấp.  
**Vì sao:** Hiệu quả tính toán cao hơn FIR cùng yêu cầu gần tương đương.  
**Liên kết:** Câu 67.

**Câu 63.** 🔴 **Nhược điểm lớn nhất của IIR?**  
**Đáp:** Pha phi tuyến và nguy cơ mất ổn định.  
**Vì sao:** Pole có thể gây méo pha/không ổn định nếu đặt sai.  
**Liên kết:** Câu 34.

**Câu 64.** **Vì sao chọn Chebyshev Type I thay vì Butterworth?**  
**Đáp:** Vì cho sườn dốc hơn với cùng bậc.  
**Vì sao:** Chấp nhận ripple nhỏ dải thông để tăng độ sắc cạnh.  
**Liên kết:** Câu 65.

**Câu 65.** 🔴 **`cheb1ord()` dùng để làm gì?**  
**Đáp:** Tính bậc tối thiểu thỏa `Rp`, `Rs`.  
**Vì sao:** Tránh chọn bậc thủ công cảm tính.  
**Liên kết:** Câu 67.

**Câu 66.** **`cheby1()` làm gì?**  
**Đáp:** Sinh hệ số bộ lọc Chebyshev Type I.  
**Vì sao:** Từ bậc và tần số cắt để đưa vào lọc số.  
**Liên kết:** Câu 65.

**Câu 67.** 🔴 **Vì sao trong demo bậc IIR là 4?**  
**Đáp:** Do `cheb1ord` với `Rp=1 dB`, `Rs=15 dB` trả về bậc tối thiểu 4.  
**Vì sao:** Đủ thỏa chỉ tiêu đã đặt.  
**Liên kết:** So với FIR 66/20.

**Câu 68.** **Vì sao IIR thường ít hệ số hơn FIR?**  
**Đáp:** Do có hồi tiếp nên “mạnh” hơn về đặc tính phổ.  
**Vì sao:** Đây là bản chất cấu trúc đệ quy.  
**Liên kết:** Câu 62.

**Câu 69.** **`group_delay` cho IIR thường thế nào?**  
**Đáp:** Không hằng theo tần số.  
**Vì sao:** Pha IIR phi tuyến.  
**Liên kết:** Hình 06, 07.

**Câu 70.** **Kết luận nhanh phần IIR khi vấn đáp?**  
**Đáp:** IIR tiết kiệm tài nguyên nhưng đánh đổi pha và yêu cầu kiểm soát ổn định.  
**Vì sao:** Đây là trade-off cốt lõi.  
**Liên kết:** 61–69.

---

### PHẦN 7 — BILINEAR, PRE-WARP, TÍNH THAM SỐ

**Câu 71.** 🔴 **Vì sao nhắc bilinear transform trong báo cáo?**  
**Đáp:** Vì đây là cầu nối analog prototype sang digital filter.  
**Vì sao:** Tránh aliasing của đáp ứng analog khi ánh xạ.  
**Liên kết:** Câu 72.

**Câu 72.** 🔴 **Vì sao cần pre-warp?**  
**Đáp:** Vì bilinear gây méo trục tần số.  
**Vì sao:** Nếu không pre-warp sẽ lệch điểm cắt mong muốn.  
**Liên kết:** Câu 73–74.

**Câu 73.** **Công thức pre-warp là gì?**  
**Đáp:** $\Omega=\frac{2}{T}\tan\left(\frac{\omega}{2}\right)$.  
**Vì sao:** Quan hệ chuẩn của bilinear.  
**Liên kết:** Câu 72.

**Câu 74.** 🔴 **Trong đề tài, $\Omega_p$, $\Omega_s$ xấp xỉ bao nhiêu?**  
**Đáp:** $\Omega_p\approx28657.92$ rad/s, $\Omega_s\approx44940.14$ rad/s.  
**Vì sao:** Thay số từ $F_s=44.1$ kHz, $\omega_p=0.2\pi$, $\omega_s=0.3\pi$.  
**Liên kết:** Câu 43.

**Câu 75.** **Vì sao code vẫn in pre-warp dù thiết kế digital trực tiếp được?**  
**Đáp:** Để bám sát logic lý thuyết và MATLAB trong báo cáo.  
**Vì sao:** Giúp giải thích rõ khi bảo vệ.  
**Liên kết:** `design_analysis.py`.

**Câu 76.** **Tham số nào điều khiển độ sắc cạnh lọc?**  
**Đáp:** Dải chuyển tiếp và ràng buộc ripple/suy giảm.  
**Vì sao:** Chúng quyết định độ dốc cần đạt.  
**Liên kết:** Câu 45.

**Câu 77.** **Vì sao đổi từ chuẩn hóa sang Hz là bước bắt buộc?**  
**Đáp:** Để diễn giải vật lý đúng với bài toán âm thanh.  
**Vì sao:** Hội đồng thường hỏi bằng Hz, không hỏi bằng $\pi$.  
**Liên kết:** Câu 42–43.

**Câu 78.** **Khi nào cần dùng thêm frequency mapping?**  
**Đáp:** Khi cần đổi low-pass chuẩn sang high-pass/band-pass/band-stop.  
**Vì sao:** Dựa trên biến đổi miền tần số của mẫu thiết kế.  
**Liên kết:** Phần lý thuyết Report.

**Câu 79.** **Nếu dải chuyển tiếp thu hẹp một nửa thì chuyện gì thường xảy ra?**  
**Đáp:** Bậc lọc cần tăng đáng kể.  
**Vì sao:** Yêu cầu đáp ứng gắt hơn trong miền tần số.  
**Liên kết:** Câu 45, 76.

**Câu 80.** **Kết luận phần tham số khi trả lời vấn đáp?**  
**Đáp:** Luôn đi theo chuỗi: đề bài → chuẩn hóa → Hz → (nếu IIR) pre-warp → bậc tối thiểu.  
**Vì sao:** Trả lời theo quy trình sẽ thuyết phục và ít sót.  
**Liên kết:** 41–79.

---

### PHẦN 8 — ỨNG DỤNG NOTCH 50 HZ VÀ ECHO

**Câu 81.** 🔴 **Vì sao không dùng low-pass để khử nhiễu 50 Hz?**  
**Đáp:** Vì nhiễu là hẹp băng tại 50 Hz, low-pass không tối ưu.  
**Vì sao:** Có thể giữ nhầm 50 Hz hoặc làm mất thành phần hữu ích khác.  
**Liên kết:** Câu 82.

**Câu 82.** 🔴 **Vì sao notch là lựa chọn đúng cho nhiễu điện lưới?**  
**Đáp:** Chặn rất hẹp quanh 50 Hz, bảo toàn phần phổ còn lại.  
**Vì sao:** Tối ưu cho nhiễu đơn tần.  
**Liên kết:** Hình 08.

**Câu 83.** **`Q` trong notch filter là gì?**  
**Đáp:** Hệ số chất lượng, quyết định độ hẹp notch.  
**Vì sao:** `Q` lớn → notch hẹp; `Q` nhỏ → notch rộng.  
**Liên kết:** Câu 84.

**Câu 84.** **Vì sao demo chọn `Q=30`?**  
**Đáp:** Cân bằng giữa khử đúng 50 Hz và không “ăn” dải lân cận.  
**Vì sao:** Phù hợp bài toán minh họa thực tế.  
**Liên kết:** Câu 83.

**Câu 85.** **SNR trước/sau lọc trong demo là bao nhiêu?**  
**Đáp:** Trước ~4.37 dB, sau ~11.33 dB.  
**Vì sao:** Thành phần nhiễu 50 Hz giảm mạnh.  
**Liên kết:** Câu 86.

**Câu 86.** 🔴 **Vì sao SNR tăng chứng minh bộ lọc hiệu quả?**  
**Đáp:** Vì tỷ lệ năng lượng tín hiệu/nhiễu được cải thiện định lượng.  
**Vì sao:** Không chỉ “nhìn thấy đẹp” mà có số đo khách quan.  
**Liên kết:** Câu 15, 16.

**Câu 87.** **Vì sao phải xem cả waveform và FFT trong notch demo?**  
**Đáp:** Waveform cho dạng sóng, FFT cho vị trí tần số nhiễu.  
**Vì sao:** Hai miền xác nhận lẫn nhau.  
**Liên kết:** Hình 08.

**Câu 88.** **`simulate_echo()` dùng mô hình nào?**  
**Đáp:** $y(n)=x(n)+\alpha x(n-D)$.  
**Vì sao:** Mô hình echo rời rạc chuẩn, đơn giản và trực quan.  
**Liên kết:** Hình 09.

**Câu 89.** **Tăng `delay_ms` ảnh hưởng gì?**  
**Đáp:** Tiếng vọng xuất hiện muộn hơn.  
**Vì sao:** Số mẫu trễ $D$ tăng.  
**Liên kết:** Câu 88.

**Câu 90.** **Tăng `decay` ảnh hưởng gì?**  
**Đáp:** Tiếng vọng mạnh hơn.  
**Vì sao:** Hệ số nhân nhánh trễ lớn hơn.  
**Liên kết:** Câu 88.

---

### PHẦN 9 — KIẾN TRÚC CODE, BÁO CÁO VÀ TÁI LẬP KẾT QUẢ

**Câu 91.** **Vì sao phải tách module thay vì 1 file lớn?**  
**Đáp:** Dễ debug, test, và mở rộng chức năng.  
**Vì sao:** Giảm phụ thuộc chéo và giảm phạm vi lỗi.  
**Liên kết:** `modules/*`.

**Câu 92.** **`demo_runner.py` đóng vai trò gì?**  
**Đáp:** Orchestrator gọi toàn bộ demo theo thứ tự logic.  
**Vì sao:** Tạo pipeline nhất quán từ đầu đến cuối.  
**Liên kết:** Luồng báo cáo hợp nhất.

**Câu 93.** **`plot_config.py` ngoài style còn làm gì mới?**  
**Đáp:** Hỗ trợ lưu ảnh bằng `build_save_path` và `finalize_figure(save_path=...)`.  
**Vì sao:** Tự động hóa tạo tài liệu hình ảnh.  
**Liên kết:** `--save-plots-dir`.

**Câu 94.** **Bộ ảnh `imgaes/v3` dùng cho mục đích gì?**  
**Đáp:** Là minh chứng trực quan gắn thẳng vào báo cáo khoa học.  
**Vì sao:** Tăng tính tái lập và kiểm chứng.  
**Liên kết:** BaoCao V3 và bản hợp nhất.

**Câu 95.** **Vì sao báo cáo hợp nhất bỏ phần 9,10 cũ mà vẫn hợp lý?**  
**Đáp:** Vì nội dung kết luận/tài liệu tham khảo được đánh lại số và vẫn đủ logic khoa học.  
**Vì sao:** Không mất thông tin cốt lõi kỹ thuật.  
**Liên kết:** `BaoCao_HopNhat_V1_V2_V3.md`.

**Câu 96.** **Quy trình tạo HTML/PDF từ Markdown trong dự án hiện tại là gì?**  
**Đáp:** Markdown → HTML (Python markdown) → PDF (WeasyPrint).  
**Vì sao:** `pandoc` không có sẵn nên dùng tuyến thay thế khả dụng.  
**Liên kết:** File hợp nhất PDF.

**Câu 97.** **Khi bị hỏi “làm sao tái lập kết quả”, trả lời ngắn gọn thế nào?**  
**Đáp:** Chạy `python dsp_audio_filter.py --no-plots --save-plots-dir imgaes/v3`, sau đó build báo cáo MD→HTML→PDF.  
**Vì sao:** Đủ để tái sinh số liệu và ảnh.  
**Liên kết:** Câu 93, 96.

**Câu 98.** **Nếu hội đồng hỏi “đóng góp mới của bản code hiện tại là gì”, trả lời gì?**  
**Đáp:** Có sampling+Nyquist+aliasing, module hóa rõ, xuất ảnh tự động, báo cáo hợp nhất tái lập.  
**Vì sao:** Đây là khác biệt rõ so với bản MATLAB mô tả thuần lý thuyết.  
**Liên kết:** So sánh V1–V3.

**Câu 99.** **Nếu bị hỏi “hạn chế hiện tại”, nên nói gì?**  
**Đáp:** Chưa chạy real-time trên DSP thật, chưa benchmark fixed-point, chưa xử lý WAV đa kênh đầy đủ.  
**Vì sao:** Nêu đúng giới hạn giúp phần phản biện thuyết phục hơn.  
**Liên kết:** Hướng phát triển.

**Câu 100.** 🔴 **Câu chốt khi vấn đáp: “Toàn bộ quy trình kỹ thuật của đề tài là gì?”**  
**Đáp:**  
(1) Phân tích input và điều kiện lấy mẫu;  
(2) rời rạc hóa và kiểm tra Nyquist/aliasing;  
(3) thiết kế FIR/IIR theo thông số;  
(4) kiểm tra ổn định và đáp ứng;  
(5) ứng dụng notch/echo và đo SNR;  
(6) xuất ảnh + hợp nhất báo cáo để tái lập.  
**Vì sao:** Đây là chuỗi từ bài toán đến bằng chứng định lượng và tài liệu khoa học.  
**Liên kết:** Tổng kết toàn bộ 99 câu trước.

---

## C. MẸO TRẢ LỜI VẤN ĐÁP NHANH (30–45 GIÂY/CÂU)

- Mẫu trả lời tốt: **Định nghĩa ngắn → công thức/tiêu chí → số liệu của đề tài → kết luận**.
- Với câu tính toán: luôn nói rõ đơn vị (Hz, rad/s, dB).
- Với câu so sánh FIR/IIR: luôn nói theo dạng **trade-off**, tránh kết luận tuyệt đối.
- Với câu ứng dụng: luôn nêu cả **hình** và **chỉ số** (ví dụ SNR).
- Câu khó bị truy sâu nhất thường là: **Nyquist, bậc lọc, pole-zero ổn định, lý do chọn notch**.

---

## D. PHẦN CHUYÊN SÂU (DÙNG KHI HỘI ĐỒNG HỎI TRUY SÂU)

### D.1 12 câu truy sâu rất hay gặp

1) **Nếu $F_s > 2f_{max}$ rồi thì có chắc chắn không aliasing ngoài thực tế?**  
**Đáp sâu:** Chưa chắc, vì điều kiện đó chỉ đúng khi tín hiệu analog đã bị giới hạn băng trước ADC. Nếu front-end không có anti-aliasing filter thì thành phần ngoài dải vẫn gấp phổ vào băng quan sát.  
**Điểm ăn điểm:** Nêu rõ vai trò của khối anti-aliasing trong chuỗi đo.

2) **Vì sao IIR bậc thấp nhưng vẫn đạt dốc tốt?**  
**Đáp sâu:** Do cơ chế hồi tiếp tạo cực gần vòng tròn đơn vị, làm biên độ biến thiên mạnh theo tần số quanh vùng cắt. Đổi lại, pha phi tuyến tăng và hệ nhạy hơn với sai số hệ số.

3) **Tại sao FIR thường được gọi là “an toàn hơn” trong audio?**  
**Đáp sâu:** Không hồi tiếp nên ổn định cấu trúc; có thể ép đối xứng hệ số để gần pha tuyến tính, giảm méo dạng sóng trong miền thời gian.

4) **Nếu yêu cầu stopband tăng từ 15 dB lên 40 dB thì chuyện gì xảy ra?**  
**Đáp sâu:** Bậc lọc tăng (đặc biệt với FIR), chi phí MAC tăng, độ trễ nhóm tăng. Đây là trade-off giữa chất lượng lọc và tài nguyên tính toán.

5) **Vì sao phải quan tâm group delay thay vì chỉ magnitude?**  
**Đáp sâu:** Magnitude chỉ cho biết giữ/chặn biên độ, còn group delay cho biết biến dạng pha theo tần số. Audio nghe “méo” có thể do pha dù biên độ đạt chuẩn.

6) **Parks-McClellan “tối ưu” theo nghĩa nào?**  
**Đáp sâu:** Tối ưu chuẩn minimax (Chebyshev): cực tiểu hóa sai số lớn nhất có trọng số giữa các dải tần.

7) **Sự khác nhau giữa pre-warp và đổi đơn vị tần số?**  
**Đáp sâu:** Đổi đơn vị chỉ là chuyển chuẩn hóa ↔ Hz; pre-warp là hiệu chỉnh phi tuyến tần số trước bilinear để bù méo trục tần số.

8) **Vì sao notch phù hợp hơn low-pass cho nhiễu 50 Hz?**  
**Đáp sâu:** Vì nhiễu đơn tần/hẹp băng. Notch tác động cục bộ quanh 50 Hz nên bảo toàn phổ hữu ích tốt hơn lọc toàn dải.

9) **SNR tăng có đủ kết luận bộ lọc tốt chưa?**  
**Đáp sâu:** Chưa đủ. Cần nhìn thêm phổ FFT, độ méo pha, và cảm nhận theo ứng dụng (audio perceptual quality).

10) **Nếu hội đồng hỏi “độ phức tạp tính toán” thì trả lời sao?**  
**Đáp sâu:** So theo số phép nhân-cộng mỗi mẫu. FIR bậc $M$ cần xấp xỉ $M+1$ MAC/mẫu; IIR bậc thấp thường ít MAC hơn nhưng cần kiểm soát ổn định/sai số số học.

11) **Khi nào kết quả mô phỏng khác phần cứng DSP thực?**  
**Đáp sâu:** Khi có lượng tử hóa fixed-point, bão hòa số, trễ I/O, nhiễu đồng hồ, hoặc sai khác front-end analog.

12) **Điểm chốt học thuật để bảo vệ đồ án này là gì?**  
**Đáp sâu:** Khả năng chứng minh nhất quán 4 lớp: lý thuyết → tham số thiết kế → đồ thị kiểm chứng → chỉ số định lượng (SNR/ổn định/bậc lọc).

### D.2 Công thức trọng điểm nên thuộc

1. **Nyquist:** $F_s \ge 2f_{max}$  
2. **Rời rạc hóa:** $x[n]=x(nT_s),\; T_s=1/F_s$  
3. **Đổi chuẩn hóa sang Hz:** $f=\omega F_s/(2\pi)$  
4. **Hàm truyền đạt:** $H(z)=B(z)/A(z)$  
5. **Ổn định rời rạc:** $|p_k|<1$  
6. **Pre-warp:** $\Omega=\frac{2}{T}\tan(\omega/2)$  
7. **Hamming bậc gần đúng:** $M\approx\left\lceil\frac{6.6\pi}{\Delta\omega}\right\rceil$  
8. **Echo:** $y(n)=x(n)+\alpha x(n-D)$

### D.3 8 lỗi trả lời thường bị trừ điểm

1. Nói “$F_s$ cao là đủ” nhưng quên anti-aliasing analog.  
2. Chỉ nói magnitude, bỏ qua phase/group delay.  
3. Nhầm giữa “ổn định theo pole” và “độ dốc theo magnitude”.  
4. Nói FIR luôn “tốt hơn” IIR hoặc ngược lại (kết luận tuyệt đối).  
5. Không nêu đơn vị khi tính toán (Hz, rad/s, dB).  
6. Không gắn số liệu đề tài khi trả lời lý thuyết.  
7. Nói notch tốt nhưng không chứng minh bằng FFT/SNR.  
8. Trả lời dài nhưng thiếu cấu trúc định nghĩa → công thức → số liệu → kết luận.

### D.4 Mẫu trả lời 20 giây cho 3 câu hay bị hỏi nhất

**Mẫu 1 – Nyquist:**  
“Trong đề tài, tín hiệu có $f_{max}=3$ kHz nên theo Nyquist cần $F_s\ge6$ kHz. Em dùng $F_s=44.1$ kHz nên thỏa điều kiện rất an toàn; đồng thời em có phản ví dụ $F_s=4$ kHz để chứng minh aliasing xuất hiện ở FFT.”

**Mẫu 2 – Vì sao chọn IIR Chebyshev:**  
“Em chọn IIR Chebyshev Type I vì cần bậc thấp để tiết kiệm MAC trên DSP fixed-point. Với ràng buộc $R_p=1$ dB, $R_s=15$ dB thì `cheb1ord` cho bậc tối thiểu $N=4$, đáp ứng độ dốc tốt nhưng chấp nhận pha phi tuyến.”

**Mẫu 3 – Vì sao chọn notch 50 Hz:**  
“Nhiễu là đơn tần tại 50 Hz nên notch là đúng bản chất bài toán hơn low-pass. Kết quả em chứng minh bằng cả phổ FFT và SNR: từ ~4.37 dB lên ~11.33 dB sau lọc.”
