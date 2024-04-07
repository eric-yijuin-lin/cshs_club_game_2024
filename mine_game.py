import pygame
from enum import Enum
from random import randint, uniform
from game_assets import tile_images, pickaxe_image, button_images
from game_data import Card, UserInventory, ResourceType
from scene_convert import get_child_scene_position
from card_composer import compose_card_surface
from recipe import primitive_cards

class MiningStatus(Enum):
    Hiden = 0
    Running = 1
    SellOrCollect = 2

MINE_MAP_ROW_SIZE = 5
MINE_MAP_COLUMN_SIZE = 6
MINE_TILE_WIDTH = 50
MINE_TILE_HEIGHT = 50
MAX_PICKAXE_COUNT = MINE_MAP_ROW_SIZE * MINE_MAP_COLUMN_SIZE // 2
CARD_FRAME_DELAY = 30

RESOURCE_CELL_RATE = 0.6
RESOURCE_LEVEL_RANGE = (0.9, 0.7, 0)

SELL_BUTTON_RECT = pygame.Rect(5, 320, 75, 45)
COLLECT_BUTTON_RECT = pygame.Rect(345, 320, 75, 45)

class MineMapCell:
    def __init__(self, cell_index: int) -> None:
        self.recource_level = 0
        self.is_revealed = False
        self.resource_type = ResourceType.Nothing
        index_x = cell_index % MINE_MAP_ROW_SIZE
        index_y = cell_index // MINE_MAP_ROW_SIZE
        self.rect = pygame.Rect(
            80 + index_x * MINE_TILE_WIDTH, 
            10 + index_y * MINE_TILE_HEIGHT,
            MINE_TILE_WIDTH,
            MINE_TILE_HEIGHT
        )

    def roll_cell(self) -> None:
        if uniform(0, 1) > RESOURCE_CELL_RATE:
            self.resource_type = ResourceType.Nothing
        else:
            type_count = len(ResourceType)
            self.resource_type = ResourceType(randint(1, type_count - 1)) # 0 = nothing, last = n -1
            self.roll_resource_level()

    def roll_resource(self) -> None:
        num_recoures = len(ResourceType)
        self.resource_type = ResourceType(randint(1, num_recoures))
        self.roll_resource_level()

    def roll_resource_level(self) -> None:
        max_level = len(RESOURCE_LEVEL_RANGE)
        rand = uniform(0, 1)
        for i in range(max_level):
            if rand > RESOURCE_LEVEL_RANGE[i]:
                self.recource_level = max_level - i
                break

class MineGameManager:
    def __init__(self, rect: tuple, user_inventory: UserInventory) -> None:
        self.canvas_rect = rect
        self.user_inventory = user_inventory
        self.game_status = MiningStatus.Running
        self.saved_status = MiningStatus.Hiden
        self.canvas = pygame.Surface(
            (self.canvas_rect[2],
             self.canvas_rect[3])
        )
        self.pickaxe_count = MAX_PICKAXE_COUNT
        self.mine_map = self.new_mine_map()
        self.font = pygame.font.SysFont('arial', 16)
        self.card_frame_delay = 0
        self.revealed_cell: MineMapCell = None

    def new_mine_map(self) -> list[MineMapCell]:
        mine_map = []
        for i in range(MINE_MAP_ROW_SIZE * MINE_MAP_COLUMN_SIZE):
            mine_map_cell = MineMapCell(i)
            mine_map_cell.roll_cell()
            mine_map.append(mine_map_cell)
        return mine_map

    def blit_mine_map(self) -> None:
        for tile in self.mine_map:
            img = tile_images[0] if tile.is_revealed else tile_images[1]
            self.canvas.blit(img, tile.rect)
    
    def reveal_mine_cell(self, position: tuple) -> MineMapCell:
        for cell in self.mine_map:
            if cell.rect.collidepoint(position) and not cell.is_revealed:
                cell.is_revealed = True
                self.pickaxe_count -= 1
                # print(cell.rect)
                # print(cell.resource_type)
                # print(cell.recource_level)
                return cell
        return None
    
    def add_resource_by_cell(self, cell: MineMapCell) -> None:
        if cell is None or cell.resource_type == ResourceType.Nothing:
          return
        idx = cell.resource_type.value - 1
        self.user_inventory.resources[idx] += 1

    def add_coin_by_cell(self, cell: MineMapCell) -> None:
        if cell is None or cell.resource_type == ResourceType.Nothing:
          return
        self.user_inventory.add_coins

    def blit_pickaxe(self) -> None:
        text = self.font.render(str(self.pickaxe_count), True, (0, 0, 0))
        self.canvas.blit(pickaxe_image, (180, 315))
        self.canvas.blit(text, (220, 320))

    def blit_card(self, mine_cell: MineMapCell):
        if mine_cell is None or mine_cell.resource_type == ResourceType.Nothing:
            return
        card = self.get_resource_card(mine_cell)
        surface = compose_card_surface(card)
        self.canvas.blit(surface, (80, 0))

    def get_resource_card(self, mine_cell: MineMapCell) -> str:
        resource_type = ""
        if mine_cell.resource_type == ResourceType.Stone:
            resource_type = "stone"
        elif mine_cell.resource_type == ResourceType.Water:
            resource_type = "water"
        elif mine_cell.resource_type == ResourceType.Wood:
            resource_type = "wood"
        elif mine_cell.resource_type == ResourceType.Food:
            resource_type = "food"
        elif mine_cell.resource_type == ResourceType.Metal:
            resource_type = "metal"
        elif mine_cell.resource_type == ResourceType.Jewel:
            resource_type = "jewel"
        card_id = f"{resource_type}_{mine_cell.recource_level}_1"
        return primitive_cards[card_id]

    def process_frame(self, events: list) -> pygame.Surface:
        if self.game_status == MiningStatus.Hiden:
            return None
        for e in events:
            if e.type == pygame.MOUSEBUTTONUP:
                self.process_click()
        if self.game_status == MiningStatus.SellOrCollect:
            self.canvas.fill((255, 255, 255))
            self.blit_card(self.revealed_cell)
            self.blit_collect_sell_buttons()
        else:
            self.canvas.fill((255, 255, 255))
            self.blit_mine_map()
            self.blit_pickaxe()
        return self.canvas
    
    def process_click(self) -> None:
        global_position = pygame.mouse.get_pos()
        position = get_child_scene_position(global_position, self.canvas_rect)
        if self.game_status == MiningStatus.Running:
            self.process_minig_click(position)
            if self.revealed_cell and self.revealed_cell.resource_type != ResourceType.Nothing:
                self.game_status = MiningStatus.SellOrCollect
        elif self.game_status == MiningStatus.SellOrCollect:
            done = self.process_collect_or_sell_click(position)
            if done:
                self.revealed_cell = None
                self.game_status = MiningStatus.Running

    def process_minig_click(self, child_scene_position) -> None:
        self.revealed_cell = self.reveal_mine_cell(child_scene_position)
        if self.pickaxe_count <= 0:
            self.mine_map = self.new_mine_map()
            self.pickaxe_count = MAX_PICKAXE_COUNT
        if self.revealed_cell:
            self.process_collect_or_sell_click(child_scene_position)

    def process_collect_or_sell_click(self, child_scene_position) -> bool:
        if SELL_BUTTON_RECT.collidepoint(child_scene_position):
            self.add_coin_by_cell(self.revealed_cell)
            return True
        elif COLLECT_BUTTON_RECT.collidepoint(child_scene_position):
            self.add_resource_by_cell(self.revealed_cell)
            return True
        return False

    def add_coin_by_cell(self, mine_cell: MineMapCell) -> None:
        card_id = self.get_card_id(mine_cell)
        card = primitive_cards[card_id]
        self.user_inventory.add_coins(card.sell_coin)

    def get_card_id(self, mine_cell: MineMapCell) -> Card:
        resource = ""
        if mine_cell.resource_type == ResourceType.Stone:
            resource = "stone"
        if mine_cell.resource_type == ResourceType.Water:
            resource = "water"
        if mine_cell.resource_type == ResourceType.Wood:
            resource = "wood"
        if mine_cell.resource_type == ResourceType.Food:
            resource = "food"
        if mine_cell.resource_type == ResourceType.Metal:
            resource = "metal"
        if mine_cell.resource_type == ResourceType.Jewel:
            resource = "jewel"
        return f"{resource}_{mine_cell.recource_level}_1"

    def blit_collect_sell_buttons(self) -> None:
        self.canvas.blit(button_images["collect"], COLLECT_BUTTON_RECT.topleft)
        self.canvas.blit(button_images["sell"], SELL_BUTTON_RECT.topleft)
    
    def hide(self) -> None:
        self.saved_status = self.game_status
        self.game_status = MiningStatus.Hiden

    def activate(self) -> None:
        self.game_status = self.saved_status
