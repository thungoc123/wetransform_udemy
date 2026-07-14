import {
  AUTH_DEMO_CREDENTIALS,
  AUTH_LOCK_DURATION_MS,
  AUTH_MAX_ATTEMPTS,
  STORAGE_KEYS,
} from "@/lib/constants";
import { setSession } from "@/lib/session";
import { AuthCredentials, AuthResult, LoginAttemptState } from "@/types/auth";

const DEFAULT_ATTEMPT_STATE: LoginAttemptState = {
  failedAttempts: 0,
  lockUntil: null,
};

function delay(ms: number): Promise<void> {
  return new Promise((resolve) => {
    setTimeout(resolve, ms);
  });
}

function readAttemptState(): LoginAttemptState {
  if (typeof window === "undefined") {
    return DEFAULT_ATTEMPT_STATE;
  }

  const raw = window.localStorage.getItem(STORAGE_KEYS.attemptState);
  if (!raw) {
    return DEFAULT_ATTEMPT_STATE;
  }

  try {
    const parsed = JSON.parse(raw) as LoginAttemptState;
    return {
      failedAttempts: parsed.failedAttempts ?? 0,
      lockUntil: parsed.lockUntil ?? null,
    };
  } catch {
    return DEFAULT_ATTEMPT_STATE;
  }
}

function writeAttemptState(next: LoginAttemptState): void {
  if (typeof window === "undefined") {
    return;
  }

  window.localStorage.setItem(STORAGE_KEYS.attemptState, JSON.stringify(next));
}

function clearAttemptState(): void {
  writeAttemptState(DEFAULT_ATTEMPT_STATE);
}

function isLocked(state: LoginAttemptState): boolean {
  return typeof state.lockUntil === "number" && state.lockUntil > Date.now();
}

export async function loginWithMock(credentials: AuthCredentials): Promise<AuthResult> {
  await delay(900);

  if (credentials.email.trim().toLowerCase() === "network@fail.test") {
    return {
      success: false,
      code: "NETWORK_ERROR",
      message: "Unable to connect. Please check your internet connection and retry.",
    };
  }

  const state = readAttemptState();
  if (isLocked(state)) {
    return {
      success: false,
      code: "ACCOUNT_LOCKED",
      message: "Your account is temporarily locked after multiple failed sign-in attempts.",
      lockUntil: state.lockUntil ?? undefined,
    };
  }

  const normalizedEmail = credentials.email.trim().toLowerCase();
  const isValidCredential =
    normalizedEmail === AUTH_DEMO_CREDENTIALS.email &&
    credentials.password === AUTH_DEMO_CREDENTIALS.password;

  if (!isValidCredential) {
    const nextFailedAttempts = state.failedAttempts + 1;

    if (nextFailedAttempts >= AUTH_MAX_ATTEMPTS) {
      const lockUntil = Date.now() + AUTH_LOCK_DURATION_MS;
      writeAttemptState({
        failedAttempts: AUTH_MAX_ATTEMPTS,
        lockUntil,
      });

      return {
        success: false,
        code: "ACCOUNT_LOCKED",
        message: "Your account has been locked for 15 minutes due to repeated failed attempts.",
        lockUntil,
      };
    }

    writeAttemptState({
      failedAttempts: nextFailedAttempts,
      lockUntil: null,
    });

    return {
      success: false,
      code: "INVALID_CREDENTIALS",
      message: "Email or password is incorrect.",
      attemptsRemaining: AUTH_MAX_ATTEMPTS - nextFailedAttempts,
    };
  }

  clearAttemptState();

  const session = {
    token: `mock-token-${Date.now()}`,
    user: {
      id: "teacher-001",
      name: "Course Creator",
      role: "teacher" as const,
      email: AUTH_DEMO_CREDENTIALS.email,
    },
  };

  setSession(session);

  return {
    success: true,
    session,
  };
}