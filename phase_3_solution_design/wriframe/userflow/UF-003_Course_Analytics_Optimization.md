# User Flow: UF-003 - Course Analytics & AI Optimization (Phân tích khóa học & Tối ưu hóa bằng AI)

Tài liệu này đặc tả chi tiết luồng phân tích sức khỏe khóa học, xác định điểm dừng (drop-off) và khám phá các đề xuất cải tiến nội dung bằng AI.

---

## 1. Flow Overview
* **Flow ID**: UF-003
* **Flow Name**: Course Analytics & AI Optimization (Phân tích khóa học & Tối ưu hóa bằng AI)
* **Description**: Giảng viên xem Dashboard tổng quan khóa học, đi sâu phân tích biểu đồ phễu bài giảng để tìm ra điểm nóng học viên dừng học đột ngột (drop-off), kiểm tra timeline video bị tắt, và xem các đề xuất cải thiện nội dung từ trợ lý AI.
* **Primary Actor**: Teacher / Course Creator (Giảng viên / Người tạo khóa học)
* **User Goal**: Xác định chính xác bài giảng bị lỗi nội dung và áp dụng các đề xuất tối ưu hóa cụ thể của AI để cải thiện tỷ lệ hoàn thành khóa học.
* **Related User Stories**: 
  * [US-003: Xem Dashboard tổng quan về khóa học](file:///c:/Users/admin/Documents/AI%20for%20vietnam/Agentic%20SDLC/phase_2_story_definition/UserStories.md#us-003-xem-dashboard-tổng-quan-về-khóa-học)
  * [US-004: Xem phân tích điểm dừng (Drop-off Point Analysis)](file:///c:/Users/admin/Documents/AI%20for%20vietnam/Agentic%20SDLC/phase_2_story_definition/UserStories.md#us-004-xem-phân-tích-điểm-dừng-drop-off-point-analysis)
  * [US-005: Xem gợi ý nguyên nhân từ AI và đề xuất cải thiện](file:///c:/Users/admin/Documents/AI%20for%20vietnam/Agentic%20SDLC/phase_2_story_definition/UserStories.md#us-005-xem-gợi-ý-nguyên-nhân-từ-ai-và-đề-xuất-cải-thiện)

---

## 2. Entry Points
* Đăng nhập thành công từ [UF-001](file:///c:/Users/admin/Documents/AI%20for%20vietnam/Agentic%20SDLC/phase_3_solution_design/wriframe/userflow/UF-001_Authentication.md) tự động chuyển hướng về trang chủ Dashboard.
* Nhấp chọn vào một khóa học cụ thể từ danh sách khóa học ở trang quản trị hệ thống.

---

## 3. Preconditions
* Giảng viên đã nạp dữ liệu Udemy thành công cho ít nhất một khóa học (hoàn thành [UF-002](file:///c:/Users/admin/Documents/AI%20for%20vietnam/Agentic%20SDLC/phase_3_solution_design/wriframe/userflow/UF-002_Data_Integration.md)).
* Nền tảng đã xử lý xong các tác vụ nền (background jobs) phân tích cấu trúc bài học và logs hoạt động của học viên.

---

## 4. Happy Path
| Step | Actor | Action | System Response | Related Story |
| :---: | :---: | :---: | :---: | :---: |
| 1 | Giảng viên | Truy cập trang chủ hệ thống | Hiển thị danh sách các khóa học đã kết nối kèm các thông tin tóm tắt nhanh. | [US-003](file:///c:/Users/admin/Documents/AI%20for%20vietnam/Agentic%20SDLC/phase_2_story_definition/UserStories.md#us-003-xem-dashboard-tổng-quan-về-khóa-học) |
| 2 | Giảng viên | Chọn một khóa học cụ thể cần phân tích | Tải và hiển thị Dashboard tổng quan khóa học gồm: Completion Rate, Drop-off Rate, số lượng học viên theo phân loại (Active, Inactive, At-risk). | [US-003](file:///c:/Users/admin/Documents/AI%20for%20vietnam/Agentic%20SDLC/phase_2_story_definition/UserStories.md#us-003-xem-dashboard-tổng-quan-về-khóa-học) |
| 3 | Giảng viên | Nhấp chuyển sang Tab "Phân tích điểm dừng" | Hiển thị biểu đồ hình phễu (funnel chart) theo thứ tự các bài giảng trong khóa học. Các bài giảng có tỷ lệ drop-off >20% sẽ được tô màu đỏ nổi bật trong danh sách "Điểm nóng cần cải thiện". | [US-004](file:///c:/Users/admin/Documents/AI%20for%20vietnam/Agentic%20SDLC/phase_2_story_definition/UserStories.md#us-004-xem-phân-tích-điểm-dừng-drop-off-point-analysis) |
| 4 | Giảng viên | Nhấp chọn một bài giảng bị cảnh báo (loại Video, đã có trên 30 học viên) | Mở trang chi tiết bài học, hiển thị biểu đồ dòng thời gian (timeline chart) chỉ ra giây/phút học viên bấm tắt video nhiều nhất. | [US-004](file:///c:/Users/admin/Documents/AI%20for%20vietnam/Agentic%20SDLC/phase_2_story_definition/UserStories.md#us-004-xem-phân-tích-điểm-dừng-drop-off-point-analysis) |
| 5 | Giảng viên | Nhấp vào khu vực tab "Phân tích AI & Gợi ý" | 1. Hiển thị thông báo miễn trừ trách nhiệm (BR-009).<br>2. Hiển thị giả thuyết nguyên nhân (ví dụ: video bài giảng dài quá 15 phút gây oải).<br>3. Hiển thị danh sách đề xuất giải pháp kèm nút "Đã áp dụng" và "Bỏ qua". | [US-005](file:///c:/Users/admin/Documents/AI%20for%20vietnam/Agentic%20SDLC/phase_2_story_definition/UserStories.md#us-005-xem-gợi-ý-nguyên-nhân-từ-ai-và-đề-xuất-cải-thiện) |
| 6 | Giảng viên | Nhấp chọn "Bỏ qua" một đề xuất AI không phù hợp | Hệ thống ghi nhận phản hồi, ẩn đề xuất đó khỏi giao diện, và điều chỉnh trọng số thuật toán học máy (để giảm các gợi ý tương tự về sau). | [US-005](file:///c:/Users/admin/Documents/AI%20for%20vietnam/Agentic%20SDLC/phase_2_story_definition/UserStories.md#us-005-xem-gợi-ý-nguyên-nhân-từ-ai-và-đề-xuất-cải-thiện) |

---

## 5. Decision Points
### D-001: Giảng viên đã nạp dữ liệu khóa học nào chưa?
* **YES**: Hiển thị Dashboard khóa học đầy đủ thông số.
* **NO**: Chuyển tới **Exception Flow: Dashboard trống**.

### D-002: Tỷ lệ drop-off của bài giảng có vượt ngưỡng cấu hình (mặc định 20%)?
* **YES**: Tô màu đỏ/cam nổi bật bài học trên biểu đồ hình phễu và đưa vào danh sách "Điểm nóng cần cải thiện".
* **NO**: Hiển thị màu xanh/xám tiêu chuẩn.

### D-003: Số lượng học viên tương tác với bài giảng đạt tối thiểu 30 người?
* **YES**: Bật đầy đủ biểu đồ chi tiết điểm dừng timeline và phân tích AI.
* **NO**: Chuyển tới **Exception Flow: Không đủ độ tin cậy thống kê** (Khóa hiển thị biểu đồ timeline/AI).

### D-004: Bài giảng được chọn có định dạng Video không?
* **YES**: Hiển thị biểu đồ timeline mức độ giữ chân học viên theo từng giây/phút của video.
* **NO** *(Ví dụ: Bài tập, Tài liệu PDF)*: Chuyển tới **Exception Flow: Bài giảng không phải video** (Chỉ hiển thị tỷ lệ hoàn thành/dừng chung).

---

## 6. Alternative Flows
### AF-001: Thay đổi cấu hình ngưỡng cảnh báo Drop-off
* **Mô tả**: Giảng viên điều chỉnh ngưỡng cảnh báo để hệ thống lọc các điểm nóng theo mong muốn của mình.
* **Các bước thực hiện**:
  1. Tại màn hình "Phân tích điểm dừng", giảng viên nhấp vào biểu tượng Cài đặt kế bên phễu bài giảng.
  2. Điều chỉnh thanh trượt (slider) thay đổi ngưỡng cảnh báo (ví dụ: hạ xuống 15%).
  3. Hệ thống tính toán lại lập tức và cập nhật danh sách "Điểm nóng cần cải thiện" theo ngưỡng mới.

---

## 7. Exception Flows
### EF-001: Dashboard trống (Chưa có dữ liệu)
* **Mô tả**: Giảng viên đăng nhập lần đầu và chưa import dữ liệu Udemy.
* **Các bước thực hiện**:
  1. Giảng viên vào Dashboard.
  2. Hệ thống phát hiện không có dữ liệu khóa học nào tồn tại.
  3. Hệ thống hiển thị giao diện trống (Empty State) kèm hình minh họa và thông điệp: *"Chào mừng giảng viên! Hãy kết nối hoặc tải lên dữ liệu Udemy để bắt đầu phân tích sức khỏe khóa học."*
  4. Hiển thị nút bấm CTA nổi bật "Kết nối dữ liệu" chuyển hướng sang [UF-002](file:///c:/Users/admin/Documents/AI%20for%20vietnam/Agentic%20SDLC/phase_3_solution_design/wriframe/userflow/UF-002_Data_Integration.md).

### EF-002: Không đủ độ tin cậy thống kê (Dưới 30 học viên)
* **Mô tả**: Bài giảng được chọn có số học viên tham gia quá ít, dữ liệu không đại diện.
* **Các bước thực hiện**:
  1. Giảng viên nhấp chọn một bài giảng có dưới 30 học viên.
  2. Hệ thống chặn vẽ biểu đồ timeline video và chặn tạo gợi ý AI.
  3. Hệ thống hiển thị thông báo thay thế: *"Bài học này chỉ có [X]/30 học viên tham gia học. Hiện chưa đủ độ tin cậy thống kê để tiến hành phân tích chi tiết. Vui lòng quay lại khi có thêm nhiều học viên hoàn thành hơn."*

### EF-003: Bài giảng không phải Video (Tài liệu đọc, bài tập thực hành)
* **Mô tả**: Bài giảng thuộc định dạng văn bản (text/PDF) hoặc bài tập trắc nghiệm/coding.
* **Các bước thực hiện**:
  1. Giảng viên nhấp chọn một bài giảng thuộc dạng bài tập thực hành.
  2. Hệ thống kiểm tra thấy không có dữ liệu timeline video.
  3. Hệ thống ẩn biểu đồ dòng thời gian (timeline chart) và thay thế bằng biểu đồ hình cột phân phối tỷ lệ học viên: Hoàn thành, Không hoàn thành, Bỏ dở giữa chừng.
  4. Các gợi ý AI (nếu có) sẽ được thiết kế riêng cho dạng bài tập (ví dụ: gợi ý giảm độ khó của câu hỏi trắc nghiệm).

### EF-004: Thời gian tải biểu đồ chậm do dữ liệu lớn (Edge Case)
* **Mô tả**: Dữ liệu có lượng học viên lớn hoặc nhiều bài học làm chậm truy vấn.
* **Các bước thực hiện**:
  1. Giảng viên tải trang Dashboard hoặc chuyển Tab Phân tích điểm dừng.
  2. Hệ thống tải dữ liệu lâu hơn 2 giây.
  3. Hệ thống hiển thị trạng thái tải ảo (Skeleton Loading Screen) ở vị trí các biểu đồ để tạo trải nghiệm mượt mà, ngăn giảng viên click lặp đi lặp lại gây treo trang.

### EF-005: Đề xuất AI nằm ngoài khả năng hỗ trợ của Udemy (Edge Case)
* **Mô tả**: AI đề xuất thay đổi vượt quá công nghệ hoặc tính năng Udemy cung cấp.
* **Các bước thực hiện**:
  1. Hệ thống AI phân tích bài giảng và đưa ra đề xuất kỹ thuật (ví dụ: *"Hãy tích hợp thêm một trò chơi mini-game tương tác ở phút thứ 5 của video"*).
  2. Hệ thống phát hiện đề xuất này không tương thích trực tiếp với Udemy Editor.
  3. Hệ thống đính kèm nhãn cảnh báo: **[Thực hiện thủ công ngoài Udemy]**.
  4. Giảng viên xem đề xuất và có thể nhấp "Bỏ qua". Hệ thống ghi nhận để phạt thuật toán sinh gợi ý này.

---

## 8. Business Rules Applied
* **BR-006 (Phân loại trạng thái học viên)**:
  * **Học viên Active**: Có ghi nhận hoạt động học tập trong 7 ngày gần nhất.
  * **Học viên Inactive**: Không ghi nhận hoạt động học tập nào trong 30 ngày gần nhất.
  * **Học viên At-risk**: Không ghi nhận hoạt động học tập mới từ 14 ngày đến 29 ngày. *(Nguồn: US-003)*
* **BR-007 (Ngưỡng cảnh báo mặc định)**: Ngưỡng tỷ lệ drop-off mặc định để đánh dấu cảnh báo một bài học là từ 20% trở lên. Giảng viên có quyền cấu hình động ngưỡng này. *(Nguồn: US-004)*
* **BR-008 (Ngưỡng tin cậy thống kê)**: Chỉ kích hoạt tính năng phân tích điểm dừng chi tiết (Timeline video) và sinh gợi ý AI khi bài học có tối thiểu 30 học viên từng tham gia học. *(Nguồn: US-004, US-005)*
* **BR-009 (Tuyên bố miễn trừ trách nhiệm của AI)**: Bắt buộc hiển thị tuyên bố rõ ràng: *"Các gợi ý, nhận định của trợ lý AI được tự động tạo dựa trên hành vi học tập và chỉ mang tính chất tham khảo. Giảng viên chịu trách nhiệm cuối cùng đối với quyết định thay đổi nội dung khóa học trên Udemy."* *(Nguồn: US-005)*

---

## 9. Success State
* Các số liệu Dashboard hiển thị chính xác tương ứng với dữ liệu Udemy đã import.
* Điểm nóng bài giảng được làm nổi bật trực quan trên biểu đồ.
* Giáo viên đọc được giả thuyết nguyên nhân và các đề xuất hành động cụ thể từ AI.
* Mọi hành vi bấm "Bỏ qua" hoặc "Đã áp dụng" của giảng viên đều được lưu trữ thành công để tối ưu hóa AI.

---

## 10. Failure State
* Không tải được biểu đồ và hiển thị thông báo lỗi mạng.
* Các chỉ số hiển thị sai lệch hoặc không khớp với dữ liệu gốc của Udemy.

---

## 11. Mermaid User Flow
```mermaid
flowchart TD
    Start([Bắt đầu]) --> CheckData{D-001: Có dữ liệu khóa học?}
    
    CheckData -- NO (EF-001) --> EmptyDash[Hiển thị Giao diện trống]
    EmptyDash --> ClickImport[Nhấn CTA Kết nối dữ liệu] --> Redirect[Chuyển sang UF-002]
    
    CheckData -- YES --> RenderOverview[Tải Dashboard tổng quan khóa học]
    RenderOverview --> ViewStats[Xem Completion, Drop-off, Active, Inactive, At-risk]
    
    ViewStats --> TabDropOff[Chuyển sang Tab Phân tích điểm dừng]
    TabDropOff --> GetFunnel[Hệ thống hiển thị Biểu đồ hình phễu]
    
    GetFunnel --> CheckDropOff{D-002: Drop-off > Ngưỡng 20%?}
    CheckDropOff -- YES --> HighlightRed[Tô đỏ bài học & Đưa vào Điểm nóng]
    CheckDropOff -- NO --> StyledNormal[Hiển thị bài giảng bình thường]
    
    HighlightRed --> ClickLesson[Nhấp chọn xem chi tiết Bài học]
    StyledNormal --> ClickLesson
    
    ClickLesson --> CheckStatsSig{D-003: Số học viên >= 30?}
    
    CheckStatsSig -- NO (EF-002) --> ShowLowStats[Hiển thị cảnh báo: Thiếu dữ liệu thống kê]
    
    CheckStatsSig -- YES --> CheckVideo{D-004: Bài học là Video?}
    
    CheckVideo -- NO (EF-003) --> RenderBarChart[Hiển thị Biểu đồ cột hoàn thành bài tập/file]
    CheckVideo -- YES --> RenderTimeline[Hiển thị Biểu đồ dòng thời gian giữ chân học viên]
    
    RenderTimeline --> OpenAI[Mở khu vực Phân tích AI]
    RenderBarChart --> OpenAI
    
    OpenAI --> ShowDisclaimer[Hiển thị Tuyên bố miễn trừ trách nhiệm AI (BR-009)]
    ShowDisclaimer --> RenderInsights[Hiển thị Giả thuyết nguyên nhân & Đề xuất giải pháp]
    
    RenderInsights --> ClickOption{Giáo viên chọn option?}
    
    ClickOption -- "Bấm Đã áp dụng" --> MarkApplied[Ghi nhận áp dụng & Cập nhật mô hình AI]
    ClickOption -- "Bấm Bỏ qua" --> HideOption[Ghi nhận bỏ qua, ẩn gợi ý & Điều chỉnh AI]
    
    MarkApplied --> Success([Hoàn thành Phân tích & Tối ưu hóa])
    HideOption --> Success
```

---

## 12. Story Mapping
| Step | Story |
| :--- | :--- |
| Step 1, 2: Tải Dashboard tổng quan và xem phân phối học viên (Active/Inactive/At-risk) | [US-003](file:///c:/Users/admin/Documents/AI%20for%20vietnam/Agentic%20SDLC/phase_2_story_definition/UserStories.md#us-003-xem-dashboard-tổng-quan-về-khóa-học) |
| Step 3, 4: Xem biểu đồ phễu bài giảng và timeline chi tiết điểm dừng video | [US-004](file:///c:/Users/admin/Documents/AI%20for%20vietnam/Agentic%20SDLC/phase_2_story_definition/UserStories.md#us-004-xem-phân-tích-điểm-dừng-drop-off-point-analysis) |
| Step 5, 6: Xem phân tích AI, đề xuất cải tiến nội dung và thực hiện thao tác Bỏ qua/Áp dụng | [US-005](file:///c:/Users/admin/Documents/AI%20for%20vietnam/Agentic%20SDLC/phase_2_story_definition/UserStories.md#us-005-xem-gợi-ý-nguyên-nhân-từ-ai-và-đề-xuất-cải-thiện) |

---

## 13. UX Improvement Suggestions
* **Chức năng so sánh trước/sau (A/B testing concept)**: Cho phép giáo viên đánh dấu thời điểm họ sửa đổi video trên Udemy, sau đó hệ thống tự động so sánh tỷ lệ drop-off của nhóm học viên học trước và sau ngày sửa đổi.
* **Xuất báo cáo phân tích**: Thêm tính năng tải báo cáo điểm nóng bài học dưới dạng PDF để giảng viên tiện làm việc nhóm hoặc lưu trữ cá nhân.
* **Bộ lọc nâng cao (Filters)**: Cho phép lọc phễu theo nhóm học viên (ví dụ: xem biểu đồ drop-off chỉ đối với nhóm học viên At-risk).

---

## 14. Missing Requirements
* **Lọc theo khoảng thời gian**: Chưa xác định MVP có cần tính năng chọn khoảng thời gian phân tích (ví dụ: xem dữ liệu học trong 30 ngày qua, 90 ngày qua) hay luôn luôn phân tích toàn bộ dữ liệu lịch sử đã nạp. *(Câu hỏi mở từ US-003)*
* **Tự động đồng bộ ngược lên Udemy**: AI gợi ý chia nhỏ bài học hoặc tạo quiz, tuy nhiên hệ thống MVP chưa hỗ trợ đồng bộ các thay đổi này ngược lên Udemy (giảng viên phải vào Udemy Editor để thao tác thủ công). Cần giải thích rõ điều này trong hướng dẫn của đề xuất AI.
