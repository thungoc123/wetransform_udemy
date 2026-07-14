"use client";

import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { getReminderTemplateMock } from "@/lib/mocks/student-intervention.mock";
import { AtRiskStudentItem } from "@/types/student-intervention";

interface ReminderComposerModalProps {
  student: AtRiskStudentItem;
  open: boolean;
  isSending: boolean;
  onClose: () => void;
  onSend: (content: string) => void;
}

export function ReminderComposerModal({
  student,
  open,
  isSending,
  onClose,
  onSend,
}: ReminderComposerModalProps) {
  const [content, setContent] = useState("");
  const [subject, setSubject] = useState("");
  const [error, setError] = useState<string>("");

  useEffect(() => {
    if (!open) {
      return;
    }

    let active = true;

    async function loadTemplate() {
      const template = await getReminderTemplateMock(student);
      if (!active) {
        return;
      }
      setSubject(template.subject);
      setContent(template.body);
    }

    loadTemplate();

    return () => {
      active = false;
    };
  }, [open, student]);

  function handleSend() {
    if (!content.trim()) {
      setError("Nội dung nhắc nhở không được để trống.");
      return;
    }

    setError("");
    onSend(content);
  }

  if (!open) {
    return null;
  }

  return (
    <div className="intervention-modal-backdrop" role="presentation">
      <div className="intervention-modal" role="dialog" aria-modal="true" aria-label="Reminder composer">
        <h2>Reminder Composer Modal</h2>
        <p className="metric-note">To: {student.displayId}</p>
        <p className="metric-note">Subject: {subject || "Loading template..."}</p>

        <label className="field-label" htmlFor="reminder-content">
          Message content
        </label>
        <textarea
          id="reminder-content"
          className="intervention-textarea"
          value={content}
          onChange={(event) => setContent(event.target.value)}
        />

        {error ? (
          <div className="alert alert-error" role="alert" style={{ marginTop: 10 }}>
            {error}
          </div>
        ) : null}

        <div className="integration-form-actions" style={{ marginTop: 14 }}>
          <Button type="button" variant="secondary" onClick={onClose}>
            Hủy
          </Button>
          <Button type="button" variant="primary" disabled={isSending} onClick={handleSend}>
            {isSending ? "Đang gửi..." : "Xác nhận gửi"}
          </Button>
        </div>
      </div>
    </div>
  );
}
