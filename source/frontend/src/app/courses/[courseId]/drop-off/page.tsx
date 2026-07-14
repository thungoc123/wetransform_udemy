type DropOffPageProps = {
	params: {
		courseId: string;
	};
};

export default function DropOffPage({ params }: DropOffPageProps) {
	return (
		<main className="page-shell">
			<section className="content-card">
				<h1>Drop-off Analysis</h1>
				<p>Course ID: {params.courseId}</p>
			</section>
		</main>
	);
}
