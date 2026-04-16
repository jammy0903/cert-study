# 취약점 & 강점 추적

## 완료된 개념
- ✅ HAVING vs WHERE 구분 (문제 1,2,3에서 확인)
- ✅ 기본 집계함수: SUM, AVG, COUNT, MAX, MIN 이해
- ✅ GROUP BY 다중 컬럼 (문제 3에서 습득)

## 현재 취약점
- ❌ JOIN 기본 문법 (문제 4에서 발견)
  - `FROM 테이블1 JOIN 테이블2 ON 조건` 형태 아직 미숙
  - ON 절에 `=` 연산자 필수 인식 부족
  - 테이블 별칭 활용 미흡
  
- ❌ 집계함수 선택 실수 (문제 2에서 발견, 아직 개선 필요)
  - 의미 없는 함수 사용 (예: SUM(문자형))

## 다음 단원
- [ ] JOIN 심화 (LEFT, RIGHT, FULL, INNER)
- [ ] 서브쿼리
- [ ] UNION / INTERSECT / EXCEPT
- [ ] 윈도우 함수
