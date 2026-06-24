from flask import request, jsonify, make_response
from flask_restful import Resource, Api
from models import db, User, Trek, Booking
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

api = Api(prefix='/api')

class UserAPI(Resource):
    def get(self):
        user = User.query.all()
        response = []
        for u in user:
            if u.role != 'admin':
                response.append(
                    {'id': u.id, 
                    'email': u.email, 
                    'phone': u.phone, 
                    'fullname': u.fullname})
        return make_response(jsonify(response), 200)
    
    def post(self):
        data = request.get_json()
        email = data.get('email')
        phone = data.get('phone')
        password = data.get('password')
        fullname = data.get('fullname')
        if not data or not email or not phone or not password or not fullname:
            return make_response(jsonify({'error': 'Please provide all the required fields'}), 400)
        user = User(email=email, phone=phone, passhash=generate_password_hash(password), fullname=fullname)
        db.session.add(user)
        db.session.commit()
        return make_response(jsonify({'message': 'User created successfully'}), 201)
api.add_resource(UserAPI, '/users')

class LoginApi(Resource):
    def post(self):
        data=request.get_json()
        email = data.get('email')
        password=data.get('password')
        user=User.query.filter_by(email=email).first()
        if not user:
            result={'message': 'Invalid User'}
            return make_response(jsonify(result),400)
        
        if user and check_password_hash(user.passhash, password):
            result={'message': 'Logged in successfulyy'}
            return make_response(jsonify(result),200)
        else:
            result={'message': 'Invalid Password'}
            return make_response(jsonify(result),400)
        
api.add_resource(LoginApi, '/login')