import requests
from PIL import Image, ImageDraw, ImageFont
import os

# [필수] 여기에 Access Token 넣어주세요 (Bearer 부분은 자동으로 붙음)
ACCESS_TOKEN = 'v^1.1#i^1#r^0#p^1#f^0#I^3#t^H4sIAAAAAAAA/+VYbWwURRjutdc2bSkgCggCuS6fAXdv9uPu9pbelev3YWkPri3YxJS93dl2YW93s7tne9WQoxH8YSRBNEFMLMEY/EGQRAmpEWIsIrESQEwMmvjHkBA/YmIxEj6Cs3dHuVYCSC+xiffnMu+8887zPPO+M7MDUiVlq3c37/6r0lFaeDAFUoUOB1kBykqK18wsKlxYXAByHBwHU8tSzsGiq9UmH1d0bhM0dU01oas/rqgmlzYGsIShchpvyian8nFocpbARUMbWjiKAJxuaJYmaArmCtcHMJIkGYqk/RQpeHmKopBVvRuzXQtgIvCzUJRY1kNTPtLvRf2mmYBh1bR41QpgFKA8OPDhwN8O/JyH4Ria8Pl8XZirExqmrKnIhQBYMA2XS481crA+GCpvmtCwUBAsGA41RttC4fqG1vZqd06sYFaHqMVbCXNiq04ToauTVxLwwdOYaW8umhAEaJqYO5iZYWJQLnQXzGPAT0sNISRprwhjPMOwFEXnRcpGzYjz1oNx2BZZxKW0KwdVS7aSD1MUqRHbBgUr22pFIcL1LvtvY4JXZEmGRgBrqA09H4pEsGALhFFe7WnGmyAKDuMKHtlUj8dY6JdgTGRxwUvHxBjpy06UiZaVedJMdZoqyrZopqtVs2ohQg0na8PkaIOc2tQ2IyRZNqIcP5Ic15Dushc1s4oJq1e11xXGkRCudPPhKzA+2rIMOZaw4HiEyR1piQIYr+uyiE3uTOdiNn36zQDWa1k653b39fURfTShGT1uCgDSvWVDS1TohXEeQ752rWf85YcPwOU0FQGikabMWUkdYelHuYoAqD1YEBWxl6Kyuk+EFZxs/Ychh7N7YkXkrUIEEtKC1+cFjJ+SSJCPCglmk9Rt40C1l8TjvLEdWrrCCxAXUJ4l4tCQRY72SBTNShAXvX4JZ/yShMc8ohcnJQgBhLGY4Gf/T4XyqKkehYIBrbzket7yfGBTR5Jf08W0NA60JaQtSqMA6xhG1CC9zaN0xgZ6w5HNEtPU61/PBB61Gu5Lvk6RkTLtaP58CGDXev5EaNZMC4pTohcVNB1GNEUWktNrgWlDjPCGlYxCRUGGKZEM6Xo4P3t13uj9y23i8Xjn74z6j86n+7Iy7ZSdXqzs8SYKwOsyYZ9AhKDF3Xatazy6ftjm7jTqKfGW0c11WrFGJDNsZTFz5STSdAnzRYEwoKklDHTbJtrsG1i7th2q6DyzDE1RoNFJTrme4/GExccUON0KOw8JLvPT7LAlfR4KeBiWpafES0gfpd3TbUvKx1bsbHrMa7V74kd+sCD9Iwcdn4NBx6lChwNUg+XkUlBVUtThLJqx0EQICZmXCFPuUdG3qwGJ7TCp87JR+GTB+Zkt4s7mlj9TscSJzddq2ILKnDeGgy+Ap8dfGcqKyIqcJwew6F5PMTlrfiXlAT7gB34Pw9BdYOm9Xic5z/kU9+Ov+msj69i20bO3fgi+gr99eU0HqBx3cjiKC5yDjoLI3qIu5dbeIz93d79/O/HHe74VyuCpDzcenrPgwqW5NVc6nrhqgOVffT2yZPXN2akjFftvHKr9hVix4Ivogec+aqkZrRxw4jPGxla9u3jRnVn9Yz+VfDw0t3Tfy+ruDy556+bMq3nn2OHFOy7u+fSbT87dqe4sl17vLimtIE9cO//9zuM9385pWNfqGl7o23f89LWtl/0H3ho+Wba/rQzUbd3FruKun321dO2ypTu+vHi2wTvMXr0xrF+oGjoU3tk4tDJwu3bomWevHDt/c6Xcs6fYt4Vd/4a+602teHRG+VF8/8Bn5VeqLhzDft/QX3T99JKmvrFzR+f/Vts5u/wOtvnMdy9hWytPrh09MzJyO7OWfwN4shim/REAAA=='
SELLER_ID = 'anglingcentre'
SEARCH_QUERY = 'carp'
LIMIT = 4

# Browse API로 상품 가져오기
def fetch_items():
    url = f'https://api.ebay.com/buy/browse/v1/item_summary/search'
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

# 상품명 → 이미지로 저장
def text_to_image(text, out_file):
    img = Image.new('RGB', (800, 100), color='white')
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype('arial.ttf', 30)
    except IOError:
        font = ImageFont.load_default()
    draw.text((10, 30), text, font=font, fill=(0, 0, 0))
    img.save(out_file)

# 실행 로직
def main():
    items = fetch_items()
    if len(items) < 1:
        print('상품이 없습니다.')
        return

    for i, item in enumerate(items, start=1):
        title = item.get('title', 'Untitled')
        filename = f'title{i}.png'
        text_to_image(title, filename)
        print(f'{filename} 저장 완료: {title}')

if __name__ == '__main__':
    main()
