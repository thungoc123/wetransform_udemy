import { DashboardShell } from "@/components/layout/dashboard-shell";
import { ProcessingStatus } from "@/components/data-integration/processing-status";
import { DataMethod } from "@/types/data-integration";

interface DataIntegrationProcessingPageProps {
  searchParams?: {
    source?: string;
    scenario?: string;
    fileName?: string;
  };
}

export default function DataIntegrationProcessingPage({
  searchParams,
}: DataIntegrationProcessingPageProps) {
  const source: DataMethod = searchParams?.source === "file" ? "file" : "api";
  const scenarioRaw = searchParams?.scenario;
  const scenario: "success" | "warning" | "error" =
    scenarioRaw === "warning" || scenarioRaw === "error" ? scenarioRaw : "success";

  return (
    <DashboardShell>
      <ProcessingStatus source={source} scenario={scenario} fileName={searchParams?.fileName} />
    </DashboardShell>
  );
}
