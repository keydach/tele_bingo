import logging
import pathlib
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ContentTypes, Message, CallbackQuery
from telethon import TelegramClient
from aiogram.contrib.middlewares.logging import LoggingMiddleware

import inline_keyboard
from utils import States
from bingo import parse_data, print_cards
from settings import config


bot = Bot(token=config.bot_token.get_secret_value())
dp = Dispatcher(bot, storage=MemoryStorage())

logging.basicConfig(level=logging.INFO, format=u'%(levelname)-8s [%(asctime)s] %(message)s',)
dp.middleware.setup(LoggingMiddleware())

t_client = TelegramClient(
    "t_client",
    api_id=config.api_id.get_secret_value(),
    api_hash=config.api_hash.get_secret_value()
)
input_dir = '{}/{}'.format(pathlib.Path(__file__).parent.resolve(), config.source_dir)


@dp.message_handler(state='*', commands=['start'])
async def start(message: Message):
    state = dp.current_state(user=message.from_user.id)
    await state.reset_state()
    await state.set_state(States.all()[0])
    await message.answer(text='BINGO Music Генератор', reply_markup=inline_keyboard.START)


@dp.message_handler(state='*', commands=['help'])
async def show_help_message(message: Message):
    state = dp.current_state(user=message.from_user.id)
    await state.reset_state()
    await message.answer(text='Это бот для генерации карточек бинго, наберите /start и все увидите сами')


@dp.callback_query_handler(state=States.all(), text='example')
async def example(callback_query: CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    await t_client.start(bot_token=config.bot_token.get_secret_value())
    await t_client.send_file(
        callback_query.message.chat.id, '{}{}'.format(input_dir, config.example_songs))
    await t_client.send_file(
        callback_query.message.chat.id, '{}{}'.format(input_dir, config.example_card), force_document=True)
    await t_client.send_file(
        callback_query.message.chat.id, '{}{}'.format(input_dir, config.example_back_card), force_document=True)
    await t_client.disconnect()

    logging.info('user {} get example'.format(callback_query.from_user.id))

    await bot.send_message(
        callback_query.from_user.id, text='BINGO Music Генератор', reply_markup=inline_keyboard.START)


@dp.callback_query_handler(state=States.all(), text='songs_list')
async def lets_go(callback_query: CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    state = dp.current_state(user=callback_query.from_user.id)
    await state.set_state(States.all()[1])
    logging.info('User {} start'.format(callback_query.from_user.id))

    await bot.send_message(callback_query.from_user.id, text='Загрузите плейлист в формате TXT')


@dp.message_handler(state=States.STATE_1, content_types=ContentTypes.TEXT)
async def not_doc_txt_songs_handler(message):
    await bot.send_message(message.from_user.id, text='Я жду документ...')


@dp.message_handler(state=States.STATE_1, content_types=ContentTypes.PHOTO)
async def not_doc_photo_songs_handler(message):
    await bot.send_message(message.from_user.id, text='Нет, вы не поняли, надо TXT файл')


@dp.message_handler(state=States.STATE_1, content_types=ContentTypes.DOCUMENT)
async def songs_handler(message: Message):
    if document := message.document:
        await document.download(destination_file='{}{}_songs.txt'.format(input_dir, message.from_user.id))

    try:
        with open('{}{}_songs.txt'.format(input_dir, message.from_user.id), "r") as file_:
            raw_text = file_.read()
        cur_songs, cur_win_songs = parse_data(raw_text)
    except UnicodeDecodeError:
        await bot.send_message(message.from_user.id, text='Что-то пошло не так, файл точно правильный? Попробуем еще?')

    else:
        state = dp.current_state(user=message.from_user.id)
        await state.update_data(cur_songs=cur_songs, cur_win_songs=cur_win_songs)

        mess = 'Приняли файл, {} песен и еще {} итого {}'.format(
            len(cur_songs), len(cur_win_songs), len(cur_songs) + len(cur_win_songs))
        logging.info(mess)
        await message.answer(text='{} \nВсе верно?'.format(mess), reply_markup=inline_keyboard.CHECK_SONGS)


@dp.callback_query_handler(state=States.STATE_1, text='background')
async def prepare_background_handler(callback_query: CallbackQuery):
    state = dp.current_state(user=callback_query.from_user.id)
    await state.set_state(States.all()[2])
    await bot.send_message(callback_query.from_user.id, text='Загрузите лицевой фон в формате PNG (без сжатия)')


@dp.message_handler(state=States.STATE_2, content_types=ContentTypes.TEXT)
async def not_doc_txt_background_handler(message):
    await bot.send_message(message.from_user.id, text='Я жду документ...')


@dp.message_handler(state=States.STATE_2, content_types=ContentTypes.PHOTO)
async def not_doc_photo_background_handler(message):
    await bot.send_message(message.from_user.id, text='Нет, вы не поняли, надо "как документ" без сжатия')


@dp.message_handler(state=States.STATE_2, content_types=ContentTypes.DOCUMENT)
async def background_handler(message):
    if document := message.document:
        await document.download(destination_file='{}{}_bingo.png'.format(input_dir, message.from_user.id))

    state = dp.current_state(user=message.from_user.id)
    await state.set_state(States.all()[3])
    await bot.send_message(message.from_user.id, text='Загрузите фон рубашки в формате PNG (без сжатия)')


@dp.message_handler(state=States.STATE_3, content_types=ContentTypes.TEXT)
async def not_doc_txt_back_background_handler(message):
    await bot.send_message(message.from_user.id, text='Я жду документ...')


@dp.message_handler(state=States.STATE_3, content_types=ContentTypes.PHOTO)
async def not_doc_photo_back_background_handler(message):
    await bot.send_message(message.from_user.id, text='Нет, вы не поняли, надо "как документ" без сжатия')


@dp.message_handler(state=States.STATE_3, content_types=ContentTypes.DOCUMENT)
async def back_background_handler(message):
    if document := message.document:
        await document.download(destination_file='{}{}_bingo_back.png'.format(input_dir, message.from_user.id))

    state = dp.current_state(user=message.from_user.id)
    await state.set_state(States.all()[4])
    await bot.send_message(message.from_user.id,
                           text='Введите количество карточек от 1 до {}'.format(config.max_card_cnt))


@dp.message_handler(state=States.STATE_4)
async def print_handler(message):
    try:
        cnt_card = int(message.text)
    except ValueError:
        await bot.send_message(message.from_user.id, text='{}\nЭто не похоже на число'.format(message.text))
    else:
        if 0 < cnt_card <= config.max_card_cnt:
            await bot.send_message(message.from_user.id, text='Дождитесь формирования файла... Одну-две минутки')

            state = dp.current_state(user=message.from_user.id)
            _user = str(message.from_user.id)
            _data = state.storage.data[_user][_user]['data']
            cur_songs, cur_win_songs = _data['cur_songs'], _data['cur_win_songs']
            pf_name = print_cards(cur_songs, cur_win_songs, _user, cnt_card)
            logging.info('Файл {} готов!'.format(pf_name))

            await t_client.start(bot_token=config.bot_token.get_secret_value())
            await t_client.send_file(message.chat.id, '{}{}'.format(input_dir, pf_name))
            await t_client.disconnect()
            logging.info('Файл {} отправлен пользователю'.format(pf_name))

            await bot.send_message(message.from_user.id, text='Приятно было с вами поработать')
        else:
            await bot.send_message(message.from_user.id, text='Нет, давайте от 1 до {}'.format(config.max_card_cnt))


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
