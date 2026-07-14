import { STORAGE_KEYS } from "@/lib/constants";
import { SessionData } from "@/types/auth";

function isBrowser(): boolean {
  return typeof window !== "undefined";
}

export function getSession(): SessionData | null {
  if (!isBrowser()) {
    return null;
  }

  const raw = window.localStorage.getItem(STORAGE_KEYS.session);
  if (!raw) {
    return null;
  }

  try {
    return JSON.parse(raw) as SessionData;
  } catch {
    return null;
  }
}

export function setSession(session: SessionData): void {
  if (!isBrowser()) {
    return;
  }

  window.localStorage.setItem(STORAGE_KEYS.session, JSON.stringify(session));
}

export function clearSession(): void {
  if (!isBrowser()) {
    return;
  }

  window.localStorage.removeItem(STORAGE_KEYS.session);
}