import asyncio
import re

import aiocron
import aiohttp
import telepot
import telepot.aio
from telepot.aio.loop import MessageLoop

from commands import Dispatcher

try:
    import config
except ImportError:
    raise Exception(
        'Must create a `config.py` file with at least a TOKEN entry.')


async def process(disp, text):
    rgx = r'^/(?P<cmd>\w+)(?:@Chingolo_bot)?(?P<args> .*)?$'
    match = re.match(rgx, text, re.IGNORECASE)
    if match:
        cmd, args = match.groups()

        if args:
            args = args.strip()

        if cmd == 'help':
            await disp.help()
        elif cmd == 'js':
            await disp.js(args)
        elif cmd == 'vape':
            await disp.vape(args)
        elif cmd == 'sadness':
            await disp.sadness()
        elif cmd == 'puppy':
            await disp.puppy()
        elif cmd == 'remember':
            await disp.remember(args)
        elif cmd == 'urban':
            await disp.urban(args)
        elif cmd == 'money':
            await disp.money(args)
        elif cmd == 'shrek':
            await disp.shrek()
        elif cmd == 'test':
            await disp.test(args)
        else:
            pass
    else:
        pass


async def handle(msg):
    """ Takes a message and acts accordingly.

        If not `text` type, banana.
        Otherwise, `process`.
    """
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id)

    if content_type == 'text':
        disp = Dispatcher(bot, chat_id)
        await process(disp, msg['text'])
    else:
        await bot.sendMessage(chat_id, text='🍌')


bot = telepot.aio.Bot(config.TOKEN)


@aiocron.crontab('0 14 * * *')
async def notify_venta_pasajes_tren_mdq():
    async with aiohttp.ClientSession(raise_for_status=True,
                                     conn_timeout=30,
                                     read_timeout=30) as session:
        url = 'https://www.argentina.gob.ar/argentina.gob.ar/transporte/trenes-argentinos/horarios-tarifas-y' \
              '-recorridos/servicios-regionales-larga-distancia/buenosaires-mardelplataf'

        async with session.get(url) as resp:
            result = await resp.text()

    match = re.search(r'hasta el (.*)</strong>', result)
    fecha = match.group(1)
    await bot.sendMessage(8092568, 'Se pueden sacar pasajes hasta el {}'.format(fecha))


def main():
    """ Set up the `event_loop`.
    """

    loop = asyncio.get_event_loop()
    loop.create_task(MessageLoop(bot, handle).run_forever())
    print('Running like crazy yo!')

    loop.run_forever()


if __name__ == "__main__":
    main()
