import Link from "next/link";

export default function HomePage() {
	return (
		<main className="page-shell">
			<section className="hero-card">
				<p className="eyebrow">AI Learning Analytics MVP</p>
				<h1>Frontend is configured and ready to run.</h1>
				<p>
					Use the links below to verify the routed screens while the UI is being
					implemented.
				</p>
				<div className="link-list">
					<Link href="/login">Login</Link>
					<Link href="/dashboard">Dashboard</Link>
					<Link href="/courses/demo-course/drop-off">Drop-off Analysis</Link>
					<Link href="/courses/demo-course/insights">AI Insights</Link>
					<Link href="/courses/demo-course/reminders">Reminders</Link>
				</div>
			</section>
		</main>
	);
}
