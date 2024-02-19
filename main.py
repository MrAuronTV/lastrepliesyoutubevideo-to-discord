#Coded by Eddie's Tech (eddiestech.co.uk) - Adapted from YouTube API example
import os
import pickle
import requests
import json
import time
from urllib import request
from urllib.error import HTTPError
from json import loads

PATH = '/PATH/TO/SCRIPT' #Path where you stock stream id for doesnt spam discord
WEBHOOK = "WEBHOOK_URL" #webhook url discord
CHANNEL_ID = 'CHANNEL_ID'
API_KEY = 'YOUR_API_KEY'

try:
    id = pickle.load(open("{}/lastrepliescomment".format(PATH), "rb"))

except (OSError, IOError) as e:
    foo = 3
    pickle.dump(foo, open("{}/lastrepliescomment".format(PATH), "wb"))

API_ENDPOINT = 'https://youtube.googleapis.com/youtube/v3/commentThreads?part=replies&allThreadsRelatedToChannelId={0}&moderationStatus=published&order=time&textFormat=plainText&key={1}&maxResults=1'.format(CHANNEL_ID,API_KEY)
r = requests.get(url = API_ENDPOINT)

GETLASTREPLIES = loads(r.text)['items'][0]['replies']['comments'] #GET ALL REPLIES FROM LAST COMMENT
GETLASTREPLIES.reverse() #REVERSE
LASTREPLIES = GETLASTREPLIES[0]['snippet']['textDisplay'] #LAST REPLIES FROM CHANNEL
VIDEOID = GETLASTREPLIES[0]['snippet']['videoId']  #VIDEOID FROM LAST REPLIES
AUTHOR = GETLASTREPLIES[0]['snippet']['authorDisplayName']  #USER FROM LAST REPLIES
PUBLISH = GETLASTREPLIES[0]['snippet']['publishedAt']  #DATE LAST REPLIES
COMMENTID = GETLASTREPLIES[0]['id'] #COMMENT ID FROM LAST REPLIES

# La payload
payload = {
    'username':"USERNAME",
    'avatar_url':"AVATAR_URL",
    'embeds': [
        {
            'title': LASTREPLIES,
            'url': 'https://www.youtube.com/watch?v={0}&lc={1}&feature=em-comments'.format(VIDEOID,COMMENTID),
            "color": 16711680,
            'author': {'name': AUTHOR},
            'timestamp': PUBLISH,
        },
    ]
}


#REQUEST SETTINGS
headers = {
    'Content-Type': 'application/json',
    'user-agent': 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11'
}

req = request.Request(url=WEBHOOK,
                      data=json.dumps(payload).encode('utf-8'),
                      headers=headers,
                      method='POST')

if COMMENTID:
    if COMMENTID != id :
       response = request.urlopen(req)
with open('{}/lastrepliescomment'.format(PATH), 'wb') as f:
    pickle.dump(COMMENTID, f)
