import { AIInsightPanel } from "@/components/course-analytics/ai-insight-panel";
import { DashboardShell } from "@/components/layout/dashboard-shell";

interface AIInsightPageProps {
  params: {
    courseId: string;
    lessonId: string;
  };
}

export default function AIInsightPage({ params }: AIInsightPageProps) {
  return (
    <DashboardShell>
      <AIInsightPanel courseId={params.courseId} lessonId={params.lessonId} />
    </DashboardShell>
  );
}