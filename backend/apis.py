from flask import request, jsonify, make_response
from flask_restful import Resource, Api
from models import db, User, Trek, Booking
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity , verify_jwt_in_request, get_jwt  
from functools import wraps
from datetime import datetime

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
            result={'message': 'Logged in successfulyy' , 'access_token': access_token, 'user': user.get_user()}
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
        user_count=User.query.filter_by(role='user').count()
        staff_count=User.query.filter_by(role='staff').count()
        treks=Trek.query.count()
        bookings=Booking.query.count()
        
        return make_response(jsonify({ 'user_count': user_count, 'staff_count': staff_count, 'treks': treks, 'bookings': bookings}), 200)

api.add_resource(AdminDashboard, '/admin')

class AdminTrekAPI(Resource):
    @admin_required
    def get(self , id=None):
        if id:
            trek = Trek.query.filter_by(id=id).first()
            if not trek:
                return make_response(jsonify({'message': 'Trek does not exist'}), 404)
            return make_response(jsonify(trek.get_trek()), 200)
        else:
            trek = Trek.query.all()
            response = []
            for t in trek:
                response.append(t.get_trek())
            return make_response(jsonify(response), 200)
    
    @admin_required
    def post(self):
        data = request.get_json()
        name = data.get('name')
        location = data.get('location')
        difficulty = data.get('difficulty')
        price = data.get('price')
        description = data.get('description')
        available_slots = data.get('available_slots')
        assigned_staff_id = data.get('assigned_staff_id')
        start_date = datetime.strptime(data.get('start_date'), '%Y-%m-%d').date()
        end_date = datetime.strptime(data.get('end_date'), '%Y-%m-%d').date()
        status = data.get('status')
        image_url = data.get('image_url')
        if not data or not name or not location or not difficulty or not price or not available_slots or not start_date or not end_date or not image_url:
            return make_response(jsonify({'message': 'Please provide all the required fields'}), 400)
        if price <= 0:
            return make_response(jsonify({'message': 'Price should be greater than or equal to 0'}), 400)
        if available_slots <= 0:
            return make_response(jsonify({'message': 'Available Slots should be greater than or equal to 0'}), 400)
        if assigned_staff_id and not status:
            return make_response(jsonify({'message': 'You have to select trek status if you have assigned staff'}), 400)
        if not assigned_staff_id and status:
            return make_response(jsonify({'message': 'You can not select trek status if you have not assigned staff'}), 400)
        if not assigned_staff_id:
            assigned_staff_id = None
            status = 'Pending'
        
        if start_date > end_date:
            return make_response(jsonify({'message': 'Start Date should be earlier than End Date'}), 400)
        
        duration = (end_date - start_date).days
        
        
        try:
            trek = Trek(name=name, location=location, difficulty=difficulty, price=price, description=description, available_slots=available_slots, assigned_staff_id=assigned_staff_id, start_date=start_date, end_date=end_date, duration=duration, status=status, image_url=image_url)
            db.session.add(trek)
            db.session.commit()
            return make_response(jsonify({'message': 'Trek created successfully'}), 201)
        except:
            return make_response(jsonify({'message': 'Something went wrong while creating trek'}), 500)
        
    @admin_required
    def put(self,id):
        if not id:
            return make_response(jsonify({'message': 'Please provide a valid id'}), 400)
        data = request.get_json()
        try:
            trek = Trek.query.filter_by(id=id).first()
            if not trek:
                return make_response(jsonify({'message': 'Trek does not exist'}), 404)
        except:
            return make_response(jsonify({'message': 'Something went wrong while updating trek'}), 500)
        id = data.get('id')
        name = data.get('name')
        location = data.get('location')
        difficulty = data.get('difficulty')
        price = data.get('price')
        description = data.get('description')
        available_slots = data.get('available_slots')
        assigned_staff_id = data.get('assigned_staff_id')
        start_date = datetime.strptime(data.get('start_date'), '%Y-%m-%d').date()
        end_date = datetime.strptime(data.get('end_date'), '%Y-%m-%d').date()
        status = data.get('status')
        image_url = data.get('image_url')
        if not data or not name or not location or not difficulty or not price or not available_slots or not start_date or not end_date or not image_url:
            return make_response(jsonify({'message': 'Please provide all the required fields'}), 400)
        if price <= 0:
            return make_response(jsonify({'message': 'Price should be greater than or equal to 0'}), 400)
        if available_slots <= 0:
            return make_response(jsonify({'message': 'Available Slots should be greater than or equal to 0'}), 400)
        if assigned_staff_id and not status:
            return make_response(jsonify({'message': 'You have to select trek status if you have assigned staff'}), 400)
        if not assigned_staff_id and status:
            return make_response(jsonify({'message': 'You can not select trek status if you have not assigned staff'}), 400)
        if not assigned_staff_id:
            assigned_staff_id = None
            status = 'Pending'
        
        if start_date > end_date:
            return make_response(jsonify({'message': 'Start Date should be earlier than End Date'}), 400)
        
        duration = (end_date - start_date).days
        
        
        trek.name = name
        trek.location = location
        trek.difficulty = difficulty
        trek.price = price
        trek.description = description
        trek.available_slots = available_slots
        trek.assigned_staff_id = assigned_staff_id
        trek.start_date = start_date
        trek.end_date = end_date
        trek.duration = duration
        trek.status = status
        trek.image_url = image_url
        db.session.commit()
        return make_response(jsonify({'message': 'Trek updated successfully'}), 200)

api.add_resource(AdminTrekAPI, '/admin/treks' , '/admin/trek/<int:id>')


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
        email = data.get('email')
        password = data.get('password')
        cpassword = data.get('cpassword')
        fullname = data.get('fullname')
        phone = data.get('phone')
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

class TrekAPI(Resource):
    @admin_required
    def get(self):
        trek = Trek.query.all()
        response = []
        for t in trek:
            response.append(t.get_trek())
        return make_response(jsonify(response), 200)

api.add_resource(TrekAPI, '/trek')