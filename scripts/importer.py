import os
import pathlib

from src.trello2youtrack.trello import Trello
from src.trello2youtrack.youtrack import YouTrack

YOUTRACK_API_BASE_URL = os.getenv('YOUTRACK_API_BASE_URL')
YOUTRACK_PERM_TOKEN = os.getenv('YOUTRACK_PERM_TOKEN')

ASSETS_DIR = pathlib.Path('assets')


def main():
    trello = Trello(board_json_path=ASSETS_DIR / 'trello-board.json')
    youtrack = YouTrack(api_base_url=YOUTRACK_API_BASE_URL,
                        perm_token=YOUTRACK_PERM_TOKEN)


if __name__ == '__main__':
    pass
