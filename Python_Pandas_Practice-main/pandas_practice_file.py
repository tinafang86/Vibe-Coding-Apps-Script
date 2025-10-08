import pandas as od
import datetime as dt
import pandas as pd
sales_data = pd.read_csv(
    "/Users/tinafung8686/Desktop/python_sales-data/Sales-Data-Analysis.csv")
sales_data

# 以下爲常用解析資料
sales_data.size  # 共有2286個項目，只會考慮列數*欄數，不考慮遺漏值(NaN)
sales_data.count()  # 回傳非空值 (non-null)
sales_data.values  # 打印出所有的值
sales_data.columns  # 打印出所有的欄位值
sales_data.describe()
sales_data.sum()
sales_data.index  # 索引值 # RangeIndex(start=0, stop=254, step=1) 有253列
sales_data.shape  # (行,列) # (254, 9)
sales_data.dtypes  # 各欄內值的type
sales_data.head()  # 預設前五
sales_data.tail()  # 預設後五
250 in sales_data.index  # 250為表格中其中一個index
"Product" in sales_data  # True
"Beverages" in sales_data.values

# 以下處理單一欄位

# 我只看有多少product。透過column_name取得
datas = pd.read_csv("/Users/tinafung8686/Desktop/python_sales-data/Sales-Data-Analysis.csv",
                    usecols=["Product", "Payment Method"])
datas
# 我只看有多少product和Payment method。透過column_index取得
datas = pd.read_csv(
    "/Users/tinafung8686/Desktop/python_sales-data/Sales-Data-Analysis.csv", usecols=[2, 5])
datas

datas = pd.read_csv("/Users/tinafung8686/Desktop/python_sales-data/Sales-Data-Analysis.csv",
                    usecols=["Product"]).squeeze("columns")


# 調整欄列順序
datas = pd.read_csv("/Users/tinafung8686/Desktop/python_sales-data/Sales-Data-Analysis.csv",
                    usecols=["Product", "Payment Method"])
datas

pd.DataFrame(datas, columns=["Payment Method", "Product"])
pd.DataFrame(datas, columns=["Product", "Payment Method"])

data_restored = datas[["Product", "Payment Method"]]
data_restored = datas[["Payment Method", "Product"]]

# 排序數字

# Series
# 第一種寫法
new_data = pd.read_csv(
    "/Users/tinafung8686/Desktop/python_sales-data/Sales-Data-Analysis.csv", usecols=["Price"]).sort_values(by="Price")
# 第二種寫法
new_data = pd.read_csv(
    "/Users/tinafung8686/Desktop/python_sales-data/Sales-Data-Analysis.csv", usecols=["Price"]).squeeze("columns").sort_values()

# DataFrame
# 單一sort
sales_data = pd.read_csv(
    "/Users/tinafung8686/Desktop/python_sales-data/Sales-Data-Analysis.csv")
sales_data.sort_values(by="Price")  # 價錢由小到大
sales_data.sort_values(by="Price", ascending=False)  # 價錢由大到小

# 雙重sort
sales_data = pd.read_csv(
    "/Users/tinafung8686/Desktop/python_sales-data/Sales-Data-Analysis.csv")
sales_data.sort_values(by=["Price", "Quantity"])  # 價錢由小到大
sales_data.sort_values(by=["Price", "Quantity"],
                       ascending=[False, True])  # 價錢由小到大

# sort_index()
df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]}, index=['C', 'A', 'B'])

# 使用 sort_index() 進行升序排序 (預設)。不需要寫by，但要透過axis操作資料表
df_sorted = df.sort_index(axis=0)
# axis = 0針對列索引值排序，axis = 1針對欄索引值排序
df_sorted = df.sort_index(axis=0, ascending=False)
df_sorted = df.sort_index(axis=1, ascending=False)  # 操作欄，由大到小排序

# 取得標籤值

sales_data = pd.read_csv(
    "/Users/tinafung8686/Desktop/python_sales-data/Sales-Data-Analysis.csv")
sales_data

# 將原始資料轉為Series，Product為索引index，Price為欄
data01 = pd.read_csv(
    "/Users/tinafung8686/Desktop/python_sales-data/Sales-Data-Analysis.csv", usecols=["Product", "Price"], index_col=["Product"])
# 發現index重複度很高，用groupby()將一樣的值合併，但需要注意groupby()是分組操作不會直接顯示成果
# <pandas.core.groupby.generic.DataFrameGroupBy object at 0x1269b6c60>
onlydata = data01.groupby(by="Product")
print(onlydata.mean())

# 透過loc找出burger的價錢
# get_group將所有資料都print
burgerdata = onlydata.get_group("Burgers")

# loc
data01 = pd.read_csv(
    "/Users/tinafung8686/Desktop/python_sales-data/Sales-Data-Analysis.csv", usecols=["Product", "Price"], index_col=["Product"])
# 發現index重複度很高，用groupby()將一樣的值合併，但需要注意groupby()是分組操作不會直接顯示成果
onlydata = data01.groupby(by="Product")
average_data = onlydata.mean()
# loc["第一個索引值，取索引標籤"，"第二個索引值，取欄位"]
burgerdata = average_data.loc["Burgers", "Price"]

# 如果我要取得OrderID 10452 在Product買的東西是什麼，價錢多少
sales_data.get(["Product", "Price"])
sales_data

# 計算column的值

datas = pd.read_csv("/Users/tinafung8686/Desktop/python_sales-data/Sales-Data-Analysis.csv",
                    usecols=["Product"])
datas.value_counts()  # 計算個數
# 計算個數並換算為比例 # Return proportions rather than frequencies.
datas.value_counts(normalize=True)
datas.shape

# 計算欄位為數字的項目並加總，如Quantity
sales_data = pd.read_csv(
    "/Users/tinafung8686/Desktop/python_sales-data/Sales-Data-Analysis.csv", usecols=["Quantity", "Price"])
sales_data
sales_data.sum(axis=0)
sales_data.sum(axis=1)

# map

sales_data = pd.read_csv(
    "/Users/tinafung8686/Desktop/python_sales-data/Sales-Data-Analysis.csv")

# 有哪些欄位
agg_product_data = sales_data.groupby(by="Product").nunique()  # 查看不重複清單的值
agg_product_data

# 新增美味分數

flavor_score = {
    "Beverages": 10,
    "Burgers": 5,
    "Chicken Sandwiches": 3,
    "Fries": 6,
    "Sides & Other": 2}

sales_data["flavor_score"] = sales_data['Product'].map(flavor_score)
print(sales_data)  # 只印出前五筆，方便檢查

# 處理遺漏值

sales_data = pd.read_csv(
    "/Users/tinafung8686/Desktop/python_sales-data/Sales-Data-Analysis.csv").dropna(how="all", subset=["Order ID"])

# 最後透過size檢查個數是否有增減情況確認遺漏值
sales_data.size

# 整欄或列為NaN(Not a Number)才會drop，但其他遺漏值希望補0
# 指定原始資料若有NaN則補0
sales_data = sales_data.fillna(0).astype(int)

# 資料篩選 isin()


# 假設這是你的銷售資料
data = {
    'Product': ['Beverages', 'Burgers', 'Fries', 'Beverages', 'Sides & Other'],
    'Quantity': [10, 5, 6, 8, 2],
    'Price': [25, 50, 30, 20, 15]
}
sales_data = pd.DataFrame(data)
print(sales_data)

# 1. 定義你感興趣的商品清單
products_to_filter = ['Beverages', 'Fries']

# 2. 使用 isin() 檢查 'Product' 欄位的值是否在清單中
is_in_list = sales_data['Product'].isin(products_to_filter)
print(is_in_list)  # 回傳一個boolean


# 3. 使用布林值進行篩選
filtered_sales = sales_data[is_in_list]
print("篩選後的銷售數據：")
print(filtered_sales)

# 找出空缺值

sales_data = pd.read_csv(
    "/Users/tinafung8686/Desktop/python_sales-data/Sales-Data-Analysis.csv")
missing_value = sales_data["Order ID"].isnull()  # 找出空缺值
exist_value = sales_data["Order ID"].notnull()  # 找出非空缺值

# 查詢數值區間 df.between()

sales_data = pd.read_csv(
    "/Users/tinafung8686/Desktop/python_sales-data/Sales-Data-Analysis.csv")
# 查詢ID 10452 訂單時間是否介於2022/11/1-2022/11/31

# 原地覆蓋值
sales_data["Date"] = pd.to_datetime(sales_data["Date"], format=('%d-%m-%Y'))


id = 10452  # int為10452時會是True, string為"10452"時為False
start_time = pd.to_datetime('01-11-2022')
end_time = pd.to_datetime('30-11-2022')

# 用來篩選布林值
is_match = (sales_data['Order ID'] == id) & (
    sales_data['Date'].between(start_time, end_time))
print(is_match)

# 根據布林值 Series 篩選 DataFrame中實際的欄位
query_result = sales_data[is_match]
print(query_result)

# df.duplicated

sales_data = pd.read_csv(
    "/Users/tinafung8686/Desktop/python_sales-data/Sales-Data-Analysis.csv")
sales_data

sales_data["Product"].duplicated()

# 印出所有重複的值，所以可以看到表格從index 5開始
sales_data[~sales_data["Product"].duplicated(keep="first")]
sales_data[sales_data["Product"].duplicated(keep=False)]

# df.drop_duplicated("欄位")

sales_data = pd.read_csv(
    "/Users/tinafung8686/Desktop/python_sales-data/Sales-Data-Analysis.csv")
sales_data

sales_data.drop_duplicates("Manager")

df = pd.DataFrame(data, columns=columns)

# 轉換日期格式

sales_data = pd.read_csv(
    "/Users/tinafung8686/Desktop/python_sales-data/Sales-Data-Analysis.csv")
sales_data["Date"] = pd.to_datetime(sales_data["Date"], format="%d-%m-%Y")
sales_data.info()

# 一氣呵成的變化時間格式
sales_data = pd.read_csv(
    "/Users/tinafung8686/Desktop/python_sales-data/Sales-Data-Analysis.csv", parse_dates=["Date"], date_format="%d-%m-%Y")
sales_data

# 篩出商品為Fries的所有資料
sales_data["Product"] == "Fries"  # 出現一列boolean
sales_data[sales_data["Product"] == "Fries"]

sales_data[sales_data["Date"] <=
           "2022-11-15"].sort_values("Date", ascending=False)

future_date = today + dt.timedelta(days=7)
print(f"今天加 7 天: {future_date}")

current_time = dt.datetime.now()
two_hours_later = current_time + dt.timedelta(hours=2)
print(f"現在加 2 小時: {two_hours_later}")

# 篩選

# AND
# 篩選出Purchase Type為In-store	 且 Payment Method是Gift Card的人
sales_data = pd.read_csv(
    "/Users/tinafung8686/Desktop/python_sales-data/Sales-Data-Analysis.csv", parse_dates=["Date"], date_format="%d-%m-%Y")
product_is_fries = sales_data["Product"] == "Fries"
city_is_london = sales_data["City"] == "London"
date_after_1225 = sales_data["Date"] > "2022-12-25"
sales_data[(product_is_fries & city_is_london) | date_after_1225].tail()

# 處理文字數據

sales_data = pd.read_csv(
    "/Users/tinafung8686/Desktop/python_sales-data/Sales-Data-Analysis.csv", parse_dates=["Date"], date_format="%d-%m-%Y")

# 全改為小寫
sales_data["Product"].str.lower()  # 全小寫
sales_data["Product"].str.upper()  # 全大寫
sales_data["Product"].str.title()  # 首字大寫，其徐小寫
sales_data["Product"].str.len()
sales_data["Product"].str.strip()  # 移除空白
sales_data["Product"].str.lstrip()  # 移除開頭空白
sales_data["Product"].str.rstrip()  # 移除結尾空白
sales_data["Product"].str.replace("Beverages", "drinks")  # 移除結尾空白
sales_data[sales_data["Payment Method"].str.contains("Gift")].head()

# 更改欄列的值
sales_data = pd.read_csv(
    "/Users/tinafung8686/Desktop/python_sales-data/Sales-Data-Analysis.csv", index_col=["Order ID"])
sales_data.columns = sales_data.columns.str.lower()
print(sales_data)

# get

sales_data = pd.read_csv(
    "/Users/tinafung8686/Desktop/python_sales-data/Sales-Data-Analysis.csv")
sales_data["Manager"].str.split(expand=True, n=1)  # expand，根據一個空格


# groupby案例1

sales_data = pd.DataFrame({
    '團隊': ['A隊', 'B隊', 'A隊', 'B隊', 'C隊', 'A隊'],
    '銷售額': [100, 150, 120, 180, 90, 110],
    '年齡': [25, 30, 28, 35, 22, 26]
})
print(sales_data)
# 使用 groupby()，將相同團隊合併並算出分組後的年齡平均值
team_avg_sales = sales_data.groupby('團隊').mean()
print(team_avg_sales)

# groupby案例2

sales_data = pd.read_csv(
    "/Users/tinafung8686/Desktop/python_sales-data/Sales-Data-Analysis.csv")
# 先查看壹下不重複值的狀況，方便我決定誰要當作groupby的項
# Product, City都很適合
sales_data.nunique()
new_data = sales_data.groupby("Purchase Type")
print(new_data)
# 查詢三種Purchase Type的第一項
new_data.size()
new_data.first()
new_data.last()

# groupby案例3
sales_data = pd.read_csv(
    "/Users/tinafung8686/Desktop/python_sales-data/Sales-Data-Analysis.csv")
new_data = sales_data.groupby(["Product", "Manager"])
new_data["Quantity"].sum()
new_data.size()
new_data = new_data({"Quantity": "sum"})

sales_data = pd.read_csv(
    "/Users/tinafung8686/Desktop/python_sales-data/Sales-Data-Analysis.csv", index_col=["Order ID"])
sales_data.columns = sales_data.columns.str.lower()
print(sales_data.columns)

sales_data["Manager"].str.split(expand=False)
sales_data = pd.read_csv(
    "/Users/tinafung8686/Desktop/python_sales-data/Sales-Data-Analysis.csv")
name = sales_data["Manager"].str.split(expand=True, n=1)
print(name)
# 根據一個空個分裂

# 九、merge DataFrame

food = pd.read_csv(
    "/Users/tinafung8686/Desktop/python_sales-data/restaurant_foods.csv")
customers = pd.read_csv(
    "/Users/tinafung8686/Desktop/python_sales-data/restaurant_customers.csv")
week1 = pd.read_csv(
    "/Users/tinafung8686/Desktop/python_sales-data/restaurant_week_1_sales.csv")
week2 = pd.read_csv(
    "/Users/tinafung8686/Desktop/python_sales-data/restaurant_week_2_sales.csv")

# 當欄位名稱一治，可以直接concat

# concat the two dataframe

len(week1)  # 250
len(week2)  # 250
# concat之後會是500 rows

pd.concat([week1, week2])
pd.concat([week1, week2], ignore_index=False)
pd.concat([week1, week2], ignore_index=True)
pd.concat([week1, week2], keys=["Week1", "Week2"]).sort_index()

#
df1 = pd.DataFrame([1, 2, 3], columns=["A"])
df2 = pd.DataFrame([1, 2, 3], columns=["B"])
pd.concat([df1, df2])
pd.concat([df1, df2], axis="index")
pd.concat([df1, df2], axis="columns")

# left joins using merge
week1.head()
food.head()
week1.merge(food, how="left", on="Food ID")

# right joins

week2.head()
customers.head()

# 現在要做merge。右邊是custimers, 左邊是week2

week2.merge(customers, how="left", left_on="Customer ID", right_on="ID").head()

# ID出現兩次，透過drop column移除重複欄位
week2.merge(customers, how="left", left_on="Customer ID",
            right_on="ID").drop(columns="ID")


week1.head()
week2.head()
week1.merge(week2, how="inner", on="Customer ID")
week1.merge(week2, how="inner", on="Customer ID",
            suffixes=[" - Week1", " - Week2"])

# (2)找出同個顧客連續2週買同樣food ID

week1.merge(week2, how="inner", on=[
            "Customer ID", "Food ID"]).sort_values("Customer ID")

condition1 = week1["Customer ID"] == 21  # boolean
condition2 = week1["Food ID"] == 4  # boolean
week1[condition1 & condition2]

condition1 = week2["Customer ID"] == 21  # boolean
condition2 = week2["Food ID"] == 4  # boolean
week2[condition1 & condition2]

# full joins()

week1.merge(week2, how="outer", on="Customer ID",
            suffixes=["Week1", " - Week2"])
merge = week1.merge(week2, how="outer", on="Customer ID",
                    suffixes=["Week1", " - Week2"], indicator=True)
merge["_merge"].value_counts()

merge[merge["_merge"].isin(["left_only", "right_only"])]

# merge

food = pd.read_csv(
    "/Users/tinafung8686/Desktop/python_sales-data/restaurant_foods.csv", index_col="Food ID")
customers = pd.read_csv(
    "/Users/tinafung8686/Desktop/python_sales-data/restaurant_customers.csv", index_col="ID")
week1 = pd.read_csv(
    "/Users/tinafung8686/Desktop/python_sales-data/restaurant_week_1_sales.csv")
week2 = pd.read_csv(
    "/Users/tinafung8686/Desktop/python_sales-data/restaurant_week_2_sales.csv")
week1.head()
customers.head()
week1.merge(customers, how='left', left_on="Customer ID",
            right_index=True)  # 右表要合併的不是columns而是index

# merge with food table

food.head()
week1.merge(customers, how='left', left_on="Customer ID", right_index=True).merge(
    food, how="left", left_on="Food ID", right_index=True)

# the join method

food = pd.read_csv(
    "/Users/tinafung8686/Desktop/python_sales-data/restaurant_foods.csv", index_col="Food ID")
customers = pd.read_csv(
    "/Users/tinafung8686/Desktop/python_sales-data/restaurant_customers.csv", index_col="ID")
week1 = pd.read_csv(
    "/Users/tinafung8686/Desktop/python_sales-data/restaurant_week_1_sales.csv")
week2 = pd.read_csv(
    "/Users/tinafung8686/Desktop/python_sales-data/restaurant_week_2_sales.csv")
week1_time = pd.read_csv(
    "/Users/tinafung8686/Desktop/python_sales-data/restaurant_week_1_times.csv")

week1_time.head()

week1.merge(week1_time, how="left", left_index=True, right_index=True)
# a shortcut method
week1.join(week1_time)

# dates and time


someday = dt.date(2025, 10, 30)
someday.year  # 2025
someday.month  # 10
someday.day  # 30

sometime = dt.datetime(2025, 10, 30, 1, 4, 30)
sometime.hour  # 1
sometime.minute  # 4
sometime.second  # 30

# ------------------
pd.Timestamp(2025, 10, 23)
pd.Timestamp(dt.date(2025, 10, 23))

pd.Timestamp(2025, 10, 23, 23, 59, 59)
pd.Timestamp(dt.datetime(2025, 10, 23, 23, 59, 59))

pd.Timestamp("2025-01-02")
pd.Timestamp("2025/01/02")
pd.Timestamp("2025/01/02 10:23:40")


# pd.date_range()

pd.date_range(start="2025-01-20", end="2025-01-31")

pd.date_range(start="2025-01-20", end="2025-01-31", freq="2D")
pd.date_range(start="2025-01-20", end="2025-01-31", freq="B")
pd.date_range(start="2025-01-20", end="2025-01-31", freq="W-Fri")
pd.date_range(start="2025-01-20 00:00:00", end="2025-01-20 12:00:00", freq="H")
pd.date_range(start="2025-01-01", end="2025-12-31", freq="M")
pd.date_range(start="2025-01-01", end="2025-12-31", freq="MS")
pd.date_range(start="2025-01-01", end="2030-12-31", freq="AS")
pd.date_range(start="2025-01-20", freq="D", periods=11)

# dt->datetime

selected_days = pd.Series(pd.date_range(
    start="2025-01-01", end="2025-5-30", freq="10D 12H"))
selected_days

selected_days.dt.year
selected_days.dt.month
selected_days.dt.hour
selected_days.dt.day_of_year
selected_days.dt.day_of_week
selected_days.dt.day_name()
selected_days.dt.is_month_end  # boolean，是否為當月最後一天
selected_days.dt.is_quarter_start
selected_days[selected_days.dt.is_quarter_start]

# 121.select rows from a dataframe

stocks = pd.read_csv(
    "/Users/tinafung8686/Desktop/python vscode/pandas/Incomplete/ibm.csv")
stocks.head()

# 將日期設為index
stocks = pd.read_csv(
    "/Users/tinafung8686/Desktop/python vscode/pandas/Incomplete/ibm.csv", index_col="Date").sort_index()
stocks.head()
stocks.info()

stocks.iloc[300]  # 第300行資料數據
stocks.loc["2020-10-30"]  # label為2020/10/30數據

# 以下結果相等
stocks.loc["2020-10-30": "2020-12-31"]  # 取時間區間
stocks.loc[pd.Timestamp(2020, 10, 30):pd.Timestamp(2020, 12, 31)]
stocks.truncate("2020-10-30", "2020-12-31")

#
stocks.loc["2020-10-30", "Close"]
# np.float64(99.8367)
stocks.loc["2020-10-30", "High":"Close"]
# High     99.9730
# Low      96.3450
# Close    99.8367
# Name: 2020-10-30, dtype: float64

# 計算date

stocks = pd.read_csv(
    "/Users/tinafung8686/Desktop/python vscode/pandas/Incomplete/ibm.csv", parse_dates=["Date"], index_col="Date").sort_index()
stocks.head()
stocks.info()

# 針對每個日期，加減5天
stocks.index
stocks.index + pd.DateOffset(days=5)
stocks.index - pd.DateOffset(years=5)
stocks.index + pd.DateOffset(years=1, months=2,
                             days=3, hours=9, minutes=34, seconds=17)

# find the IBM stock on every of my birthday(10/30)

my_birthday = pd.date_range(
    start="1992-10-30", end="2020-10-30", freq=pd.DateOffset(years=1))
stocks[stocks.index.isin(my_birthday)]

# timedeltas

pd.Timestamp("2023-10-31 21:40:39") - pd.Timestamp("2023-10-10 12:49:02")
pd.Timestamp("2023-10-10 12:49:02") - pd.Timestamp("2023-10-31 21:40:39")
pd.Timedelta(days=3, hours=23, minutes=28, seconds=53)
pd.Timedelta("10 hours 4 minutes 1 seconds")

# ex1:查找下單到運送之間的時間差

ecommerce = pd.read_csv("/Users/tinafung8686/Desktop/python vscode/pandas/Incomplete/ecommerce.csv",
                        index_col="ID", parse_dates=["order_date", "delivery_date"], date_format="%m/%d/%y")
ecommerce.dtypes  # datetime64[ns]

# 取得兩時間差
ecommerce["delivery_date"] - ecommerce["order_date"]

# 將時間差黏在原先表格中

ecommerce["delivery_time"] = ecommerce["delivery_date"] - \
    ecommerce["order_date"]
ecommerce

# 若所需運送時間變為2倍

ecommerce["double_delivery_time"] = ecommerce["delivery_date"] + \
    ecommerce["delivery_time"]
ecommerce

# input and output


def safe_read_csv(url: str, **kwargs) -> pd.DataFrame:
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    with urlopen(url, context=ssl_context) as response:
        csv_data = response.read().decode("utf-8")
    return pd.read_csv(StringIO(csv_data), **kwargs)


url = "https://data.cityofnewyork.us/api/views/25th-nujf/rows.csv"
baby_names = safe_read_csv(url)

# 下載csv
baby_names.to_csv("crazy_baby_names.csv")

# import excel
import pandas as pd
single_data = pd.read_excel(
    "/Users/tinafung8686/Desktop/python vscode/pandas/Incomplete/Data - Single Worksheet.xlsx")

#若一張表格裡有多個分頁，預設只會讀取第一個分頁
multiple_data1 = pd.read_excel("/Users/tinafung8686/Desktop/python vscode/pandas/Incomplete/Data - Multiple Worksheets.xlsx", sheet_name="Data 1") # sheet_name = 0
multiple_data2 = pd.read_excel("/Users/tinafung8686/Desktop/python vscode/pandas/Incomplete/Data - Multiple Worksheets.xlsx", sheet_name="Data 2") # sheet_name = 1
# 同時匯入多張分頁
multiple_data12 = pd.read_excel("/Users/tinafung8686/Desktop/python vscode/pandas/Incomplete/Data - Multiple Worksheets.xlsx", sheet_name=["Data 1","Data 2"]) ## sheet_name = 0,1

# 如果要抓到所有分頁，還可以透過None
multiple_data12 = pd.read_excel("/Users/tinafung8686/Desktop/python vscode/pandas/Incomplete/Data - Multiple Worksheets.xlsx", sheet_name=None) ## sheet_name = 全部。在 pd.read_excel() 這個函式中，當你將 sheet_name 設為 None 時，Pandas 就會把這個行為解釋為：「使用者沒有指定任何特定的工作表，所以我的預設行為是處理所有工作表。」

# 想要根據性別，男性一張表、女性一張表

# visualization

import pandas as pd
import matplotlib.pyplot as plt

ibm = pd.read_csv("/Users/tinafung8686/Desktop/python vscode/pandas/Incomplete/ibm.csv", parse_dates=["Date"],index_col="Date").sort_index()
ibm.head()
# 繪製圖
ibm.plot()

# 指定x\y軸
ibm.plot(y="Close")

#有顏色的style
plt.style.available
plt.style.use("seaborn-v0_8-colorblind")
# ibm.plot(y="Close") 

# bar charts

import pandas as pd
import matplotlib.pyplot as plt
ibm = pd.read_csv("/Users/tinafung8686/Desktop/python vscode/pandas/Incomplete/ibm.csv", parse_dates=["Date"],index_col="Date").sort_index()
def rank_performance(stock_price):
    if stock_price <= 50:
        return "Poor"
    elif stock_price > 50 and stock_price <= 100:
        return "Average"
    else:
        return "Excellent"

ibm["Close"].apply(rank_performance)
ibm["Close"].apply(rank_performance).value_counts() # an ideal shape for a bar chart
ibm["Close"].apply(rank_performance).value_counts().plot(kind = "bar")
ibm["Close"].apply(rank_performance).value_counts().plot(kind = "barh") #horizontal

# pie charts

average_stock_price = ibm["Close"].mean()

def average_stock(stock_price):
    if stock_price <= average_stock_price:
        return "Below Average"
    else:
        return "Above Average"
    
plot_data = ibm["Close"].apply(average_stock).value_counts().plot(kind="pie", legend=True)

# options and settings

## 使用np.array產出亂數表格

import pandas as pd
import numpy as np
# np隨便產出一個整數，介於0-100
np.random.randint(0,100)
# np隨便產出一個整數，介於0-100,欄位大小為20*30
np.random.randint(0,100,[20,30])
type(np.random.randint(0,100,[20,30])) #numpy.ndarray

## 指定為表格

pd.DataFrame(np.random.randint(0,100,[20,30]))


