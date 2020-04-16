import mysql.connector
import requests
import data

db = mysql.connector.connect(
	host = data.get_mysql_host(),
	user = data.get_mysql_user(),
	passwd = data.get_mysql_passwd(),
	database = data.get_mysql_database()
)

url = "https://swgoh.gg/api/characters/"
img_path = "https://swgoh.gg"
response_character = requests.get(url)

result_character = response_character.json()

for x in result_character:
	image = img_path + x["image"]
	cursor = db.cursor()
	sql = "UPDATE unit SET img_link = %s WHERE NameID = %s"
	val = (image, x["base_id"])
	cursor.execute(sql, val)
	db.commit()


url = "https://swgoh.gg/api/ships/"
response_ship = requests.get(url)

result_ship = response_ship.json()

for x in result_ship:
	image = img_path + x["image"]
	cursor = db.cursor()
	sql = "UPDATE unit SET img_link = %s WHERE NameID = %s"
	val = (image, x["base_id"])
	cursor.execute(sql, val)
	db.commit()