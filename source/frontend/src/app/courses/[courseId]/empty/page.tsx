import { EmptyLowDataState } from "@/components/course-analytics/empty-low-data-state";
import { DashboardShell } from "@/components/layout/dashboard-shell";

interface CourseEmptyPageProps {
  params: {
    courseId: string;
  };
  searchParams?: {
    reason?: string;
  };
}

export default function CourseEmptyPage({ params, searchParams }: CourseEmptyPageProps) {
  const reasonRaw = searchParams?.reason;
  const reason = reasonRaw === "low-data" || reasonRaw === "error" ? reasonRaw : "empty";

  return (
    <DashboardShell>
      <EmptyLowDataState courseId={params.courseId} reason={reason} />
    </DashboardShell>
  );
}
