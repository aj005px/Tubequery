from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs

def get_vid_id(url):
    parsed = urlparse(url)
    return parse_qs(parsed.query).get("v", [None])[0]

def get_transcript(vid):
    api = YouTubeTranscriptApi()
    transcript_list = api.list(vid)

    try:
        # Try English first
        transcript = transcript_list.find_transcript(["en"])
    except:
        try:
            # Try English translation
            transcript = transcript_list.find_generated_transcript(
                [t.language_code for t in transcript_list]
            )
            transcript = transcript.translate("en")
        except:
            # Just grab whatever language is available as-is
            transcript = transcript_list.find_generated_transcript(
                [t.language_code for t in transcript_list]
            )

    return transcript.fetch()

vid = get_vid_id(input("Enter a youtube link: "))
transcript = get_transcript(vid)

texts = []
for line in transcript:
    texts.append(line.text)

vid_joined = " ".join(texts)

with open("youtube_transcripts.txt", "w", encoding="utf-8") as f:
    f.write(f"VIDEO ID: {vid}\n\n")
    f.write(vid_joined)
