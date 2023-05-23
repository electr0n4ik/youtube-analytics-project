import isodate

from src.video import PLVideo


class PlayList(PLVideo):
    list_res = []

    def __init__(self, playlist_id):
        """Экземпляр инициализирует id плейлиста. Дальше все данные будут подтягиваться по API."""
        self.playlist_id = playlist_id
        # Достаем информацию по самому плейлисту
        self.playlist_videos = self.get_service().playlists().list(id=playlist_id,
                                                                   part='snippet',
                                                                   maxResults=50,
                                                                   ).execute()
        # Инициализируем дополнительный атрибут
        self.title = self.playlist_videos['items'][0]['snippet']['title']
        self.url = f"https://www.youtube.com/playlist?list={playlist_id}"

    @property
    def get_video_response(self):
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in super().playlist_response()['items']]
        video_response = self.get_service().videos().list(part='contentDetails,statistics',
                                                          id=','.join(video_ids)
                                                          ).execute()
        return video_response

    @property
    def total_seconds(self):

        duration = []
        result = 0
        for video in self.get_video_response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration.append(iso_8601_duration)

        for i in duration:
            m1, m2 = int(i[2]), int(i[3])  # вытаскиваем из строки минуты и преобразуем в int для операций
            s1, s2 = int(i[5]), int(i[6])  # секунды
            # общее количество секунд в плейлисте
            result += (m1 * 600) + m2 + (s1 * 10) + s2
        return result

    @property
    def total_duration(self):
        duration = isodate.parse_duration("PT0S")
        for video in self.get_video_response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration += isodate.parse_duration(iso_8601_duration)

        return duration

    def show_best_video(self):
        like_count = 0
        id_vid = ""
        # return self.printj(self.get_video_response)
        for i in self.get_video_response["items"]:
            likes = i["statistics"]["likeCount"]
            if like_count < int(likes):
                like_count = int(likes)
                id_vid = i["id"]

        return f"https://youtu.be/{id_vid}"
