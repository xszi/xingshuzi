from app import db
from datetime import datetime

class Book(db.Model):
    __tablename__ = 'books'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100))
    category = db.Column(db.String(50))
    description = db.Column(db.Text)
    cover_image = db.Column(db.String(255))
    price = db.Column(db.Numeric(10, 2))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'category': self.category,
            'description': self.description,
            'cover_image': self.cover_image,
            'price': float(self.price) if self.price else 0,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }


