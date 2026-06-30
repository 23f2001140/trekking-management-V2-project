from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone= db.Column(db.String(10), unique=True, nullable=False)
    passhash = db.Column(db.String(256), nullable=False)
    fullname = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='user')
    is_blacklisted = db.Column(db.Boolean, nullable=False, default=False)
    
    bookings = db.relationship('Booking', backref='user', lazy=True)
    assigned_treks = db.relationship('Trek', backref='assigned_staff', lazy=True)
    
    def __repr__(self):
        return f"<User {self.fullname}>"
    
    def get_user(self):
        return {'id': self.id, 
                'email': self.email, 
                'phone': self.phone, 
                'fullname': self.fullname,
                'role':self.role,
                'is_blacklisted': self.is_blacklisted
                }
    
class Trek(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    difficulty = db.Column(db.String(20), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)
    duration = db.Column(db.Integer, nullable=False) 
    available_slots = db.Column(db.Integer, nullable=False)
    assigned_staff_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Open')
    image_url = db.Column(db.String(2000), nullable=True)
    
    bookings = db.relationship('Booking', backref='trek', lazy=True)    
    
    def __repr__(self):
        return f"<Trek {self.name}>"
    
    def get_trek(self):
        return {'id': self.id, 
                'name': self.name, 
                'location': self.location, 
                'difficulty': self.difficulty, 
                'price': self.price, 
                'description': self.description, 
                'duration': self.duration, 
                'available_slots': self.available_slots, 
                'assigned_staff_id': self.assigned_staff_id, 
                'start_date': self.start_date, 
                'end_date': self.end_date, 
                'status': self.status,
                'image_url': self.image_url,
                'assigned_staff': self.assigned_staff.get_user() if self.assigned_staff else None
                }
    
class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    trek_id = db.Column(db.Integer, db.ForeignKey('trek.id'), nullable=False)
    booking_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Booked') 
    
    def __repr__(self):
        return f"<Booking {self.id}>"
    
    def get_booking(self):
        return {'id': self.id, 
                'user_id': self.user_id, 
                'trek_id': self.trek_id, 
                'booking_date': self.booking_date, 
                'status': self.status,
                'trek': self.trek.get_trek()
                }