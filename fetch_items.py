# fetch_items.py
# eBay에서 상품 정보를 가져와 items.json으로 저장

import requests
import json

# 발급받은 eBay 토큰 입력
ACCESS_TOKEN = 'v^1.1#i^1#r^0#f^0#I^3#p^1#t^H4sIAAAAAAAA/+VYW2wUVRje3V4IwaICAUOALAPFCM7smdmZ3Z2RXbP0ulBoYdsCaxo8M3OmHZidWWdmabdeslQlGqRpfPDBqlR9wFt8wFISwsWiETRcDBaJCSFqDDGaGC81ECKJM7NL2VYCSDexifuyOf/5z3++7zv/f86ZA7Ll05fvrN95ucI9zTOQBVmP203OANPLy1bMLPHML3OBAgf3QHZptrSn5MeVBkwqKW4DMlKaaiBvV1JRDc4xhrG0rnIaNGSDU2ESGZwpcPHo2gaOIgCX0jVTEzQF88aqw1iI53kkAoYVeR6wKGRZ1esxm7UwhkSaDUJJZIOSJARIZPUbRhrFVMOEqhnGKEAxOAjigG0GLMcEOMAQNE0lMG8r0g1ZUy0XAmARBy7njNULsN4aKjQMpJtWECwSi9bGG6Ox6pp1zSt9BbEieR3iJjTTxvhWlSYibytU0ujW0xiONxdPCwIyDMwXyc0wPigXvQ7mLuA7Ugdpiff7WZolA0EGklRRpKzV9CQ0b43DtsgiLjmuHFJN2czcTlFLDX4rEsx8a50VIlbttf/Wp6EiSzLSw1jNqujmaFMTFmlAKA7V9nq8DlnBUVLBmzZU43wIsRLixRAuBPy8yJPB/ES5aHmZJ8xUpamibItmeNdp5ipkoUYTtaELtLGcGtVGPSqZNqICP5K8rqE/kLAXNbeKabNDtdcVJS0hvE7z9iswNto0dZlPm2gswsQOR6IwBlMpWcQmdjq5mE+fLiOMdZhmivP5Ojs7iU4/oentPgoA0rdpbUNc6EBJiFm+dq3n/OXbD8Blh4pglanlz5mZlIWly8pVC4DajkUYPxWgqLzu42FFJlr/YSjg7BtfEcWqEIkkJcDTFGQEf4AO+otRIZF8kvpsHIiHGTwJ9W3ITClQQLhg5Vk6iXRZ5PyMRPlDEsLFACvhNCtJOM+IAZyUEAII8bzAhv5PhXKnqR5Hgo7MouR60fK8e0NLBq5I0A213Y1paZNSK6AqmhY15N/KKK18d0esaaNE13Wwq+nwnVbDTclXKbKlTLM1fzEEsGu9eCLUa4aJxEnRiwtaCjVpiixkptYC+3WxCepmJo4UxTJMimQ0lYoVZ68uGr1/uU3cHe/inVH/0fl0U1aGnbJTi5U93rACwJRM2CcQIWhJn13rGrSuH7Z5i4N6Urxl6+Y6pVhbJHNsZTF35SQcuoSxXSB0ZGhp3bptE432DaxZ24ZU6zwzdU1RkN5KTrqek8m0CXkFTbXCLkKCy3CKHbZkkKEAQ7MBZlK8BOco3TLVtqRibMWldXd5rfaN/8iPuJwf2eM+BnrcRzxuN1gJKsklYHF5SUtpyT3zDQshIUOJMOR21fp21RGxDWVSUNY9s11nZjaIO+ob/szy6QMbRx8NuSoK3hgG2sADY68M00vIGQVPDmDBjZ4y8t55FRQDgoAFLBMATAIsudFbSs4tncMdeDoSfRYO9+zefL7y6ve/Dy3Ysx1UjDm53WWu0h63q3yhulsXB4/M3n+4ffB47+dvjpxekw0s3Lf8lZd2Pdk/S3hbOhOY1XZw37WdV06eHnhEv3bC2/F+5Rp29KP7hLpz/Z7+K0TZxb4XPC2r5yI3Ab0XD+757qG1R1/s2jty4dwh/mrIWwepw9MGHjtq/Lbli2mn5nz911D/yImXt+4/E/ns/OOL38VMgH6Szw7+8Grw0lM7fv5yV2LRJ9/2NlauqP312FdPzBuMfLhn09n3lu1969Nnems2t5xDH4Tcz69+7fWRITJ+9rlT/uFLpxPfdC9a8MuhoOv+y3/gNUOR3pJ4Z9+F9cvWHK8Y7uvcsVgXY6MfL61b/86Db6y64mqbN1qbaDs5vKT35LWHhdxa/g2FNzpX/REAAA=='
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
