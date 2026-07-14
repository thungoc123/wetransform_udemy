"use client";

import { FormEvent, useEffect, useMemo, useRef, useState } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { AUTH_DEMO_CREDENTIALS } from "@/lib/constants";
import { loginWithMock } from "@/lib/mocks/auth.mock";
import { getSession } from "@/lib/session";

interface FieldErrors {
  email?: string;
  password?: string;
}

interface LoginFormProps {
  initialEmail?: string;
}

export function LoginForm({ initialEmail }: LoginFormProps) {
  const router = useRouter();
  const emailRef = useRef<HTMLInputElement | null>(null);

  const [email, setEmail] = useState(initialEmail ?? AUTH_DEMO_CREDENTIALS.email);
  const [password, setPassword] = useState(AUTH_DEMO_CREDENTIALS.password);
  const [fieldErrors, setFieldErrors] = useState<FieldErrors>({});
  const [networkError, setNetworkError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    const existingSession = getSession();
    if (existingSession) {
      router.replace("/dashboard");
      return;
    }

    emailRef.current?.focus();
  }, [router]);

  const helperText = useMemo(
    () =>
      `Demo credentials: ${AUTH_DEMO_CREDENTIALS.email} / ${AUTH_DEMO_CREDENTIALS.password}`,
    [],
  );

  function validate(): FieldErrors {
    const nextErrors: FieldErrors = {};

    if (!email.trim()) {
      nextErrors.email = "Email is required.";
    }

    if (!password.trim()) {
      nextErrors.password = "Password is required.";
    }

    return nextErrors;
  }

  async function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    const nextErrors = validate();
    setFieldErrors(nextErrors);
    setNetworkError(null);

    if (Object.keys(nextErrors).length > 0) {
      return;
    }

    setIsSubmitting(true);

    const result = await loginWithMock({
      email,
      password,
    });

    setIsSubmitting(false);

    if (result.success) {
      router.replace("/dashboard");
      return;
    }

    if (result.code === "NETWORK_ERROR") {
      setNetworkError(result.message);
      return;
    }

    const params = new URLSearchParams({
      reason: result.code,
      message: result.message,
      email: email.trim(),
    });

    if (typeof result.lockUntil === "number") {
      params.set("lockUntil", String(result.lockUntil));
    }

    if (typeof result.attemptsRemaining === "number") {
      params.set("attemptsRemaining", String(result.attemptsRemaining));
    }

    router.replace(`/login/error?${params.toString()}`);
  }

  return (
    <form onSubmit={onSubmit} noValidate>
      {networkError ? (
        <div className="alert alert-error" role="alert">
          {networkError}
        </div>
      ) : null}

      <div className="form-group">
        <label className="field-label" htmlFor="email">
          Email
        </label>
        <Input
          ref={emailRef}
          id="email"
          type="email"
          autoComplete="email"
          value={email}
          onChange={(event) => setEmail(event.target.value)}
          aria-invalid={Boolean(fieldErrors.email)}
          disabled={isSubmitting}
        />
        {fieldErrors.email ? <span className="input-error">{fieldErrors.email}</span> : null}
      </div>

      <div className="form-group">
        <label className="field-label" htmlFor="password">
          Password
        </label>
        <Input
          id="password"
          type="password"
          autoComplete="current-password"
          value={password}
          onChange={(event) => setPassword(event.target.value)}
          aria-invalid={Boolean(fieldErrors.password)}
          disabled={isSubmitting}
        />
        {fieldErrors.password ? <span className="input-error">{fieldErrors.password}</span> : null}
      </div>

      <Button type="submit" variant="primary" disabled={isSubmitting} aria-disabled={isSubmitting}>
        {isSubmitting ? "Signing in..." : "Sign In"}
      </Button>

      <p className="subtitle" style={{ marginBottom: 0, marginTop: 12, fontSize: 13 }}>
        {helperText}
      </p>
    </form>
  );
}
