from enum import Enum

class ResourceType(Enum):
    Nothing = 0
    Stone = 1
    Water = 2
    Wood = 3
    Food = 4
    Metal = 5
    Jewel = 6

class CardType(Enum):
    Stone = 1
    Water = 2
    Wood = 3
    Food = 4
    Metal = 5
    Jewel = 6
    Item = 7

class Card:
    def __init__(self, data_row: list) -> None:
        self.id = data_row[0]
        self.name = data_row[1]
        self.type = Card.get_card_type(data_row[2])
        self.level = data_row[3]
        self.resource_amount = data_row[4]
        self.sell_coin = data_row[5]
        self.description = data_row[15]

    @staticmethod
    def get_card_type(type: str) -> CardType:
        if type == "石頭":
            return CardType.Stone
        if type == "水":
            return CardType.Water
        if type == "木材":
            return CardType.Wood
        if type == "食物":
            return CardType.Food
        if type == "金屬":
            return CardType.Metal
        if type == "珠寶":
            return CardType.Jewel
        if type == "物品":
            return CardType.Item
        raise ValueError("invalid type string")

class GameItem:
    def __init__(self, item_id: str, name: str, level: int, user_id: str) -> None:
        self.item_id = item_id
        self.name = name
        self.level = level
        self.count = 1
        self.owner_id = user_id
