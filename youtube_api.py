import requests

YOUTUBE_API_KEY = "AIzaSyAv3sZNcE_2g7Fs37oeLHC_Q_9rJfDheWM" 

def search_youtube(query, max_results=5):
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "key": YOUTUBE_API_KEY,
        "q": query,
        "part": "snippet",
        "type": "video",
        "maxResults": max_results
    }
    res = requests.get(url, params=params).json()
    return [{
        "video_id": item["id"]["videoId"],
        "title": item["snippet"]["title"]
    } for item in res.get("items", [])]

def get_recommendations(video_id, max_results=5):
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "key": YOUTUBE_API_KEY,
        "relatedToVideoId": video_id,
        "part": "snippet",
        "type": "video",
        "maxResults": max_results
    }
    res = requests.get(url, params=params).json()
    return [{
        "video_id": item["id"]["videoId"],
        "title": item["snippet"]["title"]
    } for item in res.get("items", [])]
