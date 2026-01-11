#!/bin/bash

# MySQL备份脚本

BACKUP_DIR="/root/mysql_backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="${BACKUP_DIR}/xingshuzi_${TIMESTAMP}.sql"

# 创建备份目录
mkdir -p ${BACKUP_DIR}

echo "开始备份MySQL数据库..."
echo "时间: $(date)"

# 备份数据库
docker compose exec mysql mysqldump -uroot -pMyStrongRootPassword123 \
  --single-transaction \
  --quick \
  --lock-tables=false \
  xingshuzi > ${BACKUP_FILE}

# 检查备份是否成功
if [ $? -eq 0 ]; then
    # 压缩备份文件
    gzip ${BACKUP_FILE}
    echo "✅ 备份成功: ${BACKUP_FILE}.gz"
    
    # 显示备份文件大小
    du -h ${BACKUP_FILE}.gz
    
    # 删除7天前的备份
    find ${BACKUP_DIR} -name "*.sql.gz" -mtime +7 -delete
    echo "已清理7天前的旧备份"
    
    # 显示当前所有备份
    echo ""
    echo "当前备份列表:"
    ls -lh ${BACKUP_DIR}/*.sql.gz 2>/dev/null || echo "暂无备份文件"
else
    echo "❌ 备份失败"
    exit 1
fi

