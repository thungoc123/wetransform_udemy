"use client";

import { useEffect, useMemo, useState } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { getCourseOverviewMock } from "@/lib/mocks/course-analytics.mock";
import { getSession } from "@/lib/session";
import { CourseOverviewData } from "@/types/course-analytics";

type ViewState = "loading" | "ready" | "error";

interface CourseDashboardProps {
  courseId: string;
  state?: "default" | "empty" | "loading-error";
}

export function CourseDashboard({ courseId, state = "default" }: CourseDashboardProps) {
  const router = useRouter();
  const [viewState, setViewState] = useState<ViewState>("loading");
  const [data, setData] = useState<CourseOverviewData | null>(null);
  const [error, setError] = useState<string>("");

  useEffect(() => {
    if (!getSession()) {
      router.replace("/login");
      return;
    }

    let active = true;

    async function run() {
      setViewState("loading");
      try {
        const response = await getCourseOverviewMock(courseId, state);
        if (!active) {
          return;
        }
        setData(response);
        setViewState("ready");
      } catch (err) {
        if (!active) {
          return;
        }
        const message = err instanceof Error ? err.message : "Unknown error";
        if (message === "NO_DATA") {
          router.replace(`/courses/${courseId}/empty?reason=empty`);
          return;
        }
        setError("Không tải được dữ liệu dashboard. Vui lòng thử lại.");
        setViewState("error");
      }
    }

    run();

    return () => {
      active = false;
    };
  }, [courseId, router, state]);

  const selectedOption = useMemo(
    () => data?.options.find((option) => option.id === data.courseId)?.id ?? courseId,
    [courseId, data],
  );

  return (
    <section>
      <header className="dashboard-header">
        <div>
          <h1>Course Dashboard</h1>
          <p className="subtitle" style={{ margin: "6px 0 0" }}>
            Tổng quan completion, drop-off và phân loại Active/Inactive/At-risk.
          </p>
        </div>
        <Button variant="secondary" onClick={() => router.push(`/courses/${courseId}/drop-off`)}>
          Phân tích điểm dừng
        </Button>
      </header>

      {viewState === "loading" ? (
        <div className="dashboard-grid" aria-busy="true" aria-live="polite">
          {[0, 1, 2].map((item) => (
            <div key={item} className="metric-card skeleton" style={{ height: 148 }} />
          ))}
        </div>
      ) : null}

      {viewState === "error" ? (
        <div className="alert alert-error" role="alert">
          {error}
        </div>
      ) : null}

      {viewState === "ready" && data ? (
        <>
          <div className="analytics-toolbar">
            <label className="field-label" htmlFor="course-selector">
              Course
            </label>
            <select
              id="course-selector"
              className="analytics-select"
              value={selectedOption}
              onChange={(event) => router.push(`/courses/${event.target.value}`)}
            >
              {data.options.map((option) => (
                <option key={option.id} value={option.id}>
                  {option.title}
                </option>
              ))}
            </select>
          </div>

          <div className="dashboard-grid">
            <article className="metric-card">
              <p className="metric-label">Completion Rate</p>
              <p className="metric-value">{data.metrics.completionRate}%</p>
              <p className="metric-note">Overall progress of enrolled learners</p>
            </article>
            <article className="metric-card">
              <p className="metric-label">Drop-off Rate</p>
              <p className="metric-value">{data.metrics.dropOffRate}%</p>
              <p className="metric-note">Threshold warning default: 20%</p>
            </article>
            <article className="metric-card">
              <p className="metric-label">Student Health Split</p>
              <p className="metric-note">Active: {data.metrics.active}</p>
              <p className="metric-note">At-risk: {data.metrics.atRisk}</p>
              <p className="metric-note">Inactive: {data.metrics.inactive}</p>
            </article>
          </div>
        </>
      ) : null}
    </section>
  );
}