from app import db
from datetime import datetime
from config.config import Config
from app.utils.uploads import normalize_upload_url

# 时段枚举：早 / 中 / 傍晚 / 晚
PERIODS = ('morning', 'noon', 'evening', 'night')

# 同学枚举：A / B / C 三位同学
STUDENTS = ('a', 'b', 'c', 'd')

# 所挂商品可选项（多选，可为空）
PRODUCTS = ('考研', '雅思', '六级', '四级', '小学语法学习纸')


class XhsPost(db.Model):
    """小红书发布内容：每条记录对应某一天某位同学某个时段的一篇内容。

    通过 (post_date, student, period) 唯一约束，
    保证每天每位同学每个时段只有一篇。
    """
    __tablename__ = 'xhs_posts'

    id = db.Column(db.Integer, primary_key=True)
    # 发布日期，格式 YYYY-MM-DD
    post_date = db.Column(db.Date, nullable=False)
    # 账号：a(号1) / b(号2) / c(号3) / d(号4)
    student = db.Column(db.String(10), nullable=False, default='a')
    # 时段：morning(早) / noon(中) / evening(傍晚) / night(晚)
    period = db.Column(db.String(20), nullable=False)
    # 大字报文字（配图上的醒目短句）
    poster_text = db.Column(db.String(200))
    # 标题
    title = db.Column(db.String(200))
    # 配图：多张图片地址，存为 JSON 数组字符串
    images = db.Column(db.Text)
    # 文案
    content = db.Column(db.Text)
    # 所挂商品：可多选，存为 JSON 数组字符串
    product = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint('post_date', 'student', 'period', name='uq_date_student_period'),
    )

    def to_dict(self):
        import json
        try:
            images = json.loads(self.images) if self.images else []
        except (ValueError, TypeError):
            images = []

        # 所挂商品现为多选，存为 JSON 数组；兼容旧的纯文本单值
        products = []
        if self.product:
            try:
                parsed = json.loads(self.product)
                products = parsed if isinstance(parsed, list) else [parsed]
            except (ValueError, TypeError):
                products = [self.product]

        return {
            'id': self.id,
            'post_date': self.post_date.strftime('%Y-%m-%d') if self.post_date else None,
            'student': self.student or 'a',
            'period': self.period,
            'poster_text': self.poster_text or '',
            'title': self.title or '',
            'images': [
                normalize_upload_url(u, Config.PUBLIC_BASE_URL) for u in images
            ],
            'content': self.content or '',
            'products': products,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None
        }
