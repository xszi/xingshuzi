from app import db

class HomeBanner(db.Model):
    __tablename__ = 'home_banners'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    # 线上 home_banners 表的列名为 image / link
    image_url = db.Column('image', db.String(500))
    link_url = db.Column('link', db.String(500))
    sort_order = db.Column(db.Integer, default=0)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'image_url': self.image_url,
            'link_url': self.link_url,
            'sort_order': self.sort_order
        }


