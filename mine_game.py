import pygame
from enum import Enum
from random import randint, uniform
from game_assets import tile_images, pickaxe_image, card_images

class ResourceType(Enum):
    Nothing = 0
    Stone = 1
    Water = 2
    Wood = 3
    Food = 4
    Metal = 5
    Jewel = 6

class GameStatus(Enum):
    Hiden = 0
    Running = 1
    Pause = 2

MINE_MAP_ROW_SIZE = 5
MINE_MAP_COLUMN_SIZE = 6
MINE_TILE_WIDTH = 50
MINE_TILE_HEIGHT = 50
MAX_PICKAXE_COUNT = MINE_MAP_ROW_SIZE * MINE_MAP_COLUMN_SIZE // 2

RESOURCE_CELL_RATE = 0.6
RESOURCE_LEVEL_RANGE = (0.9, 0.7, 0)


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
    def __init__(self, rect: tuple) -> None:
        self.canvas_rect = rect
        self.game_status = GameStatus.Running
        self.canvas = pygame.Surface(
            (self.canvas_rect[2],
             self.canvas_rect[3])
        )
        self.pickaxe_count = MAX_PICKAXE_COUNT
        self.mine_map = self.new_mine_map()
        self.font = pygame.font.SysFont('arial', 16)
        self.card_frame_delay = 60 # with fps=40, means pause 1.5 seconds

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
            if cell.rect.collidepoint(position):
                cell.is_revealed = True
                self.pickaxe_count -= 1
                # print(cell.rect)
                # print(cell.resource_type)
                # print(cell.recource_level)
                return cell
        return None

    def blit_pickaxe(self) -> None:
        text = self.font.render(str(self.pickaxe_count), True, (0, 0, 0))
        self.canvas.blit(pickaxe_image, (180, 315))
        self.canvas.blit(text, (220, 320))

    def blit_card(self, mine_cell: MineMapCell):
        if mine_cell is None or mine_cell.resource_type == ResourceType.Nothing:
            return
        idx = mine_cell.resource_type.value - 1
        img = card_images[idx]
        self.canvas.blit(img, (80, 0))
        self.card_frame_delay = 60
        self.game_status = GameStatus.Pause

    def process_frame(self, events: list) -> pygame.Surface:
        if self.game_status == GameStatus.Hiden:
            return None
        if self.game_status == GameStatus.Pause:
            self.card_frame_delay -= 1
            if self.card_frame_delay <= 0:
                self.game_status = GameStatus.Running
            return self.canvas
        if self.game_status == GameStatus.Running:
            self.canvas.fill((255, 255, 255))
            self.blit_mine_map()
            self.blit_pickaxe()
            for e in events:
                if e.type == pygame.MOUSEBUTTONUP:
                    main_screen_position = pygame.mouse.get_pos()
                    child_scene_position = self.get_child_scene_position(main_screen_position)
                    revealed_cell = self.reveal_mine_cell(child_scene_position)
                    self.blit_card(revealed_cell)
            return self.canvas
        
    def get_child_scene_position(self, main_screen_position: tuple) -> tuple:
        return (
            main_screen_position[0] - self.canvas_rect[0],
            main_screen_position[1] - self.canvas_rect[1] 
        )
