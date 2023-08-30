from flask import *
import json
from collections import Counter

app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True

data_list=[]
mrt_list=[]

def filter_attraction(attraction):
    id=attraction["_id"]
    name=attraction["name"]
    category=attraction["CAT"]
    description=attraction["description"]
    address=attraction["address"]
    transport=attraction["direction"]
    mrt=attraction["MRT"]
    lat=float(attraction["latitude"])
    lng=float(attraction["longitude"])
    link_list=attraction["file"].split("https://www.travel.taipei")
    images=["https://www.travel.taipei"+link for link in link_list if link and not link.endswith(".mp3")]
    
    if mrt:
        mrt_list.append(attraction["MRT"])

    return {
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
with open("data/taipei-attractions.json") as file:
    travel_data=json.load(file)
    attractions_list=travel_data["result"]["results"]
    data_list=[filter_attraction(attraction) for attraction in attractions_list]

mrt_counts=Counter(mrt_list)
most_common_mrt=mrt_counts.most_common()


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
        mrt_data=[mrt for mrt, _ in most_common_mrt]
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