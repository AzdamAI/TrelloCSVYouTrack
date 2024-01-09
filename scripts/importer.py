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

    card_powerups = trello.get_card_powerups(cards)
    trello.export_board_csv(card_powerups, 'trello-board.csv')

    youtrack = YouTrack(api_base_url=YOUTRACK_API_BASE_URL,
                        perm_token=YOUTRACK_PERM_TOKEN)


if __name__ == '__main__':
    with Logger(__file__) as logger:
        pass
