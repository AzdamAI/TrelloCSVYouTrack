import os

from src.trcsvyt.logger import Logger
from src.trcsvyt.youtrack import YouTrack

YOUTRACK_API_BASE_URL = os.getenv('YOUTRACK_API_BASE_URL')
YOUTRACK_PERM_TOKEN = os.getenv('YOUTRACK_PERM_TOKEN')


def import_youtrack():
    youtrack = YouTrack(api_base_url=YOUTRACK_API_BASE_URL,
                        perm_token=YOUTRACK_PERM_TOKEN)

    raise NotImplementedError(
        'CSV -> YouTrack import is not implemented yet. '
        'Build your mapping and creation/updating logic here.'
    )


if __name__ == '__main__':
    with Logger(__file__) as logger:
        import_youtrack()
