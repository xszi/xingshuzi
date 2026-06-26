from run import app
from app.models.user import User
from flask_jwt_extended import create_access_token, decode_token

with app.app_context():
    # 获取 admin 用户
    admin = User.query.filter_by(username='admin').first()
    
    if admin:
        print(f"User found: {admin.username}, ID: {admin.id}")
        
        # 生成 token (convert to string)
        token = create_access_token(identity=str(admin.id))
        print(f"\nGenerated Token:\n{token}\n")
        
        # 尝试解码 token
        try:
            decoded = decode_token(token)
            print(f"Token decoded successfully!")
            print(f"Subject (user_id): {decoded.get('sub')}")
            print(f"Token type: {decoded.get('type')}")
        except Exception as e:
            print(f"Error decoding token: {e}")
    else:
        print("Admin user not found!")

