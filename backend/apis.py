from flask import request, jsonify, make_response
from flask_restful import Resource, Api
from models import db, User, Trek, Booking
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity , verify_jwt_in_request, get_jwt  
from functools import wraps

api = Api(prefix='/api')

def admin_required(f):
    @wraps(f)
    @jwt_required()
    def decorated(*args, **kwargs):
        id= get_jwt_identity()
        user = User.query.filter_by(id=id).first()
        if user.role != 'admin':
            return make_response(jsonify({'message': 'You are not authorized to access this resource'}), 401)
        return f(*args, **kwargs)
    return decorated

def user_required(f):
    @wraps(f)
    @jwt_required()
    def decorated(*args, **kwargs):
        id= get_jwt_identity()
        user = User.query.filter_by(id=id).first()
        if user.role != 'user':
            return make_response(jsonify({'message': 'You are not authorized to access this resource'}), 401)
        return f(*args, **kwargs)
    return decorated

def staff_required(f):
    @wraps(f)
    @jwt_required()
    def decorated(*args, **kwargs):
        id= get_jwt_identity()
        user = User.query.filter_by(id=id).first()
        if user.role != 'staff':
            return make_response(jsonify({'message': 'You are not authorized to access this resource'}), 401)
        return f(*args, **kwargs)
    return decorated



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
            if user.is_blacklisted:
                result={'message': 'Your account has been blacklisted Please contatct support at support@trekcentral.com'}
                return make_response(jsonify(result),400)
            access_token = create_access_token(identity=str(user.id), additional_claims={'role': user.role})
            result={'message': 'Logged in successfulyy' , 'access_token': access_token, 'user': user.get_user(), 'role': user.role}
            return make_response(jsonify(result),200)
        else:
            result={'message': 'Invalid Password'}
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
            return make_response(jsonify({'message': 'Please provide all the required fields'}), 400)
        if password != cpassword:
            return make_response(jsonify({'message': 'Passwords do not match'}), 400)
        if len(password) < 6:
            return make_response(jsonify({'message': 'Password must be at least 6 characters long'}), 400)
        if not '.' in email or not '@' in email:
            return make_response(jsonify({'message': 'Invalid email'}), 400)
        user = User.query.filter_by(email=email).first()
        if user:
            return make_response(jsonify({'message': 'User already exists'}), 400)
        user = User.query.filter_by(phone=phone).first()
        if user:
            return make_response(jsonify({'message': 'User with this Phone number already exists'}), 400)
        
        user = User(email=email, phone=phone, passhash=generate_password_hash(password), fullname=fullname)
        db.session.add(user)
        db.session.commit()
        return make_response(jsonify({'message': 'User created successfully'}), 201)
api.add_resource(RegisterApi, '/register')

class AdminDashboard(Resource):
    @admin_required
    def get(self):
        id= get_jwt_identity()
        user = User.query.filter_by(id=id).first()
        if user.role != 'admin':
            return make_response(jsonify({'message': 'You are not authorized to access this resource'}), 401)
        name=user.fullname
        user_count=User.query.filter_by(role='user').count()
        staff_count=User.query.filter_by(role='staff').count()
        treks=Trek.query.count()
        bookings=Booking.query.count()
        
        return make_response(jsonify({'name': name, 'user_count': user_count, 'staff_count': staff_count, 'treks': treks, 'bookings': bookings}), 200)

api.add_resource(AdminDashboard, '/admin')


class UserAPI(Resource):
    @admin_required
    def get(self):
        user = User.query.filter_by(role='user').all()
        response = []
        for u in user:
            response.append(u.get_user())
        return make_response(jsonify(response), 200)
api.add_resource(UserAPI, '/users')

class StaffAPI(Resource):
    @admin_required
    def get(self):
        user = User.query.filter_by(role='staff').all()
        response = []
        for u in user:
            if u.role == 'staff':
                response.append(u.get_user())
        return make_response(jsonify(response), 200)
    @admin_required
    def post(self):
        data = request.get_json()
        email = data['email']
        password = data['password']
        cpassword = data['cpassword']
        fullname = data['fullname']
        phone = data['phone']
        if not data or not email or not password or not fullname or not phone or not cpassword:
            return make_response(jsonify({'message': 'Please provide all the required fields'}), 400)
        if password != cpassword:
            return make_response(jsonify({'message': 'Passwords do not match'}), 400)
        if len(password) < 6:
            return make_response(jsonify({'message': 'Password must be at least 6 characters long'}), 400)
        if not '.' in email or not '@' in email:
            return make_response(jsonify({'message': 'Invalid email'}), 400)
        user = User.query.filter_by(email=email).first()
        if user:
            return make_response(jsonify({'message': 'User already exists with this email'}), 400)
        user = User.query.filter_by(phone=phone).first()
        if user:
            return make_response(jsonify({'message': 'User with This Phone number already exists'}), 400)
        user = User(email=email, phone=phone, passhash=generate_password_hash(password), fullname=fullname, role='staff')
        db.session.add(user)
        db.session.commit()
        return make_response(jsonify({'message': 'Staff created successfully'}), 201)
api.add_resource(StaffAPI, '/staff')