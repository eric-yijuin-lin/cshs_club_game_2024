import csv
from pygame.image import load

card_images = {
    "stone_1_1": load("img/card_images/stone_1_1.png"),
    "water_1_1": load("img/card_images/water_1_1.png"),
    "wood_1_1": load("img/card_images/wood_1_1.png"),
    "food_1_1": load("img/card_images/food_1_1.png"),
    "metal_1_1": load("img/card_images/metal_1_1.png"),
    "jewel_1_1": load("img/card_images/jewel_1_1.png"),
}

icon_images = [
    load("img/stone_icon.png"),
    load("img/water_icon.png"),
    load("img/wood_icon.png"),
    load("img/food_icon.png"),
    load("img/metal_icon.png"),
    load("img/jewel_icon.png"),
    load("img/items_icon.png"),
]

coin_image = load("img/coin_icon.png")

tile_images = [
    load("img/mud_tile_revealed.png"),
    load("img/mud_tile.png"),
]

pickaxe_image = load("img/pickaxe.png")

button_images = {
    "mining_menu": load("img/mining_menu_button.png"),
    "craft_menu": load("img/craft_menu_button.png"),
    "rank_menu": load("img/rank_menu_button.png"),
    "left_arrow": load("img/left_arrow.png"),
    "right_arrow": load("img/right_arrow.png"),
    "confirm_craft": load("img/confirm_craft_button.png"),
}

card_teamplates = {
    "resource": {
        "stone": load("img/card_templates/resource_stone.png"),
        "water": load("img/card_templates/resource_water.png"),
        "wood": load("img/card_templates/resource_wood.png"),
        "food": load("img/card_templates/resource_food.png"),
        "metal": load("img/card_templates/resource_metal.png"),
        "jewel": load("img/card_templates/resource_jewel.png"),
    },
    "item": {
        "lv_1": load("img/card_templates/item_lv_1.png"),
        "lv_2": load("img/card_templates/item_lv_2.png"),
        "lv_3": load("img/card_templates/item_lv_3.png"),
        "lv_4": load("img/card_templates/item_lv_4.png"),
        "lv_5": load("img/card_templates/item_lv_5.png"),
    }
}


# key: 合成配方 (石頭, 水, 木材, 食物, 金屬, 珠寶, 物品1 ID, 物品2 ID)
# value: 合成出來的資源/物品 ID
recipe_csv = []
with open('recipes.csv', encoding="utf8") as f:
    reader = csv.reader(f, delimiter=',')
    column_num = 0
    for row in reader:
        if reader.line_num == 1:
            # print("表頭欄位：", row)
            pass
        else:
            recipe_csv.append(row)
            card_id = row[0]
            if not card_id in card_images:
                card_images[card_id] = load(f"img/card_images/{card_id}.png")