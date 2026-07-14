type RemindersPageProps = {
	params: {
		courseId: string;
	};
};

export default function RemindersPage({ params }: RemindersPageProps) {
	return (
		<main className="page-shell">
			<section className="content-card">
				<h1>Student Reminders</h1>
				<p>Course ID: {params.courseId}</p>
			</section>
		</main>
	);
}
