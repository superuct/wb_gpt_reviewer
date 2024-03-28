import requests
import json
import os

# curl -X 'POST' \
#   'https://xxx/v1/chat/completions' \
#   -H 'accept: application/json' \
#   -H 'Authorization: ' \
#   -H 'Content-Type: application/json' \
#   -d '{
#   "channelId": "12199477xxxxxxxx",
#   "messages": [
#     {
#       "content": "下午好",
#       "role": "user"
#     }
#   ],
#   "model": "gpt-4",
#   "stream": false
# }'

headers = {
    "accept": "application/json",
    "Authorization": "",
    "Content-Type": "application/json"
}
data = {
    "channelId": "",
    "messages": [
        {
            "content": "下午好",
            "role": "user"
        }
    ],
    "model": "gpt-4",
    "stream": False
}

def ask_openai(question):
    url = os.environ.get('OPENAI_URL')
    headers['Authorization'] = os.environ.get('OPENAI_AUTH')
    data['channelId'] = os.environ.get('DISCORD_CHANNEL')
    if len(question) == 0:
        data["messages"][0]["content"] = "给我说一句积极向上的话吧。例如：长风破浪会有时，直挂云帆济沧海。"
    else:
        data["messages"][0]["content"] = question
        data["messages"][0]["role"] = "你是一位擅长发表犀利评论的微博杠精，掌握着锐利且辛辣的吐槽技巧。例如，输入：java 是世界上最好的语言。输出：创始人头发都没有了，还是最好的语言？"
    response = requests.post(url, headers=headers, data=json.dumps(data),timeout=1800)

    if response.status_code == 200:
        response_json = response.json()
        return response_json.get("choices")[0].get("message").get("content")
    else:
        print("Error:", response.text)
        return None