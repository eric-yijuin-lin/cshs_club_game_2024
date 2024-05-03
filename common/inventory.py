
from common.game_data import GameItem, ResourceType

class UserInventory:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.resources = [0] * 6 # [stone, water, wood, food, metal, jewel]
        self.coins = 0
        self.items: list[GameItem] = []
        self.item_count = 0
        self.item_index = 0
        self.init_user_items()

    def init_user_items(self) -> None:
        self.items = [
            GameItem("", "", 0, ""),
            GameItem("debug_1", "綠色乖乖", 99, "")
        ]
        self.item_count = len(self.items)

    def get_resource_amount(self, resource_type: ResourceType) -> int:
        if resource_type == ResourceType.Stone:
            return self.resources[0]
        if resource_type == ResourceType.Water:
            return self.resources[1]
        if resource_type == ResourceType.Wood:
            return self.resources[2]
        if resource_type == ResourceType.Food:
            return self.resources[3]
        if resource_type == ResourceType.Metal:
            return self.resources[4]
        if resource_type == ResourceType.Jewel:
            return self.resources[5]
    
    def add_item(self, item: GameItem) -> None:
        item_found = next((i for i in self.items if i.item_id == item.item_id), None)
        if item_found:
            item_found.count += 1
        else:
            self.items.append(item)
            self.item_count = len(self.items)

    def refresh_item_list(self, items: list[GameItem]) -> None:
        for item in items:
            self.add_item(item)

    def consume_resources(self, resources: tuple[int]) -> None:
        for i in range(len(self.resources)):
            self.resources[i] -= resources[i]

    def consume_item(self, item_id: str) -> None:
        item = next((i for i in self.items if i.item_id == item_id))
        item.count -= 1

    def add_coins(self, amount: int) -> None:
        self.coins += amount

    def consume_coins(self, amount: int) -> None:
        if self.coins < amount:
            raise ValueError("insufficient coins")
        self.coins -= amount

    def enough_ingredients(self, ingredients: tuple) -> bool:
        if not self.enough_resource(ingredients):
            return False
        if not self.enough_items(ingredients):
            return False
        return True
    
    def enough_resource(self, ingredients: tuple) -> bool:
        resource_count = len(self.resources)
        for i in range(resource_count):
            if self.resources[i] < ingredients[i]:
                return False
        return True

    def enough_items(self, ingredients: tuple) -> bool:
        item_count_dict = self.get_needed_item_counts(ingredients)
        for item_id in item_count_dict:
            need_count = item_count_dict[item_id]
            item = next((i for i in self.items if i.item_id == item_id), None)
            if item is None or item.count < need_count:
                return False
        return True

    def get_needed_item_counts(self, ingredients: tuple) -> dict:
        item_counts = {}
        id_1 = ingredients[6]
        id_2 = ingredients[7]
        if id_1:
            item_counts[id_1] = 1
        if id_2:
            if id_1 == id_2:
                item_counts[id_1] += 1
            else:
                item_counts[id_2] = 1
        return item_counts
