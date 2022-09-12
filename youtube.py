# Install dependencies  
from requests_html import HTMLSession   
from bs4 import BeautifulSoup as bs # importing BeautifulSoup  
import re  
import json as json  
# copy youtube url from YouTube website  
video_url = "https://youtu.be/u4N45v8f7cY"  
  
# init an HTML Session  
session = HTMLSession()  
  
def extract_video_informations(url):  
    # It will download HTML code  
    resp = session.get(url)  
    # execute Javascript  
    resp.html.render(timeout=60)  
    # create beautiful soup object to parse HTML  
    soup = bs(resp.html.html, "html.parser")  
    # initialize the result dictionary to store data  
    result = {}  
  
    result["title"] = soup.find("meta", itemprop="name")['content']  
    result["views"] = soup.find("meta",itemprop="interactionCount")['content']  
    result["description"] = soup.find("meta",itemprop="description")['content']  
  
    result["date_published"] = soup.find("meta", itemprop="datePublished")['content']  
  
    result["duration"] = soup.find("span", {"class": "ytp-time-duration"}).text  
    result["tags"] = ', '.join([ meta.attrs.get("content") for meta in soup.find_all("meta", {"property": "og:video:tag"}) ])  
  
    data = re.search(r"var ytInitialData = ({.*?});", soup.prettify()).group(1)  
    data_json = json.loads(data)  
    videoPrimaryInfoRenderer = data_json['contents']['twoColumnWatchNextResults']['results']['results']['contents'][0]['videoPrimaryInfoRenderer']  
    videoSecondaryInfoRenderer = data_json['contents']['twoColumnWatchNextResults']['results']['results']['contents'][1]['videoSecondaryInfoRenderer']  
    # number of likes  
    likes_label = videoPrimaryInfoRenderer['videoActions']['menuRenderer']['topLevelButtons'][0]['toggleButtonRenderer']['defaultText']['accessibility']['accessibilityData']['label'] # "No likes" or "###,### likes"  
    likes_str = likes_label.split(' ')[0].replace(',','')  
    result["likes"] = '0' if likes_str == 'No' else likes_str  
  
    channel_tag = soup.find("meta", itemprop="channelId")['content']  
    # channel name  
    channel_name = soup.find("span", itemprop="author").next.next['content']  
    
    channel_url = f"https://www.youtube.com/{channel_tag}"  
    # number of subscribers as str  
    channel_subscribers = videoSecondaryInfoRenderer['owner']['videoOwnerRenderer']['subscriberCountText']['accessibility']['accessibilityData']['label']  
  
    result['channel'] = {'name': channel_name, 'url': channel_url, 'subscribers': channel_subscribers}  
    return result  
  
print(extract_video_informations(video_url))  
