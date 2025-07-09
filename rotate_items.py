import json, os, requests

# 설정
BATCH_SIZE = 4

# 데이터 로드
with open('items.json', 'r') as f:
    items = json.load(f)

with open('rotation_index.json', 'r') as f:
    index_data = json.load(f)

i = index_data["current_index"]
total = index_data["total_items"]
subset = items[i:i+BATCH_SIZE]
if len(subset) < BATCH_SIZE:
    subset += items[:BATCH_SIZE - len(subset)]

# 폴더 생성
os.makedirs("output", exist_ok=True)

# 처리
for idx, item in enumerate(subset):
    image_url = item["image"]
    item_url = item["itemWebUrl"]

    # 썸네일 이미지 저장
    img_data = requests.get(image_url).content
    with open(f'output/thumb{idx+1}.jpg', 'wb') as f:
        f.write(img_data)

    # HTML 링크 파일 생성
    with open(f'output/go{idx+1}.html', 'w') as f:
        f.write(f'<meta http-equiv="refresh" content="0;url={item_url}">')

# 인덱스 갱신
index_data["current_index"] = (i + BATCH_SIZE) % total
with open('rotation_index.json', 'w') as f:
    json.dump(index_data, f)
