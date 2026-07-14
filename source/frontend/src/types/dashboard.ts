export interface DashboardMetric {
  id: string;
  label: string;
  value: string;
  note: string;
}

export interface DashboardOverview {
  metrics: DashboardMetric[];
  announcements: string[];
}

export type DashboardMode = "default" | "empty" | "error";