from app import create_app, db
import os

app = create_app()

@app.cli.command("init-db")
def init_db():
    """Initialize the database."""
    with app.app_context():
        db.create_all()
        print("Database initialized.")

if __name__ == '__main__':
    # Ensure tables are created (optional, better to use migrations in real projects)
    with app.app_context():
        try:
            db.create_all()
        except Exception as e:
            print(f"Error creating database tables: {e}")
            print("Make sure your MySQL server is running and the database exists.")
    
    # Get configuration from environment
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    port = int(os.getenv('FLASK_PORT', '5000'))
    # debug=True 默认会开启 reloader，改代码时整进程重启；本地开发默认关闭，需热重载时设 FLASK_USE_RELOADER=true
    use_reloader = os.getenv('FLASK_USE_RELOADER', 'false').lower() == 'true'

    app.run(host='0.0.0.0', port=port, debug=debug, use_reloader=use_reloader)


