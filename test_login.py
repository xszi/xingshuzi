from run import app, db
from app.models.user import User

with app.app_context():
    admin = User.query.filter_by(username='admin').first()
    
    if admin:
        print(f'User found: {admin.username}')
        print(f'Email: {admin.email}')
        print(f'Role: {admin.role}')
        print(f'Password hash exists: {len(admin.password_hash) > 0}')
        print(f'Password hash: {admin.password_hash[:60]}...')
        
        # Test password verification
        test_passwords = ['admin123', 'Admin123', 'ADMIN123', 'admin']
        for pwd in test_passwords:
            result = admin.check_password(pwd)
            print(f'Testing password "{pwd}": {result}')
    else:
        print('Admin user not found!')


