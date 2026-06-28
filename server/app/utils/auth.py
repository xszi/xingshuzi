from functools import wraps
from flask import jsonify, request
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from app.models.user import User
from app.utils.app_settings import check_xhs_submit_password

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        
        if not user or user.role != 'admin':
            return jsonify({
                'code': 403,
                'msg': 'Admin access required'
            }), 403
        
        return fn(*args, **kwargs)
    return wrapper

def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        return fn(*args, **kwargs)
    return wrapper


def current_request_is_admin():
    """当前请求是否携带有效管理员 JWT。"""
    try:
        verify_jwt_in_request(optional=True)
        user_id = get_jwt_identity()
        if not user_id:
            return False
        user = User.query.get(int(user_id))
        return user is not None and user.role == 'admin'
    except Exception:
        return False


def _extract_submit_password():
    """从 JSON 或 multipart 表单读取提交密码；未传字段返回 None。"""
    if request.is_json:
        data = request.get_json(silent=True) or {}
        if 'submit_password' in data:
            return str(data.get('submit_password') or '')
    if 'submit_password' in request.form:
        return str(request.form.get('submit_password') or '')
    return None


def xhs_submit_auth(fn):
    """小红书写入：携带 submit_password 时仅校验密码；未携带时允许管理员 JWT。"""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        submit_password = _extract_submit_password()

        if submit_password is not None:
            if check_xhs_submit_password(submit_password):
                return fn(*args, **kwargs)
            return jsonify({
                'code': 403,
                'msg': '提交密码错误'
            }), 403

        if current_request_is_admin():
            return fn(*args, **kwargs)

        return jsonify({
            'code': 403,
            'msg': '提交密码错误或缺失'
        }), 403

    return wrapper

