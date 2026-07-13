#!/bin/bash
# Backup Script for PostgreSQL Database
# Usage: ./backup_db.sh

# Exit immediately if a command exits with a non-zero status
set -e

# Configuration
DB_CONTAINER="learning_analytics_db"
DB_USER="user"
DB_NAME="learning_analytics"
BACKUP_DIR="./backups"
DATE=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="${BACKUP_DIR}/${DB_NAME}_${DATE}.sql.gz"

# Create backup directory if it doesn't exist
mkdir -p "${BACKUP_DIR}"

echo "Starting backup for database: ${DB_NAME} at ${DATE}..."

# Execute pg_dump inside the docker container, then compress it
docker exec -t ${DB_CONTAINER} pg_dump -U ${DB_USER} ${DB_NAME} | gzip > "${BACKUP_FILE}"

echo "Backup successfully saved to: ${BACKUP_FILE}"

# Optional: Delete backups older than 7 days
find "${BACKUP_DIR}" -type f -name "*.sql.gz" -mtime +7 -exec rm {} \;
echo "Cleaned up old backups (older than 7 days)."
