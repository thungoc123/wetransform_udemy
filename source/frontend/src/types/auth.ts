export interface AuthCredentials {
  email: string;
  password: string;
}

export type AuthErrorCode =
  | "INVALID_CREDENTIALS"
  | "ACCOUNT_LOCKED"
  | "NETWORK_ERROR"
  | "UNKNOWN_ERROR";

export interface AuthFailure {
  success: false;
  code: AuthErrorCode;
  message: string;
  attemptsRemaining?: number;
  lockUntil?: number;
}

export interface SessionUser {
  id: string;
  name: string;
  role: "teacher";
  email: string;
}

export interface SessionData {
  token: string;
  user: SessionUser;
}

export interface AuthSuccess {
  success: true;
  session: SessionData;
}

export type AuthResult = AuthSuccess | AuthFailure;

export interface LoginAttemptState {
  failedAttempts: number;
  lockUntil: number | null;
}
