# 100 CÂU HỎI VÀ TRẢ LỜI GHI NHỚ CHO ĐỀ TÀI DSP ÂM THANH

## Mức 1: Rất cơ bản

1. **Hỏi:** DSP là gì?  
   **Đáp:** DSP là xử lý số tín hiệu, tức là dùng thuật toán số để phân tích, biến đổi hoặc cải thiện tín hiệu.

2. **Hỏi:** Tín hiệu âm thanh số là gì?  
   **Đáp:** Là tín hiệu âm thanh sau khi được lấy mẫu và lượng tử hóa thành dãy số.

3. **Hỏi:** `Fs` là gì?  
   **Đáp:** `Fs` là tần số lấy mẫu, đơn vị Hz.

4. **Hỏi:** Vì sao chọn `Fs = 44.1 kHz`?  
   **Đáp:** Đây là chuẩn phổ biến của audio và đủ để biểu diễn tần số đến 22.05 kHz.

5. **Hỏi:** Định lý Nyquist nói gì?  
   **Đáp:** Tần số lấy mẫu phải ít nhất gấp đôi tần số lớn nhất của tín hiệu.

6. **Hỏi:** Bộ lọc số là gì?  
   **Đáp:** Là hệ thống xử lý tín hiệu rời rạc nhằm giữ lại hoặc loại bỏ một dải tần số.

7. **Hỏi:** Bộ lọc thông thấp là gì?  
   **Đáp:** Là bộ lọc cho qua tần số thấp và chặn tần số cao.

8. **Hỏi:** Bộ lọc thông cao là gì?  
   **Đáp:** Là bộ lọc cho qua tần số cao và chặn tần số thấp.

9. **Hỏi:** Bộ lọc thông dải là gì?  
   **Đáp:** Là bộ lọc chỉ cho qua một dải tần xác định.

10. **Hỏi:** Bộ lọc chắn dải là gì?  
   **Đáp:** Là bộ lọc loại bỏ một dải tần xác định.

11. **Hỏi:** FIR là gì?  
   **Đáp:** FIR là bộ lọc có đáp ứng xung hữu hạn.

12. **Hỏi:** IIR là gì?  
   **Đáp:** IIR là bộ lọc có đáp ứng xung vô hạn do có phần hồi tiếp.

13. **Hỏi:** FIR có ưu điểm gì?  
   **Đáp:** Luôn ổn định và dễ đạt pha tuyến tính.

14. **Hỏi:** IIR có ưu điểm gì?  
   **Đáp:** Đạt đáp ứng dốc với bậc thấp hơn FIR.

15. **Hỏi:** `matplotlib` dùng để làm gì trong đề tài này?  
   **Đáp:** Dùng để hiển thị waveform, phổ FFT, đáp ứng biên độ, pha, group delay và Z-plane.

16. **Hỏi:** `numpy` dùng để làm gì?  
   **Đáp:** Dùng cho tính toán vector, ma trận và thao tác mảng số.

17. **Hỏi:** `scipy.signal` dùng để làm gì?  
   **Đáp:** Dùng để thiết kế bộ lọc, phân tích hệ thống và xử lý tín hiệu.

18. **Hỏi:** Tín hiệu rời rạc được biểu diễn như thế nào?  
   **Đáp:** Bằng dãy mẫu $x(n)$ theo chỉ số nguyên $n$.

19. **Hỏi:** Năng lượng tín hiệu được tính thế nào?  
   **Đáp:** Bằng công thức $E = \sum |x(n)|^2$.

20. **Hỏi:** Hàm `energy()` trong code làm gì?  
   **Đáp:** Tính năng lượng của tín hiệu đầu vào.

## Mức 2: Thao tác tín hiệu cơ bản

21. **Hỏi:** `sigshift()` làm gì?  
   **Đáp:** Dịch trục chỉ số của tín hiệu sang trái hoặc phải.

22. **Hỏi:** `sigfold()` làm gì?  
   **Đáp:** Gấp tín hiệu theo trục thời gian, tức biến $x(n)$ thành $x(-n)$.

23. **Hỏi:** `sigadd()` làm gì?  
   **Đáp:** Cộng hai tín hiệu có thể khác miền chỉ số bằng cách căn chỉnh lại trục.

24. **Hỏi:** Vì sao phải căn chỉnh chỉ số trước khi cộng tín hiệu?  
   **Đáp:** Vì nếu index không khớp thì các mẫu tương ứng sẽ bị cộng sai vị trí.

25. **Hỏi:** Khi debug `sigadd()` cần chú ý gì?  
   **Đáp:** Cần kiểm tra `n_start`, `n_stop` và vùng gán mảng con.

26. **Hỏi:** Dịch tín hiệu có làm đổi biên độ không?  
   **Đáp:** Không, chỉ đổi vị trí thời gian.

27. **Hỏi:** Gấp tín hiệu có làm đổi năng lượng không?  
   **Đáp:** Không, chỉ đảo trục thời gian.

28. **Hỏi:** Vì sao chương trình demo dùng `stem()`?  
   **Đáp:** Vì tín hiệu rời rạc nên hiển thị theo cọc mẫu là phù hợp.

29. **Hỏi:** Chương 1 trong code dùng để làm gì?  
   **Đáp:** Dùng để minh họa các phép toán cơ bản trên dãy rời rạc.

30. **Hỏi:** `demo_signal_ops()` trả về gì?  
   **Đáp:** Trả về dữ liệu tín hiệu để có thể quan sát hoặc debug tiếp.

## Mức 3: Biến đổi Z và ổn định

31. **Hỏi:** Biến đổi Z dùng để làm gì?  
   **Đáp:** Dùng để phân tích hệ rời rạc trong miền phức.

32. **Hỏi:** Hàm truyền đạt rời rạc có dạng gì?  
   **Đáp:** $H(z)=\frac{B(z)}{A(z)}$.

33. **Hỏi:** `residuez()` dùng để làm gì?  
   **Đáp:** Phân tích hàm truyền thành tổng các phân thức đơn giản.

34. **Hỏi:** Pole là gì?  
   **Đáp:** Là nghiệm của mẫu số $A(z)$.

35. **Hỏi:** Zero là gì?  
   **Đáp:** Là nghiệm của tử số $B(z)$.

36. **Hỏi:** Điều kiện ổn định của hệ IIR rời rạc là gì?  
   **Đáp:** Tất cả cực phải nằm trong vòng tròn đơn vị.

37. **Hỏi:** `zplane()` trong code làm gì?  
   **Đáp:** Vẽ zero, pole và vòng tròn đơn vị trên mặt phẳng phức.

38. **Hỏi:** Nếu một pole nằm ngoài vòng tròn đơn vị thì sao?  
   **Đáp:** Hệ sẽ không ổn định.

39. **Hỏi:** Vì sao Z-plane quan trọng?  
   **Đáp:** Vì nó cho thấy trực quan tính ổn định và đặc tính phổ của hệ.

40. **Hỏi:** `demo_z_transform()` minh họa nội dung gì?  
   **Đáp:** Minh họa khai triển phân thức đơn giản và phân tích cực-không.

## Mức 4: FIR cơ bản

41. **Hỏi:** Vì sao FIR thích hợp cho âm thanh Hi-Fi?  
   **Đáp:** Vì FIR có thể đạt pha tuyến tính, giảm méo pha.

42. **Hỏi:** Pha tuyến tính nghĩa là gì?  
   **Đáp:** Các thành phần tần số bị trễ gần như như nhau theo thời gian.

43. **Hỏi:** Hàm `design_fir_hamming()` dùng gì?  
   **Đáp:** Dùng phương pháp cửa sổ Hamming để thiết kế FIR thông thấp.

44. **Hỏi:** Tại sao dùng cửa sổ Hamming?  
   **Đáp:** Vì nó giảm ripple do hiện tượng Gibbs tốt hơn cửa sổ chữ nhật.

45. **Hỏi:** `firwin()` làm gì?  
   **Đáp:** Tạo hệ số FIR theo tần số cắt và loại cửa sổ.

46. **Hỏi:** Vì sao code làm tròn bậc FIR lên số chẵn?  
   **Đáp:** Để nhận được bộ lọc Type-1 có đối xứng, hỗ trợ pha tuyến tính.

47. **Hỏi:** Tần số cắt trong code Hamming được chọn thế nào?  
   **Đáp:** Chọn tại trung điểm giữa $\omega_p$ và $\omega_s$.

48. **Hỏi:** `plot_fir_response()` vẽ gì?  
   **Đáp:** Vẽ đáp ứng biên độ và pha của các bộ lọc FIR.

49. **Hỏi:** FIR Hamming có nhược điểm gì?  
   **Đáp:** Thường cần nhiều hệ số hơn để đạt cùng mức sắc cạnh.

50. **Hỏi:** Vì sao FIR luôn ổn định?  
   **Đáp:** Vì không có phần hồi tiếp như IIR.

## Mức 5: FIR nâng cao

51. **Hỏi:** Parks-McClellan là gì?  
   **Đáp:** Là thuật toán thiết kế FIR equiripple tối ưu theo chuẩn Chebyshev.

52. **Hỏi:** Trong Python dùng hàm nào cho Parks-McClellan?  
   **Đáp:** Dùng `remez()`.

53. **Hỏi:** `design_fir_pm()` khác `design_fir_hamming()` ở đâu?  
   **Đáp:** `design_fir_pm()` tối ưu ripple theo trọng số còn Hamming dùng cửa sổ cố định.

54. **Hỏi:** Vì sao cần đổi ripple dB sang biên độ tuyến tính?  
   **Đáp:** Vì thuật toán thiết kế dùng giá trị biên độ thật để tối ưu.

55. **Hỏi:** `weight` trong `remez()` có ý nghĩa gì?  
   **Đáp:** Quy định mức ưu tiên sai số giữa dải thông và dải chắn.

56. **Hỏi:** Vì sao FIR Parks-McClellan thường ngắn hơn?  
   **Đáp:** Vì nó tối ưu hóa tốt hơn nên đạt yêu cầu với bậc nhỏ hơn.

57. **Hỏi:** FIR equiripple nghĩa là gì?  
   **Đáp:** Ripple trong mỗi dải gần như phân bố đều theo chuẩn tối ưu cực đại.

58. **Hỏi:** Khi nào nên ưu tiên Parks-McClellan?  
   **Đáp:** Khi cần bộ lọc ngắn hơn nhưng vẫn đúng chỉ tiêu.

59. **Hỏi:** Khi nào Hamming vẫn hữu ích?  
   **Đáp:** Khi muốn thiết kế nhanh, ổn định và dễ hiểu.

60. **Hỏi:** Trong đồ án, FIR nào tối ưu hơn về số hệ số?  
   **Đáp:** FIR Parks-McClellan.

## Mức 6: IIR cơ bản

61. **Hỏi:** Vì sao IIR tiết kiệm tài nguyên hơn FIR?  
   **Đáp:** Vì IIR đạt đáp ứng dốc với bậc thấp hơn nhiều.

62. **Hỏi:** IIR có nhược điểm gì?  
   **Đáp:** Pha phi tuyến và phải kiểm soát ổn định.

63. **Hỏi:** Trong đề tài dùng họ IIR nào?  
   **Đáp:** Chebyshev Type I.

64. **Hỏi:** `cheb1ord()` dùng để làm gì?  
   **Đáp:** Tính bậc tối thiểu của bộ lọc thỏa yêu cầu gợn sóng và suy giảm.

65. **Hỏi:** `cheby1()` dùng để làm gì?  
   **Đáp:** Sinh hệ số bộ lọc Chebyshev Type I.

66. **Hỏi:** Vì sao báo cáo nói đến bilinear transformation?  
   **Đáp:** Vì đây là cách ánh xạ bộ lọc analog sang digital mà tránh aliasing.

67. **Hỏi:** Công thức pre-warp là gì?  
   **Đáp:** $\Omega = \frac{2}{T}\tan\left(\frac{\omega}{2}\right)$.

68. **Hỏi:** Mục đích của pre-warp là gì?  
   **Đáp:** Bù méo tần số do phép biến đổi song tuyến gây ra.

69. **Hỏi:** `afd_chb1_bilinear()` trong code làm gì?  
   **Đáp:** Tính pre-warp, tìm bậc Chebyshev và thiết kế bộ lọc IIR thông thấp.

70. **Hỏi:** Vì sao code vẫn in ra `OmegaP`, `OmegaS`?  
   **Đáp:** Để giải thích đúng phần lý thuyết analog-to-digital trong báo cáo.

## Mức 7: IIR nâng cao

71. **Hỏi:** Group delay là gì?  
   **Đáp:** Là độ trễ theo tần số của tín hiệu qua bộ lọc.

72. **Hỏi:** Vì sao IIR thường có group delay không hằng?  
   **Đáp:** Vì pha của IIR phi tuyến.

73. **Hỏi:** `group_delay()` trong code dùng để làm gì?  
   **Đáp:** Tính và vẽ trễ nhóm của bộ lọc.

74. **Hỏi:** Tại sao phải xem cả magnitude lẫn phase?  
   **Đáp:** Vì biên độ tốt chưa đủ, pha có thể làm méo dạng sóng.

75. **Hỏi:** Nếu IIR có cực sát vòng tròn đơn vị thì sao?  
   **Đáp:** Hệ vẫn có thể ổn định nhưng nhạy hơn với sai số số học.

76. **Hỏi:** Tại sao IIR hợp với DSP fixed-point?  
   **Đáp:** Vì bậc thấp hơn nên cần ít phép MAC hơn.

77. **Hỏi:** Tại sao audio chất lượng cao vẫn hay dùng FIR?  
   **Đáp:** Vì ưu tiên bảo toàn pha tuyến tính hơn là tiết kiệm hệ số.

78. **Hỏi:** `plot_iir_response()` vẽ mấy đồ thị?  
   **Đáp:** Vẽ 4 đồ thị: magnitude, phase, group delay và Z-plane.

79. **Hỏi:** Kết luận ổn định trong code lấy từ đâu?  
   **Đáp:** Từ điều kiện mọi cực có mô-đun nhỏ hơn 1.

80. **Hỏi:** Bậc IIR trong ví dụ nhỏ hơn FIR hay không?  
   **Đáp:** Có, nhỏ hơn đáng kể.

## Mức 8: Ứng dụng thực tế và debug

81. **Hỏi:** Mục tiêu của notch 50Hz là gì?  
   **Đáp:** Loại bỏ nhiễu điện lưới chồng lên tín hiệu âm thanh.

82. **Hỏi:** Hàm nào thiết kế notch filter?  
   **Đáp:** `design_notch_50hz()`.

83. **Hỏi:** Trong Python dùng hàm nào tạo notch?  
   **Đáp:** Dùng `signal.iirnotch()`.

84. **Hỏi:** Tham số `Q` trong notch filter nghĩa là gì?  
   **Đáp:** Là hệ số chất lượng, quyết định độ hẹp của dải chắn.

85. **Hỏi:** `demo_notch()` đánh giá hiệu quả bằng gì?  
   **Đáp:** Bằng SNR trước và sau lọc, waveform và phổ FFT.

86. **Hỏi:** Vì sao sau lọc SNR tăng?  
   **Đáp:** Vì thành phần nhiễu 50Hz bị suy giảm mạnh.

87. **Hỏi:** Hàm `simulate_echo()` mô phỏng gì?  
   **Đáp:** Mô phỏng tiếng vọng trễ trong hệ âm thanh.

88. **Hỏi:** Công thức echo trong code là gì?  
   **Đáp:** $y(n)=x(n)+\alpha x(n-D)$.

89. **Hỏi:** Tăng `delay_ms` sẽ làm gì?  
   **Đáp:** Làm tiếng vọng xuất hiện muộn hơn.

90. **Hỏi:** Tăng `decay` sẽ làm gì?  
   **Đáp:** Làm tiếng vọng mạnh hơn.

91. **Hỏi:** Vì sao tách code thành module giúp debug?  
   **Đáp:** Vì có thể chạy và kiểm tra từng phần độc lập.

92. **Hỏi:** File chạy chính hiện làm gì?  
   **Đáp:** Chỉ nhận tham số và gọi `run_all()`.

93. **Hỏi:** Tại sao có `--no-plots`?  
   **Đáp:** Để chạy không cần giao diện đồ họa, thuận tiện kiểm thử.

94. **Hỏi:** Module nào điều phối toàn bộ chương trình?  
   **Đáp:** [modules/demo_runner.py](modules/demo_runner.py).

95. **Hỏi:** Muốn debug riêng FIR thì import module nào?  
   **Đáp:** Import từ [modules/fir_filters.py](modules/fir_filters.py).

96. **Hỏi:** Muốn debug riêng IIR thì import module nào?  
   **Đáp:** Import từ [modules/iir_filters.py](modules/iir_filters.py).

97. **Hỏi:** Muốn debug phần ứng dụng âm thanh thì import module nào?  
   **Đáp:** Import từ [modules/applications.py](modules/applications.py).

98. **Hỏi:** Hướng mở rộng tốt nhất tiếp theo là gì?  
   **Đáp:** Đọc file `.wav` thật để lọc âm thanh thực tế.

99. **Hỏi:** Có thể thêm adaptive filter không?  
   **Đáp:** Có, có thể thêm LMS để khử vọng hoặc khử nhiễu thích nghi.

100. **Hỏi:** Ý nghĩa lớn nhất của code này là gì?  
   **Đáp:** Biến lý thuyết DSP trong báo cáo thành mô phỏng Python trực quan, dễ debug và dễ mở rộng.
