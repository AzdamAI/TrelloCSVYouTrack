import csv
import json
import logging
import os
from typing import Tuple, List, Dict, Union, Any

import requests

# For a complete list of Action Types refer to:
# https://developer.atlassian.com/cloud/trello/guides/rest-api/action-types
ACTION_TYPES = {
    'create_card': 'createCard',
    'update_card': 'updateCard',
    'comment_card': 'commentCard',
}

LIST_FIELDS = ['all']

MEMBER_FIELDS = ['all']

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

    @staticmethod
    def read_users_mapping(
            csv_path: Union[str, bytes, os.PathLike]
    ) -> Dict[str, str]:
        users_mapping = {}
        with open(csv_path, 'r') as file_handle:
            csv_reader = csv.reader(file_handle)
            # Skip the header
            next(csv_reader)
            for row in csv_reader:
                users_mapping[row[0]] = row[1]
        return users_mapping

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

    def get_card_list(self,
                      card_id: str,
                      list_fields: List[str] = None) -> Dict[str, Any]:
        list_fields = ','.join(list_fields or LIST_FIELDS)
        response = self.request(method='GET',
                                url=f'/cards/{card_id}/list',
                                params={'fields': list_fields})
        response.raise_for_status()
        return response.json()

    def get_card_list_bulk(
            self,
            cards: List[Dict[str, Any]],
            list_fields: List[str] = None
    ) -> Dict[str, List[Dict[str, Any]]]:
        session = requests.Session()
        session.params = {'key': self.api_key, 'token': self.api_token}

        list_fields = ','.join(list_fields or LIST_FIELDS)
        list_mapping = {}
        for card in cards:
            response = session.get(
                url=f'{self.api_base_url}/cards/{card["shortLink"]}/list',
                params={'fields': list_fields}
            )
            response.raise_for_status()
            list_mapping[card['shortLink']] = response.json()
            if len(list_mapping) % 10 == 0:
                print(f'List {len(list_mapping)}')
        print('Finished retrieving Cards list\n')
        return list_mapping

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
    ) -> Dict[str, List[Dict[str, Any]]]:
        session = requests.Session()
        session.params = {'key': self.api_key, 'token': self.api_token}

        action_filter = ','.join(action_types or ACTION_TYPES.values())
        actions_mapping = {}
        for card in cards:
            response = session.get(
                url=f'{self.api_base_url}/cards/{card["shortLink"]}/actions',
                params={'filter': action_filter, 'limit': action_limit}
            )
            response.raise_for_status()
            actions_mapping[card['shortLink']] = response.json()
            if len(actions_mapping) % 10 == 0:
                print(f'Actions: {len(actions_mapping)}')
        print('Finished retrieving Cards Actions\n')
        return actions_mapping

    def get_card_members(
            self,
            card_id: str,
            member_fields: List[str] = None
    ) -> List[Dict[str, Any]]:
        member_fields = ','.join(member_fields or MEMBER_FIELDS)
        response = self.request(method='GET',
                                url=f'/cards/{card_id}/members',
                                params={'fields': member_fields})
        response.raise_for_status()
        return response.json()

    def get_cards_members_bulk(
            self,
            cards: List[Dict[str, Any]],
            member_fields: List[str] = None
    ) -> Dict[str, List[Dict[str, Any]]]:
        session = requests.Session()
        session.params = {'key': self.api_key, 'token': self.api_token}

        member_fields = ','.join(member_fields or MEMBER_FIELDS)
        members_mapping = {}
        for card in cards:
            response = session.get(
                url=f'{self.api_base_url}/cards/{card["shortLink"]}/members',
                params={'fields': member_fields}
            )
            response.raise_for_status()
            members_mapping[card['shortLink']] = response.json()
            if len(members_mapping) % 10 == 0:
                print(f'Members: {len(members_mapping)}')
        print('Finished retrieving Cards Members\n')
        return members_mapping

    def get_card_powerups(self,
                          card_id: str) -> List[Dict[str, Any]]:
        response = self.request(method='GET',
                                url=f'/cards/{card_id}/pluginData')
        response.raise_for_status()
        return response.json()

    def get_cards_powerups_bulk(
            self,
            cards: List[Dict[str, Any]],
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Returns a mapping of Power-Ups (Plugins) data for the given cards.

        :param cards: List of the cards to get the Power-Ups for
        :param timeout: Timeout in seconds to wait between API calls
        :return: Mapping of card Short Links to the Power-Ups (Plugins)
        """
        session = requests.Session()
        session.params = {'key': self.api_key, 'token': self.api_token}

        powerups_mapping = {}
        for card in cards:
            response = session.get(
                url=f'{self.api_base_url}/cards/{card["shortLink"]}/pluginData'
            )
            response.raise_for_status()
            powerups_mapping[card['shortLink']] = response.json()
            if len(powerups_mapping) % 10 == 0:
                print(f'Power-Ups: {len(powerups_mapping)}')
        print('Finished retrieving Cards Power-Ups\n')
        return powerups_mapping

    @staticmethod
    def parse_card_number(card: Dict[str, Any], assignee_index: int) -> str:
        try:
            return f'{card["idShort"]}-{assignee_index}'
        except Exception:
            logging.error(f'Failed to parse Card number: {card}')
        return ''

    @staticmethod
    def parse_card_creator_username_and_date(
            actions: List[Dict[str, Any]],
            users_mapping: Dict[str, str],
    ) -> Tuple[str, str]:
        try:
            for action in actions:
                if action['type'] == ACTION_TYPES['create_card']:
                    trello_username = action['memberCreator']['username']
                    youtrack_username = users_mapping.get(trello_username, '')
                    return youtrack_username, action['date']
            else:
                raise KeyError()
        except Exception:
            logging.error(f'Failed to parse the Card creator: {actions}')
        return '', ''

    @staticmethod
    def parse_card_summary(card: Dict[str, Any]) -> str:
        try:
            return card['name']
        except Exception:
            logging.error(f'Failed to parse Card summary: {card}')
        return ''

    @staticmethod
    def parse_card_description(card: Dict[str, Any]) -> str:
        try:
            return card['desc']
        except Exception:
            logging.error(f'Failed to parse Card description: {card}')
        return ''

    @staticmethod
    def parse_card_due(card: Dict[str, Any]) -> str:
        try:
            return card['due']
        except Exception:
            logging.error(f'Failed to parse Card due date: {card}')
        return ''

    @staticmethod
    def parse_card_assignees_username(
            members: List[Dict[str, Any]]
    ) -> List[str]:
        if not members:
            return []
        try:
            return [member['username'] for member in members]
        except Exception:
            logging.error(f'Failed to parse Card assignee: {members}')
        return []

    @staticmethod
    def parse_story_points(powerups: List[Dict[str, Any]]) -> str:
        try:
            for powerup in powerups:
                if powerup['idPlugin'] == AGILE_TOOLS_PLUGIN_ID:
                    parsed_points = json.loads(powerup['value'])
                    return str(parsed_points['points'])
        except Exception:
            logging.error(f'Failed to parse Story Points: {powerups}')
        return ''

    @staticmethod
    def sort_board(board: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return sorted(board,
                      key=lambda row: int(row['ID'].split('-')[0]),
                      reverse=False)

    def export_board_csv(self,
                         board: List[Dict[str, Any]],
                         csv_path: Union[str, bytes, os.PathLike],
                         csv_header: List[str]) -> None:
        """
        Writes the given board to a CSV file at the given path.

        :param board: List of Board Cards each as a row
        :param csv_path: Path to the output CSV file
        :param csv_header: CSV header
        :return:
        """
        with open(csv_path, mode='w', newline='', encoding='utf-8') as file:
            csv_writer = csv.DictWriter(file, fieldnames=csv_header)
            # Write the header
            csv_writer.writeheader()
            # Write the rows beyond the header
            for row in board:
                csv_writer.writerow(row)
        print(f'Successfully exported {len(board)} rows!')
