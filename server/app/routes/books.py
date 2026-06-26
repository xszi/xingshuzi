from flask import Blueprint, jsonify, request
from app import db
from app.models.book import Book
from app.utils.auth import admin_required

books_bp = Blueprint('books', __name__)

@books_bp.route('/list', methods=['GET'])
def get_books():
    category = request.args.get('category')
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)
    
    query = Book.query
    if category:
        query = query.filter_by(category=category)
    
    books = query.paginate(page=page, per_page=limit, error_out=False)
    
    return jsonify({
        'code': 200,
        'msg': 'success',
        'data': {
            'list': [book.to_dict() for book in books.items],
            'total': books.total,
            'page': page,
            'limit': limit
        }
    })

# Admin CRUD endpoints
@books_bp.route('/admin/list', methods=['GET'])
@admin_required
def admin_get_all_books():
    category = request.args.get('category')
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)
    
    query = Book.query
    if category:
        query = query.filter_by(category=category)
    
    books = query.order_by(Book.created_at.desc())\
        .paginate(page=page, per_page=limit, error_out=False)
    
    return jsonify({
        'code': 200,
        'msg': 'success',
        'data': {
            'list': [book.to_dict() for book in books.items],
            'total': books.total,
            'page': page,
            'limit': limit
        }
    })

@books_bp.route('/admin', methods=['POST'])
@admin_required
def admin_create_book():
    data = request.get_json()
    
    if not data or not data.get('title'):
        return jsonify({
            'code': 400,
            'msg': 'Title is required'
        }), 400
    
    book = Book(
        title=data['title'],
        author=data.get('author'),
        category=data.get('category'),
        description=data.get('description'),
        cover_image=data.get('cover_image'),
        price=data.get('price', 0)
    )
    
    db.session.add(book)
    db.session.commit()
    
    return jsonify({
        'code': 200,
        'msg': 'Book created successfully',
        'data': book.to_dict()
    })

@books_bp.route('/admin/<int:book_id>', methods=['GET'])
@admin_required
def admin_get_book(book_id):
    book = Book.query.get(book_id)
    
    if not book:
        return jsonify({
            'code': 404,
            'msg': 'Book not found'
        }), 404
    
    return jsonify({
        'code': 200,
        'msg': 'success',
        'data': book.to_dict()
    })

@books_bp.route('/admin/<int:book_id>', methods=['PUT'])
@admin_required
def admin_update_book(book_id):
    book = Book.query.get(book_id)
    
    if not book:
        return jsonify({
            'code': 404,
            'msg': 'Book not found'
        }), 404
    
    data = request.get_json()
    
    if data.get('title'):
        book.title = data['title']
    if data.get('author') is not None:
        book.author = data['author']
    if data.get('category') is not None:
        book.category = data['category']
    if data.get('description') is not None:
        book.description = data['description']
    if data.get('cover_image') is not None:
        book.cover_image = data['cover_image']
    if data.get('price') is not None:
        book.price = data['price']
    
    db.session.commit()
    
    return jsonify({
        'code': 200,
        'msg': 'Book updated successfully',
        'data': book.to_dict()
    })

@books_bp.route('/admin/<int:book_id>', methods=['DELETE'])
@admin_required
def admin_delete_book(book_id):
    book = Book.query.get(book_id)
    
    if not book:
        return jsonify({
            'code': 404,
            'msg': 'Book not found'
        }), 404
    
    db.session.delete(book)
    db.session.commit()
    
    return jsonify({
        'code': 200,
        'msg': 'Book deleted successfully'
    })

