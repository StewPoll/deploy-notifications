import getopt
import requests
import sys


def send_message(user, server, status, url, channel):
    if server == 'all':
        server = 'ALL SERVERS'

    text_info = {
        'user': user,
        'server': server,
        'status': status
    }

    if status == 'complete':
        color = 'good'
        text = 'DEPLOYMENT TO *{server}* BY *{user}* SUCCESSFULLY COMPLETED'
    elif status == 'commenced':
        color = '#439FE0'
        text = 'DEPLOYMENT TO *{server}* COMMENCED BY *{user}*'
    elif status == 'failed':
        color = 'danger'
        text = 'DEPLOYMENT TO *{server}* BY *{user}* FAILED\nPLEASE CHECK LOGS AND REDEPLOY'
    else:
        color = 'warning'
        text = 'DEPLOYMENT TO *{server}* BY *{user}* MOVED TO STATUS: *{status}*'

    info = {
        'username': 'Deployment Bot',
        'icon_emoji': ':construction:',
        'attachments': [
            {
                'text': text.format(**text_info),
                'mrkdwn_in': [
                    'text'
                ],
                'color': color
            }
        ]
    }

    if channel:
        info['channel'] = channel

    res = requests.post(url, json=info)
    if res.status_code >= 300 or res.status_code <= 199:
        print('An error occured sending the message to slack.\nPlease check your Slack webhook URL or the channel name')
        sys.exit(4)
    else:
        sys.exit(0)

if __name__ == '__main__':
    try:
        options = [
            "user=",
            "server=",
            "status=",
            "url=",
            'channel='
        ]
        opts, args = getopt.getopt(sys.argv[1:], "", options)
    except getopt.GetoptError:
        print(getopt.GetoptError)
        print('Usage: python deploy-notifications.py user="some_name" url="webhook_url" [--server=au --status=complete]')
        print('E.G. python deploy-notifications.py user="ben" url="https://hooks.slack.com/XXXXXX" --server=eu --status="IN PROGRESS"')
        sys.exit(1)

    # Defaults
    status = 'commenced'
    server = 'all'
    user = ''
    webhook_url = ''
    channel = ''

    for opt, arg in opts:
        if opt == '--status':
            status = arg
        elif opt == '--user':
            user = arg
        elif opt == '--server':
            server = arg
        elif opt == '--url':
            webhook_url = arg
        elif opt == '--channel':
            channel = arg

    if not user:
        print('Please specify the user that is deploying')
        sys.exit(2)
    elif not webhook_url:
        print('Please specify a webhook URL')
        sys.exit(3)
    else:
        send_message(user, server, status, webhook_url, channel)
