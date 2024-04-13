import csv

from assets.game_assets import recipe_csv
from common.game_data import Card, CardType

class CraftRecipe:
    def __init__(self, csv_row: list) -> None:
        data_row = CraftRecipe.get_converted_row(csv_row)
        self.ingredients = CraftRecipe.extract_ingredients(data_row)
        self.coin_cost = data_row[14]
        self.is_craftable = CraftRecipe.get_craftability(self.ingredients)
        self.card = Card(data_row)

    @staticmethod
    def get_converted_row( csv_row) -> tuple:
        return (
            csv_row[0], # 卡片 ID，不計入合成配方
            csv_row[1], # 卡片名稱，不計入合成配方
            csv_row[2], # 卡片分類，不計入合成配方
            int(csv_row[3]), # 卡片等級
            int(csv_row[4]), # 獲得資源
            int(csv_row[5]), # 販賣金幣
            int(csv_row[6]), # 合成所需石頭
            int(csv_row[7]), # 合成所需水
            int(csv_row[8]), # 合成所需木材
            int(csv_row[9]), # 合成所需食物
            int(csv_row[10]), # 合成所需金屬
            int(csv_row[11]), # 合成所需珠寶   
            csv_row[12], # 合成所需物品 1
            csv_row[13], # 合成所需物品 2
            int(csv_row[14]), # 消耗金幣，此版本不計入合成配方
            csv_row[15], # 卡片描述，不計入合成配方
        )

    @staticmethod
    def extract_ingredients(data_row) -> tuple:
        return (
            data_row[6], # 石頭
            data_row[7], # 水
            data_row[8], # 木材
            data_row[9], # 食物
            data_row[10], # 金屬
            data_row[11], # 珠寶
            data_row[12], # 物品1
            data_row[13], # 物品2
            # data_row[14] # 消耗金幣，此版本不計入合成配方
        )
    
    @staticmethod
    def get_craftability(recipe: tuple) -> bool:
        primitive_values = (0 ,0 ,0, 0, 0, 0, "", "", 0)
        for i in range(len(recipe)):
            if recipe[i] != primitive_values[i]:
                return True
        return False

# key: 合成配方 (石頭, 水, 木材, 食物, 金屬, 珠寶, 物品1 ID, 物品2 ID)
# value: 合成出來的資源/物品卡片
craft_recipes: dict[tuple, CraftRecipe] = {}
primitive_cards: dict[str, Card] = {}
for row in recipe_csv:
    craft = CraftRecipe(row)
    if craft.is_craftable:
        craft_recipes[craft.ingredients] = craft
    else:
        primitive_cards[craft.card.id] = craft.card

# 為避免 None Error，把還沒加入配方的高級資源加進 primitive_cards
type_texts = {
    CardType.Stone: "石頭",
    CardType.Water: "水",
    CardType.Wood: "木材",
    CardType.Food: "食物",
    CardType.Metal: "金屬",
    CardType.Jewel: "珠寶",
}
for t_enum in CardType:
    if t_enum == CardType.Item: 
        continue
    type_name = t_enum.name.lower()
    for lv in range(1, 6):
        card_id = f"{type_name}_{lv}_1"
        if card_id not in primitive_cards:
            card = Card([
                card_id,
                card_id,
                type_texts[t_enum],
                lv,
                lv,
                lv * 10,
                0,0,0,0,0,0,"","",
                0,
                card_id
            ])
            primitive_cards[card_id] = card
