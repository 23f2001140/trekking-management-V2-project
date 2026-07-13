from flask import request, jsonify, make_response
from flask_restful import Resource, Api
from models import db, User, Trek, Booking
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity , verify_jwt_in_request, get_jwt  
from functools import wraps
from datetime import datetime
from flask_caching import Cache

api = Api(prefix='/api')
cache = Cache()

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

def not_blacklisted(f):
    @wraps(f)
    @jwt_required()
    def decorated(*args, **kwargs):
        id= get_jwt_identity()
        user = User.query.filter_by(id=id).first()
        if user.is_blacklisted:
            return make_response(jsonify({'message': 'Your account has been blacklisted Please contatct support at support@trekcentral.com'}), 401)
        return f(*args, **kwargs)
    return decorated

class LoginApi(Resource):
    def post(self):
        data=request.get_json()
        if not data:
            return make_response(jsonify({'message': 'Please provide a valid data'}), 400)
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
        if not data:
            return make_response(jsonify({'message': 'Please provide a valid data'}), 400)
        email = data.get('email')
        password=data.get('password')
        cpassword=data.get('cpassword')
        fullname = data.get('fullname')
        phone = data.get('phone')
        if not email or not password or not cpassword or not fullname or not phone:
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
    @cache.cached()
    def get(self):
        user_count=User.query.filter_by(role='user').count()
        staff_count=User.query.filter_by(role='staff').count()
        treks=Trek.query.count()
        bookings=Booking.query.count()
        
        trekss=Trek.query.all()
        chart_labels=[]
        chart_count=[]
        revenue=[]
        for trek in trekss:
            bookings_count=len([booking for booking in trek.bookings if booking.status == 'Booked'])
            if bookings_count > 0:
                chart_labels.append(trek.name)
                chart_count.append(bookings_count)
                revenue.append(bookings_count*trek.price)
        
        return make_response(jsonify({ 'user_count': user_count, 'staff_count': staff_count, 'treks': treks, 'bookings': bookings, 'chart_labels': chart_labels, 'chart_count': chart_count, 'revenue': revenue}), 200)

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
            
            cached_treks = cache.get('all_treks')
            if cached_treks:
                return make_response(jsonify(cached_treks), 200)
            
            treks = Trek.query.all()
            response = []
            for trek in treks:
                response.append(trek.get_trek())
                
            cache.set('all_treks', response)
            return make_response(jsonify(response), 200)
    
    @admin_required
    def post(self):
        data = request.get_json()
        if not data:
            return make_response(jsonify({'message': 'Please provide a valid data'}), 400)
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
        if not name or not location or not difficulty or not price or not available_slots or not start_date or not end_date:
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
        if assigned_staff_id:
            staff = User.query.get(assigned_staff_id)
            if staff and staff.is_blacklisted:
                return make_response(jsonify({'message': 'You can not assign blacklisted staff to trek'}), 400)
        
        if start_date > end_date:
            return make_response(jsonify({'message': 'Start Date should be earlier than End Date'}), 400)
        
        duration = (end_date - start_date).days
        
        
        try:
            trek = Trek(name=name, location=location, difficulty=difficulty, price=price, description=description, available_slots=available_slots, assigned_staff_id=assigned_staff_id, start_date=start_date, end_date=end_date, duration=duration, status=status, image_url=image_url)
            db.session.add(trek)
            db.session.commit()
            cache.clear()
            return make_response(jsonify({'message': 'Trek created successfully'}), 201)
        except:
            return make_response(jsonify({'message': 'Something went wrong while creating trek'}), 500)
        
    @admin_required
    def put(self,id):
        if not id:
            return make_response(jsonify({'message': 'Please provide a valid id'}), 400)
        data = request.get_json()
        if not data:
            return make_response(jsonify({'message': 'Please provide a valid data'}), 400)
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
        available_slots = data.get('available_slots') or None
        assigned_staff_id = data.get('assigned_staff_id')
        start_date = datetime.strptime(data.get('start_date'), '%Y-%m-%d').date()
        end_date = datetime.strptime(data.get('end_date'), '%Y-%m-%d').date()
        status = data.get('status')
        image_url = data.get('image_url')
        if not data or not name or not location or not difficulty or not price or not start_date or not end_date:
            return make_response(jsonify({'message': 'Please provide all the required fields'}), 400)
        if price <= 0:
            return make_response(jsonify({'message': 'Price should be greater than or equal to 0'}), 400)
        if available_slots is None:
            return make_response(jsonify({'message': 'Please provide available slots'}), 400)
        if available_slots and available_slots < 0:
            return make_response(jsonify({'message': 'Available Slots should be greater than or equal to 0'}), 400)
        if assigned_staff_id and not status:
            return make_response(jsonify({'message': 'You have to select trek status if you have assigned staff'}), 400)
        if not assigned_staff_id and status:
            return make_response(jsonify({'message': 'You can not select trek status if you have not assigned staff'}), 400)
        if not assigned_staff_id:
            assigned_staff_id = None
            status = 'Pending'
        if assigned_staff_id:
            staff = User.query.get(assigned_staff_id)
            if staff and staff.is_blacklisted:
                return make_response(jsonify({'message': 'You can not assign blacklisted staff to trek'}), 400)
        
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
        cache.clear()
        return make_response(jsonify({'message': 'Trek updated successfully'}), 200)
    
    @admin_required
    def delete(self,id):
        if not id:
            return make_response(jsonify({'message': 'Please provide a valid id'}), 400)
        trek = Trek.query.filter_by(id=id).first()
        if not trek:
            return make_response(jsonify({'message': 'Trek does not exist'}), 404)
        if trek.bookings:
            return make_response(jsonify({'message': 'Trek cannot be deleted as it has bookings'}), 400)
        db.session.delete(trek)
        db.session.commit()
        cache.clear()
        return make_response(jsonify({'message': 'Trek deleted successfully'}), 200)


api.add_resource(AdminTrekAPI, '/admin/treks' , '/admin/trek/<int:id>')


class AdminUserAPI(Resource):
    @admin_required
    def get(self):
        user = User.query.filter_by(role='user').all()
        response = []
        for u in user:
            response.append(u.get_user())
        return make_response(jsonify(response), 200)
    
    @admin_required
    def patch(self, id):
        if not id:
            return make_response(jsonify({'message': 'Please provide a valid id'}), 400)
        data = request.get_json()
        user = User.query.filter_by(id=id).first()
        if not user:
            return make_response(jsonify({'message': 'User does not exist'}), 404)
        is_blacklisted = data.get('is_blacklisted')
        if is_blacklisted in [True, False]:
            user.is_blacklisted = is_blacklisted
            db.session.commit()
            if(is_blacklisted and user.role == 'user'):
                return make_response(jsonify({'message': 'User blacklisted successfully'}), 200)
            elif(is_blacklisted and user.role == 'staff'):
                return make_response(jsonify({'message': 'Staff blacklisted successfully'}), 200)
            elif(not is_blacklisted and user.role == 'user'):
                return make_response(jsonify({'message': 'User Activated successfully'}), 200)
            elif(not is_blacklisted and user.role == 'staff'):
                return make_response(jsonify({'message': 'Staff Activated successfully'}), 200)
        else:
            return make_response(jsonify({'message': 'Invalid data provided'}), 400)
api.add_resource(AdminUserAPI, '/admin/users' , '/admin/users/<int:id>')

class AdminStaffAPI(Resource):
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
        if not data:
            return make_response(jsonify({'message': 'Please provide a valid data'}), 400)
        email = data.get('email')
        password = data.get('password')
        cpassword = data.get('cpassword')
        fullname = data.get('fullname')
        phone = data.get('phone')
        if not email or not password or not fullname or not phone or not cpassword:
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
        cache.clear()
        return make_response(jsonify({'message': 'Staff created successfully'}), 201)
api.add_resource(AdminStaffAPI, '/admin/staff')

class AdminBookingsAPI(Resource):
    @admin_required
    def get(self):
        bookings = Booking.query.all()
        bookings.reverse()
        response = []
        for booking in bookings:
            response.append(booking.admin_get_booking())
        return make_response(jsonify(response), 200)
    
api.add_resource(AdminBookingsAPI, '/admin/bookings')   

class UserDashboardAPI(Resource):
    @user_required
    @not_blacklisted
    def get(self):
        
        userid=get_jwt_identity()
        cache_key=f'user_{userid}'
        cached_user=cache.get(cache_key)
        if cached_user:
            return make_response(jsonify(cached_user), 200)
        
        treks = Trek.query.filter_by(status='Open').all()
        upcoming_treks = Trek.query.filter_by(status='Approved').all()
        bookings=Booking.query.filter_by(user_id=get_jwt_identity()).all()
        bookings_status={ booking.trek_id: booking.status for booking in bookings }
        response = []
        response2 = []
        for trek in treks:
            response.append(trek.get_trek())
        for trek in upcoming_treks:
            response2.append(trek.get_trek())
            
        result={'treks': response, 'upcoming_treks': response2,'bookings_status': bookings_status}
        
        cache.set(cache_key, result)
        return make_response(jsonify(result), 200)
api.add_resource(UserDashboardAPI, '/user')

class UserBookingAPI(Resource):
    @user_required
    @not_blacklisted
    def get(self):
        bookings = Booking.query.filter_by(user_id=get_jwt_identity()).all()
        ongoing_bookings = [booking for booking in bookings if booking.trek.status in ['Open' , 'Closed' , 'Started'] and booking.status == 'Booked']
        past_bookings = [booking for booking in bookings if booking.trek.status == 'Completed' or booking.status == 'Cancelled']
        response = []
        response2 = []
        for booking in ongoing_bookings:
            response.append(booking.get_booking())
        for booking in past_bookings:
            response2.append(booking.get_booking())
        return make_response(jsonify({'ongoing': response, 'past': response2}), 200)    


    @user_required
    @not_blacklisted
    def post(self, id):
        if not id:
            return make_response(jsonify({'message': 'Please provide a valid id'}), 400)
        trek = Trek.query.get(id)
        if not trek:
            return make_response(jsonify({'message': 'Trek does not exist'}), 404)
        if trek.status != 'Open':
            return make_response(jsonify({'message': 'This trek is not open for booking'}), 400)
        if trek.available_slots == 0:
            return make_response(jsonify({'message': 'This trek is fully booked'}), 400)
        cu_id = get_jwt_identity()
        if(Booking.query.filter_by(user_id=cu_id, trek_id=id, status='Booked').first()):
            return make_response(jsonify({'message': 'You have already booked this trek'}), 400)
        if(Booking.query.filter_by(user_id=cu_id, trek_id=id, status='Cancelled').first()):
            return make_response(jsonify({'message': 'You have cancelled your booking for this trek'}), 400)
        
        trek.available_slots -= 1
        booking = Booking(user_id=get_jwt_identity(), trek_id=id, booking_date=datetime.now())
        db.session.add(booking)
        db.session.commit()
        cache.clear()
        return make_response(jsonify({'message': 'Booking successful !'}), 201)
    
    @user_required
    @not_blacklisted
    def patch(self, id):
        if not id:
            return make_response(jsonify({'message': 'Please provide a valid id'}), 400)
        booking = Booking.query.filter_by(id=id).first()
        if not booking:
            return make_response(jsonify({'message': 'Booking does not exist'}), 404)
        if booking.user_id != int(get_jwt_identity()):
            return make_response(jsonify({'message': 'You are not authorized to cancel this booking!'}), 401)
        if booking.status == 'Cancelled':
            return make_response(jsonify({'message': 'Booking is already cancelled'}), 400)
        booking.trek.available_slots += 1
        booking.status = 'Cancelled'
        db.session.commit()
        cache.clear()
        return make_response(jsonify({'message': 'Booking cancelled successfully'}), 200)

api.add_resource(UserBookingAPI, '/user/booking' , '/user/booking/<int:id>')

class StaffDashboardAPI(Resource):
    @staff_required
    @not_blacklisted
    def get(self):
        staff_id=get_jwt_identity()
        cache_key=f'staff_{staff_id}'
        cached_staff=cache.get(cache_key)
        if cached_staff:
            return make_response(jsonify(cached_staff), 200)
        
        treks = Trek.query.filter_by(assigned_staff_id=get_jwt_identity()).all()
        registered_users = {}
        response = []
        total_participants = 0
        for trek in treks:
            response.append(trek.get_trek())
            registered_users[trek.id] = len([booking for booking in trek.bookings if booking.status == 'Booked'])
            total_participants += registered_users[trek.id]
        
        result={'treks': response , 'registered_users': registered_users, 'total_participants': total_participants}
        cache.set(cache_key, result)
        return make_response(jsonify(result), 200)
api.add_resource(StaffDashboardAPI, '/staff')

class StaffTrekManageAPI(Resource):
    
    @staff_required
    @not_blacklisted
    def get(self, id):
        if not id:
            return make_response(jsonify({'message': 'Please provide a valid id'}), 400)
        trek = Trek.query.filter_by(id=id).first()
        if not trek:
            return make_response(jsonify({'message': 'Trek does not exist'}), 404)
        if trek.assigned_staff_id != int(get_jwt_identity()):
            return make_response(jsonify({'message': 'You are not authorized to manage this trek'}), 401)
        registered_users = [booking.get_booking_with_user() for booking in trek.bookings if booking.status == 'Booked']
        cancelled_users = [booking.get_booking_with_user() for booking in trek.bookings if booking.status == 'Cancelled']
        
        response={
            'name': trek.name,
            'location': trek.location,
            'difficulty': trek.difficulty,
            'duration': trek.duration,
            'available_slots': trek.available_slots,
            'start_date': trek.start_date,
            'end_date': trek.end_date,
            'status': trek.status,
        }
            
        return make_response(jsonify({'trek': response, 'registered_users': registered_users, 'cancelled_users': cancelled_users}), 200)

    @staff_required
    @not_blacklisted
    def patch(self, id):
        if not id:
            return make_response(jsonify({'message': 'Please provide a valid id'}), 400)
        data = request.get_json()
        if not data:
            return make_response(jsonify({'message': 'Please provide a valid data'}), 400)
        trek = Trek.query.filter_by(id=id).first()
        if not trek:
            return make_response(jsonify({'message': 'Trek does not exist'}), 404)
        if trek.assigned_staff_id != int(get_jwt_identity()):
            return make_response(jsonify({'message': 'You are not authorized to manage this trek'}), 401)
        status = data.get('status')
        available_slots = data.get('available_slots')
        if status:
            if status not in [ 'Open', 'Closed', 'Started', 'Completed']:
                return make_response(jsonify({'message': 'Invalid status provided'}), 400)
            trek.status = status
            db.session.commit()
            cache.clear()
            return make_response(jsonify({'message': 'Trek Status Updated Successfully'}), 200)
        if available_slots != None:
            if available_slots < 0:
                return make_response(jsonify({'message': 'Available Slots should be greater than or equal to 0'}), 400)
            trek.available_slots = available_slots
            db.session.commit()
            cache.clear()
            return make_response(jsonify({'message': 'Trek Available Slots Updated Successfully'}), 200)
        
api.add_resource(StaffTrekManageAPI, '/staff/trek/<int:id>')

class ProfileUpdateAPI(Resource):
    @jwt_required()
    @not_blacklisted
    def put(self):
        data = request.get_json()
        
        if not data:
            return make_response(jsonify({'message': 'Please provide a valid data'}), 400)
        
        fullname = data.get('fullname')
        email = data.get('email')
        phone = data.get('phone')
        password = data.get('password')
        new_password = data.get('new_password')
        cnpassword = data.get('cnpassword')
    
        if not fullname or not email or not phone or not password:
            return make_response(jsonify({'message': 'Please provide all the required fields'}), 400)
        if new_password and len(new_password) < 6:
            return make_response(jsonify({'message': 'New Password must be at least 6 characters long'}), 400)
        if new_password and new_password != cnpassword:
            return make_response(jsonify({'message': 'New Passwords do not match'}), 400)
        
        user = User.query.get(get_jwt_identity())
        if not user:
            return make_response(jsonify({'message': 'You are not authorized to update your profile'}), 401)
        if not check_password_hash(user.passhash, password):
            return make_response(jsonify({'message': 'Wrong password'}), 400)
        if email != user.email:
            if user.role == 'staff':
                return make_response(jsonify({'message': 'Staff is not allowed to change their email'}), 400)
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                return make_response(jsonify({'message': 'Email already exists'}), 400)
        if phone != user.phone:
            existing_user = User.query.filter_by(phone=phone).first()
            if existing_user:
                return make_response(jsonify({'message': 'Phone number already exists'}), 400)
        
        user.fullname = fullname
        user.email = email
        user.phone = phone
        if new_password:
            user.passhash = generate_password_hash(new_password)
        db.session.commit()
        return make_response(jsonify({'message': 'Profile updated successfully' , 'user': user.get_user()}), 200)

api.add_resource(ProfileUpdateAPI, '/update_profile')

class UserExportCSVAPI(Resource):
    @user_required
    def post(self):
        from celery_app import export_user_bookings_csv
        user_id = get_jwt_identity()
        export_user_bookings_csv.delay(user_id)
        return make_response(jsonify({'message': 'Export started. Check your email shortly.'}), 200)

api.add_resource(UserExportCSVAPI, '/user/export_csv')