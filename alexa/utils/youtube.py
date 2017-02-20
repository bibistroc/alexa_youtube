import re
from alexa.utils.config import LocalConfig
from apiclient.discovery import build

config = LocalConfig()


class YoutubeVideoInformation:
    def __init__(self, video=None):
        if video is not None:
            self.__id = str(video['id']['videoId'])
            self.__title = video['snippet']['title']

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, val):
        self.__id = val

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, title):
        pattern = re.compile('[\W_]+')
        self.__title = pattern.sub(' ', title)

    @property
    def stream_url(self):
        return '%s/stream/%s.mp3' % (config.general['url'], self.id)

    def __str__(self):
        return self.title

    def __repr__(self):
        return self.__str__()

    def to_list(self):
        return {
            'id': self.id,
            'title': self.__str__()
        }


class Youtube:
    def __init__(self, items=None, session=None):
        if items is None:
            items = []
        self.__items = items
        self.__current = 0
        self.__y = None
        self.__session = session

    def to_list(self):
        item_list = []
        for item in self.__items:
            item_list.append(item.to_list())

        return item_list

    @property
    def current_index(self):
        return self.__current

    @property
    def __length(self):
        # TODO: maybe cache this value?
        return len(self.__items)

    def __rebuild(self):
        if self.__session is None or self.__length > 0:
            return

        for item in self.__session.attributes['playlist']:
            video = YoutubeVideoInformation()
            video.id = item.id
            video.title = item.title
            self.__items.append(video)

    def current(self):
        self.__rebuild()
        if self.__length == 0:
            return None

        return self.__items[self.__current]

    def next(self):
        self.__rebuild()
        self.__current += 1
        if self.__current >= self.__length:
            return None

        return self.current()

    def prev(self):
        self.__rebuild()
        self.__current -= 1
        if self.__current <= 0:
            return None

        return self.current()

    def clear(self):
        self.__items = []
        self.__current = 0
        self.__session = None

    @property
    def y(self):
        if self.__y is not None:
            return self.__y

        api_key = config.youtube['api_key']
        api_service_name = config.youtube['api_service_name']
        api_version = config.youtube['api_version']

        self.__y = build(api_service_name, api_version,
                         developerKey=api_key)

        return self.__y

    def save_session(self):
        if self.__session is not None:
            self.__session.attributes['playlist'] = self.to_list()
            self.__session.attributes['current'] = self.current_index

    def search(self, query):
        search_response = self.y.search().list(
            q=query,
            part="id,snippet",
            maxResults=1,
            type="video",
            fields="items(id(videoId),snippet(title))"
        ).execute()

        result_list = search_response.get("items", [])
        self.__items.append(YoutubeVideoInformation(result_list[0]))

        search_response = self.y.search().list(
            relatedToVideoId=self.current().id,
            part="id,snippet",
            maxResults=9,
            type="video",
            fields="items(id(videoId),snippet(title))"
        ).execute()

        result_list = search_response.get("items", [])
        for item in result_list:
            self.__items.append(YoutubeVideoInformation(item))








