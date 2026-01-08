from flask import Blueprint, jsonify, request
from app import db
from app.models.product import Product
from app.utils.auth import admin_required

products_bp = Blueprint('products', __name__)

@products_bp.route('/agriculture', methods=['GET'])
def get_agriculture_products():
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)
    
    products = Product.query.filter_by(category='agriculture')\
        .paginate(page=page, per_page=limit, error_out=False)
    
    return jsonify({
        'code': 200,
        'msg': 'success',
        'data': {
            'list': [product.to_dict() for product in products.items],
            'total': products.total,
            'page': page,
            'limit': limit
        }
    })

# Admin CRUD endpoints
@products_bp.route('/admin/list', methods=['GET'])
@admin_required
def admin_get_all_products():
    category = request.args.get('category')
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)
    
    query = Product.query
    if category:
        query = query.filter_by(category=category)
    
    products = query.order_by(Product.created_at.desc())\
        .paginate(page=page, per_page=limit, error_out=False)
    
    return jsonify({
        'code': 200,
        'msg': 'success',
        'data': {
            'list': [product.to_dict() for product in products.items],
            'total': products.total,
            'page': page,
            'limit': limit
        }
    })

@products_bp.route('/admin', methods=['POST'])
@admin_required
def admin_create_product():
    data = request.get_json()
    
    if not data or not data.get('name'):
        return jsonify({
            'code': 400,
            'msg': 'Name is required'
        }), 400
    
    product = Product(
        name=data['name'],
        description=data.get('description'),
        category=data.get('category', 'agriculture'),
        origin=data.get('origin'),
        price=data.get('price', 0),
        image_url=data.get('image_url')
    )
    
    db.session.add(product)
    db.session.commit()
    
    return jsonify({
        'code': 200,
        'msg': 'Product created successfully',
        'data': product.to_dict()
    })

@products_bp.route('/admin/<int:product_id>', methods=['GET'])
@admin_required
def admin_get_product(product_id):
    product = Product.query.get(product_id)
    
    if not product:
        return jsonify({
            'code': 404,
            'msg': 'Product not found'
        }), 404
    
    return jsonify({
        'code': 200,
        'msg': 'success',
        'data': product.to_dict()
    })

@products_bp.route('/admin/<int:product_id>', methods=['PUT'])
@admin_required
def admin_update_product(product_id):
    product = Product.query.get(product_id)
    
    if not product:
        return jsonify({
            'code': 404,
            'msg': 'Product not found'
        }), 404
    
    data = request.get_json()
    
    if data.get('name'):
        product.name = data['name']
    if data.get('description') is not None:
        product.description = data['description']
    if data.get('category') is not None:
        product.category = data['category']
    if data.get('origin') is not None:
        product.origin = data['origin']
    if data.get('price') is not None:
        product.price = data['price']
    if data.get('image_url') is not None:
        product.image_url = data['image_url']
    
    db.session.commit()
    
    return jsonify({
        'code': 200,
        'msg': 'Product updated successfully',
        'data': product.to_dict()
    })

@products_bp.route('/admin/<int:product_id>', methods=['DELETE'])
@admin_required
def admin_delete_product(product_id):
    product = Product.query.get(product_id)
    
    if not product:
        return jsonify({
            'code': 404,
            'msg': 'Product not found'
        }), 404
    
    db.session.delete(product)
    db.session.commit()
    
    return jsonify({
        'code': 200,
        'msg': 'Product deleted successfully'
    })

