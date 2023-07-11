from googleapiclient.discovery import build
import re
from datetime import timedelta
apiKey="AIzaSyAg0YIDv59IDSqG_1SDpuMkvFd83yZNKuE"
playlist="https://www.youtube.com/playlist?list=PLrDd_kMiAuNmSb-CKWQqq9oBFN_KNMTaI"
yt=build('youtube','v3',developerKey=apiKey)

request= yt.playlistItems().list(part='contentDetails', playlistId="PLrDd_kMiAuNmSb-CKWQqq9oBFN_KNMTaI")

response= request.execute()
vidId=[]
for item in response['items']:
    vidId.append(item['contentDetails']['videoId'])


vidRequest= yt.videos().list(part='contentDetails', id=','.join(vidId))

vidResponse= vidRequest.execute()
durationList=[]
for item in vidResponse['items']:
    durationList.append(item['contentDetails']['duration'])

minutesPattern= re.compile(r'(\d+)M')
secondsPattern= re.compile(r'(\d+)S')
hoursPattern= re.compile(r'(\d+)H')
for item in durationList:
    hours=hoursPattern.search(item)
    minutes=minutesPattern.search(item)
    seconds=secondsPattern.search(item)
    hours=int(hours.group(1)) if hours else 0
    minutes=int(minutes.group(1)) if minutes else 0
    seconds=int(seconds.group(1)) if seconds else 0

    videoSeconds= timedelta(hours=hours, minutes=minutes, seconds=seconds).total_seconds
    
