"use client";

import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";

interface EmptyLowDataStateProps {
  courseId: string;
  reason: "empty" | "low-data" | "error";
}

export function EmptyLowDataState({ courseId, reason }: EmptyLowDataStateProps) {
  const router = useRouter();

  const message =
    reason === "low-data"
      ? "Bài học này có dưới 30 học viên tham gia. Hiện chưa đủ độ tin cậy thống kê để phân tích chi tiết."
      : reason === "error"
        ? "Dữ liệu analytics hiện chưa sẵn sàng. Vui lòng thử lại sau hoặc kiểm tra nguồn dữ liệu."
        : "Chưa có dữ liệu khóa học để phân tích. Hãy kết nối hoặc tải dữ liệu Udemy trước.";

  return (
    <section>
      <header className="dashboard-header">
        <div>
          <h1>Empty / Low Data State</h1>
          <p className="subtitle" style={{ margin: "6px 0 0" }}>
            Fallback khi dữ liệu chưa có hoặc chưa đủ độ tin cậy.
          </p>
        </div>
      </header>

      <div className="integration-result-card">
        <div className="result-icon error" aria-hidden="true">
          !
        </div>
        <h2>Dữ liệu chưa đủ để hiển thị analytics</h2>
        <p>{message}</p>
        <div className="integration-form-actions">
          <Button type="button" variant="secondary" onClick={() => router.push(`/courses/${courseId}`)}>
            Quay lại Course Dashboard
          </Button>
          <Button type="button" variant="primary" onClick={() => router.push("/data-integration") }>
            Kết nối dữ liệu
          </Button>
        </div>
      </div>
    </section>
  );
}
