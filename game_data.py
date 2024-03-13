from enum import Enum
from mine_game import MineMapCell

class ResourceType(Enum):
    Nothing = 0
    Stone = 1
    Water = 2
    Wood = 3
    Food = 4
    Metal = 5
    Jewel = 6

class UserResource:
    def __init__(self):
        # [stone, water, wood, food, metal, jewel]
        self.recoures = [0] * 6

    def add_resource_by_cell(self, cell: MineMapCell) -> None:
        if cell is None or cell.recource_type == ResourceType.Nothing:
          return
        idx = cell.recource_type.value - 1
        self.recoures[idx] += 1

    def get_amount(self, resource_type: ResourceType) -> int:
        if resource_type == ResourceType.Stone:
            return self.recoures[0]
        if resource_type == ResourceType.Water:
            return self.recoures[1]
        if resource_type == ResourceType.Wood:
            return self.recoures[2]
        if resource_type == ResourceType.Food:
            return self.recoures[3]
        if resource_type == ResourceType.Metal:
            return self.recoures[4]
        if resource_type == ResourceType.Jewel:
            return self.recoures[5]

    def change_amount(self, resource_type: ResourceType, amount: int) -> None:
        if resource_type == ResourceType.Stone:
            self.recoures[0] += amount
            if self.recoures[0] < 0:
                self.recoures[0] = 0
        if resource_type == ResourceType.Water:
            self.recoures[1] += amount
            if self.recoures[1] < 0:
                self.recoures[1] = 0
        if resource_type == ResourceType.Wood:
            self.recoures[2] += amount
            if self.recoures[2] < 0:
                self.recoures[2] = 0
        if resource_type == ResourceType.Food:
            self.recoures[3] += amount
            if self.recoures[3] < 0:
                self.recoures[3] = 0
        if resource_type == ResourceType.Metal:
            self.recoures[4] += amount
            if self.recoures[4] < 0:
                self.recoures[4] = 0
        if resource_type == ResourceType.Jewel:
            self.recoures[5] += amount
            if self.recoures[5] < 0:
                self.recoures[5] = 0
