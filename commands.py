import requests

def help():
    return {'text': """
# Commands
*/js <library>*: checks if library is cool or not
*/help*: return this
            """,
            'parse_mode': 'Markdown'}

def js(string):
    if string:
        return {'text': '{} is gay'.format(string)}
    else:
        return None
