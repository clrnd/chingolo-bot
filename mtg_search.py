import asyncio
import logging

import scrython
from telegram import InlineQueryResultPhoto


async def inline_query_handler(update, context):
    query = update.inline_query.query

    if not query or len(query) < 3:
        return

    try:
        search = scrython.cards.Search(q=query)
        await asyncio.sleep(0.5)
    except Exception as e:
        logging.error(e)
        return

    results = [
        [
            InlineQueryResultPhoto(
                id=result['illustration_id'],
                photo_url=result['image_uris']['normal'],
                thumbnail_url=result['image_uris']['small'],
            )
        ] if 'image_uris' in result else [
            InlineQueryResultPhoto(
                id=face['illustration_id'],
                photo_url=face['image_uris']['normal'],
                thumbnail_url=face['image_uris']['small'],
            ) for face in result['card_faces']
        ]
        for result in search.data()[:10]
    ]

    await update.inline_query.answer([item for items in results for item in items])
