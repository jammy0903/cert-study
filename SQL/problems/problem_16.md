# 문제 16: WHERE + 서브쿼리 (기초)

## 문제
개발 부서(dept_name='개발')의 모든 직원 이름을 출력하라.

컬럼: `name`

### 테이블
```
departments
| dept_id | dept_name |
|---------|-----------|
| 1 | 개발 |
| 2 | 영업 |

employees
| emp_id | name | dept_id | salary |
|--------|------|---------|--------|
| 1 | 김철수 | 1 | 5000 |
| 2 | 이영희 | 1 | 6000 |
| 3 | 박민수 | 2 | 4000 |
| 4 | 최수진 | 2 | 3000 |
```

## 기대 출력
| name |
|------|
| 김철수 |
| 이영희 |

---

## 사용자 답변
```sql
select name
from employees
where dept_id = (select dept_id from departments where dept_name ='개발')
```

## 분석
✅ **완벽함!**

### 잘한 점
1. **서브쿼리 구조 정확**
   - 안: `(SELECT dept_id FROM ...)` → 값 1 반환
   - 바깥: `WHERE dept_id = 1` → 직원 필터링

2. **괄호 정확** (서브쿼리는 필수!)

3. **비교 연산자** (`=`) 정확

## 정답 쿼리
```sql
SELECT name
FROM employees
WHERE dept_id = (SELECT dept_id FROM departments WHERE dept_name = '개발');
```

또는 JOIN 방식:
```sql
SELECT e.name
FROM employees e
JOIN departments d ON e.dept_id = d.dept_id
WHERE d.dept_name = '개발';
```

## 핵심 개념
- **서브쿼리 = SQL 안의 SQL**
- **WHERE 서브쿼리 = 조건으로 단일값 비교**
- **실행 순서: 서브쿼리 먼저 → 메인 쿼리에 결과 대입**

---

## 취약점 파악
✓ 서브쿼리 기본 구조 완벽
