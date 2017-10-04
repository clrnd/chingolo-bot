import asyncio
from aiohttp import web

async def hello(request):
    await asyncio.sleep(1)
    return web.json_response({
        'result_type': 'exact',
        'list': [{
            'definition': 'Lol **my _buddd_ <lol> \n> sdsdsd\n`',
            'example': 'Pepe ` * _ [ [ [ ] < > { } \n#sss\n + - .'}]})

app = web.Application()
app.router.add_get('/', hello)

web.run_app(app, port=8000)
