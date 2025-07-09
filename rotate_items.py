import json, os
from PIL import Image, ImageDraw, ImageFont

with open('items.json', 'r') as f:
    items = json.load(f)

with open('rotation_index.json', 'r') as f:
    index_data = json.load(f)

i = index_data["current_index"]
total = index_data["total_items"]
batch = 4

# 다음 4개 추출
subset = items[i:i+batch]
if len(subset) < batch:
    subset += items[:batch - len(subset)]  # 끝까지 갔으면 처음부터 다시

# 이미지 저장
for idx, item in enumerate(subset):
    title = item['title']
    thumb = item['image']
    # 저장...
    print(f"title{idx+1}.png ← {title}")
    print(f"thumb{idx+1}.jpg ← {thumb}")

# 인덱스 갱신
next_index = (i + batch) % total
index_data['current_index'] = next_index
with open('rotation_index.json', 'w') as f:
    json.dump(index_data, f)
