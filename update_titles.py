import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import os

# 🔐 eBay OAuth Access Token (Bearer 생략)
ACCESS_TOKEN = 'v^1.1#i^1#f^0#I^3#p^1#r^0#t^H4sIAAAAAAAA/+VYfWwTZRhvt26ywBCBiCIx9aYJiHe9u35dz7Vb991R1kHHwBkg7929t9643tW7K1tHlLooSCSSkBjlS4cGGBCJGIkQEyHGPySAEFT8+gMTNcGogRgIhODHe9cyukkAWROX2H+ae97nfd7f7/c+z/tFZssrHl/TsuZypf2eksEsmS2x26mJZEV52dzJpSUzy2xkgYN9MPto1jFQeq5aB0k5xS6EekpVdOjsS8qKzlrGIJbWFFYFuqSzCkhCnTV4Nh6eH2VpgmRTmmqovCpjzkhDEBNEKuAVOIEBEPhJH4WsyvWYHWoQcwsM5eF4gRbdwC0yZruup2FE0Q2gGEGMJmkvTvpxMtBBUaybYSmaoCl/F+bshJouqQpyIUgsZMFlrb5aAdZbQwW6DjUDBcFCkXBTPBaONDS2dVS7CmKF8jrEDWCk9ZFf9aoAnZ1ATsNbD6Nb3mw8zfNQ1zFXKDfCyKBs+DqYu4BvSQ1JyHMUTZIMT3uBTyiKlE2qlgTGrXGYFknARcuVhYohGZnbKYrU4Hogb+S/2lCISIPT/FuQBrIkSlALYo114afC7e1YKAphHCjdLXgzRMFhUsbbFzbgHAMDIkS5hfM+NydwlD8/UC5aXuZRI9WriiCZounONtWogwg1HK0NXaANcoopMS0sGiaiQj/3dQ1Jpsuc1Nwspo2EYs4rTCIhnNbn7WdguLdhaBKXNuBwhNENlkRBDKRSkoCNbrRyMZ8+fXoQSxhGinW5ent7iV43oWrdLpQdlGvJ/GicT8AkwJCvWes5f+n2HXDJosJD1FOXWCOTQlj6UK4iAEo3FvK6aR9N53UfCSs02voPQwFn18iKKFaFMB4IPD7IAJHxuEXaX4wKCeWT1GXigBzI4EmgrYBGSgY8xHmUZ+kk1CSBdXtF2s2IEBd8ARH3BEQR57yCD6dEiCoXchwfYP5PhXKnqR6HvAaNouR60fK8f+GiDJjb5Yk29cfS4hK5iYf1Ho+gQnePV+7k+hOR9sWipzkRaPUE77Qabkq+XpaQMh1o/GIIYNZ68URoUXUDCmOiF+fVFGxXZYnPjK8JdmtCO9CMTBzKMjKMiWQ4lYoUZ60uGr1/uUzcHe/i7VH/0f50U1a6mbLji5XZX0cBQEoizB2I4NWky6x1FaDjh2lebqEeE28JnVzHFWtEMsdWEnJHTsKiS+greUKDuprW0GmbiJknsA51BVTQfmZoqixDrZMacz0nk2kDcDIcb4VdhASXwDjbbCm/l0Y3RzIwNl68tZUuH29LUjGWYkfzXR6rXSMv+SGb9aMG7B+TA/aPSux2spp8jKoiHykvXeQonTRTRwgJCYiELnUr6O6qQWIFzKSApJVMs52cHBWeb4leynLpDxZfrGFslQVvDINLyQeGXxkqSqmJBU8O5KwbLWXUvTMqaS/pJwMU5WYouousutHqoO53TH+p4eeenZtPTmt59sn7uC+6iVW+xK9k5bCT3V5mcwzYbW1f7jgrnfrrh50HJXHLpMsX9+z6feNXT1cdeP3s4b7jq2b09MzbdW2CY9m+D4fWfdq/IfTKa3WxF7Gqmvddl4Vj207X2vYswyd0Xjq1vPLK+qpvYrO2nVRemJ44/ElVzfn9rVt2PzPnUOpq8u1u6fxUds+munDFiQcvzN945A1u45ufBUK7a1c2rr2wYXvHnOpYLfwx2rC/9srq9cHAjnN7y6/W/PH5q2ey725ufodfcPDra66mva4zv4CrgeB3U1t7e8oBtn3rsczk1nmnB46GBk+s+3Pf0ivznngIfPvye1uE54bo3y6+tXL1T4fmrh38Hh4n2g7O1pu3Pjw0m2ztPHJt0/mjLQekKcemDE3y5+byb8+kQkr9EQAA'
SELLER_ID = 'anglingcentre'
SEARCH_QUERY = 'carp'
LIMIT = 4

# 📦 Browse API로 상품 목록 가져오기
def fetch_items():
    url = 'https://api.ebay.com/buy/browse/v1/item_summary/search'
    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}',
        'Content-Type': 'application/json',
        'X-EBAY-C-MARKETPLACE-ID': 'EBAY_GB'
    }
    params = {
        'q': SEARCH_QUERY,
        'filter': f'seller:{SELLER_ID}',
        'limit': LIMIT
    }
    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    if 'itemSummaries' not in data:
        print('❌ 상품을 가져오지 못했습니다.')
        print(data)
        return []

    return data['itemSummaries']

# 🖼 상품명 → 이미지 저장
def text_to_image(text, out_file):
    img = Image.new('RGB', (800, 100), color='white')
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype('arial.ttf', 30)
    except IOError:
        font = ImageFont.load_default()
    draw.text((10, 30), text, font=font, fill=(0, 0, 0))
    img.save(out_file)

# 🌄 썸네일 이미지 다운로드 및 저장
def download_thumbnail(url, out_file):
    try:
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        img.save(out_file)
    except Exception as e:
        print(f'❌ 이미지 다운로드 실패: {url}')
        print(e)

# 🚀 실행 메인
def main():
    items = fetch_items()
    if not items:
        print('상품이 없습니다.')
        return

    for i, item in enumerate(items, start=1):
        title = item.get('title', 'Untitled')
        text_filename = f'title{i}.png'
        thumb_filename = f'thumb{i}.jpg'

        # 텍스트 이미지 저장
        text_to_image(title, text_filename)
        print(f'🖋 {text_filename} 저장 완료: {title}')

        # 썸네일 이미지 저장
        img_url = item.get('image', {}).get('imageUrl')
        if img_url:
            download_thumbnail(img_url, thumb_filename)
            print(f'🖼 {thumb_filename} 저장 완료: {img_url}')
        else:
            print(f'⚠️ 썸네일 없음: {title}')

if __name__ == '__main__':
    main()
