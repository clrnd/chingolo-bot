import asyncio

import scrython
from telegram import InlineQueryResultPhoto


async def inline_query_handler(update, context):
    query = update.inline_query.query

    if not query or len(query) < 3:
        return

    try:
        search = scrython.cards.Search(q=query)
        await asyncio.sleep(1)
    except Exception as e:
        print(e)
        return

    results = [
        InlineQueryResultPhoto(
            id=result['id'],
            photo_url=result['image_uris']['normal'],
            thumbnail_url=result['image_uris']['small'],
        )
        for result in search.data()[:10]
    ]

    await update.inline_query.answer(results)
