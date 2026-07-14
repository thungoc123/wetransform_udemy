# Decision Log - UF-002 Data Integration Update

| STT | Nội dung cập nhật | Nội dung cũ | Nội dung mới | Người cập nhật | Ngày và giờ |
|---|---|---|---|---|---|
| 1 | Cập nhật phạm vi tích hợp Udemy API trong UF-002 | Mô tả nhánh API ngầm hiểu có thể nạp dữ liệu học tập chi tiết để phân tích | Nhánh API chỉ dùng Udemy API key để lấy danh sách khóa học của giáo viên đang đăng nhập; dữ liệu chi tiết phục vụ phân tích phải nạp qua file CSV/XLSX | GitHub Copilot | 2026-07-14 10:40:49 |
| 2 | Cập nhật Happy Path nhánh A trong UF-002 | Step 3 mô tả tải về danh sách khóa học, bài học và logs tiến trình học tập | Step 3 đổi thành đồng bộ course list, lưu metadata khóa học, hiển thị giới hạn phạm vi API key và gợi ý upload file để nạp dữ liệu chi tiết | GitHub Copilot | 2026-07-14 10:40:49 |
| 3 | Cập nhật Decision Points, Exception Flows, Business Rules và Success State của UF-002 | Logic giới hạn MVP, success state và rule chưa phân biệt rõ giữa nhánh API và nhánh file | Tách rõ giới hạn theo nhánh API/file, thêm rule về phạm vi Udemy API key, success state riêng cho course list và dữ liệu chi tiết | GitHub Copilot | 2026-07-14 10:40:49 |
| 4 | Cập nhật Mermaid User Flow và Missing Requirements của UF-002 | Mermaid thể hiện API branch có thể kéo dữ liệu phân tích đầy đủ; missing requirements còn mở về video timeline qua API | Mermaid đổi sang luồng API chỉ đồng bộ course list; missing requirements đổi sang đặc tả metadata course list và chiến lược refresh định kỳ | GitHub Copilot | 2026-07-14 10:40:49 |
