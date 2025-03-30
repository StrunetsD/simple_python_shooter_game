import json
from glom import glom

with open("json/waves.json", "r", encoding="utf-8") as file:
    data = json.load(file)
    waves = data["waves"]

with open("json/enemy.json", "r", encoding="utf-8") as file:
    enemy_data = json.load(file)

enemy_one = glom(enemy_data, 'enemy_one')
enemy_two = glom(enemy_data, 'enemy_two')
enemy_three = glom(enemy_data, 'enemy_three')
enemy_four = glom(enemy_data, 'enemy_four')
enemy_five = glom(enemy_data, 'enemy_five')

with open("json/player.json", "r", encoding="utf-8") as file:
    player_stat = json.load(file)

with open("json/weapon.json", "r", encoding="utf-8") as file:
    weapon_stat = json.load(file)

