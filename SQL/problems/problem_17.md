# 문제 17: WHERE + IN + 서브쿼리

## 문제
직원이 2명 이상인 부서에 속한 모든 직원의 이름을 출력하라.

컬럼: `name`

### 테이블
```
departments
| dept_id | dept_name |
|---------|-----------|
| 1 | 개발 |
| 2 | 영업 |
| 3 | 인사 |

employees
| emp_id | name | dept_id | salary |
|--------|------|---------|--------|
| 1 | 김철수 | 1 | 5000 |
| 2 | 이영희 | 1 | 6000 |
| 3 | 박민수 | 2 | 4000 |
| 4 | 최수진 | 2 | 3000 |
| 5 | 정다은 | 3 | 2500 |
```

## 기대 출력
| name |
|------|
| 김철수 |
| 이영희 |
| 박민수 |
| 최수진 |

---

## 사용자 답변
```sql
select name 
from employees
where dept_id in (
  select dept_id
  from employees
  group by dept_id
  having count(*)>=2
);
```

## 분석
✅ **완벽함!**

### 잘한 점
1. **IN 연산자 정확**
   - 여러 값(1, 2)과 비교

2. **서브쿼리 구조 정확**
   - GROUP BY + HAVING으로 조건 맞음
   - COUNT(*) >= 2 정확

3. **괄호 정확**

## 정답 쿼리
```sql
SELECT name 
FROM employees
WHERE dept_id IN (
  SELECT dept_id
  FROM employees
  GROUP BY dept_id
  HAVING COUNT(*) >= 2
);
```

또는 JOIN 방식:
```sql
SELECT DISTINCT e.name
FROM employees e
JOIN (
  SELECT dept_id FROM employees 
  GROUP BY dept_id 
  HAVING COUNT(*) >= 2
) AS valid_depts ON e.dept_id = valid_depts.dept_id;
```

## 핵심 개념
- **IN = 여러 값 중 하나?**
- **IN (서브쿼리) = 서브쿼리 결과와 비교**
- **서브쿼리 실행 순서: 먼저 내부 → 외부로 대입**

## 실행 흐름
```
서브쿼리: SELECT dept_id FROM employees GROUP BY dept_id HAVING COUNT(*) >= 2
→ 결과: (1, 2)

메인: WHERE dept_id IN (1, 2)
→ 개발, 영업 부서 직원만 출력
```

---

## 취약점 파악
✓ IN 연산자 완벽
✓ 서브쿼리 + GROUP BY + HAVING 조합 완벽
