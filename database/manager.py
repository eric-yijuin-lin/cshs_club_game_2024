from datetime import datetime
import gspread

from common.game_data import Card

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
        self.user: dict = {}
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
                self.user = user
                return
        raise ValueError("user_id 不存在, 請檢查是否有用 MD5 加密學號，然後取代掉 user_id 變數的值")
    def insert_craft_record(self, card: Card) -> None:
        date_str = datetime.now().strftime('%Y-%m-%d')
        time_str = datetime.now().strftime('%H:%M:%S')
        # 合成物品	組別	姓名	日期	時間
        row = [
            card.name,
            self.user["組別"],
            self.user["姓名"],
            date_str,
            time_str
        ]
        try:
            self.record_sheet.insert_row(row, 2)
        except Exception as ex:
            print("無法新增合成紀錄，錯誤訊息：", str(ex))
