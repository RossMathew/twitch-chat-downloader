import requests
from app import Config, CLI
from typing import Generator


class InvalidURLFormat(Exception):
    pass


class InvalidAPIRequest(Exception):
    pass


class TwitchAPI:
    url: str = Config().data['twitch_api']
    client_id: str = Config().data['client_id']

    def __init__(self, url: str = None, client_id: str = None):
        # Custom URL
        if url:
            if '{path}' in url:
                self.url: str = url
            else:
                raise InvalidURLFormat('Twitch API base URL must contain {path}.')

        # Custom client ID
        if client_id:
            self.client_id = client_id

    def get(self, path: str, params: dict = None, headers: dict = None) -> requests.Response:
        params = {} if params is None else params
        headers = {} if headers is None else headers
        params['client_id'] = self.client_id

        response: requests.Response = requests.get(url=str(self.url).format(path=path), params=params, headers=headers)
        if response.status_code != requests.codes.ok:
            raise InvalidAPIRequest(
                f'Twitch API returned status code {response.status_code}.'
                f'\nUrl\t{response.url}\nParams\t{params}\nHeaders\t{headers}\n')
        return response

    def video(self, video_id: str) -> dict:
        if CLI().arguments.verbose:
            print('Downloading video metadata from Twitch API')
        return self.get('videos/{}'.format(video_id)).json()

    def comment_fragment(self, video_id: str, cursor: str = '') -> dict:
        return self.get('videos/{}/comments'.format(video_id), {'cursor': cursor}).json()

    def comments(self, video_id: str) -> Generator[dict, None, None]:
        if CLI().arguments.verbose:
            print('Downloading comments from Twitch API')

        fragment: dict = {'_next': ''}

        while '_next' in fragment:
            fragment = self.comment_fragment(video_id, fragment['_next'])
            for comment in fragment['comments']:
                yield comment
