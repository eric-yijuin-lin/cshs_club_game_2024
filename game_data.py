from enum import Enum

class ResourceType(Enum):
    Nothing = 0
    Stone = 1
    Water = 2
    Wood = 3
    Food = 4
    Metal = 5
    Jewel = 6

class GameItem:
    def __init__(self, id: str, name: str, level: int) -> None:
        self.id = id
        self.name = name
        self.level = level
        self.count = 1

class UserInventory:
    def __init__(self):
        self.recoures = [0] * 6 # [stone, water, wood, food, metal, jewel]
        self.items: list[GameItem] = []
        self.item_count = 0
        self.item_index = 0
        self.init_user_items()

    def init_user_items(self) -> None:
        self.items = [
            GameItem("", "", 0),
            GameItem("debug_1", "綠色乖乖", 99)
        ]
        self.item_count = len(self.items)

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
    
    def add_item(self, item: GameItem) -> None:
        item_found = next((i for i in self.items if i.id == item.id), None)
        if item_found:
            item_found.count += 1
        else:
            self.items.append(item)
            self.item_count = len(self.items)

    def get_item(self, item_index: int) -> GameItem:
        return self.items[item_index]

    def use_item(self, item_index, count: int) -> None:
        item = self.items[item_index]
        item.count -= count
        if item.count == 0:
            del self.items[item_index]
            self.item_count = len(self.items)

            