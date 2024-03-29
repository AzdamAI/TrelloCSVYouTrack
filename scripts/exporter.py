import os

from src.trcsvyt.logger import Logger
from src.trcsvyt.trello import Trello

TRELLO_API_KEY = os.getenv('TRELLO_API_KEY')
TRELLO_API_TOKEN = os.getenv('TRELLO_API_TOKEN')
TRELLO_BOARD_ID = os.getenv('TRELLO_BOARD_ID')

CSV_HEADER = [
    'ID', 'Author', 'Created', 'Summary', 'Description',
    'State (state)', 'Sprint (version)', 'Story Points (integer)',
    'Assignee (user)', 'Due Date (date)',
]

RESOLVED_STATE = 'Done'

USERS_CSV_PATH = 'assets/users.csv'
EXPORT_CSV_PATH = 'assets/trello-board.csv'


def export_trello():
    trello = Trello(api_key=TRELLO_API_KEY, api_token=TRELLO_API_TOKEN)
    users_mapping = trello.read_users_mapping(USERS_CSV_PATH)

    cards = trello.get_board_cards(TRELLO_BOARD_ID)
    list_mapping = trello.get_card_list_bulk(cards)
    actions_mapping = trello.get_cards_actions_bulk(cards)
    members_mapping = trello.get_cards_members_bulk(cards)
    powerups_mapping = trello.get_cards_powerups_bulk(cards)

    board = []
    for card in cards:
        card_id = card['shortLink']
        assignees = trello.parse_card_assignees_username(
            members_mapping[card_id]
        )
        # Duplicate row per Card Members with the same info but the assignee
        for i, assignee in enumerate(assignees):
            row = {}
            row['ID'] = trello.parse_card_number(card, i)
            (row['Author'],
             row['Created']) = trello.parse_card_creator_username_and_date(
                actions_mapping[card_id], users_mapping
            )
            row['Summary'] = trello.parse_card_summary(card)
            row['Description'] = trello.parse_card_description(card)
            row['State (state)'] = RESOLVED_STATE  # Consider past Cards Done
            row['Sprint (version)'] = trello.parse_card_list(
                list_mapping[card_id]
            )
            row['Story Points (integer)'] = trello.parse_story_points(
                powerups_mapping[card_id]
            )
            row['Assignee (user)'] = users_mapping.get(assignee, '')
            row['Due Date (date)'] = trello.parse_card_due(card)

            board.append(row)
    board = trello.sort_board(board)
    trello.export_board_csv(board, EXPORT_CSV_PATH, CSV_HEADER)


if __name__ == '__main__':
    with Logger(__file__) as logger:
        export_trello()
