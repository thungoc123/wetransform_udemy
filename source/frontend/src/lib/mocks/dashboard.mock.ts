import { DashboardMode, DashboardOverview } from "@/types/dashboard";

function delay(ms: number): Promise<void> {
  return new Promise((resolve) => {
    setTimeout(resolve, ms);
  });
}

export async function getDashboardOverviewMock(mode: DashboardMode): Promise<DashboardOverview> {
  await delay(800);

  if (mode === "error") {
    throw new Error("Failed to load dashboard summary.");
  }

  if (mode === "empty") {
    return {
      metrics: [],
      announcements: [],
    };
  }

  return {
    metrics: [
      {
        id: "total-courses",
        label: "Total Courses",
        value: "12",
        note: "2 new this month",
      },
      {
        id: "active-students",
        label: "Active Students",
        value: "1,842",
        note: "+6.1% from last week",
      },
      {
        id: "completion-rate",
        label: "Completion Rate",
        value: "78%",
        note: "Target: 80%",
      },
    ],
    announcements: [
      "Sync your Udemy data source to refresh latest engagement trends.",
      "Review at-risk learners in Student Intervention module.",
    ],
  };
}