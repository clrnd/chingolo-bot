import requests
import random

import config

def help():
    msg = """
*Command list*

`/js <library>` - checks if library is cool or not
`/help` - return this
`/sadness` - cry
    """
    return 'message', {'text': msg, 'parse_mode': 'Markdown'}

def js(string):
    if string:
        return 'message', {'text': '{} is gay'.format(string)}
    else:
        return None, None

def sadness():
    url = 'https://api.tumblr.com/v2/blog/{}/posts/photo?api_key={}'\
            .format('vaporwave.tumblr.com', config.TUMBLR_KEY)

    r = requests.get(url)

    if r.ok:
        data = r.json()
        post = random.choice(data['response']['posts'])
        text = post['summary']
        url = post['photos'][0]['original_size']['url']
        return 'photo', {'photo': url, 'caption': text}
    else:
        return None, None
