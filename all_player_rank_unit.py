import requests
import json
import sys
import subprocess
import data


# authentification to api.swgoh.help
headers_auth = {
	"method": "post",
	"content-type": "application/x-www-form-urlencoded"
}
data = data.get_swgoh_connection_data()

# sending request to obtain the token
auth = requests.post("https://api.swgoh.help/auth/signin", data=data, headers=headers_auth)
token = auth.json()["access_token"]
token_str = "Bearer " + token
headers = {
	"method": "post",
	"content-type": "application/json",
	"Authorization": token_str
}
url_path = "https://api.swgoh.help/swgoh/"
ext = "guilds"
if len(sys.argv) > 1:
	payload = {
		"allycode":sys.argv[1],
		"languages":"fre_FR"
	}
else:
	print("Give an allycode of a member of the guild")


# sending post request and saving response as response object
response = requests.post(url_path+ext, data=json.dumps(payload), headers=headers)
result = response.json()[0]["roster"]

subprocess.call("python /home/pi/Projet/swgoh.api/swgoh_bdd/player.py " + str(sys.argv[1]) + " " + str(token), shell=True)
subprocess.call("python /home/pi/Projet/swgoh.api/swgoh_bdd/guild.py " + str(sys.argv[1]) + " " + str(token), shell=True)

counter = 1
for x in result:
	print(x["name"].encode('utf8') + " is updating...  " + str(counter) + " / " + str(len(result)))
	counter = counter + 1
	subprocess.call("python /home/pi/Projet/swgoh.api/swgoh_bdd/player_rank.py " + str(x["allyCode"]) + " " + str(token), shell=True)
	subprocess.call("python /home/pi/Projet/swgoh.api/swgoh_bdd/unit.py " + str(x["allyCode"]) + " " + str(token), shell=True)