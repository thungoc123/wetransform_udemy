import {
  AtRiskStudentItem,
  ReEngagementSummaryData,
  ReminderSendResult,
  ReminderTemplate,
} from "@/types/student-intervention";

function delay(ms: number): Promise<void> {
  return new Promise((resolve) => {
    setTimeout(resolve, ms);
  });
}

const STUDENTS: AtRiskStudentItem[] = [
  {
    studentId: "s-001",
    displayId: "STD-10A2",
    lessonRef: "Lesson 2 - Student Motivation Patterns",
    inactiveDays: 19,
    segment: "at-risk",
    lastSentDaysAgo: null,
    deliveryStatus: "none",
  },
  {
    studentId: "s-002",
    displayId: "STD-22B9",
    lessonRef: "Lesson 3 - Practice Worksheet",
    inactiveDays: 33,
    segment: "inactive",
    lastSentDaysAgo: 3,
    deliveryStatus: "monitoring",
  },
  {
    studentId: "s-003",
    displayId: "STD-41C7",
    lessonRef: "Lesson 4 - Capstone Demo",
    inactiveDays: 24,
    segment: "at-risk",
    lastSentDaysAgo: 9,
    deliveryStatus: "monitoring",
  },
  {
    studentId: "s-004",
    displayId: "STD-55D5",
    lessonRef: "Lesson 1 - Intro To Learning Signals",
    inactiveDays: 42,
    segment: "inactive",
    lastSentDaysAgo: null,
    deliveryStatus: "none",
  },
];

export async function getAtRiskStudentListMock(): Promise<AtRiskStudentItem[]> {
  await delay(500);
  return STUDENTS;
}

export async function getReminderTemplateMock(student: AtRiskStudentItem): Promise<ReminderTemplate> {
  await delay(350);

  return {
    subject: `Gentle reminder for ${student.displayId}`,
    body:
      `Hi ${student.displayId},\n\n` +
      `We noticed you paused at \"${student.lessonRef}\". ` +
      "Best-practice learners completed this lesson by splitting study into 15-minute sessions and reviewing one key example before moving on.\n\n" +
      "Would you like to rejoin this week? We are here to support your progress.",
  };
}

export async function sendReminderMock(studentId: string, body: string): Promise<ReminderSendResult> {
  await delay(650);

  if (!body.trim()) {
    return {
      status: "error",
      message: "Nội dung nhắc nhở không được để trống.",
      studentId,
    };
  }

  if (body.toLowerCase().includes("unsubscribe") || studentId === "s-004") {
    return {
      status: "error",
      message: "Không thể gửi tin nhắn do học viên đã từ chối nhận thông báo hoặc email không khả dụng.",
      studentId,
    };
  }

  return {
    status: "success",
    message: "Đã gửi nhắc nhở thành công. Bắt đầu theo dõi phản hồi trong 7 ngày.",
    studentId,
  };
}

export async function getReEngagementSummaryMock(): Promise<ReEngagementSummaryData> {
  await delay(500);

  return {
    sentCount: 12,
    reEngagedCount: 5,
    monitoredCount: 7,
    students: [
      {
        studentId: "s-001",
        displayId: "STD-10A2",
        status: "re-engaged",
        note: "Returned to lesson activity in day 3.",
      },
      {
        studentId: "s-003",
        displayId: "STD-41C7",
        status: "monitoring",
        note: "No new activity yet, monitoring still active.",
      },
      {
        studentId: "s-002",
        displayId: "STD-22B9",
        status: "sent-error",
        note: "Delivery bounced in previous campaign.",
      },
    ],
  };
}
