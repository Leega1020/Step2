from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_, func
from sqlalchemy.orm import relationship,joinedload

from flask import *

app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True

app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:12345678@localhost/attractions'
db = SQLAlchemy(app)

class Attraction(db.Model):
    __tablename__='attraction_Info'
    id=db.Column(db.Integer, primary_key=True)
    origin_id=db.Column(db.Integer)
    name=db.Column(db.String(255))
    category=db.Column(db.String(255))
    description=db.Column(db.Text)
    address=db.Column(db.Text)
    transport=db.Column(db.Text)
    mrt=db.Column(db.String(255))
    lat=db.Column(db.Float)
    lng=db.Column(db.Float)
    picture_urls = db.relationship('picture_urls', backref='attraction', lazy=True)

    def __init__(self,origin_id,name,category,description,address,transport,mrt,lat,lng):
        self.origin_id=origin_id
        self.name=name
        self.category=category
        self.description=description
        self.address=address
        self.transport=transport
        self.mrt=mrt
        self.lat=lat
        self.lng=lng
        
class picture_urls(db.Model):
    __tablename__ = 'picture_urls'
    id = db.Column(db.Integer,primary_key=True)
    attraction_id=db.Column(db.Integer,db.ForeignKey('attraction_Info.id'),nullable=False)
    urls= db.Column(db.String(255),nullable=False)

    def __init__(self,attraction_id,urls):
        self.attraction_id=attraction_id
        self.urls=urls

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

        response_data={
            "data":mrt_data
        }

        json_data=json.dumps(response_data,ensure_ascii=False).encode("utf-8")
        response=Response(json_data,content_type="application/json")
        return response
    except Exception as e:
        error_message="伺服器內部錯誤"
        response_data={
            "error":True,
            "message":error_message
        }
        json_data=json.dumps(response_data, ensure_ascii=False).encode('utf-8')
        response=Response(json_data, status=500, content_type="application/json")
        return response
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