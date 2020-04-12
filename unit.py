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
	arg_allycode = sys.argv[1]
	payload = {
		"allycode":arg_allycode,
		"languages":"fre_FR"
	}
else:
	print("Give the allycode of the member")

# sending post request and saving response as response object
response = requests.post(url_path+ext, data=json.dumps(payload), headers=headers)
result = response.json()[0]["roster"]

# print(json.dumps(result[0], sort_keys=True, indent=2))

print("unit updating ...")
for x in result:
	sql_unit = "SELECT * FROM unit WHERE allycode = (%s) AND name = (%s)"
	val_unit = (arg_allycode, x["nameKey"])
	cursor_unit = db.cursor()
	cursor_unit.execute(sql_unit, val_unit)
	result = cursor_unit.fetchall()
	if len(result) > 0:
		if (x["gear"] == 13 and x["gear"] == result[0][3] and x["rarity"] == result[0][4] and x["gp"] == result[0][5] and (x["relic"]["currentTier"] - 2) == result[0][6]) or (x["gear"] != 13 and x["gear"] == result[0][3] and x["rarity"] == result[0][4] and x["gp"] == result[0][5]):
			#print(x["nameKey"] + " already exists and is update")
			pass
		else:
			cursor_update_unit = db.cursor()
			sql_update_unit = "UPDATE unit SET gear = (%s) WHERE allycode = (%s) AND name = (%s)"
			val_update_unit = (x["gear"], arg_allycode, x["nameKey"])
			cursor_update_unit.execute(sql_update_unit, val_update_unit)
			db.commit()
			cursor_update_unit = db.cursor()
			sql_update_unit = "UPDATE unit SET star = (%s) WHERE allycode = (%s) AND name = (%s)"
			val_update_unit = (x["rarity"], arg_allycode, x["nameKey"])
			cursor_update_unit.execute(sql_update_unit, val_update_unit)
			db.commit()
			cursor_update_unit = db.cursor()
			sql_update_unit = "UPDATE unit SET power = (%s) WHERE allycode = (%s) AND name = (%s)"
			val_update_unit = (x["gp"], arg_allycode, x["nameKey"])
			cursor_update_unit.execute(sql_update_unit, val_update_unit)
			db.commit()
			if x["gear"] == 13:
				cursor_update_unit = db.cursor()
				sql_update_unit = "UPDATE unit SET relic = (%s) WHERE allycode = (%s) AND name = (%s)"
				val_update_unit = ((x["relic"]["currentTier"] - 2), arg_allycode, x["nameKey"])
				cursor_update_unit.execute(sql_update_unit, val_update_unit)
				db.commit()
				# print(x["nameKey"] + " is updated")
	else:
		cursor = db.cursor()
		if x["gear"] == 13:
			relic = x["relic"]["currentTier"] - 2
		else:
			relic = 0
		sql = "INSERT INTO unit (name, allycode, gear, star, power) VALUES (%s, %s, %s, %s, %s)"
		val = (x["nameKey"].lower(), arg_allycode,x["gear"], x["rarity"], x["gp"])
		cursor.execute(sql, val)
		db.commit()
		# print(x["nameKey"].encode('utf8') + " inserted.")