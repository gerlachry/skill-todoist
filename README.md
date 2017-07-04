# Todoist skill
Uses https://developer.todoist.com/?python#api-overviewapi APIs for creating tasks under a project.

## Requirements
* install todoist-python library to mycroft-core virtualenv
    * pip install todoist-python
* git clone to skill directory
* find Todoist API token under your Todoist account, Settings > Integrations menu
* add Todoist API token to Mycroft configs, ~/.mycroft/mycroft.conf
```python
{ "TodoistSkill": {
	"token": "123456789101012131415"	}
}
```

## Usage:
* `add milk to grocery list`
* `add mowing lawn to outside list`
* `add study Python to personal project`
