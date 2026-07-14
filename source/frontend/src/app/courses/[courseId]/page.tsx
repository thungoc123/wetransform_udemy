type CoursePageProps = {
	params: {
		courseId: string;
	};
};

export default function CoursePage({ params }: CoursePageProps) {
	return (
		<main className="page-shell">
			<section className="content-card">
				<h1>Course Overview</h1>
				<p>Course ID: {params.courseId}</p>
			</section>
		</main>
	);
}
