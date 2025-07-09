import json
import os

# JSON 파일 로드
with open('items.json', 'r', encoding='utf-8') as f:
    items = json.load(f)

# 이미지 및 HTML 리디렉트 생성
for i, item in enumerate(items[:4], start=1):
    # 제목 이미지 생성
    from PIL import Image, ImageDraw, ImageFont
    title = item['title']
    img = Image.new('RGB', (800, 100), color='white')
    d = ImageDraw.Draw(img)
    font = ImageFont.truetype('arial.ttf', 30)
    d.text((10, 30), title, font=font, fill=(0, 0, 0))
    image_filename = f'title{i}.png'
    img.save(image_filename)
    print(f'{image_filename} 저장 완료')

    # HTML 리디렉트 생성
    redirect_url = item['url']
    html_content = f"""<!DOCTYPE html>
<html>
  <head>
    <meta http-equiv=\"refresh\" content=\"0; url={redirect_url}\" />
    <script>
      window.location.href = \"{redirect_url}\";
    </script>
    <title>Redirecting...</title>
  </head>
  <body>
    <p>Redirecting to eBay...</p>
  </body>
</html>"""

    html_filename = f'go{i}.html'
    with open(html_filename, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f'{html_filename} 생성 완료 → {redirect_url}')
