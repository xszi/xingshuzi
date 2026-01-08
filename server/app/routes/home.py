from flask import Blueprint, jsonify, request
from app import db
from app.models.home import HomeBanner
from app.utils.auth import admin_required

home_bp = Blueprint('home', __name__)

@home_bp.route('/banners', methods=['GET'])
def get_banners():
    banners = HomeBanner.query.order_by(HomeBanner.sort_order).all()
    return jsonify({
        'code': 200,
        'msg': 'success',
        'data': [banner.to_dict() for banner in banners]
    })

@home_bp.route('/featured', methods=['GET'])
def get_featured():
    # Placeholder for featured content on home page
    return jsonify({
        'code': 200,
        'msg': 'success',
        'data': {
            'courses': [],
            'books': [],
            'products': []
        }
    })

# Admin CRUD endpoints for banners
@home_bp.route('/admin/banners', methods=['GET'])
@admin_required
def admin_get_all_banners():
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)
    
    banners = HomeBanner.query.order_by(HomeBanner.sort_order)\
        .paginate(page=page, per_page=limit, error_out=False)
    
    return jsonify({
        'code': 200,
        'msg': 'success',
        'data': {
            'list': [banner.to_dict() for banner in banners.items],
            'total': banners.total,
            'page': page,
            'limit': limit
        }
    })

@home_bp.route('/admin/banners', methods=['POST'])
@admin_required
def admin_create_banner():
    data = request.get_json()
    
    if not data or not data.get('title'):
        return jsonify({
            'code': 400,
            'msg': 'Title is required'
        }), 400
    
    banner = HomeBanner(
        title=data['title'],
        image_url=data.get('image_url'),
        link_url=data.get('link_url'),
        sort_order=data.get('sort_order', 0)
    )
    
    db.session.add(banner)
    db.session.commit()
    
    return jsonify({
        'code': 200,
        'msg': 'Banner created successfully',
        'data': banner.to_dict()
    })

@home_bp.route('/admin/banners/<int:banner_id>', methods=['GET'])
@admin_required
def admin_get_banner(banner_id):
    banner = HomeBanner.query.get(banner_id)
    
    if not banner:
        return jsonify({
            'code': 404,
            'msg': 'Banner not found'
        }), 404
    
    return jsonify({
        'code': 200,
        'msg': 'success',
        'data': banner.to_dict()
    })

@home_bp.route('/admin/banners/<int:banner_id>', methods=['PUT'])
@admin_required
def admin_update_banner(banner_id):
    banner = HomeBanner.query.get(banner_id)
    
    if not banner:
        return jsonify({
            'code': 404,
            'msg': 'Banner not found'
        }), 404
    
    data = request.get_json()
    
    if data.get('title'):
        banner.title = data['title']
    if data.get('image_url') is not None:
        banner.image_url = data['image_url']
    if data.get('link_url') is not None:
        banner.link_url = data['link_url']
    if data.get('sort_order') is not None:
        banner.sort_order = data['sort_order']
    
    db.session.commit()
    
    return jsonify({
        'code': 200,
        'msg': 'Banner updated successfully',
        'data': banner.to_dict()
    })

@home_bp.route('/admin/banners/<int:banner_id>', methods=['DELETE'])
@admin_required
def admin_delete_banner(banner_id):
    banner = HomeBanner.query.get(banner_id)
    
    if not banner:
        return jsonify({
            'code': 404,
            'msg': 'Banner not found'
        }), 404
    
    db.session.delete(banner)
    db.session.commit()
    
    return jsonify({
        'code': 200,
        'msg': 'Banner deleted successfully'
    })

