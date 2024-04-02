from enum import Enum

import pygame
from pygame import Rect, Surface, font
from game_assets import icon_images, button_images, craft_recipes, coin_image
from game_data import GameItem, UserInventory
from recipe import CraftRecipe
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
        self.selected_item_1 = GameItem("", "", 0)
        self.selected_item_2 = GameItem("", "", 0)
        if type == IngredientType.Item:
            self.set_available_items(user_inventory.items)
        else:
            self.set_resources(user_inventory.recoures)

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

class ConfirmCraftComponent:
    def __init__(self) -> None:
        self.cost_font = font.Font('./msjh.ttf', 16)
        self.sprites: dict[str, GameSprite] = {}
        self.init_sprites()

    def init_sprites(self) -> None:   
        self.sprites["message_sprite"] = GameSprite(
            self.cost_font.render("發現可合成配方！", True, (0, 0, 0)),
            Rect(50, 330, 150, 40)
        )
        self.sprites["coin_icon_sprite"] = GameSprite(
            coin_image,
            Rect(200, 330, 30, 30)
        )
        self.sprites["cost_amount_sprite"] = GameSprite(
            self.cost_font.render("0", True, (0, 0, 0)),
            Rect(230, 330, 50, 40)
        )
        self.sprites["craft_button_sprite"] = GameSprite(
            button_images["confirm_craft"],
            Rect(300, 330, 30, 30)
        )
    
    def update_cost(self, amount: int) -> None:
        self.sprites["cost_amount_sprite"].image = self.cost_font.render(str(amount), True, (0, 0, 0))

    def is_craft_button_clicked(self, child_scene_position: tuple) -> bool:
        return self.sprites["craft_button_sprite"].is_clicked(child_scene_position)

class CraftManager:
    def __init__(self, rect: tuple, inventory: UserInventory) -> None:
        self.canvas_rect = rect
        self.canvas = Surface(
            (self.canvas_rect[2],
             self.canvas_rect[3])
        )
        self.inventory = inventory
        self.material_rows: list[IngredientRowSprite] = []
        self.ingredients: tuple = None
        self.matched_recipe: CraftRecipe = None
        self.show_craft_component = False
        self.craft_component = ConfirmCraftComponent()
        self.refresh_material_rows()

    def refresh_material_rows(self) -> None:
        ingred_types = [
            IngredientType.Stone,
            IngredientType.Water,
            IngredientType.Wood,
            IngredientType.Food,
            IngredientType.Metal,
            IngredientType.Jewel,
            IngredientType.Item,
            IngredientType.Item,
        ]
        self.material_rows = []
        for i in range(len(ingred_types)):
            ingred_type = ingred_types[i]
            row = IngredientRowSprite(i, ingred_type, self.inventory)
            self.material_rows.append(row)

    def process_frame(self, events: list) -> Surface:
        self.canvas.fill((255, 255, 255))
        for row in self.material_rows:
            self.blit_row(row)
        if self.show_craft_component:
            self.blit_craft_component()
        for e in events:
            if e.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                self.process_click(pos)
        return self.canvas

    def blit_row(self, row: IngredientRowSprite) -> None:
        for sprite in row.child_sprites.values():
            self.canvas.blit(sprite.image, sprite.rect)

    def blit_craft_component(self) -> None:
        for sprite in self.craft_component.sprites.values():
            self.canvas.blit(sprite.image, sprite.rect)

    def process_click(self, global_position: tuple) -> None:
        position = get_child_scene_position(global_position, self.canvas_rect)
        if self.show_craft_component:
            if self.craft_component.is_craft_button_clicked(position):
                self.process_craft_click()
                return
        row = self.get_clicked_row(position)
        if not row:
            return
        if row.is_left_arrow_clicked(position):
            self.process_arrow_click(row, "left")
        elif row.is_right_arrow_clicked(position):
            self.process_arrow_click(row, "right")

    def get_clicked_row(self, child_scene_position: tuple) -> IngredientRowSprite:
        for row in self.material_rows:
            if row.child_sprites["container"].is_clicked(child_scene_position):
                # row.child_sprites["container"].image.fill((255, 0, 0))
                return row
        return None
    
    def process_arrow_click(self, row: IngredientRowSprite, arrow: str) -> None:
        if row.material.type == IngredientType.Nothing:
            return
        if arrow == "left":
            if row.material.type == IngredientType.Item:
                row.material.next_item(-1)
            else:
                row.material.change_amount(-1)
        elif arrow == "right":
            if row.material.type == IngredientType.Item:
                row.material.next_item(1)
            else:
                row.material.change_amount(1)
        else:
            raise ValueError("unsupported arrow click")
        row.update_text_sprite()
        self.update_recipe()

    def process_craft_click(self) -> None:
        pass

    def enough_ingredients(self) -> bool:
        if not self.enough_resource():
            return False
        if not self.enough_items():
            return False
    
    def enough_resource(self) -> bool:
        resource_count = len(self.inventory.recoures)
        for i in range(resource_count):
            if self.ingredients[i] < self.inventory.recoures[i]:
                return False

    def enough_items(self) -> bool:
        id_1 = self.ingredients[6]
        id_2 = self.ingredients[7]
        item_1 = next((i for i in self.inventory.items if i.id == id_1), None)
        item_2 = next((i for i in self.inventory.items if i.id == id_2), None)
        if item_1 is None or item_2 is None:
            return False
        if item_1.count < 1 or item_2.count < 1:
            return False
        if id_1 == id_2 and item_1.count < 2:
            return False

    def update_recipe(self) -> None:
        self.ingredients = self.get_selected_ingredients()
        if self.ingredients in craft_recipes:
            recipe = craft_recipes[self.ingredients]
            if recipe.is_craftable:
                print(f"recipe matched: {self.ingredients}")
                self.matched_recipe = craft_recipes[self.ingredients]
                self.craft_component.update_cost(self.matched_recipe.money_cost)
                self.show_craft_component = True
        else:
            self.show_craft_component = False
            self.matched_recipe = None
    
    def get_selected_ingredients(self) -> tuple:
        ingredients = []
        for row in self.material_rows:
            if row.material.type == IngredientType.Item:
                ingredients.append(row.material.selected_item_1.id)
            else:
                ingredients.append(row.material.use_amount)
        return tuple(ingredients)
