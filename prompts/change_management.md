# 🔄 Quy trình Quản trị Sự thay đổi (Change Management Workflow)

Để đảm bảo hệ thống và AI luôn hoạt động trên thông tin nhất quán, mọi thay đổi (yêu cầu, kỹ thuật, tiến độ) phải được cập nhật tuần tự theo quy trình dưới đây.

---

## 🗺️ Luồng lan truyền thay đổi (Change Propagation)

```
       [Thay đổi xuất hiện]
                 │
                 ▼
 ┌───────────────────────────────┐
 │   1. Cập nhật file gốc        │ (PRD, API Spec, Architecture...)
 └───────────────┬───────────────┘
                 │
                 ▼
 ┌───────────────────────────────┐
 │   2. task_breakdown.md        │ (Chạy prompt_breakdown_task.md)
 └───────────────┬───────────────┘
                 │
                 ▼
 ┌───────────────────────────────┐
 │   3. task_dependencies.md     │ (Chạy prompt_task_dependencies.md)
 └───────────────┬───────────────┘
                 │
                 ▼
 ┌───────────────────────────────┐
 │   4. Spec.md (Master Spec)    │ (Cập nhật Task List & Decision Log)
 └───────────────────────────────┘
```

---

## ⏱️ Chi tiết quy trình cho từng loại thay đổi

### 1. Khi thay đổi Yêu cầu / Nghiệp vụ (Requirement Change)
*Ví dụ: Khách hàng yêu cầu thêm tính năng OTP khi đăng nhập.*

1. **Cập nhật Tài liệu gốc (Pha 1 & 2):**
   - Sửa `phase_1_discovery/BC/product_scope.md` (thêm tính năng vào phạm vi).
   - Chạy prompt sinh User Story mới và cập nhật vào `phase_2_story_definition/UserStories.md`.
   - Chạy prompt sinh API Spec mới và cập nhật vào `phase_2_story_definition/APISpec.md`.
2. **Cập nhật `task_breakdown.md` (Pha 4):**
   - Chạy lại `prompts/prompt_breakdown_task.md` với các file đầu vào mới để sinh ra danh sách task tương ứng cho tính năng OTP.
3. **Cập nhật `task_dependencies.md` (Pha 4):**
   - Chạy lại `prompts/prompt_task_dependencies.md` để xác định task OTP phụ thuộc vào những task nào và có block task nào khác không.
4. **Cập nhật `Spec.md` (Quản trị):**
   - Cập nhật mục **5. Danh sách Task** với các task mới.
   - Ghi nhận quyết định thay đổi này vào mục **10. Decision Log** (Ví dụ: "D-002: Thêm xác thực OTP theo yêu cầu bảo mật").

---

### 2. Khi thay đổi Giải pháp Kỹ thuật / Kiến trúc (Technical Change)
*Ví dụ: Chuyển Database từ PostgreSQL sang MongoDB.*

1. **Cập nhật Tài liệu gốc (Pha 3):**
   - Cập nhật `phase_3_solution_design/TechLead/techstack.md` và `architectureoverview.md`.
   - Cập nhật `phase_3_solution_design/BE/databasestandards.md`.
2. **Cập nhật `task_breakdown.md`:**
   - Cập nhật các task liên quan đến DB setup, migration, repository code để đổi sang dùng MongoDB.
3. **Cập nhật `task_dependencies.md`:**
   - Điều chỉnh lại đồ thị phụ thuộc (Ví dụ: frontend không còn đợi DB schema SQL nữa mà đợi MongoDB model).
4. **Cập nhật `Spec.md`:**
   - Thay đổi thông tin Tech Stack tại mục **2. Tech Stack CỐ ĐỊNH**.
   - Cập nhật mục **10. Decision Log** ghi rõ lý do chuyển đổi DB để tránh tranh cãi sau này.

---

### 3. Khi cập nhật Tiến độ & Phân công (Progress Update)
*Ví dụ: Developer hoàn thành task AUTH-001 và chuẩn bị làm AUTH-002.*

1. **Cập nhật `task_breakdown.md`:**
   - Chuyển trạng thái của task `AUTH-001` sang `DONE`.
2. **Cập nhật `task_dependencies.md`:**
   - Cập nhật đồ thị phụ thuộc: Di chuyển các task được gỡ block (ví dụ: `AUTH-002`) vào mục **Can Start Immediately** (Có thể chạy ngay).
3. **Cập nhật `Spec.md`:**
   - Cập nhật trạng thái trong mục **5. Danh sách Task** để PM/PO theo dõi trực quan tiến độ tổng thể.

---

## 🧠 Nguyên tắc vàng của Agentic SDLC
> "Mọi sự thay đổi không được ghi nhận vào Spec.md, task_breakdown.md, và task_dependencies.md đều được coi là không tồn tại đối với AI."

Khi bạn prompt AI thực hiện code, luôn yêu cầu AI đọc đồng thời 3 file này để đảm bảo AI code đúng task, đúng thứ tự ưu tiên và không vi phạm các ràng buộc nghiệp vụ/kỹ thuật mới nhất.
