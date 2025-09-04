# Leetcode Practice - Easy

## 511. Game Play Analysis I

- 找出每個玩家第一次登入的id, first_login

| player_id | device_id | event_date | games_played |
|-----------|-----------|------------|--------------|
| 1         | 2         | 2016-03-01 | 5            |
| 1         | 2         | 2016-05-02 | 6            |
| 2         | 3         | 2017-06-25 | 1            |
| 3         | 1         | 2016-03-02 | 0            |
| 3         | 4         | 2018-07-03 | 5            |
Output: 

| player_id | first_login |
|-----------|-------------|
| 1         | 2016-03-01  |
| 2         | 2017-06-25  |
| 3         | 2016-03-02  |


#### 寫法一：直接用min去找

```sql
select player_id,
       min(event_date) as first_login
from Activity
group by player_id
order by player_id ASC;
```

#### 寫法二：window function

- 先針對有rank的結果寫一個CTE (common table expression)
- 接著操作CTE取出rank = 1的player_id
- RANK()：排序方式為 1,1,3,3,3,3,7

```sql
WITH CTE AS (
SELECT
    player_id,
    event_date AS first_login,
    RANK() OVER (PARTITION BY player_id ORDER BY event_date ASC) AS rank_of_day
FROM
    Activity)
 SELECT player_id,
        first_login
 FROM CTE
 WHERE rank_of_day = 1;
 ```

#### 寫法三：FIRST_VALUE

- 透過first_value找出第一個值，ASC排序下第一個值就是最小登入日期
- 因為window function 下player_id有重複值，因此補上distinct player_id

```sql
SELECT DISTINCT player_id,
       FIRST_VALUE(event_date) OVER (PARTITION BY player_id ORDER BY event_date) AS first_login
 FROM Activity;
```

## 586. Customer Placing the Largest Number of Orders

- 找出最大的order number次數，然後找出這位的customer_id
- 如果最大次數重複，則印出所有customer_id


#### 解法一：

- 思路：創建一個CTE，呈現customer_id, 對應的order count, max_order count
- 若order count = max_order count時，就可以回推customer_id
- 發現網路上一些order by 搭配limit的寫法，當customer_id有1個以上時會error，所以最佳做法應該是透過window_function rank或子查詢

```sql
WITH CTE AS (
SELECT customer_number,
       count(order_number) AS order_count,
       max(count(order_number)) over() AS max_order_count
FROM orders
GROUP BY customer_number)

SELECT customer_number 
FROM CTE
WHERE order_count = max_order_count;
```

#### 解法二：

```sql
WITH CTE AS (
    SELECT customer_number,
           RANK() OVER (ORDER BY COUNT(*) DESC) AS rnk
    FROM Orders
    GROUP BY customer_number
)
SELECT customer_number
FROM CTE
WHERE rnk = 1;

```