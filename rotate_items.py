import json, os
from PIL import Image
import requests

# 경로 설정
ITEMS_JSON = 'items.json'
INDEX_JSON = 'rotation_index.json'
OUTPUT_DIR = 'output'
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 아이템 데이터 로드
with open(ITEMS_JSON, 'r') as f:
    items = json.load(f)

# rotation_index.json 없으면 초기화
if not os.path.exists(INDEX_JSON):
    index_data = {"current_index": 0, "total_items": len(items)}
    with open(INDEX_JSON, 'w') as f:
        json.dump(index_data, f)
else:
    with open(INDEX_JSON, 'r') as f:
        index_data = json.load(f)

i = index_data["current_index"]
total = index_data["total_items"]
batch = 4

# 다음 4개 아이템 선택
subset = items[i:i+batch]
if len(subset) < batch:
    subset += items[:batch - len(subset)]

# 이미지 및 HTML 저장
for idx, item in enumerate(subset):
    image_url = item["image"]
    item_url = item["itemWebUrl"]

    # 이미지 저장
    img_path = os.path.join(OUTPUT_DIR, f"thumb{idx+1}.jpg")
    with open(img_path, 'wb') as img_file:
        img_file.write(requests.get(image_url).content)

    # HTML 저장
    html_path = os.path.join(OUTPUT_DIR, f"go{idx+1}.html")
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(f'<meta http-equiv="refresh" content="0; url={item_url}">')

    print(f"Saved: {img_path}, {html_path}")

# 인덱스 갱신
next_index = (i + batch) % total
index_data['current_index'] = next_index
with open(INDEX_JSON, 'w') as f:
    json.dump(index_data, f)
