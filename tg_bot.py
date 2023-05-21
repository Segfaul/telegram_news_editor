from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.web_app_info import WebAppInfo


class TelegramBot:

    def __init__(self, api_token: str, chat_id: int = None, web_app_url: str = 'https://hello.world/'):
        self.bot = Bot(token=api_token)
        self.dp = Dispatcher(self.bot)
        self.chat_id = chat_id
        self.web_app_url = web_app_url
        self.handlers()

    @staticmethod
    def keyboard(commands: list) -> types.ReplyKeyboardMarkup:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        for command in commands:
            markup.add(types.KeyboardButton(command))

        return markup

    def handlers(self):

        @self.dp.message_handler(commands=['start'])
        async def start(message: types.Message):
            markup = types.ReplyKeyboardMarkup()
            markup.add(types.KeyboardButton('Open web page', web_app=WebAppInfo(
                url=self.web_app_url)))
            await message.answer('Hello, my friend!', reply_markup=markup)

    def start(self, skip_updates: bool = True):
        executor.start_polling(self.dp, skip_updates=skip_updates)
