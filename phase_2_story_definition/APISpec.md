# API Specification Overview

- **API Specification ID**: API-001
- **Related User Flow**: UF-001_Authentication.md, UF-002_Data_Integration.md, UF-003_Course_Analytics_Optimization.md, UF-004_Student_Intervention.md
- **Related Screen Specification**: SS-001_Authentication.md, SS-002_Data_Integration.md, SS-003_Course_Analytics_Optimization.md, SS-004_Student_Intervention.md
- **Feature Name**: AI Learning Analytics MVP
- **Description**: Hợp đồng API implementation-ready cho các luồng đăng nhập, kết nối dữ liệu Udemy, phân tích khóa học, đề xuất AI và can thiệp học viên.

---

# API Inventory

| API ID | Endpoint | Method | Purpose | Related Screen(s) |
|---|---|---|---|---|
| API-001 | /api/v1/auth/login | POST | Xác thực giáo viên và tạo session | S-001, S-002, S-003 |
| API-002 | /api/v1/data/sources | GET | Lấy các phương thức ingest dữ liệu có sẵn | S-101 |
| API-003 | /api/v1/data/udemy-connection | POST | Thiết lập kết nối API Udemy | S-102 |
| API-004 | /api/v1/data/upload | POST | Upload file Udemy export và bắt đầu xử lý | S-103, S-104, S-105 |
| API-005 | /api/v1/courses | GET | Lấy danh sách khóa học thuộc quyền giáo viên | S-201 |
| API-006 | /api/v1/courses/{courseId}/dashboard | GET | Lấy tổng quan dashboard khóa học | S-201 |
| API-007 | /api/v1/courses/{courseId}/drop-off-analysis | GET | Lấy phân tích drop-off và hot spots | S-202 |
| API-008 | /api/v1/courses/{courseId}/lessons/{lessonId}/analytics | GET | Lấy chi tiết phân tích bài học | S-203 |
| API-009 | /api/v1/courses/{courseId}/lessons/{lessonId}/ai-insights | GET | Lấy gợi ý AI cho bài học | S-204 |
| API-010 | /api/v1/courses/{courseId}/lessons/{lessonId}/recommendations/{recommendationId}/action | POST | Ghi nhận hành động áp dụng/bỏ qua đề xuất AI | S-204 |
| API-011 | /api/v1/courses/{courseId}/lessons/{lessonId}/at-risk-students | GET | Lấy danh sách học viên At-risk và mẫu nhắc nhở | S-301, S-302 |
| API-012 | /api/v1/courses/{courseId}/lessons/{lessonId}/send-reminder | POST | Gửi nhắc nhở cho học viên được chọn | S-302, S-303, S-304 |

---

## API-001: Login

### API Information
- **API ID**: API-001
- **Endpoint**: POST /api/v1/auth/login
- **HTTP Method**: POST
- **Purpose**: Xác thực giáo viên để đăng nhập vào hệ thống.
- **Related Screens**: S-001, S-002, S-003
- **Related User Flow Steps**: UF-001 Happy Path, Exception Flows EF-001, EF-002, EF-003

### Trigger
- Người dùng nhập email và mật khẩu trên S-001 và bấm đăng nhập.
- Nếu thông tin sai, frontend chuyển sang S-002.

### Authentication
- Public

### Authorization
- Không cần quyền bổ sung; tài khoản phải hợp lệ.

### Request

#### Headers
- Authorization: Không bắt buộc
- Content-Type: application/json
- Accept: application/json

#### Path Parameters
- Không có

#### Query Parameters
- Không có

#### Request Body
| Name | Type | Required | Validation | Description |
|---|---|---|---|---|
| email | string | Yes | Format email, không được trống | Email giáo viên |
| password | string | Yes | Không được trống | Mật khẩu đăng nhập |

### Response
- **200 OK**: `token`, `teacherId`, `name`, `expiresAt`
- **400 Bad Request**: Thiếu trường bắt buộc hoặc định dạng sai
- **401 Unauthorized**: Email hoặc mật khẩu không chính xác
- **423 Locked**: Tài khoản bị khóa tạm thời

### Business Rules
- Mật khẩu phải được mã hóa khi truyền tải và lưu trữ.
- Sau 5 lần đăng nhập sai liên tiếp, tài khoản bị khóa 15 phút.

### Error Cases
- `400`: Trường email/password rỗng hoặc sai định dạng
- `401`: Sai credentials
- `423`: Tài khoản bị khóa

### Traceability
- User Flow: UF-001
- Screen Specification: SS-001
- Business Rules: BR-001, BR-002

---

## API-002: Get Data Source Options

### API Information
- **API ID**: API-002
- **Endpoint**: GET /api/v1/data/sources
- **HTTP Method**: GET
- **Purpose**: Lấy các phương thức nhập dữ liệu Udemy có sẵn cho giáo viên.
- **Related Screens**: S-101
- **Related User Flow Steps**: UF-002 Entry Point, Happy Path Step 1

### Trigger
- Khi người dùng mở màn hình Quản lý nguồn dữ liệu trên S-101.

### Authentication
- Authenticated User

### Authorization
- Giáo viên đã đăng nhập.

### Request

#### Headers
- Authorization: Bearer token
- Accept: application/json

#### Path Parameters
- Không có

#### Query Parameters
- Không có

#### Request Body
- Không có

### Response
- **200 OK**: `sources` gồm `id`, `name`, `type`, `description`, `enabled`

### Business Rules
- Chỉ trả về các phương thức đang được bật cho tài khoản hiện tại.

### Error Cases
- `401 Unauthorized`
- `403 Forbidden`

### Traceability
- User Flow: UF-002
- Screen Specification: SS-002

---

## API-003: Connect Udemy API

### API Information
- **API ID**: API-003
- **Endpoint**: POST /api/v1/data/udemy-connection
- **HTTP Method**: POST
- **Purpose**: Thiết lập kết nối API Udemy cho phép đồng bộ dữ liệu.
- **Related Screens**: S-102, S-104, S-105
- **Related User Flow Steps**: UF-002 Happy Path Nhánh A, EF-001

### Trigger
- Người dùng nhập Client ID và Client Secret trên S-102 và bấm kết nối.

### Authentication
- Authenticated User

### Authorization
- Giáo viên đã xác thực.

### Request

#### Headers
- Authorization: Bearer token
- Content-Type: application/json
- Accept: application/json

#### Path Parameters
- Không có

#### Query Parameters
- Không có

#### Request Body
| Name | Type | Required | Validation | Description |
|---|---|---|---|---|
| clientId | string | Yes | Không trống | Client ID từ Udemy |
| clientSecret | string | Yes | Không trống | Client Secret / API Key |

### Response
- **200 OK**: `connectionId`, `status`, `connectedAt`
- **400 Bad Request**: Thiếu trường hoặc format sai
- **401 Unauthorized**: Credentials không hợp lệ
- **429 Too Many Requests**: Rate limit hoặc timeout từ Udemy

### Business Rules
- Trước khi lưu trạng thái kết nối, hệ thống phải xác thực thông tin với Udemy.
- Nếu kết nối không hợp lệ, trạng thái phải giữ là chưa kết nối.

### Error Cases
- `400`: Thiếu clientId/clientSecret
- `401`: Thông tin kết nối không hợp lệ
- `429`: Timeout hoặc rate limit

### Traceability
- User Flow: UF-002
- Screen Specification: SS-002
- Business Rules: BR-003

---

## API-004: Upload Udemy Export File

### API Information
- **API ID**: API-004
- **Endpoint**: POST /api/v1/data/upload
- **HTTP Method**: POST
- **Purpose**: Upload file CSV/XLSX từ Udemy và bắt đầu xử lý import.
- **Related Screens**: S-103, S-104, S-105
- **Related User Flow Steps**: UF-002 Happy Path Nhánh B, EF-002, EF-003, EF-004

### Trigger
- Người dùng chọn hoặc kéo thả file trên S-103 và bấm tải lên.

### Authentication
- Authenticated User

### Authorization
- Giáo viên đã đăng nhập và có quyền import dữ liệu.

### Request

#### Headers
- Authorization: Bearer token
- Content-Type: multipart/form-data
- Accept: application/json

#### Path Parameters
- Không có

#### Query Parameters
- `source=udemy` (optional)

#### Request Body
| Name | Type | Required | Validation | Description |
|---|---|---|---|---|
| file | binary | Yes | CSV/XLSX, đúng cấu trúc Udemy | File export từ Udemy |

### Response
- **202 Accepted**: `importId`, `status`, `fileName`
- **400 Bad Request**: File không hợp lệ hoặc thiếu cột cần thiết
- **413 Payload Too Large**: File quá lớn

### Business Rules
- Chỉ chấp nhận file xuất bản chính thức từ Udemy.
- Dữ liệu PII phải được ẩn danh hóa ngay trong quá trình import.
- Tổng quy mô import không vượt quá 3 khóa học và 2.600 học viên trong MVP.

### Error Cases
- `400`: File sai định dạng/thiếu cột
- `413`: File vượt giới hạn

### Traceability
- User Flow: UF-002
- Screen Specification: SS-002
- Business Rules: BR-003, BR-004, BR-005

---

## API-005: Get Course List

### API Information
- **API ID**: API-005
- **Endpoint**: GET /api/v1/courses
- **HTTP Method**: GET
- **Purpose**: Lấy danh sách khóa học thuộc quyền sở hữu của giáo viên đang đăng nhập.
- **Related Screens**: S-201
- **Related User Flow Steps**: UF-003 Happy Path Steps 1-2

### Trigger
- Khi người dùng mở dashboard analytics trên S-201.

### Authentication
- Authenticated User

### Authorization
- Chỉ giáo viên có quyền truy cập mới được xem.

### Request

#### Headers
- Authorization: Bearer token
- Accept: application/json

#### Path Parameters
- Không có

#### Query Parameters
- `status` (optional)

#### Request Body
- Không có

### Response
- **200 OK**: `courses` array với `courseId`, `title`, `studentCount`, `status`

### Business Rules
- Chỉ trả về các khóa học thuộc quyền sở hữu của giáo viên.

### Error Cases
- `401 Unauthorized`
- `403 Forbidden`

### Traceability
- User Flow: UF-003
- Screen Specification: SS-003

---

## API-006: Get Course Dashboard Overview

### API Information
- **API ID**: API-006
- **Endpoint**: GET /api/v1/courses/{courseId}/dashboard
- **HTTP Method**: GET
- **Purpose**: Lấy các chỉ số tổng quan của một khóa học.
- **Related Screens**: S-201
- **Related User Flow Steps**: UF-003 Happy Path Steps 2-3

### Trigger
- Khi giáo viên chọn khóa học trên S-201.

### Authentication
- Authenticated User

### Authorization
- Giáo viên có quyền truy cập khóa học đó.

### Request

#### Headers
- Authorization: Bearer token
- Accept: application/json

#### Path Parameters
| Name | Type | Required | Validation | Description |
|---|---|---|---|---|
| courseId | string | Yes | UUID/string | ID khóa học |

#### Query Parameters
- Không có

#### Request Body
- Không có

### Response
- **200 OK**: `courseId`, `completionRate`, `dropOffRate`, `activeStudents`, `inactiveStudents`, `atRiskStudents`

### Business Rules
- Active: có tương tác trong 7 ngày gần nhất.
- Inactive: không có tương tác trong 30 ngày gần nhất.
- At-risk: không học bài mới từ 14 đến 29 ngày.

### Error Cases
- `403 Forbidden`
- `404 Not Found`

### Traceability
- User Flow: UF-003
- Screen Specification: SS-003
- Business Rules: BR-006

---

## API-007: Get Drop-off Point Analysis

### API Information
- **API ID**: API-007
- **Endpoint**: GET /api/v1/courses/{courseId}/drop-off-analysis
- **HTTP Method**: GET
- **Purpose**: Trả về phân tích phễu drop-off theo các bài học của khóa học.
- **Related Screens**: S-202, S-203
- **Related User Flow Steps**: UF-003 Happy Path Steps 3-4, AF-001

### Trigger
- Khi giáo viên mở tab phễu drop-off trên S-202.

### Authentication
- Authenticated User

### Authorization
- Giáo viên có quyền truy cập khóa học.

### Request

#### Headers
- Authorization: Bearer token
- Accept: application/json

#### Path Parameters
| Name | Type | Required | Validation | Description |
|---|---|---|---|---|
| courseId | string | Yes | string | ID khóa học |

#### Query Parameters
- `threshold` (optional, numeric)

#### Request Body
- Không có

### Response
- **200 OK**: `modules` array, mỗi module có `lessons` array với `lessonId`, `lessonTitle`, `type`, `dropOffRate`, `hasWarning`, `timelineAnalysis`

### Business Rules
- `hasWarning=true` khi drop-off >20%.
- Phân tích chi tiết timeline chỉ có nếu ít nhất 30 học viên từng tham gia.

### Error Cases
- `403 Forbidden`
- `404 Not Found`

### Traceability
- User Flow: UF-003
- Screen Specification: SS-003
- Business Rules: BR-007, BR-008

---

## API-008: Get Lesson Analytics Detail

### API Information
- **API ID**: API-008
- **Endpoint**: GET /api/v1/courses/{courseId}/lessons/{lessonId}/analytics
- **HTTP Method**: GET
- **Purpose**: Lấy dữ liệu chi tiết cho một bài giảng được chọn.
- **Related Screens**: S-203
- **Related User Flow Steps**: UF-003 Happy Path Step 4, EF-002, EF-003

### Trigger
- Khi giáo viên chọn một bài học trên S-202 để xem chi tiết trên S-203.

### Authentication
- Authenticated User

### Authorization
- Giáo viên có quyền truy cập khóa học và bài học tương ứng.

### Request

#### Headers
- Authorization: Bearer token
- Accept: application/json

#### Path Parameters
| Name | Type | Required | Validation | Description |
|---|---|---|---|---|
| courseId | string | Yes | string | ID khóa học |
| lessonId | string | Yes | string | ID bài học |

#### Query Parameters
- Không có

#### Request Body
- Không có

### Response
- **200 OK**: `lessonId`, `lessonTitle`, `type`, `engagementMetrics`, `timelineAnalysis`, `reliabilityMessage`

### Business Rules
- Nếu số lượng học viên dưới ngưỡng 30, API trả về trạng thái low-data thay vì timeline đầy đủ.
- Với bài tập/text, timeline có thể không có và trả về chart thay thế.

### Error Cases
- `403 Forbidden`
- `404 Not Found`

### Traceability
- User Flow: UF-003
- Screen Specification: SS-003
- Business Rules: BR-008

---

## API-009: Get AI Insights for Lesson

### API Information
- **API ID**: API-009
- **Endpoint**: GET /api/v1/courses/{courseId}/lessons/{lessonId}/ai-insights
- **HTTP Method**: GET
- **Purpose**: Trả về giả thuyết nguyên nhân và đề xuất cải thiện từ AI cho một bài học.
- **Related Screens**: S-204
- **Related User Flow Steps**: UF-003 Happy Path Step 5, EF-005

### Trigger
- Khi giáo viên mở tab AI Insight trên S-204.

### Authentication
- Authenticated User

### Authorization
- Giáo viên có quyền xem khóa học.

### Request

#### Headers
- Authorization: Bearer token
- Accept: application/json

#### Path Parameters
| Name | Type | Required | Validation | Description |
|---|---|---|---|---|
| courseId | string | Yes | string | ID khóa học |
| lessonId | string | Yes | string | ID bài học |

#### Query Parameters
- Không có

#### Request Body
- Không có

### Response
- **200 OK**: `lessonId`, `insights`, `recommendations`, `disclaimerText`

### Business Rules
- Không sinh insight nếu bài học chưa đủ độ tin cậy (dưới 30 học viên).
- Phải trả về disclaimer: AI chỉ mang tính tham khảo.

### Error Cases
- `403 Forbidden`
- `404 Not Found`

### Traceability
- User Flow: UF-003
- Screen Specification: SS-003
- Business Rules: BR-008, BR-009

---

## API-010: Update Recommendation Status

### API Information
- **API ID**: API-010
- **Endpoint**: POST /api/v1/courses/{courseId}/lessons/{lessonId}/recommendations/{recommendationId}/action
- **HTTP Method**: POST
- **Purpose**: Ghi nhận phản hồi của giáo viên đối với đề xuất AI.
- **Related Screens**: S-204
- **Related User Flow Steps**: UF-003 Happy Path Step 6

### Trigger
- Khi giáo viên bấm “Đã áp dụng” hoặc “Bỏ qua” trên S-204.

### Authentication
- Authenticated User

### Authorization
- Giáo viên có quyền tác động vào recommendation của khóa học.

### Request

#### Headers
- Authorization: Bearer token
- Content-Type: application/json
- Accept: application/json

#### Path Parameters
| Name | Type | Required | Validation | Description |
|---|---|---|---|---|
| courseId | string | Yes | string | ID khóa học |
| lessonId | string | Yes | string | ID bài học |
| recommendationId | string | Yes | string | ID đề xuất AI |

#### Query Parameters
- Không có

#### Request Body
| Name | Type | Required | Validation | Description |
|---|---|---|---|---|
| action | string | Yes | enum: applied, ignored | Hành động của giáo viên |

### Response
- **200 OK**: `recommendationId`, `status`, `updatedAt`
- **400 Bad Request**: `action` không hợp lệ
- **404 Not Found**: Recommendation không tồn tại

### Business Rules
- Nếu action là ignored, recommendation bị ẩn khỏi UI và ghi nhận lịch sử phản hồi.

### Error Cases
- `400`: action không đúng định dạng
- `404`: recommendation không tồn tại

### Traceability
- User Flow: UF-003
- Screen Specification: SS-003

---

## API-011: Get At-risk Students & Message Template

### API Information
- **API ID**: API-011
- **Endpoint**: GET /api/v1/courses/{courseId}/lessons/{lessonId}/at-risk-students
- **HTTP Method**: GET
- **Purpose**: Trả về danh sách học viên At-risk và mẫu tin nhắc nhở tối ưu.
- **Related Screens**: S-301, S-302
- **Related User Flow Steps**: UF-004 Happy Path Steps 1-3, EF-001

### Trigger
- Khi giáo viên mở danh sách học viên cần can thiệp trên S-301.

### Authentication
- Authenticated User

### Authorization
- Giáo viên có quyền truy cập khóa học và bài học.

### Request

#### Headers
- Authorization: Bearer token
- Accept: application/json

#### Path Parameters
| Name | Type | Required | Validation | Description |
|---|---|---|---|---|
| courseId | string | Yes | string | ID khóa học |
| lessonId | string | Yes | string | ID bài học |

#### Query Parameters
- Không có

#### Request Body
- Không có

### Response
- **200 OK**: `lessonId`, `defaultMessageTemplate`, `students` array với `studentId`, `maskedName`, `daysInactive`, `canSendReminder`

### Business Rules
- Tên học viên phải được ẩn danh hóa trước khi trả về frontend.
- `defaultMessageTemplate` phải có placeholders `{student_name}`, `{lesson_name}`, `{best_practice_tip}`.
- `canSendReminder=false` nếu học viên đã nhận nhắc nhở trong vòng 7 ngày.

### Error Cases
- `403 Forbidden`
- `404 Not Found`

### Traceability
- User Flow: UF-004
- Screen Specification: SS-004
- Business Rules: BR-010, BR-011

---

## API-012: Send Student Reminder

### API Information
- **API ID**: API-012
- **Endpoint**: POST /api/v1/courses/{courseId}/lessons/{lessonId}/send-reminder
- **HTTP Method**: POST
- **Purpose**: Gửi nhắc nhở cá nhân hóa tới danh sách học viên được chọn.
- **Related Screens**: S-302, S-303, S-304
- **Related User Flow Steps**: UF-004 Happy Path Steps 3-5, EF-001, EF-002

### Trigger
- Khi giáo viên chỉnh sửa nội dung trên S-302 và bấm gửi.

### Authentication
- Authenticated User

### Authorization
- Giáo viên có quyền gửi nhắc nhở cho khóa học đó.

### Request

#### Headers
- Authorization: Bearer token
- Content-Type: application/json
- Accept: application/json

#### Path Parameters
| Name | Type | Required | Validation | Description |
|---|---|---|---|---|
| courseId | string | Yes | string | ID khóa học |
| lessonId | string | Yes | string | ID bài học |

#### Query Parameters
- Không có

#### Request Body
| Name | Type | Required | Validation | Description |
|---|---|---|---|---|
| studentIds | array[string] | Yes | Không rỗng | Danh sách học viên được chọn |
| messageBody | string | Yes | Không trống | Nội dung tin nhắn/email |

### Response
- **200 OK**: `sentCount`, `failedCount`, `failures`
- **400 Bad Request**: Danh sách học viên hoặc nội dung rỗng
- **429 Too Many Requests**: Vi phạm tần suất gửi trong vòng 7 ngày

### Business Rules
- Chặn gửi nếu bất kỳ học viên nào trong danh sách đã nhận nhắc nhở trong vòng 7 ngày.
- Sau khi gửi thành công, hệ thống tự động kích hoạt theo dõi phản hồi 7 ngày.

### Error Cases
- `400`: studentIds/messageBody rỗng
- `429`: gửi vượt tần suất cho học viên

### Traceability
- User Flow: UF-004
- Screen Specification: SS-004
- Business Rules: BR-010, BR-012
