from typing import List, Dict, Any

import requests


class Trello:
    def __init__(self, api_base_url: str = 'https://api.trello.com/1',
                 api_key: str = None, api_token=None):
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

    def get_board_cards(self, board_id: str) -> List[Dict[str, Any]]:
        response = self.request(method='GET',
                                url=f'/boards/{board_id}/cards')
        return response.json()

    def get_card(self, card_id: str) -> Dict[str, Any]:
        response = self.request(method='GET',
                                url=f'/cards/{card_id}')
        return response.json()

    def get_card_powerups(self, card_id: str) -> List[Dict[str, Any]]:
        response = self.request(method='GET',
                                url=f'/cards/{card_id}/pluginData')
        return response.json()

    def get_board_cards_powerups(self,
                                 board_id: str,
                                 timeout: int = 1) -> List[Dict[str, Any]]:
        """
        Returns a list of Power-Ups (Plugins) data for all cards
        on the given board.

        :param board_id: ID of the board
        :param timeout: Timeout in seconds to wait between API calls
        :return: List of Power-Ups data
        """
        cards = self.get_board_cards(board_id)

        session = requests.Session()
        query_params = {'key': self.api_key, 'token': self.api_token}
        powerups = []
        for card in cards:
            response = session.get(
                url=f'{self.api_base_url}/cards/{card["shortLink"]}/pluginData',
                params=query_params,
                timeout=timeout,
            )
            powerups.append(response.json())
            if len(powerups) % 10 == 0:
                print('Progress:', len(powerups))
        return powerups
