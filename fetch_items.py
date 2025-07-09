# fetch_items.py
# eBay에서 상품 정보를 가져와 items.json으로 저장

import requests
import json

# 발급받은 eBay 토큰 입력
ACCESS_TOKEN = 'YOUR_EBAY_ACCESS_TOKEN'
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
