import re
import inspect
import config
import random
from os import path

from helpers import async_get, command


class Dispatcher:
    """ A simple unifying interface for commands.
        The @command decorator provides metadata for the /help command.
    """

    def __init__(self, bot, chat_id):
        self.bot = bot
        self.chat_id = chat_id

        fname = path.join(path.dirname(__file__), 'welcome.txt')
        with open(fname) as f:
            self.welcome_text = f.read()

    @command('/help - return this')
    async def help(self):
        predicate = lambda f: inspect.ismethod(f) and hasattr(f, 'docstring')
        fns = inspect.getmembers(self, predicate=predicate)

        msg = "Lista de comandos:\n\n"
        for _, f in fns:
            msg += f.docstring + '\n'

        await self.bot.sendMessage(self.chat_id, msg)


    @command('/sadness - cry')
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


    @command('/vape <text> - A E S T H E T I C S')
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


    @command('/exchange <amount> <coin> to <coin> - exchange rate')
    async def exchange(self, args):
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


    @command('/welcome - envía el mensaje de bienvenida')
    async def welcome(self):
        await self.bot.sendMessage(self.chat_id, '¡Hola! Bienvenide 👋')
        await self.bot.sendMessage(self.chat_id, self.welcome_text)
