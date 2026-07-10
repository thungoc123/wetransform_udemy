# Screen Specification Overview

- **Specification ID**: SS-002
- **Related User Flow**: UF-002_Data_Integration.md
- **Related Screen Flow**: SF-002_Data_Integration.md
- **Feature Name**: Data Integration
- **Description**: Mô tả chi tiết giao diện và hành vi cho luồng kết nối và nạp dữ liệu từ Udemy.
- **Primary Actor**: Teacher / Course Creator

---

# Screen List

| Screen ID | Screen Name | Screen Type |
|-----------|-------------|-------------|
| S-101 | Data Source Management | Page |
| S-102 | API Connection Form | Form |
| S-103 | File Upload Screen | Page |
| S-104 | Processing Status | Processing Page |
| S-105 | Success / Error Feedback | Result Page |

---

# Screen Specifications

## S-101 Data Source Management

### Screen Information
- **Screen ID**: S-101
- **Screen Name**: Data Source Management
- **Screen Type**: Page
- **Purpose**: Cho phép giáo viên chọn phương thức nhập dữ liệu Udemy.
- **Description**: Màn hình lựa chọn giữa API kết nối và upload file.

### Entry Conditions
- **Previous Screen**: Dashboard hoặc Settings
- **Entry Action**: Người dùng mở quản lý nguồn dữ liệu
- **Entry Condition**: Tài khoản đã authenticated
- **Required Backend Preconditions**: Có thể load các tùy chọn nhập dữ liệu hiện có

### Exit Conditions
- **Possible Destination(s)**: S-102, S-103
- **Exit Trigger**: Người dùng chọn API hoặc upload file
- **Required Backend Interaction**: Không bắt buộc, nhưng có thể load metadata cho phương thức đã chọn

### Layout Structure
- Title và mô tả ngắn
- 2 option cards
- CTA cho mỗi phương thức
- Helper text về giới hạn MVP

### UI Components
- Cards
- Buttons
- Helper text
- Info callout

### User Actions
- Chọn Kết nối API
- Chọn Tải file
- Xem quy định giới hạn MVP

### Validation Rules
- Không có validation form tại màn hình này
- Chỉ cho phép chọn phương thức hợp lệ

### Screen States
- Default

### Screen Lifecycle
- Initialize → Render options → User selects method → Navigate

### Navigation
- **Destination**: S-102
- **Condition**: Chọn API
- **Navigation Type**: Redirect

- **Destination**: S-103
- **Condition**: Chọn File Upload
- **Navigation Type**: Redirect

### Business Rules
- BR-003: Chỉ chấp nhận file format chuẩn Udemy
- BR-005: Hỗ trợ tối đa 3 khóa học và 2.600 học viên trong MVP

### Backend Interactions
- **Interaction Type**: Read
- **Trigger**: On load
- **Business Purpose**: Load tùy chọn phương thức và giới hạn hệ thống
- **HTTP Method**: GET
- **Endpoint**: To Be Defined

### Permissions
- Authenticated teacher

### Error Handling
- Nếu không có dữ liệu hoặc option không khả dụng, hiển thị warning

### Loading Behaviour
- Không có loading chính, chỉ render ngay

### Empty State
- Không áp dụng

### Accessibility Considerations
- Các option cards phải có nhãn và focus rõ ràng
- Hỗ trợ keyboard

### Responsive Behaviour
- Desktop và mobile

### Dependencies
- Data source options service
- Design system: cards, buttons

---

## S-102 API Connection Form

### Screen Information
- **Screen ID**: S-102
- **Screen Name**: API Connection Form
- **Screen Type**: Form
- **Purpose**: Thu thập thông tin kết nối để đồng bộ dữ liệu từ Udemy qua API.
- **Description**: Form nhập credentials và bắt đầu quá trình đồng bộ.

### Entry Conditions
- **Previous Screen**: S-101
- **Entry Action**: Người dùng chọn API integration
- **Entry Condition**: Chưa có kết nối thành công
- **Required Backend Preconditions**: Tài khoản teacher hợp lệ

### Exit Conditions
- **Possible Destination(s)**: S-104 Processing Status, S-105 Success / Error Feedback
- **Exit Trigger**: Submit credentials và kết quả auth
- **Required Backend Interaction**: Verify credentials và bắt đầu import

### Layout Structure
- Form header
- Các trường Client ID, API Key
- Nút kết nối
- Error state area

### UI Components
- Text fields
- Primary button
- Validation hints
- Error alert

### User Actions
- Nhập credentials
- Submit kết nối
- Sửa lại thông tin sau khi lỗi

### Validation Rules
- Client ID và API Key là bắt buộc
- Invalid credentials hiển thị lỗi cụ thể
- Mismatch với schema hoặc timeout phải báo lỗi

### Screen States
- Default
- Error
- Processing

### Screen Lifecycle
- Render form → User input → Submit → Validate → Backend auth → Navigate to processing/result

### Navigation
- **Destination**: S-104
- **Condition**: Credentials hợp lệ
- **Navigation Type**: Redirect

- **Destination**: S-105
- **Condition**: Kết nối thất bại
- **Navigation Type**: Modal/Result Page

### Business Rules
- BR-003: Chỉ sử dụng thông tin credentials hợp lệ
- BR-004: Dữ liệu import phải được ẩn danh hóa PII
- BR-005: Chặn nếu vượt quá giới hạn MVP

### Backend Interactions
- **Interaction Type**: Authentication / Create
- **Trigger**: Submit form
- **Business Purpose**: Verify API credentials và bắt đầu import dữ liệu
- **HTTP Method**: POST
- **Endpoint**: To Be Defined

### Permissions
- Authenticated teacher

### Error Handling
- Sai credentials: hiển thị lỗi trên form
- Timeout/rate limit: hiển thị thông báo retry
- Nếu server fail, chuyển sang S-105 với error state

### Loading Behaviour
- Hiển thị loading state khi đang kiểm tra kết nối

### Empty State
- Không áp dụng

### Accessibility Considerations
- Labels phải luôn visible
- Alert phải được announced
- Hỗ trợ keyboard và focus management

### Responsive Behaviour
- Desktop và mobile

### Dependencies
- Udemy API integration
- Authentication service
- Design system: form, button, alert

---

## S-103 File Upload Screen

### Screen Information
- **Screen ID**: S-103
- **Screen Name**: File Upload Screen
- **Screen Type**: Page
- **Purpose**: Cho phép giáo viên upload file dữ liệu Udemy.
- **Description**: Màn hình upload cho luồng file-based import.

### Entry Conditions
- **Previous Screen**: S-101
- **Entry Action**: Người dùng chọn upload file
- **Entry Condition**: File upload method selected
- **Required Backend Preconditions**: Giáo viên đã authenticated

### Exit Conditions
- **Possible Destination(s)**: S-104 Processing Status, S-105 Success / Error Feedback
- **Exit Trigger**: Upload hợp lệ hoặc không hợp lệ
- **Required Backend Interaction**: Upload file và parse schema

### Layout Structure
- Upload area
- File metadata section
- CTA upload
- Error/help text

### UI Components
- File upload area
- Drag/drop zone
- File list / preview
- Button
- Error text

### User Actions
- Chọn file
- Drag và drop file
- Upload file
- Hủy hoặc chọn lại file

### Validation Rules
- Chỉ chấp nhận CSV/XLSX chuẩn Udemy
- Kiểm tra cấu trúc cột và dữ liệu
- Chặn upload nếu quá giới hạn MVP

### Screen States
- Default
- Error
- Processing

### Screen Lifecycle
- Render uploader → User selects file → Validate → Upload → Processing

### Navigation
- **Destination**: S-104
- **Condition**: File hợp lệ
- **Navigation Type**: Redirect

- **Destination**: S-105
- **Condition**: File không hợp lệ hoặc vượt giới hạn
- **Navigation Type**: Modal/Result Page

### Business Rules
- BR-003: File phải đúng cấu trúc Udemy
- BR-004: Dữ liệu phải được ẩn danh hóa
- BR-005: Chặn khi vượt giới hạn MVP

### Backend Interactions
- **Interaction Type**: Upload
- **Trigger**: Upload file
- **Business Purpose**: Validate, parse và lưu dữ liệu file
- **HTTP Method**: POST
- **Endpoint**: To Be Defined

### Permissions
- Authenticated teacher

### Error Handling
- File format sai: hiển thị lỗi rõ ràng
- Thiếu cột bắt buộc: hiển thị danh sách cột lỗi
- Vượt quá giới hạn: hiển thị cảnh báo và cho phép điều chỉnh

### Loading Behaviour
- Hiển thị progress bar và trạng thái đang upload

### Empty State
- Prompt để chọn file

### Accessibility Considerations
- Upload control cần accessible label
- Các error messages cần rõ ràng
- Hỗ trợ keyboard

### Responsive Behaviour
- Desktop và mobile

### Dependencies
- File upload service
- Data parser service
- Design system: upload area, buttons

---

## S-104 Processing Status

### Screen Information
- **Screen ID**: S-104
- **Screen Name**: Processing Status
- **Screen Type**: Processing Page
- **Purpose**: Hiển thị tiến trình xử lý dữ liệu sau khi kết nối hoặc upload.
- **Description**: Màn hình trung gian cho các bước validate, parse, anonymize và lưu dữ liệu.

### Entry Conditions
- **Previous Screen**: S-102 hoặc S-103
- **Entry Action**: Kết nối hoặc upload bắt đầu
- **Entry Condition**: Backend đã nhận request và đang xử lý
- **Required Backend Preconditions**: Job xử lý dữ liệu được tạo thành công

### Exit Conditions
- **Possible Destination(s)**: S-105 Success / Error Feedback
- **Exit Trigger**: Xử lý hoàn tất hoặc thất bại
- **Required Backend Interaction**: Cập nhật trạng thái job và kết quả

### Layout Structure
- Title
- Progress bar/stepper
- Status message area
- Optional cancel action

### UI Components
- Progress bar
- Status text
- Step indicator
- Button (nếu cho phép hủy)

### User Actions
- Chờ tiến trình
- Hủy nếu hệ thống hỗ trợ

### Validation Rules
- Không có input validation tại màn hình này
- Chỉ hiển thị trạng thái quy trình

### Screen States
- Processing
- Success
- Error

### Screen Lifecycle
- Start processing → Update progress → Complete or fail → Navigate

### Navigation
- **Destination**: S-105
- **Condition**: Job hoàn tất hoặc lỗi
- **Navigation Type**: Replace Page

### Business Rules
- BR-004: PII phải được ẩn danh trong quá trình xử lý
- BR-005: Nếu vượt giới hạn MVP, workflow phải dừng

### Backend Interactions
- **Interaction Type**: Read / Create / Update
- **Trigger**: Background processing job
- **Business Purpose**: Lưu dữ liệu và cập nhật trạng thái xử lý
- **HTTP Method**: POST/GET
- **Endpoint**: To Be Defined

### Permissions
- Authenticated teacher

### Error Handling
- Nếu processing fail, chuyển sang S-105 error state
- Nếu dữ liệu không đồng nhất, hiển thị warning

### Loading Behaviour
- Màn hình chủ yếu là loading/progress state

### Empty State
- Không áp dụng

### Accessibility Considerations
- Cập nhật tiến trình cần được announced
- Progress bar cần có label

### Responsive Behaviour
- Desktop và mobile

### Dependencies
- Background job service
- Data processing service

---

## S-105 Success / Error Feedback

### Screen Information
- **Screen ID**: S-105
- **Screen Name**: Success / Error Feedback
- **Screen Type**: Result Page
- **Purpose**: Hiển thị kết quả cuối cùng của quá trình import.
- **Description**: Màn hình feedback cho kết quả thành công hoặc lỗi import.

### Entry Conditions
- **Previous Screen**: S-104 hoặc S-102/S-103
- **Entry Action**: Xử lý kết thúc
- **Entry Condition**: Job hoàn thành hoặc fail
- **Required Backend Preconditions**: Kết quả xử lý đã được tính toán

### Exit Conditions
- **Possible Destination(s)**: Dashboard, S-101, S-103
- **Exit Trigger**: Người dùng chọn tiếp tục, thử lại hoặc quay lại
- **Required Backend Interaction**: Có thể cần load dashboard summary sau import thành công

### Layout Structure
- Result card
- Success/error icon
- Message text
- CTA buttons

### UI Components
- Status icon
- Alert/message box
- Buttons
- Summary text

### User Actions
- Quay về dashboard
- Thử lại import
- Chỉnh sửa file hoặc credentials

### Validation Rules
- Không áp dụng

### Screen States
- Success
- Error

### Screen Lifecycle
- Process result → Render message → User chooses next action

### Navigation
- **Destination**: Dashboard
- **Condition**: Import thành công
- **Navigation Type**: Redirect

- **Destination**: S-101 or S-103
- **Condition**: Import lỗi
- **Navigation Type**: Back/Retry

### Business Rules
- BR-003/BR-004/BR-005 vẫn áp dụng ở mức thông báo
- Errors phải được hiển thị rõ ràng và không bị silent fail

### Backend Interactions
- **Interaction Type**: Read / Update
- **Trigger**: Finalize import result
- **Business Purpose**: Cập nhật trạng thái import và bổ sung summary
- **HTTP Method**: GET/POST
- **Endpoint**: To Be Defined

### Permissions
- Authenticated teacher

### Error Handling
- Import fail: hiển thị error detail
- Schema mismatch: hiển thị cột bị thiếu
- Permission denied: hiển thị thông báo phù hợp

### Loading Behaviour
- Không có loading chính

### Empty State
- Không áp dụng

### Accessibility Considerations
- Kết quả cần được announced
- CTA nên có contrast và focus rõ

### Responsive Behaviour
- Desktop và mobile

### Dependencies
- Dashboard route
- Import result service

---

# Shared Components

## Layout
- Header
- Sidebar
- Content body

## Navigation
- Tabs / choice cards
- CTA buttons

## Forms
- API form
- Upload form

## Feedback
- Progress bar
- Alert
- Toast

## Data Display
- File metadata summary
- Result cards

## Overlay
- Modal result state (optional)

---

# Assumptions
- Màn hình kết quả có thể là page hoặc modal tùy implementation
- Trong MVP, workflow import chỉ hỗ trợ một lần upload tại một thời điểm
