import csv
from pygame.image import load
import os

card_images = {
    "stone_1_1": load("assets/img/card_images/stone_1_1.png"),
    "water_1_1": load("assets/img/card_images/water_1_1.png"),
    "wood_1_1": load("assets/img/card_images/wood_1_1.png"),
    "food_1_1": load("assets/img/card_images/food_1_1.png"),
    "metal_1_1": load("assets/img/card_images/metal_1_1.png"),
    "jewel_1_1": load("assets/img/card_images/jewel_1_1.png"),
    "secret": load("assets/img/card_images/secret.png"),
}

icon_images = [
    load("assets/img/stone_icon.png"),
    load("assets/img/water_icon.png"),
    load("assets/img/wood_icon.png"),
    load("assets/img/food_icon.png"),
    load("assets/img/metal_icon.png"),
    load("assets/img/jewel_icon.png"),
    load("assets/img/items_icon.png"),
]

coin_image = load("assets/img/coin_icon.png")

tile_images = [
    load("assets/img/mud_tile_revealed.png"),
    load("assets/img/mud_tile.png"),
]

pickaxe_image = load("assets/img/pickaxe.png")

button_images = {
    "mining_menu": load("assets/img/mining_menu_button.png"),
    "craft_menu": load("assets/img/craft_menu_button.png"),
    "rank_menu": load("assets/img/rank_menu_button.png"),
    "left_arrow": load("assets/img/left_arrow.png"),
    "right_arrow": load("assets/img/right_arrow.png"),
    "confirm_craft": load("assets/img/confirm_craft_button.png"),
    "collect": load("assets/img/collect_button.png"),
    "sell": load("assets/img/sell_button.png"),
}

card_teamplates = {
    "resource": {
        "stone": load("assets/img/card_templates/resource_stone.png"),
        "water": load("assets/img/card_templates/resource_water.png"),
        "wood": load("assets/img/card_templates/resource_wood.png"),
        "food": load("assets/img/card_templates/resource_food.png"),
        "metal": load("assets/img/card_templates/resource_metal.png"),
        "jewel": load("assets/img/card_templates/resource_jewel.png"),
    },
    "item": {
        "lv_1": load("assets/img/card_templates/item_lv_1.png"),
        "lv_2": load("assets/img/card_templates/item_lv_2.png"),
        "lv_3": load("assets/img/card_templates/item_lv_3.png"),
        "lv_4": load("assets/img/card_templates/item_lv_4.png"),
        "lv_5": load("assets/img/card_templates/item_lv_5.png"),
    }
}


# key: 合成配方 (石頭, 水, 木材, 食物, 金屬, 珠寶, 物品1 ID, 物品2 ID)
# value: 合成出來的資源/物品 ID
recipe_csv = []
with open('assets/recipes.csv', encoding="utf8") as f:
    reader = csv.reader(f, delimiter=',')
    column_num = 0
    for row in reader:
        if reader.line_num != 1:
            recipe_csv.append(row)
            card_id = row[0]
            if card_id not in card_images:
                card_images[card_id] = load(f"assets/img/card_images/{card_id}.png")