import re
import requests
import random
import shelve

import config


def help():
    msg = """
*Command list*

`/js <library>` - checks if library is cool or not
`/help` - return this
`/sadness` - cry
`/remember <keyword> <text>` - have memories
    """
    return 'message', {'text': msg, 'parse_mode': 'Markdown'}


def js(string):
    if not string:
        return None, None
    else:
        r = requests.get("https://api.npms.io/v2/search?q={}".format(string))
        if r.ok:
            data = r.json()
            if data['results']:
                popularity = data['results'][0]['score']['detail']['popularity']
            else:
                return 'message', {'text': 'that shit don\'t exist nigga'}
            if popularity > 0.90:
                return 'message', {'text': '{} is what the cool kids are using'.format(string)}
            else:
                return 'message', {'text': '{} ?? That shit? Really?'.format(string)}
        else:
            return None, None


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


def remember(string):
    """ Splits on spaces and takes first
        word as `keyword` rest as `body`.
        If body is not empty store that in memory,
        else return it.
    """
    if not string:
        return None, None

    with shelve.open('db', 'c') as db:
        keyword, *body = string.split()
        if body:
            db[keyword] = ' '.join(body)
            txt = 'I\'ll remember that'
        else:
            result = db.get(keyword, None)
            if result:
                txt = '{} = {}'.format(keyword, result)
            else:
                txt = 'No idea about {}'.format(keyword)
    return 'message', {'text': txt}
