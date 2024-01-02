class Trello:
    def __init__(self, board_json_path: str):
        """
        Adapter class for Trello.

        :param board_json_path: File path to the Trello board JSON file
        """
        self.board_json_path = board_json_path
