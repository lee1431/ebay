import json
import os
import urllib.request

with open('items.json', 'r') as f:
    items = json.load(f)

with open('rotation_index.json', 'r') as f:
    index_data = json.load(f)

total = index_data["total_items"]

if total == 0:
    print("❌ items.json에 유효한 항목이 없습니다. fetch_items.py 확인 필요.")
    exit(1)

i = index_data["current_index"]
batch = 4

# 다음 4개 추출
subset = items[i:i + batch]
if len(subset) < batch:
    subset += items[:batch - len(subset)]  # 순환 처리

# 이미지 저장 및 링크 생성
html_lines = ["<html><body><h1>추천 상품</h1>"]
for idx, item in enumerate(subset):
    title = item["title"]
    image = item["image"]
    url = item["itemWebUrl"]
    filename = f"thumb{idx + 1}.jpg"

    urllib.request.urlretrieve(image, filename)
    print(f"{filename} 저장 완료: {title}")

    html_lines.append(f'<a href="{url}" target="_blank"><img src="{filename}" width="225"></a>')

html_lines.append("</body></html>")

with open("go1.html", "w") as f:
    f.write("\n".join(html_lines))
print("✅ go1.html 생성 완료")

# 인덱스 갱신
next_index = (i + batch) % total
index_data['current_index'] = next_index
with open('rotation_index.json', 'w') as f:
    json.dump(index_data, f)
