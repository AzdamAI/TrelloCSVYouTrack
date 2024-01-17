## TrelloCSVYouTrack

📤 Export Trello Board in CSV for **FREE** [and optionally] Import to YouTrack.

### Quickstart
You can run the desired script at the `scripts/` dir:
 * `scripts/exporter.py` to export a Trello board in CSV.
 * `scripts/importer.py` [stub] to import or update YouTrack Issues.


### Notes

* The import is tested only on the cloud version of YouTrack.
* The Trello boards as well as all other subsequent platforms are arranged
  \[loosely\] to follow the Scrum framework.
  Although it is not a strict requirement for the current export/import
  process.

### Export Trello board

* Make sure you have the list of user emails.

### Import into YouTrack

1. [Read the official documentation](https://www.jetbrains.com/help/youtrack/server/new-import-from-jira.html).
2. Create a fresh Project (with type Scrum)
3. Attach project Workflows:
    - [OPTIONAL] attach Due Date:
        - de-activate `Require due dates for submitted issues`
4. [pre-import] Edit project **Fields**:
    - set **Type** of `Story points` to `float`: to allow CSV values of `float`
      to be merged (YouTrack does not accept `integer` when importing from
      CSV).
    - set **Type** of `Assignee` to `Multiple values`: again, to allow CSV
      values to be merged and not to create a duplicate field (YouTrack
      imports `user` as multi-value field).
    - [OPTIONAL] define `Priority` **values**
    - [OPTIONAL] select the desired **Default Value** of `Priority`
    - [OPTIONAL] set **Default Value** of `Priority` to the desired value
    - [OPTIONAL] set **Default Value** of `Type` to `User Story`
5. Import the CSV via `Integrations > Imports`
6. [post-import] Edit project **Fields**:
    - [OPTIONAL] set **Type** of `Story points` to `integer`
    - [OPTIONAL] set **Type** of `Assignee` to `Single value`

  