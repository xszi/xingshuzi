import os
import json
import uuid
from datetime import datetime
from flask import Blueprint, jsonify, request, current_app
from werkzeug.utils import secure_filename
from app import db
from app.models.xhs_post import XhsPost, PERIODS, STUDENTS, PRODUCTS, WEEKDAYS
from app.utils.auth import admin_required, xhs_submit_auth
from app.utils.uploads import build_upload_url, normalize_upload_url

xhs_posts_bp = Blueprint('xhs_posts', __name__)


def _allowed_image(filename):
    if '.' not in filename:
        return False
    ext = filename.rsplit('.', 1)[1].lower()
    return ext in current_app.config['ALLOWED_IMAGE_EXTENSIONS']


def _parse_weekday(value):
    if value in WEEKDAYS:
        return value
    return None


@xhs_posts_bp.route('/upload', methods=['POST'])
@xhs_submit_auth
def upload_image():
    """上传单张配图，返回可访问的图片 URL。"""
    if 'file' not in request.files:
        return jsonify({'code': 400, 'msg': '未找到上传文件'}), 400

    file = request.files['file']
    if not file or file.filename == '':
        return jsonify({'code': 400, 'msg': '文件名为空'}), 400

    if not _allowed_image(file.filename):
        allowed = ', '.join(sorted(current_app.config['ALLOWED_IMAGE_EXTENSIONS']))
        return jsonify({'code': 400, 'msg': f'不支持的图片格式，仅支持: {allowed}'}), 400

    ext = file.filename.rsplit('.', 1)[1].lower()
    filename = f'{uuid.uuid4().hex}.{ext}'

    sub_dir = 'xhs'
    save_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], sub_dir)
    os.makedirs(save_dir, exist_ok=True)
    file.save(os.path.join(save_dir, secure_filename(filename)))

    rel_path = f'{sub_dir}/{filename}'
    base_url = current_app.config.get('PUBLIC_BASE_URL', '')
    url = build_upload_url(base_url, rel_path)

    return jsonify({'code': 200, 'msg': '上传成功', 'data': {'url': url}})


@xhs_posts_bp.route('', methods=['GET'])
def get_posts_by_weekday():
    """获取某个星期全部时段的发布内容。

    查询参数: weekday=mon|tue|...|sun
    """
    weekday = _parse_weekday(request.args.get('weekday', '').strip().lower())
    if not weekday:
        return jsonify({'code': 400, 'msg': f'weekday 无效，需为 {list(WEEKDAYS)} 之一'}), 400

    posts = XhsPost.query.filter_by(weekday=weekday).all()
    return jsonify({
        'code': 200,
        'msg': 'success',
        'data': [post.to_dict() for post in posts]
    })


@xhs_posts_bp.route('/weekdays', methods=['GET'])
def get_marked_weekdays():
    """返回已有发布内容的星期列表（用于打点）。"""
    rows = (
        XhsPost.query
        .with_entities(XhsPost.weekday)
        .distinct()
        .all()
    )
    weekdays = sorted(
        (d[0] for d in rows if d[0] in WEEKDAYS),
        key=lambda w: WEEKDAYS.index(w)
    )
    return jsonify({'code': 200, 'msg': 'success', 'data': {'weekdays': weekdays}})


@xhs_posts_bp.route('/month', methods=['GET'])
def get_marked_days():
    """兼容旧接口：按月查日期已废弃，返回空列表。"""
    return jsonify({'code': 200, 'msg': 'success', 'data': {'dates': []}})


@xhs_posts_bp.route('', methods=['POST'])
@xhs_submit_auth
def save_post():
    """保存某个星期某位同学某时段的发布内容。

    请求体: { weekday, student, period, poster_text, title, images, content, products }
    """
    data = request.get_json() or {}

    weekday = _parse_weekday(str(data.get('weekday', '')).strip().lower())
    if not weekday:
        return jsonify({'code': 400, 'msg': f'weekday 无效，需为 {list(WEEKDAYS)} 之一'}), 400

    student = data.get('student', 'a')
    if student not in STUDENTS:
        return jsonify({'code': 400, 'msg': f'student 无效，需为 {list(STUDENTS)} 之一'}), 400

    period = data.get('period')
    if period not in PERIODS:
        return jsonify({'code': 400, 'msg': f'period 无效，需为 {list(PERIODS)} 之一'}), 400

    images = data.get('images', [])
    if not isinstance(images, list):
        images = [images] if images else []
    base_url = current_app.config.get('PUBLIC_BASE_URL', '')
    images = [normalize_upload_url(u, base_url) for u in images]
    images_json = json.dumps(images, ensure_ascii=False)

    products = data.get('products', [])
    if not isinstance(products, list):
        products = [products] if products else []
    products = [p for p in PRODUCTS if p in products]
    raw_products = data.get('products', [])
    if isinstance(raw_products, list) and raw_products:
        invalid = [p for p in raw_products if p not in PRODUCTS]
        if invalid:
            return jsonify({'code': 400, 'msg': f'所挂商品包含无效项: {invalid}'}), 400
    products_json = json.dumps(products, ensure_ascii=False)

    post = XhsPost.query.filter_by(
        weekday=weekday, student=student, period=period
    ).first()
    if post is None:
        post = XhsPost(weekday=weekday, student=student, period=period)
        db.session.add(post)

    post.poster_text = (data.get('poster_text') or '').strip()
    post.title = (data.get('title') or '').strip()
    post.images = images_json
    post.content = (data.get('content') or '').strip()
    post.product = products_json

    db.session.commit()

    return jsonify({
        'code': 200,
        'msg': '保存成功',
        'data': post.to_dict()
    })


@xhs_posts_bp.route('/<int:post_id>', methods=['DELETE'])
@admin_required
def delete_post(post_id):
    """删除某条发布内容"""
    post = XhsPost.query.get(post_id)
    if not post:
        return jsonify({'code': 404, 'msg': '内容不存在'}), 404

    db.session.delete(post)
    db.session.commit()
    return jsonify({'code': 200, 'msg': '删除成功'})


@xhs_posts_bp.route('/submit-password', methods=['PUT'])
@admin_required
def change_submit_password():
    """修改小红书提交密码（仅管理员）。"""
    from app.utils.app_settings import set_xhs_submit_password

    data = request.get_json() or {}
    new_password = (data.get('new_password') or '').strip()

    if len(new_password) < 4:
        return jsonify({'code': 400, 'msg': '新提交密码至少 4 位'}), 400

    set_xhs_submit_password(new_password)
    return jsonify({'code': 200, 'msg': '提交密码已更新'})
