# 문제 14: LEFT JOIN + COALESCE (직접 풀어보기)

## 문제
모든 매장의 매장명과 총 판매액을 출력하라. (판매가 없는 매장도 포함, 없으면 0으로 표시)

컬럼: `store_name`, `total_sales`

### 테이블
```
stores
| store_id | store_name |
|----------|-----------|
| 1 | 서울점 |
| 2 | 부산점 |
| 3 | 대구점 |
| 4 | 인천점 |

sales
| sale_id | store_id | amount |
|---------|----------|--------|
| 1 | 1 | 50000 |
| 2 | 1 | 30000 |
| 3 | 2 | 80000 |
| 4 | 1 | 20000 |
```

**주의:** 대구점(3), 인천점(4)은 판매 기록 없음

## 기대 출력
| store_name | total_sales |
|------------|------------|
| 서울점 | 100000 |
| 부산점 | 80000 |
| 대구점 | 0 |
| 인천점 | 0 |

---

## 사용자 답변
```sql
select store_name,coalesce(sum(amount),0) as total_sales
from stores
left join sales on stores.store_id = sales.store_id
```

## 분석
⚠️ **거의 완벽, 1가지 빠짐**

### 문제점
1. **GROUP BY 누락** (또 한 번!)
   - SUM을 쓰려면 GROUP BY 필수
   - `GROUP BY stores.store_id, store_name` 필요

## 정답 쿼리
```sql
SELECT store_name, COALESCE(SUM(amount), 0) AS total_sales
FROM stores
LEFT JOIN sales ON stores.store_id = sales.store_id
GROUP BY stores.store_id, store_name;
```

또는 별칭:
```sql
SELECT s.store_name, COALESCE(SUM(sa.amount), 0) AS total_sales
FROM stores s
LEFT JOIN sales sa ON s.store_id = sa.store_id
GROUP BY s.store_id, s.store_name;
```

## 핵심 패턴
```
FROM 왼쪽 테이블
LEFT JOIN 오른쪽 테이블 ON 조건
GROUP BY 왼쪽.id, 왼쪽.컬럼
COALESCE(SUM(오른쪽.컬럼), 0)
```

---

## 취약점 파악
✗ GROUP BY 자꾸 빼먹음 (3회 반복! 🔴 매우 높음)
✓ LEFT JOIN ON 완벽
✓ COALESCE 완벽
✓ SUM 완벽
