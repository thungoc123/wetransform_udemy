import { LoginErrorPanel } from "@/components/auth/login-error-panel";

interface LoginErrorPageProps {
  searchParams?: {
    reason?: string;
    message?: string;
    email?: string;
    attemptsRemaining?: string;
    lockUntil?: string;
  };
}

export default function LoginErrorPage({ searchParams }: LoginErrorPageProps) {
  const lockUntilRaw = searchParams?.lockUntil;

  return (
    <div className="page-shell">
      <section className="auth-layout">
        <div className="auth-brand-panel">
          <span className="auth-kicker">Authentication Alert</span>
          <h1>Sign-in could not be completed.</h1>
          <p>
            We kept your context to help you retry quickly while preserving account protection rules.
          </p>
        </div>

        <div className="auth-card">
          <h2>Login Error State</h2>
          <p className="subtitle">Review the issue and continue with retry when available.</p>
          <LoginErrorPanel
            reason={searchParams?.reason}
            message={searchParams?.message}
            email={searchParams?.email}
            attemptsRemaining={searchParams?.attemptsRemaining}
            lockUntil={lockUntilRaw ? Number(lockUntilRaw) : null}
          />
        </div>
      </section>
    </div>
  );
}
