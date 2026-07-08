# 📚 References — Prompt Files Index

> Đây là danh mục tổng hợp toàn bộ các prompt mẫu trong thư mục `prompts/`, phục vụ cho các pha khác nhau trong quy trình phát triển Agentic SDLC.

---

## 🛠️ Bộ Prompt Quy trình Phát triển (Core SDLC Prompts)

| Mã | Tên Prompt | File chi tiết | Đầu vào (Input) | Đầu ra (Output) | Vai trò sử dụng |
|---|---|---|---|---|---|
| **P1** | **User Story Generator** | [`prompt_userstories.md`](file:///c:/Users/admin/Documents/AI%20for%20vietnam/Agentic%20SDLC/prompts/prompt_userstories.md) | Requirement thô | `UserStories.md` (12 trường thông tin chi tiết) | Product Owner / BA |
| **P2** | **API Contract Lite** | [`prompt_apispec.md`](file:///c:/Users/admin/Documents/AI%20for%20vietnam/Agentic%20SDLC/prompts/prompt_apispec.md) | User Story + Acceptance Criteria | `APISpec.md` (Bảng contract tối giản) | Tech Lead / BA / Dev |
| **P3** | **Task Breakdown Generator** | [`prompt_breakdown_task.md`](file:///c:/Users/admin/Documents/AI%20for%20vietnam/Agentic%20SDLC/prompts/prompt_breakdown_task.md) | User Stories + API Spec + Domain | `task_breakdown.md` (Các task độc lập kèm DoD) | Tech Lead / PM |
| **P4** | **Task Dependencies Analyzer** | [`prompt_task_dependencies.md`](file:///c:/Users/admin/Documents/AI%20for%20vietnam/Agentic%20SDLC/prompts/prompt_task_dependencies.md) | `task_breakdown.md` | `task_dependencies.md` (Critical Path & Parallel Stages) | Tech Lead / PM |
| **P5** | **GitHub Issue Creator** | [`prompt_createIssue.md`](file:///c:/Users/admin/Documents/AI%20for%20vietnam/Agentic%20SDLC/prompts/prompt_createIssue.md) | `task_breakdown.md` | Hướng dẫn tạo GitHub Issues tự động | PM / AI Engineer |

---
