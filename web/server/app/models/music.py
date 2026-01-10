from app import db
from datetime import datetime

class MusicAlbum(db.Model):
    __tablename__ = 'music_albums'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    artist = db.Column(db.String(100))
    description = db.Column(db.Text)
    cover_image = db.Column(db.String(255))
    release_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'artist': self.artist,
            'description': self.description,
            'cover_image': self.cover_image,
            'release_date': self.release_date.strftime('%Y-%m-%d') if self.release_date else None,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }


