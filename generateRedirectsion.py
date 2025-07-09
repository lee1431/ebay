import json

# JSON 파일 로드
with open('items.json', 'r', encoding='utf-8') as f:
    items = json.load(f)

# 최대 4개까지만 처리 (items가 4개 이상일 경우)
for i, item in enumerate(items[:4], start=1):
    redirect_url = item['url']
    html_content = f"""<!DOCTYPE html>
<html>
  <head>
    <meta http-equiv="refresh" content="0; url={redirect_url}" />
    <script>
      window.location.href = "{redirect_url}";
    </script>
    <title>Redirecting...</title>
  </head>
  <body>
    <p>Redirecting to eBay...</p>
  </body>
</html>"""

    # go1.html, go2.html ... 으로 저장
    with open(f'go{i}.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f'go{i}.html 생성 완료 → {redirect_url}')
