import asyncio
from datetime import datetime, timedelta

from work_db import *
from parse_news import NewsParser
from tg_bot import TelegramBot
import aiogram.utils.markdown as md
from aiogram.types import ParseMode

from cfg import *


async def telegram_news_posting(db_root: str, bot: TelegramBot) -> None:
    try:
        print("Telegram News started...")
        django_project_path: str = '/'.join(db_root.split('/')[:-1])
        # 1 - Title, 2 - Description, 3 - Photo

        while 1:
            upcoming_posts = get_upcoming_post(db_root)

            for upcoming_post in upcoming_posts:
                upcoming_date = datetime.strptime(get_upcoming_post(db_root)[0][4], '%Y-%m-%d %H:%M:%S')

                if (upcoming_date - datetime.now()) >= timedelta(minutes=15) \
                        or (upcoming_date - datetime.now()) <= timedelta(minutes=0.5):

                    if len(upcoming_post[3]) > 0:
                        with open(django_project_path + '/media/' + upcoming_post[3], 'rb') as photo_file:
                            await bot.bot.send_photo(chat_id=bot.chat_id,
                                                     photo=photo_file,
                                                     caption=md.text(md.hbold(upcoming_post[1]) + '\n\n'
                                                                     + upcoming_post[2] + '\n\n'
                                                                     + '&#169 '
                                                                     + '<b><a href="https://google.com">'
                                                                       'NAME_BUFFER</a></b>'
                                                                     )
                                                     , parse_mode=ParseMode.HTML
                                                     )

                    else:

                        await bot.bot.send_message(bot.chat_id,
                                                   md.text(md.hbold(upcoming_post[1]) + '\n\n'
                                                           + upcoming_post[2] + '\n\n'
                                                           + '&#169 '
                                                           + '<b><a href="https://google.com">NAME_BUFFER</a></b>'
                                                           )
                                                   , parse_mode=ParseMode.HTML
                                                   , disable_web_page_preview=True
                                                   )

                    publish_post(db_root, upcoming_post[0])

            await asyncio.sleep(15)

    except Exception as error:
        print(error.__class__, error.args[0])
        await bot.bot.send_message(tg_own_id, f"TG-parser quited with:\n\n{error.__class__}\n{error.args[0]}",
                                   parse_mode='html')
        quit()


async def void_logic(db_root: str, news_parser: NewsParser, bot: TelegramBot) -> None:
    try:
        print("News parser started...")
        while 1:
            links: list or int = news_parser.get_news_list

            for link in list(reversed(links[:11])):
                main_info: dict or int = news_parser.get_news_page(link)

                if type(main_info) == dict:
                    check_existing_post: bool = check_post_on_exist(db_root, main_info['title'])

                    if not check_existing_post:
                        input_post(db_root, main_info['title'], main_info['content'])

                await asyncio.sleep(1)

            print("Ended up parsing all els")

            await asyncio.sleep(15 * 60)

    except Exception as error:
        print(error.__class__, error.args[0])
        await bot.bot.send_message(tg_own_id, f"NEWS-parser quited with:\n\n{error.__class__}\n{error.args[0]}",
                                   parse_mode='html')
        quit()


async def main() -> None:
    # Int type given if request was unsuccessful or Value/Type errors occurred

    try:

        base_link = "crypto_web_link"
        db_root = "news_editor/db.sqlite3"
        telegram_bot = TelegramBot(tg_api_token, tg_chat_id)
        news_parser = NewsParser(base_link, {'https': f'http://{american_proxy}'})

        tasks = [
            asyncio.create_task(telegram_news_posting(db_root, telegram_bot)),
            asyncio.create_task(void_logic(db_root, news_parser, telegram_bot))
        ]
        await asyncio.gather(*tasks)

    except Exception as error:
        print(error.__class__, error.args[0])


if __name__ == '__main__':
    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(main())
    finally:
        loop.close()
