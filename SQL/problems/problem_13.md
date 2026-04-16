# 문제 13: LEFT JOIN + GROUP BY + COUNT 조합

## 문제
모든 카테고리의 카테고리명과 상품 개수를 출력하라. (상품이 없는 카테고리도 포함, 없으면 0)

컬럼: `category_name`, `product_count`

### 테이블
```
categories
| category_id | category_name |
|-------------|---------------|
| 1 | 의류 |
| 2 | 신발 |
| 3 | 악세서리 |
| 4 | 가방 |

products
| product_id | name | category_id |
|------------|------|-------------|
| 1 | 티셔츠 | 1 |
| 2 | 청바지 | 1 |
| 3 | 운동화 | 2 |
| 4 | 목걸이 | 3 |
| 5 | 귀걸이 | 3 |
```

**주의:** 카테고리 4(가방)에는 상품 없음

## 기대 출력
| category_name | product_count |
|---------------|---------------|
| 의류 | 2 |
| 신발 | 1 |
| 악세서리 | 2 |
| 가방 | 0 |

---

## 사용자 답변
```sql
select category_name,colesce(count(category_id),0)as product_count
from categories
left join products on categories.category_id = products.category_id
group by category_id
```

## 분석
⚠️ **거의 맞음, 3가지 수정 필요**

### 문제점
1. **COUNT 대상 오류** (매우 중요!)
   - `COUNT(category_id)` ❌ → `COUNT(p.product_id)` ✅
   - 왜? LEFT JOIN 후 LEFT의 컬럼은 항상 있음, RIGHT의 컬럼은 NULL일 수 있음
   - 상품이 없는 카테고리는 product_id가 NULL → COUNT는 0

2. **GROUP BY 불완전**
   - `GROUP BY category_id` ❌
   - `GROUP BY category_id, category_name` ✅

3. **COALESCE 오타**
   - `colesce` ❌
   - `COALESCE` ✅
   - 참고: COUNT(p.product_id)는 이미 NULL을 0으로 처리하므로 COALESCE는 선택사항

## 정답 쿼리
```sql
SELECT c.category_name, COUNT(p.product_id) AS product_count
FROM categories c
LEFT JOIN products p ON c.category_id = p.category_id
GROUP BY c.category_id, c.category_name;
```

## 핵심 개념

### LEFT JOIN에서 COUNT 선택
```
LEFT 테이블 컬럼: 항상 값 있음 → COUNT는 1 이상
RIGHT 테이블 컬럼: NULL 가능 → COUNT는 0 가능 (상품 없을 때)
```

가방 카테고리 예:
- COUNT(c.category_id) = 1 ❌ (category_id가 있으므로)
- COUNT(p.product_id) = 0 ✅ (product_id가 NULL이므로)

---

## 취약점 파악
✗ LEFT JOIN에서 COUNT 대상 선택 (오른쪽 테이블 우선)
✓ LEFT JOIN ON 키워드 완벽
✓ GROUP BY 구조 (이제 습득됨)
✓ COALESCE 개념 (선택사항임 이해)
