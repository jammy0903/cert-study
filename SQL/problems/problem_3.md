# 문제 3: 지역별 상품 판매 집계

## 문제
같은 지역에서 같은 상품이 2번 이상 팔린 경우를 출력하라.
컬럼: `region`, `product`, `count`

### 테이블
```
sales
| sale_id | product | region | amount |
|---------|---------|--------|--------|
| 1 | 노트북 | 서울 | 1500 |
| 2 | 마우스 | 서울 | 50 |
| 3 | 노트북 | 서울 | 1500 |
| 4 | 키보드 | 서울 | 120 |
| 5 | 마우스 | 부산 | 50 |
| 6 | 마우스 | 부산 | 50 |
| 7 | 노트북 | 대구 | 1500 |
```

## 기대 출력
| region | product | count |
|--------|---------|-------|
| 서울 | 노트북 | 2 |
| 부산 | 마우스 | 2 |

---

## 사용자 답변
```sql
select  region,product,count
from sales
group by region
group by product
having count(*)>=2
```

## 분석
❌ **틀림**

### 문제점
1. **GROUP BY 문법 오류**: GROUP BY를 두 번 쓰면 안 됨
   - 여러 컬럼으로 그룹화할 땐 쉼표로 구분: `GROUP BY region, product`

2. **SELECT에서 집계함수 누락**: `count`라고 쓰면 컬럼이지 집계가 아님
   - `COUNT(*) AS count`로 명시해야 함

## 정답 쿼리
```sql
SELECT region, product, COUNT(*) AS count
FROM sales
GROUP BY region, product
HAVING COUNT(*) >= 2;
```

## 핵심 개념
- **GROUP BY 다중 컬럼**: `GROUP BY col1, col2` = col1과 col2의 조합으로 묶음
- 다중 GROUP BY는 모든 컬럼을 한 번에 쓸 것

---

## 취약점 파악
✗ GROUP BY 여러 컬럼 문법 (쉼표 구분)
✓ HAVING vs WHERE 구분 (이전 문제에서 완료)
✓ 집계함수 개념 (이전 문제에서 일부 완료)
