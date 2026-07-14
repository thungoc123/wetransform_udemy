"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { ReactNode } from "react";
import { cn } from "@/lib/utils";

interface DashboardShellProps {
  children: ReactNode;
}

export function DashboardShell({ children }: DashboardShellProps) {
  const pathname = usePathname();

  return (
    <div className="dashboard-shell">
      <aside className="dashboard-sidebar">
        <div className="dashboard-brand">EduInsight AI</div>
        <nav className="dashboard-nav" aria-label="Primary">
          <Link
            href="/dashboard"
            className={cn("dashboard-nav-item", pathname === "/dashboard" && "active")}
          >
            Dashboard Overview
          </Link>
          <Link
            href="/courses/course-001"
            className={cn(
              "dashboard-nav-item",
              pathname.startsWith("/courses") && !pathname.includes("/reminders") && "active",
            )}
          >
            Course Analytics
          </Link>
          <Link
            href="/data-integration"
            className={cn("dashboard-nav-item", pathname.startsWith("/data-integration") && "active")}
          >
            Data Integration
          </Link>
          <Link
            href="/courses/course-001/reminders"
            className={cn("dashboard-nav-item", pathname.includes("/reminders") && "active")}
          >
            Student Intervention
          </Link>
        </nav>
      </aside>
      <main className="dashboard-main">{children}</main>
    </div>
  );
}
