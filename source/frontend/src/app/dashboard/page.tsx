import { DashboardOverviewContent } from "@/components/dashboard/overview-content";
import { DashboardShell } from "@/components/layout/dashboard-shell";
import { DashboardMode } from "@/types/dashboard";

interface DashboardPageProps {
	searchParams?: {
		state?: string;
	};
}

export default function DashboardPage({ searchParams }: DashboardPageProps) {
	const routeMode = searchParams?.state;
	const mode: DashboardMode =
		routeMode === "empty" || routeMode === "error" ? routeMode : "default";

	return (
		<DashboardShell>
			<DashboardOverviewContent mode={mode} />
		</DashboardShell>
	);
}
