from flask import Flask
from models import db, User
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
db.init_app(app)

def create_admin():
    with app.app_context():
        
        
        
        admin = User.query.filter_by(username='admin').first()
        if admin:
            print('Admin user already exists!')
            return

        admin = User(
            username='admin',
            email='admin@example.com',
            password=generate_password_hash('admin123'),
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()
        print('Admin user created successfully!')

if __name__ == '__main__':
    create_admin()