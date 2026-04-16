# 문제 7: LEFT JOIN + COALESCE 직접 풀어보기

## 문제
모든 상품의 상품명과 총 판매량을 출력하라. (판매가 없는 상품도 포함, 없으면 0으로 표시)
컬럼: `product_name`, `total_quantity`

### 테이블
```
products
| product_id | product_name |
|------------|--------------|
| 1 | 노트북 |
| 2 | 마우스 |
| 3 | 키보드 |
| 4 | 모니터 |

sales
| sale_id | product_id | quantity |
|---------|-----------|----------|
| 1 | 1 | 5 |
| 2 | 1 | 3 |
| 3 | 2 | 10 |
| 4 | 1 | 2 |
```

**주의:** 상품 3(키보드), 4(모니터)는 판매 기록 없음

## 기대 출력
| product_name | total_quantity |
|--------------|----------------|
| 노트북 | 10 |
| 마우스 | 10 |
| 키보드 | 0 |
| 모니터 | 0 |

---

## 사용자 답변
```sql
select product_name, count(quantity) as total_quantity
from product_name
left join sales on product.product_id = sales.product_id
group by product_name
```

## 분석
❌ **틀림**

### 문제점
1. **테이블명 오류**: `product_name`은 컬럼명, 테이블명은 `products`
2. **집계함수 오류**: `COUNT(quantity)` ❌ → `SUM(quantity)` ✅
   - COUNT는 행의 개수 세기 (틀린 결과)
   - SUM은 값을 합산 (올바른 결과)
3. **COALESCE 누락**: NULL(판매 없음)을 0으로 표시 못 함
4. **GROUP BY 불완전**: `GROUP BY p.product_id, p.product_name` 권장

## 정답 쿼리
```sql
SELECT p.product_name, COALESCE(SUM(s.quantity), 0) AS total_quantity
FROM products p
LEFT JOIN sales s ON p.product_id = s.product_id
GROUP BY p.product_id, p.product_name;
```

## 구조 분석
```
FROM products p                          ← 왼쪽 (모든 상품)
LEFT JOIN sales s                        ← 오른쪽 (판매 기록)
ON p.product_id = s.product_id           ← 연결 조건
GROUP BY p.product_id, p.product_name    ← 상품별 집계
COALESCE(SUM(s.quantity), 0)             ← NULL을 0으로 변환
```

## 핵심 개념
- **COUNT vs SUM**: COUNT는 행 개수, SUM은 값 합산
- **COALESCE**: NULL이면 기본값(0) 사용
- **LEFT JOIN + GROUP BY + COALESCE**: 매우 흔한 조합

---

## 취약점 파악
✗ COUNT vs SUM 구분 (자주 헷갈림)
✗ 테이블명 vs 컬럼명 구분
✓ LEFT JOIN 위치 (이제 맞음)
✓ COALESCE 개념 (이제 직접 사용함)
