import { IntegrationResult } from "@/components/data-integration/integration-result";
import { DashboardShell } from "@/components/layout/dashboard-shell";
import { DataMethod } from "@/types/data-integration";

interface DataIntegrationResultPageProps {
  searchParams?: {
    status?: string;
    source?: string;
    message?: string;
    warning?: string;
  };
}

export default function DataIntegrationResultPage({ searchParams }: DataIntegrationResultPageProps) {
  const status = searchParams?.status === "error" ? "error" : "success";
  const source: DataMethod = searchParams?.source === "file" ? "file" : "api";
  const message =
    searchParams?.message ??
    (status === "success"
      ? "Dữ liệu đã được import thành công."
      : "Import thất bại. Vui lòng kiểm tra dữ liệu và thử lại.");

  return (
    <DashboardShell>
      <IntegrationResult status={status} source={source} message={message} warning={searchParams?.warning} />
    </DashboardShell>
  );
}