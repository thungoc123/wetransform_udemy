# P1 — User Story Generator

> **Mục đích:** Chuyển Requirement thành các User Story phục vụ cho AI-assisted development.
> **Người dùng:** BC / Product Owner
> **Dùng khi:** Nhận được requirement từ khách hàng, cần chia thành User Story

---

## Prompt

```
Dựa trên Requirement đã được thống nhất, hãy chuyển thành các User Story phục vụ cho AI-assisted development.

Nguyên tắc:
- Mỗi User Story chỉ giải quyết một mục tiêu nghiệp vụ.
- Có thể hoàn thành độc lập và triển khai end-to-end.
- Không mô tả giải pháp kỹ thuật.
- Không thiết kế database hoặc API.
- Chỉ mô tả hành vi và kết quả mong muốn.
- Nếu Requirement quá lớn, hãy tự chia thành nhiều User Story nhỏ.
- Nếu thiếu thông tin để hoàn thành User Story, ghi rõ Open Question thay vì tự suy diễn.

Với mỗi User Story, sử dụng cấu trúc sau:

1. Story ID       → Một ID duy nhất (ví dụ: US-001)
2. Title          → Tên ngắn gọn mô tả mục tiêu
3. Business Goal  → User Story này giúp đạt mục tiêu kinh doanh nào?
4. Primary Actor  → Ai thực hiện hành động?
5. Preconditions  → Điều kiện trước khi bắt đầu
6. User Flow      → Liệt kê tuần tự các bước người dùng thực hiện
7. Expected Outcome → Kết quả mong đợi sau khi hoàn thành
8. Acceptance Criteria → Danh sách các tiêu chí nghiệm thu có thể kiểm thử
9. Business Rules → Những quy tắc nghiệp vụ liên quan
10. Edge Cases    → Các tình huống ngoại lệ cần xử lý
11. Dependencies  → User Story hoặc module khác mà story này phụ thuộc
12. Open Questions → Những điểm chưa rõ cần Domain Expert xác nhận

Input:
- Requirement: [Mô tả requirement của bạn bằng ngôn ngữ tự nhiên]
```

---

## Hướng dẫn sử dụng

1. Copy toàn bộ nội dung trong block ` ``` ` ở trên
2. Điền requirement vào phần `Input`
3. Paste vào AI và nhận output
4. Lưu output vào `references/UserStories.md`
5. Dùng output này làm Input cho **P2 — API Contract Lite**

---

## Output mẫu

| Field | Nội dung |
|---|---|
| **Story ID** | US-003 |
| **Title** | User tạo Task mới |
| **Business Goal** | Cho phép PM tạo task để quản lý công việc trong project |
| **Primary Actor** | Project Manager |
| **Preconditions** | Project đang ở trạng thái Active. Người dùng có quyền PM. |
| **User Flow** | 1. Mở Project → 2. Chọn Create Task → 3. Nhập thông tin → 4. Lưu |
| **Expected Outcome** | Task mới được tạo và hiển thị trong danh sách |
| **Acceptance Criteria** | - Task được tạo thành công với dữ liệu hợp lệ<br>- Title là bắt buộc<br>- Estimate mặc định bằng 0 nếu không nhập |
| **Business Rules** | Chỉ PM được tạo Task. Không tạo Task trong Project Archived. |
| **Edge Cases** | Thiếu Title, Project không tồn tại, người dùng không có quyền |
| **Dependencies** | User Authentication, Project Module |
| **Open Questions** | Estimate tối đa là bao nhiêu? Có cho phép tạo Task khi Project ở trạng thái Pending không? |

---

*Owner: BC / Product Owner | Cập nhật: 2026-07-08*
