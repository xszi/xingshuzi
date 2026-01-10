from app import db

class HomeBanner(db.Model):
    __tablename__ = 'home_banners'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    image_url = db.Column(db.String(255))
    link_url = db.Column(db.String(255))
    sort_order = db.Column(db.Integer, default=0)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'image_url': self.image_url,
            'link_url': self.link_url,
            'sort_order': self.sort_order
        }


