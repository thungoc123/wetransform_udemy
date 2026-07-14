type InsightsPageProps = {
	params: {
		courseId: string;
	};
};

export default function InsightsPage({ params }: InsightsPageProps) {
	return (
		<main className="page-shell">
			<section className="content-card">
				<h1>AI Insights</h1>
				<p>Course ID: {params.courseId}</p>
			</section>
		</main>
	);
}
