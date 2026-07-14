"use client";

import { useEffect, useMemo, useState } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { getAIInsightsMock } from "@/lib/mocks/course-analytics.mock";
import { getSession } from "@/lib/session";
import { AIInsightItem } from "@/types/course-analytics";

type ViewState = "loading" | "ready" | "error";

interface AIInsightPanelProps {
  courseId: string;
  lessonId: string;
}

export function AIInsightPanel({ courseId, lessonId }: AIInsightPanelProps) {
  const router = useRouter();

  const [state, setState] = useState<ViewState>("loading");
  const [insights, setInsights] = useState<AIInsightItem[]>([]);

  useEffect(() => {
    if (!getSession()) {
      router.replace("/login");
      return;
    }

    let active = true;

    async function load() {
      setState("loading");
      try {
        const response = await getAIInsightsMock(lessonId);
        if (!active) {
          return;
        }
        setInsights(response.insights);
        setState("ready");
      } catch {
        if (!active) {
          return;
        }
        setState("error");
      }
    }

    load();

    return () => {
      active = false;
    };
  }, [lessonId, router]);

  const pendingCount = useMemo(
    () => insights.filter((insight) => insight.status === "pending").length,
    [insights],
  );

  function markInsight(id: string, mode: "applied" | "dismissed") {
    setInsights((current) =>
      current.map((item) =>
        item.id === id
          ? {
              ...item,
              status: mode,
            }
          : item,
      ),
    );
  }

  return (
    <section>
      <header className="dashboard-header">
        <div>
          <h1>AI Insight Panel</h1>
          <p className="subtitle" style={{ margin: "6px 0 0" }}>
            Giả thuyết nguyên nhân và đề xuất tối ưu hóa nội dung bài học.
          </p>
        </div>
        <Button variant="secondary" onClick={() => router.back()}>
          Quay lại Lesson Detail
        </Button>
      </header>

      <div className="alert alert-warning" role="note">
        Các gợi ý, nhận định của trợ lý AI được tự động tạo dựa trên hành vi học tập và chỉ mang tính
        chất tham khảo. Giảng viên chịu trách nhiệm cuối cùng đối với quyết định thay đổi nội dung khóa
        học trên Udemy.
      </div>

      {state === "loading" ? <div className="metric-card skeleton" style={{ height: 220 }} /> : null}

      {state === "error" ? (
        <div className="alert alert-error" role="alert">
          Không thể tải AI insights lúc này. Vui lòng thử lại sau.
        </div>
      ) : null}

      {state === "ready" ? (
        <>
          <p className="metric-note" style={{ marginBottom: 12 }}>
            Pending recommendations: {pendingCount}
          </p>
          <div className="insight-grid">
            {insights.map((item) => (
              <article key={item.id} className="metric-card">
                <p className="metric-label">Hypothesis</p>
                <p className="metric-note">{item.hypothesis}</p>
                <p className="metric-label" style={{ marginTop: 12 }}>
                  Recommendation
                </p>
                <p className="metric-note">{item.suggestion}</p>
                {item.manualOnly ? <span className="warning-chip">Thực hiện thủ công ngoài Udemy</span> : null}
                <p className="metric-note" style={{ marginTop: 10 }}>
                  Status: {item.status}
                </p>
                <div className="integration-form-actions">
                  <Button
                    type="button"
                    variant="secondary"
                    onClick={() => markInsight(item.id, "dismissed")}
                  >
                    Bỏ qua
                  </Button>
                  <Button
                    type="button"
                    variant="primary"
                    onClick={() => markInsight(item.id, "applied")}
                  >
                    Đã áp dụng
                  </Button>
                </div>
              </article>
            ))}
          </div>
        </>
      ) : null}
    </section>
  );
}