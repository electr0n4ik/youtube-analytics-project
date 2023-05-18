import os
import json
from googleapiclient.discovery import build


class Video:

    def __init__(self, id_video):
        self.id_video = id_video
        video_response = self.get_service().videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                          id=id_video
                                                          ).execute()
        self.title: str = video_response['items'][0]['snippet']['title']
        self.url = f"https://www.youtube.com/watch?v={id_video}"
        self.view_count: int = video_response['items'][0]['statistics']['viewCount']
        self.like_count: int = video_response['items'][0]['statistics']['likeCount']

    def __str__(self):
        return self.title

    @classmethod
    def get_service(cls):
        """Возвращает объект для работы с YouTube API"""
        api_key: str = os.getenv('YT_API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube


class PLVideo(Video):

    def __init__(self, id_video, playlist_id):
        self.playlist_id = playlist_id
        playlist_videos = self.get_service().playlistItems().list(part='contentDetails',
                                                                  maxResults=50,
                                                                  playlistId=playlist_id
                                                                  ).execute()
        for i in playlist_videos["items"]:
            if i["contentDetails"]["videoId"] == id_video:
                super().__init__(id_video)
