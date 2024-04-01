from pygame.image import load
from recipe import craft_recipes

card_images = [
    load("img/stone_1.png"),
    load("img/water_1.png"),
    load("img/wood_1.png"),
    load("img/food_1.png"),
    load("img/metal_1.png"),
    load("img/jewel_1.png"),
]

icon_images = [
    load("img/stone_icon.png"),
    load("img/water_icon.png"),
    load("img/wood_icon.png"),
    load("img/food_icon.png"),
    load("img/metal_icon.png"),
    load("img/jewel_icon.png"),
    load("img/items_icon.png"),
]

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
