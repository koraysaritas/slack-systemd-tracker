import json

import requests


def payload_from_message(message):
    return {'text': message}


def send_message(slack_store, message):
    response = requests.post(
        slack_store.slack_url_webhook, data=json.dumps(payload_from_message(message)),
        headers=slack_store.request_header
    )
    if response.status_code != 200:
        print('Request to slack returned an error {0}, the response is:\n{1}'.format(response.status_code,
                                                                                     response.text))


def slack_send_jentry_to_channel(slack_store, j):
    if slack_store.verbose:
        print(j.friendly_message)
    send_message(slack_store, j.friendly_message)


def slack_send_msg_channel(slack_store, msg):
    print(msg)
    send_message(slack_store, msg)
