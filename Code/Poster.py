from datetime import datetime, timezone
from Code.Hydratable import Hydratable



class Poster(Hydratable):

    __slots__ = \
        (
            '__author_first_name',
            '__chat_start_time_utc',
            '__chat_end_time_utc',
            '__chat_detail_id',
            '__chat_sessions',
            '__session_start_time_utc',
            '__session_end_time_utc',
            '__video_sessions',
            '__in_person_start_time_utc',
            '__in_person_end_time_utc',
            '__in_person_sessions',
            '__id',
            '__title',
            '__poster_title',
            '__poster_authors',
            '__poster_institutes',
            '__author',
            '__author_surname',
            '__thumbnail',
            '__published',
            '__abstract_id',
            '__display_themes',
            '__author_institutes',
            '__notice',
            '__award_icon_name',
            '__metadata',
            '__author_title_prefix',
            '__theme',
            '__presenter',
            '__day',
            '__time'
        )

    class __Metadata(Hydratable):

        __slots__ = \
            (
                '__final_paper_number',
                '__person_affiliation',
                '__section',
                '__session_start_time_utc'
            )

        __UTC_TIMEZONE = timezone.utc
        __DATE_FORMAT = '%Y-%m-%dT%H:%M:%S.%f0Z'

        def __init__\
                (
                    self,
                    final_paper_number: str,
                    person_affiliation: str,
                    section: str = None,
                    session_start_time_utc: str = None
                ) -> None:
            super().__init__()
            self.__final_paper_number = str(final_paper_number)
            self.__person_affiliation = str(person_affiliation)
            self.__section = str(section)
            if session_start_time_utc is not None:
                start_date = datetime.strptime(str(session_start_time_utc), self.__DATE_FORMAT)
                self.__session_start_time_utc = start_date.replace(tzinfo=timezone.utc)
            else:
                self.__session_start_time_utc = None
            return


    def __init__\
            (
                self,
                id: str,
                title: str,
                authorfirstname: str,
                authorsurname: str,
                author: str,
                thumbnail: str,
                abstract_i_d: int,
                metadata: __Metadata,
                chatstarttimeutc: datetime = None,
                chatendtimeutc: datetime = None,
                chat_detail_id: str = None,
                chatsessions: str = None,
                sessionstarttimeutc: datetime = None,
                sessionendtimeutc: datetime = None,
                videosessions: str = None,
                inpersonstarttimeutc: datetime = None,
                inpersonendtimeutc: datetime = None,
                inpersonsessions: str = None,
                poster_title: str = '',
                poster_authors: str = '',
                poster_institutes: str = '',
                published: bool = False,
                display_theme: str = '',
                author_institutes: str = '',
                notice: str = '',
                award_icon_name: str = None,
                author_title_prefix: str = None,
                theme: str = None,
                presenter: str = None,
                day: str = None,
                time: str = None
            ) -> None:
        super().__init__()
        self.__author_first_name = authorfirstname
        self.__chat_start_time_utc = chatstarttimeutc
        self.__chat_end_time_utc = chatendtimeutc
        self.__chat_detail_id = chat_detail_id
        self.__chat_sessions = chatsessions
        self.__session_start_time_utc = sessionstarttimeutc
        self.__session_end_time_utc = sessionendtimeutc
        self.__video_sessions = videosessions
        self.__in_person_start_time_utc = inpersonstarttimeutc
        self.__in_person_end_time_utc = inpersonendtimeutc
        self.__in_person_sessions = inpersonsessions
        self.__id = int(id.replace('-', ''), 16)
        self.__title = title
        self.__poster_title = poster_title
        self.__poster_authors = poster_authors
        self.__poster_institutes = poster_institutes
        self.__author = author
        self.__author_surname = authorsurname
        self.__thumbnail = thumbnail
        self.__published = bool(published)
        try:
            self.__abstract_id = int(abstract_i_d)
        except ValueError:
            self.__abstract_id = None
        self.__display_themes = display_theme
        self.__author_institutes = author_institutes
        self.__notice = notice
        self.__award_icon_name = award_icon_name
        self.__metadata = metadata
        self.__author_title_prefix = author_title_prefix
        self.__theme = theme
        self.__presenter = presenter
        self.__day = day
        self.__time = time
        return


    @classmethod
    def hydrate(cls, data: dict):
        if data['metadata'] == dict():
            metadata_object = None
        else:
            metadata_dict = data['metadata']
            metadata_object = cls.__Metadata.hydrate(metadata_dict)
        data['metadata'] = metadata_object
        return super().hydrate(data)



    def __get_poster_id(self) -> str:
        as_hex = hex(self.__id)[2:].zfill(32).upper()
        return '-'.join([as_hex[i:i + 2] for i in range(0, len(as_hex), 2)])

    id = property(fget=__get_poster_id, doc=f"{__get_poster_id.__doc__}")

    def __get_title(self) -> str:
        return self.__title

    title = property(fget=__get_title, doc=f"{__get_title.__doc__}")
