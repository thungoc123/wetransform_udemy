"use client";

import { useEffect, useMemo, useState } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { formatCountdown } from "@/lib/utils";

interface LoginErrorPanelProps {
  reason?: string;
  message?: string;
  email?: string;
  attemptsRemaining?: string;
  lockUntil?: number | null;
}

export function LoginErrorPanel({
  reason = "UNKNOWN_ERROR",
  message = "Sign-in failed. Please try again.",
  email = "",
  attemptsRemaining,
  lockUntil = null,
}: LoginErrorPanelProps) {
  const router = useRouter();

  const [remainingMs, setRemainingMs] = useState(() =>
    lockUntil ? Math.max(0, lockUntil - Date.now()) : 0,
  );

  const isLocked = reason === "ACCOUNT_LOCKED" && lockUntil && remainingMs > 0;

  useEffect(() => {
    if (!isLocked) {
      return;
    }

    const timer = window.setInterval(() => {
      setRemainingMs(Math.max(0, (lockUntil ?? Date.now()) - Date.now()));
    }, 1000);

    return () => window.clearInterval(timer);
  }, [isLocked, lockUntil]);

  useEffect(() => {
    if (reason === "ACCOUNT_LOCKED" && lockUntil && remainingMs === 0) {
      const query = email ? `?email=${encodeURIComponent(email)}` : "";
      router.replace(`/login${query}`);
    }
  }, [email, lockUntil, reason, remainingMs, router]);

  const subMessage = useMemo(() => {
    if (isLocked) {
      return `Retry available in ${formatCountdown(remainingMs)}.`;
    }

    if (attemptsRemaining) {
      return `Attempts remaining before temporary lock: ${attemptsRemaining}.`;
    }

    return "Review your credentials and try again.";
  }, [attemptsRemaining, isLocked, remainingMs]);

  function onRetry() {
    const query = email ? `?email=${encodeURIComponent(email)}` : "";
    router.replace(`/login${query}`);
  }

  return (
    <div>
      <div className={isLocked ? "alert alert-warning" : "alert alert-error"} role="alert" aria-live="assertive">
        <strong>{message}</strong>
        <div style={{ marginTop: 6 }}>{subMessage}</div>
      </div>

      <Button type="button" variant="secondary" onClick={onRetry} disabled={Boolean(isLocked)}>
        Retry Sign In
      </Button>
    </div>
  );
}
