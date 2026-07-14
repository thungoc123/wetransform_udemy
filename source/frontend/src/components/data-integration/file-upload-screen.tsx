"use client";

import { ChangeEvent, useEffect, useMemo, useState } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { validateUdemyFileMock } from "@/lib/mocks/data-integration.mock";
import { getSession } from "@/lib/session";

export function FileUploadScreen() {
  const router = useRouter();

  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    if (!getSession()) {
      router.replace("/login");
    }
  }, [router]);

  const helper = useMemo(
    () =>
      "Mẹo test: đặt tên file chứa missing-columns, over-limit hoặc inconsistent để mô phỏng lỗi/cảnh báo.",
    [],
  );

  function onPickFile(event: ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0] ?? null;
    setSelectedFile(file);
    setErrorMessage(null);
    setProgress(0);
  }

  async function onUpload() {
    if (!selectedFile) {
      setErrorMessage("Vui lòng chọn file CSV/XLSX trước khi tải lên.");
      return;
    }

    setErrorMessage(null);
    setIsUploading(true);
    setProgress(25);

    const validation = await validateUdemyFileMock(selectedFile);

    if (!validation.ok) {
      setIsUploading(false);
      setProgress(0);

      const missingColumnsText = validation.missingColumns?.length
        ? ` Thiếu cột: ${validation.missingColumns.join(", ")}.`
        : "";

      const fullMessage = `${validation.message}${missingColumnsText}`;
      setErrorMessage(fullMessage);

      const params = new URLSearchParams({
        status: "error",
        source: "file",
        code: validation.code,
        message: fullMessage,
      });
      router.push(`/data-integration/result?${params.toString()}`);
      return;
    }

    setProgress(100);

    const params = new URLSearchParams({
      source: "file",
      scenario: validation.scenario,
      fileName: validation.fileName,
    });

    router.push(`/data-integration/processing?${params.toString()}`);
  }

  return (
    <section>
      <header className="dashboard-header" style={{ marginBottom: 16 }}>
        <div>
          <h1>File Upload Screen</h1>
          <p className="subtitle" style={{ margin: "6px 0 0" }}>
            Upload file CSV/XLSX xuất chuẩn từ Udemy để hệ thống xử lý.
          </p>
        </div>
      </header>

      <div className="integration-form-card">
        <label htmlFor="udemyFile" className="upload-dropzone">
          <span className="upload-title">Kéo thả file vào đây hoặc bấm để chọn file</span>
          <span className="upload-subtitle">Hỗ trợ định dạng .csv và .xlsx</span>
          <input
            id="udemyFile"
            type="file"
            accept=".csv,.xlsx"
            className="upload-input"
            onChange={onPickFile}
            aria-label="Chọn file dữ liệu Udemy"
          />
        </label>

        {selectedFile ? (
          <div className="upload-meta" role="status">
            <strong>File đã chọn:</strong> {selectedFile.name} ({Math.ceil(selectedFile.size / 1024)} KB)
          </div>
        ) : null}

        {isUploading ? (
          <div className="progress-wrap" aria-live="polite">
            <div className="progress-label">Đang tải lên: {progress}%</div>
            <div className="progress-track" role="progressbar" aria-valuemin={0} aria-valuemax={100} aria-valuenow={progress}>
              <div className="progress-fill" style={{ width: `${progress}%` }} />
            </div>
          </div>
        ) : null}

        {errorMessage ? (
          <div className="alert alert-error" role="alert" style={{ marginTop: 12 }}>
            {errorMessage}
          </div>
        ) : null}

        <div className="integration-form-actions">
          <Button type="button" variant="secondary" onClick={() => router.push("/data-integration")}>
            Hủy
          </Button>
          <Button type="button" variant="primary" onClick={onUpload} disabled={isUploading}>
            {isUploading ? "Đang upload..." : "Tải lên & Phân tích"}
          </Button>
        </div>

        <p className="integration-helper-text">{helper}</p>
      </div>
    </section>
  );
}
