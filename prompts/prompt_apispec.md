# P2 — API Contract Lite Generator

> **Mục đích:** Chuyển User Story + Acceptance Criteria thành API Contract Lite làm contract giữa các AI Engineer triển khai feature.
> **Người dùng:** Tech Lead / BA
> **Dùng sau:** Khi đã có User Story (P1) và AC đã được confirm

---

## Prompt

```
Dựa trên feature và Acceptance Criteria dưới đây, hãy tạo API Contract Lite để làm contract giữa các AI Engineer triển khai feature.

Yêu cầu:
- Không sinh OpenAPI/Swagger.
- Không mô tả chi tiết schema JSON hay HTTP headers.
- Chỉ tập trung vào thông tin cần thiết để AI hiểu contract và triển khai chính xác.
- Mỗi API trình bày dưới dạng một bảng với các cột:
  - API Name
  - Purpose
  - Endpoint (Method + Path)
  - Actor
  - Input (chỉ liệt kê các field chính, kiểu dữ liệu đơn giản, required/optional)
  - Output (chỉ các field chính)
  - Business Rules
  - Error Cases
  - Related Acceptance Criteria
- Nếu feature cần nhiều API, hãy tạo một bảng cho mỗi API.
- Không suy diễn nghiệp vụ ngoài những gì được cung cấp. Nếu thiếu thông tin, ghi rõ "Assumption Needed".
- Ưu tiên tính rõ ràng và ổn định để AI Backend và AI Frontend có thể triển khai độc lập mà không cần trao đổi thêm.

Input:
- Feature Description: [Mô tả tính năng]
- User Story: [Dán User Story]
- Acceptance Criteria: [Dán AC]
- Business Rules (nếu có): [Dán Business Rules]
```

---

## Hướng dẫn sử dụng

1. Copy toàn bộ nội dung trong block ` ``` ` ở trên
2. Điền thông tin vào 4 phần `Input`
3. Paste vào AI và nhận output
4. Lưu output vào `references/APISpec.md`

---

## Output mẫu

| Field | Nội dung |
|---|---|
| **API Name** | Create Task |
| **Purpose** | Tạo một task mới trong project |
| **Endpoint** | `POST /api/v1/projects/{projectId}/tasks` |
| **Actor** | Project Manager |
| **Input** | `title` (string, required), `description` (string, optional), `estimate` (int, optional, default=0) |
| **Output** | `taskId`, `title`, `status`, `createdAt` |
| **Business Rules** | Chỉ PM được tạo Task. Project phải ở trạng thái Active. |
| **Error Cases** | 400 - Thiếu title \| 403 - Không có quyền \| 404 - Project không tồn tại |
| **Related AC** | AC-01, AC-02, AC-03 |

---

*Owner: Tech Lead | Cập nhật: 2026-07-08*
