from flask import request, jsonify, make_response
from flask_restful import Resource, Api
from models import db, User, Trek, Booking
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity , verify_jwt_in_request, get_jwt  

api = Api(prefix='/api')


class LoginApi(Resource):
    def post(self):
        data=request.get_json()
        email = data.get('email')
        password=data.get('password')
        user=User.query.filter_by(email=email).first()
        if not user:
            result={'error': 'Invalid User'}
            return make_response(jsonify(result),400)
        
        if user and check_password_hash(user.passhash, password):
            if user.is_blacklisted:
                result={'error': 'Your account has been blacklisted Please contatct support at support@trekcentral.com'}
                return make_response(jsonify(result),400)
            access_token = create_access_token(identity=str(user.id), additional_claims={'role': user.role})
            result={'message': 'Logged in successfulyy' , 'access_token': access_token, 'user': user.get_user()}
            return make_response(jsonify(result),200)
        else:
            result={'error': 'Invalid Password'}
            return make_response(jsonify(result),400)
        
api.add_resource(LoginApi, '/login')

class RegisterApi(Resource):
    def post(self):
        data=request.get_json()
        email = data.get('email')
        password=data.get('password')
        cpassword=data.get('cpassword')
        fullname = data.get('fullname')
        phone = data.get('phone')
        if not data or not email or not password or not cpassword or not fullname or not phone:
            return make_response(jsonify({'error': 'Please provide all the required fields'}), 400)
        if password != cpassword:
            return make_response(jsonify({'error': 'Passwords do not match'}), 400)
        if len(password) < 6:
            return make_response(jsonify({'error': 'Password must be at least 6 characters long'}), 400)
        if not '.' in email or not '@' in email:
            return make_response(jsonify({'error': 'Invalid email'}), 400)
        user = User.query.filter_by(email=email).first()
        if user:
            return make_response(jsonify({'error': 'User already exists'}), 400)
        user = User.query.filter_by(phone=phone).first()
        if user:
            return make_response(jsonify({'error': 'User with this Phone number already exists'}), 400)
        
        user = User(email=email, phone=phone, passhash=generate_password_hash(password), fullname=fullname)
        db.session.add(user)
        db.session.commit()
        return make_response(jsonify({'message': 'User created successfully'}), 201)
api.add_resource(RegisterApi, '/register')


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
api.add_resource(UserAPI, '/users')
