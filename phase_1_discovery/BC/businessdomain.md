
## 1. Domain của hệ thống

**Learning Analytics / EdTech / Course Performance Optimization**
Cụ thể: phân tích hành vi học viên Udemy để giúp giáo viên biết **học viên dừng ở đâu, vì sao dừng, và nên cải thiện gì**, đồng thời chuyển insight này thành kế hoạch phù hợp cho lớp học offline theo mô hình Online-to-Offline (O2O).

## 2. Business Entity chính

| Entity                         | Ý nghĩa                                          |
| ------------------------------ | ------------------------------------------------ |
| Teacher / Course Creator       | Người dùng chính của hệ thống                    |
| Offline Instructor             | Giảng viên vận hành buổi học offline             |
| Student                        | Học viên Udemy, người hưởng lợi gián tiếp        |
| Course                         | Khóa học được phân tích                          |
| Lesson / Module                | Bài học hoặc học phần nơi có thể xảy ra drop-off |
| Learning Activity              | Dữ liệu hành vi học tập                          |
| Drop-off Point                 | Điểm học viên thường dừng học                    |
| AI Insight                     | Giả thuyết AI về nguyên nhân vấn đề              |
| Recommendation                 | Đề xuất hành động cải thiện khóa học             |
| Reminder / Message             | Tin nhắn/email nhắc học viên quay lại            |
| Data Import / Udemy Connection | Nguồn dữ liệu từ API hoặc file Udemy             |

## 3. Thuật ngữ nghiệp vụ quan trọng

Completion rate, drop-off rate, active student, inactive student, drop-off point, AI insight, actionable insight, intervention, reminder, best practice, Udemy data import, course performance.

## 4. Quy trình nghiệp vụ chính

1. Giáo viên đăng nhập.
2. Kết nối API Udemy hoặc import file dữ liệu.
3. Hệ thống phân tích hành vi học viên.
4. Phát hiện điểm drop-off cao.
5. AI gợi ý nguyên nhân.
6. Hệ thống đề xuất hành động cải thiện, bao gồm cách áp dụng cho lớp học offline.
7. Giáo viên/giảng viên offline gửi reminder hoặc điều chỉnh kế hoạch buổi học cho nhóm học viên phù hợp.
8. Hệ thống theo dõi hiệu quả sau can thiệp. 

## 5. Business Rules luôn phải tuân thủ

| Rule                                      | Mô tả                                                  |   |
| ----------------------------------------- | ------------------------------------------------------ | - |
| Chỉ hỗ trợ Udemy trong MVP                | Không tích hợp nền tảng khác                           |   |
| AI chỉ đưa ra giả thuyết                  | Không thay thế quyết định chuyên môn của giáo viên     |   |
| Không spam học viên                       | Reminder không được gửi trùng lặp hoặc quá mức         |   |
| Bảo mật dữ liệu học viên                  | Dữ liệu cần được mã hóa hoặc ẩn danh hóa               |   |
| Phân tích dựa trên dữ liệu thực tế        | Insight phải có căn cứ từ hành vi học tập              |   |
| Không tự động chỉnh sửa nội dung khóa học | Hệ thống chỉ đề xuất, không sửa video/nội dung tự động |   |

## 6. Trạng thái của Business Entity

| Entity          | Trạng thái chính                                                    |
| --------------- | ------------------------------------------------------------------- |
| Teacher         | Chưa đăng nhập → Đã đăng nhập → Đã kết nối dữ liệu → Đang can thiệp |
| Course          | Chưa import → Đã import → Đã phân tích → Đang cải thiện             |
| Student         | Active → At-risk → Inactive → Re-engaged                            |
| Lesson / Module | Bình thường → Có drop-off cao → Được đề xuất cải thiện              |
| AI Insight      | Chưa tạo → Đã tạo → Được giáo viên xem xét → Được áp dụng / bỏ qua  |
| Recommendation  | Được đề xuất → Được chọn → Đã thực hiện → Được đánh giá             |
| Reminder        | Draft → Scheduled/Sent → Delivered → Responded / Ignored            |
| Data Import     | Pending → Processing → Success / Failed                             |

## 7. Actors tham gia

| Actor                         | Vai trò                                                             |
| ----------------------------- | ------------------------------------------------------------------- |
| Teacher / Course Creator      | Người dùng chính, xem dashboard, quyết định cải thiện, gửi reminder |
| Student                       | Nhận nhắc nhở, tiếp tục học                                         |
| AI System                     | Phân tích dữ liệu, tạo insight, đề xuất hành động                   |
| Udemy API / Udemy Export File | Nguồn dữ liệu                                                       |
| System Admin / Operator       | Giám sát vận hành, bảo mật, lỗi dữ liệu                             |

## 8. Ràng buộc hoặc giới hạn nghiệp vụ

MVP chỉ tập trung vào Udemy, dữ liệu kiểm thử ban đầu gồm **3 khóa học mẫu và khoảng 2.600 học viên hoạt động**, chưa hỗ trợ mobile app, marketplace riêng, recommendation engine phức tạp, A/B testing toàn diện hoặc tích hợp nền tảng ngoài Udemy. 

## 9. Sự kiện nghiệp vụ quan trọng

| Event                 | Mô tả                               |
| --------------------- | ----------------------------------- |
| TeacherLoggedIn       | Giáo viên đăng nhập                 |
| UdemyDataConnected    | Kết nối dữ liệu thành công          |
| DataImported          | Import dữ liệu thành công           |
| DropOffDetected       | Phát hiện điểm học viên bỏ cuộc cao |
| AIInsightGenerated    | AI tạo insight                      |
| RecommendationCreated | Hệ thống tạo đề xuất                |
| ReminderSent          | Gửi nhắc nhở cho học viên           |
| StudentReEngaged      | Học viên quay lại học               |
| InterventionEvaluated | Đánh giá hiệu quả can thiệp         |

## 10. Edge Cases cần xử lý

| Edge Case                                     | Cách cần xử lý                                          |
| --------------------------------------------- | ------------------------------------------------------- |
| File Udemy thiếu cột hoặc sai format          | Báo lỗi rõ ràng, không phân tích sai                    |
| API Udemy lỗi hoặc mất kết nối                | Retry / thông báo giáo viên                             |
| Dữ liệu học viên bị thiếu                     | Chỉ phân tích phần đủ dữ liệu, cảnh báo độ tin cậy thấp |
| Drop-off quá ít dữ liệu                       | Không đưa insight chắc chắn                             |
| AI tạo insight không hợp lý                   | Giáo viên phải có quyền bỏ qua                          |
| Reminder gửi trùng                            | Chặn duplicate để tránh spam                            |
| Học viên đã hoàn thành khóa học               | Không gửi nhắc quay lại học                             |
| Học viên inactive nhưng không có email hợp lệ | Không gửi, ghi nhận lỗi                                 |
| Một học viên thuộc nhiều nhóm can thiệp       | Ưu tiên rule tránh gửi nhiều tin                        |
| Dữ liệu nhạy cảm                              | Phải ẩn danh hóa/mã hóa trước khi xử lý                 |
