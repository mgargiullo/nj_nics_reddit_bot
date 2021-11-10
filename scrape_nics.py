import praw
from lxml import html
import requests
import json

page = requests.get('https://www.njportal.com/njsp/nicsverification')
tree = html.fromstring(page.content)

msg = tree.xpath('//div[@class="message-group"]/text()')
if len(msg) == 0:
    print("No data found")
else:
    clean_msg = msg[0].strip()
    msg_parts = clean_msg.split('. ')
    msg_part_one = msg_parts[0].strip()
    msg_part_one_parts = msg_part_one.split(' ')
    post_title = "NJ NICS Update as of " + msg_part_one_parts[0] + " on " + msg_part_one_parts[1]

    post_body = " ".join(msg_part_one_parts[2:]) + " as of " + msg_part_one_parts[0] + " on " + msg_part_one_parts[1] + \
                ". " + msg_parts[1].strip() + ".\r\n \r\n^(Fetched: " + page.headers['Date'] + ")"

    credentials = 'client_secrets.json'

    with open(credentials) as f:
        creds = json.load(f)

    reddit = praw.Reddit(client_id=creds['client_id'],
                         client_secret=creds['client_secret'],
                         user_agent=creds['user_agent'],
                         redirect_uri=creds['redirect_uri'],
                         refresh_token=creds['refresh_token'])

    reddit.validate_on_submit = True

    sub_r = 'NJGuns'

    subreddit = reddit.subreddit(sub_r)

    subreddit.submit(post_title, selftext=post_body)

print("Done.")
