import logging
import re

import aiocron
import aiohttp
import nest_asyncio
from telegram.ext import ApplicationBuilder, InlineQueryHandler

from commands import Commands
from mtg_search import inline_query_handler

nest_asyncio.apply()

try:
    import config
except ImportError:
    raise Exception(
        'Must create a `config.py` file with at least a TOKEN entry.')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logging.getLogger('httpx').setLevel(logging.WARNING)


@aiocron.crontab('0 14 * * *', start=False)
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
    # await bot.sendMessage(8092568, 'Se pueden sacar pasajes hasta el {}'.format(fecha))


def main():
    print('🍌')
    application = ApplicationBuilder().token(config.TOKEN).build()

    commands = Commands()
    commands.add_handlers(application)

    application.add_handler(InlineQueryHandler(inline_query_handler))

    application.run_polling()


if __name__ == "__main__":
    main()
