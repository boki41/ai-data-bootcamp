# 옷장패션 데이터 — 결측치/이상치 정제 리포트

## 1. 데이터 개요
- 행/열: (1,500행, 8열)
- 주요 컬럼: order_id, customer_age, category, channel, price, quantity, amount, return_amount

## 2. 구조 진단 (shape / info / describe)
- 자료형 요약: customer_age·quantity는 int64, price·amount·return_amount는 float64, order_id·category·channel은 object
- 수치 요약에서 눈에 띈 점: customer_age std(43.9)가 mean(34.9)보다 커서 극단값 의심, amount std가 mean의 10배 → 이상치 의심

## 3. 품질 진단 (결측 / 중복 / 표기)
- 결측: amount 51건(3.4%), price 5건(0.33%)
- 이상치(IQR): customer_age 18건, quantity 1건(200), amount 145건(50,000,000 등)
- return_amount는 대부분 0원이라 IQR 기준 적용 부적합(122건 오탐)

## 4. 패턴 (처리 근거)
- amount 결측: 특정 채널(app)에 쏠려 있어 MAR로 판단 → 채널별 중앙값 대체
- customer_age: 999·0살 등 물리적으로 불가능한 값 → NaN 처리 후 중앙값 대체 (처리 후 범위 5~60, 5세는 추가 검토 필요)
- price 결측(5건): 건수 적어 MCAR로 가정 → 카테고리별 중앙값 대체
- amount 이상치(145건): 고액 결제 가능성 있어 삭제 대신 outlier 플래그로 보존

## 5. 다음 분석 제안
- customer_age 최소값 5세가 유효 고객인지 도메인 확인 필요
- amount 결측의 채널 쏠림을 통계 검정으로 재확인해 MAR 가정 보강
- quantity=200 같은 대량 주문건은 도매/이상거래 여부 구분 컬럼 추가 검토
