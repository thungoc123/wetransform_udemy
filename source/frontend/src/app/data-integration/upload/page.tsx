import { FileUploadScreen } from "@/components/data-integration/file-upload-screen";
import { DashboardShell } from "@/components/layout/dashboard-shell";

export default function DataIntegrationUploadPage() {
  return (
    <DashboardShell>
      <FileUploadScreen />
    </DashboardShell>
  );
}
