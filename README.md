## Trello2YouTrack

📥 Import Trello Cards into YouTrack Issues.

## How to Import

### Notes

* We need Atlassian Jira as an intermediary in the import process.
* The import is tested only on the cloud version of Jira and YouTrack.
* The Trello boards as well as all other subsequent platforms are prepared
  \[loosely\] based on the Scrum methodology.
  Although it is not a strict requirement in following the current import
  process.

### High-level overview

* Import from Trello into Jira
* Then, import from Jira into YouTrack

### Detailed import process

* For Trello:
    * Make sure you have the list of user emails
      which is going to be used to map users on Jira and YouTrack.
* Follow
  Jira's [official documentation](https://support.atlassian.com/jira-cloud-administration/docs/import-data-from-trello/)
  and:
    * first create a Project with the **Scrum template** and
      choose the **project type** (**Team-managed** is tested)
* Follow
  YouTrack's [official documentation](https://www.jetbrains.com/help/youtrack/server/new-import-from-jira.html)
  and: