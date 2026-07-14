"use client";

import { useEffect, useMemo, useState } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { getDropOffAnalysisMock } from "@/lib/mocks/course-analytics.mock";
import { getSession } from "@/lib/session";
import { DropOffAnalysisData } from "@/types/course-analytics";

type ViewState = "loading" | "ready" | "error";

interface DropOffAnalysisProps {
  courseId: string;
}

export function DropOffAnalysis({ courseId }: DropOffAnalysisProps) {
  const router = useRouter();

  const [threshold, setThreshold] = useState(20);
  const [state, setState] = useState<ViewState>("loading");
  const [data, setData] = useState<DropOffAnalysisData | null>(null);
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
        const response = await getDropOffAnalysisMock(courseId, threshold);
        if (!active) {
          return;
        }
        setData(response);
        setState("ready");
      } catch (err) {
        if (!active) {
          return;
        }
        const message = err instanceof Error ? err.message : "Unknown error";
        if (message === "NO_DATA") {
          router.replace(`/courses/${courseId}/empty?reason=empty`);
          return;
        }
        setError("Không thể tải dữ liệu drop-off. Vui lòng thử lại.");
        setState("error");
      }
    }

    load();

    return () => {
      active = false;
    };
  }, [courseId, router, threshold]);

  const hotspots = useMemo(
    () => (data?.lessons ?? []).filter((lesson) => lesson.dropOffRate >= threshold),
    [data, threshold],
  );

  return (
    <section>
      <header className="dashboard-header">
        <div>
          <h1>Drop-off Analysis View</h1>
          <p className="subtitle" style={{ margin: "6px 0 0" }}>
            Funnel view và danh sách bài học vượt ngưỡng cảnh báo.
          </p>
        </div>
        <Button variant="secondary" onClick={() => router.push(`/courses/${courseId}`)}>
          Quay lại Dashboard
        </Button>
      </header>

      <div className="analytics-toolbar">
        <label className="field-label" htmlFor="threshold-slider">
          Warning Threshold: {threshold}%
        </label>
        <input
          id="threshold-slider"
          type="range"
          min={10}
          max={40}
          step={1}
          value={threshold}
          onChange={(event) => setThreshold(Number(event.target.value))}
          className="analytics-range"
        />
      </div>

      {state === "loading" ? (
        <div className="metric-card skeleton" style={{ height: 180 }} />
      ) : null}

      {state === "error" ? (
        <div className="alert alert-error" role="alert">
          {error}
        </div>
      ) : null}

      {state === "ready" ? (
        <>
          <div className="analytics-funnel" role="img" aria-label="Drop-off funnel chart summary">
            {(data?.lessons ?? []).map((lesson) => (
              <div key={lesson.lessonId} className="funnel-row">
                <span className="funnel-label">{lesson.lessonTitle}</span>
                <div className="funnel-bar-track">
                  <div
                    className={lesson.dropOffRate >= threshold ? "funnel-bar warning" : "funnel-bar"}
                    style={{ width: `${Math.max(10, lesson.dropOffRate)}%` }}
                  />
                </div>
                <span className="funnel-value">{lesson.dropOffRate}%</span>
              </div>
            ))}
          </div>

          <div className="metric-card" style={{ marginTop: 16 }}>
            <p className="metric-label">Hot Spots Need Attention</p>

            {hotspots.length === 0 ? (
              <p className="metric-note">Không có bài học nào vượt ngưỡng hiện tại.</p>
            ) : (
              <div className="hotspot-list">
                {hotspots.map((lesson) => (
                  <button
                    key={lesson.lessonId}
                    type="button"
                    className="hotspot-item"
                    onClick={() => router.push(`/courses/${courseId}/lessons/${lesson.lessonId}`)}
                  >
                    <span>{lesson.lessonTitle}</span>
                    <span className="warning-chip">{lesson.dropOffRate}%</span>
                  </button>
                ))}
              </div>
            )}
          </div>
        </>
      ) : null}
    </section>
  );
}
