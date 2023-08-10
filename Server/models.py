from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100),nullable=False)
    email = db.Column(db.String(100),nullable=False,unique=True)
    password = db.Column(db.String(100),nullable=False)
    is_admin = db.Column(db.Boolean,default=False)
    is_user = db.Column(db.Boolean,default=False)
    last_login = db.Column(db.DateTime,default=datetime.utcnow)
    
    def __init__(self,name,email,password,is_admin=False,is_user=False):
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)
        self.is_admin = is_admin
        self.is_user = is_user

    @classmethod
    def authenticate(cls,**kwargs):
        email = kwargs.get('email')
        password = kwargs.get('password')

        if not email or not password:
            return None

        user = cls.query.filter_by(email=email,is_user=True).first()
        if not user or not check_password_hash(user.password,password):
            return None

        return user
    
    @classmethod
    def authenticate_admin(cls,**kwargs):
        email = kwargs.get('email')
        password = kwargs.get('password')

        if not email or not password:
            return None
        
        user = cls.query.filter_by(email=email,is_admin=True).first()
        if not user or not check_password_hash(user.password,password):
            return None
        
        return user

class movievenue(db.Model):
    __tablename__ = 'movievenue'
    id = db.Column(db.Integer,primary_key=True)
    admin_id = db.Column(db.Integer,db.ForeignKey('user.id',ondelete='CASCADE',onupdate='CASCADE'),nullable=False)
    name = db.Column(db.String(100),nullable=False,unique=True)
    location = db.Column(db.String(100),nullable=False)
    capacity = db.Column(db.Integer,nullable=False)
    image = db.Column(db.Text,nullable=False)
    description = db.Column(db.String(100),nullable=False)
    
    def __init__(self,name,location,capacity,image,description,admin_id):
        self.admin_id = admin_id
        self.name = name
        self.location = location
        self.capacity = capacity
        self.image = image
        self.description = description

    def to_dict(self):
        return {
            'id':self.id,
            'name':self.name,
            'location':self.location,
            'capacity':self.capacity,
            'image':self.image,
            'description':self.description,
            'admin_id':self.admin_id
        }

class movieshow(db.Model):
    __tablename__ = 'movieshow'
    id = db.Column(db.Integer,primary_key=True)
    venue_id = db.Column(db.Integer,db.ForeignKey('movievenue.id',ondelete='CASCADE',onupdate='CASCADE'),nullable=False)
    movie = db.Column(db.String(100),nullable=False)
    rating = db.Column(db.String(100),nullable=False)
    tags = db.Column(db.String(100))
    date = db.Column(db.DateTime,default=datetime.utcnow)
    duration = db.Column(db.DateTime,nullable=False)
    price = db.Column(db.Integer,nullable=False)
    image = db.Column(db.Text,nullable=False)
    description = db.Column(db.String(100),nullable=False)
    current_capacity = db.Column(db.Integer,nullable=False)
    enabled = db.Column(db.Boolean,default=True)
    
    def __init__(self,movie,date,price,image,description,venue_id,duration,current_capacity,rating,tags,enabled):
        self.movie = movie
        self.date = date
        self.current_capacity = current_capacity
        self.price = price
        self.image = image
        self.description = description
        self.venue_id = venue_id
        self.duration = duration
        self.rating = rating
        self.tags = tags
        self.enabled = enabled

class booking(db.Model):
    __tablename__ = 'booking'
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id',ondelete='CASCADE',onupdate='CASCADE'),nullable=False)
    show_id = db.Column(db.Integer,db.ForeignKey('movieshow.id',ondelete='CASCADE',onupdate='CASCADE'),nullable=False)
    quantity = db.Column(db.Integer,nullable=False)
    total = db.Column(db.Integer,nullable=False)
    date = db.Column(db.DateTime,default=datetime.utcnow)
    movie = db.Column(db.String(100),nullable=False)
    venue = db.Column(db.String(100),nullable=False)
    status = db.Column(db.String(100),nullable=False)
    rating = db.Column(db.Float,default=6)
    
    def __init__(self,user_id,show_id,quantity,total,date,movie,venue,status):
        self.user_id = user_id
        self.show_id = show_id
        self.quantity = quantity
        self.total = total
        self.date = date
        self.movie = movie
        self.venue = venue
        self.status = status

    def to_dict(self):
        return {
            'id':self.id,
            'user_id':self.user_id,
            'show_id':self.show_id,
            'quantity':self.quantity,
            'total':self.total,
            'date':self.date,
            'movie':self.movie,
            'venue':self.venue,
            'status':self.status,
            'rating':self.rating
        }
