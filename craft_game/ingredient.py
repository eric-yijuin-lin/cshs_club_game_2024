from enum import Enum
from pygame import Rect, Surface, font

from common.game_data import GameItem
from common.inventory import UserInventory
from common.sprite import GameSprite
from assets.game_assets import icon_images, button_images

row_rect_templates: dict[str, tuple] = {
    "container": (80, 5, 245, 40),
    "icon": (85, 10, 25, 25),
    "left_arrow": (150, 15, 25, 25),
    "value_text": (185, 15, 105, 35),
    "right_arrow": (300, 15, 25, 25),
}

def get_shifted_rect(template: tuple, row_index: int) -> Rect:
    row_height = row_rect_templates["container"][3]
    return Rect(
        template[0],
        template[1] + row_index * row_height, # y = y + index * height
        template[2],
        template[3]
    )

font.init()
mideum_font = font.Font('assets/msjh.ttf', 14)
small_font = font.Font('assets/msjh.ttf', 10)

# need to refactor later, to synchronize ResourceType and MaterialType
class IngredientType(Enum):
    Nothing = 0
    Stone = 1
    Water = 2
    Wood = 3
    Food = 4
    Metal = 5
    Jewel = 6
    Item = 7

class CraftIngredient:
    def __init__(self, type: IngredientType, user_inventory: UserInventory) -> None:
        if type == IngredientType.Nothing:
            raise ValueError("cannot init a material object with 'Nothing' type")
        self.type = type
        self.use_amount = 0
        self.max_amount = 0
        self.available_items: list[GameItem] = []
        self.item_count = 0
        self.item_index = 0
        self.selected_item_1 = GameItem("", "", 0, "")
        self.selected_item_2 = GameItem("", "", 0, "")
        if type == IngredientType.Item:
            self.set_available_items(user_inventory.items)
        else:
            self.set_resources(user_inventory.resources)

    def set_resources(self, resources: list[int]) -> None:
        index = self.type.value - 1
        self.max_amount = resources[index]

    def set_available_items(self, items: list[GameItem]) -> None:
        if self.type != IngredientType.Item:
            raise ValueError("can not set items to a non-item material")
        self.available_items = items
        self.item_count = len(items)
        self.item_index = 0
        self.selected_item_1 = items[0]

    def change_amount(self, amount: int) -> None:
        if self.type == IngredientType.Item:
            raise ValueError("can not change amount of an item")
        self.use_amount += amount
        if self.use_amount < 0:
            self.use_amount = self.max_amount
        elif self.use_amount > self.max_amount:
            self.use_amount = 0

    def next_item(self, index_change: int) -> None:
        if self.type != IngredientType.Item:
            raise ValueError("can not change item id of resources")
        self.item_index += index_change
        self.item_index %= self.item_count
        self.selected_item_1 = self.available_items[self.item_index]


class IngredientRowSprite:
    def __init__(self, row_index: int, material_type: IngredientType, inventory: UserInventory) -> None:
        self.material = CraftIngredient(material_type, inventory)
        self.child_sprites: dict[str, GameSprite] = self.init_child_sprites(row_index, material_type)

    def init_child_sprites(self, row_index: int, material_type: IngredientType) -> dict:
        sprites = {}
        
        sprites["container"] = self.get_container_sprite(row_index)
        sprites["icon"] = self.get_icon_sprite(row_index, material_type)
        sprites["left_arrow"] = self.get_arrow_sprite(row_index, "left")
        sprites["right_arrow"] = self.get_arrow_sprite(row_index, "right")
        sprites["value_text"] = self.get_text_sprite(row_index)
        return sprites
    
    def get_container_sprite(self, row_index: int) -> dict:
        template = row_rect_templates["container"]
        image = Surface((template[2], template[3]))
        image.fill((255, 255, 255))
        rect = get_shifted_rect(template, row_index)
        return GameSprite(image, rect)

    def get_icon_sprite(self, row_index: int, ingred_type: IngredientType) -> GameSprite:
        icon_index = ingred_type.value - 1
        image = icon_images[icon_index]
        template = row_rect_templates["icon"]
        rect = get_shifted_rect(template, row_index)
        return GameSprite(image, rect)

    def get_arrow_sprite(self, row_index: int, direction: str) -> GameSprite:
        image: Surface = None
        template: tuple = None
        if direction == "left":
            image = button_images["left_arrow"]
            template = row_rect_templates["left_arrow"]
        elif direction == "right":
            image = button_images["right_arrow"]
            template = row_rect_templates["right_arrow"]
        else:
            raise ValueError("direction must be either left or right")
        rect = get_shifted_rect(template, row_index)
        return GameSprite(image, rect)
    
    def get_text_sprite(self, row_index: int) -> GameSprite:
        template = row_rect_templates["value_text"]
        text_surface = self.get_text_surface()
        rect = get_shifted_rect(template, row_index)
        return GameSprite(text_surface, rect)

    def update_text_sprite(self) -> None:
        self.child_sprites["value_text"].image = self.get_text_surface()
    
    def get_text_surface(self) -> Surface:
        value = str(self.material.use_amount)
        surface: Surface = None
        if self.material.type == IngredientType.Item:
            value = self.material.selected_item_1.name
        if len(value) < 8:
            surface = mideum_font.render(value, True, (0, 0, 0))
        else:
            surface = small_font.render(value, True, (0, 0, 0))
        return surface
    
    def is_left_arrow_clicked(self, child_scene_position: tuple) -> bool:
        left_arrow = self.child_sprites["left_arrow"]
        return left_arrow.is_clicked(child_scene_position)

    def is_right_arrow_clicked(self, child_scene_position: tuple) -> bool:
        right_arrow = self.child_sprites["right_arrow"]
        return right_arrow.is_clicked(child_scene_position)
