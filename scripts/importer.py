import os

from src.trello2youtrack.logger import Logger
from src.trello2youtrack.trello import Trello
from src.trello2youtrack.youtrack import YouTrack

TRELLO_API_KEY = os.getenv('TRELLO_API_KEY')
TRELLO_API_TOKEN = os.getenv('TRELLO_API_TOKEN')
TRELLO_BOARD_ID = os.getenv('TRELLO_BOARD_ID')

YOUTRACK_API_BASE_URL = os.getenv('YOUTRACK_API_BASE_URL')
YOUTRACK_PERM_TOKEN = os.getenv('YOUTRACK_PERM_TOKEN')

CSV_HEADER = [
    'ID', 'Author', 'Created', 'Summary', 'Description', 'Due Date',
    'Assignee (user)', 'State (state)', 'Story Points (integer)'
]


def main():
    trello = Trello(api_key=TRELLO_API_KEY, api_token=TRELLO_API_TOKEN)
    cards = trello.get_board_cards(TRELLO_BOARD_ID)
    actions_mapping = trello.get_cards_actions_bulk(cards)
    powerups_mapping = trello.get_cards_powerups_bulk(cards)

    board = []
    for card in cards:
        row = {}
        row['id'] = trello.parse_card_id(card)
        author, created = trello.parse_card_creator_username_and_date(
            actions_mapping[card['shortLink']]
        )
        row['author'] = author
        row['created'] = created
        row['summary'] = trello.parse_card_summary(card)
        row['description'] = trello.parse_card_description(card)
        row['due_date'] = ''
        row['assignee'] = ''
        row['state'] = ''
        row['story_points'] = trello.parse_story_points(
            powerups_mapping[card['shortLink']]
        )
        board.append(row)

    # trello.export_board_csv(card_powerups, 'trello-board.csv')

    youtrack = YouTrack(api_base_url=YOUTRACK_API_BASE_URL,
                        perm_token=YOUTRACK_PERM_TOKEN)


if __name__ == '__main__':
    with Logger(__file__) as logger:
        pass
