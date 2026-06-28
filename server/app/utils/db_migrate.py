"""数据库表结构幂等迁移（部署新代码后自动补齐缺失字段）。"""

from sqlalchemy import inspect, text


def _index_exists(inspector, table, index_name):
    return any(
        idx['name'] == index_name
        for idx in inspector.get_indexes(table)
    )


def ensure_xhs_posts_schema(db):
    """补齐 xhs_posts 缺失列，并迁移为按星期维度存储。"""
    try:
        inspector = inspect(db.engine)
        if 'xhs_posts' not in inspector.get_table_names():
            return

        columns = {c['name'] for c in inspector.get_columns('xhs_posts')}

        if 'student' not in columns:
            db.session.execute(text(
                "ALTER TABLE xhs_posts "
                "ADD COLUMN student varchar(10) NOT NULL DEFAULT 'a' "
                "COMMENT '账号: a/b/c/d' AFTER post_date"
            ))
            db.session.commit()
            print('[migrate] Added column xhs_posts.student')
            columns.add('student')

        if 'poster_text' not in columns:
            db.session.execute(text(
                "ALTER TABLE xhs_posts "
                "ADD COLUMN poster_text varchar(200) DEFAULT NULL "
                "COMMENT '大字报文字' AFTER period"
            ))
            db.session.commit()
            print('[migrate] Added column xhs_posts.poster_text')
            columns.add('poster_text')

        if 'weekday' not in columns:
            db.session.execute(text(
                "ALTER TABLE xhs_posts "
                "ADD COLUMN weekday varchar(10) DEFAULT NULL "
                "COMMENT '星期: mon~sun' AFTER id"
            ))
            db.session.commit()
            print('[migrate] Added column xhs_posts.weekday')
            columns.add('weekday')

        if 'weekday' in columns and 'post_date' in columns:
            db.session.execute(text("""
                UPDATE xhs_posts SET weekday = CASE DAYOFWEEK(post_date)
                    WHEN 2 THEN 'mon' WHEN 3 THEN 'tue' WHEN 4 THEN 'wed'
                    WHEN 5 THEN 'thu' WHEN 6 THEN 'fri' WHEN 7 THEN 'sat'
                    WHEN 1 THEN 'sun'
                END
                WHERE weekday IS NULL AND post_date IS NOT NULL
            """))
            db.session.execute(text(
                "UPDATE xhs_posts SET weekday = 'mon' WHERE weekday IS NULL"
            ))
            db.session.commit()
            print('[migrate] Backfilled xhs_posts.weekday from post_date')

            db.session.execute(text("""
                DELETE t1 FROM xhs_posts t1
                INNER JOIN xhs_posts t2
                  ON t1.weekday = t2.weekday
                 AND t1.student = t2.student
                 AND t1.period = t2.period
                 AND t1.id < t2.id
            """))
            db.session.commit()
            print('[migrate] Deduped xhs_posts by weekday/student/period')

        if 'weekday' in columns:
            db.session.execute(text(
                "ALTER TABLE xhs_posts MODIFY COLUMN weekday varchar(10) NOT NULL"
            ))
            db.session.commit()

        if 'post_date' in columns:
            db.session.execute(text(
                "ALTER TABLE xhs_posts MODIFY COLUMN post_date date NULL "
                "COMMENT '遗留字段，不再作为业务维度'"
            ))
            db.session.commit()
            print('[migrate] Made xhs_posts.post_date nullable')

        inspector = inspect(db.engine)

        if _index_exists(inspector, 'xhs_posts', 'uq_date_student_period'):
            db.session.execute(text(
                "ALTER TABLE xhs_posts DROP INDEX uq_date_student_period"
            ))
            db.session.commit()
            print('[migrate] Dropped old index uq_date_student_period')

        inspector = inspect(db.engine)
        if not _index_exists(inspector, 'xhs_posts', 'uq_weekday_student_period'):
            db.session.execute(text(
                "ALTER TABLE xhs_posts "
                "ADD UNIQUE KEY uq_weekday_student_period (weekday, student, period)"
            ))
            db.session.commit()
            print('[migrate] Added index uq_weekday_student_period')

    except Exception as e:
        db.session.rollback()
        print(f'[migrate] xhs_posts schema check failed: {e}')


def ensure_app_settings_schema(db):
    """确保 app_settings 表存在并写入默认提交密码。"""
    try:
        from app.utils.app_settings import ensure_default_xhs_submit_password
        inspector = inspect(db.engine)
        if 'app_settings' not in inspector.get_table_names():
            db.create_all()
        ensure_default_xhs_submit_password()
    except Exception as e:
        db.session.rollback()
        print(f'[migrate] app_settings check failed: {e}')
