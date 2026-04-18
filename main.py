from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs

def get_vid_id(url):
    parsed = urlparse(url)
    return parse_qs(parsed.query).get("v", [None])[0]# the video id is stored in query where it has a key of 'v'

vid = get_vid_id(input("Enter a youtube link: "))

transcript = YouTubeTranscriptApi().fetch(vid)

texts = []

for line in transcript:
    texts.append(line.text) # 'text' key contains spoken words

vid_joined = " ".join(texts)

print(vid_joined)
