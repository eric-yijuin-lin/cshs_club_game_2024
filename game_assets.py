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
    "mining" : load("img/mining_button.png"),
    "synthesize" : load("img/synthesize_button.png"),
    "ranking" : load("img/ranking_button.png"),
    "left_arrow" : load("img/left_arrow.png"),
    "right_arrow" : load("img/right_arrow.png"),
}

sythesize_images = [
    load("img/material_empty.png"),
]

# pre-process images
sythesize_images[0].set_alpha(75)
