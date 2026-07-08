# 📚 PROMPT LIBRARY — Agentic SDLC

> **Mục đích:** Tập hợp các prompt chuẩn cho từng bước trong vòng đời phát triển phần mềm.
> Dùng đúng prompt → AI ra output nhất quán → Team không phải trao đổi lại.

---

## 🗺️ Khi nào dùng prompt nào?

```
Requirement
    │
    ▼
[P1] Tạo User Story          ← BC/Product Owner dùng
    │
    ▼
[P2] Tạo API Contract Lite   ← Tech Lead / BA dùng
    │
    ├──────────────────┐
    ▼                  ▼
[P3] Generate Code    [P4] Generate Unit Test
(AI Backend/Frontend)  (AI Dev)
    │
    ▼
[P5] Code Review             ← AI Reviewer dùng
    │
    ▼
[P6] Debug / RCA             ← AI Dev dùng khi có bug
```

---

## 📋 Danh sách Prompt

| ID | Tên Prompt | Dùng khi nào | File |
|---|---|---|---|
| P1 | **User Story Generator** | Có requirement, cần chia thành User Story | `02_user_story.md` |
| P2 | **API Contract Lite** | Có User Story, cần định nghĩa API trước khi code | `03_api_spec.md` |
| P3 | **Code Generator** | Có API Spec + User Story, cần sinh code | *(sắp có)* |
| P4 | **Unit Test Generator** | Có service/function cần viết test | *(sắp có)* |
| P5 | **Code Reviewer** | Trước khi merge PR | *(sắp có)* |
| P6 | **Debug & RCA** | Có bug/lỗi cần tìm nguyên nhân | *(sắp có)* |

---

## ⚡ Prompt nhanh (Quick Reference)

### P1 — User Story Generator
> **Khi nào dùng:** Nhận được requirement từ khách hàng/PO, cần chuyển thành User Story
> **Input cần chuẩn bị:** Mô tả tính năng (bằng ngôn ngữ tự nhiên)
> **Output nhận được:** Danh sách User Story theo chuẩn `US-XXX`

```
[Dán prompt từ 02_user_story.md vào đây]
Input: [Mô tả requirement của bạn]
```

---

### P2 — API Contract Lite
> **Khi nào dùng:** Sau khi có User Story + Acceptance Criteria, trước khi team bắt đầu code
> **Input cần chuẩn bị:** User Story + Acceptance Criteria
> **Output nhận được:** Bảng API Contract cho từng endpoint

```
[Dán prompt từ 03_api_spec.md vào đây]
Input: [Dán User Story và Acceptance Criteria]
```

---

### P3 — Code Generator *(Draft)*
> **Khi nào dùng:** Có API Contract + Coding Standards, cần AI sinh code
> **Input cần chuẩn bị:** API Contract + Tech Stack + Folder Structure
> **Output nhận được:** Code đúng convention, đúng layer

```
Bạn là AI Backend Engineer của dự án [Tên dự án].

Hãy đọc và tuân thủ:
- Coding Standards: [link BE/codingstandards.md]
- Folder Structure: [link TechLead/project_struture.md]
- Tech Stack: [link TechLead/techstack.md]

Nhiệm vụ: Implement API sau theo đúng layer architecture.

API Contract:
[Dán bảng API Contract từ P2]

Yêu cầu output:
1. Controller: nhận request, validate, gọi service
2. Service: business logic
3. Repository: truy vấn DB
4. DTO: request/response object
5. Không hardcode, không magic number
6. Xử lý exception theo global handler
```

---

### P4 — Unit Test Generator *(Draft)*
> **Khi nào dùng:** Sau khi có code, cần viết test
> **Input cần chuẩn bị:** Code của Service cần test
> **Output nhận được:** Unit test đầy đủ happy path + edge case

```
Bạn là AI QA Engineer của dự án [Tên dự án].

Hãy viết Unit Test cho đoạn code Service sau.

Yêu cầu:
- Test framework: [Jest / JUnit / pytest / ...]
- Coverage: happy path + tất cả edge case trong Acceptance Criteria
- Mock: tất cả dependency (Repository, External Service)
- Tên test phải mô tả rõ scenario: "should_[result]_when_[condition]"
- Không test implementation detail, chỉ test behavior

Service cần test:
[Dán code]

Acceptance Criteria gốc:
[Dán AC từ User Story]
```

---

### P5 — Code Reviewer *(Draft)*
> **Khi nào dùng:** Trước khi tạo PR / merge code
> **Input cần chuẩn bị:** Code diff hoặc file cần review
> **Output nhận được:** Danh sách issues theo mức độ

```
Bạn là Senior AI Code Reviewer của dự án [Tên dự án].

Hãy review đoạn code sau và phân loại issues theo 3 mức:
- 🔴 BLOCKER: Phải fix trước khi merge (security, logic sai, crash)
- 🟡 MAJOR: Nên fix (performance, maintainability)
- 🟢 MINOR: Gợi ý cải thiện (naming, style)

Tiêu chí review dựa trên:
- Coding Standards: [link BE/codingstandards.md]
- Security Rules: [link DevOps/securityrules.md]
- AI Working Rules (Forbidden list): [link AIContext/aiworkingrules.md]

Code cần review:
[Dán code]
```

---

### P6 — Debug & Root Cause Analysis *(Draft)*
> **Khi nào dùng:** Có bug hoặc behavior không như mong đợi
> **Input cần chuẩn bị:** Error message + relevant code + expected behavior
> **Output nhận được:** Root cause + fix suggestion

```
Bạn là AI Senior Engineer của dự án [Tên dự án].

Tôi đang gặp bug sau, hãy phân tích root cause và đề xuất fix.

Môi trường:
- Tech Stack: [...]
- Env: [Local / Dev / UAT / Prod]

Bug description:
- Expected: [Mô tả hành vi mong đợi]
- Actual: [Mô tả hành vi thực tế]

Error log:
[Dán error / stack trace]

Relevant code:
[Dán code liên quan]

Yêu cầu output:
1. Root Cause (giải thích ngắn gọn)
2. Fix đề xuất (code cụ thể)
3. Cách verify fix đúng
4. Có cần update unit test không?
```

---

## 📌 Quy tắc khi thêm Prompt mới

1. **Đặt ID** theo thứ tự: P7, P8...
2. **Mô tả rõ** `Khi nào dùng`, `Input`, `Output`
3. **Thêm vào bảng** Danh sách Prompt ở đầu file
4. **Không xóa** prompt cũ dù đã lỗi thời → đánh dấu `[DEPRECATED]`
5. **Test prompt** với ít nhất 1 example thực tế trước khi add vào library

---

*Cập nhật: 2026-07-08 | Owner: Tech Lead / AI Lead*
