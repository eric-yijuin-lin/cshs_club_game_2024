from enum import Enum

import pygame
from pygame import Rect, Surface, font
from game_assets import icon_images, button_images
from game_data import GameItem, UserInventory
from scene_convert import get_child_scene_position
from sprite import GameSprite

row_rect_templates: dict[str, tuple] = {
    "container": (80, 5, 245, 40),
    "icon": (85, 10, 25, 25),
    "left_arrow": (150, 15, 25, 25),
    "value_text": (185, 15, 105, 35),
    "right_arrow": (300, 15, 25, 25),
}

font.init()
mideum_font = font.Font('./msjh.ttf', 14)
small_font = font.Font('./msjh.ttf', 10)

def get_shifted_rect(template: tuple, row_index: int) -> Rect:
    row_height = row_rect_templates["container"][3]
    return Rect(
        template[0],
        template[1] + row_index * row_height, # y = y + index * height
        template[2],
        template[3]
    )


# need to refactor later, to synchronize ResourceType and MaterialType
class MaterialType(Enum):
    Nothing = 0
    Stone = 1
    Water = 2
    Wood = 3
    Food = 4
    Metal = 5
    Jewel = 6
    Item = 7
    
class SynthesizeMaterial:
    def __init__(self, type: MaterialType, user_inventory: UserInventory) -> None:
        if type == MaterialType.Nothing:
            raise ValueError("cannot init a material object with 'Nothing' type")
        self.type = type
        self.use_amount = 0
        self.max_amount = 0
        self.available_items: list[GameItem] = []
        self.item_count = 0
        self.item_index = 0
        self.selected_item = GameItem("empty", "", 0)
        if type == MaterialType.Item:
            self.set_available_items(user_inventory.items)
        else:
            self.set_resources(user_inventory.recoures)

    def set_resources(self, resources: list[int]) -> None:
        index = self.type.value - 1
        self.max_amount = resources[index]

    def set_available_items(self, items: list[GameItem]) -> None:
        if self.type != MaterialType.Item:
            raise ValueError("can not set items to a non-item material")
        self.available_items = items
        self.item_count = len(items)
        self.item_index = 0
        self.selected_item = items[0]

    def change_amount(self, amount: int) -> None:
        if self.type == MaterialType.Item:
            raise ValueError("can not change amount of an item")
        self.use_amount += amount
        if self.use_amount < 0:
            self.use_amount = self.max_amount
        elif self.use_amount > self.max_amount:
            self.use_amount = 0

    def next_item(self, index_change: int) -> None:
        if self.type != MaterialType.Item:
            raise ValueError("can not change item id of resources")
        self.item_index += index_change
        self.item_index %= self.item_count
        self.selected_item = self.available_items[self.item_index]

class MaterialRowSprite:
    def __init__(self, material_type: MaterialType, inventory: UserInventory) -> None:
        self.material = SynthesizeMaterial(material_type, inventory)
        self.child_sprites: dict[str, GameSprite] = self.init_child_sprites(material_type)

    def init_child_sprites(self, material_type: MaterialType) -> dict:
        sprites = {}
        row_index = material_type.value - 1
        sprites["container"] = self.get_container_sprite(row_index)
        sprites["icon"] = self.get_icon_sprite(row_index)
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

    def get_icon_sprite(self, row_index: int) -> GameSprite:
        image = icon_images[row_index]
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
        if self.material.type == MaterialType.Item:
            value = self.material.selected_item.name
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
    
class SynthesizeManager:
    def __init__(self, rect: tuple, inventory: UserInventory) -> None:
        self.canvas_rect = rect
        self.canvas = Surface(
            (self.canvas_rect[2],
             self.canvas_rect[3])
        )
        self.inventory = inventory
        self.material_rows: list[MaterialRowSprite] = []
        self.item_dict: dict[str, str] = {}
        self.refresh_material_rows()

    def refresh_material_rows(self) -> None:
        self.material_rows = []
        for m in MaterialType:
            if m == MaterialType.Nothing:
                continue
            row = MaterialRowSprite(m, self.inventory)
            self.material_rows.append(row)

    def process_frame(self, events: list) -> Surface:
        self.canvas.fill((255, 255, 255))
        for row in self.material_rows:
            self.blit_row(row)
        for e in events:
            if e.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                self.process_click(pos)
        return self.canvas

    def blit_row(self, row: MaterialRowSprite) -> None:
        for sprite in row.child_sprites.values():
            self.canvas.blit(sprite.image, sprite.rect)

    def process_click(self, global_position: tuple) -> None:
        child_scene_position = get_child_scene_position(global_position, self.canvas_rect)
        row = self.get_clicked_row(child_scene_position)
        if not row:
            return
        if row.is_left_arrow_clicked(child_scene_position):
            self.process_arrow_click(row, "left")
        elif row.is_right_arrow_clicked(child_scene_position):
            self.process_arrow_click(row, "right")

    def get_clicked_row(self, child_scene_position: tuple) -> MaterialRowSprite:
        for row in self.material_rows:
            if row.child_sprites["container"].is_clicked(child_scene_position):
                # row.child_sprites["container"].image.fill((255, 0, 0))
                return row
        return None
    
    def process_arrow_click(self, row: MaterialRowSprite, arrow: str) -> None:
        if row.material.type == MaterialType.Nothing:
            return
        if arrow == "left":
            if row.material.type == MaterialType.Item:
                row.material.next_item(-1)
            else:
                row.material.change_amount(-1)
        elif arrow == "right":
            if row.material.type == MaterialType.Item:
                row.material.next_item(1)
            else:
                row.material.change_amount(1)
        row.update_text_sprite()
