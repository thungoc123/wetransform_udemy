import { ApiConnectionForm } from "@/components/data-integration/api-connection-form";
import { DashboardShell } from "@/components/layout/dashboard-shell";

export default function DataIntegrationApiPage() {
  return (
    <DashboardShell>
      <ApiConnectionForm />
    </DashboardShell>
  );
}