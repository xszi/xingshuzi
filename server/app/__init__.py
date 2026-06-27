import os
from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config.config import Config

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # 确保上传目录存在
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Initialize extensions
    db.init_app(app)
    
    # CORS configuration - allow all origins and necessary headers
    CORS(app, resources={
        r"/api/*": {
            "origins": "*",
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "expose_headers": ["Content-Type", "Authorization"],
            "supports_credentials": False
        },
        # 配图跨域 fetch / 分享保存需要
        r"/uploads/*": {
            "origins": "*",
            "methods": ["GET", "OPTIONS"],
            "allow_headers": ["Content-Type"],
            "expose_headers": ["Content-Type"],
            "supports_credentials": False
        }
    })
    
    jwt.init_app(app)

    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.home import home_bp
    from app.routes.courses import courses_bp
    from app.routes.music import music_bp
    from app.routes.books import books_bp
    from app.routes.products import products_bp
    from app.routes.xhs_posts import xhs_posts_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(home_bp, url_prefix='/api/home')
    app.register_blueprint(courses_bp, url_prefix='/api/courses')
    app.register_blueprint(music_bp, url_prefix='/api/music')
    app.register_blueprint(books_bp, url_prefix='/api/books')
    app.register_blueprint(products_bp, url_prefix='/api/products')
    app.register_blueprint(xhs_posts_bp, url_prefix='/api/xhs-posts')

    # 提供上传文件的访问：/uploads/<path>
    @app.route('/uploads/<path:filename>')
    def serve_upload(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    return app

