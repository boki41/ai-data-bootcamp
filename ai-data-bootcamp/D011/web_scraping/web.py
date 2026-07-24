from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import re
import csv

url = "https://www.musinsa.com/brand/musinsastandardwoman/products?categoryCode=003&gf=A"

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

driver.get(url)
time.sleep(3)

html = driver.page_source
driver.quit()

soup = BeautifulSoup(html, "html.parser")
items = soup.find_all("div", class_=lambda c: c and "GoodsItem" in c)

results = []
seen = set()

for item in items:
    text = item.get_text(separator="|", strip=True)
    parts = [p.strip() for p in text.split("|") if p.strip()]

    if any("원" in p for p in parts) and len(parts) >= 5:
        name = parts[0]
        if name in seen:
            continue
        seen.add(name)

        discount_str = next((p for p in parts if re.fullmatch(r"\d+%", p)), None)
        discount = int(discount_str.replace("%", "")) if discount_str else 0
        price_str = next((p for p in parts if "원" in p and re.search(r"\d", p)), None)
        price_digits = re.sub(r"[^\d]", "", price_str) if price_str else ""
        price = int(price_digits) if price_digits else None

        if price is None:
            continue  # 가격 정보가 없는 상품은 건너뛰기

        review_str = next((p for p in parts if re.fullmatch(r"\(\d+\)", p)), None)
        review_count = int(review_str.strip("()")) if review_str else None

        original_price = round(price / (1 - discount / 100)) if price and discount else price

        results.append({
            "상품명": name,
            "판매가": price,
            "정가": original_price,
            "할인율": discount,
            "리뷰수": review_count
        })

print("최종 상품 개수:", len(results))
print("-" * 50)

for i, r in enumerate(results):
    print(f"[{i+1}] {r['상품명']} | 판매가:{r['판매가']} | 정가:{r['정가']} | 할인율:{r['할인율']}% | 리뷰수:{r['리뷰수']}")

with open("musinsa_pants.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=["상품명", "판매가", "정가", "할인율", "리뷰수"])
    writer.writeheader()
    writer.writerows(results)

print("\nmusinsa_pants.csv 저장 완료")