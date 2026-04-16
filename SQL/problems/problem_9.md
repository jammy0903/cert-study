# 문제 9: RIGHT JOIN

## 문제
오른쪽 테이블(grades)의 모든 성적 기록을 기준으로, 해당 학생의 이름과 평균 성적을 출력하라.
컬럼: `name`, `avg_score`

### 테이블
```
students
| student_id | name |
|------------|------|
| 1 | 김철수 |
| 2 | 이영희 |
| 3 | 박민수 |

grades
| grade_id | student_id | score |
|----------|-----------|-------|
| 1 | 1 | 95 |
| 2 | 1 | 88 |
| 3 | 2 | 92 |
| 4 | 4 | 85 |
```

**주의:** 
- 학생 3(박민수)은 성적 기록 없음
- grades의 student_id 4는 students에 없음 (name = NULL)

## 기대 출력
| name | avg_score |
|------|-----------|
| 김철수 | 91.5 |
| 이영희 | 92 |
| NULL | 85 |

---

## 사용자 답변
```sql
from grades
right join students on students.student_id = grades.student_id
group by student_id, name
```

## 분석
❌ **틀림**

### 문제점
1. **RIGHT JOIN 방향 오류** (중요!)
   - `FROM grades RIGHT JOIN students` = 학생 모두를 기준
   - 문제는 "grades 모두를 기준" → LEFT JOIN 써야 함
   
2. **SELECT 누락**: 집계함수 없음
   - `SELECT s.name, AVG(g.score) AS avg_score` 필요

## 정답 쿼리
```sql
SELECT s.name, AVG(g.score) AS avg_score
FROM students s
RIGHT JOIN grades g ON s.student_id = g.student_id
GROUP BY g.student_id, s.name;
```

또는 LEFT로 (더 직관적):
```sql
SELECT s.name, AVG(g.score) AS avg_score
FROM grades g
LEFT JOIN students s ON g.student_id = s.student_id
GROUP BY g.student_id, s.name;
```

## 핵심 개념

### LEFT vs RIGHT JOIN
| | 왼쪽(FROM) | 오른쪽(JOIN) |
|--|-----------|-----------|
| LEFT JOIN | **모두** | 매칭된 것 |
| RIGHT JOIN | 매칭된 것 | **모두** |

**판단 방법:** "어느 테이블의 모든 기록이 필요한가?"
- grades 모두 필요 → `FROM grades LEFT JOIN students` 또는 `FROM students RIGHT JOIN grades`

---

## 취약점 파악
✗ LEFT vs RIGHT 방향 (아직 헷갈림)
✗ SELECT 누락 (기본기 재확인)
✓ ON 키워드 포함 (이제 잘함!)
✓ GROUP BY 구조 (이전 문제에서 배움)
