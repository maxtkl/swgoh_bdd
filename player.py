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
	# print("Give the token for the authentification")


headers = {
	"method": "post",
	"content-type": "application/json",
	"Authorization": token_str
}
url = "https://api.swgoh.help/swgoh/guilds"

if len(sys.argv) > 1:
	payload = {
		"allycode":sys.argv[1],
		"languages":"fre_FR"
	}
else:
	print("Give an allycode of a member of the guild")

# sending post request and saving response as response object
response = requests.post(url, data=json.dumps(payload), headers=headers)
guild_name = response.json()[0]["name"]
result = response.json()[0]["roster"]
current_member = []

for x in result:
	current_member.append(x["allyCode"])
	exist = False
	sql_exist_already = "SELECT * FROM player"
	cursor_exist_already = db.cursor()
	cursor_exist_already.execute(sql_exist_already)
	result_already_exist = cursor_exist_already.fetchall()
	for (Xallycode,Xname,Xrank,Xfleet,Xguild,Xsquadron,Xleader_squad) in result_already_exist:
		if Xallycode == x["allyCode"]:
			exist = True
			break

	if exist:
		if Xguild == guild_name:
			print(Xname.encode('utf8') + " is already in database and update")
			pass
		else:
			cursor_update = db.cursor()
			sql_update = "UPDATE player SET guild_name = (%s) WHERE allycode = (%s)"
			val_update = (guild_name, Xallycode)
			cursor_update.execute(sql_update, val_update)
			db.commit()
			print("guild of the player update to " + guild_name)
	else:
		cursor = db.cursor()
		sql = "INSERT INTO player (allycode, name, guild_name,leader_squadron) VALUES (%s, %s, %s,%s)"
		val = (x["allyCode"], x["name"].lower(),guild_name,0)
		cursor.execute(sql, val)
		db.commit()
		print(x["name"] + " inserted.")

cursor_remove_extra_member = db.cursor()
sql_remove_extra_member = "SELECT * FROM player WHERE guild_name = '" + guild_name + "'"
val_remove_extra_member = guild_name
cursor_remove_extra_member.execute(sql_remove_extra_member, val_remove_extra_member)
result_remove_extra_member = cursor_remove_extra_member.fetchall()
for (Xallycode,Xname,Xrank,Xfleet,Xguild,Xsquadron,Xleader_squad) in result_remove_extra_member:
	if Xallycode not in current_member:
		cursor_remove_player = db.cursor()
		sql_remove_player = "UPDATE player SET guild_name = '' WHERE allycode = " + str(Xallycode)
		val_remove_player = (str(Xallycode))
		cursor_remove_player.execute(sql_remove_player)
		db.commit()
		print("guild of the player " + Xname.encode('utf8') + " is no more " + guild_name)