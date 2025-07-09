import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import os

# 🔐 eBay OAuth Access Token (Bearer 생략)
ACCESS_TOKEN = 'v^1.1#i^1#r^0#f^0#I^3#p^1#t^H4sIAAAAAAAA/+VYW2wUVRje3V4IwaICAUOALAPFCM7smdmZ3Z2RXbP0ulBoYdsCaxo8M3OmHZidWWdmabdeslQlGqRpfPDBqlR9wFt8wFISwsWiETRcDBaJCSFqDDGaGC81ECKJM7NL2VYCSDexifuyOf/5z3++7zv/f86ZA7Ll05fvrN95ucI9zTOQBVmP203OANPLy1bMLPHML3OBAgf3QHZptrSn5MeVBkwqKW4DMlKaaiBvV1JRDc4xhrG0rnIaNGSDU2ESGZwpcPHo2gaOIgCX0jVTEzQF88aqw1iI53kkAoYVeR6wKGRZ1esxm7UwhkSaDUJJZIOSJARIZPUbRhrFVMOEqhnGKEAxOAjigG0GLMcEOMAQNE0lMG8r0g1ZUy0XAmARBy7njNULsN4aKjQMpJtWECwSi9bGG6Ox6pp1zSt9BbEieR3iJjTTxvhWlSYibytU0ujW0xiONxdPCwIyDMwXyc0wPigXvQ7mLuA7Ugdpiff7WZolA0EGklRRpKzV9CQ0b43DtsgiLjmuHFJN2czcTlFLDX4rEsx8a50VIlbttf/Wp6EiSzLSw1jNqujmaFMTFmlAKA7V9nq8DlnBUVLBmzZU43wIsRLixRAuBPy8yJPB/ES5aHmZJ8xUpamibItmeNdp5ipkoUYTtaELtLGcGtVGPSqZNqICP5K8rqE/kLAXNbeKabNDtdcVJS0hvE7z9iswNto0dZlPm2gswsQOR6IwBlMpWcQmdjq5mE+fLiOMdZhmivP5Ojs7iU4/oentPgoA0rdpbUNc6EBJiFm+dq3n/OXbD8Blh4pglanlz5mZlIWly8pVC4DajkUYPxWgqLzu42FFJlr/YSjg7BtfEcWqEIkkJcDTFGQEf4AO+otRIZF8kvpsHIiHGTwJ9W3ITClQQLhg5Vk6iXRZ5PyMRPlDEsLFACvhNCtJOM+IAZyUEAII8bzAhv5PhXKnqR5Hgo7MouR60fK8e0NLBq5I0A213Y1paZNSK6AqmhY15N/KKK18d0esaaNE13Wwq+nwnVbDTclXKbKlTLM1fzEEsGu9eCLUa4aJxEnRiwtaCjVpiixkptYC+3WxCepmJo4UxTJMimQ0lYoVZ68uGr1/uU3cHe/inVH/0fl0U1aGnbJTi5U93rACwJRM2CcQIWhJn13rGrSuH7Z5i4N6Urxl6+Y6pVhbJHNsZTF35SQcuoSxXSB0ZGhp3bptE432DaxZ24ZU6zwzdU1RkN5KTrqek8m0CXkFTbXCLkKCy3CKHbZkkKEAQ7MBZlK8BOco3TLVtqRibMWldXd5rfaN/8iPuJwf2eM+BnrcRzxuN1gJKsklYHF5SUtpyT3zDQshIUOJMOR21fp21RGxDWVSUNY9s11nZjaIO+ob/szy6QMbRx8NuSoK3hgG2sADY68M00vIGQVPDmDBjZ4y8t55FRQDgoAFLBMATAIsudFbSs4tncMdeDoSfRYO9+zefL7y6ve/Dy3Ysx1UjDm53WWu0h63q3yhulsXB4/M3n+4ffB47+dvjpxekw0s3Lf8lZd2Pdk/S3hbOhOY1XZw37WdV06eHnhEv3bC2/F+5Rp29KP7hLpz/Z7+K0TZxb4XPC2r5yI3Ab0XD+757qG1R1/s2jty4dwh/mrIWwepw9MGHjtq/Lbli2mn5nz911D/yImXt+4/E/ns/OOL38VMgH6Szw7+8Grw0lM7fv5yV2LRJ9/2NlauqP312FdPzBuMfLhn09n3lu1969Nnems2t5xDH4Tcz69+7fWRITJ+9rlT/uFLpxPfdC9a8MuhoOv+y3/gNUOR3pJ4Z9+F9cvWHK8Y7uvcsVgXY6MfL61b/86Db6y64mqbN1qbaDs5vKT35LWHhdxa/g2FNzpX/REAAA=='
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
