from app import db

class HomeBanner(db.Model):
    __tablename__ = 'home_banners'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    image = db.Column(db.String(500))  # 匹配数据库字段名
    link = db.Column(db.String(500))   # 匹配数据库字段名
    sort_order = db.Column(db.Integer, default=0)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'image_url': self.image,  # 返回给前端时使用image_url
            'link_url': self.link,    # 返回给前端时使用link_url
            'sort_order': self.sort_order
        }


