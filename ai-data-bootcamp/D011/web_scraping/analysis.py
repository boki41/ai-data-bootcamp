import pandas as pd
import matplotlib.pyplot as plt

# 한글 폰트 설정 (깨짐 방지)
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# CSV 불러오기
df = pd.read_csv("musinsa_pants.csv")

# 리뷰수가 없는 행 제거
df = df.dropna(subset=["리뷰수", "할인율"])

print("분석 대상 상품 개수:", len(df))
print(df[["상품명", "할인율", "리뷰수"]])

# 상관계수 계산
corr = df["할인율"].corr(df["리뷰수"])
print(f"\n할인율과 리뷰수의 상관계수: {corr:.3f}")

# 산점도 그리기
plt.figure(figsize=(8, 6))
plt.scatter(df["할인율"], df["리뷰수"], alpha=0.7)
plt.xlabel("할인율 (%)")
plt.ylabel("리뷰수")
plt.title(f"할인율 vs 리뷰수 (상관계수: {corr:.3f})")
plt.grid(True, alpha=0.3)

# 그래프 저장 + 화면에 보이기
plt.savefig("discount_vs_review.png")
plt.show()