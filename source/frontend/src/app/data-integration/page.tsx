import { DataSourceManagement } from "@/components/data-integration/data-source-management";
import { DashboardShell } from "@/components/layout/dashboard-shell";

export default function DataIntegrationPage() {
  return (
    <DashboardShell>
      <DataSourceManagement />
    </DashboardShell>
  );
}