# 문제 21: ORDER BY (정렬)

## 문제
직원들을 급여로 내림차순 정렬하여 이름과 급여를 출력하라.

컬럼: `name`, `salary`

### 테이블
```
employees
| emp_id | name | dept | salary |
|--------|------|------|--------|
| 1 | 김철수 | 개발 | 5000 |
| 2 | 이영희 | 개발 | 6000 |
| 3 | 박민수 | 영업 | 4000 |
| 4 | 최수진 | 영업 | 3000 |
| 5 | 정다은 | 인사 | 2500 |
```

## 기대 출력
| name | salary |
|------|--------|
| 이영희 | 6000 |
| 김철수 | 5000 |
| 박민수 | 4000 |
| 최수진 | 3000 |
| 정다은 | 2500 |

---

## 사용자 답변
```sql
select name , salary
from employees 
where salary desc
```

## 분석
❌ **틀림**

### 문제점
1. **ORDER BY 누락**: WHERE에 DESC를 잘못 사용
   - WHERE는 조건 필터링용 (행 거르기)
   - DESC는 ORDER BY와 함께만 사용
   
## 정답 쿼리
```sql
SELECT name, salary
FROM employees
ORDER BY salary DESC;
```

## 핵심 개념
- **WHERE**: 조건으로 행 거르기
- **ORDER BY**: 정렬 (ASC 오름차순 / DESC 내림차순)
- **ORDER BY는 SELECT 끝 부분에 위치**

### 순서
```
SELECT ... → FROM ... → WHERE ... → ORDER BY ...
```

---

## 취약점 파악
✗ WHERE vs ORDER BY 혼동
✓ SELECT 구조 이해 (다른 문제에서 배움)
