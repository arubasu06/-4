import pandas as pd
import sys
import datetime

ITEM_MASTER_CSV_PATH="./item_master.csv"
RECEIPT_FOLDER="./receipt"

class Food_MenuItem:
    def __init__(self, item_code, item_name, price):
        self.item_code = item_code
        self.item_name = item_name
        self.price = price

    def info(self):
        return self.item_name + ': ¥' + str(self.price)

    def get_total_price(self, count):
        total_price = self.price * count
        return round(total_price)

class Order:
    def __init__(self,item_master):
        self.item_order_list=[]
        self.item_count_list=[]
        self.item_master=item_master
        self.set_datetime()
    
    def set_datetime(self):
        self.datetime=datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')

    def get_item_data(self,item_code):
        for m in self.item_master:
            if item_code==m.item_code:
                return m.item_name,m.price

    def add_item_order(self, item_code, item_name, price):
        self.food_order_list=[]
        food1 = Food_MenuItem('01','サンドイッチ', 500)
        food2 = Food_MenuItem('02','ホットドッグ', 400)
        food3 = Food_MenuItem('03','ハンバーガー', 600)  
        foods = [food1, food2, food3]

        print('食べ物メニュー')
        index = 0
        for food in foods:
            print(str(index) + '. ' + food.info())
            index += 1

        print('-----------------------------------')

    def input_order(self):
        print("いらっしゃいませ！")
        food_order = int(input('商品番号を選択してください: '))
        selected_food = foods[food_order]
        count = int(input("何セット買いますか？"))
        result = selected_food.get_total_price(count)
        print("合計は" + str(result) + "円です")
    
    def view_order(self):
        number=1
        self.sum_price=0
        self.sum_count=0
        self.receipt_name="receipt_{}.log".format(self.datetime)
        self.write_receipt("-----------------------------------------------")
        self.write_receipt("オーダー登録された商品一覧\n")
        for item_order,item_count in zip(self.item_order_list,self.item_count_list):
            result=self.get_item_data(item_order)
            self.sum_price+=result[1]*int(item_count)
            self.sum_count+=int(item_count)
            receipt_data="{0}.{2}({1}) : ￥{3:,}　{4}個 = ￥{5:,}".format(number,item_order,result[0],result[1],item_count,int(result[1])*int(item_count))
            self.write_receipt(receipt_data)
            number+=1

        # 合計金額、個数の表示
        self.write_receipt("-----------------------------------------------")
        self.write_receipt("合計金額:￥{:,} {}個".format(self.sum_price,self.sum_count))

    def input_change_money(self):
        money = input("お預かり金を入力してください >>> ")
        change_money = money - get_total_price
        while True:
            if change_money>=0:
                print("お預り金は" + str(money) + '円です')
                print("お釣りは" + str(change_money) + '円です')
                break
            else:
                print("お預かり金が不足しています。再度入力してください")
        
        print("お買い上げありがとうございました！")

    def write_receipt(self,text):
        print(text)
        with open(RECEIPT_FOLDER + "\\" + self.receipt_name,mode="a",encoding="utf-8_sig") as f:
            f.write(text+"\n")

def add_item_master_by_csv(csv_path):
    print("------- マスタ登録開始 ---------")
    item_master=[]
    count=0
    try:
        item_master_df=pd.read_csv(csv_path,dtype={"item_code":object}) # CSVでは先頭の0が削除されるためこれを保持するための設定
        for item_code,item_name,price in zip(list(item_master_df["item_code"]),list(item_master_df["item_name"]),list(item_master_df["price"])):
            item_master.append(Food_MenuItem(item_code,item_name,price))
            print("{}({})".format(item_name,item_code))
            count+=1
        print("{}品の登録を完了しました。".format(count))
        print("------- マスタ登録完了 ---------")
        return item_master
    except:
        print("マスタ登録が失敗しました")
        print("------- マスタ登録完了 ---------")
        sys.exit()

def main():
    item_master=add_item_master_by_csv(ITEM_MASTER_CSV_PATH) # CSVからマスタへ登録
    order=Order(item_master) #マスタをオーダーに登録
    
    order.input_order()
    
    order.view_order()
    order.input_change_money()

if __name__ == "__main__":
    main()