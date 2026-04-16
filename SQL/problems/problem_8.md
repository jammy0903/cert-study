# 문제 8: COUNT vs SUM 동시 사용

## 문제
각 고객의 이름, 주문 건수, 총 주문 금액을 출력하라.
컬럼: `name`, `order_count`, `total_amount`

### 테이블
```
customers
| customer_id | name |
|-------------|------|
| 101 | 김철수 |
| 102 | 이영희 |
| 103 | 박민수 |

orders
| order_id | customer_id | amount |
|----------|-------------|--------|
| 1 | 101 | 5000 |
| 2 | 101 | 3000 |
| 3 | 102 | 8000 |
| 4 | 101 | 2000 |
| 5 | 103 | 1000 |
```

## 기대 출력
| name | order_count | total_amount |
|------|-------------|--------------|
| 김철수 | 3 | 10000 |
| 이영희 | 1 | 8000 |
| 박민수 | 1 | 1000 |

---

## 사용자 답변
```sql
select name,count(order_id) as order_count,sum(amount) as total_amount
from customers 
left join orders customers.customer_id = orders.customer_id
group by customer_id
```

## 분석
❌ **틀림**

### 문제점
1. **LEFT JOIN에 ON 키워드 누락** (반복 실수)
   - `LEFT JOIN orders customers.customer_id = ...` ❌
   - `LEFT JOIN orders ON customers.customer_id = ...` ✅

2. **GROUP BY 불완전**
   - SELECT에 `name`이 있는데 GROUP BY에 없음
   - `GROUP BY customer_id, name` 필요

## 정답 쿼리
```sql
SELECT c.name, COUNT(o.order_id) AS order_count, SUM(o.amount) AS total_amount
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name;
```

또는 (별칭 없이):
```sql
SELECT name, COUNT(order_id) AS order_count, SUM(amount) AS total_amount
FROM customers
LEFT JOIN orders ON customers.customer_id = orders.customer_id
GROUP BY customers.customer_id, name;
```

## 핵심 개념
- **SELECT에 여러 집계함수 동시 사용 가능**
- **COUNT(컬럼) vs SUM(컬럼) 용도 명확히 구분**
  - COUNT: 행의 개수
  - SUM: 값의 합산
- **LEFT JOIN 문법: ON 키워드 필수!**
- **GROUP BY: SELECT의 모든 non-aggregated 컬럼 포함**

---

## 취약점 파악
✗ LEFT JOIN에서 ON 누락 (자주 반복되는 실수 🔴)
✗ GROUP BY 불완전 (컬럼 빼먹음)
✓ COUNT vs SUM 올바른 사용
✓ 여러 집계함수 동시 사용 이해
