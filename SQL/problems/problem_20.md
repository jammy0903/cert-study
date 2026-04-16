# 문제 20: UNION + WHERE 조합

## 문제
2024년과 2025년의 상품 중 가격이 100 이상인 상품들을 출력하라. (중복 제거)

컬럼: `name`, `price`

### 테이블
```
products_2024
| product_id | name | price |
|------------|------|-------|
| 1 | 노트북 | 1500 |
| 2 | 마우스 | 50 |
| 3 | 키보드 | 120 |

products_2025
| product_id | name | price |
|------------|------|-------|
| 1 | 모니터 | 300 |
| 2 | 마우스 | 50 |
| 3 | 헤드폰 | 200 |
```

## 기대 출력
| name | price |
|------|-------|
| 노트북 | 1500 |
| 키보드 | 120 |
| 모니터 | 300 |
| 헤드폰 | 200 |

---

## 사용자 답변
```sql
selecet name
from product_2024
where price >= 100
union
select name 
from product_2025
where price >=100
```

## 분석
❌ **4가지 실수**

### 문제점
1. **오타**: `selecet` → `select`
2. **테이블명 오타**: `product_2024` → `products_2024`
3. **SELECT 컬럼 빠짐**: `name` 만 선택 → `name, price` 모두 필요
4. **두 번째도 마찬가지**: `product_2025` → `products_2025`

## 정답 쿼리
```sql
SELECT name, price FROM products_2024 WHERE price >= 100
UNION
SELECT name, price FROM products_2025 WHERE price >= 100;
```

## 핵심: UNION의 규칙
```
UNION은 두 SELECT의 컬럼 개수와 순서가 같아야 함!

❌ SELECT name, price ... UNION SELECT name ...
✅ SELECT name, price ... UNION SELECT name, price ...
```

---

## 취약점 파악
✗ 오타 (selecet)
✗ 테이블명 정확도
✗ SELECT 컬럼 빠짐 (기대 출력과 맞춰야 함)
✓ WHERE + UNION 구조 이해
