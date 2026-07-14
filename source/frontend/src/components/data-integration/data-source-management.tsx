import Link from "next/link";

export function DataSourceManagement() {
  return (
    <section>
      <header className="dashboard-header" style={{ marginBottom: 16 }}>
        <div>
          <h1>Data Source Management</h1>
          <p className="subtitle" style={{ margin: "6px 0 0" }}>
            Chọn phương thức nạp dữ liệu Udemy để bắt đầu phân tích.
          </p>
        </div>
      </header>

      <div className="integration-choice-grid">
        <article className="integration-choice-card">
          <h2>Kết nối API Udemy</h2>
          <p>
            Đồng bộ dữ liệu trực tiếp bằng Client ID và API Key. Phù hợp khi cần cập nhật dữ liệu
            thường xuyên.
          </p>
          <Link href="/data-integration/api" className="button button-primary integration-choice-cta">
            Chọn Kết nối API
          </Link>
        </article>

        <article className="integration-choice-card">
          <h2>Tải file Udemy</h2>
          <p>
            Tải lên file CSV/XLSX xuất chuẩn từ Udemy để xử lý theo lô trong môi trường MVP.
          </p>
          <Link
            href="/data-integration/upload"
            className="button button-secondary integration-choice-cta"
          >
            Chọn Tải File
          </Link>
        </article>
      </div>

      <div className="alert alert-warning" role="status" style={{ marginTop: 16 }}>
        Giới hạn MVP: tối đa 3 khóa học và 2.600 học viên cho mỗi lần import.
      </div>
    </section>
  );
}