# 문제 19: 기초 UNION

## 문제
개발팀과 영업팀의 모든 직원명을 출력하라. (중복 제거)

컬럼: `name`

### 테이블
```
dev_team
| name |
|------|
| 김철수 |
| 이영희 |
| 박민수 |

sales_team
| name |
|------|
| 최수진 |
| 정다은 |
| 이영희 |
```

**주의:** 이영희는 두 테이블에 모두 있음

## 기대 출력
| name |
|------|
| 김철수 |
| 이영희 |
| 박민수 |
| 최수진 |
| 정다은 |

---

## 사용자 답변
```sql
select name
from dev_team union select name from sales_team
```

## 분석
✅ **완벽함!**

### 잘한 점
1. **UNION 구조 정확**
2. **두 SELECT 모두 같은 컬럼 수** (name)
3. **중복 자동 제거**

## 정답 쿼리
```sql
SELECT name FROM dev_team
UNION
SELECT name FROM sales_team;
```

또는 (같은 결과):
```sql
SELECT name FROM dev_team
UNION ALL
SELECT name FROM sales_team;
-- 결과: 6개 행 (이영희가 2개)
```

## 핵심 개념
- **UNION = 두 SELECT 결과 합치기**
- **UNION = 자동으로 중복 제거**
- **UNION ALL = 중복 포함**

---

## 취약점 파악
✓ UNION 구조 완벽
