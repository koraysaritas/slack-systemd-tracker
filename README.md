# Slack systemd Tracker
Stream systemd logs into Slack.

###### Supported syslog identifiers
- sshd
- sudo

## Prerequisites
- Git (1.7.x or newer)
- Python 3.5+
- A Slack App and a Bot User
  - https://YOUR-TEAM-HERE.slack.com/apps/manage

## Installing
You can install from source:

###### Clone from source
    $ git clone https://github.com/koraysaritas/slack-systemd-tracker

###### Create and activate a new virtual environment
    $ cd slack-systemd-tracker
    $ python3 -m venv venv
    $ source venv/bin/activate

###### Install project requirements
    $ pip install -r requirements.txt

## Configuration
You need to define the following parameters in the ``config.yaml`` file:
- ``token: '<SLACK-TOKEN-HERE>'``
  - Example: ``token: 'xoxb-15...'``
- ``webhook-url: '<SLACK-WEBHOOK-URL-HERE>'``
  - Example: ``webhook-url: 'https://hooks.slack.com/services/T32...'``
- ``bot-name: '<SLACK-BOT-NAME-HERE>'``
  - Example: ``bot-name: 'kerata'``
- ``channel-name: '<SLACK-CHANNEL-HERE>'``
  - Example: ``channel-name: 'general'``

## Screenshots

###### sudo commands
![01](https://github.com/koraysaritas/slack-systemd-tracker/blob/master/screenshots/d1_small.png)

###### login failed
![03](https://github.com/koraysaritas/slack-systemd-tracker/blob/master/screenshots/d2_small.PNG)

###### login
![02](https://github.com/koraysaritas/slack-systemd-tracker/blob/master/screenshots/d3_small.png)