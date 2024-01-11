## TrelloCSV

📤 Export Trello Board in CSV for **FREE** [and optionally] Import to YouTrack.

## How to Export as CSV

### Notes

* The import is tested only on the cloud version of YouTrack.
* The Trello boards as well as all other subsequent platforms are prepared
  \[loosely\] based on the Scrum methodology.
  Although it is not a strict requirement to follow the current import
  process.

### Detailed Process

#### Trello:

* Make sure you have the list of user emails.

#### YouTrack:

1. [Read the official documentation](https://www.jetbrains.com/help/youtrack/server/new-import-from-jira.html).
2. Create a fresh Project (with type Scrum)
3. Attach project Workflows:
    - attach Due Date:
        - de-activate `Require due dates for submitted issues`
4. [pre-import] Edit project **Fields**:
    - define `Priority` **values**
    - select the desired **Default Value** of `Priority`
    - set **Default Value** of `Priority` to the desired value
    - set **Default Value** of `Type` to `User Story`
    - set **Type** of `Story points` to `float`
    - set **Type** of `Assignee` to `Multiple values`
5. Import the CSV via `Integrations > Imports`
6. [post-import] Edit project **Fields**:
    - set **Type** of `Story points` to `integer`
    - set **Type** of `Assignee` to `Single value`

  