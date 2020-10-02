from commands import Dispatcher

import re
import asyncio
import telepot
import telepot.aio
from telepot.aio.loop import MessageLoop

try:
    import config
except ImportError:
    raise Exception(
            'Must create a `config.py` file with at least a TOKEN entry.')


async def process(disp, text):
    rgx = r'^/(?P<cmd>\w+)(?:@AntikytheraBot)?(?P<args> .*)?$'
    match = re.match(rgx, text, re.IGNORECASE)

    if not match: return

    cmd, args = match.groups()

    if args:
        args = args.strip()

    if cmd == 'help':
        await disp.help()
    elif cmd == 'sadness':
        await disp.sadness()
    elif cmd == 'vape':
        await disp.vape(args)
    elif cmd == 'exchange':
        await disp.exchange(args)
    elif cmd == 'welcome':
        await disp.welcome()


async def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id)

    disp = Dispatcher(bot, chat_id)

    if content_type == 'text':
        await process(disp, msg['text'])
    elif content_type in ['new_chat_member', 'new_chat_members']:
        await disp.welcome()

bot = telepot.aio.Bot(config.TOKEN)

def main():

    loop = asyncio.get_event_loop()
    loop.create_task(MessageLoop(bot, handle).run_forever())
    print('Running like crazy yo!')

    loop.run_forever()

if __name__ == "__main__":
    main()
