from app import create_app, db
from app.models.user import User

def init_admin():
    """Initialize admin user"""
    app = create_app()
    with app.app_context():
        # Check if admin exists
        admin = User.query.filter_by(username='admin').first()
        if admin:
            print('Admin user already exists')
            return
        
        # Create admin user
        admin = User(
            username='admin',
            email='admin@xingshuzi.com',
            role='admin'
        )
        admin.set_password('admin123')
        
        db.session.add(admin)
        db.session.commit()
        
        print('Admin user created successfully!')
        print('Username: admin')
        print('Password: admin123')
        print('Please change the password after first login.')

if __name__ == '__main__':
    init_admin()


