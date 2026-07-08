# API Contract Lite Spec - Nền tảng AI Learning Analytics

Tài liệu này xác định API Contract Lite đóng vai trò là hợp đồng giao tiếp giữa AI Frontend và AI Backend để phát triển các tính năng MVP của hệ thống AI Learning Analytics cho giáo viên Udemy.

---

## Danh sách API

* [[POST] Login](#1-post-login)
* [[POST] Connect Udemy API](#2-post-connect-udemy-api)
* [[POST] Upload Udemy Export File](#3-post-upload-udemy-export-file)
* [[GET] Get Course List](#4-get-get-course-list)
* [[GET] Get Course Dashboard Overview](#5-get-get-course-dashboard-overview)
* [[GET] Get Drop-off Point Analysis](#6-get-get-drop-off-point-analysis)
* [[GET] Get AI Insights for Lesson](#7-get-get-ai-insights-for-lesson)
* [[POST] Update Recommendation Status](#8-post-update-recommendation-status)
* [[GET] Get At-risk Students & Message Template](#9-get-get-at-risk-students--message-template)
* [[POST] Send Student Reminder](#10-post-send-student-reminder)

---

### 1. [POST] Login

| Field | Nội dung |
|---|---|
| **API Name** | Login |
| **Purpose** | Giáo viên đăng nhập để xác thực tài khoản vào hệ thống. |
| **Endpoint** | `POST /api/v1/auth/login` |
| **Actor** | Teacher / Course Creator |
| **Input** | `email` (string, required), `password` (string, required) |
| **Output** | `token` (string), `teacherId` (string), `name` (string) |
| **Business Rules** | - Mật khẩu phải được mã hóa trước khi truyền tải.<br>- Sau 5 lần đăng nhập sai liên tiếp, tài khoản của giáo viên sẽ tạm thời bị khóa trong vòng 15 phút. |
| **Error Cases** | - `400 Bad Request` - Thiếu các trường bắt buộc.<br>- `401 Unauthorized` - Email hoặc mật khẩu không chính xác.<br>- `423 Locked` - Tài khoản đang bị khóa tạm thời. |
| **Related AC** | US-001 AC-01, AC-02, AC-03 |

---

### 2. [POST] Connect Udemy API

| Field | Nội dung |
|---|---|
| **API Name** | Connect Udemy API |
| **Purpose** | Thiết lập kết nối API Udemy tự động. |
| **Endpoint** | `POST /api/v1/data/udemy-connection` |
| **Actor** | Teacher / Course Creator |
| **Input** | `clientId` (string, required), `clientSecret` (string, required) |
| **Output** | `connectionId` (string), `status` (string, e.g., "connected"), `connectedAt` (datetime) |
| **Business Rules** | Hệ thống phải kiểm tra thông tin kết nối bằng cách gửi yêu cầu xác thực thử tới Udemy trước khi lưu trạng thái. |
| **Error Cases** | - `400 Bad Request` - Thiếu Client ID hoặc Client Secret.<br>- `401 Unauthorized` - Thông tin kết nối không hợp lệ từ phía Udemy. |
| **Related AC** | US-002 AC-01 |

---

### 3. [POST] Upload Udemy Export File

| Field | Nội dung |
|---|---|
| **API Name** | Upload Udemy File |
| **Purpose** | Giáo viên tải tệp CSV/XLSX xuất từ Udemy lên hệ thống để phân tích thủ công. |
| **Endpoint** | `POST /api/v1/data/upload` |
| **Actor** | Teacher / Course Creator |
| **Input** | `file` (binary/multipart, required, format: CSV/XLSX) |
| **Output** | `importId` (string), `status` (string, e.g., "processing"), `fileName` (string) |
| **Business Rules** | - Chỉ chấp nhận các tệp xuất bản chính thức từ Udemy.<br>- Dữ liệu cá nhân nhạy cảm của học viên (như Email) phải được mã hóa/ẩn danh hóa ngay trong quá trình nạp dữ liệu.<br>- Giới hạn MVP: Tổng quy mô xử lý không quá 3 khóa học mẫu và 2.600 học viên. |
| **Error Cases** | - `400 Bad Request` - Không tải file hoặc file sai định dạng/thiếu các cột dữ liệu bắt buộc.<br>- `413 Payload Too Large` - Kích thước tệp vượt giới hạn cho phép. |
| **Related AC** | US-002 AC-02, AC-03 |

---

### 4. [GET] Get Course List

| Field | Nội dung |
|---|---|
| **API Name** | Get Course List |
| **Purpose** | Lấy danh sách các khóa học đã được kết nối/import của giáo viên hiện tại. |
| **Endpoint** | `GET /api/v1/courses` |
| **Actor** | Teacher / Course Creator |
| **Input** | None |
| **Output** | `courses` (array of objects) gồm: `courseId` (string), `title` (string), `studentCount` (int), `status` (string) |
| **Business Rules** | Chỉ trả về danh sách các khóa học thuộc quyền sở hữu của giáo viên đang đăng nhập (xác thực qua token). |
| **Error Cases** | - `401 Unauthorized` - Token không hợp lệ hoặc đã hết hạn. |
| **Related AC** | US-003 AC-02 |

---

### 5. [GET] Get Course Dashboard Overview

| Field | Nội dung |
|---|---|
| **API Name** | Get Course Dashboard Overview |
| **Purpose** | Lấy dữ liệu và chỉ số tổng quan phục vụ cho việc hiển thị Dashboard khóa học. |
| **Endpoint** | `GET /api/v1/courses/{courseId}/dashboard` |
| **Actor** | Teacher / Course Creator |
| **Input** | `courseId` (string, required in path) |
| **Output** | `courseId` (string), `completionRate` (float), `dropOffRate` (float), `activeStudents` (int), `inactiveStudents` (int), `atRiskStudents` (int) |
| **Business Rules** | - Học viên Active: Có tương tác trong 7 ngày gần nhất.<br>- Học viên Inactive: Không có tương tác trong 30 ngày gần nhất.<br>- Học viên At-risk: Không học bài mới từ 14 đến 29 ngày.<br>- Kiểm tra quyền sở hữu khóa học trước khi trả về dữ liệu. |
| **Error Cases** | - `403 Forbidden` - Giáo viên không có quyền truy cập khóa học này.<br>- `404 Not Found` - Không tồn tại khóa học hoặc chưa có dữ liệu phân tích. |
| **Related AC** | US-003 AC-01 |

---

### 6. [GET] Get Drop-off Point Analysis

| Field | Nội dung |
|---|---|
| **API Name** | Get Drop-off Point Analysis |
| **Purpose** | Lấy sơ đồ phễu qua các bài học để định vị vị trí dừng học phổ biến nhất. |
| **Endpoint** | `GET /api/v1/courses/{courseId}/drop-off-analysis` |
| **Actor** | Teacher / Course Creator |
| **Input** | `courseId` (string, required in path) |
| **Output** | `modules` (array of objects) gồm:<br>- `moduleId` (string), `moduleTitle` (string)<br>- `lessons` (array of objects) gồm: `lessonId` (string), `lessonTitle` (string), `type` (string), `dropOffRate` (float), `hasWarning` (boolean), `timelineAnalysis` (array of objects, optional) |
| **Business Rules** | - Đánh dấu `hasWarning` = true nếu bài học có tỷ lệ drop-off > 20%.<br>- Chỉ thực hiện phân tích chi tiết nếu bài học có tối thiểu 30 học viên đã từng tham gia học. |
| **Error Cases** | - `403 Forbidden` - Giáo viên không có quyền truy cập khóa học này.<br>- `404 Not Found` - Không tồn tại dữ liệu phân tích điểm dừng cho khóa học này. |
| **Related AC** | US-004 AC-01, AC-02 |

---

### 7. [GET] Get AI Insights for Lesson

| Field | Nội dung |
|---|---|
| **API Name** | Get AI Insights for Lesson |
| **Purpose** | Lấy giả thuyết phân tích nguyên nhân và các đề xuất hành động từ AI cho bài học cụ thể. |
| **Endpoint** | `GET /api/v1/courses/{courseId}/lessons/{lessonId}/ai-insights` |
| **Actor** | Teacher / Course Creator |
| **Input** | `courseId` (string, required in path), `lessonId` (string, required in path) |
| **Output** | `lessonId` (string), `insights` (array of objects gồm: `insightId`, `hypothesis`, `confidenceScore`), `recommendations` (array of objects gồm: `recommendationId`, `suggestionText`, `status`) |
| **Business Rules** | - Không sinh insight nếu bài học chưa đủ độ tin cậy về số lượng dữ liệu (dưới 30 học viên).<br>- Phải trả về kèm văn bản từ chối trách nhiệm pháp lý (AI chỉ mang tính tham khảo). |
| **Error Cases** | - `403 Forbidden` - Giáo viên không có quyền truy cập khóa học này.<br>- `404 Not Found` - Không tìm thấy bài giảng hoặc chưa tạo gợi ý AI cho bài giảng này. |
| **Related AC** | US-005 AC-01 |

---

### 8. [POST] Update Recommendation Status

| Field | Nội dung |
|---|---|
| **API Name** | Update Recommendation Status |
| **Purpose** | Ghi nhận hành động của giáo viên đối với đề xuất của AI (Áp dụng hoặc Bỏ qua). |
| **Endpoint** | `POST /api/v1/courses/{courseId}/lessons/{lessonId}/recommendations/{recommendationId}/action` |
| **Actor** | Teacher / Course Creator |
| **Input** | `courseId` (string, required in path), `lessonId` (string, required in path), `recommendationId` (string, required in path), `action` (string, required, enum: ["applied", "ignored"]) |
| **Output** | `recommendationId` (string), `status` (string), `updatedAt` (datetime) |
| **Business Rules** | - Nếu action là "ignored", hệ thống sẽ ẩn đề xuất khỏi giao diện hiển thị cho giáo viên và ghi nhận lịch sử phản hồi để tối ưu hóa các đề xuất AI trong tương lai. |
| **Error Cases** | - `400 Bad Request` - Trường action không đúng định dạng.<br>- `404 Not Found` - Không tìm thấy đề xuất phù hợp để cập nhật. |
| **Related AC** | US-005 AC-02 |

---

### 9. [GET] Get At-risk Students & Message Template

| Field | Nội dung |
|---|---|
| **API Name** | Get At-risk Students & Template |
| **Purpose** | Lấy danh sách học viên bỏ dở của bài giảng và mẫu tin nhắn đã tối ưu theo best practice. |
| **Endpoint** | `GET /api/v1/courses/{courseId}/lessons/{lessonId}/at-risk-students` |
| **Actor** | Teacher / Course Creator |
| **Input** | `courseId` (string, required in path), `lessonId` (string, required in path) |
| **Output** | `lessonId` (string), `defaultMessageTemplate` (string), `students` (array of objects) gồm: `studentId` (string), `maskedName` (string), `daysInactive` (int), `canSendReminder` (boolean) |
| **Business Rules** | - Tên học viên trả về ở frontend phải được ẩn danh hóa (ví dụ: "Nguy*** A***").<br>- Mẫu tin nhắn `defaultMessageTemplate` được dựng từ AI, tích hợp best practice từ học viên hoàn thành nhanh và hỗ trợ các placeholders: `{student_name}`, `{lesson_name}`, `{best_practice_tip}`.<br>- Thuộc tính `canSendReminder` = false nếu học viên đã nhận tin nhắn trong vòng 7 ngày qua. |
| **Error Cases** | - `403 Forbidden` - Giáo viên không có quyền truy cập khóa học này.<br>- `404 Not Found` - Không tìm thấy thông tin bài học. |
| **Related AC** | US-006 AC-01, AC-03 |

---

### 10. [POST] Send Student Reminder

| Field | Nội dung |
|---|---|
| **API Name** | Send Student Reminder |
| **Purpose** | Gửi tin nhắn/email nhắc nhở cá nhân hóa cho danh sách học viên được chọn. |
| **Endpoint** | `POST /api/v1/courses/{courseId}/lessons/{lessonId}/send-reminder` |
| **Actor** | Teacher / Course Creator |
| **Input** | `courseId` (string, required in path), `lessonId` (string, required in path), `studentIds` (array of strings, required), `messageBody` (string, required) |
| **Output** | `sentCount` (int), `failedCount` (int), `failures` (array of objects gồm: `studentId`, `reason`) |
| **Business Rules** | - Hệ thống chặn gửi nhắc nhở nếu có bất kỳ học viên nào trong danh sách nhận được tin nhắn trong vòng 7 ngày qua.<br>- Sau khi gửi thành công, hệ thống tự động đăng ký trigger theo dõi kết quả hoạt động của học viên đó trong vòng 7 ngày tiếp theo để đánh giá hiệu quả can thiệp. |
| **Error Cases** | - `400 Bad Request` - Danh sách học viên hoặc nội dung tin nhắn rỗng.<br>- `429 Too Many Requests` - Vi phạm tần suất gửi tin nhắn đối với học viên (dưới 7 ngày). |
| **Related AC** | US-006 AC-01, AC-02, AC-03 |