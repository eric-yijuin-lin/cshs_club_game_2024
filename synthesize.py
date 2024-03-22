from enum import Enum

import pygame
from pygame import Rect, Surface, font
from game_assets import icon_images, button_images
from game_data import UserResource
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
    def __init__(self, type = MaterialType) -> None:
        self.type = type
        self.amount = 0
        self.item_id = "debug_1"
        self.item_name = "阿姆斯特朗旋風噴射"

    def change_amount(self, amount: int) -> None:
        if self.type == MaterialType.Item:
            raise ValueError("can not change amount of an item")
        self.amount += amount
        if self.amount < 0:
            self.amount = 0
        elif self.amount > 9999:
            self.amount = 9999

    def change_item(self, item: dict[str, str]) -> None:
        if self.material.type != MaterialType.Item:
            raise ValueError("can not change item id of resources")
        self.item_id = item["id"]
        self.item_name = item["name"]

class MaterialRowSprite:
    def __init__(self, material_type: MaterialType) -> None:
        self.material = SynthesizeMaterial(material_type)
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
        value = str(self.material.amount)
        text_surface: Surface = None
        if self.material.type == MaterialType.Item:
            value = self.material.item_name
        if len(value) < 8:
            text_surface = mideum_font.render(value, True, (0, 0, 0))
        else:
            text_surface = small_font.render(value, True, (0, 0, 0))
        template = row_rect_templates["value_text"]
        rect = get_shifted_rect(template, row_index)
        return GameSprite(text_surface, rect)
    
class SynthesizeManager:
    def __init__(self, rect: tuple, user_resources: UserResource) -> None:
        self.canvas_rect = rect
        self.canvas = Surface(
            (self.canvas_rect[2],
             self.canvas_rect[3])
        )
        self.material_rows: list[MaterialRowSprite] = []
        self.init_material_rows()

    def init_material_rows(self) -> None:
        for m in MaterialType:
            if m == MaterialType.Nothing:
                continue
            row = MaterialRowSprite(m)
            self.material_rows.append(row)

    def process_frame(self, events: list) -> Surface:
        self.canvas.fill((255, 255, 255))
        for row in self.material_rows:
            self.blit_row(row)
        for e in events:
            if e.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                self.get_clicked_row(pos)
        return self.canvas

    def blit_row(self, row: MaterialRowSprite) -> None:
        for sprite in row.child_sprites.values():
            self.canvas.blit(sprite.image, sprite.rect)

    def get_clicked_row(self, position: tuple) -> MaterialRowSprite:
        main_screen_position = pygame.mouse.get_pos()
        child_scene_position = get_child_scene_position(main_screen_position, self.canvas_rect)
        for row in self.material_rows:
            if row.child_sprites["container"].is_clicked(child_scene_position):
                # row.child_sprites["container"].image.fill((255, 0, 0))
                return row
