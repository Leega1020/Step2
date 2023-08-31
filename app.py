from flask import *
import json
from collections import Counter
import mysql.connector.pooling


app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True

data_list=[]
mrt_list=[]
attractions_list=[]
dbconfig = {
    "database": "attractions",
    "user": "root",
    "host": "localhost",
    "password": "12345678",
}

connection_pool = mysql.connector.pooling.MySQLConnectionPool(**dbconfig)
con = connection_pool.get_connection()
cur = con.cursor()
cur.execute("SELECT*FROM attraction_Info")
all_data=cur.fetchall()


for i in all_data:
    travel_data= {
        "id":i[0],
        "name":i[2],
        "category":i[3],
        "description":i[4],
        "address":i[5],
        "transport":i[6],
        "mrt":i[7],
        "lat":i[8],
        "lng":i[9],
    }
    cur.execute("SELECT urls FROM picture_urls WHERE attraction_id=%s",(i[0],))
    picture_data=cur.fetchall()
    image_urls=[row[0] for row in picture_data]
    travel_data["images"]=image_urls
    cur.execute("SELECT mrt FROM attraction_Info")
    mrt=cur.fetchall()
    most_common_mrt=Counter(mrt).most_common()
    data_list.append(travel_data)

@app.route("/api/attractions",methods=['GET'])
def get_data_list():
    try:
        page=request.args.get('page',type=int,default=0)
        keyword=request.args.get('keyword',type=str)
        
        filtered_data=data_list
        if keyword:
            filtered_data=[attraction for attraction in filtered_data if keyword in attraction["name"] or (attraction["mrt"] is not None and keyword in attraction["mrt"])]

        single_page=12
        all_items=len(filtered_data)
        all_pages=all_items/single_page 

        start_index=page*single_page
        end_index=start_index+single_page
        single_data=filtered_data[start_index:end_index]

        if page<all_pages-1:
            next_page=page+1
        else:next_page=None
    
        travel={
            "nextPage":next_page,
            "data":single_data    
        }

        json_data=json.dumps(travel,ensure_ascii=False).encode('utf-8')
        response=Response(json_data,content_type="application/json;")
        return response
    except Exception as e:
        error_message="伺服器內部錯誤"
        response_data={
        "error":True,
        "message":error_message}
        json_data=json.dumps(response_data,ensure_ascii=False).encode('utf-8')
        response=Response(json_data,status=500,content_type="application/json")
        return response
       

@app.route("/api/attraction/<attractionId>",methods=['GET'])
def search_attractionId(attractionId):
    try:
        attraction=None 
        for item in data_list:
            if item["id"]==int(attractionId):
                attraction=item
                
        if attraction:
            json_data=json.dumps({"data":attraction},ensure_ascii=False).encode('utf-8')
            response=Response(json_data,content_type="application/json;")
            return response
        else:
            error_message="景點編號不正確"
            response_data={
            "error":True,
            "message":error_message}
            json_data=json.dumps(response_data,ensure_ascii=False).encode('utf-8')
            response=Response(json_data,status=400,content_type="application/json")
            return response
       
    except Exception as e:
        error_message="伺服器內部錯誤"
        response_data={
        "error":True,
        "message":error_message}
        json_data=json.dumps(response_data,ensure_ascii=False).encode('utf-8')
        response=Response(json_data,status=500,content_type="application/json")
        return response
    
@app.route("/api/mrts")
def get_mrts():
    try:
        
        
        
        max_mrt_display=31
        if len(mrt_data)>max_mrt_display:
            json_data=json.dumps({"data":mrt_data[0:max_mrt_display+1]},ensure_ascii=False).encode('utf-8')
            response = Response(json_data,content_type="application/json;")
            return response
    except Exception as e:
        error_message="伺服器內部錯誤"
        response_data={
        "error":True,
        "message":error_message}
        json_data=json.dumps(response_data,ensure_ascii=False).encode('utf-8')
        response=Response(json_data,status=500,content_type="application/json")
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

app.run(host="0.0.0.0", port=3000)