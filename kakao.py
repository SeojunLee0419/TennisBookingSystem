import json
import requests
# https://foss4g.tistory.com/1636


def refresh_token():
    url = "https://kauth.kakao.com/oauth/token"
    data = {
        "grant_type": "refresh_token",
        "client_id": "341330418c6907893cd0b7d2ac2e1ad9",
        "refresh_token": "wcrtR-iwsu2qmS1Se07xMoTlTG80Vc5obOIKKw0gAAABi_0w3--IenTzhLqDRQ"
    }
    response = requests.post(url, data=data)
    tokens = response.json()

    print(tokens)
    return tokens['access_token']


def send_kakao_talk(message):
    access_token = refresh_token()
    url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
    header = {"Authorization": 'Bearer ' + access_token}
    data = {
        "template_object": json.dumps({
            "object_type": "text",
            "text": message,
            "link": {
                "web_url": "https://www.google.co.kr/search?q=deep+learning&source=lnms&tbm=nws",
                "mobile_web_url": "https://www.google.co.kr/search?q=deep+learning&source=lnms&tbm=nws"
            },
            "button_title": "NYTC Courts"
        })
    }

    response = requests.post(url, headers=header, data=data)
    print(response.status_code)


def kakao_friends_list():
    access_token = refresh_token()
    header = {"Authorization": 'Bearer ' + access_token}
    url = "https://kapi.kakao.com/v1/api/talk/friends"

    response = requests.get(url, headers=header)
    print(response)

    # result = json.loads(requests.get(url, headers=header).text)
    #
    # friends_list = result.get("elements")
    # friends_id = []
    #
    # print(requests.get(url, headers=header).text)
    # print(friends_list)
    #
    # for friend in friends_list:
    #     friends_id.append(str(friend.get("uuid")))
    #
    #     return friends_id


if __name__ == "__main__":
    # https://kauth.kakao.com/oauth/authorize?client_id=341330418c6907893cd0b7d2ac2e1ad9&redirect_uri=https://localhost:3000&response_type=code&scope=talk_message,friends
    # it will return the code(after login to kakaotalk)

    # url = "https://kauth.kakao.com/oauth/token"
    # data = {
    #     "grant_type" : "authorization_code",
    #     "client_id" : "341330418c6907893cd0b7d2ac2e1ad9",
    #     "redirect_url" : "https://localhost:3000",
    #     "code" : "N6wuo7ArizYT6-a6o2nBSO79KGDUv7xaMSGlO-9ZM7CTNxKQKzYr7kBCnUEKKiUQAAABi_0upeDSDh85zpcCzQ"
    # }
    # response = requests.post(url, data=data)
    # tokens = response.json()
    # print(tokens)

    # {'access_token': 'NSSosu7O9B75CqJxRzHDrnq-sQoDPx9bO-EKKw0gAAABi_0w3_KIenTzhLqDRQ',
    #  'token_type': 'bearer',
    #  'refresh_token': 'wcrtR-iwsu2qmS1Se07xMoTlTG80Vc5obOIKKw0gAAABi_0w3--IenTzhLqDRQ',
    #  'expires_in': 21599,
    #  'scope': 'talk_message friends',
    #  'refresh_token_expires_in': 5183999}

    send_kakao_talk("Hello, kakao")
    # kakao_friends_list()


# https://kauth.kakao.com/oauth/authorize?client_id=341330418c6907893cd0b7d2ac2e1ad9&redirect_uri=https://localhost:3000&response_type=code&scope=talk_message,friends
# https://localhost:3000/?code=N6wuo7ArizYT6-a6o2nBSO79KGDUv7xaMSGlO-9ZM7CTNxKQKzYr7kBCnUEKKiUQAAABi_0upeDSDh85zpcCzQ


# url = "https://kauth.kakao.com/oauth/token"
# data = {
#     "grant_type" : "authorization_code",
#     "client_id" : "341330418c6907893cd0b7d2ac2e1ad9",
#     "redirect_url" : "https://localhost:3000",
#     "code" : "N6wuo7ArizYT6-a6o2nBSO79KGDUv7xaMSGlO-9ZM7CTNxKQKzYr7kBCnUEKKiUQAAABi_0upeDSDh85zpcCzQ"
# }
# response = requests.post(url, data=data)
# tokens = response.json()
# {'access_token': 'Hi_bk22AdNJzKBPhULoqJYPBzcqfl9ytP1wKPXUaAAABiztqafSIenTzhLqDRQ', 'token_type': 'bearer', 'refresh_token': 'qcvJ-ICKNlQLyH7Vd2ov9cHk7PeKgH2z708KPXUaAAABiztqafKIenTzhLqDRQ', 'expires_in': 21599, 'scope': 'talk_message friends', 'refresh_token_expires_in': 5183999}

# access_token='Hi_bk22AdNJzKBPhULoqJYPBzcqfl9ytP1wKPXUaAAABiztqafSIenTzhLqDRQ'
# # print(access_token)
#
#
# url= "https://kapi.kakao.com/v2/api/talk/memo/default/send"
# header = {"Authorization": 'Bearer ' + access_token}
# data={
#     "template_object": json.dumps({
#         "object_type":"text",
#         "text":"딥러닝 뉴스",
#         "link":{
#             "web_url" : "https://www.google.co.kr/search?q=deep+learning&source=lnms&tbm=nws",
#             "mobile_web_url" : "https://www.google.co.kr/search?q=deep+learning&source=lnms&tbm=nws"
#         },
#         "button_title": "뉴스 보기"
#     })
# }
# response = requests.post(url, headers=header, data=data)
# print(response.status_code)


#
# curl -v -X POST "https://kauth.kakao.com/oauth/token" \
#  -H "Content-Type: application/x-www-form-urlencoded" \
#  -d "grant_type=authorization_code" \
#  -d "client_id=341330418c6907893cd0b7d2ac2e1ad9" \
#  --data-urlencode "redirect_uri=http://127.0.0.1:9000/kakaocallback" \
#  -d "code=_xcEbVPeNQ0_qhAkgyEOIEaJMRx4oVXcNvyETN4SYFTcDvrfnL8i7_-nDmcKPXTaAAABizcfMpz-oZq-Jypvmw"

# {
#     "access_token": "YytfUT46aW48W2RnV2tfaxCXKJqvOeedlP0KPXKYAAABizcGDGiIenTzhLqDRQ",
#     "token_type" : "bearer",
#     "refresh_token" : "nce5vPR1xQssNDM8GSeg27wlijO_ac6xNCEKPXKYAAABizcGDGaIenTzhLqDRQ",
#     "expires_in" : 21599,
#     "refresh_token_expires_in" : 5183999
# }

# curl -v -X POST "https://kapi.kakao.com/v2/api/talk/memo/default/send" \
#     -H "Content-Type: application/x-www-form-urlencoded" \
#     -H "Authorization: Bearer Hi_bk22AdNJzKBPhULoqJYPBzcqfl9ytP1wKPXUaAAABiztqafSIenTzhLqDRQ" \
#     --data-urlencode 'template_object={
#         "object_type": "text",
#         "text": "텍스트 영역입니다. 최대 200자 표시 가능합니다.",
#         "link": {
#             "web_url": "https://developers.kakao.com",
#             "mobile_web_url": "https://developers.kakao.com"
#         },
#         "button_title": "바로 확인"
#     }'
#
