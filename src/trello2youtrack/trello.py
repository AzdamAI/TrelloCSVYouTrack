import csv
import json
import logging
import os
from typing import List, Dict, Union, Any

import requests

# For a complete list of Action Types refer to:
# https://developer.atlassian.com/cloud/trello/guides/rest-api/action-types
ACTION_TYPES = {
    'create_card': 'createCard',
    'update_card': 'updateCard',
    'comment_card': 'commentCard',
}

# Story Points Power-Up (plugin) free:
# https://trello.com/power-ups/59d4ef8cfea15a55b0086614
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

    def get_card_members(self,
                         card_id: str,
                         fields: str = 'all') -> List[Dict[str, Any]]:
        response = self.request(method='GET',
                                url=f'/cards/{card_id}/members',
                                params={'fields': fields})
        response.raise_for_status()
        return response.json()

    def get_card_actions(self,
                         card_id: str,
                         action_types: List[str] = None,
                         action_limit: int = 1000) -> List[Dict[str, Any]]:
        action_filter = ','.join(action_types or ACTION_TYPES.values())
        response = self.request(method='GET',
                                url=f'/cards/{card_id}/actions',
                                params={'filter': action_filter,
                                        'limit': action_limit})
        response.raise_for_status()
        return response.json()

    def get_cards_actions_bulk(
            self,
            cards: List[Dict[str, Any]],
            action_types: List[str] = None,
            action_limit: int = 1000,
            timeout: int = 1
    ) -> Dict[str, List[Dict[str, Any]]]:
        action_filter = ','.join(action_types or ACTION_TYPES.values())

        session = requests.Session()
        actions_mapping = {}
        for card in cards:
            response = session.get(
                url=f'{self.api_base_url}/cards/{card["shortLink"]}/actions',
                params={'key': self.api_key, 'token': self.api_token,
                        'filter': action_filter, 'limit': action_limit},
                timeout=timeout,
            )
            response.raise_for_status()
            actions_mapping[card['shortLink']] = response.json()
            if len(actions_mapping) % 10 == 0:
                print(f'Progress: {len(actions_mapping)}')
        return actions_mapping

    def get_card_powerups(self,
                          card_id: str) -> List[Dict[str, Any]]:
        response = self.request(method='GET',
                                url=f'/cards/{card_id}/pluginData')
        response.raise_for_status()
        return response.json()

    def get_cards_powerups_bulk(
            self,
            cards: List[Dict[str, Any]],
            timeout: int = 1
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Returns a mapping of Power-Ups (Plugins) data for the given cards.

        :param cards: List of the cards to get the Power-Ups for
        :param timeout: Timeout in seconds to wait between API calls
        :return: Mapping of card Short Links to the Power-Ups (Plugins)
        """
        session = requests.Session()
        powerups_mapping = {}
        for card in cards:
            response = session.get(
                url=f'{self.api_base_url}/cards/{card["shortLink"]}/pluginData',
                params={'key': self.api_key, 'token': self.api_token},
                timeout=timeout,
            )
            response.raise_for_status()
            powerups_mapping[card['shortLink']] = response.json()
            if len(powerups_mapping) % 10 == 0:
                print(f'Progress: {len(powerups_mapping)}')
        return powerups_mapping

    @staticmethod
    def parse_card_id(card: Dict[str, Any]) -> str:
        try:
            return card['idShort']
        except Exception:
            logging.error(f'Could not parse Card ID: {card}')
        return ''

    @staticmethod
    def parse_card_creator_username(card_actions: List[Dict[str, Any]]) -> str:
        try:
            for card_action in card_actions:
                if card_action['actionType'] == ACTION_TYPES['create_card']:
                    return card_action['memberCreator']['username']
            else:
                raise KeyError()
        except Exception:
            logging.error(
                f'Failed to parse the card creator username: {card_actions}'
            )
        return ''

    @staticmethod
    def parse_story_points(powerups: List[Dict[str, Any]]) -> str:
        try:
            for powerup in powerups:
                if powerup['idPlugin'] == AGILE_TOOLS_PLUGIN_ID:
                    parsed_points = json.loads(powerup['value'])
                    return str(parsed_points['points'])
        except Exception:
            logging.error(f'Could not parse Story Points: {powerups}')
        return ''

    def export_board_csv(
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
            for cp in card_powerups:
                story_points = self.parse_story_points(cp)
                writer.writerow([cp['name'], story_points])
