import requests


class Trello:
    def __init__(self, api_base_url: str = 'https://api.trello.com/1',
                 api_key: str = None, api_token=None) -> None:
        """
        Adapter class for Trello.
        Follow Trello's REST API documentation to obtain an API key and token:
        https://developer.atlassian.com/cloud/trello/guides/rest-api/api-introduction

        :param api_base_url: Trello API base URL
        :param api_key: Trello API key
        :param api_token: Trello API token
        """
        self.api_base_url = api_base_url
        self.api_key = api_key
        self.api_token = api_token
        if not api_base_url or not api_key or not api_token:
            raise ValueError('Base URL, API Key, and API token are required')

    def request(self, method: str, url: str, **kwargs) -> requests.Response:
        kwargs['params'] = {'key': self.api_key,
                            'token': self.api_token,
                            **kwargs.get('params', {})}
        return requests.request(method,
                                f'{self.api_base_url}{url}',
                                **kwargs)
