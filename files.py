import json

with open("json/waves.json", "r", encoding="utf-8") as file:
    data = json.load(file)
    waves = data["waves"]

with open("json/enemy.json", "r", encoding="utf-8") as file:
    enemy_stat = json.load(file)

with open("json/player.json", "r", encoding="utf-8") as file:
    player_stat = json.load(file)

with open("json/weapon.json", "r", encoding="utf-8") as file:
    weapon_stat = json.load(file)
