from typing import List, Dict, Any

import requests

ISSUE_FIELDS = \
    'id,summary,created,updated,' \
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

    def get_issue(self,
                  issue_id: str,
                  fields: str = None) -> Dict[str, Any]:
        fields = fields or ISSUE_FIELDS
        response = self.session.get(
            url=f'{self.api_base_url}/api/issues/{issue_id}',
            params={'fields': fields}
        )
        response.raise_for_status()
        return response.json()

    def get_all_issues(self,
                       count: int = 1_000_000,
                       fields: str = None) -> List[Dict[str, Any]]:
        """
        Returns a list of top `count` Issues.

        :param count: Number of Issues to be retrieved
        :return: List of Issues
        """
        fields = fields or ISSUE_FIELDS
        response = self.session.get(
            url=f'{self.api_base_url}/api/issues',
            params={'fields': fields, '$top': count}
        )
        response.raise_for_status()
        return response.json()

    def update_issue_story_points(self,
                                  issue_id: str,
                                  story_points: int,
                                  story_points_field_id: str = '192-57',
                                  fields: str = None) -> Dict[str, Any]:
        fields = fields or ISSUE_FIELDS
        response = self.session.post(
            url=f'{self.api_base_url}/api/issues/{issue_id}',
            params={'fields': fields},
            json={'customFields': [{'$type': 'SimpleIssueCustomField',
                                    'id': story_points_field_id,
                                    'name': 'Story points',
                                    'value': story_points}]}
        )
        response.raise_for_status()
        return response.json()
