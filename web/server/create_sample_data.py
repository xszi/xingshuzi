from app import create_app, db
from app.models.course import Course
from app.models.music import MusicAlbum
from app.models.book import Book
from app.models.product import Product
from app.models.home import HomeBanner
from datetime import date

def create_sample_data():
    """创建示例数据"""
    app = create_app()
    with app.app_context():
        # 清空现有数据（可选，小心使用）
        # db.drop_all()
        # db.create_all()
        
        print("Creating sample data...")
        
        # 创建编程课程
        programming_courses = [
            Course(
                title="Python 零基础入门",
                description="适合没有编程经验的初学者，从零开始学习 Python",
                category="programming",
                cover_image="https://picsum.photos/400/300?random=1",
                price=99.00
            ),
            Course(
                title="Java Web 开发实战",
                description="学习 Spring Boot 框架，开发企业级 Web 应用",
                category="programming",
                cover_image="https://picsum.photos/400/300?random=2",
                price=199.00
            ),
            Course(
                title="前端开发 Vue3 全栈课程",
                description="掌握最新的 Vue3 技术栈，包含项目实战",
                category="programming",
                cover_image="https://picsum.photos/400/300?random=3",
                price=149.00
            )
        ]
        
        # 创建音乐课程
        music_courses = [
            Course(
                title="钢琴入门教程",
                description="零基础学钢琴，从识谱到演奏简单曲目",
                category="music",
                cover_image="https://picsum.photos/400/300?random=4",
                price=299.00
            ),
            Course(
                title="吉他弹唱速成",
                description="30天学会吉他弹唱，适合忙碌的上班族",
                category="music",
                cover_image="https://picsum.photos/400/300?random=5",
                price=199.00
            )
        ]
        
        for course in programming_courses + music_courses:
            db.session.add(course)
        
        # 创建音乐专辑
        albums = [
            MusicAlbum(
                title="夜的钢琴曲",
                artist="石进",
                description="优美舒缓的钢琴音乐，适合夜晚聆听",
                cover_image="https://picsum.photos/400/300?random=6",
                release_date=date(2010, 6, 1)
            ),
            MusicAlbum(
                title="卡农精选集",
                artist="帕赫贝尔",
                description="经典的卡农变奏曲集",
                cover_image="https://picsum.photos/400/300?random=7",
                release_date=date(2015, 3, 15)
            ),
            MusicAlbum(
                title="流行钢琴曲精选",
                artist="Various Artists",
                description="精选最受欢迎的流行歌曲钢琴版",
                cover_image="https://picsum.photos/400/300?random=8",
                release_date=date(2023, 8, 20)
            )
        ]
        
        for album in albums:
            db.session.add(album)
        
        # 创建书籍
        books = [
            Book(
                title="活着",
                author="余华",
                category="文学",
                description="余华代表作，讲述了一个人和他命运的友情",
                cover_image="https://picsum.photos/300/400?random=9",
                price=35.00
            ),
            Book(
                title="三体",
                author="刘慈欣",
                category="科幻",
                description="中国科幻文学的里程碑之作",
                cover_image="https://picsum.photos/300/400?random=10",
                price=29.00
            ),
            Book(
                title="百年孤独",
                author="加西亚·马尔克斯",
                category="文学",
                description="魔幻现实主义的代表作",
                cover_image="https://picsum.photos/300/400?random=11",
                price=45.00
            ),
            Book(
                title="Python编程：从入门到实践",
                author="埃里克·马瑟斯",
                category="技术",
                description="Python编程的最佳入门书籍",
                cover_image="https://picsum.photos/300/400?random=12",
                price=89.00
            ),
            Book(
                title="解忧杂货店",
                author="东野圭吾",
                category="小说",
                description="温暖治愈系的奇幻故事",
                cover_image="https://picsum.photos/300/400?random=13",
                price=39.00
            )
        ]
        
        for book in books:
            db.session.add(book)
        
        # 创建助农产品
        products = [
            Product(
                name="陕西洛川红富士苹果",
                description="来自黄土高原的优质苹果，香甜脆爽",
                category="agriculture",
                origin="陕西洛川",
                price=12.80,
                image_url="https://picsum.photos/400/400?random=14"
            ),
            Product(
                name="新疆阿克苏冰糖心苹果",
                description="独特的冰糖心，甜度极高",
                category="agriculture",
                origin="新疆阿克苏",
                price=15.90,
                image_url="https://picsum.photos/400/400?random=15"
            ),
            Product(
                name="云南褚橙",
                description="励志橙，口感酸甜适中",
                category="agriculture",
                origin="云南玉溪",
                price=9.90,
                image_url="https://picsum.photos/400/400?random=16"
            ),
            Product(
                name="山东烟台大樱桃",
                description="新鲜采摘，个大饱满",
                category="agriculture",
                origin="山东烟台",
                price=68.00,
                image_url="https://picsum.photos/400/400?random=17"
            ),
            Product(
                name="东北黑龙江五常大米",
                description="优质东北大米，米粒饱满",
                category="agriculture",
                origin="黑龙江五常",
                price=6.50,
                image_url="https://picsum.photos/400/400?random=18"
            )
        ]
        
        for product in products:
            db.session.add(product)
        
        # 创建首页轮播图
        banners = [
            HomeBanner(
                title="新春特惠，全场8折",
                image_url="https://picsum.photos/1200/400?random=19",
                link_url="/activity/spring-sale",
                sort_order=1
            ),
            HomeBanner(
                title="精选编程课程，限时免费",
                image_url="https://picsum.photos/1200/400?random=20",
                link_url="/courses/programming",
                sort_order=2
            ),
            HomeBanner(
                title="音乐专辑上新",
                image_url="https://picsum.photos/1200/400?random=21",
                link_url="/music/albums",
                sort_order=3
            )
        ]
        
        for banner in banners:
            db.session.add(banner)
        
        # 提交所有数据
        db.session.commit()
        
        print("Created 5 courses")
        print("Created 3 music albums")
        print("Created 5 books")
        print("Created 5 agriculture products")
        print("Created 3 banners")
        print("\nSample data created successfully!")

if __name__ == '__main__':
    create_sample_data()

