import os

from src.trello2youtrack.logger import Logger
from src.trello2youtrack.youtrack import YouTrack

YOUTRACK_API_BASE_URL = os.getenv('YOUTRACK_API_BASE_URL')
YOUTRACK_PERM_TOKEN = os.getenv('YOUTRACK_PERM_TOKEN')


def import_youtrack():
    youtrack = YouTrack(api_base_url=YOUTRACK_API_BASE_URL,
                        perm_token=YOUTRACK_PERM_TOKEN)

    raise NotImplementedError('Implement your import into YouTrack script.')


if __name__ == '__main__':
    with Logger(__file__) as logger:
        import_youtrack()
