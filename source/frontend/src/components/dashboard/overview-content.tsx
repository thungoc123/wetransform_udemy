"use client";

import { useCallback, useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { Card, CardNote, CardTitle, CardValue } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { getDashboardOverviewMock } from "@/lib/mocks/dashboard.mock";
import { getSession } from "@/lib/session";
import { DashboardMode, DashboardOverview } from "@/types/dashboard";

type LoadState = "loading" | "success" | "error";

interface DashboardOverviewContentProps {
  mode: DashboardMode;
}

export function DashboardOverviewContent({ mode }: DashboardOverviewContentProps) {
  const router = useRouter();

  const [state, setState] = useState<LoadState>("loading");
  const [data, setData] = useState<DashboardOverview | null>(null);
  const [errorMessage, setErrorMessage] = useState<string>("");

  const loadData = useCallback(async () => {
    setState("loading");
    setErrorMessage("");

    try {
      const response = await getDashboardOverviewMock(mode);
      setData(response);
      setState("success");
    } catch {
      setState("error");
      setErrorMessage("Unable to load dashboard summary. Please retry.");
    }
  }, [mode]);

  useEffect(() => {
    const existingSession = getSession();
    if (!existingSession) {
      router.replace("/login");
      return;
    }

    loadData();
  }, [loadData, router]);

  return (
    <>
      <header className="dashboard-header">
        <div>
          <h1>Dashboard Overview</h1>
          <p className="subtitle" style={{ margin: "6px 0 0" }}>
            Teaching performance and learner engagement snapshot.
          </p>
        </div>
        <Button variant="secondary" onClick={() => router.push("/dashboard?state=empty")}>
          Simulate Empty State
        </Button>
      </header>

      {state === "loading" ? (
        <div className="dashboard-grid" aria-live="polite" aria-busy="true">
          {[0, 1, 2].map((item) => (
            <div key={item} className="metric-card skeleton" style={{ height: 152 }} />
          ))}
        </div>
      ) : null}

      {state === "error" ? (
        <div className="alert alert-error" role="alert">
          <div>{errorMessage}</div>
          <Button variant="secondary" style={{ marginTop: 12 }} onClick={loadData}>
            Retry
          </Button>
        </div>
      ) : null}

      {state === "success" && data && data.metrics.length === 0 ? (
        <div className="metric-card" role="status">
          <CardTitle>No course analytics available yet</CardTitle>
          <CardNote>
            Connect your data source to start seeing engagement and completion trends.
          </CardNote>
          <Button variant="primary" style={{ marginTop: 14 }} onClick={() => router.push("/data-integration")}>
            Connect Data Source
          </Button>
        </div>
      ) : null}

      {state === "success" && data && data.metrics.length > 0 ? (
        <div className="dashboard-grid">
          {data.metrics.map((metric) => (
            <Card key={metric.id}>
              <CardTitle>{metric.label}</CardTitle>
              <CardValue>{metric.value}</CardValue>
              <CardNote>{metric.note}</CardNote>
            </Card>
          ))}
        </div>
      ) : null}
    </>
  );
}