#!/usr/bin/env python3
"""手动执行数据库结构迁移（也可在 Flask 启动时自动运行）。"""
from app import create_app, db
from app.utils.db_migrate import ensure_xhs_posts_schema

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        ensure_xhs_posts_schema(db)
        print('数据库迁移检查完成。')
