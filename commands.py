import inspect
import logging
import random
import shelve
from functools import wraps
from os import path

import scrython
from telegram.ext import CommandHandler

import config
from helpers import async_get, markdown_escapes


def command(help_text):
    def wrapped(fn):
        @wraps(fn)
        def wrapped_f(*args, **kwargs):
            return fn(*args, **kwargs)

        wrapped_f.help_text = help_text
        return wrapped_f

    return wrapped


class Commands:
    """ A simple unifying interface for commands.
        The @command decorator provides metadata for the `/help`
        endpoint.
    """

    def add_handlers(self, application):
        for name, f in self.commands():
            application.add_handler(CommandHandler(name, f))

    def commands(self):
        def predicate(fn):
            return inspect.ismethod(fn) and hasattr(fn, 'help_text')

        return inspect.getmembers(self, predicate=predicate)

    @command('`/help` - return this')
    async def help(self, update, context):
        msg = "*Command list*\n\n"

        for _, f in self.commands():
            msg += f.help_text + '\n'

        await update.effective_chat.send_message(msg, parse_mode='Markdown')

    @command('`/random` - rand card')
    async def random(self, update, context):
        card = scrython.cards.Random()
        await update.effective_chat.send_photo(photo=card.image_uris()['normal'], caption=caption)

    # @command('')
    async def test(self, args):
        # data = await async_get('http://localhost:8000/')
        print(path.dirname(__file__))

    @command('`/js <library>` - checks if library is cool or not')
    async def js(self, update, context):
        string = ' '.join(context.args)

        def messages(desc, pop):
            n = pop * 100
            tmpl = '{}: {}.\nScore: {:.1f} out of 100, {}'
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

            return tmpl.format(string, desc, n, m)

        if not string:
            return

        data = await async_get(
            'https://api.npms.io/v2/search?q={}'.format(string))

        if data['results']:
            pop = data['results'][0]['score']['detail']['popularity']
            desc = data['results'][0]['package']['description']
            await update.effective_chat.send_message(messages(desc, pop))
        else:
            await update.effective_chat.send_message('No')

    @command('`/sadness` - cry')
    async def sadness(self, update, context):
        tag = random.choice(['vaporwaveaesthetic',
                             'vaporwaveart',
                             'vaporwave',
                             'lofiaesthetic',
                             'aesthetics',
                             '2000s',
                             'y2k'])

        try:
            api_url = 'https://api.tumblr.com/v2/tagged?tag={}&api_key={}' \
                .format(tag, config.TUMBLR_API_KEY)
            data = await async_get(api_url, headers={'User-Agent': 'HTTPie/3.2.1'})

            photo_posts = filter(lambda p: p['type'] == 'photo', data['response'])
            post = random.choice(list(photo_posts))
            img = random.choice(post['photos'])

            caption = img['caption']
            url = img['original_size']['url']
            await update.effective_chat.send_photo(photo=url, caption=caption)
        except Exception as e:
            logging.error(e)
            await update.effective_chat.send_message('lol')

    @command('`/remember <keyword> <text>` - have memories')
    async def remember(self, update, context):
        """ Splits on spaces and takes first
            word as `keyword` rest as `body`.
            If body is not empty store that in memory,
            else return it.
        """
        string = ' '.join(context.args)
        if not string:
            return

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
        await update.effective_chat.send_message(txt)

    @command('`/vape <text>` - A E S T H E T I C S')
    async def vape(self, update, context):
        text = ' '.join(context.args)

        def trans(c):
            i = ord(c)
            if ord('!') <= i <= ord('}'):
                return chr(0xFF01 + i - ord('!'))
            else:
                return c

        if text:
            await update.effective_chat.send_message(''.join(trans(c) for c in text))
        else:
            await update.effective_chat.send_message('ｎｅｖｅｒｍｉｎｄ')

    @command('`/shrek` - swamp boy')
    async def shrek(self, update, context):
        if random.random() > 0.15:
            pack = await context.bot.get_sticker_set('ShrekLitoris')
            sticker = random.choice(pack['stickers'])
            await update.effective_chat.send_sticker(sticker['file_id'])
        else:
            fname = path.join(path.dirname(__file__), 'allstar.txt')
            with open(fname) as f:
                await update.effective_chat.send_message(f.read())
                await update.effective_chat.send_message('`You have been Shrek\'d`', parse_mode='Markdown')
