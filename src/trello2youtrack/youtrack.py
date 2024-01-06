from typing import Dict

import requests

ISSUE_FIELDS = \
    'id,summary,' \
    'customFields(id,name,' \
    'value(avatarUrl,buildLink,color(id),fullName,id,isResolved,' \
    'localizedName,login,minutes,name,presentation,text))'


class YouTrack:
    def __init__(self, api_base_url: str = None, perm_token: str = None):
        """
        Adapter class for YouTrack.

        :param api_base_url: YouTrack REST API base URL
            (e.g. https://www.example.com/youtrack/api).
        :param perm_token: YouTrack permanent token. Refer to:
            https://www.jetbrains.com/help/youtrack/devportal/authentication-with-permanent-token.html
        """
        self.api_base_url = api_base_url
        self.perm_token = perm_token
        if not self.api_base_url or not self.perm_token:
            raise ValueError('Both base URL and permanent token are required.')

        self.session = self.init_session()

    def init_session(self) -> requests.Session:
        session = requests.Session()
        # Set the common headers for GET/POST requests
        session.headers.update({
            'Authorization': f'Bearer {self.perm_token}',
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        })
        return session

    def get_issue(self, issue_id: str) -> Dict:
        response = self.session.get(
            url=f'{self.api_base_url}/api/issues/{issue_id}',
            params={'fields': ISSUE_FIELDS}
        )
        response.raise_for_status()
        return response.json()

    def update_issue_story_points(self,
                                  issue_id: str,
                                  story_points: int) -> Dict:
        response = self.session.post(
            url=f'{self.api_base_url}/api/issues/{issue_id}',
            params={'fields': ISSUE_FIELDS},
            json={'customFields': [{'$type': 'SimpleIssueCustomField',
                                    'id': '192-57',
                                    'name': 'Story points',
                                    'value': story_points}]}
        )
        response.raise_for_status()
        return response.json()
