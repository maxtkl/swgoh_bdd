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
auth = requests.post("https://api.swgoh.help/auth/signin", data=data, headers=headers_auth)
#print("auth: ", auth.json()["access_token"])
token = "Bearer " + auth.json()["access_token"]

headers = {
	"method": "post",
	"content-type": "application/json",
	"Authorization": token
}
url_path = "https://api.swgoh.help/swgoh/"
ext = "guilds"

if len(sys.argv) > 1:
	payload = {
		"allycode":sys.argv[1],
		"languages":"fre_FR"
	}
else:
	print("Give an allycode of a member of the guilde to add")

# sending post request and saving response as response object
response = requests.post(url_path+ext, data=json.dumps(payload), headers=headers)
result = response.json()[0]
guild_name = result["name"]
nb_members = result["members"]

## insertion of the guild info to db
exist = False
sql_exist_already = "SELECT * FROM guild"
cursor_exist_already = db.cursor()
cursor_exist_already.execute(sql_exist_already)
result = cursor_exist_already.fetchall()
for x in result:
  if x[1] == guild_name:
  	exist = True
  	db_nb_members = x[2]

if exist:
	if db_nb_members == nb_members:
		print(guild_name + " is already in database and updated")
	else:
		cursor_update = db.cursor()
		sql_update = "UPDATE guild SET nb_member = (%s) WHERE name = (%s)"
		val_update = (nb_members, guild_name)
		cursor_update.execute(sql_update, val_update)
		db.commit()
		print("number of member update to " + str(nb_members))
else:
	cursor = db.cursor()
	sql = "INSERT INTO guild (name, nb_member) VALUES (%s, %s)"
	val = (guild_name, nb_members)
	cursor.execute(sql, val)
	db.commit()
	print(str(cursor.rowcount) + " record inserted.")