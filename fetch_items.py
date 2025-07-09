# fetch_items.py
# eBay에서 상품 정보를 가져와 items.json으로 저장

import requests
import json

# 발급받은 eBay 토큰 입력
ACCESS_TOKEN = 'v^1.1#i^1#f^0#I^3#p^1#r^0#t^H4sIAAAAAAAA/+VYfWwTZRhvt26ywBCBiCIx9aYJiHe9u35dz7Vb991R1kHHwBkg7929t9643tW7K1tHlLooSCSSkBjlS4cGGBCJGIkQEyHGPySAEFT8+gMTNcGogRgIhODHe9cyukkAWROX2H+ae97nfd7f7/c+z/tFZssrHl/TsuZypf2eksEsmS2x26mJZEV52dzJpSUzy2xkgYN9MPto1jFQeq5aB0k5xS6EekpVdOjsS8qKzlrGIJbWFFYFuqSzCkhCnTV4Nh6eH2VpgmRTmmqovCpjzkhDEBNEKuAVOIEBEPhJH4WsyvWYHWoQcwsM5eF4gRbdwC0yZruup2FE0Q2gGEGMJmkvTvpxMtBBUaybYSmaoCl/F+bshJouqQpyIUgsZMFlrb5aAdZbQwW6DjUDBcFCkXBTPBaONDS2dVS7CmKF8jrEDWCk9ZFf9aoAnZ1ATsNbD6Nb3mw8zfNQ1zFXKDfCyKBs+DqYu4BvSQ1JyHMUTZIMT3uBTyiKlE2qlgTGrXGYFknARcuVhYohGZnbKYrU4Hogb+S/2lCISIPT/FuQBrIkSlALYo114afC7e1YKAphHCjdLXgzRMFhUsbbFzbgHAMDIkS5hfM+NydwlD8/UC5aXuZRI9WriiCZounONtWogwg1HK0NXaANcoopMS0sGiaiQj/3dQ1Jpsuc1Nwspo2EYs4rTCIhnNbn7WdguLdhaBKXNuBwhNENlkRBDKRSkoCNbrRyMZ8+fXoQSxhGinW5ent7iV43oWrdLpQdlGvJ/GicT8AkwJCvWes5f+n2HXDJosJD1FOXWCOTQlj6UK4iAEo3FvK6aR9N53UfCSs02voPQwFn18iKKFaFMB4IPD7IAJHxuEXaX4wKCeWT1GXigBzI4EmgrYBGSgY8xHmUZ+kk1CSBdXtF2s2IEBd8ARH3BEQR57yCD6dEiCoXchwfYP5PhXKnqR6HvAaNouR60fK8f+GiDJjb5Yk29cfS4hK5iYf1Ho+gQnePV+7k+hOR9sWipzkRaPUE77Qabkq+XpaQMh1o/GIIYNZ68URoUXUDCmOiF+fVFGxXZYnPjK8JdmtCO9CMTBzKMjKMiWQ4lYoUZ60uGr1/uUzcHe/i7VH/0f50U1a6mbLji5XZX0cBQEoizB2I4NWky6x1FaDjh2lebqEeE28JnVzHFWtEMsdWEnJHTsKiS+greUKDuprW0GmbiJknsA51BVTQfmZoqixDrZMacz0nk2kDcDIcb4VdhASXwDjbbCm/l0Y3RzIwNl68tZUuH29LUjGWYkfzXR6rXSMv+SGb9aMG7B+TA/aPSux2spp8jKoiHykvXeQonTRTRwgJCYiELnUr6O6qQWIFzKSApJVMs52cHBWeb4leynLpDxZfrGFslQVvDINLyQeGXxkqSqmJBU8O5KwbLWXUvTMqaS/pJwMU5WYouousutHqoO53TH+p4eeenZtPTmt59sn7uC+6iVW+xK9k5bCT3V5mcwzYbW1f7jgrnfrrh50HJXHLpMsX9+z6feNXT1cdeP3s4b7jq2b09MzbdW2CY9m+D4fWfdq/IfTKa3WxF7Gqmvddl4Vj207X2vYswyd0Xjq1vPLK+qpvYrO2nVRemJ44/ElVzfn9rVt2PzPnUOpq8u1u6fxUds+munDFiQcvzN945A1u45ufBUK7a1c2rr2wYXvHnOpYLfwx2rC/9srq9cHAjnN7y6/W/PH5q2ey725ufodfcPDra66mva4zv4CrgeB3U1t7e8oBtn3rsczk1nmnB46GBk+s+3Pf0ivznngIfPvye1uE54bo3y6+tXL1T4fmrh38Hh4n2g7O1pu3Pjw0m2ztPHJt0/mjLQekKcemDE3y5+byb8+kQkr9EQAA'
SELLER_ID = 'anglingcentre'
HEADERS = {
    'Authorization': f'Bearer {ACCESS_TOKEN}',
    'Content-Type': 'application/json',
    'X-EBAY-C-MARKETPLACE-ID': 'EBAY_GB'
}

# 검색 URL (카테고리 없이 전체 셀러 상품 조회)
SEARCH_URL = 'https://api.ebay.com/buy/browse/v1/item_summary/search'
PARAMS = {
    'q': 'fishing',
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
