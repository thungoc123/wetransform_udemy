import { DashboardShell } from "@/components/layout/dashboard-shell";
import { DeliveryState } from "@/components/student-intervention/delivery-state";

interface ReminderResultPageProps {
  params: {
    courseId: string;
  };
  searchParams?: {
    status?: string;
    message?: string;
  };
}

export default function ReminderResultPage({ params, searchParams }: ReminderResultPageProps) {
  const status = searchParams?.status === "error" ? "error" : "success";
  const message =
    searchParams?.message ??
    (status === "success"
      ? "Đã gửi nhắc nhở thành công và bắt đầu theo dõi 7 ngày."
      : "Gửi nhắc nhở thất bại. Vui lòng kiểm tra trạng thái học viên.");

  return (
    <DashboardShell>
      <DeliveryState courseId={params.courseId} status={status} message={message} />
    </DashboardShell>
  );
}