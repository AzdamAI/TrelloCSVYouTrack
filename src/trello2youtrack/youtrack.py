class YouTrack:
    def __init__(self, api_base_url: str, perm_token: str):
        """
        Adapter class for YouTrack.

        :param api_base_url: YouTrack REST API base URL
        (e.g. https://www.example.com/youtrack/api).
        :param perm_token: YouTrack permanent token. Refer to:
        https://www.jetbrains.com/help/youtrack/devportal/authentication-with-permanent-token.html
        """
        self.api_base_url = api_base_url
        self._perm_token = perm_token
