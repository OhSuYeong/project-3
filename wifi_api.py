import urllib.request
from xml.etree.ElementTree import fromstring, ElementTree
from elasticsearch import Elasticsearch, helpers

es = Elasticsearch("http://211.183.3.10:9200")

docs = []

for i in range(1, 22):
    iStart = (i - 1) * 1000 + 1
    iEnd = i * 1000

    url = 'http://openapi.seoul.go.kr:8088/755254476877623038394a4d4e4365/xml/TbPublicWifiInfo/' + str(iStart) + '/' + str(iEnd) + '/'
    response = urllib.request.urlopen(url)
    xml_str = response.read().decode('utf-8')

    tree = ElementTree(fromstring(xml_str))
    root = tree.getroot()

    # (1) 구 이름, 설치장소 및 위/경도 정보 수집하여
    for row in root.iter("row"):
        gu_nm = row.find('X_SWIFI_WRDOFC').text
        place_nm = row.find('X_SWIFI_MAIN_NM').text
        place_x = float(row.find('LAT').text)
        place_y = float(row.find('LNT').text)

        # 위도와 경도가 뒤바뀐 경우 수정
        if place_x > 90:
            place_x, place_y = place_y, place_x

        # (2) 지정된 인덱스에 도큐먼트 소스로 넣기
        doc = {
            "_index": "seoulwifi",  # 미리 seoulwifi 인덱스, 인덱스 패턴을 생성해 둔다
            "_source": {
                "gu_nm": gu_nm,
                "place_nm": place_nm,
                "instl_xy": {
                    "lat": place_x,
                    "lon": place_y
                }
            }
        }
        docs.append(doc)

    print("END", iStart, "~", iEnd)

res = helpers.bulk(es, docs)
print("END")
