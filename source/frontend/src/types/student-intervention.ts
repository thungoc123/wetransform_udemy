export type RiskSegment = "at-risk" | "inactive";

export type ReminderDeliveryStatus = "none" | "monitoring" | "sent-error" | "re-engaged";

export interface AtRiskStudentItem {
  studentId: string;
  displayId: string;
  lessonRef: string;
  inactiveDays: number;
  segment: RiskSegment;
  lastSentDaysAgo: number | null;
  deliveryStatus: ReminderDeliveryStatus;
}

export interface ReminderTemplate {
  subject: string;
  body: string;
}

export interface ReminderSendResult {
  status: "success" | "error";
  message: string;
  studentId: string;
}

export interface ReEngagementSummaryData {
  sentCount: number;
  reEngagedCount: number;
  monitoredCount: number;
  students: Array<{
    studentId: string;
    displayId: string;
    status: ReminderDeliveryStatus;
    note: string;
  }>;
}