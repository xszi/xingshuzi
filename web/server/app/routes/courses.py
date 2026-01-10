from flask import Blueprint, jsonify, request
from app import db
from app.models.course import Course
from app.utils.auth import admin_required

courses_bp = Blueprint('courses', __name__)

@courses_bp.route('/programming', methods=['GET'])
def get_programming_courses():
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)
    
    courses = Course.query.filter_by(category='programming')\
        .paginate(page=page, per_page=limit, error_out=False)
    
    return jsonify({
        'code': 200,
        'msg': 'success',
        'data': {
            'list': [course.to_dict() for course in courses.items],
            'total': courses.total,
            'page': page,
            'limit': limit
        }
    })

@courses_bp.route('/music', methods=['GET'])
def get_music_courses():
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)
    
    courses = Course.query.filter_by(category='music')\
        .paginate(page=page, per_page=limit, error_out=False)
    
    return jsonify({
        'code': 200,
        'msg': 'success',
        'data': {
            'list': [course.to_dict() for course in courses.items],
            'total': courses.total,
            'page': page,
            'limit': limit
        }
    })

# Admin CRUD endpoints
@courses_bp.route('/admin/list', methods=['GET'])
@admin_required
def admin_get_all_courses():
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)
    category = request.args.get('category')
    
    query = Course.query
    if category:
        query = query.filter_by(category=category)
    
    courses = query.order_by(Course.created_at.desc())\
        .paginate(page=page, per_page=limit, error_out=False)
    
    return jsonify({
        'code': 200,
        'msg': 'success',
        'data': {
            'list': [course.to_dict() for course in courses.items],
            'total': courses.total,
            'page': page,
            'limit': limit
        }
    })

@courses_bp.route('/admin', methods=['POST'])
@admin_required
def admin_create_course():
    data = request.get_json()
    
    if not data or not data.get('title'):
        return jsonify({
            'code': 400,
            'msg': 'Title is required'
        }), 400
    
    course = Course(
        title=data['title'],
        description=data.get('description'),
        category=data.get('category', 'programming'),
        cover_image=data.get('cover_image'),
        price=data.get('price', 0)
    )
    
    db.session.add(course)
    db.session.commit()
    
    return jsonify({
        'code': 200,
        'msg': 'Course created successfully',
        'data': course.to_dict()
    })

@courses_bp.route('/admin/<int:course_id>', methods=['GET'])
@admin_required
def admin_get_course(course_id):
    course = Course.query.get(course_id)
    
    if not course:
        return jsonify({
            'code': 404,
            'msg': 'Course not found'
        }), 404
    
    return jsonify({
        'code': 200,
        'msg': 'success',
        'data': course.to_dict()
    })

@courses_bp.route('/admin/<int:course_id>', methods=['PUT'])
@admin_required
def admin_update_course(course_id):
    course = Course.query.get(course_id)
    
    if not course:
        return jsonify({
            'code': 404,
            'msg': 'Course not found'
        }), 404
    
    data = request.get_json()
    
    if data.get('title'):
        course.title = data['title']
    if data.get('description') is not None:
        course.description = data['description']
    if data.get('category'):
        course.category = data['category']
    if data.get('cover_image') is not None:
        course.cover_image = data['cover_image']
    if data.get('price') is not None:
        course.price = data['price']
    
    db.session.commit()
    
    return jsonify({
        'code': 200,
        'msg': 'Course updated successfully',
        'data': course.to_dict()
    })

@courses_bp.route('/admin/<int:course_id>', methods=['DELETE'])
@admin_required
def admin_delete_course(course_id):
    course = Course.query.get(course_id)
    
    if not course:
        return jsonify({
            'code': 404,
            'msg': 'Course not found'
        }), 404
    
    db.session.delete(course)
    db.session.commit()
    
    return jsonify({
        'code': 200,
        'msg': 'Course deleted successfully'
    })

