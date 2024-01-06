import csv
import json
import os
from typing import List, Dict, Union, Any

import requests

AGILE_TOOLS_PLUGIN_ID = '59d4ef8cfea15a55b0086614'


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
        response.raise_for_status()
        return response.json()

    def get_card(self, card_id: str) -> Dict[str, Any]:
        response = self.request(method='GET',
                                url=f'/cards/{card_id}')
        response.raise_for_status()
        return response.json()

    def get_card_powerups(self, card_id: str) -> List[Dict[str, Any]]:
        response = self.request(method='GET',
                                url=f'/cards/{card_id}/pluginData')
        response.raise_for_status()
        return response.json()

    def get_board_cards_powerups(self,
                                 board_id: str,
                                 timeout: int = 1) -> List[Dict[str, Any]]:
        """
        Returns a list of Power-Ups (Plugins) data for all cards
        on the given board.

        :param board_id: ID of the board
        :param timeout: Timeout in seconds to wait between API calls
        :return: Mapping of card IDs (Short Links) to card name and Power-Ups
        """
        cards = self.get_board_cards(board_id)

        session = requests.Session()
        query_params = {'key': self.api_key, 'token': self.api_token}
        card_powerups = []
        for card in cards:
            response = session.get(
                url=f'{self.api_base_url}/cards/{card["shortLink"]}/pluginData',
                params=query_params,
                timeout=timeout,
            )
            response.raise_for_status()
            card_powerups.append({'id': card['shortLink'],
                                  'name': card['name'],
                                  'powerups': response.json()})
            if len(card_powerups) % 10 == 0:
                print('Progress:', len(card_powerups))
        return card_powerups

    def export_board_story_points(
            self,
            card_powerups: List[Dict[str, Any]],
            csv_path: Union[str, bytes, os.PathLike],
            csv_header: List[str] = None
    ) -> None:
        """
        Exports the cards' Story Points on the given board in a CSV file.

        :param card_powerups: List of Card Power-Ups data
        :param csv_path: Path to the output CSV file
        :param csv_header: CSV header
        :return:
        """

        csv_header = csv_header or ['Summary', 'Story Points']
        with open(csv_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # Write the header
            writer.writerow(csv_header)
            # Write the rows beyond the header
            for card in card_powerups:
                story_points = self.parse_powerup_points(card['powerups'])
                writer.writerow([card['name'], story_points])

    @staticmethod
    def parse_powerup_points(powerups: List[Dict[str, Any]]) -> str:
        try:
            for powerup in powerups:
                if powerup['idPlugin'] == AGILE_TOOLS_PLUGIN_ID:
                    parsed_points = json.loads(powerup['value'])
                    return str(parsed_points['points'])
        except Exception:
            pass
        return ''
