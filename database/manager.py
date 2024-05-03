from datetime import datetime
import json
import gspread
import pymysql
from common.game_data import Card, GameItem

class IDatabaseManager:
    def __init__(self) -> None:
        self.user = {"id": "debug000", "name": "debug-user"}
    def get_game_id(self) -> str:
        pass
    def get_group_id(self, user_id) -> str:
        pass
    def insert_craft_record(self, card: Card, user_id: str) -> None:
        pass
    def test(self) -> None:
        print("test for IDatabaseManager")
        print(self.user)

class GoogleSheetDatabase(IDatabaseManager):
    def __init__(self, credential: str, user_id: str) -> None:
        super().__init__()
        self.user_info: dict = {}
        self.__init_work_sheets(credential)
        self.__init_user(user_id)
    def __init_work_sheets(self, credential_path: str) -> None:
        service_account = gspread.service_account(filename = credential_path)
        work_book = service_account.open("2024資訊社遊戲")
        self.user_sheet = work_book.worksheet("使用者")
        self.record_sheet = work_book.worksheet("合成紀錄")
    def __init_user(self, user_id: str) -> None:
        for user in self.user_sheet.get_all_records():
            if user_id == user["USER_ID"]:
                self.user_info = user
                return
        raise ValueError("user_id 不存在, 請檢查是否有用 MD5 加密學號，然後取代掉 user_id 變數的值")
    def insert_craft_record(self, card: Card) -> None:
        date_str = datetime.now().strftime('%Y-%m-%d')
        time_str = datetime.now().strftime('%H:%M:%S')
        # 合成物品	組別	姓名	日期	時間
        row = [
            card.name,
            self.user_info["組別"],
            self.user_info["姓名"],
            date_str,
            time_str
        ]
        try:
            self.record_sheet.insert_row(row, 2)
        except Exception as ex:
            print("無法新增合成紀錄，錯誤訊息：", str(ex))

class MySQLDatabase(IDatabaseManager):
    def __init__(self, credential_path: str, user_info: dict) -> None:
        super().__init__()
        self.__user_info = user_info
        self.__credential = {}
        with open(credential_path) as f:
            self.__credential = json.load(f)
        self.__connection = self.__new_connection()
    
    def __new_connection(self) -> pymysql.Connection:
        return pymysql.connect(
            host = self.__credential["host"],
            port = self.__credential["port"],
            user = self.__credential["user"],
            password = self.__credential["password"],
            database = self.__credential["database"],
        )
    
    def __check_connection(self) -> None:
        if not self.__connection or not self.__connection.open:
            self.__connection = self.__new_connection()

    def insert_user_item(self, item_id: str, item_name: str) -> None:
        sql = """
            INSERT INTO `cshs_db`.`user_items`
                (`user_id`,
                `user_name`,
                `item_id`,
                `item_name`,
                `group_name`)
            VALUES
                (%s,%s,%s,%s,%s);
        """
        try:
            self.__check_connection()
            cursor = self.__connection.cursor()
            with cursor:
                params = (
                    self.__user_info["USER_ID"],
                    self.__user_info["姓名"],
                    item_id,
                    item_name,
                    self.__user_info["組別"],
                )
                cursor.execute(sql, params)
            self.__connection.commit()
        except Exception as ex:
            print("Failed to insert item: ", ex)
            if self.__connection:
                self.__connection.close()

    def get_group_items(self) -> list[GameItem]:
        sql = """
            SELECT
                 `user_id`, `user_name`, `item_id`, `item_name`, `group_name`, `used`
            FROM
                `cshs_db`.`user_items`
            WHERE
                `group_name`=%s
            ORDER BY
                `created_at`
        """
        self.__check_connection()
        cursor = self.__connection.cursor()
        db_rows = []
        group_items = []
        with cursor:
            params = (
                self.__user_info["組別"]
            )
            cursor.execute(sql, params)
            db_rows = cursor.fetchall()
        for row in db_rows:
            item_id = row[2]
            item_name = row[3]
            item_lv = int(item_id[5])
            item = GameItem(item_id, item_name, item_lv, self.__user_info["USER_ID"])
            group_items.append(item)
        return group_items

    def test(self) -> None:
        sql = """
            SELECT * FROM `cshs_db`.`user_items`LIMIT 100;
        """
        self.__check_connection()
        cursor = self.__connection.cursor()
        with cursor:
            params = (
            )
            cursor.execute(sql, params)
            data = cursor.fetchall()
            for d in data:
                print(d)
