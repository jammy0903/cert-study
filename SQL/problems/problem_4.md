# 문제 4: JOIN + GROUP BY 조합

## 문제
각 고객의 이름과 총 주문 금액을 출력하라. (주문이 있는 고객만)
컬럼: `name`, `total_amount`

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
| 6 | 102 | 4000 |
```

## 기대 출력
| name | total_amount |
|------|--------------|
| 김철수 | 10000 |
| 이영희 | 12000 |
| 박민수 | 1000 |

---

## 사용자 답변
```sql
select name,sum(amount) as 총 주문금액
from join customers, orders on customers.customers_id and orders.customers_id
```

## 분석
❌ **틀림**

### 문제점
1. **JOIN 문법 오류**: `FROM join` 형태는 없음
   - 올바른 형태: `FROM 테이블1 JOIN 테이블2 ON ...`

2. **ON 절에 비교 연산자(=) 누락**
   - `ON customers.customers_id AND orders.customers_id` ← 뭘 비교하는 건지 불명
   - `ON customers.customer_id = orders.customer_id` 필요

3. **컬럼명 오타**: `customers_id` → `customer_id`

4. **GROUP BY 누락**: 고객별로 집계하려면 GROUP BY 필수

## 정답 쿼리
```sql
SELECT c.name, SUM(o.amount) AS total_amount
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name;
```

또는 (테이블 이름 풀 형태):
```sql
SELECT customers.name, SUM(orders.amount) AS total_amount
FROM customers
JOIN orders ON customers.customer_id = orders.customer_id
GROUP BY customers.customer_id, customers.name;
```

## 핵심 개념
- **JOIN 구조**: `FROM 테이블1 JOIN 테이블2 ON 조인조건`
- **ON 절**: 두 테이블의 키를 `=`로 비교
- **테이블 별칭**: `FROM customers c` = c로 customers 지칭 가능
- **조인 후 GROUP BY**: 연결된 테이블에서 특정 컬럼으로 묶음

---

## 취약점 파악
✗ JOIN 문법 (FROM 위치, ON에 = 연산자)
✗ 테이블 별칭 (선택사항이지만 가독성 향상)
✓ GROUP BY 이해 (이전 문제에서 습득)
✓ 집계함수 이해 (이전 문제에서 습득)
