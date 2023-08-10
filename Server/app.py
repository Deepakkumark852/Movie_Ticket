from flask import Flask,request,session,jsonify,make_response,send_from_directory

from sqlalchemy.engine import Engine
from sqlalchemy import event
from models import db,User,movievenue,movieshow,booking

from functools import wraps
from datetime import datetime, timedelta
import time ,os
from fpdf import FPDF


from flask import jsonify, request

import jwt
from flask_mail import Mail, Message
import csv


from flask_migrate import Migrate
from flask_cors import CORS

from datetime import datetime, timedelta
from celery_worker import make_celery
from celery.schedules import crontab


# ..............................................................Flask Initialization.............................................................................

app = Flask(__name__, instance_path='/home/deepak/Documents/APPDEV2/Server/protected')
CORS(app,origins=["http://localhost:5173","http://localhost:5000"],supports_credentials=True,allow_headers=["Content-Type","Authorization","Access-Control-Allow-Credentials"],methods=["GET","POST","PUT","DELETE"])
app.secret_key = 'secret123'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movie.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']: 'False'
app.config['CSV_FOLDER'] = '/home/deepak/Documents/APPDEV2/Server/protected'
db.init_app(app)


migrate = Migrate(app,db,render_as_batch=True)
app.app_context().push()

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


# ..............................................................Celery Configuration.............................................................................

#                                !important   Note : Start redis server before running celery   !important

app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379',
    CELERY_RESULT_BACKEND='redis://localhost:6379'
)

celery = make_celery(app)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'sparemail852@gmail.com'
app.config['MAIL_PASSWORD'] = 'eczmywabgcdzwrqq'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

# ..............................................................Celery Tasks.............................................................................
@celery.task(name= 'app.send_email')
def send_email(recpient,body):
    print("Sending mail", recpient)
    msg = Message('Hello', sender = 'noreply@ticket.com', recipients = recpient)
    msg.body = body
    mail.send(msg)
    print("Mail sent")

@celery.task(name='app.successful_login')
def successful_login(user_id):
    print("Sending mail", user_id)
    msg = Message('Hello', sender = 'noreply@ticket.com', recipients = [user_id])
    msg.body = "You have successfully logged in"
    mail.send(msg)
    print("Mail sent")

@celery.task(name='app.successful_logout')
def successful_logout(user_id):
    print("Sending mail", user_id)
    msg = Message('Hello', sender = 'noreply@ticket.com', recipients = [user_id])
    msg.body = "You have successfully logged out"
    mail.send(msg)
    print("Mail sent")

@celery.task(name='app.send_entertainmentreport')
def send_entertainmentreport(recipient):
    print("Sending entertainment report")
    # mime type email attached file to message
    id= recipient
    recipient = User.query.with_entities(User.email).filter_by(id=recipient).first()
    recipient = recipient[0]
    print("Sending mail", recipient)
    msg = Message('Entertainment Report', sender = "noreply@ticket.com", recipients = [recipient])
    msg.body = "Hey there, \n\nGood evening, superstar movie buff! 🌟\n\nWe hope this email brings a dash of excitement to your day! 🎉 It's time to grab your popcorn, snuggle up on the couch, and embark on a cinematic adventure like no other with Ticketboss! 🎬🍿\n\nWe know you've got an eye for fantastic films and an insatiable appetite for captivating shows. That's why we're here to remind you to dive into our treasure trove of thrilling movies and binge-worthy series!\n\nWhy waste time endlessly scrolling through streaming services when you can explore an extensive collection of blockbusters, indie gems, and award-winning shows on Ticketboss? 🤩\n\nWe've got something for everyone, so you can enjoy a movie marathon with your family, a romantic date night with your partner, or a fun-filled evening with your friends! 🎉\n\nSo, what are you waiting for? 🤔 Grab your popcorn and get ready for a movie marathon like no other! 🍿\n\nHappy watching!\n\nRegards,\nTeam Ticketboss"
    with app.open_resource("/home/deepak/Documents/APPDEV2/Server/protected/entertainment_report"+str(id)+".pdf") as fp:
        msg.attach("entertainment_report"+str(id)+".pdf", "application/pdf", fp.read())
    mail.send(msg)
    print("Entertainment report sent")

@celery.task(name='app.monthly_user')
def monthly_user():
    monthly_user = User.query.with_entities(User.id).all()
    monthly_ = [i[0] for i in monthly_user]
    print("monthly",monthly_)
    for user1 in monthly_:
        print(user1)
        monthly_user = booking.query.filter(booking.user_id==user1)
        monthly_user = [i.to_dict() for i in monthly_user]
        print(monthly_user)
        rows = []
        for i in monthly_user:
            rows.append([i['show_id'],i['movie'],i['quantity'],i['total'],i['date'],i['rating']])
        filename = '/home/deepak/Documents/APPDEV2/Server/protected/monthly_user.csv'
        fields = ['id','user_id','show_id','no_of_tickets','total_price','booking_date','rating']
        #generating pdf file for monthly user with booking details show_id, no_of_tickets, total_price, booking_date, rating
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Monthly User Report", ln=1, align='C')
        for each in rows:
            pdf.cell(200, 10, txt=str(each), ln=2, align='C')
        pdf.output("/home/deepak/Documents/APPDEV2/Server/protected/entertainment_report"+str(user1)+".pdf")
        send_entertainmentreport.delay(user1)
              
    
@celery.task(name = 'app.generate_csv')
def generate_csv(id):
    print("Generating CSV")
    time.sleep(6)
    venue_data = movievenue.query.filter_by(admin_id=id).all()
    print(venue_data)
    venue_data = [i.to_dict() for i in venue_data]
    rows = []
    for i in venue_data:
        rows.append([i['id'],i['name'],i['location'],i['capacity'],i['description'],i['admin_id']])
    filename = '/home/deepak/Documents/APPDEV2/Server/protected/venue.csv'
    fields = ['id','name','location','capacity','description','admin_id']
   
    with open(filename, 'w') as csvfile: 
        csvwriter = csv.writer(csvfile) 
         
        csvwriter.writerow(fields) 
        
        csvwriter.writerows(rows)
    print("CSV generated")


@celery.on_after_configure.connect
def setup_periodic_tasks(sender , **kwargs):
    today = datetime.today()
    yesterday = today - timedelta(days=1)
    print("yesterday",yesterday)
    sender.add_periodic_task(crontab(hour=13, minute=12),monthly_user.s(),name="monthly user")

    user = User.query.with_entities(User.email).filter(User.last_login < yesterday).all()
    user = [i[0] for i in user]
    print(user)
    mssage = '''Hey there,

Good evening, superstar movie buff! 🌟

We hope this email brings a dash of excitement to your day! 🎉 It's time to grab your popcorn, snuggle up on the couch, and embark on a cinematic adventure like no other with Ticketboss! 🎬🍿

We know you've got an eye for fantastic films and an insatiable appetite for captivating shows. That's why we're here to remind you to dive into our treasure trove of thrilling movies and binge-worthy series!

Why waste time endlessly scrolling through streaming services when you can explore an extensive collection of blockbusters, indie gems, and all-time classics, right at your fingertips? 🌟'''

    # sender.add_periodic_task(30.0,send_email.s(user,mssage),name="send email every 30 seconds")
    sender.add_periodic_task(crontab(hour=11, minute=55),send_email.s(user,mssage),name="send email every 10 seconds")

@app.route("/status/<task_id>")
def taskstatus(task_id):
    res = celery.AsyncResult(task_id)
    return {
        "task_id":task_id,
        "state":res.state,
        "result":res.result
    }

# ..............................................................Function and Decorators.............................................................................

def round_dt(dt, delta):
    return datetime.min + round((dt - datetime.min) / delta) * delta

def getslots(hours, appointments, duration):
    slot=[]
    slots = sorted([(hours[0], hours[0])] + appointments + [(hours[1], hours[1])])
    for start, end in ((slots[i][1], slots[i+1][0]) for i in range(len(slots)-1)):
        assert start <= end, "Cannot attend all appointments"
        if start != slots[0][1]:
                start += timedelta(minutes=30)
                start = round_dt(start, timedelta(minutes=30))
        while start + duration <= end:
            slot.append((start.strftime("%Y-%m-%d %H:%M:%S"), (start + duration).strftime("%Y-%m-%d %H:%M:%S")))
            start = duration +start + timedelta(minutes=30)
            start = round_dt(start, timedelta(minutes=30))
    return slot

def token_required(f):
    @wraps(f)
    def _verify(*args,**kwargs):
        auth_headers = request.headers.get('Authorization', '').split()

        invalid_msg = {
            'message':'Invalid token. Registration and / or authentication required for login',
            'authenticated':False
        }
        expired_msg = {
            'message':'Expired token. Reauthentication required.',
            'authenticated':False
        }

        if len(auth_headers) != 2:
            return jsonify(invalid_msg),401

        try:
            token = auth_headers[1]
            print("token:" , token)
            data = jwt.decode(token,app.secret_key)
            print("data:" , data['sub'])
            user = User.query.filter_by(id=data['sub']).first()
            if not user:
                raise RuntimeError('User not found')
            return f(user,*args,**kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify(expired_msg),401
        except (jwt.InvalidTokenError,Exception) as e:
            print(e)
            return jsonify(invalid_msg),401
    return _verify

def access_level(access_level):
    def decorator(f):
        @wraps(f)
        def verify(*args,**kwargs):
            auth_headers = request.headers.get('Authorization', '').split()

            invalid_msg = {
                'message':'Invalid token. Registration and / or authentication required for Access',
                'authenticated':False
            }
            expired_msg = {
                'message':'Expired token. Reauthentication required.',
                'authenticated':False
            }

            if len(auth_headers) != 2:
                return jsonify(invalid_msg),401

            try:
                token = auth_headers[1]
                print("token:" , token)
                data = jwt.decode(token,app.secret_key)
                print("data:" , data['role'])
                if data['role'] in access_level:
                    return f(*args,**kwargs)
                else:
                    return jsonify({'message':'Access Denied'}),401
            except jwt.ExpiredSignatureError:
                return jsonify(expired_msg),401
            except (jwt.InvalidTokenError,Exception) as e:
                print(e)
                return jsonify(invalid_msg),401
        return verify
    return decorator

############################################# API's #####################################################

############################################# User API's #################################################

@app.route('/userlogin',methods=['GET','POST'])
def userlogin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        print(email,password)
        user = User.authenticate(email=email,password=password,is_user=True)
        if not user:
            return make_response('Notfound',404)
        else:
            session['user_id'] = user.id
            session['user_name'] = user.name
            session['is_user'] = user.is_user
            session['is_admin'] = user.is_admin
            print("sesion_id",session.get('user_id'))
            if user.is_admin and user.is_user:
                token = jwt.encode({
                'sub':user.id,
                'role':2,
                'iat':datetime.utcnow(),
                'exp':datetime.utcnow() + timedelta(minutes=30)},
                app.secret_key)
            else:
                token = jwt.encode({
                    'sub':user.id,
                    'role':0,
                    'iat':datetime.utcnow(),
                    'exp':datetime.utcnow() + timedelta(minutes=30)},
                    app.secret_key)
            user.last_login = datetime.now()
            db.session.commit()
            successful_login.delay(user.email)
            return jsonify({ 'token': token.decode('UTF-8') })
    return make_response('method not allowed',405)

@app.route('/userregister',methods=['GET','POST'])
def userregister():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        is_user = True
        if User.query.filter_by(email=email).first():
            user = User.query.filter_by(email=email).first()
            user.is_user = True
            db.session.commit()
            return jsonify({'message':'User Registered'},200)
        else:
            user = User(name=name,email=email,password=password,is_user=is_user)
            db.session.add(user)
            db.session.commit()
            return jsonify({'message':'User Registered'},200)
    return jsonify({'message':'User Not Registered'},401)

@app.route('/userlogout',methods=['GET','POST'])
def userlogout(current_user):
    if request.method == 'POST':
        session.pop('user_id',None)
        session.pop('user_name',None)
        session.pop('is_user',None)
        session.pop('is_admin',None)
        successful_logout.delay(current_user.email)
        return jsonify({'message':'Logout Successful'},200)
    return jsonify({'message':'Logout Failed'},401)

@app.route('/getuser',methods=['GET','POST'])
@token_required
def userprofile(current_user):
    if request.method == 'GET':
        user = User.query.filter_by(id=current_user.id).first()
        return jsonify({'name':user.name,'password':user.password,'email':user.email},200)
    return jsonify({'message':'Method Not Allowed'},405)

@app.route('/userupdate',methods=['GET','PUT'])
@token_required
def userupdate(current_user):
    if request.method == 'PUT':
        user = User.query.filter_by(id=current_user.id).first()
        user.name = request.form['name']
        user.email = request.form['email']
        user.password = request.form['password']
        db.session.commit()
        return jsonify({'message':'User Updated'},200)
    return jsonify({'message':'Method Not Allowed'},405)

@app.route('/userdelete',methods=['GET','DELETE'])
@token_required
def userdelete(current_user):
    if request.method == 'DELETE':
        user = User.query.filter_by(id=current_user.id).first()
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message':'User Deleted'},200)
    return jsonify({'message':'Method Not Allowed'},405)

            
#################################################### Admin API's ############################################

@app.route('/adminlogin',methods=['GET','POST'])
def adminlogin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        admin = User.authenticate_admin(email=email,password=password,is_admin=True)
        if admin:
            session['admin_id'] = admin.id
            session['admin_name'] = admin.name 
            session['is_admin'] = admin.is_admin
            if admin.is_user == True:
                token = jwt.encode({
                'sub':admin.id,
                'role':2,
                'iat':datetime.utcnow(),
                'exp':datetime.utcnow() + timedelta(minutes=30)},
                app.secret_key)
            else:
                token = jwt.encode({
                    'sub':admin.id,
                    'role':1, 
                    'iat':datetime.utcnow(),
                    'exp':datetime.utcnow() + timedelta(minutes=30)},
                    app.secret_key)
            admin.last_login = datetime.now()
            db.session.commit()
            successful_login.delay(admin.email)
            return jsonify({ 'token': token.decode('UTF-8') })
        else:
            return jsonify({'message':'Login Failed'},401)
    return jsonify({'message':'Login Failed'},401)

@app.route('/adminregister',methods=['GET','POST'])
def adminregister():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        is_admin = True
        if User.query.filter_by(email=email).first():
            user = User.query.filter_by(email=email).first()
            user.is_admin = True
            db.session.commit()
            return jsonify({'message':'Admin Registered'},200)
        else:
            admin = User(name=name,email=email,password=password,is_admin=is_admin)
            db.session.add(admin)
            db.session.commit()
            return jsonify({'message':'Admin Registered'},200)
    return jsonify({'message':'Admin Not Registered'},401)

@app.route('/adminlogout',methods=['GET','POST'])
def adminlogout(current_user):
    if request.method == 'POST':
        session.pop('admin_id',None)
        session.pop('admin_name',None)
        session.pop('is_admin',None)
        successful_logout.delay(current_user.email)
        return jsonify({'message':'Logout Successful'},200)
    return jsonify({'message':'Logout Failed'},401)

@app.route('/generatecsv',methods=['GET','POST'])
@token_required
@access_level([1,2])
def generatecsv(current_user):
    if request.method == 'GET':
        # a= send_email.delay(['deepakkumark852@gmail.com'],"hey Hello")
        a = generate_csv.delay(current_user.id)
        return jsonify({'task_id':a.id , 'status':a.status, 'result':a.result},200)
    return jsonify({'message':'Task Failed'},401)

@app.route('/getcsv',methods=['GET','POST'])
@token_required
@access_level([1,2])
def getcsv(current_user):
    print("current_user",current_user.id)
    return send_from_directory(os.path.join(app.instance_path,''),'venue.csv',as_attachment=True)

@app.route('/getadmin',methods=['GET','POST'])
@token_required
def adminprofile(current_user):
    if request.method == 'GET':
        admin = User.query.filter_by(id=current_user.id).first()
        return jsonify({'name':admin.name,'password':admin.password,'email':admin.email},200)
    return jsonify({'message':'Method Not Allowed'},405)

@app.route('/adminupdate',methods=['GET','PUT'])
@token_required
@access_level([1,2])
def adminupdate(current_user):
    if request.method == 'PUT':
        admin = User.query.filter_by(id=current_user.id).first()
        admin.name = request.form['name']
        admin.email = request.form['email']
        admin.password = request.form['password']
        db.session.commit()
        return jsonify({'message':'Admin Updated'},200)
    return jsonify({'message':'Method Not Allowed'},405)

@app.route('/admindelete',methods=['GET','DELETE'])
@token_required
@access_level([1,2])
def admindelete(current_user):
    if request.method == 'DELETE':
        admin = User.query.filter_by(id=current_user.id).first()
        db.session.delete(admin)
        db.session.commit()
        return jsonify({'message':'Admin Deleted'},200)
    return jsonify({'message':'Method Not Allowed'},405)


#################################################### Venue API's ############################################

@app.route('/getvenue',methods=['GET','POST'])
@token_required
@access_level([0,1,2])
def getvenue(current_user):
    if request.method == 'GET':
        venue = movievenue.query.all()
        venue_list = []
        for v in venue:
            print("id",v.id)
            venue_list.append({'id':v.id,'name':v.name,'location':v.location,'capacity':v.capacity,'image':v.image,'description':v.description})
            print(venue_list[0]['id'])
        return jsonify({'venue':venue_list},200)
    return jsonify({'message':'Venue Not Found'},401)

@app.route('/getvenuebyadmin',methods=['GET','POST'])
@token_required
@access_level([1,2])
def getvenuebyadmin(current_user):
    admin_id = current_user.id
    if request.method == 'GET':
        venue = movievenue.query.filter_by(admin_id=admin_id).all()
        venue_list = []
        for v in venue:
            venue_list.append({'id':v.id,'name':v.name,'location':v.location,'capacity':v.capacity,'image':v.image,'description':v.description})
        return jsonify({'venue':venue_list},200)
    return jsonify({'message':'Venue Not Found'},401)

@app.route('/addvenue',methods=['POST'])
@token_required
@access_level([1,2])
def addvenue(current_user):
   
    if request.method == 'POST':
       
        name = request.form['name']
        location = request.form['location']
        capacity = request.form['capacity']
        image = request.form['image']
        description = request.form['description']
        admin_id = current_user.id

        venue = movievenue(admin_id=admin_id,name=name,location=location,capacity=capacity,image=image,description=description)
        db.session.add(venue)
        db.session.commit()
        return jsonify({'message':'Venue Added'},200)
    return jsonify({'message':'Venue Not Added'},401)

@app.route('/editvenue',methods=['GET','PUT'])
@token_required
@access_level([1,2])
def editvenue(current_user):
    if request.method == 'PUT':
        venue_id = request.form['venue_id']
        venue = movievenue.query.filter_by(id=venue_id).first()
        venue.name = request.form['name']
        venue.location = request.form['location']
        venue.capacity = request.form['capacity']
        venue.image = request.form['image']
        venue.description = request.form['description']
        db.session.commit()
        return jsonify({'message':'Venue Updated'},200)
    return jsonify({'message':'Venue Not Updated'},401)

@app.route('/deletevenue',methods=['GET','DELETE'])
@token_required
@access_level([1,2])
def deletevenue(current_user):
    if request.method == 'DELETE':
        venue_id = request.form['venue_id']
        venue = movievenue.query.filter_by(id=venue_id).first()
        db.session.delete(venue)
        db.session.commit()
        return jsonify({'message':'Venue Deleted'},200)
    return jsonify({'message':'Venue Not Deleted'},401)


#################################################### Movie API's ############################################


@app.route('/addshow',methods=['GET','POST'])
@token_required
@access_level([1,2])
def addshow(current_user):
    try:
        if request.method == 'POST':
            movie = request.form['movie']
            dat = datetime.strptime(request.form['date'],'%Y-%m-%d %H:%M:%S')
            venue_id = request.form['venue_id']
            duration = datetime.strptime(request.form['duration'],'%H:%M:%S')
            show = movieshow.query.filter((movieshow.date>=dat ),movieshow.venue_id==venue_id).filter((movieshow.date<=dat+timedelta(hours=duration.hour,minutes=duration.minute,seconds=duration.second))).all()
            if show:
                print(show[0].date)
                return jsonify({'message':'Show Already Exists'},200)
            price = request.form['price']
            image = request.form['image']
            description = request.form['description']
            rating = '0/0'
            tags = request.form['tags']
            enabled = True
            current_capacity = movievenue.query.filter_by(id=venue_id).first().capacity
            show = movieshow(movie=movie,date=dat,venue_id=venue_id,price=price,image=image,description=description,duration=duration,current_capacity=current_capacity,rating=rating,tags=tags,enabled=enabled)
            db.session.add(show)
            db.session.commit()
            return jsonify({'message':'Show Added'},200)
        return jsonify({'message':'Show Not Added'},401)
    except Exception as e:
        print("E", e)
        return jsonify({'message': e},401)

@app.route('/ableshow',methods=['GET','PUT'])
@token_required
@access_level([1,2])
def ableshow(current_user):
    if request.method == 'PUT':
        show_id = request.form['show_id']
        show = movieshow.query.filter_by(id=show_id).first()
        show.enabled = not show.enabled
        db.session.commit()
        return jsonify({'message':'Show Enabled/Disabled'},200)
    return jsonify({'message':'Show Not Enabled/Disabled'},401)

@app.route('/rateshow',methods=['GET','PUT'])
@token_required
@access_level([0,2])
def rateshow(current_user):
    if request.method == 'PUT':
        print(request.form)
        show_id = request.form['show_id']
        book_id = request.form['book_id']
        rating = float(request.form['rating'])
        bookh = booking.query.filter_by(id=book_id).first()
        if bookh.rating == 6:
            bookh.rating = rating
            show = movieshow.query.filter_by(id=show_id).first()
            numerator = float(show.rating.split('/')[0])+rating
            denominator = float(show.rating.split('/')[1])+5
            show.rating = str(numerator)+'/'+str(denominator)
            db.session.commit()
            return jsonify({'message':'Show Rated'},200)
        else:
            show = movieshow.query.filter_by(id=show_id).first()
            numerator = float(show.rating.split('/')[0])-bookh.rating+rating
            show.rating = str(numerator)+'/'+str(show.rating.split('/')[1])
            bookh.rating = rating
            db.session.commit()
            return jsonify({'message':'Show ReRated'},200)
    return jsonify({'message':'Show Not Rated'},401)

@app.route('/editshow',methods=['GET','PUT'])
@token_required
@access_level([1,2])
def editshow(current_user):
    if request.method == 'PUT':
        print("sdfsdf",request.form)
        show_id = request.form['show_id']
        show = movieshow.query.filter_by(id=show_id).first()
        show.movie = request.form['movie']
        show.date = datetime.strptime(request.form['date'],'%Y-%m-%d %H:%M:%S')
        show.venue_id = request.form['venue_id']
        show.duration = datetime.strptime(request.form['duration'],'%H:%M:%S')
        show.price = request.form['price']
        show.image = request.form['image']
        show.description = request.form['description']
        show.tags = request.form['tags']
        db.session.commit()
        return jsonify({'message':'Show Edited'},200)
    return jsonify({'message':'Show Not Edited'},401)

@app.route('/deleteshow',methods=['GET','DELETE'])
@token_required
@access_level([1,2])
def deleteshow(current_user):
    if request.method == 'DELETE':
        show_id = request.form['show_id']
        show = movieshow.query.filter_by(id=show_id).first()
        db.session.delete(show)
        db.session.commit()
        return jsonify({'message':'Show Deleted'},200)
    return jsonify({'message':'Show Not Deleted'},401)


@app.route('/getfreeslots',methods=['GET','POST'])
@token_required
@access_level([1,2])
def getfreeslots(current_user):
    if request.method == 'POST':
        date = datetime.strptime(request.form['date'],'%Y-%m-%d %H:%M:%S')
        venue_id = request.form['venue_id']
        duration = datetime.strptime(request.form['duration'],'%H:%M:%S')
        duration = timedelta(hours=duration.hour,minutes=duration.minute,seconds=duration.second)
        # show = movieshow.query.filter(date<=date,movieshow.venue_id==venue_id,date>=date).all()
        show = movieshow.query.filter_by(venue_id=venue_id).filter(movieshow.date.between(date,date+timedelta(hours=23,minutes=59,seconds=59))).all()

        occupied_slots = []
        if show:
            for i in show:
                endtime = i.date + timedelta(hours=i.duration.hour,minutes=i.duration.minute,seconds=i.duration.second)
                occupied_slots.append((i.date,endtime))

        hours = (date.replace(hour=0,minute=0,second=0),date.replace(hour=23,minute=59,second=59))
        # print("ttttt  ",occupied_slots,duration,hours)
        free_slots = getslots(hours,occupied_slots,duration)
        # print(free_slots)
        return jsonify({'free_slots':free_slots},200)
    return jsonify({'message':'Slots Not Found'},401)


@app.route('/getshow',methods=['GET','POST'])
@token_required
def getshow(current_user):
    if request.method == 'GET':
        show = movieshow.query.all()
        show_list = []
        for s in show:
            show_list.append({'id':s.id,'movie':s.movie,'date':s.date,'price':s.price,'image':s.image,'description':s.description,'duration':s.duration,'current_capacity':s.current_capacity})
        return jsonify({'show':show_list},200)
    return jsonify({'message':'Show Not Found'},401)

@app.route('/getshow/<int:venue_id>/<int:isadmin>',methods=['GET','POST'])
@token_required
def getshowbyvenue(current_user,venue_id,isadmin):
    if request.method == 'GET':
        if isadmin == 1:
            show = movieshow.query.filter_by(venue_id=venue_id).all()
        else:
            print("usercall")
            show = movieshow.query.filter_by(venue_id=venue_id ,enabled=True).all()
        show_list = []
        for s in show:
            s.rating = s.rating.split('/')
            if s.rating[1] == '0':
                s.rating = 0
            else:
                s.rating = (float(s.rating[0])/float(s.rating[1]))*5
            print(s.date)
            show_list.append({'id':s.id,'movie':s.movie,'date':s.date,'price':s.price,'image':s.image,'description':s.description,'duration':s.duration,'current_capacity':s.current_capacity,'tags':s.tags,'rating':s.rating,'enabled':s.enabled})
        return jsonify({'show':show_list},200)
    return jsonify({'message':'Show Not Found'},401)



################################################### BOOKING APIs ########################################################

@app.route('/book',methods=['GET','POST'])
@token_required
@access_level([0])
def book(current_user):
    if request.method == 'POST':
        user_id = current_user.id
        show_id = request.form['show_id']
        show = movieshow.query.filter_by(id=show_id).first()
        quantity = request.form['quantity']
        if show.current_capacity == 0:
            return jsonify({'message':'Show Housefull'},401)
        total = int(quantity) * int(show.price)
        date = show.date
        time = show.time
        movie = show.movie
        venue = request.form['venue']
        status = 'Pending'

        booking = booking(user_id=user_id,show_id=show_id,quantity=quantity,total=total,date=date,time=time,movie=movie,venue=venue,status=status)
        db.session.add(booking)
        db.session.commit()
        return jsonify({'message':'Booking Done'},200)
    return jsonify({'message':'Booking Not Done'},401)

@app.route('/bookshow',methods=['GET','POST'])
@token_required
@access_level([0,2])
def bookshow(current_user):
    if request.method == 'POST':
        user_id = current_user.id
        show_id = int(request.form['show_id'])
        quantity = request.form['quantity']
        total = request.form['total']
        date =  datetime.strptime(request.form['date'], "%a, %d %b %Y %H:%M:%S %Z")
        movie = request.form['movie']
        venue = request.form['venue']
        status = 'Pending'
        show = movieshow.query.filter_by(id=show_id).first()
        show.current_capacity = show.current_capacity - int(quantity)
        db.session.commit()

        bookin = booking(user_id=user_id,show_id=show_id,quantity=quantity,total=total,date=date,movie=movie,venue=venue,status=status)
        db.session.add(bookin)
        db.session.commit()
        return jsonify({'message':'Booking Done'},200)
    return jsonify({'message':'Booking Not Done'},401)


@app.route('/getbooking',methods=['GET','POST'])
@token_required
@access_level([1,2])
def getbooking():
    if request.method == 'GET':
        booking = booking.query.all()
        booking_list = []
        for b in booking:
            booking_list.append({'id':b.id,'user_id':b.user_id,'show_id':b.show_id,'quantity':b.quantity,'total':b.total,'date':b.date,'time':b.time,'movie':b.movie,'venue':b.venue,'status':b.status})
        return jsonify({'booking':booking_list},200)
    return jsonify({'message':'Booking Not Found'},401)

@app.route('/getuserbooking',methods=['GET','POST'])
@token_required
@access_level([0,2])
def getuserbooking(current_user):
    if request.method == 'GET':
        user_id = current_user.id
        book = booking.query.filter_by(user_id=user_id).all()
        booking_list = []
        for b in book:
            booking_list.append({'id':b.id,'user_id':b.user_id,'show_id':b.show_id,'quantity':b.quantity,'total':b.total,'date':b.date,'movie':b.movie,'status':b.status,'rating':b.rating})
        return jsonify({'booking':booking_list},200)
    return jsonify({'message':'Booking Not Found'},401)

@app.route('/getchart',methods=['GET','POST'])
@token_required
@access_level([1,2])
def getchart(current_user):
    if request.method == 'POST':
        show_id = request.form['show_id']
        book = booking.query.filter_by(show_id=show_id).all()
        booking_list = []
        for b in book:
            booking_list.append({'id':b.id,'user_id':b.user_id,'show_id':b.show_id,'quantity':b.quantity,'total':b.total,'date':b.date,'movie':b.movie,'status':b.status,'rating':b.rating})
        return jsonify({'booking':booking_list},200)


if __name__ == '__main__':
    db.create_all()
    app.run(debug =True)

