import requests
import asyncio
import websockets
import json
import configparser
inifile = configparser.ConfigParser()
inifile.read('./config.ini', 'UTF-8')
#oauth = requests.get('https://slack.com/oauth/authorize')
#print(oauth.text)
token = inifile.get('settings', 'token')
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
                    if darray.pop(0).capitalize() == 'Your':
                        target = darray.pop(0)
                        if target == 'name':
                            if darray.pop(0) == 'is':
                                name = " ".join(darray)
                                r = requests.post('https://slack.com/api/users.profile.set', data={'token':token, 'name':'display_name', 'value':name})
                                print(r.text)
                        elif target == 'status':
                            if darray.pop(0) == 'is':
                                status = darray.pop(0)
                                r = requests.post('https://slack.com/api/users.profile.set', data={'token':token, 'name':'status_emoji', 'value':status})
                                print(r.text)
                        elif target == 'icon':
                            if darray.pop(0) == 'is':
                                icon = darray.pop(0)
                                print(icon.replace('<','').replace('>',''))
                                image = requests.get(icon.replace('<','').replace('>',''))
                                print(type(image.content))
                                r = requests.post('https://slack.com/api/users.setPhoto', data={'token':token}, files={'image':image.content})
                                print(r)
                                print(t.text)
                except:
                    continue

asyncio.get_event_loop().run_until_complete(hello())
requests.post('https://slack.com/api/users.profile.set', data={'token':token, 'name':'status_emoji', 'value':':old_noto_innocent:'})
print("slackbot died.")
