import os
import json
import uuid
from datetime import datetime
from flask import Blueprint, jsonify, request, current_app
from werkzeug.utils import secure_filename
from app import db
from app.models.xhs_post import XhsPost, PERIODS, STUDENTS, PRODUCTS
from app.utils.auth import admin_required
from app.utils.uploads import build_upload_url, normalize_upload_url

xhs_posts_bp = Blueprint('xhs_posts', __name__)


def _allowed_image(filename):
    if '.' not in filename:
        return False
    ext = filename.rsplit('.', 1)[1].lower()
    return ext in current_app.config['ALLOWED_IMAGE_EXTENSIONS']


def _parse_date(date_str):
    """解析 YYYY-MM-DD，失败返回 None"""
    try:
        return datetime.strptime(date_str, '%Y-%m-%d').date()
    except (ValueError, TypeError):
        return None


@xhs_posts_bp.route('/upload', methods=['POST'])
@admin_required
def upload_image():
    """上传单张配图，返回可访问的图片 URL。

    表单字段: file（图片文件）
    返回: { url: 'http://.../uploads/xhs/xxx.jpg' }
    """
    if 'file' not in request.files:
        return jsonify({'code': 400, 'msg': '未找到上传文件'}), 400

    file = request.files['file']
    if not file or file.filename == '':
        return jsonify({'code': 400, 'msg': '文件名为空'}), 400

    if not _allowed_image(file.filename):
        allowed = ', '.join(sorted(current_app.config['ALLOWED_IMAGE_EXTENSIONS']))
        return jsonify({'code': 400, 'msg': f'不支持的图片格式，仅支持: {allowed}'}), 400

    # 生成安全的唯一文件名，保留扩展名
    ext = file.filename.rsplit('.', 1)[1].lower()
    filename = f'{uuid.uuid4().hex}.{ext}'

    # 按 xhs 子目录存放
    sub_dir = 'xhs'
    save_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], sub_dir)
    os.makedirs(save_dir, exist_ok=True)
    file.save(os.path.join(save_dir, secure_filename(filename)))

    # 使用配置的对外地址，避免存成 127.0.0.1
    rel_path = f'{sub_dir}/{filename}'
    base_url = current_app.config.get('PUBLIC_BASE_URL', '')
    url = build_upload_url(base_url, rel_path)

    return jsonify({'code': 200, 'msg': '上传成功', 'data': {'url': url}})


@xhs_posts_bp.route('', methods=['GET'])
def get_posts_by_date():
    """获取某一天四个时段的发布内容。

    查询参数: date=YYYY-MM-DD
    返回: 该日期所有时段的内容列表（已存在的才返回）
    """
    date_str = request.args.get('date')
    post_date = _parse_date(date_str)
    if not post_date:
        return jsonify({'code': 400, 'msg': 'date 参数无效，需为 YYYY-MM-DD 格式'}), 400

    posts = XhsPost.query.filter_by(post_date=post_date).all()
    return jsonify({
        'code': 200,
        'msg': 'success',
        'data': [post.to_dict() for post in posts]
    })


@xhs_posts_bp.route('/month', methods=['GET'])
def get_marked_days():
    """获取某个月份中有发布内容的日期列表，用于日历打点。

    查询参数: month=YYYY-MM
    返回: { dates: ['YYYY-MM-DD', ...] }（去重后的日期）
    """
    month_str = request.args.get('month')
    try:
        first_day = datetime.strptime(month_str + '-01', '%Y-%m-%d').date()
    except (ValueError, TypeError):
        return jsonify({'code': 400, 'msg': 'month 参数无效，需为 YYYY-MM 格式'}), 400

    # 下个月第一天，作为右开区间
    if first_day.month == 12:
        next_month = first_day.replace(year=first_day.year + 1, month=1)
    else:
        next_month = first_day.replace(month=first_day.month + 1)

    rows = (
        XhsPost.query
        .with_entities(XhsPost.post_date)
        .filter(XhsPost.post_date >= first_day, XhsPost.post_date < next_month)
        .distinct()
        .all()
    )
    dates = sorted(d[0].strftime('%Y-%m-%d') for d in rows)
    return jsonify({'code': 200, 'msg': 'success', 'data': {'dates': dates}})


@xhs_posts_bp.route('', methods=['POST'])
@admin_required
def save_post():
    """保存某一天某位同学某时段的发布内容（不存在则新建，存在则更新）。

    请求体: { date, student, period, title, images(数组), content, products(数组) }
    """
    data = request.get_json() or {}

    post_date = _parse_date(data.get('date'))
    if not post_date:
        return jsonify({'code': 400, 'msg': 'date 参数无效，需为 YYYY-MM-DD 格式'}), 400

    # 同学：默认 a，兼容旧请求体不带 student 的情况
    student = data.get('student', 'a')
    if student not in STUDENTS:
        return jsonify({'code': 400, 'msg': f'student 无效，需为 {list(STUDENTS)} 之一'}), 400

    period = data.get('period')
    if period not in PERIODS:
        return jsonify({'code': 400, 'msg': f'period 无效，需为 {list(PERIODS)} 之一'}), 400

    # 配图统一存为 JSON 数组字符串
    images = data.get('images', [])
    if not isinstance(images, list):
        images = [images] if images else []
    base_url = current_app.config.get('PUBLIC_BASE_URL', '')
    images = [normalize_upload_url(u, base_url) for u in images]
    images_json = json.dumps(images, ensure_ascii=False)

    # 所挂商品：多选，至少选一个，且只能是预设的 5 个之一
    products = data.get('products', [])
    if not isinstance(products, list):
        products = [products] if products else []
    # 去重并保持可选项的固定顺序
    products = [p for p in PRODUCTS if p in products]
    if not products:
        return jsonify({'code': 400, 'msg': f'所挂商品至少选一个，需为 {list(PRODUCTS)} 之一'}), 400
    invalid = [p for p in data.get('products', []) if p not in PRODUCTS]
    if invalid:
        return jsonify({'code': 400, 'msg': f'所挂商品包含无效项: {invalid}'}), 400
    products_json = json.dumps(products, ensure_ascii=False)

    post = XhsPost.query.filter_by(
        post_date=post_date, student=student, period=period
    ).first()
    if post is None:
        post = XhsPost(post_date=post_date, student=student, period=period)
        db.session.add(post)

    post.title = data.get('title', '')
    post.images = images_json
    post.content = data.get('content', '')
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
