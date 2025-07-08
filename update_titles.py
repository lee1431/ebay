# 1. update_titles.py
# 상품명 4개를 가져와 이미지로 저장하는 메인 스크립트
import requests
import random
from PIL import Image, ImageDraw, ImageFont
import os

APP_ID = 'YOUR_APP_ID'  # <- 여기에 본인의 Production App ID 입력
SELLER_ID = 'YOUR_SELLER_ID'

# eBay Finding API로 상품 가져오기
def fetch_items():
    url = 'https://svcs.ebay.com/services/search/FindingService/v1'
    params = {
        'OPERATION-NAME': 'findItemsAdvanced',
        'SERVICE-VERSION': '1.0.0',
        'SECURITY-APPNAME': APP_ID,
        'RESPONSE-DATA-FORMAT': 'JSON',
        'itemFilter(0).name': 'Seller',
        'itemFilter(0).value': SELLER_ID,
        'paginationInput.entriesPerPage': '20'
    }
    response = requests.get(url, params=params)
    data = response.json()
    items = data['findItemsAdvancedResponse'][0]['searchResult'][0].get('item', [])
    return items

# 상품명 → 이미지 변환
def text_to_image(text, out_file):
    img = Image.new('RGB', (800, 100), color='white')
    d = ImageDraw.Draw(img)
    font = ImageFont.truetype('arial.ttf', 30)
    d.text((10, 30), text, font=font, fill=(0, 0, 0))
    img.save(out_file)

# 실행 로직
def main():
    items = fetch_items()
    if len(items) < 4:
        print('상품이 4개 미만입니다.')
        return

    selected = random.sample(items, 4)
    for i, item in enumerate(selected, start=1):
        title = item['title'][0]
        filename = f'title{i}.png'
        text_to_image(title, filename)
        print(f'{filename} 저장 완료: {title}')

if __name__ == '__main__':
    main()
