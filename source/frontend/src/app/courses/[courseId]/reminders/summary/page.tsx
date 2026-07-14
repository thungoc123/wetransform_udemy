import { DashboardShell } from "@/components/layout/dashboard-shell";
import { ReEngagementSummary } from "@/components/student-intervention/re-engagement-summary";

interface ReminderSummaryPageProps {
  params: {
    courseId: string;
  };
}

export default function ReminderSummaryPage({ params }: ReminderSummaryPageProps) {
  return (
    <DashboardShell>
      <ReEngagementSummary courseId={params.courseId} />
    </DashboardShell>
  );
}