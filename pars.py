import vk_api
import json
import requests
from vkstreaming import Streaming

app_vkid = 6712606
servise_token = "64da4c8064da4c8064da4c803464bc219e664da64da4c803f6dc6be3497baa33cf902f8"

session = vk_api.VkApi(token=servise_token, api_version="5.85", app_id=app_vkid)
vk = session.get_api()
respone = vk.streaming.getServerUrl()

streamingAPI = Streaming(respone["endpoint"], respone["key"])
streamingAPI.del_all_rules()
rules = streamingAPI.get_rules()
streamingAPI.add_rules("1", "мегафон")


@streamingAPI.stream
def my_func(event):

    event_type = event["event_type"]
    print("event type:: ", event_type)

    if event_type == 'comment' or event_type == 'post':

        author = event['author']
        author_url = author['author_url']
        if author['author_url'][15:17] == "id":
            person = list(vk.users.get(user_ids=author['id'], fields='verified'))
            print(person)
            name = dict(person[0])
        else:
            club = vk.groups.getById(group_id=str(author['id'])[1:])
            print(club)

        text = event['text']
        text = text('<br>', '')

        post = {
            'SClientId': author['author_url'],
            'Message': event['event_url'],
            'Comment': text,
            'FirstName': name['first_name'],
            'Surname': name['last_name'],
            'Verification': bool(name['verified'])
        }

        req = requests.post("http://10.241.103.127:5000/api/clientinfos", json=post)
        print(req.status_code)


streamingAPI.start()
