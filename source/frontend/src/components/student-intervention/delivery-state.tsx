"use client";

import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";

interface DeliveryStateProps {
  courseId: string;
  status: "success" | "error";
  message: string;
}

export function DeliveryState({ courseId, status, message }: DeliveryStateProps) {
  const router = useRouter();

  return (
    <section>
      <header className="dashboard-header">
        <div>
          <h1>Confirmation / Delivery State</h1>
          <p className="subtitle" style={{ margin: "6px 0 0" }}>
            Kết quả gửi nhắc nhở và trạng thái can thiệp học viên.
          </p>
        </div>
      </header>

      <div className="integration-result-card">
        <div className={status === "success" ? "result-icon success" : "result-icon error"}>
          {status === "success" ? "✓" : "!"}
        </div>
        <h2>{status === "success" ? "Gửi thành công" : "Gửi thất bại"}</h2>
        <p>{message}</p>

        <div className="integration-form-actions">
          <Button type="button" variant="secondary" onClick={() => router.push(`/courses/${courseId}/reminders`)}>
            Quay lại danh sách
          </Button>
          {status === "success" ? (
            <Button type="button" variant="primary" onClick={() => router.push(`/courses/${courseId}/reminders/summary`)}>
              Xem Re-engagement Summary
            </Button>
          ) : null}
        </div>
      </div>
    </section>
  );
}
