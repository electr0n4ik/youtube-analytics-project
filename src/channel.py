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
        self.channel_id = channel_id

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        info_to_print = self.__youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()

        print(json.dumps(info_to_print, indent=2, ensure_ascii=False))
