import os

from src.trello2youtrack.trello import Trello
from src.trello2youtrack.youtrack import YouTrack

TRELLO_API_KEY = os.getenv('TRELLO_API_KEY')
TRELLO_API_TOKEN = os.getenv('TRELLO_API_TOKEN')

YOUTRACK_API_BASE_URL = os.getenv('YOUTRACK_API_BASE_URL')
YOUTRACK_PERM_TOKEN = os.getenv('YOUTRACK_PERM_TOKEN')


def main():
    trello = Trello(api_key=TRELLO_API_KEY, api_token=TRELLO_API_TOKEN)
    youtrack = YouTrack(api_base_url=YOUTRACK_API_BASE_URL,
                        perm_token=YOUTRACK_PERM_TOKEN)


if __name__ == '__main__':
    pass
