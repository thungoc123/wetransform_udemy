import { CourseDashboard } from "@/components/course-analytics/course-dashboard";
import { DashboardShell } from "@/components/layout/dashboard-shell";

interface CoursePageProps {
	params: {
		courseId: string;
	};
	searchParams?: {
		state?: string;
	};
}

export default function CourseDetailPage({ params, searchParams }: CoursePageProps) {
	const state =
		searchParams?.state === "empty" || searchParams?.state === "loading-error"
			? searchParams.state
			: "default";

	return (
		<DashboardShell>
			<CourseDashboard courseId={params.courseId} state={state} />
		</DashboardShell>
	);
}
