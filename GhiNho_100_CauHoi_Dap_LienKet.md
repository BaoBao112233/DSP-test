# 100 CÂU HỎI - ĐÁP CÓ GIẢI THÍCH VÀ LIÊN KẾT KIẾN THỨC

Tài liệu này đi từ dễ đến khó. Mỗi câu trả lời có 2 phần:
- **Vì sao:** giải thích bản chất
- **Liên kết:** chỉ ra câu trước hoặc ý trước cần nhớ để trả lời chính xác

---

## PHẦN A — NỀN TẢNG DSP

1. **Hỏi:** DSP là gì?  
   **Đáp:** DSP là xử lý số tín hiệu, tức dùng thuật toán số để phân tích và biến đổi tín hiệu.  
   **Vì sao:** Sau khi tín hiệu được số hóa, mọi phép lọc và phân tích đều trở thành phép toán trên dãy số.  
   **Liên kết:** Đây là nền tảng để hiểu mọi câu sau.

2. **Hỏi:** Tín hiệu âm thanh số là gì?  
   **Đáp:** Là tín hiệu âm thanh đã được lấy mẫu và lượng tử hóa thành các giá trị rời rạc.  
   **Vì sao:** Máy tính không xử lý trực tiếp tín hiệu analog liên tục mà xử lý các mẫu số.  
   **Liên kết:** Dựa trên câu 1.

3. **Hỏi:** Tần số lấy mẫu `Fs` là gì?  
   **Đáp:** Là số mẫu lấy được trong 1 giây.  
   **Vì sao:** `Fs` quyết định độ phân giải theo thời gian và giới hạn phổ có thể biểu diễn.  
   **Liên kết:** Cần để hiểu định lý Nyquist ở câu 4.

4. **Hỏi:** Định lý Nyquist nói gì?  
   **Đáp:** `Fs` phải lớn hơn hoặc bằng 2 lần tần số cao nhất của tín hiệu.  
   **Vì sao:** Nếu không sẽ xảy ra aliasing.  
   **Liên kết:** Dựa trên câu 3.

5. **Hỏi:** Vì sao audio thường dùng `Fs = 44.1 kHz`?  
   **Đáp:** Vì nó cho phép biểu diễn phổ tới 22.05 kHz, đủ cho tai người trong đa số tình huống.  
   **Vì sao:** 22.05 kHz là một nửa của 44.1 kHz theo Nyquist.  
   **Liên kết:** Kết hợp câu 3 và câu 4.

6. **Hỏi:** Tín hiệu rời rạc thường ký hiệu thế nào?  
   **Đáp:** Thường ký hiệu là $x(n)$.  
   **Vì sao:** `n` là chỉ số mẫu nguyên.  
   **Liên kết:** Dùng xuyên suốt trong code.

7. **Hỏi:** Năng lượng tín hiệu là gì?  
   **Đáp:** Là tổng bình phương độ lớn các mẫu: $E=\sum |x(n)|^2$.  
   **Vì sao:** Đây là cách đo mức năng lượng tích lũy của tín hiệu rời rạc.  
   **Liên kết:** Liên quan trực tiếp tới hàm `energy()` trong code.

8. **Hỏi:** Trong code, `energy()` dùng để làm gì?  
   **Đáp:** Dùng để tính năng lượng của tín hiệu, đặc biệt trong so sánh SNR.  
   **Vì sao:** SNR cần tỷ lệ giữa năng lượng tín hiệu và nhiễu.  
   **Liên kết:** Dựa trên câu 7.

9. **Hỏi:** Bộ lọc số là gì?  
   **Đáp:** Là hệ thống biến đổi tín hiệu số nhằm giữ lại hoặc loại bỏ một số thành phần tần số.  
   **Vì sao:** Trong âm thanh, ta thường muốn bỏ nhiễu hoặc giữ dải hữu ích.  
   **Liên kết:** Kết nối từ DSP cơ bản sang thiết kế lọc.

10. **Hỏi:** Vì sao bộ lọc số quan trọng trong âm thanh?  
   **Đáp:** Vì âm thanh thường bị nhiễu, méo hoặc chứa thành phần không mong muốn cần loại bỏ.  
   **Vì sao:** Bộ lọc cho phép điều khiển phổ tín hiệu chính xác hơn mạch analog.  
   **Liên kết:** Dựa trên câu 9.

---

## PHẦN B — CÁC PHÉP TOÁN TÍN HIỆU CƠ BẢN

11. **Hỏi:** `sigshift()` làm gì?  
   **Đáp:** Dịch tín hiệu theo trục chỉ số.  
   **Vì sao:** Trong DSP, nhiều phép biến đổi chỉ làm thay đổi thời điểm xuất hiện của mẫu.  
   **Liên kết:** Áp dụng cho tín hiệu $x(n)$ từ câu 6.

12. **Hỏi:** Vì sao dịch tín hiệu không làm đổi biên độ?  
   **Đáp:** Vì chỉ số thay đổi, còn giá trị mẫu giữ nguyên.  
   **Vì sao:** Dịch là phép biến đổi theo thời gian, không phải phép khuếch đại.  
   **Liên kết:** Mở rộng từ câu 11.

13. **Hỏi:** `sigfold()` làm gì?  
   **Đáp:** Biến $x(n)$ thành $x(-n)$.  
   **Vì sao:** Đây là phép gấp tín hiệu theo trục thời gian.  
   **Liên kết:** Thường học cùng phép dịch ở câu 11.

14. **Hỏi:** Vì sao phép gấp hữu ích?  
   **Đáp:** Vì nó xuất hiện trong tích chập và phân tích đối xứng.  
   **Vì sao:** Nhiều phép toán hệ LTI cần nhìn tín hiệu ở dạng đảo thời gian.  
   **Liên kết:** Dựa trên câu 13.

15. **Hỏi:** `sigadd()` làm gì?  
   **Đáp:** Cộng hai tín hiệu có thể khác trục chỉ số.  
   **Vì sao:** Hai dãy muốn cộng đúng phải được đặt lên cùng một miền chỉ số.  
   **Liên kết:** Kết hợp hiểu biết ở câu 11 và câu 13.

16. **Hỏi:** Vì sao `sigadd()` là chỗ dễ lỗi?  
   **Đáp:** Vì nếu căn sai `n_start` hoặc `n_stop` thì mẫu sẽ lệch vị trí.  
   **Vì sao:** Đây là lỗi index điển hình khi xử lý tín hiệu rời rạc.  
   **Liên kết:** Mở rộng trực tiếp từ câu 15.

17. **Hỏi:** Vì sao chương trình dùng `stem()` thay vì `plot()` ở phần này?  
   **Đáp:** Vì tín hiệu rời rạc nên hiển thị bằng cọc mẫu rõ bản chất hơn.  
   **Vì sao:** `plot()` làm tín hiệu trông như liên tục, dễ gây nhầm.  
   **Liên kết:** Liên hệ cách biểu diễn ở câu 6.

18. **Hỏi:** Vì sao cần học các phép dịch, gấp, cộng trước khi thiết kế lọc?  
   **Đáp:** Vì đó là nền tảng để hiểu hệ LTI và đáp ứng xung.  
   **Vì sao:** Bộ lọc số thực chất là biến đổi tín hiệu rời rạc theo quy luật xác định.  
   **Liên kết:** Tổng hợp câu 11 đến 17.

19. **Hỏi:** Dịch và gấp có làm đổi năng lượng không?  
   **Đáp:** Không, trong trường hợp chỉ đổi vị trí mẫu.  
   **Vì sao:** Tập giá trị biên độ không thay đổi.  
   **Liên kết:** Gắn với khái niệm năng lượng ở câu 7.

20. **Hỏi:** Chương 1 của code nhằm mục đích gì?  
   **Đáp:** Xác nhận các thao tác tín hiệu rời rạc hoạt động đúng trước khi sang phần lọc.  
   **Vì sao:** Nếu phần nền sai, mọi bước phân tích sau sẽ sai theo.  
   **Liên kết:** Tổng kết phần B.

---

## PHẦN C — BIẾN ĐỔI Z VÀ HỆ LTI

21. **Hỏi:** Hệ LTI là gì?  
   **Đáp:** Là hệ tuyến tính và bất biến theo thời gian.  
   **Vì sao:** Đây là lớp hệ quan trọng nhất trong DSP vì dễ phân tích và thiết kế.  
   **Liên kết:** Là cầu nối sang biến đổi Z.

22. **Hỏi:** Vì sao hệ LTI quan trọng trong bộ lọc số?  
   **Đáp:** Vì bộ lọc số tiêu chuẩn thường được mô hình hóa là hệ LTI.  
   **Vì sao:** Khi đó có thể dùng đáp ứng xung, hàm truyền và phổ để phân tích.  
   **Liên kết:** Dựa trên câu 21.

23. **Hỏi:** Biến đổi Z dùng để làm gì?  
   **Đáp:** Dùng để đưa hệ rời rạc sang miền phức nhằm phân tích thuận tiện hơn.  
   **Vì sao:** Trong miền Z, phương trình sai phân trở thành dạng đại số.  
   **Liên kết:** Kế tiếp câu 21 và 22.

24. **Hỏi:** Hàm truyền đạt rời rạc có dạng gì?  
   **Đáp:** $H(z)=\frac{B(z)}{A(z)}$.  
   **Vì sao:** Tử số tạo zero, mẫu số tạo pole.  
   **Liên kết:** Dẫn sang câu 25 và 26.

25. **Hỏi:** Zero là gì?  
   **Đáp:** Là nghiệm của tử số.  
   **Vì sao:** Tại đó đáp ứng bằng 0.  
   **Liên kết:** Dựa trên câu 24.

26. **Hỏi:** Pole là gì?  
   **Đáp:** Là nghiệm của mẫu số.  
   **Vì sao:** Vị trí pole quyết định mạnh đến ổn định và dạng đáp ứng.  
   **Liên kết:** Dựa trên câu 24.

27. **Hỏi:** Điều kiện ổn định của hệ rời rạc là gì?  
   **Đáp:** Mọi pole phải nằm trong vòng tròn đơn vị.  
   **Vì sao:** Khi đó đáp ứng tự do suy giảm theo thời gian.  
   **Liên kết:** Gắn trực tiếp với câu 26.

28. **Hỏi:** `zplane()` trong code làm gì?  
   **Đáp:** Vẽ zero, pole và vòng tròn đơn vị.  
   **Vì sao:** Đây là cách trực quan nhất để kiểm tra ổn định.  
   **Liên kết:** Dựa trên câu 25 đến 27.

29. **Hỏi:** `residuez()` dùng để làm gì?  
   **Đáp:** Phân tích hàm truyền thành tổng các phân thức đơn giản.  
   **Vì sao:** Điều này giúp hiểu cấu trúc cực và đáp ứng thời gian của hệ.  
   **Liên kết:** Liên hệ với câu 23 và 24.

30. **Hỏi:** Vì sao phải học Z-plane trước khi sang IIR?  
   **Đáp:** Vì IIR phụ thuộc mạnh vào vị trí pole.  
   **Vì sao:** Nếu không hiểu pole thì khó đánh giá ổn định.  
   **Liên kết:** Tổng kết phần C.

---

## PHẦN D — PHÂN TÍCH INPUT CHO BÀI TOÁN

31. **Hỏi:** Input chính của bài toán low-pass là gì?  
   **Đáp:** Là tín hiệu audio được giả thiết cần giữ dưới 4.41 kHz và suy giảm trên 6.615 kHz.  
   **Vì sao:** Các ngưỡng này đến từ $\omega_p=0.2\pi$ và $\omega_s=0.3\pi$.  
   **Liên kết:** Kết hợp khái niệm `Fs` từ phần A với thiết kế lọc.

32. **Hỏi:** Làm sao đổi từ $\omega_p$ sang Hz?  
   **Đáp:** Dùng $f=\frac{\omega F_s}{2\pi}$.  
   **Vì sao:** Đây là liên hệ giữa tần số chuẩn hóa và tần số vật lý.  
   **Liên kết:** Cần để hiểu câu 31.

33. **Hỏi:** Với `Fs=44.1 kHz`, $\omega_p=0.2\pi$ cho ra bao nhiêu?  
   **Đáp:** $f_p=4410$ Hz.  
   **Vì sao:** Thay trực tiếp vào công thức ở câu 32.  
   **Liên kết:** Tiếp nối câu 32.

34. **Hỏi:** Với `Fs=44.1 kHz`, $\omega_s=0.3\pi$ cho ra bao nhiêu?  
   **Đáp:** $f_s=6615$ Hz.  
   **Vì sao:** Tương tự cách tính ở câu 33.  
   **Liên kết:** Cặp với câu 33.

35. **Hỏi:** Dải chuyển tiếp là gì?  
   **Đáp:** Là khoảng giữa mép dải thông và mép dải chắn.  
   **Vì sao:** Ở đó bộ lọc chuyển từ trạng thái cho qua sang chặn.  
   **Liên kết:** Dựa trên câu 33 và 34.

36. **Hỏi:** Vì sao dải chuyển tiếp quan trọng?  
   **Đáp:** Vì dải càng hẹp thì bộ lọc càng khó thiết kế và thường cần bậc cao hơn.  
   **Vì sao:** Bộ lọc phải thay đổi đáp ứng nhanh hơn theo tần số.  
   **Liên kết:** Sẽ liên quan trực tiếp đến bậc lọc ở các phần sau.

37. **Hỏi:** Input của bài toán notch demo là gì?  
   **Đáp:** Là sin 440 Hz cộng nhiễu 50 Hz và nhiễu Gaussian nhỏ.  
   **Vì sao:** Đây là mô hình đơn giản nhưng sát với nhiễu điện lưới thực tế.  
   **Liên kết:** Khác với bài toán low-pass tổng quát ở câu 31.

38. **Hỏi:** Vì sao 440 Hz được chọn làm tín hiệu hữu ích?  
   **Đáp:** Vì đó là tần số chuẩn dễ nhận biết trong âm nhạc.  
   **Vì sao:** Khi xem phổ, đỉnh 440 Hz rất dễ so với đỉnh 50 Hz.  
   **Liên kết:** Hỗ trợ phân tích câu 37.

39. **Hỏi:** Vì sao 50 Hz là nhiễu điển hình?  
   **Đáp:** Vì nhiều hệ điện lưới hoạt động ở 50 Hz.  
   **Vì sao:** Nhiễu điện lưới thường ghép vào microphone, dây dẫn hoặc nguồn cấp.  
   **Liên kết:** Cần để chọn notch ở phần sau.

40. **Hỏi:** Tóm lại cần nhận diện input thế nào trước khi chọn lọc?  
   **Đáp:** Phải biết phổ tín hiệu hữu ích nằm ở đâu, nhiễu nằm ở đâu và mục tiêu bảo toàn là gì.  
   **Vì sao:** Chọn sai bộ lọc sẽ loại cả tín hiệu tốt.  
   **Liên kết:** Tổng kết phần D.

---

## PHẦN E — FIR VÀ LÝ DO CHỌN

41. **Hỏi:** FIR là gì?  
   **Đáp:** Là bộ lọc có đáp ứng xung hữu hạn.  
   **Vì sao:** Đầu ra chỉ phụ thuộc vào số hữu hạn mẫu vào trước đó.  
   **Liên kết:** Dùng để đối chiếu với IIR sau này.

42. **Hỏi:** Vì sao FIR luôn ổn định?  
   **Đáp:** Vì không có hồi tiếp.  
   **Vì sao:** Không có cơ chế làm đáp ứng tăng vô hạn theo thời gian.  
   **Liên kết:** So sánh với IIR ở phần G.

43. **Hỏi:** Vì sao FIR phù hợp cho audio Hi-Fi?  
   **Đáp:** Vì FIR có thể có pha tuyến tính.  
   **Vì sao:** Pha tuyến tính làm các thành phần tần số bị trễ tương đối đồng đều.  
   **Liên kết:** Dựa trên mục tiêu bảo toàn tín hiệu ở phần D.

44. **Hỏi:** Pha tuyến tính quan trọng thế nào?  
   **Đáp:** Nó giảm méo dạng sóng trong miền thời gian.  
   **Vì sao:** Các thành phần phổ không bị lệch nhau quá nhiều sau lọc.  
   **Liên kết:** Giải thích sâu hơn cho câu 43.

45. **Hỏi:** Vì sao code có `design_fir_hamming()`?  
   **Đáp:** Để thiết kế FIR bằng phương pháp cửa sổ Hamming.  
   **Vì sao:** Đây là phương pháp cơ bản, dễ hiểu và sát tài liệu học.  
   **Liên kết:** Là bước thực thi cho khái niệm ở câu 41 đến 44.

46. **Hỏi:** Vì sao chọn cửa sổ Hamming?  
   **Đáp:** Vì nó giảm dao động Gibbs tốt hơn cửa sổ chữ nhật.  
   **Vì sao:** Điều này giúp đáp ứng mượt hơn trong thực tế.  
   **Liên kết:** Mở rộng câu 45.

47. **Hỏi:** Bậc FIR Hamming được tính thế nào?  
   **Đáp:** Theo công thức $M=\lceil 6.6\pi/\Delta\omega \rceil$.  
   **Vì sao:** Đây là công thức xấp xỉ thường dùng cho cửa sổ Hamming.  
   **Liên kết:** Dựa trên dải chuyển tiếp ở câu 35 và 36.

48. **Hỏi:** Vì sao với đề bài này `M = 66`?  
   **Đáp:** Vì $\Delta\omega = 0.1\pi$, nên $M=\lceil 6.6\pi / 0.1\pi \rceil = 66$.  
   **Vì sao:** Dải chuyển tiếp không quá rộng nên cần bậc tương đối lớn.  
   **Liên kết:** Là kết quả trực tiếp từ câu 47.

49. **Hỏi:** Vì sao code tăng bậc lên số chẵn nếu cần?  
   **Đáp:** Để được FIR Type-1 đối xứng.  
   **Vì sao:** Type-1 phù hợp cho low-pass và cho pha tuyến tính tốt.  
   **Liên kết:** Dựa trên câu 43 và 44.

50. **Hỏi:** Nhược điểm của FIR Hamming là gì?  
   **Đáp:** Cần nhiều hệ số hơn so với các phương pháp tối ưu.  
   **Vì sao:** Phương pháp cửa sổ không tối ưu trực tiếp ripple giữa các dải.  
   **Liên kết:** Dẫn sang Parks-McClellan.

---

## PHẦN F — PARKS-MCCLELLAN VÀ FIR TỐI ƯU

51. **Hỏi:** Parks-McClellan là gì?  
   **Đáp:** Là thuật toán thiết kế FIR equiripple tối ưu.  
   **Vì sao:** Nó giảm sai số cực đại theo chuẩn Chebyshev.  
   **Liên kết:** Là lời giải cho nhược điểm ở câu 50.

52. **Hỏi:** Trong Python dùng hàm nào cho Parks-McClellan?  
   **Đáp:** Dùng `remez()`.  
   **Vì sao:** `remez()` là hiện thực chuẩn của thuật toán này trong SciPy.  
   **Liên kết:** Bản cài đặt cụ thể của câu 51.

53. **Hỏi:** Vì sao vẫn chọn FIR Parks-McClellan thay vì bỏ hẳn FIR?  
   **Đáp:** Vì vẫn muốn giữ lợi thế pha tuyến tính của FIR.  
   **Vì sao:** Chỉ thay cách thiết kế để làm FIR gọn hơn.  
   **Liên kết:** Kết nối câu 43 với câu 51.

54. **Hỏi:** `delta1_db` và `delta2_db` là gì?  
   **Đáp:** Là ripple dải thông và suy giảm dải chắn ở đơn vị dB.  
   **Vì sao:** Đây là thông số đầu vào để ràng buộc chất lượng lọc.  
   **Liên kết:** Cần để hiểu câu 55 và 56.

55. **Hỏi:** Vì sao phải đổi dB sang biên độ tuyến tính?  
   **Đáp:** Vì thuật toán tối ưu làm việc với sai số biên độ thực.  
   **Vì sao:** dB chỉ là thang logarit để biểu diễn thuận tiện.  
   **Liên kết:** Dựa trên câu 54.

56. **Hỏi:** `weight` trong `remez()` có ý nghĩa gì?  
   **Đáp:** Nó quy định dải nào quan trọng hơn khi tối ưu sai số.  
   **Vì sao:** Có thể ưu tiên dải thông phẳng hơn hoặc dải chắn sâu hơn.  
   **Liên kết:** Mở rộng câu 54 và 55.

57. **Hỏi:** Vì sao Parks-McClellan cho bậc khoảng 20 trong code?  
   **Đáp:** Vì với bộ chỉ tiêu ripple hiện tại, thuật toán tối ưu đạt yêu cầu với ít hệ số hơn Hamming.  
   **Vì sao:** Đây là lợi thế tối ưu Chebyshev.  
   **Liên kết:** So sánh trực tiếp với câu 48.

58. **Hỏi:** Vậy FIR nào nên chọn nếu ưu tiên đơn giản?  
   **Đáp:** Chọn Hamming.  
   **Vì sao:** Dễ hiểu, dễ tính toán, sát giáo trình.  
   **Liên kết:** So với câu 57.

59. **Hỏi:** FIR nào nên chọn nếu ưu tiên ít hệ số hơn?  
   **Đáp:** Chọn Parks-McClellan.  
   **Vì sao:** Nó tối ưu hơn cùng mục tiêu low-pass.  
   **Liên kết:** Dựa trên câu 57.

60. **Hỏi:** Kết luận phần FIR là gì?  
   **Đáp:** FIR phù hợp khi cần pha tuyến tính; Hamming dễ triển khai còn Parks-McClellan tối ưu hơn về số hệ số.  
   **Vì sao:** Hai phương pháp cùng mục tiêu nhưng khác cách cân bằng giữa đơn giản và hiệu quả.  
   **Liên kết:** Tổng hợp phần E và F.

---

## PHẦN G — IIR VÀ LÝ DO CHỌN BẬC NHỎ

61. **Hỏi:** IIR là gì?  
   **Đáp:** Là bộ lọc có đáp ứng xung vô hạn.  
   **Vì sao:** Đầu ra có phụ thuộc vào đầu ra trước đó qua hồi tiếp.  
   **Liên kết:** Đối chiếu với FIR ở câu 41.

62. **Hỏi:** Vì sao IIR đạt đáp ứng dốc với bậc thấp?  
   **Đáp:** Vì hồi tiếp làm hệ tạo ra đặc tính phổ mạnh hơn với ít hệ số hơn.  
   **Vì sao:** Đây là bản chất của cấu trúc đệ quy.  
   **Liên kết:** Mở rộng từ câu 61.

63. **Hỏi:** Nhược điểm chính của IIR là gì?  
   **Đáp:** Pha phi tuyến và nguy cơ mất ổn định.  
   **Vì sao:** Pole có thể gây méo pha và nếu ra ngoài vòng tròn đơn vị thì hệ không ổn định.  
   **Liên kết:** Dựa trên phần C và câu 61.

64. **Hỏi:** Vì sao trong đề tài vẫn cần IIR?  
   **Đáp:** Vì báo cáo liên hệ đến DSP fixed-point cần tiết kiệm phép tính.  
   **Vì sao:** IIR bậc thấp phù hợp triển khai thời gian thực hơn.  
   **Liên kết:** Kết nối câu 62 và mục tiêu thực tế.

65. **Hỏi:** Vì sao chọn Chebyshev Type I?  
   **Đáp:** Vì nó đạt sườn lọc dốc hơn Butterworth với cùng bậc.  
   **Vì sao:** Chấp nhận ripple nhỏ trong dải thông để đổi lấy đáp ứng sắc hơn.  
   **Liên kết:** Trả lời bài toán tiết kiệm bậc ở câu 64.

66. **Hỏi:** `cheb1ord()` làm gì?  
   **Đáp:** Tính bậc nhỏ nhất thỏa ripple dải thông và suy giảm dải chắn.  
   **Vì sao:** Không cần đoán bậc thủ công.  
   **Liên kết:** Là công cụ chọn bậc cho câu 65.

67. **Hỏi:** Với `Rp=1 dB` và `Rs=15 dB`, vì sao bậc là 4?  
   **Đáp:** Vì `cheb1ord()` cho thấy chỉ cần bậc 4 là đủ thỏa yêu cầu.  
   **Vì sao:** Chebyshev Type I khá hiệu quả về độ dốc.  
   **Liên kết:** Kết quả trực tiếp từ câu 66.

68. **Hỏi:** Vì sao bậc IIR nhỏ hơn FIR rất nhiều?  
   **Đáp:** Vì IIR dùng hồi tiếp còn FIR thì không.  
   **Vì sao:** Hồi tiếp tăng hiệu quả phổ nhưng đánh đổi pha và ổn định.  
   **Liên kết:** So sánh câu 48, 57 và 67.

69. **Hỏi:** `cheby1()` làm gì trong code?  
   **Đáp:** Sinh hệ số số cho bộ lọc IIR Chebyshev Type I.  
   **Vì sao:** Sau khi đã biết bậc và tần số cắt, cần tạo hệ số thực thi.  
   **Liên kết:** Kế sau câu 66 và 67.

70. **Hỏi:** Kết luận phần IIR là gì?  
   **Đáp:** Nếu ưu tiên hiệu quả tính toán thì IIR Chebyshev Type I là lựa chọn mạnh, nhưng phải chấp nhận pha phi tuyến.  
   **Vì sao:** Đây là đánh đổi cốt lõi giữa FIR và IIR.  
   **Liên kết:** Tổng hợp phần G.

---

## PHẦN H — BILINEAR TRANSFORM VÀ TÍNH THAM SỐ

71. **Hỏi:** Vì sao báo cáo nhắc đến bilinear transform?  
   **Đáp:** Vì đó là phép đổi từ bộ lọc analog sang digital mà tránh aliasing.  
   **Vì sao:** Nó ánh xạ toàn bộ trục tần số analog vào miền số hữu hạn.  
   **Liên kết:** Gắn với IIR ở phần G.

72. **Hỏi:** Vì sao cần pre-warp?  
   **Đáp:** Vì bilinear transform làm méo trục tần số.  
   **Vì sao:** Nếu không pre-warp, điểm cắt sau biến đổi sẽ lệch khỏi yêu cầu.  
   **Liên kết:** Bước bắt buộc để hiểu câu 73 và 74.

73. **Hỏi:** Công thức pre-warp là gì?  
   **Đáp:** $\Omega = \frac{2}{T}\tan\left(\frac{\omega}{2}\right)$.  
   **Vì sao:** Đây là quan hệ chuẩn của bilinear transform.  
   **Liên kết:** Dựa trên câu 72.

74. **Hỏi:** Trong đề tài, $\Omega_p$ và $\Omega_s$ khoảng bao nhiêu?  
   **Đáp:** $\Omega_p \approx 28657.92$ rad/s và $\Omega_s \approx 44940.14$ rad/s.  
   **Vì sao:** Thay $F_s=44.1$ kHz, $\omega_p=0.2\pi$, $\omega_s=0.3\pi$ vào công thức.  
   **Liên kết:** Từ câu 73.

75. **Hỏi:** Vì sao vẫn in `OmegaP`, `OmegaS` trong code dù `SciPy` thiết kế digital trực tiếp được?  
   **Đáp:** Để bám sát giải thích lý thuyết trong báo cáo.  
   **Vì sao:** Đây là cách nối giữa MATLAB gốc và Python.  
   **Liên kết:** Liên quan trực tiếp câu 71 đến 74.

76. **Hỏi:** Vì sao phải đổi từ tần số chuẩn hóa sang Hz?  
   **Đáp:** Vì Hz giúp hiểu ý nghĩa vật lý của bài toán âm thanh.  
   **Vì sao:** Người làm audio quan tâm trực tiếp đến dải tần nghe được.  
   **Liên kết:** Quay lại phần D.

77. **Hỏi:** Vì sao phải đổi tiếp sang miền analog với $\Omega$?  
   **Đáp:** Vì bilinear transform xuất phát từ thiết kế analog.  
   **Vì sao:** Các họ IIR cổ điển thường được xây dựng trước ở miền analog.  
   **Liên kết:** Mở rộng câu 71 đến 75.

78. **Hỏi:** Tham số nào quyết định độ sắc của bộ lọc?  
   **Đáp:** Chủ yếu là dải chuyển tiếp và các ràng buộc ripple/suy giảm.  
   **Vì sao:** Chúng định nghĩa bộ lọc phải đổi từ cho qua sang chặn nhanh đến mức nào.  
   **Liên kết:** Liên hệ phần D, E, F, G.

79. **Hỏi:** Vì sao bộ lọc có dải chuyển tiếp hẹp thì cần bậc cao hơn?  
   **Đáp:** Vì đáp ứng cần đổi nhanh hơn trong miền tần số.  
   **Vì sao:** Đây là giới hạn bản chất của các thiết kế lọc thực tế.  
   **Liên kết:** Trả lời sâu thêm cho câu 36 và 78.

80. **Hỏi:** Kết luận phần tính tham số là gì?  
   **Đáp:** Mọi lựa chọn bộ lọc đều phải bắt đầu từ thông số phổ của input và đổi đúng giữa các miền biểu diễn.  
   **Vì sao:** Nếu tham số sai thì thiết kế sai dù thuật toán đúng.  
   **Liên kết:** Tổng kết phần H.

---

## PHẦN I — NOTCH, SNR VÀ ỨNG DỤNG THỰC TẾ

81. **Hỏi:** Vì sao không dùng low-pass để bỏ nhiễu 50 Hz?  
   **Đáp:** Vì low-pass có thể giữ lại 50 Hz nếu dải thông còn thấp, hoặc làm mất nhiều thành phần hữu ích nếu cắt quá gắt.  
   **Vì sao:** Nhiễu ở đây là hẹp băng, không phải toàn bộ tần cao.  
   **Liên kết:** Dựa trên phân tích input ở câu 37 đến 40.

82. **Hỏi:** Vì sao notch là lựa chọn chính xác cho nhiễu điện lưới?  
   **Đáp:** Vì nó chỉ chặn vùng rất hẹp quanh 50 Hz.  
   **Vì sao:** Điều này bảo toàn tốt hơn phần phổ còn lại.  
   **Liên kết:** Trả lời trực tiếp câu 81.

83. **Hỏi:** `Q` trong notch filter là gì?  
   **Đáp:** Là hệ số chất lượng, quyết định độ hẹp của dải chắn.  
   **Vì sao:** `Q` càng lớn thì notch càng hẹp.  
   **Liên kết:** Cần để hiểu cách tinh chỉnh notch.

84. **Hỏi:** Vì sao code chọn `Q = 30`?  
   **Đáp:** Vì cần chặn đủ rõ 50 Hz nhưng không ăn quá nhiều vùng lân cận.  
   **Vì sao:** Đây là giá trị cân bằng hợp lý cho demo.  
   **Liên kết:** Dựa trên câu 83.

85. **Hỏi:** SNR là gì?  
   **Đáp:** Là tỷ số năng lượng tín hiệu trên năng lượng nhiễu.  
   **Vì sao:** Đây là cách đo mức sạch của tín hiệu sau xử lý.  
   **Liên kết:** Gắn với hàm `energy()` ở phần A.

86. **Hỏi:** Vì sao SNR sau notch tăng?  
   **Đáp:** Vì thành phần 50 Hz bị giảm mạnh, nên phần nhiễu còn lại nhỏ hơn.  
   **Vì sao:** Bộ lọc tác động đúng vào nơi nhiễu tập trung.  
   **Liên kết:** Dựa trên câu 82 và 85.

87. **Hỏi:** Vì sao phổ FFT trước và sau lọc cần được vẽ?  
   **Đáp:** Vì phổ cho thấy trực quan đỉnh 50 Hz đã giảm chưa.  
   **Vì sao:** SNR chỉ là con số tổng hợp, còn FFT cho cái nhìn chi tiết.  
   **Liên kết:** Bổ sung cho câu 86.

88. **Hỏi:** Vì sao demo dùng cả waveform và FFT?  
   **Đáp:** Vì waveform cho thấy dạng sóng còn FFT cho thấy thành phần tần số.  
   **Vì sao:** Hai góc nhìn này bổ sung cho nhau.  
   **Liên kết:** Từ câu 87.

89. **Hỏi:** Nếu nhiễu không nằm đúng 50 Hz mà trôi nhẹ thì sao?  
   **Đáp:** Có thể phải giảm `Q` hoặc dùng adaptive notch.  
   **Vì sao:** Notch quá hẹp có thể bỏ sót nhiễu nếu tần số nhiễu thay đổi.  
   **Liên kết:** Dựa trên câu 83 và 84.

90. **Hỏi:** Kết luận của phần ứng dụng notch là gì?  
   **Đáp:** Khi biết rõ nhiễu đơn tần, notch filter thường là phương án tối ưu nhất.  
   **Vì sao:** Nó loại nhiễu chính xác mà ít làm tổn thương tín hiệu hữu ích.  
   **Liên kết:** Tổng kết phần I.

---

## PHẦN J — ECHO, DEBUG VÀ KIẾN TRÚC MODULE

91. **Hỏi:** `simulate_echo()` mô phỏng điều gì?  
   **Đáp:** Mô phỏng tiếng vọng trễ theo công thức $y(n)=x(n)+\alpha x(n-D)$.  
   **Vì sao:** Đây là mô hình đơn giản của âm phản xạ đến trễ hơn âm gốc.  
   **Liên kết:** Ứng dụng khác của DSP ngoài lọc phổ.

92. **Hỏi:** Vì sao tăng `delay_ms` làm tiếng vọng nghe xa hơn?  
   **Đáp:** Vì âm phản xạ xuất hiện muộn hơn.  
   **Vì sao:** Khoảng trễ lớn hơn tương ứng quãng đường phản xạ lớn hơn.  
   **Liên kết:** Dựa trên câu 91.

93. **Hỏi:** Vì sao tăng `decay` làm echo mạnh hơn?  
   **Đáp:** Vì hệ số nhân của nhánh trễ lớn hơn.  
   **Vì sao:** Năng lượng phần âm phản xạ được giữ lại nhiều hơn.  
   **Liên kết:** Mở rộng câu 91.

94. **Hỏi:** Vì sao code được tách thành module?  
   **Đáp:** Để từng phần có thể chạy độc lập và debug dễ hơn.  
   **Vì sao:** File quá dài sẽ khó theo dõi lỗi và khó tái sử dụng.  
   **Liên kết:** Liên hệ với yêu cầu thực tế của dự án.

95. **Hỏi:** Module nào quản lý style biểu đồ?  
   **Đáp:** [modules/plot_config.py](modules/plot_config.py).  
   **Vì sao:** Tách riêng giúp mọi biểu đồ nhất quán và dễ chỉnh.  
   **Liên kết:** Ví dụ của kiến trúc module ở câu 94.

96. **Hỏi:** Module nào điều phối toàn bộ demo?  
   **Đáp:** [modules/demo_runner.py](modules/demo_runner.py).  
   **Vì sao:** Nó gom luồng chạy và dữ liệu trả về từ mọi phần.  
   **Liên kết:** Tiếp nối câu 94.

97. **Hỏi:** Vì sao thêm tùy chọn `--no-plots`?  
   **Đáp:** Để chạy trên môi trường không có giao diện hoặc khi cần debug nhanh.  
   **Vì sao:** `matplotlib` có thể gây bất tiện khi chạy headless.  
   **Liên kết:** Gắn với file chính [dsp_audio_filter.py](dsp_audio_filter.py).

98. **Hỏi:** Khi debug bộ lọc, nên xem những gì trước?  
   **Đáp:** Xem input, thông số thiết kế, đáp ứng biên độ, pole/zero và kết quả đầu ra.  
   **Vì sao:** Đây là chuỗi logic từ nguyên nhân đến kết quả.  
   **Liên kết:** Tổng hợp gần như toàn bộ tài liệu.

99. **Hỏi:** Vì sao các câu hỏi trong tài liệu này phải có liên kết với nhau?  
   **Đáp:** Vì DSP là chuỗi suy luận, không thể trả lời đúng câu khó nếu thiếu nền tảng từ câu dễ.  
   **Vì sao:** Ví dụ muốn giải thích bậc IIR phải hiểu dải chuyển tiếp, ripple, pole và bilinear transform.  
   **Liên kết:** Đây chính là nguyên tắc tổ chức tài liệu.

100. **Hỏi:** Tóm tắt logic lớn nhất của toàn đề tài là gì?  
   **Đáp:** Phải phân tích đúng input trước, sau đó chọn đúng loại lọc, rồi mới tính đúng tham số và kiểm chứng bằng đồ thị cùng kết quả đầu ra.  
   **Vì sao:** Đây là quy trình chuẩn để tránh chọn đúng thuật toán nhưng sai bài toán.  
   **Liên kết:** Tổng kết toàn bộ 100 câu.
