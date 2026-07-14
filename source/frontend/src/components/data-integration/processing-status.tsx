"use client";

import { useEffect, useMemo, useState } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { finalizeProcessingMock, PROCESSING_STEPS } from "@/lib/mocks/data-integration.mock";
import { getSession } from "@/lib/session";
import { DataMethod } from "@/types/data-integration";

interface ProcessingStatusProps {
  source: DataMethod;
  scenario: "success" | "warning" | "error";
  fileName?: string;
}

export function ProcessingStatus({ source, scenario, fileName }: ProcessingStatusProps) {
  const router = useRouter();
  const [stepIndex, setStepIndex] = useState(0);

  const progress = useMemo(
    () => Math.round(((stepIndex + 1) / PROCESSING_STEPS.length) * 100),
    [stepIndex],
  );

  useEffect(() => {
    if (!getSession()) {
      router.replace("/login");
      return;
    }

    const timer = window.setInterval(() => {
      setStepIndex((current) => {
        if (current >= PROCESSING_STEPS.length - 1) {
          window.clearInterval(timer);
          return current;
        }
        return current + 1;
      });
    }, 800);

    return () => window.clearInterval(timer);
  }, [router]);

  useEffect(() => {
    if (stepIndex !== PROCESSING_STEPS.length - 1) {
      return;
    }

    let active = true;

    async function completeProcess() {
      const finalResult = await finalizeProcessingMock(source, scenario);
      if (!active) {
        return;
      }

      const params = new URLSearchParams({
        status: finalResult.status,
        source,
        message: finalResult.message,
      });

      if (finalResult.warning) {
        params.set("warning", finalResult.warning);
      }

      router.replace(`/data-integration/result?${params.toString()}`);
    }

    completeProcess();

    return () => {
      active = false;
    };
  }, [router, scenario, source, stepIndex]);

  function onCancel() {
    router.replace("/data-integration");
  }

  return (
    <section>
      <header className="dashboard-header" style={{ marginBottom: 16 }}>
        <div>
          <h1>Processing Status</h1>
          <p className="subtitle" style={{ margin: "6px 0 0" }}>
            Đang xử lý dữ liệu từ {source === "api" ? "kết nối API" : `file ${fileName ?? "upload"}`}.
          </p>
        </div>
      </header>

      <div className="integration-form-card">
        <div className="progress-wrap" aria-live="polite">
          <div className="progress-label">Tiến trình xử lý: {progress}%</div>
          <div className="progress-track" role="progressbar" aria-valuemin={0} aria-valuemax={100} aria-valuenow={progress}>
            <div className="progress-fill" style={{ width: `${progress}%` }} />
          </div>
        </div>

        <ol className="processing-step-list">
          {PROCESSING_STEPS.map((step, index) => (
            <li key={step.id} className={index <= stepIndex ? "active" : ""}>
              {step.label}
            </li>
          ))}
        </ol>

        <div className="integration-form-actions">
          <Button type="button" variant="secondary" onClick={onCancel}>
            Hủy xử lý
          </Button>
        </div>
      </div>
    </section>
  );
}
