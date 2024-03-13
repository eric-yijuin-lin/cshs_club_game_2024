from enum import Enum
from random import randint, uniform
from pygame import Rect

class ResourceType(Enum):
    Nothing = 0
    Stone = 1
    Water = 2
    Wood = 3
    Food = 4
    Metal = 5
    Jewel = 6

MINE_MAP_ROW_SIZE = 5
MINE_MAP_COLUMN_SIZE = 6
MINE_TILE_WIDTH = 50
MINE_TILE_HEIGHT = 50

RESOURCE_CELL_RATE = 0.5
RESOURCE_LEVEL_RANGE = (0.9, 0.7, 0)

class MineMapCell:
    def __init__(self, cell_index: int) -> None:
        self.recource_level = 0
        self.is_revealed = False
        self.resource_type = ResourceType.Nothing
        index_x = cell_index % MINE_MAP_ROW_SIZE
        index_y = cell_index // MINE_MAP_ROW_SIZE
        self.rect = Rect(
            75 + index_x * MINE_TILE_WIDTH, 
            100 + index_y * MINE_TILE_HEIGHT,
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
    def __init__(self) -> None:
        self.mine_map = self.new_mine_map()

    def new_mine_map(self) -> list:
        mine_map = []
        for i in range(MINE_MAP_ROW_SIZE * MINE_MAP_COLUMN_SIZE):
            mine_map_cell = MineMapCell(i)
            mine_map_cell.roll_cell()
            mine_map.append(mine_map_cell)
        return mine_map
