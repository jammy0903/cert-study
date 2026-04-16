# 문제 5: LEFT JOIN

## 문제
모든 고객의 이름과 총 주문 금액을 출력하라. (주문이 없는 고객도 포함, 주문이 없으면 0)
컬럼: `name`, `total_amount`

### 테이블
```
customers
| customer_id | name |
|-------------|------|
| 101 | 김철수 |
| 102 | 이영희 |
| 103 | 박민수 |
| 104 | 최수진 |

orders
| order_id | customer_id | amount |
|----------|-------------|--------|
| 1 | 101 | 5000 |
| 2 | 101 | 3000 |
| 3 | 102 | 8000 |
| 4 | 101 | 2000 |
| 5 | 103 | 1000 |
```

**주의:** 고객 104(최수진)는 주문 없음

## 기대 출력
| name | total_amount |
|------|--------------|
| 김철수 | 10000 |
| 이영희 | 8000 |
| 박민수 | 1000 |
| 최수진 | 0 |

---

## 사용자 답변
```sql
select name,sum(amount) as 총 주문금액
from join customers, orders on custo...
(불완전함)
```

## 분석
❌ **틀림 + 미완성**

### 문제점
1. JOIN 문법 오류 (문제 4와 유사)
2. LEFT JOIN 미사용 → 주문 없는 고객 못 가져옴
3. COALESCE 미사용 → NULL을 0으로 표시 못 함
4. GROUP BY 누락 가능

## 정답 쿼리
```sql
SELECT c.name, COALESCE(SUM(o.amount), 0) AS total_amount
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name;
```

## 핵심 개념

### LEFT JOIN vs INNER JOIN
| | 왼쪽 테이블 | 오른쪽 테이블 |
|--|-----------|-----------|
| INNER JOIN | 매칭된 행만 | 매칭된 행만 |
| LEFT JOIN | **모든 행** | 매칭된 행만 |

→ 최수진(104)은 orders에 없지만 LEFT JOIN이면 나옴

### COALESCE 함수
```sql
COALESCE(값1, 값2)
= 값1이 NULL이면 값2 사용, 아니면 값1 사용
```

최수진의 경우:
- SUM(o.amount) = NULL (주문 없음)
- COALESCE(NULL, 0) = 0

---

## 취약점 파악
✗ LEFT JOIN 개념 (처음 배움)
✗ COALESCE 함수 (처음 배움)
✓ GROUP BY 이해 (반복으로 숙달됨)
✓ 테이블 별칭 (문제 4에서 습득)
