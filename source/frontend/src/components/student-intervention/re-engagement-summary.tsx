"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { getReEngagementSummaryMock } from "@/lib/mocks/student-intervention.mock";
import { getSession } from "@/lib/session";
import { ReEngagementSummaryData } from "@/types/student-intervention";

interface ReEngagementSummaryProps {
  courseId: string;
}

type ViewState = "loading" | "ready" | "error";

export function ReEngagementSummary({ courseId }: ReEngagementSummaryProps) {
  const router = useRouter();
  const [state, setState] = useState<ViewState>("loading");
  const [data, setData] = useState<ReEngagementSummaryData | null>(null);

  useEffect(() => {
    if (!getSession()) {
      router.replace("/login");
      return;
    }

    let active = true;

    async function load() {
      setState("loading");
      try {
        const summary = await getReEngagementSummaryMock();
        if (!active) {
          return;
        }
        setData(summary);
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
  }, [router]);

  return (
    <section>
      <header className="dashboard-header">
        <div>
          <h1>Re-engagement Summary</h1>
          <p className="subtitle" style={{ margin: "6px 0 0" }}>
            Kết quả theo dõi phản hồi sau 7 ngày từ chiến dịch nhắc nhở.
          </p>
        </div>
        <Button variant="secondary" onClick={() => router.push(`/courses/${courseId}/reminders`)}>
          Quay lại At-risk List
        </Button>
      </header>

      {state === "loading" ? <div className="metric-card skeleton" style={{ height: 220 }} /> : null}

      {state === "error" ? (
        <div className="alert alert-error" role="alert">
          Chưa có dữ liệu theo dõi hoặc sync thất bại.
        </div>
      ) : null}

      {state === "ready" && data ? (
        <>
          <div className="dashboard-grid">
            <article className="metric-card">
              <p className="metric-label">Reminders Sent</p>
              <p className="metric-value">{data.sentCount}</p>
            </article>
            <article className="metric-card">
              <p className="metric-label">Re-engaged Students</p>
              <p className="metric-value">{data.reEngagedCount}</p>
            </article>
            <article className="metric-card">
              <p className="metric-label">Still Monitoring</p>
              <p className="metric-value">{data.monitoredCount}</p>
            </article>
          </div>

          <div className="metric-card" style={{ marginTop: 16 }}>
            <div className="intervention-table-head">
              <span>Student</span>
              <span>Status</span>
              <span>Note</span>
            </div>
            {data.students.map((item) => (
              <div key={item.studentId} className="intervention-table-row summary">
                <span>{item.displayId}</span>
                <span>{item.status}</span>
                <span>{item.note}</span>
              </div>
            ))}
          </div>
        </>
      ) : null}
    </section>
  );
}
