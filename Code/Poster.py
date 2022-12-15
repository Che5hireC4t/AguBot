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
        
        

    #   ██████╗ ██████╗  ██████╗ ██████╗ ███████╗██████╗ ████████╗██╗███████╗███████╗
    #   ██╔══██╗██╔══██╗██╔═══██╗██╔══██╗██╔════╝██╔══██╗╚══██╔══╝██║██╔════╝██╔════╝
    #   ██████╔╝██████╔╝██║   ██║██████╔╝█████╗  ██████╔╝   ██║   ██║█████╗  ███████╗
    #   ██╔═══╝ ██╔══██╗██║   ██║██╔═══╝ ██╔══╝  ██╔══██╗   ██║   ██║██╔══╝  ╚════██║
    #   ██║     ██║  ██║╚██████╔╝██║     ███████╗██║  ██║   ██║   ██║███████╗███████║
    #   ╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚══════╝╚═╝  ╚═╝   ╚═╝   ╚═╝╚══════╝╚══════╝

        def __get_session_start_time_utc(self):
            return self.__session_start_time_utc

        session_start_time_utc = property\
            (
                fget=__get_session_start_time_utc,
                doc=f"{__get_session_start_time_utc.__doc__}"
            )
    # ------------------------------------------------------------------------------------------------------------------

        def __get_section(self) -> str:
            return self.__section

        section = property(fget=__get_section, doc=f"{__get_section.__doc__}")
    # ------------------------------------------------------------------------------------------------------------------

        def __get_final_paper_number(self) -> str:
            return self.__final_paper_number

        final_paper_number = property(fget=__get_final_paper_number, doc=f"{__get_final_paper_number.__doc__}")
    # ------------------------------------------------------------------------------------------------------------------

        def __get_person_affiliation(self) -> str:
            return self.__person_affiliation

        person_affiliation = property(fget=__get_person_affiliation, doc=f"{__get_person_affiliation.__doc__}")
    # ------------------------------------------------------------------------------------------------------------------
    
    
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




#   ██████╗ ██████╗  ██████╗ ██████╗ ███████╗██████╗ ████████╗██╗███████╗███████╗
#   ██╔══██╗██╔══██╗██╔═══██╗██╔══██╗██╔════╝██╔══██╗╚══██╔══╝██║██╔════╝██╔════╝
#   ██████╔╝██████╔╝██║   ██║██████╔╝█████╗  ██████╔╝   ██║   ██║█████╗  ███████╗
#   ██╔═══╝ ██╔══██╗██║   ██║██╔═══╝ ██╔══╝  ██╔══██╗   ██║   ██║██╔══╝  ╚════██║
#   ██║     ██║  ██║╚██████╔╝██║     ███████╗██║  ██║   ██║   ██║███████╗███████║
#   ╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚══════╝╚═╝  ╚═╝   ╚═╝   ╚═╝╚══════╝╚══════╝

    def __get_poster_id(self) -> str:
        as_hex = hex(self.__id)[2:].zfill(32).upper()
        return '-'.join([as_hex[i:i + 2] for i in range(0, len(as_hex), 2)])

    id = property(fget=__get_poster_id, doc=f"{__get_poster_id.__doc__}")
# ----------------------------------------------------------------------------------------------------------------------

    def __get_title(self) -> str:
        return self.__title

    title = property(fget=__get_title, doc=f"{__get_title.__doc__}")
# ----------------------------------------------------------------------------------------------------------------------

    def __get_author_first_name(self) -> str:
        return self.__author_first_name

    author_first_name = property(fget=__get_author_first_name, doc=f"{__get_author_first_name.__doc__}")
# ----------------------------------------------------------------------------------------------------------------------

    def __get_chat_start_time_utc(self) -> datetime:
        return self.__chat_start_time_utc

    chat_start_time_utc = property(fget=__get_chat_start_time_utc, doc=f"{__get_chat_start_time_utc.__doc__}")
# ----------------------------------------------------------------------------------------------------------------------

    def __get_chat_end_time_utc(self) -> datetime:
        return self.__chat_end_time_utc

    chat_end_time_utc = property(fget=__get_chat_end_time_utc, doc=f"{__get_chat_end_time_utc.__doc__}")
# ----------------------------------------------------------------------------------------------------------------------

    def __get_chat_detail_id(self) -> str:
        return self.__chat_detail_id

    chat_detail_id = property(fget=__get_chat_detail_id, doc=f"{__get_chat_detail_id.__doc__}")
# ----------------------------------------------------------------------------------------------------------------------

    def __get_chat_sessions(self) -> str:
        return self.__chat_sessions

    chat_sessions = property(fget=__get_chat_sessions, doc=f"{__get_chat_sessions.__doc__}")
# ----------------------------------------------------------------------------------------------------------------------

    def __get_session_start_time_utc(self) -> datetime:
        return self.__session_start_time_utc

    session_start_time_utc = property(fget=__get_session_start_time_utc, doc=f"{__get_session_start_time_utc.__doc__}")
# ----------------------------------------------------------------------------------------------------------------------

    def __get_session_end_time_utc(self) -> datetime:
        return self.__session_end_time_utc

    session_end_time_utc = property(fget=__get_session_end_time_utc, doc=f"{__get_session_end_time_utc.__doc__}")
# ----------------------------------------------------------------------------------------------------------------------

    def __get_video_sessions(self) -> str:
        return self.__video_sessions

    video_sessions = property(fget=__get_video_sessions, doc=f"{__get_video_sessions.__doc__}")
# ----------------------------------------------------------------------------------------------------------------------

    def __get_in_person_start_time_utc(self) -> datetime:
        return self.__in_person_start_time_utc

    in_person_start_time_utc = property\
        (
            fget=__get_in_person_start_time_utc,
            doc=f"{__get_in_person_start_time_utc.__doc__}"
        )
# ----------------------------------------------------------------------------------------------------------------------

    def __get_in_person_end_time_utc(self) -> datetime:
        return self.__in_person_end_time_utc

    in_person_end_time_utc = property(fget=__get_in_person_end_time_utc, doc=f"{__get_in_person_end_time_utc.__doc__}")
# ----------------------------------------------------------------------------------------------------------------------

    def __get_in_person_sessions(self) -> str:
        return self.__in_person_sessions

    in_person_sessions = property(fget=__get_in_person_sessions, doc=f"{__get_in_person_sessions.__doc__}")
# ----------------------------------------------------------------------------------------------------------------------

    def __get_poster_title(self) -> str:
        return self.__poster_title

    poster_title = property(fget=__get_poster_title, doc=f"{__get_poster_title.__doc__}")
# ----------------------------------------------------------------------------------------------------------------------

    def __get_poster_authors(self) -> str:
        return self.__poster_authors

    poster_authors = property(fget=__get_poster_authors, doc=f"{__get_poster_authors.__doc__}")
# ----------------------------------------------------------------------------------------------------------------------

    def __get_poster_institutes(self) -> str:
        return self.__poster_institutes

    poster_institutes = property(fget=__get_poster_institutes, doc=f"{__get_poster_institutes.__doc__}")
# ----------------------------------------------------------------------------------------------------------------------

    def __get_author(self) -> str:
        return self.__author

    author = property(fget=__get_author, doc=f"{__get_author.__doc__}")
# ----------------------------------------------------------------------------------------------------------------------

    def __get_author_surname(self) -> str:
        return self.__author_surname

    author_surname = property(fget=__get_author_surname, doc=f"{__get_author_surname.__doc__}")
# ----------------------------------------------------------------------------------------------------------------------

    def __get_thumbnail(self) -> str:
        return self.__thumbnail

    thumbnail = property(fget=__get_thumbnail, doc=f"{__get_thumbnail.__doc__}")
# ----------------------------------------------------------------------------------------------------------------------

    def __get_published(self) -> bool:
        return self.__published

    published = property(fget=__get_published, doc=f"{__get_published.__doc__}")
# ----------------------------------------------------------------------------------------------------------------------

    def __get_abstract_id(self) -> int:
        return self.__abstract_id

    abstract_id = property(fget=__get_abstract_id, doc=f"{__get_abstract_id.__doc__}")
# ----------------------------------------------------------------------------------------------------------------------

    def __get_display_themes(self) -> str:
        return self.__display_themes

    display_themes = property(fget=__get_display_themes, doc=f"{__get_display_themes.__doc__}")
# ----------------------------------------------------------------------------------------------------------------------

    def __get_author_institutes(self) -> str:
        return self.__author_institutes

    author_institutes = property(fget=__get_author_institutes, doc=f"{__get_author_institutes.__doc__}")
# ----------------------------------------------------------------------------------------------------------------------

    def __get_notice(self) -> str:
        return self.__notice

    notice = property(fget=__get_notice, doc=f"{__get_notice.__doc__}")
# ----------------------------------------------------------------------------------------------------------------------

    def __get_award_icon_name(self) -> str:
        return self.__award_icon_name

    award_icon_name = property(fget=__get_award_icon_name, doc=f"{__get_award_icon_name.__doc__}")
# ----------------------------------------------------------------------------------------------------------------------

    def __get_metadata(self) -> __Metadata:
        return self.__metadata

    metadata = property(fget=__get_metadata, doc=f"{__get_metadata.__doc__}")
# ----------------------------------------------------------------------------------------------------------------------

    def __get_author_title_prefix(self) -> str:
        return self.__author_title_prefix

    author_title_prefix = property(fget=__get_author_title_prefix, doc=f"{__get_author_title_prefix.__doc__}")
# ----------------------------------------------------------------------------------------------------------------------

    def __get_theme(self) -> str:
        return self.__theme

    theme = property(fget=__get_theme, doc=f"{__get_theme.__doc__}")
# ----------------------------------------------------------------------------------------------------------------------

    def __get_presenter(self) -> str:
        return self.__presenter

    presenter = property(fget=__get_presenter, doc=f"{__get_presenter.__doc__}")
# ----------------------------------------------------------------------------------------------------------------------

    def __get_day(self) -> str:
        return self.__day

    day = property(fget=__get_day, doc=f"{__get_day.__doc__}")
# ----------------------------------------------------------------------------------------------------------------------

    def __get_time(self) -> str:
        return self.__time

    time = property(fget=__get_time, doc=f"{__get_time.__doc__}")
# ----------------------------------------------------------------------------------------------------------------------
