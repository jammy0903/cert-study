# 문제 6: LEFT JOIN 직접 풀어보기

## 문제
모든 부서의 부서명과 직원 수를 출력하라. (직원이 없는 부서도 포함)
컬럼: `dept_name`, `emp_count`

### 테이블
```
departments
| dept_id | dept_name |
|---------|-----------|
| 1 | 개발 |
| 2 | 영업 |
| 3 | 인사 |
| 4 | 재무 |

employees
| emp_id | name | dept_id | salary |
|--------|------|---------|--------|
| 101 | 김철수 | 1 | 5000 |
| 102 | 이영희 | 1 | 6000 |
| 103 | 박민수 | 2 | 4000 |
| 104 | 최수진 | NULL | 3500 |
```

**주의:** 
- 부서 3(인사), 4(재무)는 직원 없음
- 직원 104는 부서 미배치 (dept_id = NULL)

## 기대 출력
| dept_name | emp_count |
|-----------|-----------|
| 개발 | 2 |
| 영업 | 1 |
| 인사 | 0 |
| 재무 | 0 |

---

## 사용자 답변
```sql
select dept_name, count(emp_id) as emp_count
from departments
where left join employees on departments.dept_id = employees.dept_id
```

## 분석
❌ **틀림**

### 문제점
1. **LEFT JOIN 위치 오류**: `WHERE` 자리에 LEFT JOIN 삽입
   - `WHERE`는 조건 필터링용 (행 거르기)
   - `LEFT JOIN`은 테이블 연결용 (FROM 다음)

2. **GROUP BY 누락**: COUNT 사용하는데 GROUP BY 없음
   - 부서별로 묶어야 각 부서의 직원 수가 나옴

## 정답 쿼리
```sql
SELECT d.dept_name, COUNT(e.emp_id) AS emp_count
FROM departments d
LEFT JOIN employees e ON d.dept_id = e.dept_id
GROUP BY d.dept_id, d.dept_name;
```

## 구조 분석
```
FROM departments d              ← 왼쪽 (모든 부서)
LEFT JOIN employees e           ← 오른쪽 (직원이 있으면 붙임)
ON d.dept_id = e.dept_id        ← 연결 조건
GROUP BY d.dept_id, d.dept_name ← 부서별 집계
COUNT(e.emp_id)                 ← 각 부서 직원 수 (없으면 0)
```

## 핵심 개념
- **LEFT JOIN = 왼쪽 테이블 전부 + 오른쪽 매칭 데이터**
- **FROM에서 LEFT JOIN 사용** (WHERE가 아님!)
- **GROUP BY 후 COUNT** = 각 그룹별 개수

---

## 취약점 파악
✗ LEFT JOIN 위치 (WHERE vs FROM)
✗ JOIN 후 GROUP BY 조합 (반복 필요)
✓ LEFT JOIN 개념 이해 (피드백 완료)
