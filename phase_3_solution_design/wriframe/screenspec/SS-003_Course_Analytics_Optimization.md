# Screen Specification Overview

- **Specification ID**: SS-003
- **Related User Flow**: UF-003_Course_Analytics_Optimization.md
- **Related Screen Flow**: SF-003_Course_Analytics_Optimization.md
- **Feature Name**: Course Analytics & AI Optimization
- **Description**: Mô tả chi tiết giao diện và hành vi cho luồng phân tích khóa học, xác định điểm drop-off và đề xuất cải thiện từ AI.
- **Primary Actor**: Teacher / Course Creator

---

# Screen List

| Screen ID | Screen Name | Screen Type |
|-----------|-------------|-------------|
| S-201 | Course Dashboard | Page |
| S-202 | Drop-off Analysis View | Page |
| S-203 | Lesson Detail View | Page |
| S-204 | AI Insight Panel | Page |
| S-205 | Empty / Low Data State | Result Page |

---

# Screen Specifications

## S-201 Course Dashboard

### Screen Information
- **Screen ID**: S-201
- **Screen Name**: Course Dashboard
- **Screen Type**: Page
- **Purpose**: Hiển thị tổng quan sức khỏe khóa học cho giáo viên.
- **Description**: Màn hình overview các khóa học đã kết nối, bao gồm completion/drop-off và phân loại học viên.

### Entry Conditions
- **Previous Screen**: Dashboard Overview hoặc navigation từ module analytics
- **Entry Action**: Người dùng mở analytics module
- **Entry Condition**: Có dữ liệu khóa học được import thành công
- **Required Backend Preconditions**: Background jobs đã xử lý dữ liệu và sẵn sàng cho analytics

### Exit Conditions
- **Possible Destination(s)**: S-202, S-205
- **Exit Trigger**: Người dùng chọn tab phân tích hoặc không có dữ liệu
- **Required Backend Interaction**: Load course overview metrics

### Layout Structure
- Header và sidebar
- KPI cards
- Charts summary
- List khóa học / selected course area

### UI Components
- KPI cards
- Charts
- Course selector
- Tabs
- Buttons

### User Actions
- Chọn khóa học
- Chuyển sang phân tích điểm dừng
- Xem métrics tổng quan

### Validation Rules
- Nếu chưa có dữ liệu, hiển thị empty state
- Nếu dữ liệu quá ít, đưa sang low-data state

### Screen States
- Default
- Loading
- Empty

### Screen Lifecycle
- Load page → Fetch metrics → Render cards/charts → Enable drill-down

### Navigation
- **Destination**: S-202
- **Condition**: Có dữ liệu và người dùng mở tab phân tích điểm dừng
- **Navigation Type**: Redirect

- **Destination**: S-205
- **Condition**: Không có dữ liệu / dữ liệu chưa sẵn sàng
- **Navigation Type**: Replace Page

### Business Rules
- BR-006: Học viên được phân loại Active/Inactive/At-risk theo khoảng thời gian hoạt động
- BR-007: Ngưỡng drop-off mặc định là 20%

### Backend Interactions
- **Interaction Type**: Read
- **Trigger**: On page load / course selection
- **Business Purpose**: Load overview metrics cho khóa học
- **HTTP Method**: GET
- **Endpoint**: To Be Defined

### Permissions
- Authenticated teacher with access to selected course

### Error Handling
- API fail: hiển thị lỗi và fallback state
- Missing data: chuyển sang empty state

### Loading Behaviour
- Skeleton/placeholder cho cards và charts khi dữ liệu đang tải

### Empty State
- CTA “Kết nối dữ liệu” chuyển sang flow import

### Accessibility Considerations
- Các charts cần có alternative text và accessible labels
- Tab navigation phải hỗ trợ keyboard

### Responsive Behaviour
- Desktop/tablet: layout 2-column; mobile: stacked

### Dependencies
- Analytics API
- Course data service
- Design system: cards, charts, tabs

---

## S-202 Drop-off Analysis View

### Screen Information
- **Screen ID**: S-202
- **Screen Name**: Drop-off Analysis View
- **Screen Type**: Page
- **Purpose**: Hiển thị biểu đồ phễu và các điểm nóng drop-off của khóa học.
- **Description**: Màn hình cho phép giáo viên xem các bài giảng có tỷ lệ drop-off cao và điều chỉnh ngưỡng cảnh báo.

### Entry Conditions
- **Previous Screen**: S-201
- **Entry Action**: Người dùng mở tab phân tích điểm dừng
- **Entry Condition**: Có dữ liệu analytics hợp lệ
- **Required Backend Preconditions**: Lesson metrics đã được tính toán

### Exit Conditions
- **Possible Destination(s)**: S-203, S-205
- **Exit Trigger**: Người dùng chọn bài giảng hoặc dữ liệu không đủ
- **Required Backend Interaction**: Load lesson-level metrics

### Layout Structure
- Funnel chart area
- Warning list / hot spots
- Filter/threshold control

### UI Components
- Charts
- Warning chips/badges
- Lesson list
- Slider hoặc input để chỉnh ngưỡng

### User Actions
- Chọn bài giảng
- Thay đổi ngưỡng cảnh báo
- Xem danh sách hot spots

### Validation Rules
- Bài giảng chỉ được highlight nếu drop-off vượt ngưỡng
- Dữ liệu quá ít sẽ không render timeline

### Screen States
- Default
- Loading
- Empty

### Screen Lifecycle
- Load chart data → Render funnel → Highlight warnings → User drills into lesson

### Navigation
- **Destination**: S-203
- **Condition**: Người dùng chọn bài giảng hợp lệ
- **Navigation Type**: Redirect

- **Destination**: S-205
- **Condition**: Không đủ dữ liệu thống kê
- **Navigation Type**: Replace Page

### Business Rules
- BR-007: Ngưỡng cảnh báo mặc định 20%
- BR-008: Chỉ kích hoạt timeline và AI insight khi bài học có tối thiểu 30 học viên

### Backend Interactions
- **Interaction Type**: Read
- **Trigger**: On screen load / threshold change
- **Business Purpose**: Tải funnel metrics và danh sách bài giảng warning
- **HTTP Method**: GET
- **Endpoint**: To Be Defined

### Permissions
- Authenticated teacher with access to course

### Error Handling
- Nếu metrics không có, hiển thị empty state
- Nếu query fail, hiển thị warning/error banner

### Loading Behaviour
- Load indicators cho chart và list

### Empty State
- Nếu không có hot spot, hiển thị message “không có bài học nào vượt ngưỡng”

### Accessibility Considerations
- Charts cần text alternative và accessible summaries
- Filter controls phải có label rõ

### Responsive Behaviour
- Desktop/tablet: side-by-side; mobile: stacked

### Dependencies
- Analytics service
- Design system: cards, badges, chart containers

---

## S-203 Lesson Detail View

### Screen Information
- **Screen ID**: S-203
- **Screen Name**: Lesson Detail View
- **Screen Type**: Page
- **Purpose**: Hiển thị dữ liệu chi tiết cho một bài giảng bị cảnh báo.
- **Description**: Màn hình drill-down cho lesson detail, timeline and engagement metrics.

### Entry Conditions
- **Previous Screen**: S-202
- **Entry Action**: Người dùng chọn một lesson từ funnel view
- **Entry Condition**: Lesson đã được xác định và có dữ liệu
- **Required Backend Preconditions**: Lesson analytics data đã sẵn sàng

### Exit Conditions
- **Possible Destination(s)**: S-204, S-205
- **Exit Trigger**: Người dùng mở AI insight hoặc dữ liệu không đủ tin cậy
- **Required Backend Interaction**: Load lesson detail data

### Layout Structure
- Lesson header
- Timeline chart hoặc chart thay thế
- Summary cards
- CTA mở AI insights

### UI Components
- Chart
- Summary cards
- Buttons
- Warning banner

### User Actions
- Xem thông tin bài giảng
- Mở AI insights
- Quay lại analysis view

### Validation Rules
- Nếu không đủ 30 học viên, không render timeline/AI insights
- Nếu bài giảng không phải video, render chart thay thế phù hợp

### Screen States
- Default
- Loading
- Error

### Screen Lifecycle
- Load lesson detail → Render chart/cards → User opens insight

### Navigation
- **Destination**: S-204
- **Condition**: Có đủ dữ liệu
- **Navigation Type**: Redirect

- **Destination**: S-205
- **Condition**: Dưới ngưỡng tin cậy
- **Navigation Type**: Replace Page

### Business Rules
- BR-008: Chỉ hiện timeline và AI insight khi đủ 30 học viên
- Bài giảng video có timeline; tài liệu/bài tập dùng chart khác

### Backend Interactions
- **Interaction Type**: Read
- **Trigger**: On lesson selection
- **Business Purpose**: Load lesson detail và raw engagement metrics
- **HTTP Method**: GET
- **Endpoint**: To Be Defined

### Permissions
- Authenticated teacher

### Error Handling
- Không có đủ data: hiển thị warning
- API failure: hiển thị retry/error state

### Loading Behaviour
- Spinner/skeleton cho charts và details

### Empty State
- Hiển thị cảnh báo “dữ liệu không đủ”

### Accessibility Considerations
- Chart cần text alternative và readable labels
- Focus order phải rõ trong page drill-down

### Responsive Behaviour
- Desktop/tablet/mobile

### Dependencies
- Lesson analytics service
- Design system: cards, buttons, chart styles

---

## S-204 AI Insight Panel

### Screen Information
- **Screen ID**: S-204
- **Screen Name**: AI Insight Panel
- **Screen Type**: Page
- **Purpose**: Hiển thị giả thuyết nguyên nhân và các đề xuất cải thiện từ AI.
- **Description**: Màn hình insight dành cho giáo viên xem và phản hồi đề xuất AI.

### Entry Conditions
- **Previous Screen**: S-203
- **Entry Action**: Người dùng mở AI insights
- **Entry Condition**: Có đủ dữ liệu để sinh insight
- **Required Backend Preconditions**: AI recommendations đã được tạo hoặc đang được tạo

### Exit Conditions
- **Possible Destination(s)**: S-203, S-201
- **Exit Trigger**: Người dùng áp dụng/bỏ qua hoặc quay lại
- **Required Backend Interaction**: Ghi nhận feedback và cập nhật mô hình

### Layout Structure
- Disclaimer AI section
- Insight cards
- Action buttons for each recommendation

### UI Components
- Cards
- Buttons
- Alert/Disclaimer banner
- Status badges

### User Actions
- Xem insight
- Bấm “Đã áp dụng”
- Bấm “Bỏ qua”
- Quay lại lesson detail

### Validation Rules
- Insight phải rõ là AI-generated và chỉ mang tính tham khảo
- Không tự động áp dụng thay đổi lên Udemy

### Screen States
- Default
- Success
- Error

### Screen Lifecycle
- Load AI insights → Render cards → User feedback → Update feedback state

### Navigation
- **Destination**: S-203
- **Condition**: Người dùng quay lại
- **Navigation Type**: Back

### Business Rules
- BR-009: Bắt buộc hiển thị disclaimer về AI
- Feedback “Bỏ qua” hoặc “Đã áp dụng” phải được lưu lại để tối ưu hóa model

### Backend Interactions
- **Interaction Type**: Read / Update
- **Trigger**: On open / on feedback submit
- **Business Purpose**: Load recommendations và ghi nhận hành động của giáo viên
- **HTTP Method**: GET/POST
- **Endpoint**: To Be Defined

### Permissions
- Authenticated teacher

### Error Handling
- Nếu API fail, hiển thị lỗi và giữ nguyên screen
- Nếu recommendation không khả dụng, hiển thị empty state

### Loading Behaviour
- Loading state khi fetch recommendations

### Empty State
- Nếu không có recommendation, hiển thị message phù hợp

### Accessibility Considerations
- Alert disclaimer phải dễ đọc
- Buttons phải có nhãn rõ

### Responsive Behaviour
- Desktop và mobile

### Dependencies
- AI recommendation service
- Feedback logging service
- Design system: card, alert, button

---

## S-205 Empty / Low Data State

### Screen Information
- **Screen ID**: S-205
- **Screen Name**: Empty / Low Data State
- **Screen Type**: Result Page
- **Purpose**: Hỗ trợ giáo viên khi chưa có dữ liệu hoặc dữ liệu không đủ tin cậy.
- **Description**: Màn hình fallback cho empty hoặc low-data conditions.

### Entry Conditions
- **Previous Screen**: S-201 / S-202 / S-203
- **Entry Action**: Không có dữ liệu hoặc dữ liệu quá ít
- **Entry Condition**: Không thể render analytics chính xác
- **Required Backend Preconditions**: Dataset không đủ hoặc chưa sẵn sàng

### Exit Conditions
- **Possible Destination(s)**: Import flow, Dashboard
- **Exit Trigger**: Người dùng chọn kết nối dữ liệu hoặc quay lại
- **Required Backend Interaction**: Có thể load import options nếu người dùng chọn CTA

### Layout Structure
- Empty state card
- CTA button
- Support text

### UI Components
- Illustration placeholder
- CTA button
- Message text

### User Actions
- Kết nối dữ liệu
- Quay lại dashboard

### Validation Rules
- Không áp dụng

### Screen States
- Empty
- Error

### Screen Lifecycle
- Trigger empty/low-data → render guidance state

### Navigation
- **Destination**: Import flow
- **Condition**: Người dùng chọn kết nối dữ liệu
- **Navigation Type**: Redirect

### Business Rules
- Low-data state phải ngăn hiển thị insights không đáng tin cậy

### Backend Interactions
- **Interaction Type**: Read
- **Trigger**: On entry
- **Business Purpose**: Kiểm tra dữ liệu có sẵn
- **HTTP Method**: GET
- **Endpoint**: To Be Defined

### Permissions
- Authenticated teacher

### Error Handling
- Không có lỗi riêng; màn hình này là state để xử lý missing data

### Loading Behaviour
- Không áp dụng

### Empty State
- Được dùng chính cho empty state

### Accessibility Considerations
- Copy phải rõ, CTA phải visible
- Không dùng màu alone để communicate state

### Responsive Behaviour
- Desktop và mobile

### Dependencies
- Data availability service
- Design system: empty state component

---

# Shared Components

## Layout
- Header
- Sidebar
- Main content area

## Navigation
- Tabs
- Filter chips

## Forms
- Không có form chính

## Feedback
- Warning badges
- Alert banners
- Loading skeletons

## Data Display
- KPI cards
- Charts
- Lesson tables

## Overlay
- Modal (nếu mở insight hoặc filter ở overlay)

---

# Assumptions
- AI insight được render trên page thay vì modal
- Nếu dữ liệu không đủ, hệ thống hiển thị low-data state thay vì chart sai lệch
