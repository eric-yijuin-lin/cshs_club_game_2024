from enum import Enum

import pygame
from pygame import Surface
from common.game_data import GameItem, UserInventory
from craft_game.comfirm_component import ConfirmCraftComponent
from craft_game.ingredient import IngredientRowSprite, IngredientType
from craft_game.recipe import Card, CraftRecipe, craft_recipes
from common.scene_convert import get_child_scene_position
from common.card_composer import compose_card_surface
from assets.game_assets import button_images


SELL_BUTTON_RECT = pygame.Rect(5, 320, 75, 45)
COLLECT_BUTTON_RECT = pygame.Rect(345, 320, 75, 45)

class CraftStatus(Enum):
    Hiden = 0
    Running = 1
    SellOrCollect = 2

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
        self.crafted_card: Card = None
        self.show_craft_component = False
        self.craft_status = CraftStatus.Hiden
        self.saved_status = CraftStatus.Running
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
        if self.craft_status == CraftStatus.Hiden:
            return None
        for e in events:
                if e.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    self.process_click(pos)
        self.canvas.fill((255, 255, 255))
        if self.craft_status == CraftStatus.Running:
            for row in self.material_rows:
                self.blit_row(row)
            if self.craft_component.show:
                self.blit_craft_component()
        elif self.craft_status == CraftStatus.SellOrCollect:
            self.blit_card(self.crafted_card)
            self.blit_collect_sell_buttons()
        return self.canvas

    def blit_row(self, row: IngredientRowSprite) -> None:
        for sprite in row.child_sprites.values():
            self.canvas.blit(sprite.image, sprite.rect)

    def blit_craft_component(self) -> None:
        for sprite in self.craft_component.sprites.values():
            self.canvas.blit(sprite.image, sprite.rect)

    def blit_card(self, card: Card) -> None:
        card_surface = compose_card_surface(card)
        self.canvas.blit(card_surface, (80, 0))

    def process_click(self, global_position: tuple) -> None:
        position = get_child_scene_position(global_position, self.canvas_rect)
        if self.craft_status == CraftStatus.Running:
            row = self.get_clicked_row(position)
            if row:
                if row.is_left_arrow_clicked(position):
                    self.process_arrow_click(row, "left")
                    row.update_text_sprite()
                    self.update_recipe()
                elif row.is_right_arrow_clicked(position):
                    self.process_arrow_click(row, "right")
                    row.update_text_sprite()
                    self.update_recipe()
            elif self.craft_component.is_craft_button_clicked(position):
                crafted_card = self.process_craft_click()
                if crafted_card:
                    self.crafted_card = crafted_card
                    self.craft_status = CraftStatus.SellOrCollect
        elif self.craft_status == CraftStatus.SellOrCollect:
            done = self.process_collect_or_sell_click(position)
            if done:
                self.crafted_card = None
                self.refresh_material_rows()
                self.craft_status = CraftStatus.Running

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

    def process_craft_click(self) -> Card:
        if self.matched_recipe is None:
            raise ValueError("no matched recipe")
        if self.matched_recipe.coin_cost > self.inventory.coins:
            self.craft_component.update_message("金幣不足！")
            return None
        if not self.inventory.enough_ingredients(self.ingredients):
            self.craft_component.update_message("材料不足！")
            return None
        card = self.do_craft(self.inventory, self.matched_recipe)
        return card
    
    def process_collect_or_sell_click(self, child_scene_position) -> bool:
        if SELL_BUTTON_RECT.collidepoint(child_scene_position):
            coin_amount = self.crafted_card.sell_coin
            self.inventory.add_coins(coin_amount)
            return True
        elif COLLECT_BUTTON_RECT.collidepoint(child_scene_position):
            item = GameItem(self.crafted_card.id, self.crafted_card.name, self.crafted_card.level)
            self.inventory.add_item(item)
            return True
        return False

    def update_recipe(self) -> None:
        self.ingredients = self.get_selected_ingredients()
        if self.ingredients in craft_recipes:
            recipe = craft_recipes[self.ingredients]
            if recipe.is_craftable:
                print(f"recipe matched: {self.ingredients}")
                self.matched_recipe = craft_recipes[self.ingredients]
                self.craft_component.update_cost(self.matched_recipe.coin_cost)
                self.craft_component.show = True
        else:
            self.craft_component.show = False
            self.matched_recipe = None
    
    def get_selected_ingredients(self) -> tuple:
        ingredients = []
        for row in self.material_rows:
            if row.material.type == IngredientType.Item:
                ingredients.append(row.material.selected_item_1.id)
            else:
                ingredients.append(row.material.use_amount)
        return tuple(ingredients)

    def do_craft(self, inventory: UserInventory, recipe: CraftRecipe) -> Card:
        resources = recipe.ingredients[:6]
        item_id_1 = recipe.ingredients[6]
        item_id_2 = recipe.ingredients[7]
        coins = recipe.coin_cost
        inventory.consume_resources(resources)
        inventory.consume_item(item_id_1)
        inventory.consume_item(item_id_2)
        inventory.consume_coins(coins)
        return recipe.card
    
    def blit_collect_sell_buttons(self) -> None:
        self.canvas.blit(button_images["collect"], COLLECT_BUTTON_RECT.topleft)
        self.canvas.blit(button_images["sell"], SELL_BUTTON_RECT.topleft)

    def hide(self) -> None:
        self.saved_status = self.craft_status
        self.craft_status = CraftStatus.Hiden

    def activate(self) -> None:
        self.craft_status = self.saved_status
