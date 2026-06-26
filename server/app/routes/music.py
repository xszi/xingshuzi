from flask import Blueprint, jsonify, request
from app import db
from app.models.music import MusicAlbum
from app.utils.auth import admin_required
from datetime import datetime

music_bp = Blueprint('music', __name__)

@music_bp.route('/albums', methods=['GET'])
def get_music_albums():
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)
    
    albums = MusicAlbum.query.paginate(page=page, per_page=limit, error_out=False)
    
    return jsonify({
        'code': 200,
        'msg': 'success',
        'data': {
            'list': [album.to_dict() for album in albums.items],
            'total': albums.total,
            'page': page,
            'limit': limit
        }
    })

# Admin CRUD endpoints
@music_bp.route('/admin/list', methods=['GET'])
@admin_required
def admin_get_all_albums():
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)
    
    albums = MusicAlbum.query.order_by(MusicAlbum.created_at.desc())\
        .paginate(page=page, per_page=limit, error_out=False)
    
    return jsonify({
        'code': 200,
        'msg': 'success',
        'data': {
            'list': [album.to_dict() for album in albums.items],
            'total': albums.total,
            'page': page,
            'limit': limit
        }
    })

@music_bp.route('/admin', methods=['POST'])
@admin_required
def admin_create_album():
    data = request.get_json()
    
    if not data or not data.get('title'):
        return jsonify({
            'code': 400,
            'msg': 'Title is required'
        }), 400
    
    album = MusicAlbum(
        title=data['title'],
        artist=data.get('artist'),
        description=data.get('description'),
        cover_image=data.get('cover_image'),
        release_date=datetime.strptime(data['release_date'], '%Y-%m-%d').date() if data.get('release_date') else None
    )
    
    db.session.add(album)
    db.session.commit()
    
    return jsonify({
        'code': 200,
        'msg': 'Album created successfully',
        'data': album.to_dict()
    })

@music_bp.route('/admin/<int:album_id>', methods=['GET'])
@admin_required
def admin_get_album(album_id):
    album = MusicAlbum.query.get(album_id)
    
    if not album:
        return jsonify({
            'code': 404,
            'msg': 'Album not found'
        }), 404
    
    return jsonify({
        'code': 200,
        'msg': 'success',
        'data': album.to_dict()
    })

@music_bp.route('/admin/<int:album_id>', methods=['PUT'])
@admin_required
def admin_update_album(album_id):
    album = MusicAlbum.query.get(album_id)
    
    if not album:
        return jsonify({
            'code': 404,
            'msg': 'Album not found'
        }), 404
    
    data = request.get_json()
    
    if data.get('title'):
        album.title = data['title']
    if data.get('artist') is not None:
        album.artist = data['artist']
    if data.get('description') is not None:
        album.description = data['description']
    if data.get('cover_image') is not None:
        album.cover_image = data['cover_image']
    if data.get('release_date'):
        album.release_date = datetime.strptime(data['release_date'], '%Y-%m-%d').date()
    
    db.session.commit()
    
    return jsonify({
        'code': 200,
        'msg': 'Album updated successfully',
        'data': album.to_dict()
    })

@music_bp.route('/admin/<int:album_id>', methods=['DELETE'])
@admin_required
def admin_delete_album(album_id):
    album = MusicAlbum.query.get(album_id)
    
    if not album:
        return jsonify({
            'code': 404,
            'msg': 'Album not found'
        }), 404
    
    db.session.delete(album)
    db.session.commit()
    
    return jsonify({
        'code': 200,
        'msg': 'Album deleted successfully'
    })

