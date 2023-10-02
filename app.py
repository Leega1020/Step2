from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_, func
from flask import *
from decouple import config
import jwt
from datetime import datetime, timedelta
from flask_cors import CORS
import mysql.connector.pooling

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.secret_key="akksso"
dbconfig = {
    "database": "attractions",
    "user": "root",
    "host": "localhost",
    "password": "12345678",
}
connection_pool = mysql.connector.pooling.MySQLConnectionPool(**dbconfig)

con = connection_pool.get_connection()
SECRET_KEY = config('SECRET_KEY')

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:12345678@localhost/attractions'
db = SQLAlchemy(app)

CORS(app)

class Attraction(db.Model):
    __tablename__ = 'attraction_Info'
    id = db.Column(db.Integer, primary_key=True)
    origin_id = db.Column(db.Integer)
    name = db.Column(db.String(255))
    category = db.Column(db.String(255))
    description = db.Column(db.Text)
    address = db.Column(db.Text)
    transport = db.Column(db.Text)
    mrt = db.Column(db.String(255))
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)
    picture_urls = db.relationship("picture_urls", backref="attraction", lazy=True)

    def __init__(self, origin_id, name, category, description, address, transport, mrt, lat, lng):
        self.origin_id = origin_id
        self.name = name
        self.category = category
        self.description = description
        self.address = address
        self.transport = transport
        self.mrt = mrt
        self.lat = lat
        self.lng = lng

class picture_urls(db.Model):
    __tablename__ = 'picture_urls'
    id = db.Column(db.Integer, primary_key=True)
    attraction_id = db.Column(db.Integer, db.ForeignKey('attraction_Info.id'), nullable=False)
    urls = db.Column(db.String(255), nullable=False)

    def __init__(self, attraction_id, urls):
        self.attraction_id = attraction_id
        self.urls = urls

class Schedule(db.Model):
    __tablename__ = 'schedule'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    attraction_id = db.Column(db.Integer, nullable=False)
    date = db.Column(db.String(255), nullable=False)
    time = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Integer, nullable=False)

    def __init__(self, attraction_id, date, time, price):
        self.attraction_id = attraction_id
        self.date = date
        self.time = time
        self.price = price


@app.route("/api/attractions",methods=["GET"])
def get_data_list():
    try:
        page=request.args.get("page",type=int,default=0)
        keyword=request.args.get("keyword",type=str)

        query=Attraction.query

        if keyword:
            query=query.filter(or_(Attraction.name.like(f"%{keyword}%"),Attraction.mrt.like(f"%{keyword}%")))

        single_page=12
        data=query.limit(single_page).offset(page*single_page).all()

        data_list = []
        
        for attraction in data:
            picture_urls_data=picture_urls.query.filter_by(attraction_id=attraction.id).all()
            picture_urls_list=[image.urls for image in picture_urls_data]
           
            data_list.append({
                "id":attraction.id,
                "name":attraction.name,
                "category":attraction.category,
                "description":attraction.description,
                "address":attraction.address,
                "transport":attraction.transport,
                "mrt":attraction.mrt,
                "lat":attraction.lat,
                "lng":attraction.lng,
                "images":picture_urls_list 
            })

        next_page=page+1 if len(data)==single_page else None

        response_data={
            "nextPage":next_page,
            "data":data_list
        }

        json_data=json.dumps(response_data,ensure_ascii=False).encode("utf-8")
        response=Response(json_data,content_type="application/json;")
        return response
        #return jsonify({response_data})
    except Exception as e:
        error_message="伺服器內部錯誤"
        response_data={
            "error":True,
            "message":error_message
        }
        json_data=json.dumps(response_data,ensure_ascii=False).encode("utf-8")
        response=Response(json_data,status=500,content_type="application/json")
        return response

@app.route("/api/attraction/<attractionId>",methods=["GET"])
def search_attraction_id(attractionId):
    try:
        attraction=Attraction.query.filter_by(id=attractionId).first()
        if attraction:
            picture_urls_data=picture_urls.query.filter_by(attraction_id=attraction.id).all()
            picture_urls_list=[image.urls for image in picture_urls_data]

            attraction_data={
                "id":attraction.id,
                "name":attraction.name,
                "category":attraction.category,
                "description":attraction.description,
                "address":attraction.address,
                "transport":attraction.transport,
                "mrt":attraction.mrt,
                "lat":attraction.lat,
                "lng":attraction.lng,
                "images":picture_urls_list
            }
            json_data=json.dumps(attraction_data,ensure_ascii=False).encode("utf-8")
            response=Response(json_data,content_type="application/json")
            return response
        else:
            error_message="景點編號不正確"
            response_data={
                "error":True,
                "message":error_message
            }
            json_data=json.dumps(response_data,ensure_ascii=False).encode("utf-8")
            response=Response(json_data,status=400,content_type="application/json")
            return response


    except Exception as e:
        error_message="伺服器內部錯誤"
        response_data={
            "error":True,
            "message":error_message
        }
        json_data=json.dumps(response_data,ensure_ascii=False).encode('utf-8')
        response=Response(json_data,status=500,content_type="application/json")
        return response

@app.route("/api/mrts")
def get_mrts():
    try:
        mrt_counts=db.session.query(Attraction.mrt,func.count().label('count')).filter(Attraction.mrt!="").group_by(Attraction.mrt).order_by(func.count().desc()).all()
        mrt_data=[mrt[0] for mrt in mrt_counts]

        max_mrt_display=31
        if len(mrt_data)>max_mrt_display:
            mrt_data=mrt_data[:max_mrt_display+1]

        #response_data={
           # "data":mrt_data
        #}

        #json_data=json.dumps(response_data,ensure_ascii=False).encode("utf-8")
        #response=Response(json_data,content_type="application/json")
        #return response
        return jsonify({"data":mrt_data})
    except Exception as e:
        error_message="伺服器內部錯誤"
        response_data={
            "error":True,
            "message":error_message
        }
        json_data=json.dumps(response_data, ensure_ascii=False).encode('utf-8')
        response=Response(json_data, status=500, content_type="application/json")
        return response
    
@app.route("/api/user",methods=["POST"])
def getSignup():
    try:
        signUpName=request.json.get("name")
        signUpEmail=request.json.get("email")
        signUpPassword=request.json.get("password")

        cur=con.cursor()
        cur.execute("SELECT*FROM member WHERE email=%s",(signUpEmail,))
        result=cur.fetchone()

        if result:
            message="註冊失敗，重複的 Email 或其他原因"
            return jsonify({"error": True, "message": message}),400
        else:
            cur.execute("INSERT INTO member (name, email, password) VALUES (%s, %s, %s)",
                        (signUpName, signUpEmail, signUpPassword))
            con.commit()  
            return jsonify({"ok": True})
    except Exception as e:
        error_message="伺服器內部錯誤"
        response_data={
            "error":True,
            "message":error_message
        }
        return jsonify(response_data),500




@app.route("/api/user/auth",methods=["PUT"])
def handleSignin():
    try:
        signInEmail = request.json.get("email")
        signInPassword = request.json.get("password")
    
        cur=con.cursor()
        cur.execute("SELECT * FROM member WHERE email=%s AND password=%s", (signInEmail, signInPassword))
        result=cur.fetchone()
        exp=datetime.utcnow()+timedelta(days=7)
        if result:
            data = {
                "id":result[0],
                "name":result[1],
                "email":result[2],
                "exp":exp
            }
            token=jwt.encode(data,SECRET_KEY,algorithm='HS256')
            response_data={
                "token":token
            }
            return jsonify(response_data),200
        else:
            return jsonify({"error": True,"message":"登入失敗，帳號或密碼錯誤或其他原因"}),400

    except Exception as e:
        return jsonify({"error":True,"message":"伺服器內部錯誤"}),500


@app.route("/api/user/auth",methods=["GET"])
def handleAuth():
    token=request.headers.get('Authorization').split(' ')[1] 
    
    if token is None:
        response_data={
            "data":None
        }
        return jsonify(response_data),200
    else:
        try:
            decoded_token=jwt.decode(token,SECRET_KEY,algorithms=["HS256"])
            user_id=decoded_token.get("id")
            user_name=decoded_token.get("name")
            user_email=decoded_token.get("email")
            session["userName"]=user_name
            response_data={
                "data":{
                    "id":user_id,
                    "name":user_name,
                    "email":user_email
                }
            }
            return jsonify(response_data),200
        
        except Exception as e:
            response_data={
                "data":None
            }
            return jsonify(response_data),200
        
@app.route("/api/booking",methods=["POST"])
def getBookingInfo():
    token=request.headers.get('Authorization').split(' ')[1]
  
    if token is None:
        error_message = "未登入系統，拒絕存取"
        return jsonify({
            "error": True,
            "message": error_message
        }),403
    else:
        attractionId=request.json.get("id")
        date=request.json.get("date")
        time=request.json.get("time")
        price=int(request.json.get("price"))
        userName=session.get("userName")
       
        try:
            cur = con.cursor()
            cur.execute("SELECT*FROM schedule WHERE user_name=%s",(userName,))
            existing_booking=cur.fetchone()
            cur.execute("SELECT*FROM attraction_Info WHERE id = %s",(attractionId,))
            attractionData=cur.fetchone()
            
            if attractionData:
                attraction_name=attractionData[2]
                attraction_address=attractionData[5]
                cur.execute("SELECT urls FROM picture_urls WHERE attraction_id=%s LIMIT 1",(attractionId,))
                image_url=cur.fetchone()
                attraction_image=image_url[0]
               
                if existing_booking:
                    cur.execute("UPDATE schedule SET attraction_id=%s,name=%s,address=%s,image=%s,time=%s,price=%s,date=%s WHERE user_name=%s",(attractionId,attraction_name,attraction_address,attraction_image,time,price,date,userName))
                    con.commit()
                    response_data={
                        "attractionId":attractionId,
                        "date":date,
                        "time":time,
                        "price":price
                    }
                    return jsonify(response_data)
                else:
                    cur.execute("INSERT INTO schedule(attraction_id,name,address,image,time,price,date,user_name) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",(attractionId,attraction_name,attraction_address,attraction_image,time,price,date,userName))
                    response_data={
                        "attractionId":attractionId,
                        "date":date,
                        "time":time,
                        "price":price
                    }
                    con.commit()
                    print(response_data)
                    return jsonify(response_data)
            else:
                error_message="建立失敗，輸入不正確或其他原因"
                return jsonify({
                    "error": True,
                    "message": error_message
                }),400
        except Exception as e:
            error_message="伺服器內部錯誤"
            return jsonify({
                    "error": True,
                    "message": error_message
                }),500

      

@app.route("/api/booking",methods=["GET"])
def getBooking():
    token=request.headers.get('Authorization').split(' ')[1] 
    #user_name = request.headers.get("User-Name")
    user_name=session.get("userName")
    if token is None or user_name is None:
        error_message = "未登入系統，拒絕存取"
        return jsonify({
            "error":True,
            "message":error_message
        }),403
    else:
        cur=con.cursor()
        cur.execute("SELECT*FROM schedule WHERE user_name=%s",(user_name,))
        scheduleData=cur.fetchone()
        if scheduleData:
            response_data = {
                "data":{
                    "attraction": 
                        {"id":scheduleData[1],
                        "name":scheduleData[2],
                        "address":scheduleData[3],
                        "image":scheduleData[4]},
                    "date":scheduleData[5] ,
                    "time":scheduleData[6],
                    "price":scheduleData[7]
                }
            }
        else:
            response_data = {
                "data": None
            }    
        return jsonify(response_data),200

    
@app.route("/api/booking",methods=["DELETE"])
def deleteBooking():
    token = request.headers.get('Authorization').split(' ')[1]
    #userName = request.headers.get("User-Name")
    userName=session.get("userName")
    if token:
        cur = con.cursor()
        cur.execute("DELETE FROM schedule WHERE user_name=%s",(userName,))
        con.commit()
        return jsonify({"ok":True})
    else:
        error_message = "未登入系統，拒絕存取"
        return jsonify({
            "error": True,
            "message": error_message
        }),403
    

# Pages
@app.route("/")
def index():
	return render_template("index.html")
@app.route("/attraction/<id>")
def attraction(id):
	return render_template("attraction.html")
@app.route("/booking")
def booking():
	return render_template("booking.html")
@app.route("/thankyou")
def thankyou():
	return render_template("thankyou.html")
    
app.run(host="0.0.0.0",port=3000)