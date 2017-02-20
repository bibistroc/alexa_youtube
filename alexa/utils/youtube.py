import re
from alexa.utils.config import LocalConfig
from apiclient.discovery import build

config = LocalConfig()


class YoutubeVideoInformation:
    def __init__(self, video):
        pattern = re.compile('[\W_]+')
        self.id = str(video['id']['videoId'])
        self.title = pattern.sub(' ', video['snippet']['title'])
        self.thumb = video['snippet']['thumbnails']
        self._current = 0

    @property
    def stream_url(self):
        return '%s/stream/%s.mp3' % (config.general['url'], self.id)

    def __str__(self):
        return self.title

    def __repr__(self):
        return self.__str__()


class Youtube:
    def __init__(self):
        api_key = config.youtube['api_key']
        api_service_name = config.youtube['api_service_name']
        api_version = config.youtube['api_version']

        self._y = build(api_service_name, api_version,
                        developerKey=api_key)
        self._candidates = []
        self.found = False
        self.__current_index = 0

        self.__similar = []
        self.__similar_index = 0

    def clear(self):
        self._candidates = []
        self.found = False
        self.__current_index = 0

        self.__similar = []
        self.__similar_index = 0

    def current(self):
        return self._candidates[self.__current_index]

    def play_next(self):
        self.__similar_index += 1

        if len(self.__similar) == 0:
            self.__get_similar()
            self.__similar_index = 0

        if len(self.__similar) == self.__similar_index:
            last = self.__similar[self.__similar_index - 1]
            self.__get_similar(last.id)
            self.__similar_index = 0

        return self.__similar[self.__similar_index]

    def play_prev(self):
        self.__similar_index -= 1

        if self.__similar_index < 0 or len(self.__similar) == 0:
            return False

        return self.__similar[self.__similar_index]

    def __get_similar(self, video_id=False):
        limit = 10

        search_response = self._y.search().list(
            relatedToVideoId=video_id if video_id else self.current().id,
            part="id,snippet",
            maxResults=limit,
            type="video",
            fields="items(id(videoId),snippet(thumbnails,title))"
        ).execute()

        result_list = search_response.get("items", [])
        self.__similar = []
        for item in result_list:
            self.__similar.append(YoutubeVideoInformation(item))

    def search(self, query):
        limit = 1

        # https://developers.google.com/apis-explorer/?hl=en_US#p/youtube/v3/youtube.search.list
        search_response = self._y.search().list(
            q=query,
            part="id,snippet",
            maxResults=limit,
            type="video",
            fields="items(id(videoId),snippet(thumbnails,title))"
        ).execute()

        result_list = search_response.get("items", [])
        self._candidates = []
        for item in result_list:
            self._candidates.append(YoutubeVideoInformation(item))

        self.found = len(self._candidates) > 0
