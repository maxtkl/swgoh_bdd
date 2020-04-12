import mysql.connector
import requests
import json
import sys
import data

# parameters to connect to db
db = mysql.connector.connect(
	host = data.get_mysql_host(),
	user = data.get_mysql_user(),
	passwd = data.get_mysql_passwd(),
	database = data.get_mysql_database()
)

# authentification to api.swgoh.help
headers_auth = {
	"method": "post",
	"content-type": "application/x-www-form-urlencoded"
}
data = data.get_swgoh_connection_data()


# sendin request to obtain the token
if len(sys.argv) > 2:
	token_str = "Bearer " +sys.argv[2]
else:
	auth = requests.post("https://api.swgoh.help/auth/signin", data=data, headers=headers_auth)
	token_str = "Bearer " + auth.json()["access_token"]

headers = {
	"method": "post",
	"content-type": "application/json",
	"Authorization": token_str
}

url_path = "https://api.swgoh.help/swgoh/"
ext = "players"
if len(sys.argv) > 1:
	payload = {
		"allycode":sys.argv[1],
		"languages":"fre_FR"
	}
else:
	print("Give the allycode of the member")

# sending post request and saving response as response object
response = requests.post(url_path+ext, data=json.dumps(payload), headers=headers)
result = response.json()[0]

allycode = result["allyCode"]
rank = result["arena"]["char"]["rank"]
fleet_rank = result["arena"]["ship"]["rank"]

cursor_update_char = db.cursor()
sql_update_char = "UPDATE player SET rank = (%s) WHERE allycode = (%s)"
val_update_char = (rank, allycode)
cursor_update_char.execute(sql_update_char, val_update_char)
db.commit()

cursor_update_ship = db.cursor()
sql_update_ship = "UPDATE player SET fleet_rank = (%s) WHERE allycode = (%s)"
val_update_ship = (fleet_rank, allycode)
cursor_update_ship.execute(sql_update_ship, val_update_ship)
db.commit()
print("rank and fleet rank update to " + str(rank) + " and " + str(fleet_rank))