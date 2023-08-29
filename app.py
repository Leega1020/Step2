from flask import *
import json
from collections import Counter

app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
data_list=[]
mrt_list=[]


with open("data/taipei-attractions.json") as file:
    travel_data=json.load(file)
    attractions_list=travel_data["result"]["results"]

for i in attractions_list:
    id=i["_id"]
    name=i["name"]
    category=i["CAT"]
    description=i["description"]
    address=i["address"]
    transport=i["direction"]
    mrt=i["MRT"]
    lat=float(i["latitude"])
    lng=float(i["longitude"])
    #print(mrt)
    if mrt is not None:
        mrt_list.append(i["MRT"])
    link_list=i["file"].split("https://www.travel.taipei")
    images=["https://www.travel.taipei"+link for link in link_list if link and not link.endswith(".mp3")]
    

    travel = {
        "id":id,
        "name":name,
        "category":category,
        "description":description,
        "address":address,
        "transport":transport,
        "mrt":mrt,
        "lat":lat,
        "lng":lng,
        "images":images
    }

    data_list.append(travel)

mrt_counts=Counter(mrt_list)
most_common_mrt=mrt_counts.most_common()

@app.route("/api/attraction",methods=['GET'])
def get_data_list():
    try:
        page=request.args.get('page',type=int,default=0)
        keyword=request.args.get('keyword',type=str)
        
        filtered_data=data_list
        if keyword:
            filtered_data=[attraction for attraction in filtered_data if keyword in attraction['name'] or (attraction['mrt'] is not None and keyword in attraction['mrt'])]

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
        most_common_mrt=mrt_counts.most_common()
        mrt_data=[mrt for mrt, _ in most_common_mrt]
        json_data=json.dumps({"data":mrt_data},ensure_ascii=False).encode('utf-8')
        response = Response(json_data, content_type="application/json;")
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