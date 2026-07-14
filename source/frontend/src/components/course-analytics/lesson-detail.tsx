"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { getLessonDetailMock } from "@/lib/mocks/course-analytics.mock";
import { getSession } from "@/lib/session";
import { LessonDetailData } from "@/types/course-analytics";

type ViewState = "loading" | "ready" | "error";

interface LessonDetailProps {
  courseId: string;
  lessonId: string;
}

export function LessonDetail({ courseId, lessonId }: LessonDetailProps) {
  const router = useRouter();

  const [state, setState] = useState<ViewState>("loading");
  const [data, setData] = useState<LessonDetailData | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!getSession()) {
      router.replace("/login");
      return;
    }

    let active = true;

    async function load() {
      setState("loading");
      setError("");

      try {
        const response = await getLessonDetailMock(courseId, lessonId);
        if (!active) {
          return;
        }

        if (response.learnerCount < 30) {
          router.replace(`/courses/${courseId}/empty?reason=low-data&lessonId=${lessonId}`);
          return;
        }

        setData(response);
        setState("ready");
      } catch {
        if (!active) {
          return;
        }
        setError("Không thể tải chi tiết bài học. Vui lòng thử lại.");
        setState("error");
      }
    }

    load();

    return () => {
      active = false;
    };
  }, [courseId, lessonId, router]);

  return (
    <section>
      <header className="dashboard-header">
        <div>
          <h1>Lesson Detail View</h1>
          <p className="subtitle" style={{ margin: "6px 0 0" }}>
            Drill-down dữ liệu bài giảng và điểm dừng học tập.
          </p>
        </div>
        <Button variant="secondary" onClick={() => router.push(`/courses/${courseId}/drop-off`)}>
          Quay lại Drop-off
        </Button>
      </header>

      {state === "loading" ? <div className="metric-card skeleton" style={{ height: 220 }} /> : null}

      {state === "error" ? (
        <div className="alert alert-error" role="alert">
          {error}
        </div>
      ) : null}

      {state === "ready" && data ? (
        <>
          <div className="metric-card">
            <p className="metric-label">{data.lessonTitle}</p>
            <p className="metric-note">Learners: {data.learnerCount}</p>
            <p className="metric-note">Drop-off: {data.dropOffRate}%</p>
            <p className="metric-note">Completion: {data.completionRate}%</p>
          </div>

          {data.lessonType === "video" ? (
            <div className="metric-card" style={{ marginTop: 16 }}>
              <p className="metric-label">Timeline Retention</p>
              <div className="timeline-grid" role="img" aria-label="Lesson timeline retention chart">
                {data.timeline.map((point) => (
                  <div key={point.second} className="timeline-bar-wrap">
                    <div className="timeline-bar" style={{ height: `${Math.max(10, point.retention)}%` }} />
                    <span>{point.second}s</span>
                  </div>
                ))}
              </div>
            </div>
          ) : (
            <div className="metric-card" style={{ marginTop: 16 }}>
              <p className="metric-label">Non-video Completion Distribution</p>
              <p className="metric-note">Completed: {data.fallbackDistribution?.completed ?? 0}</p>
              <p className="metric-note">Incomplete: {data.fallbackDistribution?.incomplete ?? 0}</p>
              <p className="metric-note">Dropped midway: {data.fallbackDistribution?.droppedMidway ?? 0}</p>
            </div>
          )}

          <div style={{ marginTop: 16 }}>
            <Button variant="primary" onClick={() => router.push(`/courses/${courseId}/lessons/${lessonId}/ai-insights`)}>
              Mở AI Insights
            </Button>
          </div>
        </>
      ) : null}
    </section>
  );
}
