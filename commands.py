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
`/puppy` - G O O D  D O G G O
`/remember <keyword> <text>` - have memories
    """
    return 'message', {'text': msg, 'parse_mode': 'Markdown'}


def js(string):
    def messages(p):
        n = p*100
        tmpl = '{} scores {:.1f} out of 100: {}'
        if n > 90:
            m = 'cool as fuck'
        elif n > 80:
            m = 'pretty ok'
        elif n > 70:
            m = 'meh'
        elif n > 60:
            m = 'old'
        elif n > 50:
            m = 'deprecated'
        elif n > 40:
            m = 'lol seriously?'
        elif n > 30:
            m = 'lol seriously?'
        elif n > 20:
            m = 'please die'
        elif n > 20:
            m = '...'
        elif n > 10:
            m = 'burn your computer'
        else:
            m = 'Exception("<commits suicide>")'

        return tmpl.format(string, n, m)

    if not string:
        return None, None
    else:
        r = requests.get('https://api.npms.io/v2/search?q={}'.format(string))
        if r.ok:
            data = r.json()
            if data['results']:
                pop = data['results'][0]['score']['detail']['popularity']
                return 'message', {'text': messages(pop)}
            else:
                return 'message', {'text': 'No.'}
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

def puppy():
    url = 'https://imgur.com/r/puppies/hot.json'
    r = requests.get(url)
    if r.ok:
        data = r.json()
        img = random.choice(data['data'])
        text = img['title']
        url = 'https://imgur.com/{}{}'.format(img['hash'], img['ext'])
        return 'photo', {'photo': url, 'caption': text}
    else:
        return None, None

def urban(string):
    url = 'https://mashape-community-urban-dictionary.p.mashape.com/define?term={}.'.format(string)
    r = requests.get(url, headers={'X-Mashape-Key':'GNy1l9QrcUmshewiEylj8w3VdCpVp1tbthojsnpeTXm87VYeaY'})
    if r.ok:
        data = r.json()
        definition = data['list'][0]['definition']
        return 'message', {'text': definition}
    else:
        return None, None
