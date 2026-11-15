from flask import Flask
from config import Config
from models import db, User, Trek, Booking
from werkzeug.security import generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from apis import api , cache
from flask_jwt_extended import JWTManager
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    
    
    with app.app_context():
        db.create_all()
        
        admin=User.query.filter_by(email='admin@gmail.com').first()
        if not admin:
            admin_user = User(email='admin@gmail.com', phone='0000000000', passhash=generate_password_hash('admin123'), fullname='Admin', role='admin')
            db.session.add(admin_user)
            db.session.commit()
    
    return app
app = create_app()
jwt = JWTManager(app)
api.init_app(app)
cache.init_app(app)
    
CORS(app)

if ( __name__ == '__main__'):
    app.run()
    
    