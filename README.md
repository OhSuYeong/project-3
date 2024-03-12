## 구현 요소

1. 대시보드 만들기 es 에 내장된 데이터
2. 서울시 공공 와이파이 api —->es
    1. https://data.seoul.go.kr/ 에 가셔서 api 를 사용하기 위한 token 을 발급 받아야 한다.
    2. ‘서울시 공공와이파이 서비스’ 검색
    3. 앞선 실습에 기반하여 서울시에 있는 공공데이터 중 좌표가 있는 데이터를 선택하여 지도를 그리기
- 공공 데이터 오픈 api와 인증키는 미리 받음

---

## 구현 진행

1. **지도 위에 폴리곤을 그리기 위해 추가적인 시각화 도구를 사용할 수 있도록 구성**

```bash
sudo vi /etc/kibana/kibana.yml

# 가장 아래에 추가한다.
xpack.maps.showMapVisualizationTypes: true
```

- 이후 키바나 재실행

```bash
sudo systemctl restart kibana
```

2. **bulk로 전송하기**

```bash
pip install -U urllib3 requests
```

- 미리 elastic에서 DEV Console에서 인덱스 넣기

```bash
PUT seoulwifi
{
  "settings": {
    "analysis": {
      "analyzer": {
        "korean": {
          "tokenizer": "nori_tokenizer"
        }
      }
    }
  },
    "mappings":{
      "properties": {
        "gu_nm": {"type": "keyword"},
        "place_nm": {"type": "text", "analyzer": "korean"},
        "instl_xy": {"type": "geo_point"}
    }
  }
}
```

3. **필요한 각종 tool 설치**

```bash
apt install -y python3.8
apt install python3-pip
pip install -U urllib3 requests
pip install elasticsearch
```

4. **python 코드 작성**
5. **한글 분석기와 위경도 데이터 타입을 이용하기 위해**

```bash
/usr/share/elasticsearch/bin/elasticsearch-plugin install analysis-nori
```

6. 데이터가 제대로 들어온건지 체크

```bash
GET seoulwifi/_search

GET seoulwifi/_count
```

- 데이터가 들어왔는지 확인하고 제대로 원하는 데이터 개수만큼 들어왔는지 확인
![1 PNG](https://github.com/OhSuYeong/project-3/assets/101083171/0a73e5b2-5dad-4988-b5e9-6e2699a9dc2d)
![2 PNG](https://github.com/OhSuYeong/project-3/assets/101083171/1c691230-c632-4306-9df8-b295e2569d29)
**<결과>**
![3 PNG](https://github.com/OhSuYeong/project-3/assets/101083171/dcde0f10-c2d4-410e-beb2-a64009bd816f)
