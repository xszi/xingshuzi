"""应用级配置读写（存数据库，启动时自动建表与默认值）。"""

from typing import Optional
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models.app_setting import AppSetting

XHS_SUBMIT_PASSWORD_KEY = 'xhs_submit_password_hash'
DEFAULT_XHS_SUBMIT_PASSWORD = '204417'
_HASH_METHOD = 'pbkdf2:sha256'


def _hash_password(plain: str) -> str:
    return generate_password_hash(plain, method=_HASH_METHOD)


def get_xhs_submit_password_hash() -> Optional[str]:
    row = AppSetting.query.get(XHS_SUBMIT_PASSWORD_KEY)
    return row.value if row else None


def set_xhs_submit_password(plain: str) -> None:
    hashed = _hash_password(plain)
    row = AppSetting.query.get(XHS_SUBMIT_PASSWORD_KEY)
    if row is None:
        row = AppSetting(key=XHS_SUBMIT_PASSWORD_KEY, value=hashed)
        db.session.add(row)
    else:
        row.value = hashed
    db.session.commit()


def check_xhs_submit_password(plain: str) -> bool:
    if not plain:
        return False
    hashed = get_xhs_submit_password_hash()
    if not hashed:
        return plain == DEFAULT_XHS_SUBMIT_PASSWORD
    return check_password_hash(hashed, plain)


def ensure_default_xhs_submit_password() -> None:
    """首次部署写入默认提交密码。"""
    if AppSetting.query.get(XHS_SUBMIT_PASSWORD_KEY) is None:
        row = AppSetting(
            key=XHS_SUBMIT_PASSWORD_KEY,
            value=_hash_password(DEFAULT_XHS_SUBMIT_PASSWORD)
        )
        db.session.add(row)
        db.session.commit()
        print('[migrate] Seeded default xhs submit password')
