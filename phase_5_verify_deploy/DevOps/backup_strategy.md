# Chiến lược sao lưu dữ liệu (Backup Strategy)

## Mục tiêu
Đảm bảo an toàn dữ liệu, phòng tránh mất mát thông tin trong trường hợp rủi ro hệ thống.

## Công cụ sử dụng
- MVP: Dùng công cụ `pg_dump` mặc định của PostgreSQL.
- Định dạng file backup: Nén gzip (`.sql.gz`).
- Thư mục lưu trữ: `source/backend/backups/`.

## Script Backup
Script đã được tạo sẵn tại `source/backend/scripts/backup_db.sh`.
Bạn có thể chạy thủ công:
```bash
./scripts/backup_db.sh
```

## Tự động hóa với Cronjob
Để tự động backup hàng ngày vào lúc 2 giờ sáng, thiết lập cronjob trên Server (Host machine):

1. Mở cron editor:
```bash
crontab -e
```

2. Thêm dòng sau (đổi `/path/to/project` thành đường dẫn thực tế):
```bash
0 2 * * * cd /path/to/project/source/backend && ./scripts/backup_db.sh >> /var/log/db_backup.log 2>&1
```

Script sẽ tự động dọn dẹp các bản backup cũ hơn 7 ngày để tiết kiệm dung lượng.
