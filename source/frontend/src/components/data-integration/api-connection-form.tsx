"use client";

import { FormEvent, useEffect, useMemo, useRef, useState } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { connectUdemyApiMock } from "@/lib/mocks/data-integration.mock";
import { getSession } from "@/lib/session";

interface ApiFormErrors {
  clientId?: string;
  apiKey?: string;
}

export function ApiConnectionForm() {
  const router = useRouter();
  const clientIdRef = useRef<HTMLInputElement | null>(null);

  const [clientId, setClientId] = useState("");
  const [apiKey, setApiKey] = useState("");
  const [errors, setErrors] = useState<ApiFormErrors>({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [apiMessage, setApiMessage] = useState<string | null>(null);

  useEffect(() => {
    if (!getSession()) {
      router.replace("/login");
      return;
    }

    clientIdRef.current?.focus();
  }, [router]);

  const helper = useMemo(
    () =>
      "Mẹo test: nhập từ khóa invalid, timeout, ratelimit, overlimit hoặc inconsistent trong API Key để mô phỏng trạng thái.",
    [],
  );

  function validate(): ApiFormErrors {
    const next: ApiFormErrors = {};

    if (!clientId.trim()) {
      next.clientId = "Client ID là bắt buộc.";
    }

    if (!apiKey.trim()) {
      next.apiKey = "API Key là bắt buộc.";
    }

    return next;
  }

  async function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    const nextErrors = validate();
    setErrors(nextErrors);
    setApiMessage(null);

    if (Object.keys(nextErrors).length > 0) {
      return;
    }

    setIsSubmitting(true);

    const result = await connectUdemyApiMock({
      clientId,
      apiKey,
    });

    setIsSubmitting(false);

    if (result.ok) {
      const params = new URLSearchParams({
        source: "api",
        scenario: result.scenario,
      });
      router.push(`/data-integration/processing?${params.toString()}`);
      return;
    }

    setApiMessage(result.message);

    const query = new URLSearchParams({
      status: "error",
      source: "api",
      code: result.code,
      message: result.message,
    });

    router.push(`/data-integration/result?${query.toString()}`);
  }

  return (
    <section>
      <header className="dashboard-header" style={{ marginBottom: 16 }}>
        <div>
          <h1>API Connection Form</h1>
          <p className="subtitle" style={{ margin: "6px 0 0" }}>
            Nhập Client ID và API Key để bắt đầu kết nối Udemy.
          </p>
        </div>
      </header>

      {apiMessage ? (
        <div className="alert alert-error" role="alert">
          {apiMessage}
        </div>
      ) : null}

      <form className="integration-form-card" onSubmit={onSubmit} noValidate>
        <div className="form-group">
          <label className="field-label" htmlFor="clientId">
            Client ID
          </label>
          <Input
            ref={clientIdRef}
            id="clientId"
            value={clientId}
            onChange={(event) => setClientId(event.target.value)}
            aria-invalid={Boolean(errors.clientId)}
            disabled={isSubmitting}
          />
          {errors.clientId ? <span className="input-error">{errors.clientId}</span> : null}
        </div>

        <div className="form-group">
          <label className="field-label" htmlFor="apiKey">
            API Key
          </label>
          <Input
            id="apiKey"
            type="password"
            value={apiKey}
            onChange={(event) => setApiKey(event.target.value)}
            aria-invalid={Boolean(errors.apiKey)}
            disabled={isSubmitting}
          />
          {errors.apiKey ? <span className="input-error">{errors.apiKey}</span> : null}
        </div>

        <div className="integration-form-actions">
          <Button type="button" variant="secondary" onClick={() => router.push("/data-integration")}>
            Quay lại
          </Button>
          <Button type="submit" variant="primary" disabled={isSubmitting}>
            {isSubmitting ? "Đang kiểm tra kết nối..." : "Kết nối & Đồng bộ"}
          </Button>
        </div>

        <p className="integration-helper-text">{helper}</p>
      </form>
    </section>
  );
}