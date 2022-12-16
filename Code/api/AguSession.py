from time import time
from json import dumps
from requests import Session
from re import compile, search

from Code.api.exceptions import NotLoggedException, BadPasswordException



class AguSession(Session):

    __slots__ = ('__username', '__password')

    __TIMEOUT = 20
    __AGU_DOMAIN = 'agu2022fallmeeting-agu.ipostersessions.com'
    __ID_RETRIEVER_URL_TEMPLATE = 'https://agu2022fallmeeting-agu.ipostersessions.com/?s='
    __2ND_ID_REGEXP = compile(r'GetFile\.ashx\?file=([0-9A-F]{2}-){15}[0-9A-F]{2}_[0-9]{13}\.pdf')
    __LOGIN_PAGE = 'https://id.agu.org/am/XUI/?realm=/alpha&authIndexType=service&authIndexValue=AuthN&goto=https%3A%2F%2Fid.agu.org%3A443%2Fam%2Foauth2%2Fauthorize%3Fclient_id%3Diposter%26redirect_uri%3Dhttps%3A%2F%2Fagu2022fallmeeting-agu.ipostersessions.com%2FDefault.aspx%3Fs%253Doidclogin%26response_type%3Dcode%26scope%3Dopenid%2520profile%2520email%2520roles%26code_challenge%3DlCPBpABz5McDvg_03R95dEpRnVdJ-i41e0dyEA3C1Ao%26code_challenge_method%3DS256%26state%3DOpenIdConnect.AuthenticationProperties%253DJhLlCid23T1BezVyy4PjbI8ejdj9Y7k55o2860x5-VkWTizznG9g8HKSTft4nCdzW5x_g-CAJ5wNzVgWc_gRbShYa8gPgffl1Yrgkfvcf_91IasdVBPfoW4EB0u9bB5xGAwKJ6qP7AjZUeu-iCbJzBA2F4TUp1kCpscYEto_7HUUU0AhArMw-O3iy9yrc-wSsGzGyuqwR75iSb4V3dgaPwbpNxpebt1zCdI4DcI2_jYcNJPtkkir4e2UmAdXi9Z4I089xl_w7tSiam1lEHWIgA29Lnznfx2PUrwRbiW6RNXruQIlVigaxCLYoPd-kF__%26response_mode%3Dform_post%26nonce%3D638066628954244090.YjY2ODEyNWUtZTQ1NC00MzAxLTk3YjAtYjRjMDNiZGRiNTkxMDY3NWY2MjUtMzI1MC00OTgxLTg2MzktZTg4ZjhjMTRkMTgz%26service%3DAuthN%26x-client-SKU%3DID_NET461%26x-client-ver%3D5.3.0.0#/'
    __AUTHENTICATION_PAGE = 'https://id.agu.org/am/json/realms/root/realms/alpha/authenticate?authIndexType=service&authIndexValue=AuthN&goto=https%3A%2F%2Fid.agu.org%3A443%2Fam%2Foauth2%2Fauthorize%3Fclient_id%3Diposter%26redirect_uri%3Dhttps%3A%2F%2Fagu2022fallmeeting-agu.ipostersessions.com%2FDefault.aspx%3Fs%253Doidclogin%26response_type%3Dcode%26scope%3Dopenid%2520profile%2520email%2520roles%26code_challenge%3DlCPBpABz5McDvg_03R95dEpRnVdJ-i41e0dyEA3C1Ao%26code_challenge_method%3DS256%26state%3DOpenIdConnect.AuthenticationProperties%253DJhLlCid23T1BezVyy4PjbI8ejdj9Y7k55o2860x5-VkWTizznG9g8HKSTft4nCdzW5x_g-CAJ5wNzVgWc_gRbShYa8gPgffl1Yrgkfvcf_91IasdVBPfoW4EB0u9bB5xGAwKJ6qP7AjZUeu-iCbJzBA2F4TUp1kCpscYEto_7HUUU0AhArMw-O3iy9yrc-wSsGzGyuqwR75iSb4V3dgaPwbpNxpebt1zCdI4DcI2_jYcNJPtkkir4e2UmAdXi9Z4I089xl_w7tSiam1lEHWIgA29Lnznfx2PUrwRbiW6RNXruQIlVigaxCLYoPd-kF__%26response_mode%3Dform_post%26nonce%3D638066628954244090.YjY2ODEyNWUtZTQ1NC00MzAxLTk3YjAtYjRjMDNiZGRiNTkxMDY3NWY2MjUtMzI1MC00OTgxLTg2MzktZTg4ZjhjMTRkMTgz%26service%3DAuthN%26x-client-SKU%3DID_NET461%26x-client-ver%3D5.3.0.0'
    __POSTER_SEARCH_REQUEST_TEMPLATE = \
        {
            'textsearch': '',
            'dropdowna': '',
            'dropdownb': '',
            'dropdownc': '',
            'dropdownd': '',
            'dropdownchat': '',
            'happeningnow': 'false',
            'languageID': '1',
            'page': '1',
            'count': None,
            'resetSession': 'false',
            'filterTheme': '',
            'sortBy': 'FinalPaperNumber',
            'iskiosk': 'false',
            'isOldConferenceSearch': '0',
            'screen': 'gallery',
            'resetdbc': 'false',
            'test': 'v.4',
            'querydata': '{ "sortby" : "default", "metasearch" : { "coauthors" : "", "person_affiliation" : "" } }'
        }

    def __init__(self, username: str, password: str) -> None:
        super().__init__()
        self.__username = str(username)
        self.__password = str(password)
        self.headers['Referer'] = 'https://id.agu.org/'
        self.headers['Origin'] = 'https://id.agu.org/'
        self.headers['TE'] = 'trailers'
        return



    def connect(self) -> None:
        login_form = self.__query_login_api()
        login_form['callbacks'][0]['input'][0]['value'] = self.__username
        login_form = self.__query_login_api(login_form)
        login_form['callbacks'][0]['input'][0]['value'] = self.__password
        login_form = self.__query_login_api(login_form)
        self.__raise_for_incorrect_password(login_form)
        return


    def enumerate_posters(self) -> tuple:
        headers = self.headers.copy()
        headers['Accept'] = 'application/json, text/javascript, */*; q=0.01'
        headers['content-type'] = 'application/json; charset=utf-8'
        self.headers['Referer'] = f"https://{self.__AGU_DOMAIN}/Default.aspx?s=gallery"
        self.headers['Origin'] = self.__AGU_DOMAIN
        poster_search_request = self.__POSTER_SEARCH_REQUEST_TEMPLATE.copy()
        poster_search_request['count'] = 20000
        timestamp = round(time() * 1000)
        url = f"https://{self.__AGU_DOMAIN}/Templates/iPosters/iPosterService.asmx/GetBatchIPostersByQueryAndDisplay?t={timestamp}"
        response = self.post(url, headers=headers, data=dumps(poster_search_request), timeout=self.__TIMEOUT)
        response.raise_for_status()
        poster_data = response.json()['d']
        return tuple(poster_data)



    def download_poster(self, poster, directory: str = '') -> None:
        response = self.get(f"https://{self.__AGU_DOMAIN}/?s={poster.id}", timeout=self.__TIMEOUT)
        response.raise_for_status()
        try:
            file_location = search(self.__2ND_ID_REGEXP, response.text).group()
        except AttributeError:
            return
        print(f"[*] ({poster.metadata.section}) Downloading {poster.title}")
        response = self.get(f"https://{self.__AGU_DOMAIN}/{file_location}", stream=True, timeout=self.__TIMEOUT)
        response.raise_for_status()
        file_path = f"{directory}/{self.__sanitize_file_name(poster.title)}.pdf"
        with open(file_path, 'wb') as file_descriptor:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                file_descriptor.write(chunk)
        return


    @staticmethod
    def __sanitize_file_name(raw_file_name: str) -> str:
        file_name = raw_file_name.replace(' ', '_')
        file_name = file_name.replace('(', '')
        file_name = file_name.replace(')', '')
        file_name = file_name.replace('[', '')
        file_name = file_name.replace(']', '')
        file_name = file_name.replace('{', '')
        file_name = file_name.replace('}', '')
        file_name = file_name.replace('<', '')
        file_name = file_name.replace('>', '')
        file_name = file_name.replace('/', '')
        file_name = file_name.replace('\\', '')
        file_name = file_name.replace('"', '')
        file_name = file_name.replace("'", '')
        file_name = file_name.replace(',', '')
        file_name = file_name.replace('.', '')
        file_name = file_name.replace(';', '')
        file_name = file_name.replace(':', '')
        file_name = file_name.replace('!', '')
        file_name = file_name.replace('?', '')
        file_name = file_name.replace('%', '')
        file_name = file_name.replace('#', '')
        file_name = file_name.replace('+', '')
        file_name = file_name.replace('=', '')
        file_name = file_name.replace('°', '')
        file_name = file_name.replace('~', '')
        file_name = file_name.replace('^', '')
        file_name = file_name.replace('*', '')
        file_name = file_name.replace('__', '_')
        return file_name.lower()



    def __raise_for_incorrect_password(self, login_form: dict) -> None:
        if 'tokenId' in login_form:
            return
        if login_form['callbacks'][0]['output'][0]['value'] == 'Incorrect Password':
            raise BadPasswordException(self.__password, 'Password is incorrect.')
        return


    def __query_login_api(self, data=None) -> dict:
        if not data:
            data = dict()
        else:
            data['status'] = 200
            data['ok'] = True
        headers = self.headers.copy()
        headers['Accept'] = 'application/json'
        headers['content-type'] = 'application/json'
        timeout = self.__TIMEOUT
        response = self.post(self.__AUTHENTICATION_PAGE, headers=headers, data=dumps(data), timeout=timeout)
        response.raise_for_status()
        login_form = response.json()
        return login_form
