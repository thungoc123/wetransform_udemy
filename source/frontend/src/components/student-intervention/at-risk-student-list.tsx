"use client";

import { useEffect, useMemo, useState } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import {
  getAtRiskStudentListMock,
  sendReminderMock,
} from "@/lib/mocks/student-intervention.mock";
import { getSession } from "@/lib/session";
import { AtRiskStudentItem, RiskSegment } from "@/types/student-intervention";
import { ReminderComposerModal } from "./reminder-composer-modal";

type ViewState = "loading" | "ready" | "error";

interface AtRiskStudentListProps {
  courseId: string;
}

export function AtRiskStudentList({ courseId }: AtRiskStudentListProps) {
  const router = useRouter();
  const [state, setState] = useState<ViewState>("loading");
  const [items, setItems] = useState<AtRiskStudentItem[]>([]);
  const [filter, setFilter] = useState<RiskSegment | "all">("all");
  const [selected, setSelected] = useState<AtRiskStudentItem | null>(null);
  const [banner, setBanner] = useState<string>("");
  const [isSending, setIsSending] = useState(false);

  useEffect(() => {
    if (!getSession()) {
      router.replace("/login");
      return;
    }

    let active = true;

    async function load() {
      setState("loading");
      try {
        const data = await getAtRiskStudentListMock();
        if (!active) {
          return;
        }
        setItems(data);
        setState("ready");
      } catch {
        if (!active) {
          return;
        }
        setState("error");
      }
    }

    load();

    return () => {
      active = false;
    };
  }, [router]);

  const filteredItems = useMemo(
    () => (filter === "all" ? items : items.filter((item) => item.segment === filter)),
    [filter, items],
  );

  function canIntervene(item: AtRiskStudentItem): boolean {
    return item.lastSentDaysAgo === null || item.lastSentDaysAgo >= 7;
  }

  function onOpenComposer(item: AtRiskStudentItem) {
    if (!canIntervene(item)) {
      setBanner(
        `Học viên ${item.displayId} đã nhận tin ${item.lastSentDaysAgo} ngày trước. Bạn chỉ được gửi lại sau 7 ngày.`,
      );
      return;
    }

    setBanner("");
    setSelected(item);
  }

  async function onSend(content: string) {
    if (!selected) {
      return;
    }

    setIsSending(true);
    const result = await sendReminderMock(selected.studentId, content);
    setIsSending(false);
    setSelected(null);

    const params = new URLSearchParams({
      status: result.status,
      studentId: result.studentId,
      message: result.message,
    });

    router.push(`/courses/${courseId}/reminders/result?${params.toString()}`);
  }

  return (
    <section>
      <header className="dashboard-header">
        <div>
          <h1>At-risk Student List</h1>
          <p className="subtitle" style={{ margin: "6px 0 0" }}>
            Danh sách học viên At-risk/Inactive để gửi can thiệp cá nhân hóa.
          </p>
        </div>
        <Button variant="secondary" onClick={() => router.push(`/courses/${courseId}`)}>
          Quay lại Course Dashboard
        </Button>
      </header>

      <div className="analytics-toolbar">
        <label className="field-label" htmlFor="risk-filter">
          Filter segment
        </label>
        <select
          id="risk-filter"
          className="analytics-select"
          value={filter}
          onChange={(event) => setFilter(event.target.value as RiskSegment | "all")}
        >
          <option value="all">All segments</option>
          <option value="at-risk">At-risk</option>
          <option value="inactive">Inactive</option>
        </select>
      </div>

      {banner ? (
        <div className="alert alert-warning" role="alert">
          {banner}
        </div>
      ) : null}

      {state === "loading" ? <div className="metric-card skeleton" style={{ height: 220 }} /> : null}

      {state === "error" ? (
        <div className="alert alert-error" role="alert">
          Không thể tải danh sách học viên can thiệp.
        </div>
      ) : null}

      {state === "ready" && filteredItems.length === 0 ? (
        <div className="metric-card" role="status">
          <p className="metric-label">Không có học viên cần can thiệp</p>
          <p className="metric-note">Tất cả học viên hiện đang ở trạng thái ổn định.</p>
        </div>
      ) : null}

      {state === "ready" && filteredItems.length > 0 ? (
        <div className="metric-card">
          <div className="intervention-table-head">
            <span>Student</span>
            <span>Lesson</span>
            <span>Inactive Days</span>
            <span>Last Sent</span>
            <span>Action</span>
          </div>
          {filteredItems.map((item) => (
            <div key={item.studentId} className="intervention-table-row">
              <span>{item.displayId}</span>
              <span>{item.lessonRef}</span>
              <span>{item.inactiveDays}</span>
              <span>{item.lastSentDaysAgo === null ? "Never" : `${item.lastSentDaysAgo} days ago`}</span>
              <span>
                <Button
                  type="button"
                  variant={canIntervene(item) ? "primary" : "secondary"}
                  onClick={() => onOpenComposer(item)}
                >
                  Gửi nhắc nhở
                </Button>
              </span>
            </div>
          ))}
        </div>
      ) : null}

      {selected ? (
        <ReminderComposerModal
          student={selected}
          open
          isSending={isSending}
          onClose={() => setSelected(null)}
          onSend={onSend}
        />
      ) : null}
    </section>
  );
}