# User Flow: UF-002 - Data Integration & Ingestion (Kết nối & Nạp dữ liệu)

Tài liệu này đặc tả chi tiết luồng nạp dữ liệu tiến trình học tập của học viên từ Udemy vào hệ thống (thông qua API hoặc tải lên File).

---

## 1. Flow Overview
* **Flow ID**: UF-002
* **Flow Name**: Data Integration & Ingestion (Kết nối & Nạp dữ liệu)
* **Description**: Cho phép giảng viên kết nối tài khoản Udemy của họ thông qua Udemy API hoặc tải lên tệp xuất dữ liệu Udemy (CSV/XLSX) để hệ thống tiến hành phân tích hành vi học viên.
* **Primary Actor**: Teacher / Course Creator (Giảng viên / Người tạo khóa học)
* **User Goal**: Tải lên dữ liệu học tập thành công và kích hoạt quá trình phân tích dữ liệu của AI.
* **Related User Stories**: [US-002: Kết nối hoặc tải lên dữ liệu Udemy](file:///c:/Users/admin/Documents/AI%20for%20vietnam/Agentic%20SDLC/phase_2_story_definition/UserStories.md#us-002-kết-nối-hoặc-tải-lên-dữ-liệu-udemy)

---

## 2. Entry Points
* Nút CTA "Kết nối dữ liệu Udemy lần đầu" tại màn hình Dashboard trống (đối với tài khoản mới).
* Mục "Quản lý nguồn dữ liệu" (Data Source Management) trong Menu cài đặt tài khoản của giảng viên.

---

## 3. Preconditions
* Giảng viên đã đăng nhập thành công vào hệ thống (Hoàn thành [UF-001](file:///c:/Users/admin/Documents/AI%20for%20vietnam/Agentic%20SDLC/phase_3_solution_design/wriframe/userflow/UF-001_Authentication.md)).
* Đối với luồng API: Giảng viên đã có sẵn API Credentials (Client ID, API Key) từ Udemy.
* Đối với luồng File: Giảng viên đã tải xuống tệp báo cáo xuất bản chính thức từ Udemy dưới định dạng CSV hoặc XLSX.

---

## 4. Happy Path
Luồng nạp dữ liệu bao gồm 2 phương thức song song. Dưới đây là Happy Path cho từng phương thức:

### Nhánh A: Kết nối thông qua API Udemy
| Step | Actor | Action | System Response | Related Story |
| :---: | :---: | :---: | :---: | :---: |
| 1 | Giảng viên | Truy cập màn hình "Quản lý nguồn dữ liệu" và chọn tab "Kết nối API Udemy" | Hiển thị Form cấu hình kết nối API gồm các trường: Client ID, Client Secret/API Key, và nút "Kết nối & Đồng bộ". | [US-002](file:///c:/Users/admin/Documents/AI%20for%20vietnam/Agentic%20SDLC/phase_2_story_definition/UserStories.md#us-002-kết-nối-hoặc-tải-lên-dữ-liệu-udemy) |
| 2 | Giảng viên | Nhập đầy đủ thông tin API credentials và nhấn "Kết nối & Đồng bộ" | 1. Hiển thị trạng thái "Đang kiểm tra kết nối...".<br>2. Gửi request xác thực tới Udemy API.<br>3. Nhận phản hồi thành công từ Udemy. | [US-002](file:///c:/Users/admin/Documents/AI%20for%20vietnam/Agentic%20SDLC/phase_2_story_definition/UserStories.md#us-002-kết-nối-hoặc-tải-lên-dữ-liệu-udemy) |
| 3 | Hệ thống | Tự động đồng bộ và xử lý dữ liệu học tập | 1. Tải về danh sách khóa học, bài học và logs tiến trình học tập.<br>2. Áp dụng BR-004 (Ẩn danh hóa email học viên).<br>3. Lưu vào cơ sở dữ liệu hệ thống.<br>4. Chuyển trạng thái kết nối thành "Đã kết nối".<br>5. Chuyển hướng về Dashboard và hiển thị tiến trình phân tích. | [US-002](file:///c:/Users/admin/Documents/AI%20for%20vietnam/Agentic%20SDLC/phase_2_story_definition/UserStories.md#us-002-kết-nối-hoặc-tải-lên-dữ-liệu-udemy) |

### Nhánh B: Tải lên Tệp dữ liệu Udemy (File Upload)
| Step | Actor | Action | System Response | Related Story |
| :---: | :---: | :---: | :---: | :---: |
| 1 | Giảng viên | Truy cập màn hình "Tải lên dữ liệu" và chọn tab "Tải lên File" | Hiển thị vùng kéo thả file (drag & drop zone) hỗ trợ định dạng `.csv`, `.xlsx` kèm nút "Chọn tệp". | [US-002](file:///c:/Users/admin/Documents/AI%20for%20vietnam/Agentic%20SDLC/phase_2_story_definition/UserStories.md#us-002-kết-nối-hoặc-tải-lên-dữ-liệu-udemy) |
| 2 | Giảng viên | Kéo thả hoặc chọn tệp báo cáo Udemy hợp lệ, sau đó nhấn "Tải lên & Phân tích" | 1. Hiển thị thanh tiến trình upload file (0-100%).<br>2. Hệ thống kiểm tra cấu trúc và tính toàn vẹn của tệp dữ liệu. | [US-002](file:///c:/Users/admin/Documents/AI%20for%20vietnam/Agentic%20SDLC/phase_2_story_definition/UserStories.md#us-002-kết-nối-hoặc-tải-lên-dữ-liệu-udemy) |
| 3 | Hệ thống | Phân tích và lưu trữ dữ liệu học tập | 1. Đọc và parse dữ liệu tệp.<br>2. Áp dụng BR-004 (Ẩn danh hóa email học viên).<br>3. Lưu trữ dữ liệu khóa học vào hệ thống.<br>4. Hiển thị thông báo "Tải lên thành công" và tự động chuyển hướng về trang Dashboard tổng quan. | [US-002](file:///c:/Users/admin/Documents/AI%20for%20vietnam/Agentic%20SDLC/phase_2_story_definition/UserStories.md#us-002-kết-nối-hoặc-tải-lên-dữ-liệu-udemy) |

---

## 5. Decision Points
### D-001: Thông tin kết nối API có đúng không?
* **YES**: Kết nối thành công, tiến hành đồng bộ dữ liệu.
* **NO**: Chuyển tới **Exception Flow: Lỗi kết nối API Udemy** (Hiển thị thông báo lỗi chi tiết).

### D-002: Tệp tải lên có đúng cấu trúc Udemy yêu cầu không?
* **YES**: Tiến hành kiểm tra giới hạn dữ liệu.
* **NO**: Chuyển tới **Exception Flow: Sai cấu trúc tệp tải lên** (Từ chối file và hiển thị lỗi cụ thể).

### D-003: Dữ liệu tải lên/API có vượt quá giới hạn MVP (3 khóa học, 2.600 học viên) không?
* **YES**: Chuyển tới **Exception Flow: Vượt quá giới hạn MVP**.
* **NO**: Tiến hành xử lý ẩn danh hóa PII và lưu trữ dữ liệu thành công.

---

## 6. Alternative Flows
*(Không có luồng thay thế đặc thù nào khác ngoài hai nhánh tích hợp chính nêu ở mục Happy Path).*

---

## 7. Exception Flows
### EF-001: Lỗi kết nối API Udemy (Sai credentials hoặc Timeout/Rate limit)
* **Mô tả**: Thông tin API key nhập sai hoặc server Udemy không phản hồi.
* **Các bước thực hiện**:
  1. Giảng viên điền API Credentials và nhấn "Kết nối".
  2. Hệ thống kiểm tra kết nối với API Udemy và gặp lỗi (ví dụ: HTTP 401 Unauthorized hoặc HTTP 429 Too Many Requests).
  3. Hệ thống hiển thị thông báo lỗi tương ứng:
     * *Nếu sai thông tin*: *"Kết nối thất bại. Vui lòng kiểm tra lại Client ID hoặc API Key của bạn."*
     * *Nếu bị giới hạn Rate limit hoặc Timeout*: *"Hệ thống Udemy đang bận hoặc quá tải. Vui lòng thử lại sau ít phút."*
  4. Trạng thái kết nối giữ nguyên là "Chưa kết nối" để người dùng chỉnh sửa thông tin.

### EF-002: Sai cấu trúc tệp tải lên (Sai định dạng, thiếu cột)
* **Mô tả**: Tệp upload không phải định dạng CSV/XLSX, hoặc thiếu các cột dữ liệu bắt buộc của Udemy.
* **Các bước thực hiện**:
  1. Giảng viên tải lên một tệp Excel tùy biến (không phải file kết quả xuất chuẩn từ Udemy).
  2. Hệ thống kiểm tra cấu trúc dòng/cột và phát hiện thiếu các trường bắt buộc (ví dụ: thiếu cột `User ID`, `Lesson Completed`, hoặc `Timestamp`).
  3. Hệ thống hủy quá trình import và hiển thị thông báo lỗi: *"Tải lên thất bại. Tệp không đúng cấu trúc xuất chuẩn của Udemy. Thiếu các cột bắt buộc: [Tên_cột_lỗi]. Vui lòng tải lại tệp chuẩn."*
  4. Trả giao diện về trạng thái chờ chọn tệp.

### EF-003: Vượt quá giới hạn MVP
* **Mô tả**: Tệp tải lên hoặc dữ liệu API chứa nhiều hơn 3 khóa học hoặc vượt quá 2.600 học viên.
* **Các bước thực hiện**:
  1. Giảng viên tải lên tệp dữ liệu chứa 5 khóa học hoặc tổng số học viên lên tới 4.000 người.
  2. Hệ thống đếm số lượng bản ghi sau khi parse tệp/API.
  3. Hệ thống chặn tiến trình lưu và đưa ra thông báo lỗi: *"Vượt quá giới hạn phiên bản thử nghiệm (MVP). Hệ thống hiện tại chỉ hỗ trợ xử lý tối đa 3 khóa học và 2.600 học viên. Vui lòng lọc bớt dữ liệu trước khi tải lên."*
  4. Trả giao diện về trạng thái ban đầu.

### EF-004: File import chứa dữ liệu không đồng nhất (Edge Case)
* **Mô tả**: Một số học viên có dữ liệu tài khoản nhưng không có log hoạt động học tập.
* **Các bước thực hiện**:
  1. Hệ thống parse file thấy một số học viên bị trống hoàn toàn log hoạt động (activity log).
  2. Hệ thống vẫn tiếp tục nạp dữ liệu của các học viên hợp lệ khác, nhưng ghi nhận những học viên không có log này vào danh sách cảnh báo "Dữ liệu không hoàn chỉnh".
  3. Sau khi import thành công, hiển thị thông báo: *"Đã nạp thành công [X] học viên. Cảnh báo: [Y] học viên không được phân tích do thiếu lịch sử hoạt động."*

---

## 8. Business Rules Applied
* **BR-003 (Định dạng file)**: Hệ thống chỉ chấp nhận định dạng file kết xuất chính thức từ Udemy (CSV/XLSX) và kiểm tra schema nghiêm ngặt. *(Nguồn: US-002)*
* **BR-004 (Ẩn danh hóa PII)**: Tất cả dữ liệu cá nhân nhạy cảm (như địa chỉ email, tên đầy đủ nếu có) của học viên phải được ẩn danh hóa (Anonymized) hoặc băm (Hashed/Encrypted) ngay lập tức khi được import vào hệ thống để tuân thủ quy định bảo mật quyền riêng tư học viên. *(Nguồn: US-002)*
* **BR-005 (Giới hạn MVP)**: Giới hạn hệ thống xử lý tối đa 3 khóa học mẫu và 2.600 học viên hoạt động trong một tài khoản. *(Nguồn: US-002)*

---

## 9. Success State
* Dữ liệu các khóa học, bài học và logs hoạt động được lưu đầy đủ vào Cơ sở dữ liệu.
* Trạng thái nguồn dữ liệu ghi nhận: "Đã đồng bộ thành công ngày [DD/MM/YYYY]".
* Hệ thống tự động kích hoạt background task để xử lý phân tích và hiển thị Dashboard.

---

## 10. Failure State
* Không kết nối được API hoặc File bị từ chối do lỗi cấu trúc/vượt quá giới hạn.
* Cơ sở dữ liệu không lưu trữ bất kỳ bản ghi mới nào bị lỗi.
* Hệ thống hiển thị thông báo lỗi màu đỏ kèm giải pháp khắc phục.

---

## 11. Mermaid User Flow
```mermaid
flowchart TD
    Start([Bắt đầu]) --> AccessSource[Vào màn hình Quản lý nguồn dữ liệu]
    AccessSource --> ChooseMethod{Chọn phương thức nạp?}
    
    %% API Branch
    ChooseMethod -- "API Udemy" --> InputAPI[Nhập Client ID & API Key]
    InputAPI --> ClickConnect[Nhấn Kết nối & Đồng bộ]
    ClickConnect --> ConnectAPI{Kiểm tra kết nối API?}
    ConnectAPI -- NO (EF-001) --> ShowAPIError[Hiển thị lỗi API / Timeout] --> InputAPI
    
    %% File Branch
    ChooseMethod -- "Tải File" --> DragFile[Kéo thả file CSV/XLSX]
    DragFile --> ClickUpload[Nhấn Tải lên & Phân tích]
    ClickUpload --> ValFormat{Kiểm tra định dạng & cấu trúc? (BR-003)}
    ValFormat -- NO (EF-002) --> ShowFileError[Hiển thị lỗi cấu trúc file] --> DragFile
    
    %% Common Processing
    ConnectAPI -- YES --> PullData[Tải dữ liệu từ Udemy]
    ValFormat -- YES --> ParseFile[Đọc và parse dữ liệu file]
    
    PullData --> ValLimit{Vượt giới hạn MVP?\n(Max 3 khóa học, 2600 học viên - BR-005)}
    ParseFile --> ValLimit
    
    ValLimit -- YES (EF-003) --> ShowLimitError[Hiển thị lỗi vượt giới hạn MVP] --> AccessSource
    
    ValLimit -- NO --> CheckLogConsistency{Dữ liệu logs có đồng nhất? (EF-004)}
    CheckLogConsistency -- NO --> LogWarning[Ghi nhận cảnh báo logs trống] --> Anonymize
    CheckLogConsistency -- YES --> Anonymize[Ẩn danh hóa thông tin học viên (BR-004)]
    
    Anonymize --> SaveDB[Lưu vào Cơ sở dữ liệu]
    SaveDB --> TriggerAI[Kích hoạt Background Job phân tích]
    TriggerAI --> RedirectDash[Hiển thị trạng thái Thành công & Chuyển hướng Dashboard]
    RedirectDash --> Success([Nạp dữ liệu Thành công])
```

---

## 12. Story Mapping
| Step | Story |
| :--- | :--- |
| Nhánh A - Step 1, 2: Nhập API key và gửi kết nối | [US-002](file:///c:/Users/admin/Documents/AI%20for%20vietnam/Agentic%20SDLC/phase_2_story_definition/UserStories.md#us-002-kết-nối-hoặc-tải-lên-dữ-liệu-udemy) |
| Nhánh B - Step 1, 2: Tải lên tệp CSV/XLSX | [US-002](file:///c:/Users/admin/Documents/AI%20for%20vietnam/Agentic%20SDLC/phase_2_story_definition/UserStories.md#us-002-kết-nối-hoặc-tải-lên-dữ-liệu-udemy) |
| Xử lý dữ liệu (Ẩn danh hóa PII, kiểm tra giới hạn MVP) | [US-002](file:///c:/Users/admin/Documents/AI%20for%20vietnam/Agentic%20SDLC/phase_2_story_definition/UserStories.md#us-002-kết-nối-hoặc-tải-lên-dữ-liệu-udemy) |

---

## 13. UX Improvement Suggestions
* **Cung cấp File mẫu (Template File)**: Cung cấp link tải xuống file Excel mẫu có đúng cấu trúc cột để giáo viên đối chiếu trước khi import.
* **Đồng bộ tự động theo chu kỳ**: Đối với luồng API, cho phép giảng viên thiết lập lịch đồng bộ tự động (ví dụ: mỗi 24 giờ, mỗi tuần) thay vì chỉ đồng bộ thủ công.
* **Thanh tiến trình phân tích chi tiết**: Sau khi nạp dữ liệu xong, hiển thị cụ thể tiến trình AI đang xử lý (ví dụ: "Đang phân loại học viên..." -> "Đang tính toán tỷ lệ drop-off..." -> "Đang tạo gợi ý AI...").

---

## 14. Missing Requirements
* **Huỷ/Đóng kết nối**: Chưa có User Story mô tả việc giảng viên muốn xóa tệp đã import hoặc ngắt kết nối API Udemy, xóa toàn bộ dữ liệu cũ để import dữ liệu mới.
* **Chi tiết API Udemy**: Cần làm rõ API Udemy của giảng viên có trả về dữ liệu timeline video (retention rate theo giây) hay chỉ trả về trạng thái hoàn thành bài học chung. *(Câu hỏi mở từ US-002)*
