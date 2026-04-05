from youtube_transcript_api import YouTubeTranscriptApi
from langchain_core.tools import tool
import re

def extract_video_id(url: str) -> str:
    """
    Extracts the video ID from a YouTube URL.
    """
    # Quick regex for typical youtube URLs
    regex = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
    match = re.search(regex, url)
    if match:
        return match.group(1)
    return None

@tool
def youtube_transcript_tool(url: str) -> str:
    """
    Extracts the transcript from a YouTube video given its URL.
    """
    video_id = extract_video_id(url)
    if not video_id:
        return "Error: Invalid YouTube URL"
    
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_text = " ".join([t['text'] for t in transcript_list])
        return transcript_text
    except Exception as e:
        return f"Error retrieving transcript: {str(e)}"
