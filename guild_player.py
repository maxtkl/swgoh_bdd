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


# sending request to obtain the token
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


sql_remove_extra_member = "SELECT * FROM player"
val_remove_extra_member = guild_name
cursor_remove_extra_member.execute(sql_remove_extra_member)
result_remove_extra_member = cursor_remove_extra_member.fetchall()
for (Xallycode,Xname,Xrank,Xfleet,Xguild,Xsquadron,Xleader_squad) in result_remove_extra_member: