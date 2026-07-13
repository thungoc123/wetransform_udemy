# Phạm vi sản phẩm (Product Scope) - Nền tảng AI Learning Analytics

Tài liệu này xác định ranh giới phát triển, các tính năng trong và ngoài phạm vi, cùng các ràng buộc ảnh hưởng đến phiên bản hiện tại (MVP) của sản phẩm.

## 1. Mục tiêu của phiên bản hiện tại (MVP) là gì?
* **Mục tiêu chính:** Cung cấp cho giáo viên bán khóa học trên Udemy các insight có thể hành động (actionable insights) để cải thiện tỷ lệ hoàn thành khóa học của học viên, đặc biệt trong bối cảnh học online sang lớp học offline theo mô hình Online-to-Offline (O2O).
* **Mục tiêu cụ thể:**
  * Phát hiện điểm học viên thường bỏ cuộc (drop-off points).
  * Gợi ý nguyên nhân bằng AI.
  * Hỗ trợ giáo viên can thiệp (gửi nhắc nhở, gợi ý học tập) để kéo học viên quay lại.
  * Chuyển insight từ học online thành đề xuất thực hiện cho buổi học offline, ví dụ phân bổ lý thuyết và thực hành phù hợp.

## 2. Những tính năng nào sẽ được phát triển trong MVP?
Hệ thống gồm các tính năng chính sau:
* **Kết nối dữ liệu:** Hỗ trợ kết nối API Udemy hoặc nhập (import) dữ liệu thủ công từ file xuất bản của Udemy.
* **Dashboard tổng quan:** Trực quan hóa các chỉ số quan trọng như tỷ lệ hoàn thành (completion rate), tỷ lệ bỏ cuộc (drop-off rate), số lượng học viên đang hoạt động (active/inactive).
* **Phân tích điểm dừng:** Xác định cụ thể bài học (lesson/module) nào học viên có xu hướng dừng học cao nhất.
* **Gợi ý AI (AI Insight):** Tự động phân tích hành vi và đưa ra các giả thuyết/nguyên nhân tiềm ẩn (bài quá dài, bài tập khó, kiến thức cũ...).
* **Đề xuất hành động:** Đưa ra giải pháp cụ thể cho giáo viên (ví dụ: chia nhỏ video, thêm câu hỏi trắc nghiệm, cập nhật tài liệu).
* **Trigger tương tác học viên:** Hỗ trợ gửi tin nhắn/email nhắc nhở quay lại học cho những học viên có dấu hiệu bỏ dở và soạn tin nhắn cũng dựa vào insight từ những học viên hoàn thành nhanh, để nhân rộng best practice.

## 3. Những tính năng nào KHÔNG thuộc phạm vi phát triển?
Để đảm bảo tiến độ và tính tập trung của MVP, các tính năng sau sẽ không được thực hiện:
* Tạo mới hoặc tái cấu trúc tự động toàn bộ nội dung khóa học bằng AI.
* Tự động chỉnh sửa/cắt ghép video bài giảng.
* Xây dựng Marketplace riêng để bán khóa học thay thế Udemy.
* Xây dựng ứng dụng di động (Mobile App) riêng cho học viên.
* Hệ thống chấm điểm năng lực học tập nâng cao hoặc Engine gợi ý khóa học (Recommendation Engine) phức tạp cho học viên.
* Tính năng A/B testing nội dung khóa học toàn diện.
* Tích hợp các nền tảng dạy học trực tuyến khác ngoài Udemy.

## 4. Những nhóm người dùng nào được hỗ trợ?
* **Nhóm người dùng chính (Direct User):** Giáo viên, nhà sáng tạo nội dung khóa học (Course Creator) trên nền tảng Udemy và giảng viên vận hành lớp học offline.
* **Nhóm người hưởng lợi gián tiếp (Indirect User):** Học viên đăng ký học các khóa học của giáo viên trên Udemy và tham gia các buổi học offline sau đó (được nhắc nhở học tập và trải nghiệm nội dung tốt hơn).

## 5. Những quy trình nghiệp vụ nào được hỗ trợ?
Hệ thống hỗ trợ luồng nghiệp vụ khép kín sau:
1. **Đăng nhập & Xác thực:** Giáo viên đăng nhập vào hệ thống AI Learning Analytics.
2. **Thu thập dữ liệu:** Giáo viên kết nối tài khoản API Udemy hoặc tải lên tệp dữ liệu đã xuất.
3. **Phân tích dữ liệu hành vi:** Hệ thống xử lý dữ liệu học tập của học viên để tìm ra các điểm bất thường hoặc điểm drop-off cao.
4. **Phát hiện & Đề xuất:** Hệ thống hiển thị dashboard, AI suy luận nguyên nhân và gợi ý giải pháp cải thiện nội dung.
5. **Can thiệp chủ động:** Giáo viên thiết lập và gửi các thông báo nhắc nhở tự động cho nhóm học viên phù hợp.
6. **Đánh giá hiệu quả:** Hệ thống theo dõi phản hồi/tiến độ của học viên sau khi can thiệp để đo lường hiệu quả.

## 6. Có những giới hạn nào về nền tảng, thị trường hoặc quy mô?
* **Nền tảng:** Chỉ tập trung hỗ trợ nền tảng Udemy ở giai đoạn hiện tại.
* **Quy mô dữ liệu kiểm thử ban đầu:** Hệ thống được thiết kế để xử lý dữ liệu từ 3 khóa học mẫu và khoảng 2.600 học viên hoạt động.
* **Quy mô tương lai:** Hệ thống cần có khả năng mở rộng kiến trúc để xử lý lượng dữ liệu lớn hơn nhiều lần mà không làm giảm hiệu suất dashboard.

## 7. Điều kiện để phiên bản được xem là hoàn thành (Definition of Done)?
MVP được coi là hoàn thành khi đáp ứng các tiêu chuẩn sau:
* **Tính năng:** Toàn bộ 6 tính năng cốt lõi trong phần 2 được phát triển và kiểm thử thành công.
* **Tích hợp:** Dữ liệu mẫu từ Udemy (3 khóa học, 2.600 học viên) được import và phân tích chính xác, không bị lỗi cấu trúc dữ liệu.
* **Độ chính xác AI:** Các gợi ý nguyên nhân của AI phải logic, có căn cứ dựa trên dữ liệu hành vi thực tế và được giáo viên kiểm định đạt yêu cầu.
* **Vận hành:** Hệ thống trigger gửi reminder chạy ổn định, không bị trùng lặp hoặc gây spam học viên.
* **Bảo mật:** Dữ liệu học viên được mã hóa hoặc ẩn danh hóa trước khi xử lý, đảm bảo an toàn thông tin.

## 8. Có giả định hoặc ràng buộc nào ảnh hưởng đến phạm vi không?
* **Ràng buộc dữ liệu:** Chất lượng phân tích phụ thuộc hoàn toàn vào cấu trúc dữ liệu xuất ra hoặc API được Udemy hỗ trợ. Nếu dữ liệu bị thiếu hoặc không đồng nhất, kết quả phân tích có thể bị hạn chế.
* **Giới hạn của AI:** AI chỉ đưa ra giả thuyết và gợi ý mang tính chất tham khảo cho giáo viên, không thay thế hoàn toàn quyết định chuyên môn sư phạm của giáo viên.
* **Quyền riêng tư:** Việc gửi nhắc nhở và thu thập dữ liệu học viên phải tuân thủ nghiêm ngặt chính sách bảo mật của Udemy và quy định bảo vệ dữ liệu cá nhân.
