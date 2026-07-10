# Screen Specification Overview

- **Specification ID**: SS-001
- **Related User Flow**: UF-001_Authentication.md
- **Related Screen Flow**: SF-001_Authentication.md
- **Feature Name**: Authentication
- **Description**: Mô tả chi tiết giao diện và hành vi cho luồng đăng nhập và xác thực giáo viên.
- **Primary Actor**: Teacher / Course Creator

---

# Screen List

| Screen ID | Screen Name | Screen Type |
|-----------|-------------|-------------|
| S-001 | Login Page | Page |
| S-002 | Login Error State | Page |
| S-003 | Dashboard Overview | Page |

---

# Screen Specifications

## S-001 Login Page

### Screen Information
- **Screen ID**: S-001
- **Screen Name**: Login Page
- **Screen Type**: Page
- **Purpose**: Cho phép giáo viên nhập thông tin đăng nhập và truy cập hệ thống.
- **Description**: Màn hình đầu vào của luồng đăng nhập, tập trung vào form và phản hồi validation.

### Entry Conditions
- **Previous Screen**: Landing Page hoặc màn hình yêu cầu đăng nhập
- **Entry Action**: Người dùng mở URL đăng nhập hoặc chuyển hướng từ màn hình cần xác thực
- **Entry Condition**: Người dùng chưa authenticated
- **Required Backend Preconditions**: Session chưa tồn tại; tài khoản hợp lệ đã được đăng ký

### Exit Conditions
- **Possible Destination(s)**: S-003 Dashboard Overview, S-002 Login Error State
- **Exit Trigger**: Submit đăng nhập thành công hoặc thất bại
- **Required Backend Interaction**: Gửi request xác thực và lưu session/token nếu thành công

### Layout Structure
- Header nhỏ
- Card form trung tâm
- Trường Email, Mật khẩu
- Nút đăng nhập
- Area thông báo lỗi inline

### UI Components
- Form
- Text field
- Password field
- Primary button
- Inline validation message
- Alert banner (nếu cần)

### User Actions
- Nhập email
- Nhập mật khẩu
- Submit đăng nhập
- Chuyển sang màn hình forgot password nếu có trong tương lai

### Validation Rules
- Email và mật khẩu là bắt buộc
- Hiển thị lỗi ngay tại chỗ khi trường trống
- Không gửi request khi validation fail
- Sai thông tin tài khoản sẽ chuyển sang S-002

### Screen States
- Default
- Error
- Disabled

### Screen Lifecycle
- Initialize → Render form → User input → Submit → Backend auth → Navigate or display error

### Navigation
- **Destination**: S-003
- **Condition**: Credentials hợp lệ
- **Navigation Type**: Redirect

- **Destination**: S-001
- **Condition**: Trường trống hoặc validation fail
- **Navigation Type**: Inline Update

- **Destination**: S-002
- **Condition**: Sai thông tin hoặc tài khoản bị khóa
- **Navigation Type**: Replace Page

### Business Rules
- BR-001: Mật khẩu phải được mã hóa và truyền qua HTTPS
- BR-002: Sau 5 lần đăng nhập sai, tài khoản bị khóa 15 phút

### Backend Interactions
- **Interaction Type**: Authentication
- **Trigger**: Người dùng submit form
- **Business Purpose**: Xác minh tài khoản và tạo session/token
- **HTTP Method**: POST
- **Endpoint**: To Be Defined

### Permissions
- Anonymous user

### Error Handling
- Validation error cho trường trống
- Authentication failure với thông báo chung
- Network failure hiển thị alert và giữ nguyên form

### Loading Behaviour
- Hiển thị trạng thái loading khi request đang được xử lý
- Không cho phép submit lặp lại trong khi request đang chạy

### Empty State
- Không áp dụng

### Accessibility Considerations
- Label rõ ràng cho input
- Focus tự động vào Email khi màn hình mở
- Contrasts đủ cho lỗi và CTA
- Keyboard navigation hỗ trợ

### Responsive Behaviour
- Desktop và mobile

### Dependencies
- Authentication service
- Session management
- Design system: form, button, alert

---

## S-002 Login Error State

### Screen Information
- **Screen ID**: S-002
- **Screen Name**: Login Error State
- **Screen Type**: Page
- **Purpose**: Cung cấp thông tin lỗi và cho phép thử lại đăng nhập.
- **Description**: Màn hình trạng thái lỗi sau khi đăng nhập thất bại hoặc tài khoản bị khóa.

### Entry Conditions
- **Previous Screen**: S-001
- **Entry Action**: Submit đăng nhập sai hoặc tài khoản bị khóa
- **Entry Condition**: Authentication failed
- **Required Backend Preconditions**: Backend đã xác nhận lỗi hoặc khóa tài khoản

### Exit Conditions
- **Possible Destination(s)**: S-001 Login Page
- **Exit Trigger**: Người dùng nhấn retry hoặc chờ hết thời gian khóa
- **Required Backend Interaction**: Có thể cần refresh trạng thái khóa tài khoản nếu hết thời gian

### Layout Structure
- Header/brand area
- Alert message area
- Form card còn giữ thông tin email đã nhập
- CTA retry

### UI Components
- Alert banner
- Retry button
- Form fields
- Help text

### User Actions
- Thử lại đăng nhập
- Quay lại form
- Đợi thời gian khóa kết thúc

### Validation Rules
- Không có validation mới
- Bắt buộc hiển thị thông báo lỗi phù hợp

### Screen States
- Error
- Processing

### Screen Lifecycle
- Receive error → Render alert → User retries → Navigate back

### Navigation
- **Destination**: S-001
- **Condition**: Retry hoặc hết khóa
- **Navigation Type**: Back/Redirect

### Business Rules
- BR-002: Tài khoản bị khóa 15 phút sau 5 lần sai
- System response phải giữ nguyên form để nhập lại

### Backend Interactions
- **Interaction Type**: Authentication
- **Trigger**: Retry or status refresh
- **Business Purpose**: Xác thực lại hoặc kiểm tra trạng thái khóa
- **HTTP Method**: POST
- **Endpoint**: To Be Defined

### Permissions
- Anonymous user

### Error Handling
- Hiển thị lỗi chung khi credentials sai
- Hiển thị thông báo khóa tài khoản khi vượt ngưỡng
- Nếu mạng lỗi, giữ màn hình với alert network issue

### Loading Behaviour
- Khi retry, hiển thị processing state trong thời gian request

### Empty State
- Không áp dụng

### Accessibility Considerations
- Alert phải được announced cho screen reader
- Focus chuyển về lỗi hoặc form sau khi hiển thị thông báo

### Responsive Behaviour
- Desktop và mobile

### Dependencies
- Authentication service
- Session state

---

## S-003 Dashboard Overview

### Screen Information
- **Screen ID**: S-003
- **Screen Name**: Dashboard Overview
- **Screen Type**: Page
- **Purpose**: Cung cấp cho giáo viên overview sau khi đăng nhập thành công.
- **Description**: Trang đích sau khi xác thực thành công, phục vụ điều hướng tiếp theo vào các module khác.

### Entry Conditions
- **Previous Screen**: S-001
- **Entry Action**: Login success
- **Entry Condition**: Session/token được tạo thành công
- **Required Backend Preconditions**: Authenticated session exists

### Exit Conditions
- **Possible Destination(s)**: Các module tiếp theo như analytics, data integration
- **Exit Trigger**: Người dùng điều hướng sang chức năng khác
- **Required Backend Interaction**: Load dashboard summary data

### Layout Structure
- Header
- Sidebar navigation
- Main content area
- Summary cards/CTA

### UI Components
- Header
- Sidebar navigation
- Cards
- CTA buttons
- Charts (nếu có dữ liệu)

### User Actions
- Xem dashboard overview
- Điều hướng sang analytics
- Điều hướng sang data integration

### Validation Rules
- Không có validation form
- Chỉ hiển thị dữ liệu được phép với tài khoản hiện tại

### Screen States
- Default
- Loading
- Empty

### Screen Lifecycle
- Initialize → Load session/context → Render dashboard → User may navigate away

### Navigation
- **Destination**: Analytics / Data Integration
- **Condition**: Người dùng chọn module
- **Navigation Type**: Redirect

### Business Rules
- Dashboard chỉ hiển thị dữ liệu được phép cho giáo viên đã authenticated

### Backend Interactions
- **Interaction Type**: Read
- **Trigger**: On page load
- **Business Purpose**: Load dashboard summary và danh sách khóa học
- **HTTP Method**: GET
- **Endpoint**: To Be Defined

### Permissions
- Authenticated teacher

### Error Handling
- Dữ liệu load fail hiển thị cảnh báo và empty state
- Permission denied chuyển sang access denied state nếu cần

### Loading Behaviour
- Hiển thị loading skeleton khi dữ liệu chưa sẵn sàng

### Empty State
- Nếu chưa có dữ liệu khóa học, hiển thị CTA kết nối dữ liệu

### Accessibility Considerations
- Navigation phải rõ ràng
- Cards và chart cần có labels
- Keyboard support cho navigation

### Responsive Behaviour
- Desktop và mobile

### Dependencies
- Dashboard service
- Session context
- Design system: cards, navigation, CTA

---

# Shared Components

## Layout
- Header
- Sidebar
- Content container

## Navigation
- Primary navigation
- Breadcrumb

## Forms
- Login form
- Validation messages

## Feedback
- Alert banner
- Inline validation
- Loading indicator

## Data Display
- Dashboard cards
- Summary metrics

## Overlay
- Modal (future use)

---

# Assumptions
- MVP chưa bao gồm luồng forgot password riêng
- Dashboard được mở sau khi session/token được tạo thành công
