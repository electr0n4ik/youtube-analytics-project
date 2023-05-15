import os
import json
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""
    __api_key: str = os.getenv('YT_API_KEY')
    # специальный объект для работы с API
    __youtube = build('youtube', 'v3', developerKey=__api_key)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        # информация о канале
        self.channel_id = channel_id
        self.__info_to_print = self.__youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        self.title = self.__info_to_print["items"][0]["snippet"]["title"]
        self.description = self.__info_to_print["items"][0]["snippet"]["description"]
        self.customUrl = f"https://www.youtube.com/{self.__info_to_print['items'][0]['snippet']['customUrl']}"
        self.subscriberCount = self.__info_to_print["items"][0]["statistics"]["subscriberCount"]
        self.videoCount = self.__info_to_print["items"][0]["statistics"]["videoCount"]
        self.viewCount = self.__info_to_print["items"][0]["statistics"]["viewCount"]

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.__info_to_print, indent=2, ensure_ascii=False))


vdud = Channel('UCMCgOm8GZkHp8zJ6l7_hIuA')

print(vdud.title)
