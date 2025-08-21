import os
import requests
import pandas as pd
import getpass

# Prompt for API token at runtime (input is hidden)
API_TOKEN = getpass.getpass('Enter your PagerDuty API token: ')

if not API_TOKEN:
    raise ValueError("API token is required to run this script.")

HEADERS = {
    'Authorization': f'Token token={API_TOKEN}',
    'Accept': 'application/vnd.pagerduty+json;version=2'
}

def get_all_users():
    users = []
    url = 'https://api.pagerduty.com/users'
    params = {'limit': 100, 'offset': 0}
    while True:
        resp = requests.get(url, headers=HEADERS, params=params)
        resp.raise_for_status()
        data = resp.json()
        users.extend(data['users'])
        if not data.get('more'):
            break
        params['offset'] += params['limit']
    return users

def get_user_contact_methods(user_id):
    url = f'https://api.pagerduty.com/users/{user_id}/contact_methods'
    resp = requests.get(url, headers=HEADERS)
    resp.raise_for_status()
    return resp.json().get('contact_methods', [])

def get_user_notification_rules(user_id):
    url = f'https://api.pagerduty.com/users/{user_id}/notification_rules'
    resp = requests.get(url, headers=HEADERS)
    resp.raise_for_status()
    return resp.json().get('notification_rules', [])

def main():
    users = get_all_users()
    all_contact_types = set()
    user_data = []

    # First pass: collect all contact method types
    for user in users:
        contact_methods = get_user_contact_methods(user['id'])
        for cm in contact_methods:
            all_contact_types.add(cm['type'])

    contact_types = sorted(all_contact_types)

    for user in users:
        row = {
            'User ID': user['id'],
            'Name': user['name'],
            'Email': user['email']
        }

        # Contact methods
        contact_methods = get_user_contact_methods(user['id'])
        for ctype in contact_types:
            row[ctype] = ', '.join(
                cm['address'] for cm in contact_methods if cm['type'] == ctype
            )

        # Notification rules
        notification_rules = get_user_notification_rules(user['id'])
        high_urgency = []
        low_urgency = []
        for rule in notification_rules:
            rule_str = f"{rule['start_delay_in_minutes']}min via {rule['contact_method']['type']}"
            if rule['urgency'] == 'high':
                high_urgency.append(rule_str)
            elif rule['urgency'] == 'low':
                low_urgency.append(rule_str)
        row['High Urgency Notification Rules'] = '; '.join(high_urgency)
        row['Low Urgency Notification Rules'] = '; '.join(low_urgency)

        user_data.append(row)

    # Create DataFrame and save to CSV on Desktop (edit path if needed)
    output_path = os.path.expanduser('~/Desktop/pagerduty_users.csv')
    columns = ['User ID', 'Name', 'Email'] + contact_types + [
        'High Urgency Notification Rules', 'Low Urgency Notification Rules'
    ]
    df = pd.DataFrame(user_data, columns=columns)
    df.to_csv(output_path, index=False)
    print(f'CSV generated: {output_path}')

if __name__ == '__main__':
    main()
