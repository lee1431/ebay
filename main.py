# main.py
# items.json을 기반으로 제목 이미지(titleN.png)와 리디렉트 HTML(goN.html) 파일을 생성하는 스크립트

import json
import os
import random
from PIL import Image, ImageDraw, ImageFont

# JSON 로드
def load_items():
    with open('items.json', 'r', encoding='utf-8') as f:
        return json.load(f)

# 제목 이미지를 이미지로 저장
def text_to_image(text, filename):
    img = Image.new('RGB', (800, 100), color='white')
    d = ImageDraw.Draw(img)
    font = ImageFont.truetype('arial.ttf', 30)
    d.text((10, 30), text, font=font, fill=(0, 0, 0))
    img.save(filename)

# 리디렉트 HTML 생성
def generate_html(url, filename):
    html = f"""<!DOCTYPE html>
<html>
  <head>
    <meta http-equiv=\"refresh\" content=\"0; url={url}\" />
    <script>window.location.href = \"{url}\";</script>
    <title>Redirecting...</title>
  </head>
  <body><p>Redirecting to eBay...</p></body>
</html>"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)

# 실행 로직
def main():
    items = load_items()
    if len(items) < 4:
        print("상품 수가 부족합니다.")
        return

    selected = random.sample(items, 4)  # 매번 다른 4개 선택

    for i, item in enumerate(selected, 1):
        title = item['title']
        url = item['url']

        text_to_image(title, f'title{i}.png')
        generate_html(url, f'go{i}.html')

        print(f'title{i}.png & go{i}.html 생성 완료')

if __name__ == '__main__':
    main()
