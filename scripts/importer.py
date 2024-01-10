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

RESOLVED_STATE = 'Done'


def main():
    trello = Trello(api_key=TRELLO_API_KEY, api_token=TRELLO_API_TOKEN)
    cards = trello.get_board_cards(TRELLO_BOARD_ID)
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
                actions_mapping[card_id]
            )
            row['Summary'] = trello.parse_card_summary(card)
            row['Description'] = trello.parse_card_description(card)
            row['Due Date'] = trello.parse_card_due(card)
            row['Assignee (user)'] = assignee
            # Consider all the Cards in the past as Done
            row['State (state)'] = RESOLVED_STATE
            row['Story Points (integer)'] = trello.parse_story_points(
                powerups_mapping[card_id]
            )
            board.append(row)
    board = trello.sort_board(board)
    trello.export_board_csv(board, 'trello-board.csv', CSV_HEADER)

    youtrack = YouTrack(api_base_url=YOUTRACK_API_BASE_URL,
                        perm_token=YOUTRACK_PERM_TOKEN)


if __name__ == '__main__':
    with Logger(__file__) as logger:
        pass
