import { DashboardShell } from "@/components/layout/dashboard-shell";
import { AtRiskStudentList } from "@/components/student-intervention/at-risk-student-list";

interface CourseRemindersPageProps {
	params: {
		courseId: string;
	};
}

export default function CourseRemindersPage({ params }: CourseRemindersPageProps) {
	return (
		<DashboardShell>
			<AtRiskStudentList courseId={params.courseId} />
		</DashboardShell>
	);
}
