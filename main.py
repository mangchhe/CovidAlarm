import requests # http 요청을 보내는 모듈
from time import sleep
import json # 효율적으로 데이터를 저장하고 교환하는데 사용하는 텍스트 데이터 포맷

''' REQUEST(https://developers.kakao.com/docs)
POST /v2/api/talk/memo/default/send HTTP/1.1
Host: kapi.kakao.com
Authorization: Bearer {access_token}
'''

#print(requests.get('https://www.naver.com').text) # HTML 코드
#print(requests.get('https://www.naver.com').status_code) # 응답 상태 코드
#- 직접 타이핑보다 딕셔너리 형태로 정리하고 파라미터로 전달해주는 것이 좋다.
#params = {'address':'부산광역시 사상구 엄궁동'}
#print(requests.get('https://8oi9s0nnth.apigw.ntruss.com/corona19-masks/v1/storesByAddr/json',params=params).url)
#requests.post(url, data=data)
#- 조금 더 복잡한 구조로 POST 요청을 해야할 때 딕셔너리 구조를 유지하면서 문자열로 바꿔서
#- 전달해야 하는데, 이때 json 모듈을 이용한다.
#request.post(url, data=json.dumps(data))
#- 별도의 헤더, 쿠키 옵션을 추가할 경우
#headers = {'Content-Type': 'application/json; charset=utf-8'}
#cookies = {'session_id': 'sorryidontcare'}
#requests.get(URL, headers=headers, cookies=cookies)


# config

url = 'https://8oi9s0nnth.apigw.ntruss.com/corona19-masks/v1/storesByAddr/json'
KAKAO_TOKEN = ""

def send_message(msg): # 카카오톡 메시지 보내기

    header = {"Authorization" : "Bearer " + KAKAO_TOKEN}
    url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
    post = {
        "object_type": "text",
        "text": msg,
        "link": {
            "web_url": "https://developers.kakao.com",
            "mobile_web_url": "https://developers.kakao.com"
        },
        "button_title": "바로 확인"
    }
    data = {"template_object" : json.dumps(post)}
    return requests.post(url, headers=header, data=data)

def get_mask_stock(adr): # 마스크 재고 확인

    global url
    stock_msg = ''
    params = {'address' : adr}

    json_obj = requests.get(url,params=params).json()

    for store in json_obj['stores']:
        if store['remain_stat']:
            stock_msg += store['name'] + ' ' + store['remain_stat'] + ' ' + store['stock_at'] + '\n'

    return stock_msg

if __name__ == '__main__':

    adr = input('알림 받고 싶은 지역명(예 : 부산광역시 사상구)')

    while True:
        send_message(get_mask_stock(adr))
        sleep(5)
