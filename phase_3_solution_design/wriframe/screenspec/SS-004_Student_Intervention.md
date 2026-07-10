# Screen Specification Overview

- **Specification ID**: SS-004
- **Related User Flow**: UF-004_Student_Intervention.md
- **Related Screen Flow**: SF-004_Student_Intervention.md
- **Feature Name**: Student Intervention & Re-engagement
- **Description**: Mô tả chi tiết giao diện và hành vi cho luồng can thiệp và nhắc nhở học viên bỏ dở.
- **Primary Actor**: Teacher / Course Creator

---

# Screen List

| Screen ID | Screen Name | Screen Type |
|-----------|-------------|-------------|
| S-301 | At-risk Student List | Page |
| S-302 | Reminder Composer Modal | Modal |
| S-303 | Confirmation / Delivery State | Result Page |
| S-304 | Re-engagement Summary | Page |

---

# Screen Specifications

## S-301 At-risk Student List

### Screen Information
- **Screen ID**: S-301
- **Screen Name**: At-risk Student List
- **Screen Type**: Page
- **Purpose**: Hiển thị danh sách học viên cần can thiệp.
- **Description**: Màn hình danh sách học viên At-risk/Inactive để giáo viên chọn đối tượng gửi nhắc nhở.

### Entry Conditions
- **Previous Screen**: Dashboard hoặc lesson detail
- **Entry Action**: Người dùng mở danh sách intervention
- **Entry Condition**: Có dữ liệu phân nhóm học viên và quyền can thiệp
- **Required Backend Preconditions**: Student engagement data đã được phân tích

### Exit Conditions
- **Possible Destination(s)**: S-302, S-301 (spam guard state)
- **Exit Trigger**: Người dùng chọn học viên hoặc bị chặn vì spam guard
- **Required Backend Interaction**: Load danh sách học viên và trạng thái last sent

### Layout Structure
- Header và filter bar
- Bảng học viên
- Cột trạng thái, last sent, action

### UI Components
- Table
- Filters
- Action buttons
- Status chips

### User Actions
- Chọn học viên
- Gửi nhắc nhở hàng loạt
- Filter danh sách

### Validation Rules
- Nếu học viên đã nhận tin trong vòng 7 ngày, nút gửi bị khóa
- Chỉ cho phép can thiệp với học viên thuộc phân khúc phù hợp

### Screen States
- Default
- Disabled
- Error

### Screen Lifecycle
- Load list → Render rows → User selects student → Open composer or show guard

### Navigation
- **Destination**: S-302
- **Condition**: Có thể can thiệp
- **Navigation Type**: Modal

- **Destination**: S-301
- **Condition**: Spam guard active
- **Navigation Type**: Inline Update

### Business Rules
- BR-010: Tần suất gửi tối đa 1 lần/7 ngày cho cùng một học viên
- BR-011: Tin nhắn phải được tạo dựa trên best practice từ nhóm hoàn thành nhanh

### Backend Interactions
- **Interaction Type**: Read
- **Trigger**: On screen load / action click
- **Business Purpose**: Load danh sách học viên và trạng thái last-sent
- **HTTP Method**: GET
- **Endpoint**: To Be Defined

### Permissions
- Authenticated teacher

### Error Handling
- Nếu data load fail: hiển thị error banner
- Nếu spam guard active: hiển thị cảnh báo màu vàng và khóa action

### Loading Behaviour
- Skeleton / loading state cho bảng nếu dữ liệu chậm

### Empty State
- Nếu không có học viên cần can thiệp, hiển thị empty state positive message

### Accessibility Considerations
- Bảng phải có semantic headers và keyboard navigation
- Các action buttons phải có label rõ

### Responsive Behaviour
- Desktop/tablet: table; mobile: stacked card layout

### Dependencies
- Intervention list API
- Student engagement service
- Design system: table, chips, buttons

---

## S-302 Reminder Composer Modal

### Screen Information
- **Screen ID**: S-302
- **Screen Name**: Reminder Composer Modal
- **Screen Type**: Modal
- **Purpose**: Cho phép giáo viên soạn và chỉnh sửa tin nhắc nhở.
- **Description**: Modal chứa message template được personalize dựa trên best practice và dữ liệu học viên.

### Entry Conditions
- **Previous Screen**: S-301
- **Entry Action**: Người dùng chọn học viên và bấm gửi nhắc nhở
- **Entry Condition**: Không bị spam guard
- **Required Backend Preconditions**: Template và personal data đã sẵn sàng

### Exit Conditions
- **Possible Destination(s)**: S-303, S-301
- **Exit Trigger**: Người dùng gửi hoặc hủy
- **Required Backend Interaction**: Gửi/nếu cần, lưu bản nháp hoặc log action

### Layout Structure
- Modal header
- Message composer area
- Personalization variables preview
- Buttons Send / Cancel

### UI Components
- Modal container
- Text area / rich text editor (nếu được cho phép)
- Buttons
- Preview text

### User Actions
- Chỉnh sửa template
- Gửi nhắc nhở
- Hủy modal

### Validation Rules
- Nội dung không được trống trước khi gửi
- Nếu thiếu thông tin, hiển thị lỗi validation

### Screen States
- Default
- Error

### Screen Lifecycle
- Open modal → load template → edit content → submit or cancel

### Navigation
- **Destination**: S-303
- **Condition**: Gửi thành công
- **Navigation Type**: Redirect

- **Destination**: S-301
- **Condition**: Người dùng hủy
- **Navigation Type**: Close

### Business Rules
- BR-011: Nội dung cần dựa trên best practice và personal data
- BR-010: Không được gửi lặp lại trong vòng 7 ngày

### Backend Interactions
- **Interaction Type**: Create
- **Trigger**: Send reminder
- **Business Purpose**: Gửi nhắc nhở và ghi nhận thông tin can thiệp
- **HTTP Method**: POST
- **Endpoint**: To Be Defined

### Permissions
- Authenticated teacher

### Error Handling
- Gửi lỗi: hiển thị thông báo và giữ modal mở
- Nếu người dùng không có quyền, hiển thị warning

### Loading Behaviour
- Loading state khi đang gửi reminder

### Empty State
- Không áp dụng

### Accessibility Considerations
- Modal phải có focus trap và close action rõ
- Textarea phải có label và keyboard support

### Responsive Behaviour
- Desktop và mobile

### Dependencies
- Reminder template service
- Messaging service
- Design system: modal, input, button

---

## S-303 Confirmation / Delivery State

### Screen Information
- **Screen ID**: S-303
- **Screen Name**: Confirmation / Delivery State
- **Screen Type**: Result Page
- **Purpose**: Hiển thị kết quả vụ gửi nhắc nhở và trạng thái theo dõi.
- **Description**: Màn hình trạng thái sau khi nhắc nhở được gửi hoặc gửi lỗi.

### Entry Conditions
- **Previous Screen**: S-302
- **Entry Action**: Người dùng bấm send hoặc gửi thất bại
- **Entry Condition**: Request gửi reminder đã được xử lý
- **Required Backend Preconditions**: Status delivery đã được trả về

### Exit Conditions
- **Possible Destination(s)**: S-304, S-301
- **Exit Trigger**: Người dùng tiếp tục xem results hoặc quay lại list
- **Required Backend Interaction**: Có thể cập nhật trạng thái theo dõi 7 ngày

### Layout Structure
- Result card
- Message status area
- CTA tiếp tục / quay lại

### UI Components
- Success/error icon
- Status message
- Buttons

### User Actions
- Xem kết quả theo dõi
- Quay lại danh sách học viên

### Validation Rules
- Không áp dụng

### Screen States
- Success
- Error

### Screen Lifecycle
- Submit reminder → show result → user chooses next action

### Navigation
- **Destination**: S-304
- **Condition**: Gửi thành công và cần theo dõi
- **Navigation Type**: Redirect

- **Destination**: S-301
- **Condition**: Quay lại danh sách
- **Navigation Type**: Back

### Business Rules
- BR-012: Học viên được gắn tag Re-engaged khi có hoạt động mới trong vòng 7 ngày

### Backend Interactions
- **Interaction Type**: Update / Create
- **Trigger**: After send action
- **Business Purpose**: Ghi nhận reminder delivery và bắt đầu theo dõi 7 ngày
- **HTTP Method**: POST
- **Endpoint**: To Be Defined

### Permissions
- Authenticated teacher

### Error Handling
- Delivery error: hiển thị message và hướng dẫn retry/điều chỉnh
- Bounce/unsubscribe: hiển thị cảnh báo và cập nhật trạng thái

### Loading Behaviour
- Loading state ở thời điểm gửi

### Empty State
- Không áp dụng

### Accessibility Considerations
- Status message cần được announced
- Buttons phải có màu contrast đủ

### Responsive Behaviour
- Desktop và mobile

### Dependencies
- Reminder delivery service
- Monitoring service

---

## S-304 Re-engagement Summary

### Screen Information
- **Screen ID**: S-304
- **Screen Name**: Re-engagement Summary
- **Screen Type**: Page
- **Purpose**: Hiển thị kết quả sau thời gian theo dõi 7 ngày.
- **Description**: Màn hình báo cáo can thiệp và trạng thái re-engagement của học viên.

### Entry Conditions
- **Previous Screen**: S-303
- **Entry Action**: Theo dõi đủ 7 ngày
- **Entry Condition**: Reminder đã được gửi và monitoring started
- **Required Backend Preconditions**: Activity data đã được sync sau khoảng thời gian theo dõi

### Exit Conditions
- **Possible Destination(s)**: S-301, end of flow
- **Exit Trigger**: Người dùng quay lại hoặc kết thúc
- **Required Backend Interaction**: Load monitoring summary

### Layout Structure
- Summary cards
- List/ table trạng thái re-engagement
- CTA quay lại

### UI Components
- Summary cards
- Status indicators
- Table
- Buttons

### User Actions
- Xem kết quả can thiệp
- Quay lại danh sách học viên

### Validation Rules
- Không áp dụng

### Screen States
- Default
- Success
- Empty

### Screen Lifecycle
- Load monitoring summary → Render outcomes → User exits

### Navigation
- **Destination**: S-301
- **Condition**: Người dùng quay lại list
- **Navigation Type**: Back

### Business Rules
- BR-012: Re-engaged chỉ được gán khi học viên có hoạt động mới trong 7 ngày

### Backend Interactions
- **Interaction Type**: Read
- **Trigger**: On page load
- **Business Purpose**: Load re-engagement results và thống kê
- **HTTP Method**: GET
- **Endpoint**: To Be Defined

### Permissions
- Authenticated teacher

### Error Handling
- Nếu không có dữ liệu monitoring: hiển thị empty state
- Nếu sync fail: hiển thị warning

### Loading Behaviour
- Loading state khi summary đang được tính toán

### Empty State
- Nếu chưa có dữ liệu theo dõi, hiển thị message chờ kết quả

### Accessibility Considerations
- Status badges cần có text rõ và contrast đủ
- Table cần accessibility support

### Responsive Behaviour
- Desktop và mobile

### Dependencies
- Monitoring analytics service
- Design system: cards, table, badges

---

# Shared Components

## Layout
- Header
- Sidebar
- Content area

## Navigation
- Filter bar
- Action buttons

## Forms
- Reminder composer

## Feedback
- Toast
- Alert banner
- Status chips

## Data Display
- Student table
- Summary cards

## Overlay
- Modal composer

---

# Assumptions
- Modal composer có thể được thay thế bằng drawer nếu implementation cần
- Theo dõi re-engagement được cập nhật sau 7 ngày và không phải real-time
