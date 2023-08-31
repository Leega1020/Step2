import mysql.connector.pooling
import json

dbconfig = {
    "database": "attractions",
    "user": "root",
    "host": "localhost",
    "password": "123",
}

connection_pool = mysql.connector.pooling.MySQLConnectionPool(**dbconfig)
con = connection_pool.get_connection()
cur = con.cursor()

cur.execute("CREATE TABLE attraction_Info (id INT PRIMARY KEY AUTO_INCREMENT,origin_id INT NOT NULL,name VARCHAR(255) NOT NULL,category VARCHAR(255) NOT NULL,description TEXT NOT NULL,address VARCHAR(255) NOT NULL,transport TEXT NOT NULL,mrt VARCHAR(255) NOT NULL,lat FLOAT NOT NULL,lng FLOAT NOT NULL)")
cur.execute("CREATE TABLE picture_urls (id INT PRIMARY KEY AUTO_INCREMENT,attraction_id INT,urls VARCHAR(255) NOT NULL,FOREIGN KEY (attraction_id) REFERENCES attraction_Info(id))")

mrt_list = []
with open("taipei-attractions.json") as file:
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
    if mrt is None:
        mrt = ""
    
    cur.execute("INSERT INTO attraction_Info(origin_id,name,category,description,address,transport,mrt,lat,lng) VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s)", (id,name,category,description,address,transport,mrt,lat,lng))
    cur.execute("SELECT LAST_INSERT_ID()")
    attraction_id=cur.fetchone()[0]
   
    link_list = i["file"].split("https://www.travel.taipei")
    images=["https://www.travel.taipei"+link for link in link_list if link and not link.endswith(".mp3")]
    
    
    for item in images:
        cur.execute("INSERT INTO picture_urls(attraction_id, urls) VALUES (%s,%s)",(attraction_id,item))
        con.commit()
con.close()
