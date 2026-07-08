# Danh sách User Stories - Nền tảng AI Learning Analytics

Tài liệu này định nghĩa các User Story chi tiết phục vụ cho việc phát triển hệ thống MVP phân tích hành vi học viên Udemy. Các câu chuyện được thiết kế theo cấu trúc nghiệp vụ chuẩn, tập trung vào hành vi và kết quả mong muốn mà không đi sâu vào giải pháp kỹ thuật cụ thể.

---

## Danh sách User Stories

* [US-001: Giáo viên đăng nhập hệ thống](#us-001-giáo-viên-đăng-nhập-hệ-thống)
* [US-002: Kết nối hoặc tải lên dữ liệu Udemy](#us-002-kết-nối-hoặc-tải-lên-dữ-liệu-udemy)
* [US-003: Xem Dashboard tổng quan về khóa học](#us-003-xem-dashboard-tổng-quan-về-khóa-học)
* [US-004: Xem phân tích điểm dừng (Drop-off Point Analysis)](#us-004-xem-phân-tích-điểm-dừng-drop-off-point-analysis)
* [US-005: Xem gợi ý nguyên nhân từ AI và đề xuất cải thiện](#us-005-xem-gợi-ý-nguyên-nhân-từ-ai-và-đề-xuất-cải-thiện)
* [US-006: Gửi nhắc nhở (Reminder) cho học viên bỏ dở sử dụng Best Practice](#us-006-gửi-nhắc-nhở-reminder-cho-học-viên-bỏ-dở-sử-dụng-best-practice)

---

### US-001: Giáo viên đăng nhập hệ thống

| Field | Nội dung |
|---|---|
| **Story ID** | US-001 |
| **Title** | As a Course Creator, I want to log in to the system, so that I can access my course analytics dashboard. |
| **Business Goal** | Bảo mật thông tin khóa học và cá nhân hóa trải nghiệm phân tích dữ liệu cho từng giáo viên. |
| **Primary Actor** | Teacher / Course Creator |
| **Preconditions** | Giáo viên đã được cấp tài khoản hợp lệ trên hệ thống. |
| **User Flow** | 1. Giáo viên truy cập trang đăng nhập.<br>2. Nhập thông tin tài khoản gồm Email và Mật khẩu.<br>3. Nhấp chọn "Đăng nhập". |
| **Expected Outcome** | Giáo viên được xác thực thành công và tự động chuyển hướng tới Dashboard tổng quan khóa học. |
| **Acceptance Criteria** | **Given** giáo viên đang ở trang đăng nhập,<br>**When** giáo viên nhập đúng Email và Mật khẩu rồi chọn "Đăng nhập",<br>**Then** hệ thống đăng nhập thành công và chuyển hướng tới Dashboard tổng quan.<br><br>**Given** giáo viên nhập sai mật khẩu hoặc tài khoản không tồn tại,<br>**When** chọn "Đăng nhập",<br>**Then** hệ thống hiển thị thông báo lỗi "Email hoặc Mật khẩu không chính xác" và giữ nguyên giao diện đăng nhập.<br><br>**Given** trường Email hoặc Mật khẩu đang để trống,<br>**When** chọn "Đăng nhập",<br>**Then** hệ thống hiển thị thông báo yêu cầu nhập đầy đủ thông tin bắt buộc. |
| **Business Rules** | - Mật khẩu phải được mã hóa khi lưu trữ và truyền tải.<br>- Sau 5 lần đăng nhập sai liên tiếp, tài khoản của giáo viên sẽ tạm thời bị khóa trong vòng 15 phút để bảo mật. |
| **Edge Cases** | Mất kết nối internet đột ngột trong lúc gửi thông tin xác thực. |
| **Dependencies** | None |
| **Open Questions** | Hệ thống MVP có tích hợp tính năng đăng nhập một chạm (Single Sign-On - SSO) qua Google hoặc tài khoản Udemy không? |

---

### US-002: Kết nối hoặc tải lên dữ liệu Udemy

| Field | Nội dung |
|---|---|
| **Story ID** | US-002 |
| **Title** | As a Course Creator, I want to connect my Udemy API or upload my Udemy export file, so that the system can analyze my courses' and students' learning activities. |
| **Business Goal** | Thu thập và nạp dữ liệu tiến trình học tập của học viên để làm nguồn phân tích cho AI. |
| **Primary Actor** | Teacher / Course Creator |
| **Preconditions** | Giáo viên đã đăng nhập thành công vào hệ thống. |
| **User Flow** | **Luồng API:**<br>1. Vào màn hình quản lý nguồn dữ liệu.<br>2. Chọn kết nối API Udemy và điền các API Key/Client ID.<br>3. Chọn "Kết nối".<br><br>**Luồng Upload File:**<br>1. Vào màn hình tải lên dữ liệu.<br>2. Chọn kéo thả hoặc chọn tệp dữ liệu dạng CSV/XLSX xuất từ Udemy.<br>3. Chọn "Tải lên & Phân tích". |
| **Expected Outcome** | Dữ liệu về danh sách khóa học, danh sách bài học (lesson/module), và thông tin tiến độ học viên được ghi nhận thành công vào hệ thống. |
| **Acceptance Criteria** | **Given** giáo viên điền đúng thông tin kết nối API,<br>**When** hệ thống kết nối thành công với máy chủ Udemy,<br>**Then** trạng thái kết nối chuyển thành "Đã kết nối" và dữ liệu tự động đồng bộ theo chu kỳ.<br><br>**Given** giáo viên chọn tệp xuất từ Udemy hợp lệ,<br>**When** nhấn tải lên,<br>**Then** hệ thống xử lý tệp, báo "Tải lên thành công" và hiển thị tiến trình phân tích dữ liệu.<br><br>**Given** tệp tải lên bị lỗi cấu trúc, thiếu cột dữ liệu cần thiết hoặc sai định dạng,<br>**When** hệ thống kiểm tra dữ liệu đầu vào,<br>**Then** hệ thống từ chối tải lên và đưa ra thông báo lỗi định dạng dữ liệu chi tiết cho giáo viên. |
| **Business Rules** | - Chỉ chấp nhận các định dạng file dữ liệu xuất bản chính thức từ Udemy.<br>- Dữ liệu cá nhân nhạy cảm của học viên (ví dụ: email) phải được ẩn danh hóa hoặc mã hóa ngay sau khi import để tuân thủ quyền riêng tư.<br>- Giới hạn MVP ban đầu: Tối đa xử lý dữ liệu cho 3 khóa học mẫu và 2.600 học viên. |
| **Edge Cases** | - File import chứa dữ liệu không đồng nhất (ví dụ: một số học viên không có log hoạt động).<br>- Kết nối API với Udemy bị gián đoạn/timeout giữa chừng hoặc gặp giới hạn Rate Limit từ Udemy. |
| **Dependencies** | [US-001: Giáo viên đăng nhập hệ thống](#us-001-giáo-viên-đăng-nhập-hệ-thống) |
| **Open Questions** | Udemy API hiện tại có cung cấp thời gian xem video (video retention) chi tiết từng giây không hay chỉ trả về trạng thái hoàn thành (completed) bài học? |

---

### US-003: Xem Dashboard tổng quan về khóa học

| Field | Nội dung |
|---|---|
| **Story ID** | US-003 |
| **Title** | As a Course Creator, I want to view a dashboard overview of my courses, so that I can quickly assess completion rates, drop-off rates, and student activity status. |
| **Business Goal** | Cung cấp cái nhìn toàn cảnh tức thời về sức khỏe khóa học và mức độ chuyên cần của học viên. |
| **Primary Actor** | Teacher / Course Creator |
| **Preconditions** | Giáo viên đã import dữ liệu thành công của ít nhất một khóa học. |
| **User Flow** | 1. Giáo viên truy cập trang chủ.<br>2. Chọn khóa học cụ thể cần xem từ danh sách khóa học.<br>3. Xem các biểu đồ và chỉ số tổng quan. |
| **Expected Outcome** | Màn hình hiển thị đầy đủ các chỉ số đo lường hiệu suất học tập chính của khóa học. |
| **Acceptance Criteria** | **Given** khóa học đã chọn có dữ liệu hợp lệ,<br>**When** giáo viên tải trang Dashboard,<br>**Then** hệ thống hiển thị chính xác các chỉ số: Tỷ lệ hoàn thành khóa học (Completion Rate), Tỷ lệ bỏ cuộc chung (Drop-off Rate), Số học viên đang hoạt động (Active), Số học viên không hoạt động (Inactive), và Số học viên có nguy cơ bỏ cuộc (At-risk).<br><br>**Given** giáo viên mới và chưa có khóa học nào được kết nối dữ liệu,<br>**When** truy cập Dashboard,<br>**Then** hệ thống hiển thị giao diện trống kèm thông điệp hướng dẫn kết nối dữ liệu Udemy lần đầu. |
| **Business Rules** | - Học viên Active: Có hoạt động học tập ghi nhận trong 7 ngày gần nhất.<br>- Học viên Inactive: Không có hoạt động học tập trong 30 ngày gần nhất.<br>- Học viên At-risk: Không có hoạt động học tập mới từ 14 đến 29 ngày. |
| **Edge Cases** | Dữ liệu khóa học quá lớn (hơn 2.600 học viên) làm chậm tốc độ tải biểu đồ. |
| **Dependencies** | [US-002: Kết nối hoặc tải lên dữ liệu Udemy](#us-002-kết-nối-hoặc-tải-lên-dữ-liệu-udemy) |
| **Open Questions** | MVP có cần cung cấp tính năng lọc dữ liệu theo thời gian (ví dụ: tuần này, tháng này, hoặc khoảng ngày tùy chọn) không? |

---

### US-004: Xem phân tích điểm dừng (Drop-off Point Analysis)

| Field | Nội dung |
|---|---|
| **Story ID** | US-004 |
| **Title** | As a Course Creator, I want to view a detailed drop-off analysis for each lesson and module, so that I can identify exactly where students lose interest or stop learning. |
| **Business Goal** | Xác định chính xác các điểm nghẽn nội dung (lỗ hổng bài giảng) trong khóa học để lập kế hoạch tối ưu. |
| **Primary Actor** | Teacher / Course Creator |
| **Preconditions** | Dữ liệu khóa học đã được phân tích hành vi hoàn thành. |
| **User Flow** | 1. Giáo viên vào trang Dashboard khóa học.<br>2. Chọn xem Tab "Phân tích điểm dừng".<br>3. Xem biểu đồ hình phễu (funnel chart) đại diện cho tiến trình qua từng bài học.<br>4. Nhấp vào bài học có tỷ lệ drop-off cao để xem chi tiết. |
| **Expected Outcome** | Hệ thống hiển thị biểu đồ phân tích trực quan điểm rơi học viên nhiều nhất trong khóa học. |
| **Acceptance Criteria** | **Given** giáo viên xem biểu đồ phễu khóa học,<br>**When** có bài giảng có tỷ lệ drop-off vượt ngưỡng cảnh báo (ví dụ: >20%),<br>**Then** bài học đó phải được tô màu cảnh báo nổi bật (màu đỏ/cam) và đưa vào mục "Điểm nóng cần cải thiện".<br><br>**Given** bài học có cấu trúc video và dữ liệu thời gian xem cụ thể,<br>**When** giáo viên xem chi tiết bài học,<br>**Then** hệ thống hiển thị biểu đồ dòng thời gian thể hiện mốc giây/phút mà học viên bấm dừng video nhiều nhất. |
| **Business Rules** | - Ngưỡng cảnh báo drop-off mặc định là 20% trừ khi được cấu hình lại.<br>- Chỉ áp dụng phân tích drop-off point khi bài học có tối thiểu 30 học viên từng tham gia học để đảm bảo tính chính xác về mặt thống kê. |
| **Edge Cases** | Bài giảng không phải video (ví dụ: tài liệu đọc, bài tập thực hành) sẽ không hiển thị timeline chi tiết mà chỉ hiển thị tỷ lệ hoàn thành/dừng học chung của bài học đó. |
| **Dependencies** | [US-003: Xem Dashboard tổng quan về khóa học](#us-003-xem-dashboard-tổng-quan-về-khóa-học) |
| **Open Questions** | Có cần thiết lập ngưỡng drop-off động tự động thay đổi dựa trên độ dài hoặc độ khó trung bình của bài học không? |

---

### US-005: Xem gợi ý nguyên nhân từ AI và đề xuất cải thiện

| Field | Nội dung |
|---|---|
| **Story ID** | US-005 |
| **Title** | As a Course Creator, I want to receive AI-generated insights on why students dropped off and suggestions to improve the lesson, so that I can make concrete changes to increase course engagement. |
| **Business Goal** | Hỗ trợ giáo viên đưa ra quyết định cải tiến nội dung bài học nhanh chóng bằng cách dịch dữ liệu hành vi thành giải pháp cụ thể. |
| **Primary Actor** | Teacher / Course Creator |
| **Preconditions** | Hệ thống đã phát hiện điểm drop-off bất thường ở một bài giảng cụ thể. |
| **User Flow** | 1. Giáo viên xem chi tiết một bài giảng bị cảnh báo có drop-off cao.<br>2. Nhấp vào khu vực "Phân tích AI".<br>3. Đọc các giả thuyết nguyên nhân và danh sách hành động đề xuất.<br>4. Giáo viên có thể bấm "Đã áp dụng" hoặc "Bỏ qua" cho từng đề xuất. |
| **Expected Outcome** | Hiển thị các giả thuyết nguyên nhân logic kèm hành động cải tiến cụ thể (ví dụ: thêm quiz, chia nhỏ video). |
| **Acceptance Criteria** | **Given** bài học có drop-off cao,<br>**When** giáo viên mở phần phân tích AI,<br>**Then** hệ thống phải hiển thị rõ ràng: (1) Giả thuyết nguyên nhân (ví dụ: video quá dài, bài kiểm tra quá khó) và (2) Đề xuất giải pháp (chia nhỏ bài học thành 3 phần, thêm quiz gợi ý).<br><br>**Given** giáo viên bấm nút "Bỏ qua" một đề xuất,<br>**When** hệ thống ghi nhận,<br>**Then** ẩn đề xuất đó khỏi danh sách hiển thị và điều chỉnh thuật toán AI để tránh lặp lại các gợi ý tương tự trong tương lai. |
| **Business Rules** | - Hệ thống phải hiển thị tuyên bố miễn trừ trách nhiệm: Gợi ý của AI mang tính tham khảo, quyết định cuối cùng thuộc về giáo viên.<br>- Không tạo gợi ý nếu dữ liệu đầu vào của bài học chưa đạt mức tin cậy tối thiểu. |
| **Edge Cases** | AI đưa ra các đề xuất nằm ngoài khả năng kỹ thuật mà nền tảng Udemy hỗ trợ (ví dụ: tự động sửa phụ đề hoặc chèn mini-game). |
| **Dependencies** | [US-004: Xem phân tích điểm dừng (Drop-off Point Analysis)](#us-004-xem-phân-tích-điểm-dừng-drop-off-point-analysis) |
| **Open Questions** | MVP có nên tích hợp hệ thống đánh giá (Like/Dislike hoặc Rating 5 sao) của giáo viên cho từng đề xuất AI để làm dữ liệu training mô hình không? |

---

### US-006: Gửi nhắc nhở (Reminder) cho học viên bỏ dở sử dụng Best Practice

| Field | Nội dung |
|---|---|
| **Story ID** | US-006 |
| **Title** | As a Course Creator, I want to send personalized reminders to at-risk or inactive students using message templates optimized from fast-completing students' best practices, so that I can motivate them to resume learning. |
| **Business Goal** | Tăng tỷ lệ học viên quay lại học (Re-engaged Rate) bằng cách sử dụng các thông điệp truyền cảm hứng được đúc kết từ hành vi của nhóm học viên thành công nhất. |
| **Primary Actor** | Teacher / Course Creator |
| **Preconditions** | Có danh sách học viên ở trạng thái At-risk/Inactive và hệ thống đã đúc kết được best practice của nhóm học viên hoàn thành nhanh. |
| **User Flow** | 1. Giáo viên xem danh sách học viên bỏ dở của bài giảng cụ thể.<br>2. Chọn "Gửi nhắc nhở".<br>3. Hệ thống hiển thị mẫu tin nhắn được soạn thảo tự động dựa trên insight từ các học viên hoàn thành nhanh (Best Practice).<br>4. Giáo viên chỉnh sửa (nếu cần) và bấm nút "Gửi". |
| **Expected Outcome** | Tin nhắn/email nhắc nhở được gửi tới học viên; hệ thống kích hoạt cơ chế theo dõi phản hồi trong 7 ngày. |
| **Acceptance Criteria** | **Given** nhóm học viên mục tiêu đang ở trạng thái At-risk,<br>**When** giáo viên gửi tin nhắn nhắc nhở bằng mẫu Best Practice,<br>**Then** hệ thống tự động cá nhân hóa nội dung (tên học viên, bài học đang dừng, lời khuyên thành công) và gửi đi thành công.<br><br>**Given** tin nhắn đã được gửi đi thành công,<br>**When** học viên mục tiêu quay lại học bài mới trong vòng 7 ngày,<br>**Then** hệ thống ghi nhận trạng thái học viên thành "Re-engaged" và cập nhật tỷ lệ chuyển đổi trên dashboard can thiệp.<br><br>**Given** một học viên vừa nhận tin nhắn nhắc nhở từ hệ thống trong vòng 7 ngày qua,<br>**When** hệ thống hoặc giáo viên cố gắng gửi tin nhắn nhắc nhở tiếp theo,<br>**Then** hệ thống hiển thị thông báo cảnh báo và chặn hành động gửi để tránh spam học viên. |
| **Business Rules** | - Tần suất gửi nhắc nhở tối đa là 1 tin/email cho cùng một học viên trong vòng 7 ngày.<br>- Nội dung Best Practice phải được tạo ra từ việc phân tích thời gian hoàn thành bài học, thứ tự bài học và các ghi chú của nhóm học viên top đầu (hoàn thành nhanh nhất). |
| **Edge Cases** | - Học viên tắt nhận thông báo từ giảng viên hoặc email học viên bị lỗi.<br>- Một học viên rơi vào trạng thái At-risk của nhiều bài giảng cùng một thời điểm. |
| **Dependencies** | [US-002: Kết nối hoặc tải lên dữ liệu Udemy](#us-002-kết-nối-hoặc-tải-lên-dữ-liệu-udemy), [US-003: Xem Dashboard tổng quan về khóa học](#us-003-xem-dashboard-tổng-quan-về-khóa-học) |
| **Open Questions** | Kênh gửi nhắc nhở chính thức của hệ thống là gửi qua hòm thư Udemy (API Udemy Messages) hay gửi thông qua email cá nhân của ứng dụng? |