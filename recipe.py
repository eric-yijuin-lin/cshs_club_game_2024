import csv

card_type_dict = {
    "石頭": "stone",
    "水": "water",
    "木材": "wood",
    "食物": "food",
    "金屬": "metal",
    "珠寶": "jewel",
    "物品": "item"
}

class Card:
    def __init__(self, data_row: list) -> None:
        self.id = data_row[0]
        self.name = data_row[1]
        self.type = card_type_dict[data_row[2]]
        self.level = data_row[3]
        self.resource_amount = data_row[4]
        self.sell_price = data_row[5]
        self.description = data_row[15]

class CraftRecipe:
    def __init__(self, csv_row: list) -> None:
        data_row = CraftRecipe.get_converted_row(csv_row)
        self.recipe = CraftRecipe.extract_recipe(data_row)
        self.money_cost = data_row[14]
        self.is_craftable = CraftRecipe.get_craftability(self.recipe)
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
    def extract_recipe(data_row) -> tuple:
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
# value: 合成出來的資源/物品 ID
craft_recipes: dict[tuple, CraftRecipe] = {}
with open('recipes.csv', encoding="utf8") as f:
    reader = csv.reader(f, delimiter=',')
    column_num = 0
    for row in reader:
        if reader.line_num == 1:
            print("表頭欄位：", row)
        else:
            craft = CraftRecipe(row)
            if craft.is_craftable:
                craft_recipes[craft.recipe] = craft
print(craft_recipes)