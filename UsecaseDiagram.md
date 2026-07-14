# Use Case Diagram - AI Learning Analytics MVP

```mermaid
usecaseDiagram
    actor Teacher as "Teacher / Course Creator"
    actor Offline as "Offline Instructor"
    actor Student as "Student"
    actor Udemy as "Udemy API"
    actor OpenAI as "OpenAI API"
    actor Mail as "Email Gateway (SendGrid / SMTP)"
    actor Admin as "System Admin / Operator"

    rectangle "AI Learning Analytics Platform MVP" {
        (UC01 Login)
        (UC02 Connect Udemy API)
        (UC03 Upload Udemy Export File)
        (UC04 View Course Dashboard)
        (UC05 View Drop-off Analysis)
        (UC06 View AI Insights)
        (UC07 Apply/Ignore Recommendations)
        (UC08 View At-risk Students)
        (UC09 Preview Personalized Reminder)
        (UC10 Confirm and Send Reminder)
        (UC11 Track Re-engagement)
        (UC12 View O2O Insights)
        (UC13 Adjust Offline Lesson Plan)
        (UC14 Monitor System Health)
        (UC15 Review Audit Logs)
        (UC16 Handle Security Incident)
        (UC17 Run Backup)
    }

    Teacher --> (UC01 Login)
    Teacher --> (UC02 Connect Udemy API)
    Teacher --> (UC03 Upload Udemy Export File)
    Teacher --> (UC04 View Course Dashboard)
    Teacher --> (UC05 View Drop-off Analysis)
    Teacher --> (UC06 View AI Insights)
    Teacher --> (UC07 Apply/Ignore Recommendations)
    Teacher --> (UC08 View At-risk Students)
    Teacher --> (UC09 Preview Personalized Reminder)
    Teacher --> (UC10 Confirm and Send Reminder)

    Offline --> (UC12 View O2O Insights)
    Offline --> (UC13 Adjust Offline Lesson Plan)

    Admin --> (UC14 Monitor System Health)
    Admin --> (UC15 Review Audit Logs)
    Admin --> (UC16 Handle Security Incident)
    Admin --> (UC17 Run Backup)

    Udemy --> (UC02 Connect Udemy API)
    Udemy --> (UC04 View Course Dashboard)
    Udemy --> (UC05 View Drop-off Analysis)
    Udemy --> (UC11 Track Re-engagement)

    OpenAI --> (UC06 View AI Insights)
    Mail --> (UC10 Confirm and Send Reminder)
    Student --> (UC11 Track Re-engagement)

    (UC04 View Course Dashboard) .> (UC01 Login) : <<include>>
    (UC05 View Drop-off Analysis) .> (UC04 View Course Dashboard) : <<include>>
    (UC06 View AI Insights) .> (UC05 View Drop-off Analysis) : <<include>>
    (UC07 Apply/Ignore Recommendations) .> (UC06 View AI Insights) : <<extend>>
    (UC09 Preview Personalized Reminder) .> (UC08 View At-risk Students) : <<include>>
    (UC10 Confirm and Send Reminder) .> (UC09 Preview Personalized Reminder) : <<include>>
    (UC11 Track Re-engagement) .> (UC10 Confirm and Send Reminder) : <<extend>>
    (UC13 Adjust Offline Lesson Plan) .> (UC12 View O2O Insights) : <<include>>
```
