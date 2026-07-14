"use client";

import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { DataMethod } from "@/types/data-integration";

interface IntegrationResultProps {
  status: "success" | "error";
  source: DataMethod;
  message: string;
  warning?: string;
}

export function IntegrationResult({ status, source, message, warning }: IntegrationResultProps) {
  const router = useRouter();

  const retryRoute = source === "api" ? "/data-integration/api" : "/data-integration/upload";

  return (
    <section>
      <header className="dashboard-header" style={{ marginBottom: 16 }}>
        <div>
          <h1>Success / Error Feedback</h1>
          <p className="subtitle" style={{ margin: "6px 0 0" }}>
            Kết quả cuối cùng của quá trình import dữ liệu.
          </p>
        </div>
      </header>

      <div className="integration-result-card">
        <div className={status === "success" ? "result-icon success" : "result-icon error"} aria-hidden="true">
          {status === "success" ? "✓" : "!"}
        </div>

        <h2>{status === "success" ? "Import thành công" : "Import thất bại"}</h2>
        <p>{message}</p>

        {warning ? (
          <div className="alert alert-warning" role="status" style={{ marginBottom: 16 }}>
            {warning}
          </div>
        ) : null}

        <div className="integration-form-actions">
          {status === "success" ? (
            <Button type="button" variant="primary" onClick={() => router.push("/dashboard")}>
              Quay lại Dashboard
            </Button>
          ) : (
            <>
              <Button type="button" variant="secondary" onClick={() => router.push("/data-integration")}>
                Chọn phương thức khác
              </Button>
              <Button type="button" variant="primary" onClick={() => router.push(retryRoute)}>
                Thử lại
              </Button>
            </>
          )}
        </div>
      </div>
    </section>
  );
}
