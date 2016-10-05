import re
import time
import telepot

import commands

try:
    import config
except ImportError:
    raise 'Must create a `config.py` file with at least a TOKEN entry.'


def process(text):
    rgx = r'^/(?P<cmd>\w+)(?:@Chingolo_bot)?(?P<args> .*)?$'
    match = re.match(rgx, text)
    if not match:
        return None
    else:
        cmd, args = match.groups()
        if args: args = args.strip()

        print(cmd, args)

        if cmd == 'help':
            return commands.help()
        elif cmd == 'js':
            return commands.js(args)
        else:
            return None


def handle(bot, msg):
    """ Takes a message and acts accordingly.

        If not `text` type, do nothing.
        Otherwise, `process`.
    """
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id)

    if content_type == 'text':
        result = process(msg['text'])
        if result:
            bot.sendMessage(chat_id, **result)


def main():
    """ Set up `bot` and start the `message_loop`.
    """
    bot = telepot.Bot(config.TOKEN)

    bot.message_loop(lambda m: handle(bot, m))
    print('Running like crazy yo!')

    # keep async code running until C-c
    while True:
        time.sleep(10)


if __name__ == "__main__":
    main()
