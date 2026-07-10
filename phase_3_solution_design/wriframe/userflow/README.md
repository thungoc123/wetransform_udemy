# Tài liệu Phân tích và Chỉ mục User Flows (User Flow Index)

Tài liệu này thực hiện phân tích danh sách User Stories của hệ thống **Nền tảng AI Learning Analytics** và thực hiện phân nhóm chúng thành các hành trình người dùng (User Flows / User Journeys) hợp lý theo mục tiêu cốt lõi của giảng viên (Course Creator), đặc biệt trong bối cảnh chuyển đổi từ học online trên Udemy sang lớp học offline theo mô hình Online-to-Offline (O2O).

---

## Bước 1. Phân tích & Phân nhóm User Stories

Dưới đây là bảng phân tích chi tiết từng User Story dựa trên mục tiêu, tác nhân, điều kiện tiên quyết và mục tiêu kinh doanh:

| Story ID | Tiêu đề (Title) | Tác nhân chính (Actor) | Điều kiện tiên quyết (Preconditions) | Mục tiêu kinh doanh (Business Goal) | Phụ thuộc (Dependencies) |
|---|---|---|---|---|---|
| **US-001** | Giáo viên đăng nhập hệ thống | Teacher / Course Creator | Giáo viên đã được cấp tài khoản hợp lệ. | Bảo mật thông tin khóa học và cá nhân hóa trải nghiệm. | Không |
| **US-002** | Kết nối hoặc tải lên dữ liệu Udemy | Teacher / Course Creator | Giáo viên đã đăng nhập thành công. | Thu thập và nạp dữ liệu tiến trình học tập làm nguồn phân tích cho AI. | US-001 |
| **US-003** | Xem Dashboard tổng quan về khóa học | Teacher / Course Creator | Đã import dữ liệu thành công của ít nhất một khóa học. | Cung cấp cái nhìn toàn cảnh về sức khỏe khóa học và mức độ chuyên cần. | US-002 |
| **US-004** | Xem phân tích điểm dừng (Drop-off Point) | Teacher / Course Creator | Dữ liệu khóa học đã được phân tích hành vi hoàn thành. | Xác định chính xác các điểm nghẽn nội dung trong bài học. | US-003 |
| **US-005** | Xem gợi ý từ AI và đề xuất cải thiện | Teacher / Course Creator | Phát hiện điểm drop-off bất thường ở một bài giảng cụ thể. | Hỗ trợ giáo viên đưa ra quyết định cải tiến nội dung nhanh chóng bằng đề xuất cụ thể. | US-004 |
| **US-006** | Gửi nhắc nhở cho học viên bỏ dở sử dụng Best Practice | Teacher / Course Creator | Có danh sách học viên At-risk/Inactive; hệ thống đã đúc kết được best practice. | Tăng tỷ lệ học viên quay lại học (Re-engaged Rate) bằng tin nhắn tối ưu hóa. | US-002, US-003 |

### Lý do phân nhóm thành các User Flow chính:

Để đảm bảo các luồng đi liền mạch theo trải nghiệm thực tế và giải quyết trọn vẹn một mục tiêu độc lập của người dùng, chúng tôi nhóm 6 User Stories thành **4 User Flows** như sau:

1. **UF-001: Authentication (Đăng nhập & Xác thực)**
   * *Bao gồm*: [US-001](file:///c:/Users/admin/Documents/AI%20for%20vietnam/Agentic%20SDLC/phase_2_story_definition/UserStories.md#us-001-giáo-viên-đăng-nhập-hệ-thống).
   * *Lý do*: Luồng độc lập bảo mật quyền truy cập hệ thống. Đây là cánh cổng kiểm soát và thiết lập phiên làm việc cá nhân hóa cho giảng viên trước khi thao tác các tác vụ khác.

2. **UF-002: Data Integration & Ingestion (Kết nối & Nạp dữ liệu)**
   * *Bao gồm*: [US-002](file:///c:/Users/admin/Documents/AI%20for%20vietnam/Agentic%20SDLC/phase_2_story_definition/UserStories.md#us-002-kết-nối-hoặc-tải-lên-dữ-liệu-udemy).
   * *Lý do*: Tác vụ nạp dữ liệu (onboarding/setup) diễn ra độc lập. Nó bao gồm 2 nhánh hành động rõ rệt (Kết nối API và Tải tệp lên) với cơ chế xác thực, kiểm tra định dạng và báo cáo tiến trình xử lý dữ liệu đặc thù.

3. **UF-003: Course Analytics & AI Optimization (Phân tích khóa học & Tối ưu hóa bằng AI)**
   * *Bao gồm*: [US-003](file:///c:/Users/admin/Documents/AI%20for%20vietnam/Agentic%20SDLC/phase_2_story_definition/UserStories.md#us-003-xem-dashboard-tổng-quan-về-khóa-học), [US-004](file:///c:/Users/admin/Documents/AI%20for%20vietnam/Agentic%20SDLC/phase_2_story_definition/UserStories.md#us-004-xem-phân-tích-điểm-dừng-drop-off-point-analysis), [US-005](file:///c:/Users/admin/Documents/AI%20for%20vietnam/Agentic%20SDLC/phase_2_story_definition/UserStories.md#us-005-xem-gợi-y-nguyên-nhân-từ-ai-và-đề-xuất-cải-thiện).
   * *Lý do*: Tạo thành một hành trình phân tích khép kín (Analytics Loop). Giảng viên đi từ cái nhìn tổng quát (Dashboard tổng quan) -> Phát hiện điểm nghẽn chi tiết (Phân tích điểm dừng drop-off) -> Nhận giải thích lý do và hành động khắc phục cụ thể do AI gợi ý (AI Insights). 

4. **UF-004: Student Intervention & Re-engagement (Kích hoạt & Can thiệp học viên bỏ dở)**
   * *Bao gồm*: [US-006](file:///c:/Users/admin/Documents/AI%20for%20vietnam/Agentic%20SDLC/phase_2_story_definition/UserStories.md#us-006-gửi-nhắc-nhở-reminder-cho-học-viên-bỏ-dở-sử-dụng-best-practice).
   * *Lý do*: Sau khi đã hiểu vấn đề của bài học, giảng viên cần tác động trực tiếp tới các học viên bỏ dở để cứu vãn tỷ lệ hoàn thành. Luồng này tập trung vào hoạt động tương tác, biên soạn nội dung dựa trên Best Practice cá nhân hóa và quản lý tần suất gửi để tránh spam.

---

## Bước 2. Chỉ mục User Flows (User Flow Index)

Dưới đây là bảng chỉ mục chi tiết các User Flow được định nghĩa trong hệ thống:

| Flow ID | Flow Name (Tên Luồng) | User Goal (Mục tiêu của người dùng) | Related User Stories (Các Story liên quan) | Tài liệu chi tiết |
|---|---|---|---|---|
| **UF-001** | Authentication | Đăng nhập hệ thống an toàn để truy cập Dashboard | [US-001](file:///c:/Users/admin/Documents/AI%20for%20vietnam/Agentic%20SDLC/phase_2_story_definition/UserStories.md#us-001-giáo-viên-đăng-nhập-hệ-thống) | [UF-001_Authentication.md](file:///c:/Users/admin/Documents/AI%20for%20vietnam/Agentic%20SDLC/phase_3_solution_design/wriframe/userflow/UF-001_Authentication.md) |
| **UF-002** | Data Integration & Ingestion | Kết nối API Udemy hoặc tải lên tệp xuất Udemy thành công | [US-002](file:///c:/Users/admin/Documents/AI%20for%20vietnam/Agentic%20SDLC/phase_2_story_definition/UserStories.md#us-002-kết-nối-hoặc-tải-lên-dữ-liệu-udemy) | [UF-002_Data_Integration.md](file:///c:/Users/admin/Documents/AI%20for%20vietnam/Agentic%20SDLC/phase_3_solution_design/wriframe/userflow/UF-002_Data_Integration.md) |
| **UF-003** | Course Analytics & AI Optimization | Xem chỉ số tổng quan, phân tích điểm dừng và tối ưu hóa nội dung nhờ AI | [US-003](file:///c:/Users/admin/Documents/AI%20for%20vietnam/Agentic%20SDLC/phase_2_story_definition/UserStories.md#us-003-xem-dashboard-tổng-quan-về-khóa-học), [US-004](file:///c:/Users/admin/Documents/AI%20for%20vietnam/Agentic%20SDLC/phase_2_story_definition/UserStories.md#us-004-xem-phân-tích-điểm-dừng-drop-off-point-analysis), [US-005](file:///c:/Users/admin/Documents/AI%20for%20vietnam/Agentic%20SDLC/phase_2_story_definition/UserStories.md#us-005-xem-gợi-y-nguyên-nhân-từ-ai-và-đề-xuất-cải-thiện) | [UF-003_Course_Analytics_Optimization.md](file:///c:/Users/admin/Documents/AI%20for%20vietnam/Agentic%20SDLC/phase_3_solution_design/wriframe/userflow/UF-003_Course_Analytics_Optimization.md) |
| **UF-004** | Student Intervention & Re-engagement | Gửi nhắc nhở cá nhân hóa dựa trên Best Practice để giữ chân học viên | [US-006](file:///c:/Users/admin/Documents/AI%20for%20vietnam/Agentic%20SDLC/phase_2_story_definition/UserStories.md#us-006-gửi-nhắc-nhở-reminder-cho-học-viên-bỏ-dở-sử-dụng-best-practice) | [UF-004_Student_Intervention.md](file:///c:/Users/admin/Documents/AI%20for%20vietnam/Agentic%20SDLC/phase_3_solution_design/wriframe/userflow/UF-004_Student_Intervention.md) |
