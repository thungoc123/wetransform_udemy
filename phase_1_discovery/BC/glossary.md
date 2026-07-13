# Thuật ngữ dự án (Project Glossary) - Nền tảng AI Learning Analytics

Tài liệu này định nghĩa các thuật ngữ nghiệp vụ, kỹ thuật và các từ viết tắt quan trọng được sử dụng xuyên suốt trong hệ thống AI Learning Analytics cho giáo viên Udemy.

---

## 1. Thuật ngữ nghiệp vụ (Business Terms)

### Learning Analytics (Phân tích học tập)
* **Ý nghĩa:** Việc đo lường, thu thập, phân tích và báo cáo dữ liệu về người học và bối cảnh học tập nhằm mục đích thấu hiểu và tối ưu hóa việc học tập cũng như môi trường diễn ra hoạt động đó.

### Course Creator / Teacher (Nhà sáng tạo khóa học / Giáo viên)
* **Ý nghĩa:** Người dùng chính của hệ thống, người trực tiếp biên soạn, xuất bản khóa học lên Udemy và theo dõi các báo cáo phân tích để tối ưu hóa nội dung khóa học.

### Completion Rate (Tỷ lệ hoàn thành)
* **Ý nghĩa:** Phần trăm số lượng học viên hoàn thành toàn bộ khóa học hoặc một phần học cụ thể (lesson/module) trên tổng số học viên đăng ký.

### Drop-off Rate (Tỷ lệ dừng học / bỏ cuộc)
* **Ý nghĩa:** Tỷ lệ học viên dừng việc học tại một bài học hoặc thời điểm cụ thể trong khóa học. Chỉ số này giúp khoanh vùng các bài học có nội dung chưa hấp dẫn hoặc quá khó.

### Drop-off Point (Điểm dừng học)
* **Ý nghĩa:** Vị trí chính xác (bài học cụ thể hoặc mốc thời gian cụ thể trong video bài giảng) nơi ghi nhận lượng lớn học viên dừng học và không tiếp tục nữa.

### Active Student (Học viên đang hoạt động)
* **Ý nghĩa:** Học viên có hoạt động học tập, tương tác với khóa học trong một khoảng thời gian xác định gần đây (ví dụ: trong vòng 7 ngày qua).

### Inactive Student (Học viên không hoạt động)
* **Ý nghĩa:** Học viên đã lâu không truy cập hoặc có hoạt động học tập trong khóa học.

### At-risk Student (Học viên có nguy cơ bỏ cuộc)
* **Ý nghĩa:** Học viên có dấu hiệu giảm sút rõ rệt về tần suất học tập hoặc dừng lại lâu hơn bình thường tại một bài học, có nguy cơ cao chuyển sang trạng thái *Inactive*.

### Re-engaged Student (Học viên quay lại học)
* **Ý nghĩa:** Học viên từng ở trạng thái *Inactive* hoặc *At-risk* nhưng đã tiếp tục học trở lại sau khi nhận được sự can thiệp (intervention/reminder) từ giáo viên.

### Actionable Insight (Thông tin chi tiết có thể hành động)
* **Ý nghĩa:** Những thông tin phân tích hoặc gợi ý rõ ràng, thực tế từ dữ liệu, giúp giáo viên có thể thực hiện ngay một hành động sửa đổi cụ thể để cải thiện chất lượng (ví dụ: *"Học viên thường bỏ cuộc ở phút thứ 5 của video X, đề xuất chia nhỏ video này thành 2 phần"*).

### Intervention (Sự can thiệp)
* **Ý nghĩa:** Các hành động chủ động từ phía giáo viên nhằm tác động vào hành vi học tập của học viên, chẳng hạn như gửi nhắc nhở, cung cấp thêm tài liệu bổ trợ hoặc thay đổi cấu trúc bài học.

### Best Practice (Thực hành tốt nhất / Phương pháp tối ưu)
* **Ý nghĩa:** Những hành vi, thói quen hoặc phương pháp học tập của những học viên hoàn thành khóa học xuất sắc/nhanh nhất. Hệ thống phân tích để lấy làm mẫu biên soạn các thông điệp nhắc nhở và lan tỏa đến nhóm học viên khác.

---

## 2. Thuật ngữ kỹ thuật & Hệ thống (Technical & System Terms)

### Udemy Connection / Data Import (Đồng bộ dữ liệu Udemy)
* **Ý nghĩa:** Quá trình thu thập dữ liệu học tập thông qua kết nối API trực tiếp từ Udemy hoặc thông qua việc giáo viên tải lên (upload) các file dữ liệu được xuất (export) từ dashboard của Udemy.

### Student Trigger (Bộ kích hoạt tương tác)
* **Ý nghĩa:** Cơ chế tự động phát hiện khi một học viên rơi vào trạng thái nguy cơ (at-risk) và tự động kích hoạt luồng gửi nhắc nhở (Reminder).

---

## 3. Từ viết tắt (Acronyms & Abbreviations)

### API (Application Programming Interface)
* **Ý nghĩa:** Giao diện lập trình ứng dụng. Trong dự án này, API đại diện cho cổng kết nối kỹ thuật giúp hệ thống tự động đồng bộ dữ liệu học viên, tiến độ từ Udemy.

### MVP (Minimum Viable Product)
* **Ý nghĩa:** Sản phẩm khả dụng tối thiểu. Phiên bản đầu tiên của hệ thống chỉ tập trung vào các tính năng cốt lõi nhất (như phân tích điểm dừng học và gửi nhắc nhở cơ bản) để kiểm thử thực tế nhanh nhất.

### DoD (Definition of Done)
* **Ý nghĩa:** Định nghĩa hoàn thành. Tập hợp các tiêu chí kỹ thuật và nghiệp vụ mà một tính năng hoặc phiên bản phải vượt qua trước khi được bàn giao chính thức.

### LMS (Learning Management System)
* **Ý nghĩa:** Hệ thống quản lý học tập. Nền tảng quản lý và phân phối các khóa học trực tuyến (Udemy là một nền tảng LMS bên thứ ba mà hệ thống này tích hợp).
