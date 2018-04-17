import re
import inspect
import config
import random
import shelve
from os import path

from helpers import async_get, markdown_escapes, command


class Dispatcher:
    """ A simple unifying interface for commands.
        The @command decorator provides metadata for the `/help`
        endpoint.
    """

    def __init__(self, bot, chat_id):
        self.bot = bot
        self.chat_id = chat_id

    @command('`/help` - return this')
    async def help(self):
        predicate = lambda f: inspect.ismethod(f) and hasattr(f, 'docstring')
        fns = inspect.getmembers(self, predicate=predicate)

        msg = "*Command list*\n\n"
        for _, f in fns:
            msg += f.docstring + '\n'

        await self.bot.sendMessage(self.chat_id, msg, parse_mode='Markdown')


    #@command('')
    async def test(self, args):
        #data = await async_get('http://localhost:8000/')
        print(path.dirname(__file__))


    @command('`/js <library>` - checks if library is cool or not')
    async def js(self, string):
        def messages(desc, pop):
            n = pop*100
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
            await self.bot.sendMessage(self.chat_id, messages(desc, pop))
        else:
            await self.bot.sendMessage(self.chat_id, 'No')


    @command('`/sadness` - cry')
    async def sadness(self):
        sub = random.choice(['vaporwaveaesthetics',
                             'vaporwaveart',
                             'vaporwave'])

        url = 'https://imgur.com/r/{}/hot.json'.format(sub)

        data = await async_get(url)
        img = random.choice(data['data'])
        text = img['title']
        url = 'https://imgur.com/{}{}'.format(img['hash'], img['ext'])
        await self.bot.sendPhoto(self.chat_id, url, caption=text)


    @command('`/remember <keyword> <text>` - have memories')
    async def remember(self, string):
        """ Splits on spaces and takes first
            word as `keyword` rest as `body`.
            If body is not empty store that in memory,
            else return it.
        """
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
        await self.bot.sendMessage(self.chat_id, txt)

    @command('`/puppy` - good doggo')
    async def puppy(self):
        sub = 'doggos' if random.random() > 0.1 else 'boats'
        url = 'https://imgur.com/r/{}/hot.json'.format(sub)

        data = await async_get(url)

        img = random.choice(data['data'])
        text = img['title']
        url = 'https://imgur.com/{}{}'.format(img['hash'], img['ext'])

        await self.bot.sendPhoto(self.chat_id, url, caption=text)

    @command('`/urban <word>` - cool dict')
    async def urban(self, string):
        url = ('https://mashape-community-urban-dictionary.p.mashape.com/'
               'define?term={}.').format(string)
        data = await async_get(url, headers={'X-Mashape-Key':
            'GNy1l9QrcUmshewiEylj8w3VdCpVp1tbthojsnpeTXm87VYeaY'})

        if data['result_type'] == 'exact':
            info = random.choice(data['list'])
            definition = '*Definition:* {}\n'.format(
                    info['definition'].translate(markdown_escapes))
            example = '*Example:* {}'.format(
                    info['example'].translate(markdown_escapes))

            await self.bot.sendMessage(self.chat_id,
                                       definition + '\n' + example,
                                       parse_mode='Markdown')
        else:
            await self.bot.sendMessage(self.chat_id, 'Nope')

    @command('`/vape <text>` - A E S T H E T I C S')
    async def vape(self, text):
        def trans(c):
            i = ord(c)
            if ord('!') <= i <= ord('}'):
                return chr(0xFF01 + i - ord('!'))
            else:
                return c
        if text:
            await self.bot.sendMessage(self.chat_id,
                                       ''.join(trans(c) for c in text))
        else:
            await self.bot.sendMessage(self.chat_id, 'ｎｅｖｅｒｍｉｎｄ')


    @command('`/money <amount> <coin> to <coin>` - exchange rate')
    async def money(self, args):
        try:
            amount, fromcoin, _, tocoin, *_ = re.split(r' +', args)
            amount = float(amount)
        except ValueError:
            await self.bot.sendMessage(self.chat_id,
                    'Wrong format.\nExample: /money 5.9 usd to ars')
            return

        fromcoin, tocoin = fromcoin.upper(), tocoin.upper()
        url = 'http://data.fixer.io/api/latest?access_key={}'\
                .format(config.FIXER_ACCESS_KEY)
        data = await async_get(url)

        try:
            from_rate = data['rates'][fromcoin]
            to_rate = data['rates'][tocoin]
            result = amount * to_rate / from_rate
            text = '{amount} {fromcoin} = {result} {tocoin}'.format(
                        amount=amount,
                        fromcoin=fromcoin,
                        result=result,
                        tocoin=tocoin)
            await self.bot.sendMessage(self.chat_id, text)
        except (ValueError, KeyError):
            await self.bot.sendMessage(self.chat_id, 'Unknow coin (probably).')

    async def shrek(self):
        if random.random() > 0.15:
            pack = await self.bot.getStickerSet('ShrekLitoris')
            sticker = random.choice(pack['stickers'])
            await self.bot.sendSticker(self.chat_id, sticker['file_id'])
        else:
            fname = path.join(path.dirname(__file__), 'allstar.txt')
            with open(fname) as f:
                await self.bot.sendMessage(self.chat_id, f.read())
                await self.bot.sendMessage(self.chat_id,
                        '`You have been Shrek\'d`', parse_mode='Markdown')
