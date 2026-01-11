from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column('password', db.String(255), nullable=False)  # 匹配数据库字段名
    email = db.Column(db.String(100))
    role = db.Column(db.String(20), default='user')  # 'user' or 'admin'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password_text):
        # Use pbkdf2:sha256 instead of scrypt for compatibility with Python 3.9.6
        self.password = generate_password_hash(password_text, method='pbkdf2:sha256')
    
    def check_password(self, password_text):
        return check_password_hash(self.password, password_text)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }


