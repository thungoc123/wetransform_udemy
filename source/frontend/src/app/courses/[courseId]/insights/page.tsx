interface CourseInsightsPageProps {
	params: {
		courseId: string;
	};
}

export default function CourseInsightsPage({ params }: CourseInsightsPageProps) {
	return <div className="page-shell">Insights placeholder for course {params.courseId}</div>;
}
