import re
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
    if not string:
        return None, None
    elif re.match(r'macri', string, re.IGNORECASE):
        return 'message', {'text': '{} gato 😺'.format(string)}
    else string:
        return 'message', {'text': '{} is gay'.format(string)}

def sadness():
    blogs = ['vaporwavedotorg.tumblr.com',
             'vaporwave-z.tumblr.com',
             'vaporwave.tumblr.com']
    blog = random.choice(blogs)

    url = 'https://api.tumblr.com/v2/blog/{}/posts/photo?api_key={}'\
            .format(blog, config.TUMBLR_KEY)

    r = requests.get(url)
    if r.ok:
        data = r.json()
        post = random.choice(data['response']['posts'])
        text = post['summary']
        url = post['photos'][0]['original_size']['url']
        return 'photo', {'photo': url, 'caption': text}
    else:
        return None, None
