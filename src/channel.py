import os
import json
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        # информация о канале
        self.channel_id = channel_id
        youtube_channels_list = self.get_service().channels().list(id=self.channel_id, part='snippet,statistics')
        self.__info_to_print = youtube_channels_list.execute()
        self.title = self.__info_to_print["items"][0]["snippet"]["title"]
        self.description = self.__info_to_print["items"][0]["snippet"]["description"]
        self.customUrl = f"https://www.youtube.com/{self.__info_to_print['items'][0]['snippet']['customUrl']}"
        self.subscriberCount = self.__info_to_print["items"][0]["statistics"]["subscriberCount"]
        self.videoCount = self.__info_to_print["items"][0]["statistics"]["videoCount"]
        self.viewCount = self.__info_to_print["items"][0]["statistics"]["viewCount"]

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.__info_to_print, indent=2, ensure_ascii=False))

    @classmethod
    def get_service(cls):
        api_key: str = os.getenv('YT_API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube

    # @classmethod
    # def instantiate_from_csv(cls, channel_id) -> None:
    #     """Возвращает объект для работы с YouTube API"""
    #     info_to_print = cls.__youtube.channels().list(id=channel_id, part='snippet,statistics').execute()
    #     title = info_to_print["items"][0]["snippet"]["title"]
    #     description = info_to_print["items"][0]["snippet"]["description"]
    #     customUrl = f"https://www.youtube.com/{info_to_print['items'][0]['snippet']['customUrl']}"
    #     subscriberCount = info_to_print["items"][0]["statistics"]["subscriberCount"]
    #     videoCount = info_to_print["items"][0]["statistics"]["videoCount"]
    #     viewCount = info_to_print["items"][0]["statistics"]["viewCount"]
    #     channel = cls(channel_id, title, description, customUrl, subscriberCount, videoCount, viewCount)
    #     return channel


vdud = Channel("UCMCgOm8GZkHp8zJ6l7_hIuA")
print(vdud.print_info())
