from googleapiclient.discovery import build
import re
from datetime import timedelta
from config import *

yt=build('youtube','v3',developerKey=apiKey)

minutesPattern= re.compile(r'(\d+)M')
secondsPattern= re.compile(r'(\d+)S')
hoursPattern= re.compile(r'(\d+)H')

playlistDuration=0

nextPageToken=None
while True:
    playlistRequest= yt.playlistItems().list(part='contentDetails',
                                            playlistId=playlist,
                                            maxResults=50,
                                            pageToken=nextPageToken)
    
    playlistResponse= playlistRequest.execute()

    vidIds=[]
    for item in playlistResponse['items']:
        vidIds.append(item['contentDetails']['videoId'])

    vidRequest= yt.videos().list(part='contentDetails', id=','.join(vidIds))
    vidResponse= vidRequest.execute()

    durationList=[]
    for item in vidResponse['items']:
        durationList.append(item['contentDetails']['duration'])

    for item in durationList:
        hours=hoursPattern.search(item)
        minutes=minutesPattern.search(item)
        seconds=secondsPattern.search(item)

        hours=int(hours.group(1)) if hours else 0
        minutes=int(minutes.group(1)) if minutes else 0
        seconds=int(seconds.group(1)) if seconds else 0

        videoSeconds= timedelta(hours=hours, minutes=minutes, seconds=seconds).total_seconds()
        playlistDuration+=videoSeconds


    nextPageToken=playlistResponse.get('nextPageToken')
    if not nextPageToken:
        break

playlistDuration=int(playlistDuration)

minutes, seconds = divmod(playlistDuration,60)
hours, minutes = divmod(minutes,60)

print(f"{hours}h {minutes}m {seconds}s")

