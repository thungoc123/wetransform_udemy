import { LoginForm } from "@/components/auth/login-form";

interface LoginPageProps {
	searchParams?: {
		email?: string;
	};
}

export default function LoginPage({ searchParams }: LoginPageProps) {
	const initialEmail = searchParams?.email;

	return (
		<div className="page-shell">
			<section className="auth-layout">
				<div className="auth-brand-panel">
					<span className="auth-kicker">AI Learning Analytics</span>
					<h1>Turn course signals into decisions.</h1>
					<p>
						Secure access for teachers and course creators to monitor learning impact, detect risks,
						and optimize outcomes.
					</p>
				</div>

				<div className="auth-card">
					<h2>Sign in</h2>
					<p className="subtitle">Use your teacher account to access the analytics workspace.</p>
					<LoginForm initialEmail={initialEmail} />
				</div>
			</section>
		</div>
	);
}
