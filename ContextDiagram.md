flowchart LR
    %% External Actors
    T[Teacher / Course Creator]
    OI[Offline Instructor]
    ST[Student]
    UA[Udemy Instructor API]
    UF[Udemy Export File CSV/XLSX]
    OAI[OpenAI API]
    EM[Email Gateway<br/>SendGrid / SMTP]
    ADM[System Admin / Operator]
    CICD[GitHub Actions + Secrets]
    BK["PostgreSQL Backup Store<br/>pg_dump files"]

    %% System Boundary
    subgraph SYS["AI Learning Analytics Platform MVP"]
        APP["Web + API Application<br/>Authentication, Data Import, Analytics,<br/>AI Insights, Intervention"]
    end

    T -->|Login, connect Udemy, upload data<br/>View dashboard<br/>Approve/ignore recommendations<br/>Send reminders| APP
    OI -->|View O2O insights<br/>Adjust offline lesson plan| APP
    APP -->|Dashboard insights<br/>Drop-off analysis<br/>Action recommendations| T
    APP -->|Offline intervention suggestions| OI

    APP -->|Personalized reminder content| EM
    EM -->|Email reminder delivery| ST
    ST -->|Learning re-engagement behavior| UA

    UA <-->|Course, lesson, student activity sync| APP
    UF -->|Manual data import| APP
    APP <-->|Generate hypotheses and recommendations| OAI

    ADM <-->|Monitoring<br/>Audit review<br/>Security policy<br/>Incident handling| APP
    CICD -->|Build, deploy, inject runtime secrets| APP
    APP -->|Scheduled database backups| BK

    classDef center fill:#0b5d4b,stroke:#08382d,color:#ffffff,stroke-width:2px;
    classDef ext fill:#e7f7f3,stroke:#2f7a68,color:#12352d;

    class APP center;
    class T,OI,ST,UA,UF,OAI,EM,ADM,CICD,BK ext;
