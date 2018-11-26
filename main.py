import requests
import asyncio
import websockets
import json
#oauth = requests.get('https://slack.com/oauth/authorize')
#print(oauth.text)
token = 'xoxp-3069876617-4312379481-121065493056-9b64cb023821685f1379a866b39e5086'
headers = {'accept': 'application/x-www-form-urlencoded'}
r = requests.get('https://slack.com/api/rtm.connect', headers=headers, params={'token': token})
wss = r.json()['url']
async def hello():
    async with websockets.connect(wss) as websocket:
        while True:
            event = await websocket.recv()
            d = json.loads(event)
            if d['type'] == 'message':
                try:
                    darray = d['text'].split()
                    print(darray)
                    if darray.pop(0).capitalize() == 'Your':
                        target = darray.pop(0)
                        if target == 'name':
                            if darray.pop(0) == 'is':
                                name = " ".join(darray)
                                r = requests.post('https://slack.com/api/users.profile.set', data={'token':token, 'name':'display_name', 'value':name})
                                print(r)
                        elif target == 'status':
                            if darray.pop(0) == 'is':
                                status = darray.pop(0)
                                r = requests.post('https://slack.com/api/users.profile.set', data={'token':token, 'name':'status_emoji', 'value':status})
                                print(r)
                except:
                    continue

asyncio.get_event_loop().run_until_complete(hello())
