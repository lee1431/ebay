# fetch_items.py
# eBay에서 상품 정보를 가져와 items.json으로 저장

import requests
import json

# 발급받은 eBay 토큰 입력
ACCESS_TOKEN = 'v^1.1#i^1#p^1#f^0#I^3#r^0#t^H4sIAAAAAAAA/+VYa2wUVRTe2W5LChRJKEhAwzIWg8WZndnZ59hd3ba0XVO6S7e0UGNgHnfagXll7qztEk2W/kAIhNCIQk0MNRqDRmNUwFcV8ZFgBCEq8S0/jAZQFCMEQRK9s13KthJAuolN3D+bOffcc7/vu+fcF5UtK69e37T+XAU2yTmYpbJODKOnUOVlpYumlTjnlDqoAgdsMFuVdfWVHK+BnKoYbCuAhq5B4O5VFQ2yOWMET5saq3NQhqzGqQCylsCmYkuaWS9JsYapW7qgK7g7Xh/B/T4hEAQ07feJoYAYDCCrdilmmx7BaYkOhEXJ7w/7QJAPCKgdwjSIa9DiNCuCeymvn6CCBBVuo2mW8bE0Q9LBcCfubgcmlHUNuZAUHs3BZXN9zQKsV4fKQQhMCwXBo/FYQyoRi9cvbmmr8RTEiuZ1SFmclYajv+p0EbjbOSUNrj4MzHmzqbQgAAhxT3R4hNFB2dglMDcAPyc1kEIBLycKAV+ACkmCWBQpG3RT5ayr47AtskhIOVcWaJZsZa6lKFKDXw0EK//VgkLE693239I0p8iSDMwIvrg2tiKWTOLRZgBSnNbVRDQCFByoCpFsrSf4EAhLgBdDhBBgeJGng/mBhqPlZR4zUp2uibItGnS36FYtQKjBWG28Bdogp4SWMGOSZSMq9GNGNKQ77UkdnsW01a3Z8wpUJIQ793ntGRjpbVmmzKctMBJhbENOogjOGYYs4mMbc7mYT59eGMG7LctgPZ6enh6yhyF1s8vjpSjas3xJc0roBiqHI1+71of95Wt3IOQcFQGgnlBmrYyBsPSiXEUAtC486me8Aa83r/toWNGx1n8YCjh7RldEsSqE89IhBvgkKiiFeLo4i000n6QeGwfguQyhcuYaYBkKJwBCQHmWVoEpiyzjl7xMSAKEGAhLhC8sSQTvFwMELQFAAcDzQjj0fyqU6031FBBMYBUl14uW52tbl2W4RZ2+5oa1ibS0XGkQQJ3PJ+qAWe1X2vm13fFkh+Rr7A7f64tcbzVckXydIiNl2tD4xRDArvXiidCkQwuI46KXEnQDJHVFFjITa4IZU0xyppVJAUVBhnGRjBlGvDhrddHo/ctl4sZ4F2+P+o/2pyuygnbKTixWdn+IAnCGTNo7ECnoqseudZ1Dxw/bvDKHely8ZXRynVCsEclhtrI4fOQkc3RJ+IBAmgDqaROdtsmEfQJr09cADe1nlqkrCjDb6XHXs6qmLY5XwEQr7CIkuMxNsM2WDvq9FLrS+Jlx8RJyW+nKibYkFWMpdjXe4LHaM/qSH3XkfnQf9i7Vh73txDCqhlpA30bNLytZ5iqZOgcihKTMSSSUuzR0dzUBuQZkDE42nTMch6c1i+uams9m+fSrHWfuDjkqCt4YBu+nZo+8MpSX0FMKnhyoWy63lNI33Vzh9VNBKkzTjI9mOqnbLre66Fmuyo/3HzuxcGaio3HbLm3uhVlcS81Xd1AVI04YVupw9WGOPRsmq5uP8qfb8S3fZaQhx74L60/W7cWeYmoPHtmx4FaH8/lvWyt3PfnZ4WewIz1THzr95vY9ZeK610/4zw849z/x13lPxYc7d2ze9kbFqkM7D7q//mP37O7H95GTB45NuVO8feljQxv7y36+rzJ17veHq3e/8MU3rqrpQ5/8ED/1yHS+fdM7cIdS+374ZC3fQn/64oCZ+ODR3946c0qdR9XMe9Ds7299b+ji3ODihpm/fFkOX+pcNJh8ZYb6kbE1+9zelxvU3pZfF/YfulBtHZ2FbXptC+/euOKuP8P6yRnEqtjBSUurKwPkjz/NP/DsPQd2GtXHny47u+Tz0q3RSd9frNnTsb3KPdC/IRGrOjE8l38D50+Q8f0RAAA='
SELLER_ID = 'anglingcentre'
HEADERS = {
    'Authorization': f'Bearer {ACCESS_TOKEN}',
    'Content-Type': 'application/json',
    'X-EBAY-C-MARKETPLACE-ID': 'EBAY_GB'
}

# 검색 URL (카테고리 없이 전체 셀러 상품 조회)
SEARCH_URL = 'https://api.ebay.com/buy/browse/v1/item_summary/search'
PARAMS = {
    'filter': f'seller:{SELLER_ID}',
    'limit': '50'
}

# API 호출 후 결과 저장
response = requests.get(SEARCH_URL, headers=HEADERS, params=PARAMS)
data = response.json()

items = []
for item in data.get('itemSummaries', []):
    items.append({
        'itemWebUrl': item.get('itemWebUrl'),
        'legacyItemId': item.get('legacyItemId'),
        'additionalImages': [img['imageUrl'] for img in item.get('additionalImages', [])]
    })

with open('items.json', 'w', encoding='utf-8') as f:
    json.dump(items, f, ensure_ascii=False, indent=2)

print(f"총 {len(items)}개 아이템 저장 완료.")
