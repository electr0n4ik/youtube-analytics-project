import os
import json
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        # информация о канале
        self.__channel_id = channel_id
        youtube_channels_list = self.get_service().channels().list(id=self.__channel_id, part='snippet,statistics')
        self.__info_to_print = youtube_channels_list.execute()
        self.title = self.__info_to_print["items"][0]["snippet"]["title"]
        self.description = self.__info_to_print["items"][0]["snippet"]["description"]
        self.url = f"https://www.youtube.com/{self.__info_to_print['items'][0]['snippet']['customUrl']}"
        self.subscriber_count: int = int(self.__info_to_print["items"][0]["statistics"]["subscriberCount"])
        self.video_count: int = self.__info_to_print["items"][0]["statistics"]["videoCount"]
        self.view_count: int = self.__info_to_print["items"][0]["statistics"]["viewCount"]

    @property
    def channel_id(self):
        return self.__channel_id

    def __str__(self):
        """Возвращает название и ссылку на канал по шаблону"""
        return f"{self.title} ({self.url})"

    def __add__(self, other):
        """Возвращает сумму подписчиков двух объектов"""
        return self.subscriber_count + other.subscriber_count

    def __sub__(self, other):
        """Возвращает разность подписчиков двух объектов"""
        return self.subscriber_count - other.subscriber_count

    def __eq__(self, other):
        """Для равенства =="""
        return self.subscriber_count == other.subscriber_count

    def __ne__(self, other):
        """Для неравенства !="""
        return self.subscriber_count != other.subscriber_count

    def __lt__(self, other):
        """Для оператора меньше <"""
        return self.subscriber_count < other.subscriber_count

    def __le__(self, other):
        """Для оператора меньше или равно <="""
        return self.subscriber_count <= other.subscriber_count

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.__info_to_print, indent=2, ensure_ascii=False))

    @classmethod
    def get_service(cls):
        """Возвращает объект для работы с YouTube API"""
        api_key: str = os.getenv('YT_API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube

    def to_json(self, filename):
        """Сохраняет значения атрибутов экземпляра Channel в файл в формате JSON."""
        channel = {
            'channel_id': self.__channel_id,
            'title': self.title,
            'description': self.description,
            'customUrl': self.url,
            'subscriberCount': self.subscriber_count,
            'videoCount': self.video_count,
            'viewCount': self.view_count
        }
        with open(filename, "w", encoding="UTF-8") as file:
            json.dump(channel, file, ensure_ascii=False)

    # @classmethod
    # def instantiate_from_channel_id(cls, channel_id) -> None:
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
