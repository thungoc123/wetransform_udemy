# Prompt: Dự đoán và lan truyền thay đổi từ Project Context / Project Scope

> **Mục đích:** Xác định xem thay đổi trong Project Context và Project Scope có cần ảnh hưởng đến các tài liệu nghiệp vụ/kỹ thuật khác hay không, đặc biệt là User Stories, API Spec và các User Flow.
> **Người dùng:** BC / Product Owner / Business Analyst
> **Dùng khi:** Có thay đổi trong Project Scope hoặc Project Context và cần quyết định liệu có cần cập nhật các file downstream hay không.

---

## Prompt

```
Bạn là một Senior Business Analyst / Product Analyst. Hãy phân tích sự thay đổi giữa nội dung cũ và mới của 2 file sau:
- phase_1_discovery/BC/project_scope.md
- phase_1_discovery/BC/project_context.md

Nhiệm vụ của bạn là dự đoán xem sự thay đổi này có cần được lan truyền sang các tài liệu liên quan hay không.

## Ngữ cảnh
Các file cần được xem xét là:
- phase_2_story_definition/UserStories.md
- phase_2_story_definition/APISpec.md
- toàn bộ các file trong thư mục phase_3_solution_design/wriframe/userflow/

## Quy tắc quyết định
Hãy đưa ra kết luận theo 2 nhánh sau:

1. Thay đổi
Nếu các cập nhật trong project scope hoặc project context có liên quan đến bất kỳ điều nào sau đây:
- thêm tính năng mới
- thay đổi phạm vi sản phẩm
- thay đổi vai trò người dùng / actor
- thay đổi quy trình nghiệp vụ chính
- thay đổi ràng buộc, dữ liệu, tích hợp, hoặc logic hệ thống
- thay đổi ảnh hưởng trực tiếp đến việc thiết kế User Stories, API, hoặc User Flow

2. Không thay đổi
Nếu các cập nhật chỉ là:
- thay đổi ngôn ngữ, câu chữ, cách diễn đạt
- chỉnh sửa mô tả không ảnh hưởng logic nghiệp vụ
- điều chỉnh quy trình offline hoặc nội dung trình bày mà không tạo ra yêu cầu mới cho hệ thống

## Yêu cầu phân tích
Hãy làm theo các bước sau:
1. So sánh nội dung cũ và mới của project scope và project context.
2. Xác định xem thay đổi có làm thay đổi yêu cầu nghiệp vụ / hệ thống hay không.
3. Nếu là Thay đổi, xác định các file nào cần cập nhật và vì sao.
4. Nếu là Không thay đổi, giải thích rõ vì sao không cần cập nhật.

## Output bắt buộc
Trả về kết quả theo cấu trúc sau:

### 1. Decision
- Thay đổi / Không thay đổi

### 2. Reason
- Giải thích ngắn gọn và rõ ràng về lý do quyết định.

### 3. Impact Level
- Low / Medium / High

### 4. Affected Files
Liệt kê các file cần cập nhật nếu có. Nếu không có, ghi: Không cần cập nhật.
Ví dụ:
- phase_2_story_definition/UserStories.md
- phase_2_story_definition/APISpec.md
- phase_3_solution_design/wriframe/userflow/UF-003_Course_Analytics_Optimization.md
- phase_3_solution_design/wriframe/userflow/UF-004_Student_Intervention.md

### 5. Suggested Update Summary
- Liệt kê 2–5 gợi ý cập nhật cụ thể cho từng file liên quan.

### 6. Confidence
- Điểm tin cậy từ 0 đến 100.

## Quy tắc quan trọng
- Nếu chưa chắc chắn, ưu tiên kết luận là Thay đổi và nêu lý do rõ ràng.
- Chỉ dựa trên thông tin có trong project scope và project context.
- Không thêm suy luận vượt quá phạm vi đầu vào.
- Nếu thay đổi liên quan đến thêm tính năng mới, bắt buộc phải ghi nhận các file downstream cần cập nhật.
```

---

## Input
- Nội dung cũ của project scope:
- Nội dung mới của project scope:
- Nội dung cũ của project context:
- Nội dung mới của project context:

---

## Output mẫu

### 1. Decision
- Thay đổi

### 2. Reason
- Project scope và project context đã thêm bối cảnh mới liên quan đến Online-to-Offline và việc chuyển insight từ học online sang lớp học offline, điều này ảnh hưởng trực tiếp đến phạm vi yêu cầu và luồng nghiệp vụ.

### 3. Impact Level
- High

### 4. Affected Files
- phase_2_story_definition/UserStories.md
- phase_2_story_definition/APISpec.md
- phase_3_solution_design/wriframe/userflow/UF-003_Course_Analytics_Optimization.md
- phase_3_solution_design/wriframe/userflow/UF-004_Student_Intervention.md

### 5. Suggested Update Summary
- Bổ sung user story liên quan đến hỗ trợ chuyển insight sang buổi học offline.
- Cập nhật API spec để phản ánh dữ liệu và hành động phục vụ cho lớp offline.
- Điều chỉnh user flow để thêm bước sử dụng insight cho buổi học offline.

### 6. Confidence
- 95
