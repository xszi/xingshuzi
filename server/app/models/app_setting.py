from app import db
from datetime import datetime


class AppSetting(db.Model):
    """键值配置表（如小红书提交密码等）。"""
    __tablename__ = 'app_settings'

    key = db.Column(db.String(64), primary_key=True)
    value = db.Column(db.Text, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
