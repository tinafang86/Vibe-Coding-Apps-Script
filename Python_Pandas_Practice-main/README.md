# Python_Practice
這份專案練習以Kaggle中的[銷售資料](https://www.kaggle.com/datasets/rohitgrewal/restaurant-sales-data)為例作為資料庫操作練習

## 零、資料清理順序

## 一、匯入資料 

```
import pandas as pd
sales_data = pd.read_csv("/Users/tinafung8686/Desktop/python_sales-data/Sales-Data-Analysis.csv")
print(sales_data)
```

## 二、創建資料

### pd.DataFrame():最基本的創建一個DataFrame物件，可以把它想像為一個Excel表格，有以下幾種常見用法

- **字典 Dictionary：key為欄位名稱，value為欄位資料**
```
import pandas as pd
data = {
    '姓名': ['張三', '李四', '王五'],
    '年齡': [25, 30, 35],
    '城市': ['台北', '高雄', '台中']
}
df = pd.DataFrame(data)
print(df)
```
***
```
   姓名  年齡  城市
0  張三  25  台北
1  李四  30  高雄
2  王五  35  台中
```
***

- **列表List裡的字典**
```
import pandas as pd
data = [
    {'姓名': '張三', '年齡': 25, '城市': '台北'},
    {'姓名': '李四', '年齡': 30, '城市': '高雄'},
    {'姓名': '王五', '年齡': 35, '城市': '台中'}
]
df = pd.DataFrame(data)
print(df)
```
***

```
   姓名  年齡  城市
0  張三  25  台北
1  李四  30  高雄
2  王五  35  台中
```
  
- **使用二維列表 List of List**

```
import pandas as pd
data = [
    ['張三', 25, '台北'],
    ['李四', 30, '高雄'],
    ['王五', 35, '台中']
]
# 使用 columns 參數來指定欄位名稱
columns = ['姓名', '年齡', '城市']
df = pd.DataFrame(data, columns=columns)
print(df)
```
***
```
   姓名  年齡  城市
0  張三  25  台北
1  李四  30  高雄
2  王五  35  台中
```

## 三、常用解析資料指令

- sales_data.size

    - 回傳`DataFrame`中所有元素。等於欄*列，不考慮遺漏值(NaN)
    - E.G. 共有2286個項目

- sales_data.shape 

    - 回傳一個tuple，包含(列, 欄)
    - (254, 9)->25列9欄

- sales_data.count

    - 回傳非空值 (non-null)
    - E.G.，可以看到每一欄的數量一樣，代表沒有遺漏值

```
Order ID          254
Date              254
Product           254
Price             254
Quantity          254
Purchase Type     254
Payment Method    254
Manager           254
City              254
dtype: int64

```
```
import pandas as pd

# 建立一個包含遺漏值的 DataFrame
df = pd.DataFrame({
    '學生ID': [101, 102, 103, 104, 105],
    '國文': [85, 90, np.nan, 78, 88],
    '數學': [75, 88, 92, np.nan, 95],
    '英文': [95, 80, np.nan, 90, np.nan],
    '性別': ['男', '女', '男', '女', np.nan]
})

print(df)
valid_counts = df.count()
print(valid_counts)
```
```
原始 DataFrame：
   學生ID   國文   數學   英文 性別
0   101  85.0  75.0  95.0  男
1   102  90.0  88.0  80.0  女
2   103   NaN  92.0   NaN  男
3   104  78.0   NaN  90.0  女
4   105  88.0  95.0   NaN  NaN

學生ID    5
國文      4
數學      4
英文      3
性別      4
dtype: int64
```

- sales_data.values  
    - 打印出所有的值，不取labels

```
import pandas as pd
import numpy as np

data = pd.DataFrame({
    '姓名': ['小明', '小華', '小李'],
    '年齡': [25, 30, 28],
    '城市': ['台北', '台中', '高雄']
}, index=['a', 'b', 'c'])
print(data)
raw_data = data.values
print(raw_data)
```
```
原始 DataFrame：
    姓名  年齡  城市
a  小明  25  台北
b  小華  30  台中
c  小李  28  高雄
------------------------------
使用 .values 屬性後的結果：
[['小明' 25 '台北']
 ['小華' 30 '台中']
 ['小李' 28 '高雄']]
 ```

- sales_data.index  索引值

    - E.G. RangeIndex(start=0, stop=254, step=1) 有253列
    - 可以回傳所有的標籤 (row labels)
    - .index可以最為`.loc` 的選取標籤基礎，或者merge、concat dataframe時用來對齊數據

```
# label = integer
import pandas as pd
df_default = pd.DataFrame({
    '產品': ['A', 'B', 'C'],
    '價格': [100, 150, 120]
})
print(df_default.index)

# label = custom label
df_custom = pd.DataFrame({
    '產品': ['A', 'B', 'C'],
    '價格': [100, 150, 120]
}, index=['第一季', '第二季', '第三季'])
print(df_custom)
```
```
   產品  價格
0  A   100
1  B   150
2  C   120
------------
      產品  價格
第一季  A   100
第二季  B   150
第三季  C   120
```
- sales_data.columns 回傳每一欄的值
```
Index(['Order ID', 'Date', 'Product', 'Price', 'Quantity', 'Purchase Type',
       'Payment Method', 'Manager', 'City'],
      dtype='object')
```

<img src="/images/03.png" width="50%">

- sales_data.dtypes  

    - 查看個欄位的data type
```
import pandas as pd
# 建立一個模擬的 DataFrame
sales_data_mock = pd.DataFrame({
    '日期': pd.to_datetime(['2022-01-01', '2022-01-02']),
    '產品名稱': ['薯條', '漢堡'],
    '數量': [2, 1],
    '單價': [30.5, 85.0]
})
print(sales_data_mock)
data_types = sales_data_mock.dtypes
print(data_types)
```
```
    日期      產品名稱 數量 單價
0 2022-01-01    薯條   2  30.5
1 2022-01-02    漢堡   1  85.0
------------------------------
使用 .dtypes 屬性後的結果：
日期         datetime64[ns]
產品名稱           object
數量              int64
單價            float64
dtype: object
```

- sales_data.head()  

    - 預設前五筆資料
- sales_data.tail()  

    - 預設後五筆資料
- sales_data.info 

    - 查看Dtype, memory狀況等等。尤其要注意日期是否為datetime格式
```
import pandas as pd
import numpy as np
data_mock = pd.DataFrame({
    '日期': pd.to_datetime(['2022-01-01', '2022-01-02', '2022-01-03']),
    '產品名稱': ['薯條', '漢堡', '漢堡'],
    '數量': [2, 1, np.nan],
    '價格': [30.5, 85.0, 85.0],
    '城市': ['台北', np.nan, '高雄']
})
print(data_mock)
# 使用 .info() 函式
data_mock.info()
```
```
          日期 產品名稱   數量    價格   城市
0 2022-01-01    薯條  2.0  30.5  台北
1 2022-01-02    漢堡  1.0  85.0  NaN
2 2022-01-03    漢堡  NaN  85.0  高雄
------------------------------
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 3 entries, 0 to 2
Data columns (total 5 columns):
 #   Column  Non-Null Count  Dtype         
---  ------  --------------  -----         
 0   日期      3 non-null      datetime64[ns]
 1   產品名稱    3 non-null      object        
 2   數量      2 non-null      float64       ->有一個遺漏值
 3   價格      3 non-null      float64       
 4   城市      2 non-null      object        ->有一個遺漏值
dtypes: datetime64[ns](1), float64(2), object(2)
memory usage: 248.0+ bytes
```

<img src="/images/06.png" width="50%">

- sales_date.to_date()

    - to_date是一種將資料轉成日期格式的格式，但不能協助變更日期年月日呈現方式。
    - 因此format=xxx必須跟著原始raw data的形式，但若要改變呈現方式可以使用df.strftime()->字串string的格式化時間**

```
import pandas as pd
sales_data = pd.read_csv(
    "/Users/tinafung8686/Desktop/python_sales-data/Sales-Data-Analysis.csv")
sales_data["Date"] = pd.to_datetime(sales_data["Date"], format="%d-%m-%Y")
sales_data.info()
```
<img src="/images/07.png" width="50%">

一氣呵成的變換完格式。parse_date()在找遍哪一欄，date_format()則再決定變更格式

```
import pandas as pd
sales_data = pd.read_csv(
    "/Users/tinafung8686/Desktop/python_sales-data/Sales-Data-Analysis.csv", parse_dates=["Date"], date_format = "%d-%m-%Y" )
```

- sales_data.unique() 

    - 查看個欄位不重複的值的個數

```
import pandas as pd
data = {'姓名': ['小明', '小華', '小明', '小華', '小李'],
        '部門': ['業務', '', '業務', '技術', '行政'],
        '薪水': [30000, 50000, 30000, 50000, 35000]}
df = pd.DataFrame(data)
print(df)
```
```
   姓名  部門     薪水
0  小明  業務  30000
1  小華  技術  50000
2  小明  業務  30000
3  小華  技術  50000
4  小李  行政  35000
```
```
print(df.nunique())
# 若要包含NaN，則nunique(dropna = False)
```
```
姓名    3
部門    3
薪水    3
dtype: int64
```

## 四、專注處理單一或少數欄位

- 只看特定欄位，用欄位名稱查找：usecol = ["col_A", "col_B",...]
- 取得Product、Payment Method欄位，透過column name取得

```
import pandas as pd
datas = pd.read_csv("/Users/tinafung8686/Desktop/python_sales-data/Sales-Data-Analysis.csv", usecols=["Product","Payment Method"])
print(datas)
```
<img src="/images/01.png" width="50%">

***

- 只看特定欄位，用欄位index查找：usecol = ["index1", "index2",...]
- 取得Product、Payment Method欄位，透過column index取得
```
datas = pd.read_csv("/Users/tinafung8686/Desktop/python_sales-data/Sales-Data-Analysis.csv", usecols=[2,5])
datas
```

## 五、squeeze為純量（無維度）

- squeeze()擠壓，將多餘的維度擠掉讓維度降至最低

    - 從 DataFrame 變成 Series：當你的 DataFrame 只有 1 行 或 1 欄 時。
    - 從 Series 變成純量值 (Scalar)：當你的 Series 只有 1 個值 時。

- df.squeeze()：不帶參數，會自動判斷是否有只有 1 個維度可以擠壓。
- df.squeeze("columns")：明確指定要擠壓的是欄位維度。

```
datas = pd.read_csv("/Users/tinafung8686/Desktop/python_sales-data/Sales-Data-Analysis.csv", usecols=["Product"]).squeeze("columns")
```
<img src="/images/02.png" width="50%">

```
import pandas as pd

# 範例一：單欄的 DataFrame
df_one_col = pd.DataFrame({'A': [1, 2, 3]})
print(df_one_col)
print(type(df_one_col))

# 擠壓欄位
s1 = df_one_col.squeeze()
print(s1)
print(type(s1))
```
```
   A
0  1
1  2
2  3
<class 'pandas.core.frame.DataFrame'>
----------
0    1
1    2
2    3
Name: A, dtype: int64
<class 'pandas.core.series.Series'>

```

- df.squeeze("index")：明確指定要擠壓的是index維度。

    - df_one_row 只有一個索引（0），squeeze("index") 會將這個多餘的「索引」維度擠壓掉，同樣把它變成一個 Series。
    - 轉換後的 Series 保留了欄位名稱 (A, B, C) 作為新的索引，而原本的索引 (0) 則變成了 Name。型態同樣變成了 Series。


```
df_one_row = pd.DataFrame({'A': [1], 'B': [2], 'C': [3]})
print(df_one_row)
```
```
   A  B  C
0  1  2  3
```

```
import pandas as pd
# 建立一個包含多項商品的 DataFrame
products_df = pd.DataFrame({
    '商品': ['筆電', '手機', '平板'],
    '價格': [30000, 20000, 15000],
    '庫存': [10, 25, 12]
})

# 篩選出價格為 20000 的商品
single_product_df = products_df[products_df['價格'] == 20000]
print(single_product_df)
print(f"型態：{type(single_product_df)}")
```

```
   商品   價格  庫存
1  手機  20000  25
型態：<class 'pandas.core.frame.DataFrame'>
```

```
single_product_series = single_product_df.squeeze("index")
print(single_product_series)
print(f"型態：{type(single_product_series)}")
```

```
商品       手機
價格      20000
庫存       25

Name: 1, dtype: object
型態：<class 'pandas.core.series.Series'>
```

## 六、調整欄位順序

### 1. 牽涉copy（複製） and view（視圖）概念
### (1) copy：複製DataFrame

```
datas = pd.read_csv("/Users/tinafung8686/Desktop/python_sales-data/Sales-Data-Analysis.csv",
                    usecols=["Product", "Payment Method"])
```
#### 方法一：透過新變數定義新資料表。不會操作到原始資料，而是複製到 data_restored 這個新的變數 （更常用）
```
# 以下儲存兩個欄爲順續不同的DataFrame
data_restored1 = datas[["Product", "Payment Method"]]
data_restored2 = datas[["Payment Method", "Product"]]
```

#### 方法二：使用使用 pd.DataFrame() 建立新物件

- 請根據 datas 這個數據源，建立一個新的DataFrame，但新DataFrame 中只包含 Payment Method 和 Product 這兩個欄位，並且 Payment Method 必須是第一個欄位，Product 是第二個。

```
pd.DataFrame(datas, columns=["Payment Method", "Product"])
```

***

### (2) view:檢視DataFrame
#### 方法一：直接針對原始資料新增一個新欄位
```
import pandas as pd
sales_data = pd.read_csv(
    "/Users/tinafung8686/Desktop/python_sales-data/Sales-Data-Analysis.csv")
sales_data["grade"] = [100,100,100,100] ＃ 新增一個grade欄位
```

#### 方法二：使用.loc或.iloc

- .loc:基於標籤 (label) 進行索引和修改。

df.loc[列的值, 欄的值]

```
import pandas as pd
df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]}, index=['x', 'y', 'z'])

# 將索引 'y' 的 'B' 欄位值修改為 99
df.loc['y', 'B'] = 99
print(df)

------------
原始
   A   B
x  1   4
y  2   5
z  3   6
------------
結果
   A   B
x  1   4
y  2  99
z  3   6
```

```
import pandas as pd
# 創建一個 DataFrame 來記錄學生成績
grades_data = {
    '國文': [85, 92, 78],
    '數學': [90, 88, 95],
    '英文': [75, 80, 82]
}
students = ['小明', '小華', '小強']
grades_df = pd.DataFrame(grades_data, index=students)
print(grades_df)

   國文  數學  英文
小明  85  90  75
小華  92  88  80
小強  78  95  82

```

- 使用 .loc 選取 '小華' 到 '小強' (包含) 的列，和 '國文' 到 '英文' (包含) 的欄

```
subset_loc = grades_df.loc['小華':'小強', '國文':'英文']
print(subset_loc)
```

```
     國文  數學  英文
小華  92  88  80
小強  78  95  82
```

- .iloc:基於位置 (position) 進行索引和修改。

```
grades_data = {
    '國文': [85, 92, 78],
    '數學': [90, 88, 95],
    '英文': [75, 80, 82]
}
students = ['小明', '小華', '小強']
grades_df = pd.DataFrame(grades_data, index=students)
print(grades_df)
```
```
   國文  數學  英文
小明  85  90  75
小華  92  88  80
小強  78  95  82
```

```
score_iloc = grades_df.iloc[1, 1]
print(f"\n小華的數學成績 (iloc)：{score_iloc}")

# 小華的數學成績 (iloc)：88
```

## 七、整理資料

### 1.處理文字數據

```
sales_data["Product"].str.lower() #全小寫
sales_data["Product"].str.upper() #全大寫
sales_data["Product"].str.title() #首字大寫，其徐小寫
sales_data["Product"].str.len() #字數
sales_data["Product"].str.strip() # 移除空白
sales_data["Product"].str.lstrip() #移除開頭空白
sales_data["Product"].str.rstrip() #移除結尾空白
sales_data["Product"].str.replace("Beverages", "drinks") 
#將Beverages全部改為drinks
```

```
sales_data[sales_data["Payment Method"].str.contains("Gift")].head()
```
<img src="/images/08.png" width="50%">

```
sales_data[sales_data["Manager"].str.lower().str.startswith("tom")].head()
```

```
import datetime as dt
import pandas as pd
sales_data = pd.read_csv(
    "/Users/tinafung8686/Desktop/python_sales-data/Sales-Data-Analysis.csv", index_col=["Order ID"])
sales_data.columns = sales_data.columns.str.lower()
print(sales_data.columns)
```
```
Index(['date', 'product', 'price', 'quantity', 'purchase type',
       'payment method', 'manager', 'city'],
      dtype='object')
```

### 2. 處理文字數據 - .str.get()

- get(0):列表中第1個元素
- get(1):列表中第2個元素
- 以下範例解釋：從資料庫取值之後，我只要取"Manager"（姓名）欄位。因為名字中間有空白值，所以用split將其分為不同元素。例如"Tina Fang"->["Tina", "Fang"]
- get(0)用來取[ ]中第一個元素，得到"Tina"
- value_counts則將每一個元素計算unique value出現的次數

```
import datetime as dt
import pandas as pd
sales_data = pd.read_csv(
    "/Users/tinafung8686/Desktop/python_sales-data/Sales-Data-Analysis.csv")

sales_data["Manager"].str.split().str.get(0).value_counts() 

Manager
Tom       75
Joao      75
Pablo     46
Walter    30
Remy      28
Name: count, dtype: int64
```

### 3. 處理文字數據 - .str.split(expand = True/False)

- ``df..str.split(expand = False)``:預設值，會被儲存為列表方便後續操作
- ``df..str.split(expand = True)`` :會被展開成新的DataFrame
```
import datetime as dt
import pandas as pd
sales_data = pd.read_csv(
    "/Users/tinafung8686/Desktop/python_sales-data/Sales-Data-Analysis.csv")
sales_data["Manager"].str.split(expand=False)

0        [Tom, Jackson]
1        [Pablo, Perez]
2         [Joao, Silva]
3      [Walter, Muller]
4      [Walter, Muller]
             ...       
249    [Walter, Muller]
250    [Walter, Muller]
251    [Walter, Muller]
252    [Walter, Muller]
253    [Walter, Muller]
Name: Manager, Length: 254, dtype: object
```
- ``df..str.split(expand = True, n=1)``:展開為新的DataFrame，且只分割一次(n=1)
```
sales_data["Manager"].str.split(expand=True, n = 1)
# 根據一個空個分裂

	0	1
0	Tom	Jackson
1	Pablo	Perez
2	Joao	Silva
3	Walter	Muller
4	Walter	Muller
...	...	...
249	Walter	Muller
250	Walter	Muller
251	Walter	Muller
252	Walter	Muller
```


### 4. 處理遺漏值

#### (1) dropna():刪除遺漏值
- dropna(how = "all")：如果整欄或整列都為遺漏值NaN，就刪去他
- dropna(how = "any")：如果整欄或整列有一個遺漏值NaN，就刪去他

```
import pandas as pd
sales_data = pd.read_csv(
    "/Users/tinafung8686/Desktop/python_sales-data/Sales-Data-Analysis.csv").dropna(how = "all")

# 最後透過size或info檢查個數是否有增減情況確認遺漏值
sales_data.size
sales_data.info
```

#### (2) fillna():填補遺漏值
- fillna(0)：前面常見使用dropna(how = "all")刪除整列0的數據，但那些少數NaN (Not a Number)在表格裡，此時指定他為0
- NaN就算指定為0，在資料型態中仍然算是float，因此建議搭配 astype():()裡面可以放float, int, ...

```
import pandas as pd
sales_data = pd.read_csv(
    "/Users/tinafung8686/Desktop/python_sales-data/Sales-Data-Analysis.csv").dropna(how="all")
sales_data = sales_data.fillna(0).astype(int)
```
***

#### (3) billna():由遺漏值下一位數字填補

- 時間序列資料：例如預測接下來股市資料，可以用後面的數字補值會更準
- 資料延遲：股市交易時因為資料太大來不及運算，會先用NaN補空值，bfill()則可以取一個較能反應最終資料的數值。
- 與ffill為互補關係。例如最開頭的NaN
***

#### (4) isnull()/ notnull():找出空缺值 

- df.isnull():找出空缺值。若值為NaN則為True，否則為False
- df.notnull()：找出非空缺值。若值為非空缺值則為True，否則為False

```
sales_data = pd.read_csv(
    "/Users/tinafung8686/Desktop/python_sales-data/Sales-Data-Analysis.csv")
missing_value = sales_data["Order ID"].isnull() #找出空缺值
//
0      False
1      False
2      False
3      False
4      False
       ...  
249    False
250    False
251    False
252    False
253    False
Name: Order ID, Length: 254, dtype: bool
//
exist_value = sales_data["Order ID"].notnull() # 找出非空缺值

0      True
1      True
2      True
3      True
4      True
       ... 
249    True
250    True
251    True
252    True
253    True
```
***

#### (5) 處理特定資料的遺漏值：subset["",""]子集功能
- 請在 sales_data 中，只檢查 Order ID 這一個欄位。如果某列的 Order ID 欄位是空的（NaN），那麼就將整列資料都移除。
```
sales_data = pd.read_csv(
    "/Users/tinafung8686/Desktop/python_sales-data/Sales-Data-Analysis.csv").dropna(how="all", subset = ["Order ID"])
```
***
### 5. 排序數字
#### (1) sort_values(ascending = True) (由小到大)
- Series的sort_values()
```
import pandas as pd
## 第一種寫法
new_data = pd.read_csv(
    "/Users/tinafung8686/Desktop/python_sales-data/Sales-Data-Analysis.csv", usecols=["Price"]).sort_values(by = "Price")
## 第二種寫法。squeeze之後表上剩下一欄，所以不用sort by xxx
new_data = pd.read_csv(
    "/Users/tinafung8686/Desktop/python_sales-data/Sales-Data-Analysis.csv", usecols=["Price"]).squeeze("columns").sort_values()
```
- DataFrame的sort_values()

```
import pandas as pd
sales_data = {
    '地區': ['台北', '高雄', '台北', '台中'],
    '產品': ['A', 'B', 'A', 'C'],
    '銷售額': [150, 200, 100, 250],
    '日期': ['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04']
}
sales_df = pd.DataFrame(sales_data)
print(sales_df)
```

```
# by 指定排序的欄位，ascending=False 表示降序排列
sorted_by_sales = sales_df.sort_values(by='銷售額', ascending=False)
print(sorted_by_sales)
```

```
    地區 產品 銷售額   日期
3   台中  C  250  2023-01-04
1   高雄  B  200  2023-01-02
0   台北  A  150  2023-01-01
2   台北  A  100  2023-01-03
```

#### (2) 操作一個欄位
```
import pandas as pd
sales_data = pd.read_csv(
    "/Users/tinafung8686/Desktop/python_sales-data/Sales-Data-Analysis.csv")
sales_data.sort_values(by = "Price") # 價錢由小到大
sales_data.sort_values(by = "Price", ascending=False) # 價錢由大到小
```
#### (3) 操作多個欄位
```
import pandas as pd
sales_data = pd.read_csv(
    "/Users/tinafung8686/Desktop/python_sales-data/Sales-Data-Analysis.csv")
sales_data.sort_values(by = ["Price","Quantity"]) # 根據Price由小到大，Quantity也由小到大

sales_data.sort_values(by = ["Price","Quantity"], ascending=[False, True]) # 價錢由大到小，Quantity由小到大

```
- sort_index(ascending = True) (由小到大)
sort_index(ascending = False) (由大到小)

```
import pandas as pd
df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]}, index=['C', 'A', 'B'])
   A  B
C  1  4
A  2  5
B  3  6

df_sorted = df.sort_index(axis = 0) # ascending預設為True，由小到大

    A	B
A	2	5
B	3	6
C	1	4

df_sorted = df.sort_index(axis = 0, ascending = False) # axis = 0針對列索引值排序，axis = 1針對欄索引值排序

    A	B
C	1	4
B	3	6
A	2	5

df_sorted = df.sort_index(axis = 1, ascending = False) # 操作欄，由大到小排序

    B	A
C	4	1
A	5	2
B	6	3
```

### 6. Series取值
#### (1).get_group()

將原始資料轉為Series，Product為索引index，Price為欄
```
data01 = pd.read_csv(
    "/Users/tinafung8686/Desktop/python_sales-data/Sales-Data-Analysis.csv", usecols=["Product", "Price"], index_col=["Product"])
```

發現index重複度很高，用groupby()將一樣的值合併，但需要注意 ***groupby()是分組操作不會直接顯示成果***

```
onlydata = data01.groupby(by = "Product")

----
# <pandas.core.groupby.generic.DataFrameGroupBy object at 0x1269b6c60>
```
onlydata.column，得知欄位包含Beverages、Burgers、Chicken Sandwiches、Fries、Sides & Other 

```
print(onlydata.mean())
------
#                         Price
# Product                      
# Beverages            2.950000
# Burgers             12.990000
# Chicken Sandwiches  10.317308
# Fries                3.921569
# Sides & Other        4.990000
```
透過get_group找出burger的價錢

```
burgerdata = onlydata.get_group("Burgers")
print(burgerdata)

----------------
       Price
Product	
Burgers	12.99
Burgers	12.99
Burgers	12.99
Burgers	12.99
Burgers	12.99
Burgers	12.99
Burgers	12.99
Burgers	12.99
Burgers	12.99
Burgers	12.99
Burgers	12.99

```
##### (2) .loc()
```
data01 = pd.read_csv(
    "/Users/tinafung8686/Desktop/python_sales-data/Sales-Data-Analysis.csv", usecols=["Product", "Price"], index_col=["Product"])
# 發現index重複度很高，用groupby()將一樣的值合併，但需要注意groupby()是分組操作不會直接顯示成果
onlydata = data01.groupby(by = "Product")

# groupby不可以使用loc
average_data = onlydata.mean()
burgerdata = average_data.loc["Burgers", "Price"] # loc["第一個索引值，取索引標籤"，"第二個索引值，取欄位"]
# np.float64(12.99)

```

### 7. DataFrame取值

- df[value1]
- df.loc[列的標籤, 欄的標籤] (推薦)

#### 計算每一列個數

```
datas = pd.read_csv("/Users/tinafung8686/Desktop/python_sales-data/Sales-Data-Analysis.csv",
                    usecols=["Product"])

datas.value_counts()
------------------------------

                   Product           
Burgers               52
Chicken Sandwiches    52
Fries                 51
Beverages             50
Sides & Other         49
Name: count, dtype: int64
```

#### 計算每一列個數並換算為比例

```
datas = pd.read_csv("/Users/tinafung8686/Desktop/python_sales-data/Sales-Data-Analysis.csv",
                    usecols=["Product"])
datas.value_counts() #計算個數
datas.value_counts(normalize = True) #計算個數並換算為比例 # Return proportions rather than frequencies.

```

#### 計算欄位為數字的項目並加總，如Quantity
```
# 計算欄位為數字的項目並加總，如Quantity
import pandas as pd
sales_data = pd.read_csv(
    "/Users/tinafung8686/Desktop/python_sales-data/Sales-Data-Analysis.csv", usecols=["Quantity","Price"])
sales_data
----------------------
	Price	Quantity
0	3.49	573.07
1	2.95	745.76
2	4.99	200.40
3	12.99	569.67
4	9.95	201.01
...	...	...
```

垂直計算，所以會把Price這一列和Quantity這一列的所有值都相加
```
sales_data.sum(axis = 0) 
-------------------------
Price         1803.99
Quantity    116995.31
dtype: float64
```

水平計算，每一列代表Price + Quantity的值
```
sales_data.sum(axis = 1)
---------------------------
0      576.56
1      748.71
2      205.39
3      582.66
4      210.96
        ...  
249    205.39
250    767.42
251    291.36
252    633.86
253    680.92
Length: 254, dtype: float64
```

#### 處理時間

- 匯入時間模組

```
import datetime as dt
```

- date():只處理年/月/日
- time():只處理時/分/秒/微秒
- datetime(): date和time的結合，包含時區(tzinfo)
- timedelta():時間差

```
import datetime as dt
current_time = dt.datetime.now()
two_hours_later = current_time + dt.timedelta(hours=2)
print(f"現在加 2 小時: {two_hours_later}")

# 現在加 2 小時: 2025-08-06 16:20:09.147360
```
### groupby():相當於Excel的樞紐

- groupby是一個分組計劃，不是分組結果的展現。例如出現：<pandas.core.groupby.generic.DataFrameGroupBy object at 0x110f735c0>
- 核心三觀念：分(DataFrame拆成獨立的分組)、應(做四則運算)、結(呈現結過，形成一個新的DataFrame)
- 範例一
```
import pandas as pd

sales_data = pd.DataFrame({
    '團隊': ['A隊', 'B隊', 'A隊', 'B隊', 'C隊', 'A隊'],
    '銷售額': [100, 150, 120, 180, 90, 110],
    '年齡': [25, 30, 28, 35, 22, 26]
})

   團隊  銷售額  年齡
0  A隊  100  25
1  B隊  150  30
2  A隊  120  28
3  B隊  180  35
4  C隊   90  22
5  A隊  110  26

print(sales_data)
# 使用 groupby()，將相同團隊合併並算出分組後的年齡平均值
team_avg_sales = sales_data.groupby('團隊').mean()
print(team_avg_sales)

      銷售額   年齡
團隊                  
A隊  110.0  26.333333
B隊  165.0  32.500000
C隊   90.0  22.000000

```
- 範例二

```
import datetime as dt
import pandas as pd
sales_data = pd.read_csv(
    "/Users/tinafung8686/Desktop/python_sales-data/Sales-Data-Analysis.csv")
# 先查看壹下不重複值的狀況，方便我決定誰要當作groupby的項
# Product, City都很適合
sales_data.nunique()
//
Order ID          254
Date               53
Product             5
Price               7
Quantity           29
Purchase Type       3
Payment Method      3
Manager            14
City                5
dtype: int64
//

new_data = sales_data.groupby("Purchase Type")
print(new_data) # <pandas.core.groupby.generic.DataFrameGroupBy object at 0x12b0d04a0>

#查詢三種Purchase Type的第一項
new_data.size()
//
Purchase Type
Drive-thru      61
In-store        86
Online         107
dtype: int64
//
new_data.first() #查看每一個groupby的第一個結果, 同理查看最後一個結果.last()

```
<img src="/images/09.png" width="50%">

### 關於index

#### multiindex

- parse_dates["Date"]：主要在告訴pandas讀取檔案時將欄位"Date"視為日期資料處理
- date_format：指定"Date"欄位的格式
- index_col = ["col1", "col2"] ：複合index的精髓
- sort_index()：原本會根據index排序，但若是multiindex(index數>1)，則可以指定要排序哪一個index。sort_index(level = "Country")就是以Country排序，也可以寫sort_index(level = 2)

```
import pandas as pd
bigmac = pd.read_csv("bigmac.csv", parse_dates=["Date"], date_format="%Y-%m-%d", index_col=["Date", "Country"]).sort_index()
bigmac.set_index(keys = ["Date", "Country"])
```

#### get_level_values():取出所有index的值

#### set_names():取出所有index的值
```
# 將Date改為Time
bigmac.index.set_names(names="Time",level=0)
# 將Country改為Location
bigmac.index.set_names(names="Location",level=1)
# 透過List直接改寫index name
bigmac.index = bigmac.index.set_names(names=["Time","Location"])
```
#### sort)index():ascending = True/ False
```
import pandas as pd
bigmac = pd.read_csv("bigmac.csv", parse_dates=["Date"], date_format="%Y-%m-%d", index_col=["Date", "Country"]).sort_index()
bigmac.sort_index(ascending=True)
bigmac.sort_index(ascending=False)
bigmac.sort_index(ascending = [True, False]) #指定每個index的排序狀況，使用list並對照index
```


## 八、資料運算、比較

### 1.map()將同樣規則套用在某變數上面。概念為copy而非view

```
import pandas as pd
sales_data = pd.read_csv(
    "/Users/tinafung8686/Desktop/python_sales-data/Sales-Data-Analysis.csv")

#有哪些欄位
agg_product_data = sales_data.groupby(by = "Product").nunique()# 查看不重複清單的值
agg_product_data 

# 新增美味分數
flavor_score = {
          "Beverages":10,
           "Burgers":5,
           "Chicken Sandwiches":3,
           "Fries":6,
           "Sides & Other":2}

sales_data["flavor_score"] = sales_data['Product'].map(flavor_score)
print(sales_data) # 只印出前五筆，方便檢查
```

### 2.資料篩選
#### df.isin():檢查DataFrame或Series中每個元素是否包含在一個你指定的集合
```
# 假設創建一個銷售清單
import pandas as pd
data = {
    'Product': ['Beverages', 'Burgers', 'Fries', 'Beverages', 'Sides & Other'],
    'Quantity': [10, 5, 6, 8, 2],
    'Price': [25, 50, 30, 20, 15]
}

         Product  Quantity  Price
0      Beverages        10     25
1        Burgers         5     50
2          Fries         6     30
3      Beverages         8     20
4  Sides & Other         2     15

sales_data = pd.DataFrame(data)
print(sales_data)
```
***

#### 定義一個我感興趣的清單，並檢查這份清單是否在Product裡面可以找到->isin()

```
products_to_filter = ['Beverages', 'Fries']
is_in_list = sales_data['Product'].isin(products_to_filter)
print(is_in_list) #回傳一個boolean

0     True
1    False
2     True
3     True
4    False
Name: Product, dtype: bool

# 使用布林值進行篩選
filtered_sales = sales_data[is_in_list]
print(filtered_sales)

   Product  Quantity  Price
0  Beverages        10     25
2      Fries         6     30
3  Beverages         8     20
```

#### 根據情境篩選

- 找出string

```
import pandas as pd
sales_data = pd.read_csv(
    "/Users/tinafung8686/Desktop/python_sales-data/Sales-Data-Analysis.csv", parse_dates=["Date"], date_format = "%d-%m-%Y" )
sales_data

# 篩出商品為Fries的所有資料
sales_data["Product"] == "Fries" # 出現一列boolean
sales_data[sales_data["Product"] == "Fries" ]
```

- 找出datetime，發現datetime可以像是stirng一樣比大小

```
# 找出所有小於2022/11/15的資料，根據日期欄位由大排到小
sales_data[sales_data["Date"] <= "2022-11-15"].sort_values("Date", ascending=False)
```
- 但若是遇到時間格式為小時, 分, 秒，則需另外處理。dt.time()為24小時制
```
sales_data[sales_data["Time"] <= dt.time(12,0,0)].sort_values("Time")
```
#### 根據特定條件篩選

- 條件都要滿足：AND
```
import datetime as dt
import pandas as pd
sales_data = pd.read_csv(
    "/Users/tinafung8686/Desktop/python_sales-data/Sales-Data-Analysis.csv", parse_dates=["Date"], date_format = "%d-%m-%Y" )
product_is_fries = sales_data["Product"] == "Fries"
city_is_london = sales_data["City"] == "London"
sales_data[product_is_fries & city_is_london].head()
```
- 條件滿足一個即可：OR
- 滿足2個或第三個：AND + OR

**篩出產品為薯條且地區為倫敦者，或者日期> 12/25**

```
import datetime as dt
import pandas as pd
sales_data = pd.read_csv(
    "/Users/tinafung8686/Desktop/python_sales-data/Sales-Data-Analysis.csv", parse_dates=["Date"], date_format = "%d-%m-%Y" )
product_is_fries = sales_data["Product"] == "Fries"
city_is_london = sales_data["City"] == "London"
date_after_1225 = sales_data["Date"] > "2022-12-25"
sales_data[(product_is_fries & city_is_london) |date_after_1225 ].tail()
```


### 3.查詢數值區間

- df[”欄位名稱”].between(startpoint, endpoint)

#### 查詢ID 10452 訂單時間是否介於2022/7/1-2022/7/31

```
sales_data = pd.read_csv(
    "/Users/tinafung8686/Desktop/python_sales-data/Sales-Data-Analysis.csv")
# 查詢ID 10452 訂單時間是否介於2022/11/1-2022/11/31

# 原地覆蓋值。Date更改格式為datetime, 並改變年月日顯示規則
sales_data["Date"] = pd.to_datetime(sales_data["Date"], format=('%d-%m-%Y'))


id = 10452 #int為10452時會是True, string為"10452"時為False
start_time = pd.to_datetime('01-11-2022')
end_time = pd.to_datetime('30-11-2022')

# 用來篩選布林值
is_match = (sales_data['Order ID'] == id) & (sales_data['Date'].between(start_time, end_time))
print(is_match)

0       True
1      False
2      False
3      False
4      False
       ...  
249    False
250    False
251    False
252    False
253    False

# 根據布林值 Series 篩選 DataFrame中實際的欄位
query_result = sales_data[is_match]
print(query_result)

Order ID	Date	Product	Price	Quantity	Purchase Type	Payment Method	Manager	City
0	10452	2022-11-07	Fries	3.49	573.07	Online	Gift Card	Tom Jackson	London

```

### 4.查詢重複值 df.duplicated()

- df.duplicated()：所有重複值都會被記錄為"True"，不重複值為"False"

```
import pandas as pd
sales_data = pd.read_csv(
    "/Users/tinafung8686/Desktop/python_sales-data/Sales-Data-Analysis.csv")
sales_data

sales_data["Product"].duplicated()

```

0      False
1      False
2      False
3      False
4      False
       ...  
249     True
250     True
251     True
252     True
253     True
Name: Product, Length: 254, dtype: bool

```
# 印出所有重複的值，所以可以看到表格從index 5開始
sales_data[sales_data["Product"].duplicated()]
```
<img src="/images/04.png" width="50%">

- df.duplicated(keep = "first"):預設。首次出現的值會被記錄為True，重複值為False
- df.duplicated(keep = "last"):預設。尾末出現第一次的值會被記錄為True，重複值為False
- ~反轉布林值：篩出第一次出現的值
sales_data[sales_data["Product"].duplicated()]因為這邊會印出所有重複值，反轉換就會出現第一次的不重複值

```
sales_data[~sales_data["Product"].duplicated(keep="first")]

```
<img src="/images/05.png" width="50%">

### 5.去除重複值 df.drop_duplicated()

- drop_duplicated()是用來刪除整列一樣的重複列
- drop_duplicated(keep = "first")
- drop_duplicated(keep = "last")

```
import pandas as pd
df = pd.DataFrame({
    'ID': [1, 2, 2, 3, 3],
    'Product': ['A', 'B', 'B', 'C', 'C'],
    'Price': [100, 200, 200, 300, 350]
})
print(df)
unique_df = df.drop_duplicates()
print(unique_df)
```

```
原始 DataFrame：
   ID Product  Price
0   1       A    100
1   2       B    200
2   2       B    200  # 這筆資料與索引 1 完全相同
3   3       C    300
4   3       C    350
------------------------------
預設移除重複後：
   ID Product  Price
0   1       A    100
1   2       B    200
3   3       C    300
4   3       C    350
```

- 同時篩選多個條件

```
import pandas as pd
employees = pd.DataFrame({
    '姓名': ['張三', '李四', '王五', '趙六', '陳七'],
    'Senior Management': [True, False, False, True, False],
    'Team': ['工程', '行銷', '行銷', '工程', '行銷']
})
print(employees)

原始員工資料：
    姓名  Senior Management  Team
0   張三               True  工程
1   李四              False  行銷
2   王五              False  行銷
3   趙六               True  工程
4   陳七              False  行銷

```
情況一：只根據 'Senior Management' 篩選不重複
```
df1 = employees.drop_duplicates(subset=["Senior Management"])
print(df1)

    姓名  Senior Management  Team
0   張三               True  工程
1   李四              False  行銷
```
***

情況二：根據 'Senior Management' 和 'Team' 篩選不重複 (多考慮了"Team")

```
df2 = employees.drop_duplicates(subset=["Senior Management", "Team"])
print(df2)

    姓名  Senior Management  Team
0   張三               True  工程
1   李四              False  行銷

```

# 未整理重點

## 九、資料表結合 Merge DataFrame

### Our Datasets:餐廳銷售

```
import pandas as pd
food = pd.read_csv("/Users/tinafung8686/Desktop/python_sales-data/restaurant_foods.csv")
customers = pd.read_csv("/Users/tinafung8686/Desktop/python_sales-data/restaurant_customers.csv")
week1 = pd.read_csv("/Users/tinafung8686/Desktop/python_sales-data/restaurant_week_1_sales.csv")
week2 = pd.read_csv("/Users/tinafung8686/Desktop/python_sales-data/restaurant_week_2_sales.csv")
```
<img src="/images/11.png" width="50%">
<img src="/images/12.png" width="50%">
<img src="/images/13.png" width="50%">

### (1) 欄位名稱一樣時，直接做concat

- pd.concat([column1, column2])

得知若合併week1與week2會有250 rows
```
len(week1) #250
len(week2) #250
```
week1的index由0-249, week2的index也是0-249，所以下方截圖的index 249其實是week2的index

```
pd.concat([week1, week2])
```
<img src="/images/14.png" width="50%">

- pd.concat([column1, column2], ignore_index = xxxx)

```
pd.concat([week1, week2], ignore_index = False) #預設，保留index
pd.concat([week1, week2], ignore_index = True) #index繼續排序下去
```
<img src="/images/15.png" width="50%">

```
pd.concat([week1, week2], keys=["Week1", "Week2"]).sort_index()
```
<img src="/images/16.png" width="50%">

### (2)欄位名稱不同時做concat

```
df1 = pd.DataFrame([1,2,3], columns=["A"])
 
    A
0	1
1	2
2	3

df2 = pd.DataFrame([1,2,3], columns=["B"])

    B
0	1
1	2
2	3

pd.concat([df1, df2])
# 等於 pd.concat([df1, df2], axis="index")

	 A	 B
0	1.0	NaN
1	2.0	NaN
2	3.0	NaN
0	NaN	1.0
1	NaN	2.0
2	NaN	3.0

pd.concat([df1, df2], axis= "columns")

    A	B
0	1	1
1	2	2
2	3	3
 
```

### (3) merge

- 基本語法：pd.merge(left, right, on=None, how='inner')
    - left, right：想合併的2個DataFrame
    - on:要合並的共同欄位。如果欄位名稱不同，使用left_on/ right_on
    - how:如何連接
        - how = "left":
        
        它會保留 left DataFrame 中所有的資料，並根據 on 欄位去匹配 right DataFrame 的資料。如果 right DataFrame 中沒有對應的資料，同樣會用 NaN 填充。你可以把它想像成以左邊的表格為主，確保所有左邊的員工資料都會被保留。
        - how = "right":

        與 left 剛好相反，它會保留 right DataFrame 中所有的資料，並去匹配 left DataFrame 的資料。

        - how = "inner"

        這是最常用，也是預設的合併方式。它只保留兩個 DataFrame 中 on 欄位都有的資料。想像成只有同時出現在兩張表格中的員工，才會被保留下來。

        - how = "outer"

        它會保留兩個 DataFrame 中所有的資料。如果某筆資料只出現在其中一個 DataFrame，另一個 DataFrame 的欄位會用 NaN（不是一個數字，通常代表缺失值）來填充。這就像是把兩個 DataFrame 的所有員工都列出來，即使有些員工只有基本資訊沒有薪資，反之亦然。


#### A. left joins()

##### (1) joins時發現有共同欄位

- 查看week1和food，發現共同點是Food ID

```
week1.head()

	Customer ID	Food ID
0	537	         9
1	97	         4
2	658	         1
3	202	         2
4	155	         9

food.head()

	Food ID	Food Item	Price
0	1	   Sushi	   3.99
1	2	   Burrito	   9.99
2	3	   Taco    	   2.99
3	4	   Quesadilla  4.25
4	5	   Pizza	   2.49

```
- 現在我要把Food ID concat，以week1作為left table

```
week1.merge(food, how = "left", on = "Food ID")
```

<img src="/images/17.png" width="50%">

##### (2) joins時發現沒有共同欄位

- Customer ID和ID

```
week2.head()
---------
	Customer ID	Food ID
0	688	       10
1	813        7
2	495	       10
3	189	       5
4	267        3

customers.head()

--------------------
    ID	First Name	Last Name	Gender	Company	Occupation
0	1	Joseph	    Perkins	    Male	Dynazzy	Community Outreach Specialist
1	2	Jennifer	Alvarez	    Female	DabZ	Senior Quality Engineer
2	3	Roger	    Black	    Male	Tagfeed	Account Executive
3	4	Steven	    Evans	    Male	Fatz	Registered Nurse
4	5	Judy	    Morrison	Female	Demivee	Legal Assistant
```

- week2和customers表格做merge。方式是week2左邊黏著customers (how = "left")
- 沒有空同欄位不能用on，改用left on (左表格)和right on告訴panda連接欄位名稱
```
week2.merge(customers, how="left", left_on="Customer ID", right_on = "ID")
```
<img src="/images/18.png" width="50%">

- 發現Customer ID和ID重複，將ID刪除保留一項即可

```
week2.merge(customers, how="left", left_on="Customer ID", right_on = "ID").drop(columns = "ID")
```


#### B.right joins()

#### C.inner joins()

##### (1)找出連續2週都來用餐的顧客 (相同Customer ID)

- Customer ID 537在week1 買Food ID 9，在week2買Food ID 5

```
week1.merge(week2, how = "inner", on = "Customer ID").head()
-----------------------------------------
	Customer ID	Food ID_x	Food ID_y
0	   537	         9	     5
1	   155        	 9	     3
2	   503	         5	     8
3	   503	         5	     9
4	   155	         1	     3
```

- suffixes([])

```
week1.merge(week2, how = "inner", on = "Customer ID", suffixes=[" - Week1", " - Week2"]).head()
-----------------------------------------
	Customer ID	Food ID_Week1	Food ID_Week2
0	   537	         9	         5
1	   155        	 9	         3
2	   503	         5	         8
3	   503	         5	         9
4	   155	         1	         3
```
##### (2)找出同個顧客連續2週買同樣food ID

```
week1.merge(week2, how = "inner", on = ["Customer ID", "Food ID"]).sort_values("Customer ID")
---------------------------------
	Customer ID	Food ID
4	    21	    4 ->duplicate
6	    21	    4
3	    233	    3
0	    304	    3
1	    540	    3
7	    578	    5 ->duplicate
8	    578	    5
5	    922	    1 ->duplicate
2	    937	    10

```
檢查重複項

```
condition1  = week1["Customer ID"] == 21 #boolean
condition2 = week1["Food ID"] == 4 #boolean
week1[condition1 & condition2]
-------------------------------
	Customer ID	Food ID
101	    21	    4
212	    21	    4


condition1  = week2["Customer ID"] == 21 #boolean
condition2 = week2["Food ID"] == 4 #boolean
week2[condition1 & condition2]
-------------------------------
	Customer ID	Food ID
30	    21	    4

```

101 * 30 \
212 * 30\
->出現2次

#### D. full joins()

```
week1.merge(week2, how = "outer", on = "Customer ID", suffixes=["Week1"," - Week2"])
```

<img src="/images/19.png" width="50%">

- 查看合併狀況
```
week1.merge(week2, how = "outer", on = "Customer ID", suffixes=["Week1"," - Week2"], indicator=True)
```
<img src="/images/20.png" width="50%">

```
merge = week1.merge(week2, how = "outer", on = "Customer ID", suffixes=["Week1"," - Week2"], indicator=True)
merge["_merge"].value_counts()
```

```
_merge
right_only    197
left_only     195
both           62
Name: count, dtype: int64
```

- 把right_only和left_only的值取出

```
merge[merge["_merge"].isin(["left_only", "right_only"])]
```
<img src="/images/21.png" width="50%">


#### E. left_index()、right_index()

- 當左表column和右表的index合併

```
import pandas as pd
food = pd.read_csv(
    "/Users/tinafung8686/Desktop/python_sales-data/restaurant_foods.csv", index_col="Food ID")
customers = pd.read_csv(
    "/Users/tinafung8686/Desktop/python_sales-data/restaurant_customers.csv", index_col = "ID")
week1 = pd.read_csv(
    "/Users/tinafung8686/Desktop/python_sales-data/restaurant_week_1_sales.csv")
week2 = pd.read_csv(
    "/Users/tinafung8686/Desktop/python_sales-data/restaurant_week_2_sales.csv")

week1.head()

	Customer ID	Food ID
0	    537	9
1	    97	4
2	    658	1
3	    202	2
4	    155	9
-------------------------
customers.head()

week1.merge(customers, how = 'left', left_on="Customer ID", right_index=True) 
```

<img src="/images/22.png" width="50%">

- 現在，再將food表格合併

```

week1.merge(customers, how = 'left', left_on="Customer ID", right_index=True).merge(food, how = "left", left_on = "Food ID", right_index=True )
```

<img src="/images/23.png" width="50%">


#### F. the join method()

- week1的資訊和week_1_times是可以match的，因此將他們整合成一張表。
- 因為兩張表的index都是numerical numbers, 因此left/right index都是True
- 因為確認兩張表可以直接合併，使用join()會快許多

```
wee1.head()
-------------------
  Customer ID	Food ID
0	537	        9
1	97	        4
2	658	        1
3	202	        2
4	155	        9

week1_time.head()
-------------------
	Time of Day
0	14:54:59
1	20:55:17
2	01:16:22
3	16:17:26
4	19:26:11
----------------------

week1.merge(week1_time, how = "left", left_index=True, right_index=True)

# a shortcut method
week1.join(week1_time)

```

## 十、Dates and Times

### 1. dt.date()

```
import pandas as od
import datetime as dt

someday = dt.date(2025, 10, 30)
someday.year #2025
someday.month # 10
someday.day #30
```

### 2. dt.datetime()
```
import pandas as od
import datetime as dt
sometime = dt.datetime(2025, 10, 30, 1, 4, 30)
sometime.hour # 1
sometime.minute # 4
sometime.second # 30
```

### 3.TimeStamp()

- pd.Timestamp() 函式可以接受多種不同格式的輸入，並將它們都轉換成標準的 Timestamp 物件。
- 時、分、秒後面若沒有寫，預設都是00:00:00

```
pd.Timestamp(2025, 10, 23)
pd.Timestamp(dt.date(2025, 10, 23))
```

```
pd.Timestamp(2025, 10, 23, 23, 59, 59)
pd.Timestamp(dt.datetime(2025, 10, 23, 23, 59, 59))
```

- 智慧辨識不同的日期格式

```
pd.Timestamp("2025-01-02")
pd.Timestamp("2025/01/02")
pd.Timestamp("2025/01/02 10:23:40")
```

- pd.date_range()

#### freq = "D"：間距一天

```
pd.date_range(start = "2025-01-20", end ="2025-01-31" )
---------------
DatetimeIndex(['2025-01-20', '2025-01-21', '2025-01-22', '2025-01-23',
               '2025-01-24', '2025-01-25', '2025-01-26', '2025-01-27',
               '2025-01-28', '2025-01-29', '2025-01-30', '2025-01-31'],
              dtype='datetime64[ns]', freq='D')
```

#### freq = "2D"

```
pd.date_range(start = "2025-01-20", end ="2025-01-31", freq ="2D")
-------------
DatetimeIndex(['2025-01-20', '2025-01-22', '2025-01-24', '2025-01-26',
               '2025-01-28', '2025-01-30'],
              dtype='datetime64[ns]', freq='2D')
```

#### freq = "B": B for business days

```
pd.date_range(start = "2025-01-20", end ="2025-01-31", freq ="B")
------------
DatetimeIndex(['2025-01-20', '2025-01-21', '2025-01-22', '2025-01-23',
               '2025-01-24', '2025-01-27', '2025-01-28', '2025-01-29',
               '2025-01-30', '2025-01-31'],
              dtype='datetime64[ns]', freq='B')

```
#### freq = "W"：預設是列出所有Sunday，若想改則需以W-MON 這樣修改
```
pd.date_range(start = "2025-01-20", end ="2025-01-31", freq ="W-Fri")
------------
DatetimeIndex(['2025-01-24', '2025-01-31'], dtype='datetime64[ns]', freq='W-FRI')
```
#### freq = "H"：間距為小時

```
pd.date_range(start = "2025-01-20 00:00:00", end ="2025-01-20 12:00:00", freq ="H")
------------
DatetimeIndex(['2025-01-20 00:00:00', '2025-01-20 01:00:00',
               '2025-01-20 02:00:00', '2025-01-20 03:00:00',
               '2025-01-20 04:00:00', '2025-01-20 05:00:00',
               '2025-01-20 06:00:00', '2025-01-20 07:00:00',
               '2025-01-20 08:00:00', '2025-01-20 09:00:00',
               '2025-01-20 10:00:00', '2025-01-20 11:00:00',
               '2025-01-20 12:00:00'],
              dtype='datetime64[ns]', freq='h')

```

#### freq = "M"

- ME:end day
- MS:start day

```
pd.date_range(start = "2025-01-01", end ="2025-12-31", freq ="M")
--------------
DatetimeIndex(['2025-01-31', '2025-02-28', '2025-03-31', '2025-04-30',
               '2025-05-31', '2025-06-30', '2025-07-31', '2025-08-31',
               '2025-09-30', '2025-10-31', '2025-11-30', '2025-12-31'],
              dtype='datetime64[ns]', freq='ME')
```

```
pd.date_range(start = "2025-01-01", end ="2025-12-31", freq ="MS")
-------------
DatetimeIndex(['2025-01-01', '2025-02-01', '2025-03-01', '2025-04-01',
               '2025-05-01', '2025-06-01', '2025-07-01', '2025-08-01',
               '2025-09-01', '2025-10-01', '2025-11-01', '2025-12-01'],
              dtype='datetime64[ns]', freq='MS')
```

#### freq = "A" (annual)

```
pd.date_range(start = "2025-01-01", end ="2030-12-31", freq ="AS")
-------------
DatetimeIndex(['2025-01-01', '2026-01-01', '2027-01-01', '2028-01-01',
               '2029-01-01', '2030-01-01'],
              dtype='datetime64[ns]', freq='YS-JAN')
```
#### period
```
pd.date_range(start = "2025-01-20",freq = "D", periods=11)
-----------
DatetimeIndex(['2025-01-20', '2025-01-21', '2025-01-22', '2025-01-23',
               '2025-01-24', '2025-01-25', '2025-01-26', '2025-01-27',
               '2025-01-28', '2025-01-29', '2025-01-30'],
              dtype='datetime64[ns]', freq='D')
```

### 4. the dt attribute

```
selected_days = pd.Series(pd.date_range(start = "2025-01-01", end = "2025-5-30", freq="10D 12H"))
selected_days
-----------------
0    2025-01-01 00:00:00
1    2025-01-11 12:00:00
2    2025-01-22 00:00:00
3    2025-02-01 12:00:00
4    2025-02-12 00:00:00
5    2025-02-22 12:00:00
6    2025-03-05 00:00:00
7    2025-03-15 12:00:00
8    2025-03-26 00:00:00
9    2025-04-05 12:00:00
10   2025-04-16 00:00:00
11   2025-04-26 12:00:00
12   2025-05-07 00:00:00
13   2025-05-17 12:00:00
14   2025-05-28 00:00:00
dtype: datetime64[ns]

------------------------
# 求年、月、日、小時等等

selected_days.dt.year

0     2025
1     2025
2     2025
3     2025
4     2025
5     2025
6     2025
7     2025
8     2025
9     2025
10    2025
11    2025
12    2025
13    2025
14    2025
dtype: int32
-----------------------
selected_days.dt.month
selected_days.dt.hour
-----------------------
selected_days.dt.day_of_year # 一年之中第幾天
0       1
1      11
2      22
3      32
4      43
5      53
6      64
7      74
8      85
9      95
10    106
11    116
12    127
13    137
14    148
dtype: int32
----------------------
selected_days.dt.day_of_week #一年之中第幾週
----------------------
selected_days.dt.day_name()

0     Wednesday
1      Saturday
2     Wednesday
3      Saturday
4     Wednesday
5      Saturday
6     Wednesday
7      Saturday
8     Wednesday
9      Saturday
10    Wednesday
11     Saturday
12    Wednesday
13     Saturday
14    Wednesday
dtype: object
----------------------
selected_days.dt.is_month_end # boolean，是否為當月最後一天
---------------------
selected_days.dt.is_quarter_start
---------------------
0      True
1     False
2     False
3     False
4     False
5     False
6     False
7     False
8     False
9     False
10    False
11    False
12    False
13    False
14    False
dtype: bool
---------------------
selected_days[selected_days.dt.is_quarter_start]
--------------------
0   2025-01-01
dtype: datetime64[ns]

```
### 5. 指定DataFrame欄位

```
# 將日期設為index
stocks = pd.read_csv(
    "/Users/tinafung8686/Desktop/python vscode/pandas/Incomplete/ibm.csv", index_col="Date").sort_index()

stocks.iloc[300] # 第300行資料數據
stocks.loc["2020-10-30"] # label為2020/10/30數據

#以下結果相等
stocks.loc["2020-10-30": "2020-12-31"] # 取時間區間
stocks.loc[pd.Timestamp(2020,10,30):pd.Timestamp(2020,12,31)]
stocks.truncate("2020-10-30","2020-12-31")

# 特定日期取值
stocks.loc["2020-10-30", "Close"] 
----------------------
np.float64(99.8367)
----------------------
stocks.loc["2020-10-30", "High":"Close"] 
----------------------
# High     99.9730
# Low      96.3450
# Close    99.8367
# Name: 2020-10-30, dtype: float64
```

### 6. DateOffset (調整日期)

- 先將日期(type:str)轉為date type (parse = [xxx])
- 基礎：pd.DateOffset(單位=數量)
```
stocks = pd.read_csv(
    "/Users/tinafung8686/Desktop/python vscode/pandas/Incomplete/ibm.csv", parse_dates=["Date"], index_col="Date").sort_index()

# 針對每個日期，加減5天
stocks.index

DatetimeIndex(['1962-01-02', '1962-01-03', '1962-01-04', '1962-01-05',
               '1962-01-08', '1962-01-09', '1962-01-10', '1962-01-11',
               '1962-01-12', '1962-01-15',
               ...
               '2023-09-28', '2023-09-29', '2023-10-02', '2023-10-03',
               '2023-10-04', '2023-10-05', '2023-10-06', '2023-10-09',
               '2023-10-10', '2023-10-11'],
              dtype='datetime64[ns]', name='Date', length=15546, freq=None)

-------------------
stocks.index + pd.DateOffset(days=5)

['1962-01-07', '1962-01-08', '1962-01-09', '1962-01-10',
               '1962-01-13', '1962-01-14', '1962-01-15', '1962-01-16',
               '1962-01-17', '1962-01-20',
               ...
               '2023-10-03', '2023-10-04', '2023-10-07', '2023-10-08',
               '2023-10-09', '2023-10-10', '2023-10-11', '2023-10-14',
               '2023-10-15', '2023-10-16'],
              dtype='datetime64[ns]', name='Date', length=15546, freq=None)

--------------------------
stocks.index - pd.DateOffset(years=5)
stocks.index + pd.DateOffset(years=1, months=2, days = 3, hours = 9, minutes = 34, seconds = 17)
```

- find the IBM stock on every of my birthday(10/30)
```
my_birthday = pd.date_range(start="1992-10-30", end="2020-10-30", freq=pd.DateOffset(years=1))

-----------------
DatetimeIndex(['1992-10-30', '1993-10-30', '1994-10-30', '1995-10-30',
               '1996-10-30', '1997-10-30', '1998-10-30', '1999-10-30',
               '2000-10-30', '2001-10-30', '2002-10-30', '2003-10-30',
               '2004-10-30', '2005-10-30', '2006-10-30', '2007-10-30',
               '2008-10-30', '2009-10-30', '2010-10-30', '2011-10-30',
               '2012-10-30', '2013-10-30', '2014-10-30', '2015-10-30',
               '2016-10-30', '2017-10-30', '2018-10-30', '2019-10-30',
               '2020-10-30'],
              dtype='datetime64[ns]', freq='<DateOffset: years=1>')
```

- 取得生日期間的細項

```
stocks[stocks.index.isin(my_birthday)]
```
<img src="/images/24.png" width="50%">

### 7. Timedeltas (調整日期)

- TimeDeltas 字面上的意思就是「時間差」，它代表兩個時間點之間的固定時間長度，例如測量出「5 天」、「3 小時」或「10 分鐘」這樣的絕對時間間隔。
- 和前面提到的DataOffset很像，但是以下為核心差異：
    - Timedelta：代表固定的時間長度，不考慮日曆上的特殊規則（例如月末、閏年）。
    - DateOffset：代表日曆上的時間偏移量，會考慮日曆規則。

- 範例:大日期-小日期

```
pd.Timestamp("2023-10-31 21:40:39")  - pd.Timestamp("2023-10-10 12:49:02")
---
Timedelta('21 days 08:51:37')
```

- 範例：小日期-大日期得負數

```
pd.Timestamp("2023-10-10 12:49:02")  - pd.Timestamp("2023-10-31 21:40:39")
---
# Timedelta('-22 days +15:08:23')
```

- 自己創建TimeDelta

```
pd.Timedelta(days=3, hours=23, minutes=28, seconds=53)

# Timedelta('3 days 23:28:53')
-----
pd.Timedelta("10 hours 4 minutes 1 seconds")
# Timedelta('0 days 10:04:01')
```

- 範例

```
# 查找下單到運送日期之間所需時間。注意：parse_dates若後面不給date_format會出現error

ecommerce = pd.read_csv("/Users/tinafung8686/Desktop/python vscode/pandas/Incomplete/ecommerce.csv", index_col="ID", parse_dates=["order_date","delivery_date"], date_format="%m/%d/%y")
ecommerce.dtypes #datetime64[ns]

#取得時間差並創建+指定給欄位:delivery_time
ecommerce["delivery_time"] = ecommerce["delivery_date"] - ecommerce["order_date"]

#若所需運費時間變為2倍
ecommerce["double_delivery_time"] = ecommerce["delivery_date"] + ecommerce["delivery_time"]

```

## 十一、Input and Output

### 1. input外部檔案

```
import pandas as pd
import ssl
import certifi
from urllib.request import urlopen
from io import StringIO

def safe_read_csv(url: str, **kwargs) -> pd.DataFrame:
    """
    從 HTTPS 來源安全讀取 CSV，使用 certifi 的最新憑證避免 SSL 驗證失敗。
    
    :param url: CSV 來源 URL
    :param kwargs: 傳遞給 pandas.read_csv 的其他參數
    :return: pandas DataFrame
    """
    # 建立 SSL context，指定使用 certifi 憑證檔
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    
    # 先用 urllib 下載內容，再交給 pandas
    with urlopen(url, context=ssl_context) as response:
        csv_data = response.read().decode("utf-8")
    
    return pd.read_csv(StringIO(csv_data), **kwargs)

# ===== 測試 =====
url = "https://data.cityofnewyork.us/api/views/25th-nujf/rows.csv"
baby_names = safe_read_csv(url)
print(baby_names.head())

```

### 2. input Google Documents
#### share檔案
```
google_doc = "https://docs.google.com/spreadsheets/d/1YTcbe2UE7ju-zMYBJcNcB9zf3gzmHsDGHxkcYdwZTaw/edit?usp=sharing"
```

#### 確認檔案ID
```
ID = 1YTcbe2UE7ju-zMYBJcNcB9zf3gzmHsDGHxkcYdwZTaw
```

#### edit?usp=sharing 替換成 export?format=csv

```
google_doc = "https://docs.google.com/spreadsheets/d/1YTcbe2UE7ju-zMYBJcNcB9zf3gzmHsDGHxkcYdwZTaw/export?format=csv"
```

#### try

```
url = "https://docs.google.com/spreadsheets/d/1YTcbe2UE7ju-zMYBJcNcB9zf3gzmHsDGHxkcYdwZTaw/export?format=csv"
baby_names = safe_read_csv(url)
print(baby_names.head())
```

### 3.Import Excel File into Pandas

- 1個excel表格，1張分頁
```
import pandas as pd
single_data = pd.read_excel(
    "/Users/tinafung8686/Desktop/python vscode/pandas/Incomplete/Data - Single Worksheet.xlsx")

```
- 1張表格裡有多個分頁，預設只會讀取**第一個分頁**
```
multiple_data1 = pd.read_excel("/Users/tinafung8686/Desktop/python vscode/pandas/Incomplete/Data - Multiple Worksheets.xlsx", sheet_name="Data 1") # sheet_name = 0
---
multiple_data2 = pd.read_excel("/Users/tinafung8686/Desktop/python vscode/pandas/Incomplete/Data - Multiple Worksheets.xlsx", sheet_name="Data 2") # sheet_name = 1
```
- 1張表格裡同時匯入多張分頁
```
multiple_data12 = pd.read_excel("/Users/tinafung8686/Desktop/python vscode/pandas/Incomplete/Data - Multiple Worksheets.xlsx", sheet_name=["Data 1","Data 2"]) ## sheet_name = 0,1

```
- 1張表格裡讀取所有分頁->sheet_name = None
    - 在 pd.read_excel() 這個函式中，當你將 sheet_name 設為 None 時，Pandas 就會把這個行為解釋為：「使用者沒有指定任何特定的工作表，所以我的預設行為是處理所有工作表。」
```
multiple_data12 = pd.read_excel("/Users/tinafung8686/Desktop/python vscode/pandas/Incomplete/Data - Multiple Worksheets.xlsx", sheet_name=None) ## sheet_name = 全部。
```

## 十二、Visualization視覺化

### 下載

- 如果直接下載，系統會為找不到版本而提示 ``zsh: command not found: pip``
```
python3.12 -m pip install matplotlib
```

### pyplot模組

- 下載
- matplotlib 是一個龐大的函式庫，包含許多子模組，例如 pyplot、artist、cm 等等。如果你只匯入 matplotlib，你需要用 matplotlib.pyplot.plot() 這樣冗長的寫法才能呼叫繪圖函式。
- pyplot 模組幾乎是繪圖的首選

```
import pandas as pd
import matplotlib.pyplot as plt
# 整理資料，將日期string格式改為TimeStamp
ibm = pd.read_csv("/Users/tinafung8686/Desktop/python vscode/pandas/Incomplete/ibm.csv", parse_dates=["Date"],index_col="Date").sort_index()
ibm.head()
```
### 繪製圖

```
ibm.plot()
```
<img src="/images/25.png" width="50%">

### 指定x\y軸
```
ibm.plot(y="Close")
```
<img src="/images/26.png" width="50%">

### plt.style

#### 折線圖

- 叫出所有可以用的格式
```
plt.style.available
-----
['Solarize_Light2',
 '_classic_test_patch',
 '_mpl-gallery',
 '_mpl-gallery-nogrid',
 'bmh',
 'classic',
 'dark_background',
 'fast',
 'fivethirtyeight',
 'ggplot',
 'grayscale',
 'petroff10',
 'seaborn-v0_8',
 'seaborn-v0_8-bright',
 'seaborn-v0_8-colorblind',
 'seaborn-v0_8-dark',
 'seaborn-v0_8-dark-palette',
 'seaborn-v0_8-darkgrid',
 'seaborn-v0_8-deep',
 'seaborn-v0_8-muted',
 'seaborn-v0_8-notebook',
 'seaborn-v0_8-paper',
 'seaborn-v0_8-pastel',
 'seaborn-v0_8-poster',
 'seaborn-v0_8-talk',
 'seaborn-v0_8-ticks',
 'seaborn-v0_8-white',
 'seaborn-v0_8-whitegrid',
'tableau-colorblind10']
```

- 開始選擇格式。use()中間的個是可以根據上面style挑選變換

```
plt.style.use("seaborn-v0_8-colorblind")
ibm.plot(y="Close")
```
#### bar charts

- 原先的數據是散佈數據適合折線圖，現在要把它加總變成bar charts適合的數據

```
def rank_performance(stock_price):
    if stock_price <= 50:
        return "Poor"
    elif stock_price > 50 and stock_price <= 100:
        return "Average"
    else:
        return "Excellent"

ibm["Close"].apply(rank_performance)
-----------
Date
1962-01-02         Poor
1962-01-03         Poor
1962-01-04         Poor
1962-01-05         Poor
1962-01-08         Poor
                ...    
2023-10-05    Excellent
2023-10-06    Excellent
2023-10-09    Excellent
2023-10-10    Excellent
2023-10-11    Excellent
Name: Close, Length: 15546, dtype: object

```
- 分類完成，計算

```
ibm["Close"].apply(rank_performance).value_counts() 
----
Close
Poor         9423
Excellent    3085
Average      3038
Name: count, dtype: int64
```

```
ibm["Close"].apply(rank_performance).value_counts().plot(kind = "bar")
```
<img src="/images/27.png" width="50%">

```
ibm["Close"].apply(rank_performance).value_counts().plot(kind = "barh") #horizontal
```
<img src="/images/28.png" width="50%">

#### pie charts:算比例

- 計算多少比例的股價在平均之上，多少在平均之下

<img src="/images/21.png" width="50%">

```
import pandas as pd
import matplotlib.pyplot as plt
ibm = pd.read_csv("/Users/tinafung8686/Desktop/python vscode/pandas/Incomplete/ibm.csv", parse_dates=["Date"],index_col="Date").sort_index()

average_stock_price = ibm["Close"].mean()
def average_stock(stock_price):
    if stock_price <= average_stock_price:
        return "Below Average"
    else:
        return "Above Average"
    
plot_data = ibm["Close"].apply(average_stock).value_counts().plot(kind="pie", legend=True) #legend圖例
```
- 進階(調整字體、顏色、細節) (之後補)

## Options and Settings

- np
```
import pandas as pd
import numpy as np

# np隨便產出一個整數，介於0-100
np.random.randint(0,100)

# np隨便產出一個整數，介於0-100,欄位大小為20*30
np.random.randint(0,100,[20,30])

type(np.random.randint(0,100,[20,30])) 
#numpy.ndarray
```

### pd.options

- np指定為DataFrame
- 60*50，欄處在9...40，列則會全部顯示
- 61*50，欄處在9...40，列則會是4...56，這和pd.options設定有關

```
pd.DataFrame(np.random.randint(0,100,[60,50]))
pd.DataFrame(np.random.randint(0,100,[61,50]))

```
