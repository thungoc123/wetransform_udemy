import { LessonDetail } from "@/components/course-analytics/lesson-detail";
import { DashboardShell } from "@/components/layout/dashboard-shell";

interface LessonDetailPageProps {
  params: {
    courseId: string;
    lessonId: string;
  };
}

export default function LessonDetailPage({ params }: LessonDetailPageProps) {
  return (
    <DashboardShell>
      <LessonDetail courseId={params.courseId} lessonId={params.lessonId} />
    </DashboardShell>
  );
}