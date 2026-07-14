import { DropOffAnalysis } from "@/components/course-analytics/drop-off-analysis";
import { DashboardShell } from "@/components/layout/dashboard-shell";

interface CourseDropOffPageProps {
	params: {
		courseId: string;
	};
}

export default function CourseDropOffPage({ params }: CourseDropOffPageProps) {
	return (
		<DashboardShell>
			<DropOffAnalysis courseId={params.courseId} />
		</DashboardShell>
	);
}
