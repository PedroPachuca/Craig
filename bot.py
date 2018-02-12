from bs4 import BeautifulSoup as bs4
import requests
from slackclient import SlackClient
import time

slack_client = SlackClient('slackbot token')

def craigslist():
    url_base = ('https://sfbay.craigslist.org/search/sss') #Rewrite based on your location in form https://{carigslistlocid}.craigslist.org/search/sss
    params = dict(query=keyword, sort='date')
    rsp = requests.get(url_base, params=params)
    html = bs4(rsp.text, 'html.parser')
    results = []
    results = html.find_all('p', attrs={'class': 'result-info'})
    for s in results:
        price = s.find('span', attrs={'class': 'result-price'})
        if price == None:
            price = 'unknown'
        else:
            price = str(price.text)
        date = s.find('time', attrs={'class': 'result-date'})
        date = date.text
        link = s.find('a', attrs={'class': 'result-title'})
        text = link.text
        link = link.get('href')
        link = str("\n"+link)
        desc = text+"\n"+price+", "+date+link
        slack_client.api_call(
                'chat.postMessage',
                channel=channel,
                text=desc,
                as_user='true:')

if slack_client.rtm_connect():
    while True:
        events = slack_client.rtm_read()
        for event in events:
            if (
                'channel' in event and
                'text' in event and
                event.get('type') == 'message'
            ):
                channel = event['channel']
                text = event['text']
                if 'Craigslist Bot:' in text:
                    print(text)
                    keyword = text.replace("Craigslist Bot:","")
                    craigslist()
                    time.sleep(2)
else:
    print('Connection failed, confirm token')
