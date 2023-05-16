import asyncio
from datetime import datetime, timedelta

from work_db import *
from parse_news import NewsParser
from tg_bot import TelegramBot

import aiogram.utils.markdown as md
from pyrogram import Client
from pyrogram.enums import ParseMode


from cfg import *


async def main() -> None:
    # Int type given if request was unsuccessful or Value/Type errors occurred

    try:

        tg_app = Client("tg_news", api_id=tg_account_id, api_hash=tg_account_hash)
        telegram_bot = TelegramBot(tg_api_token, tg_chat_id)
        post_db_conn = PostDB(db_root)
        news_parser = NewsParser(base_parse_link, {'https': f'http://{american_proxy}'})

        tasks = [
            asyncio.create_task(telegram_news_posting(post_db_conn, tg_app, telegram_bot)),
            asyncio.create_task(void_logic(post_db_conn, news_parser, telegram_bot))
        ]

        await asyncio.gather(*tasks)

    except Exception as error:
        print(error.__class__, error.args[0])
        quit()


async def client_send_message(client_app: Client, chat_id: int,
                              message: str, date: datetime, photo: str = '') -> int:
    try:

        async with client_app:
            if photo:
                await client_app.send_photo(chat_id=chat_id,
                                            photo=photo, caption=message,
                                            parse_mode=ParseMode.HTML, schedule_date=date)

            else:
                await client_app.send_message(chat_id=chat_id,
                                              text=message,
                                              parse_mode=ParseMode.HTML, schedule_date=date)

    except Exception as error:
        print(error.__class__, error.args[0])
        return 1

    return 0


async def telegram_news_posting(post_db: PostDB, client_app: Client, bot: TelegramBot) -> None:
    try:
        print("Telegram News started...")
        # 1 - Title, 2 - Description, 3 - Photo

        while 1:
            upcoming_posts = post_db.get_upcoming_post

            for upcoming_post in upcoming_posts:
                upcoming_date = datetime.strptime(upcoming_post[4], '%Y-%m-%d %H:%M:%S')

                if (upcoming_date - datetime.now()) >= timedelta(minutes=15) \
                        or upcoming_date >= datetime.now():

                    if len(upcoming_post[3]) > 0:
                        await client_send_message(client_app,
                                                  bot.chat_id,
                                                  md.text(md.hbold(upcoming_post[1]) + '\n\n'
                                                          + upcoming_post[2] + '\n\n'
                                                          + '&#169 '
                                                          + '<b><a href="http://t.me/">'
                                                            'NAME_BUFFER</a></b>'
                                                          )
                                                  ,
                                                  upcoming_date,
                                                  upcoming_post[3]
                                                  )

                    else:

                        await client_send_message(client_app,
                                                  bot.chat_id,
                                                  md.text(md.hbold(upcoming_post[1]) + '\n\n'
                                                          + upcoming_post[2] + '\n\n'
                                                          + '&#169 '
                                                          + '<b><a href="http://t.me/">'
                                                            'NAME_BUFFER</a></b>'
                                                          )
                                                  ,
                                                  upcoming_date
                                                  )

                    post_db.publish_post(upcoming_post[0])

            await asyncio.sleep(15)

    except Exception as error:
        print(error.__class__, error.args[0])
        await bot.bot.send_message(tg_own_id, f"TG-parser quited with:\n\n{error.__class__}\n{error.args[0]}",
                                   parse_mode='html')
        quit()


async def void_logic(post_db: PostDB, news_parser: NewsParser, bot: TelegramBot) -> None:
    try:
        print("News parser started...")
        while 1:
            links: list or int = news_parser.get_news_list

            for link in list(reversed(links[:11])):
                post_link: str = news_parser.link + link

                if not post_db.check_post_on_exist(origin_link=post_link):

                    main_info: dict or int = news_parser.get_news_page(link)

                    if type(main_info) == dict:

                        if not post_db.check_post_on_exist(main_info['title']):
                            post_db.input_post(main_info['title'], main_info['content'], '', post_link)

                await asyncio.sleep(1)

            print("Ended up parsing all els")

            await asyncio.sleep(15 * 60)

    except Exception as error:
        print(error.__class__, error.args[0])
        await bot.bot.send_message(tg_own_id, f"NEWS-parser quited with:\n\n{error.__class__}\n{error.args[0]}",
                                   parse_mode='html')
        quit()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(main())

    finally:
        loop.close()
