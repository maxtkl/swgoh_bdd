# swgoh_bdd
Connect to swgoh.help api and store the data of the guild in database


**Installation :**

- Database creation
run
```bash
sudo chmod 755 database_creation.sh
./database_creation.sh
```

- Change the data in "data.py" by yours (you need an swgoh.help api account)
```bash
nano data.py
```

- Add "All_player_rank_unit.py" to your crontab (optional for automatic data collect)
```bash
crontab -e
```
Example with data download every hour at 15, insert in crontab:
```bash
15 * * * * python <path_to_folder>/swgoh_bdd/all_player_rank_unit.py <allycode>
```
You can instead put this line if you want also to keep a log of it.
```bash
15 * * * * python <path_to_folder>/swgoh_bdd/all_player_rank_unit.py <allycode> >> <path_to_folder>/cron.log 2>&1
```

**Usage :**

- run for a one time execution
```python
python all_player_rank_unit.py <allycode>
```