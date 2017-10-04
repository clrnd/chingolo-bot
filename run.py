import commands
import re
import time

import asyncio
import telepot
import telepot.aio
from telepot.aio.loop import MessageLoop

try:
    import config
except ImportError:
    raise Exception(
            'Must create a `config.py` file with at least a TOKEN entry.')


async def process(text):
    rgx = r'^/(?P<cmd>\w+)(?:@Chingolo_bot)?(?P<args> .*)?$'
    match = re.match(rgx, text, re.IGNORECASE)
    if match:
        cmd, args = match.groups()
        if args:
            args = args.strip()

        if cmd == 'help':
            return commands.help()
        elif cmd == 'js':
            return await commands.js(args)
        elif cmd == 'vape':
            return commands.vape(args)
        elif cmd == 'sadness':
            return await commands.sadness()
        elif cmd == 'puppy':
            return await commands.puppy()
        elif cmd == 'remember':
            return commands.remember(args)
        elif cmd == 'urban':
            return await commands.urban(args)
        elif cmd == 'money':
            return await commands.money(args)
        elif cmd == 'test':
            return await commands.test(args)
        else:
            return None, None
    else:
        return None, None


async def handle(msg):
    """ Takes a message and acts accordingly.

        If not `text` type, do nothing.
        Otherwise, `process`.
    """
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id)

    if content_type == 'text':
        act, result = await process(msg['text'])
        if result and act:
            if act == 'message':
                await bot.sendMessage(chat_id, **result)
            if act == 'photo':
                await bot.sendPhoto(chat_id, **result)
    else:
        await bot.sendMessage(chat_id, text='🍌')

bot = telepot.aio.Bot(config.TOKEN)

def main():
    """ Set up `bot` and start the `message_loop`.
    """

    loop = asyncio.get_event_loop()
    loop.create_task(MessageLoop(bot, handle).run_forever())
    print('Running like crazy yo!')

    loop.run_forever()

if __name__ == "__main__":
    main()
