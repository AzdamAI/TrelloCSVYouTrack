import json
import os

from typing import Union


class Trello:
    def __init__(self, board_json_path: Union[str, bytes, os.PathLike]):
        """
        Adapter class for Trello.

        :param board_json_path: File path to the Trello board JSON file
        """
        self.board_json_path = board_json_path

        self.board = self.load_board()

    def load_board(self):
        with open(self.board_json_path, 'rb') as file_handle:
            return json.load(file_handle)
