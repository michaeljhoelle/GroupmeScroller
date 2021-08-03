import datetime
import requests
import re
import yaml


def print_quotes(message_bois):
    for message in message_bois:
        text = message['text']
        if message.get('sender_type') != 'bot' and text is not None:
            if re.search(search_regex, text):
                date = datetime.datetime.fromtimestamp(message.get('created_at'))
                print(date.strftime("%m/%d/%Y") + " " + message['name'].ljust(55) + " " + text)


if __name__ == '__main__':
    with open("config.yaml") as configfile:
        cfg = yaml.safe_load(configfile)
        access_token = cfg['accessToken']
        group_id = cfg['groupId']
        search_regex = cfg['searchRegex']

    url = "https://api.groupme.com/v3/groups/" + str(group_id) + "/messages?limit=100&token=" + access_token
    chat_page_request = requests.get(url)
    messages = chat_page_request.json().get('response').get('messages')
    last_message_id = messages[99].get('id')
    print_quotes(messages)

    while True:
        page_url = url + "&before_id=" + last_message_id
        chat_page_request = requests.get(page_url)
        messages = chat_page_request.json().get('response').get('messages')
        last_message_id = messages[99].get('id')
        print_quotes(messages)
        if len(messages) < 100:
            break
