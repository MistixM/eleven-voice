# Import dependencies
from aiogram import Bot, Dispatcher, types, Router

from aiogram.filters import CommandStart, Command
from aiogram.types import FSInputFile

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

# Utils
from utils.eleven_voice import text_to_speech
from utils.inline import settings_keyboard
from utils.datetime_filter import replace_time

import os 
import asyncio
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

# Initialize bot
dp = Dispatcher()
router = Router()
dp.include_router(router)
bot = Bot(token=config['Main']['TELEGRAM_BOT_TOKEN'])


# Users data
users_data_list = {}

# FSM states
class Settings(StatesGroup):
    edit_voice_id = State()
    edit_stability = State()
    edit_similarity = State()
    edit_style = State()
    edit_speed = State()
    edit_eleven_api = State()

# User class
class User():
    def __init__(self, user_id: int):
        
        # Default values
        self.user_id = user_id
        self.voice_id = 'pNInz6obpgDQGcFmaJgB'
        self.stability = 0.0
        self.similarity_boost = 1.0
        self.style = 0.0
        self.speed = 1.0
        self.eleven_api = config['Main']['ELEVEN_API']

# Handles /start command
# Send greeting message and propose available commands
@router.message(CommandStart())
async def handle_start(msg: types.Message):
    user_id = msg.chat.id

    if not user_id == int(config["Main"]['ADMIN_ID']):
        return

    bot_info = await bot.get_me()

    if not user_id in users_data_list:
        users_data_list[user_id] = User(user_id)
    
    await msg.answer(f"<b>Hey! I'm a {bot_info.first_name}!</b> 👋🏻 I can convert your text to speech. Send me a message to get started!\n\nTo configure settings, use /settings",
                     parse_mode='HTML')


# Settings handler
# Send available settings to user
@router.message(Command(commands=['settings']))
async def handle_settings(msg: types.Message):
    kb = settings_keyboard()
    user_id = msg.chat.id 

    if not user_id == int(config["Main"]['ADMIN_ID']):
        return
    
    if user_id not in users_data_list:
        users_data_list[user_id] = User(user_id)
    
    # Get data from the class and send it to the user
    user_data = users_data_list[user_id]

    await msg.answer(text=f"Here you can setup bot settings:\n\n<b>Voice ID:</b> {user_data.voice_id}\n<b>Stability:</b> {user_data.stability}\n<b>Similarity:</b> {user_data.similarity_boost}\n<b>Style:</b> {user_data.style}\n<b>Speed:</b> {user_data.speed}\n<b>ElevenLab API:</b> {user_data.eleven_api}\n\nClick the button below to adjust option.", 
                     reply_markup=kb,
                     parse_mode='HTML')


# Callback handler
# Generally used to handle settings changes
@router.callback_query(lambda d: d.data)
async def handle_callbacks(callback: types.CallbackQuery, state: FSMContext):
    data = callback.data

    if data == 'edit_voice_id':
        await callback.message.answer("Send me a new voice ID (20 characters)")
        await state.set_state(Settings.edit_voice_id)
    elif data == 'edit_stability':
        await callback.message.answer("Send me a new stability value (greater or equal to 0.0 and lower or equal to 1.0)")
        await state.set_state(Settings.edit_stability)
    elif data == 'edit_similarity':
        await callback.message.answer("Send me a new similarity value (greater or equal to 0.0 and lower or equal to 1.0)")
        await state.set_state(Settings.edit_similarity)
    elif data == 'edit_style':
        await callback.message.answer("Send me a new style value (greater or equal to 0.0 and lower or equal to 1.0)")
        await state.set_state(Settings.edit_style)
    elif data == 'edit_speed':
        await callback.message.answer("Send me a new speed value (greater or equal to 0.7 and lower or equal to 1.2)")
        await state.set_state(Settings.edit_speed)
    elif data == 'edit_eleven_api':
        await callback.message.answer("Send me a new ElevenLab API key")
        await state.set_state(Settings.edit_eleven_api)

# Edit voice ID state handler
# Checks its length and updates the value
@router.message(Settings.edit_voice_id)
async def handle_voice_id(msg: types.Message, state: FSMContext):
    user_id = msg.chat.id
    user_data = users_data_list[user_id]
    data = msg.text

    if not len(data) == 20:
        await msg.answer("Voice ID is too short")
        return

    user_data.voice_id = data

    await msg.answer("Voice ID updated!")
    await state.clear()


# Edit stability state handler
# Checks if the value is a number and updates the value
@router.message(Settings.edit_stability)
async def handle_stability(msg: types.Message, state: FSMContext):
    user_id = msg.chat.id
    user_data = users_data_list[user_id]

    try:
        data = float(msg.text)
    except ValueError:
        await msg.answer("Stability value must be a number")
        return
    
    # Basic check (according to API requirements)
    if data > 1.0 or data < 0.0:
        await msg.answer("Stability value must be between 0 and 1")
        return

    user_data.stability = data

    await msg.answer("Stability updated!")
    await state.clear()


# Edit similarity state handler
# Checks if the value is a number and updates the value
@router.message(Settings.edit_similarity)
async def handle_similarity(msg: types.Message, state: FSMContext):
    user_id = msg.chat.id
    user_data = users_data_list[user_id]

    try:
        data = float(msg.text)
    except ValueError:
        await msg.answer("Similarity value must be a number")
        return

    # According to an API checks ranges
    if data > 1.0 or data < 0.0:
        await msg.answer("Similarity value must be between 0 and 1")
        return

    user_data.similarity_boost = data

    await msg.answer("Similarity updated!")
    await state.clear()


# Edit style state handler
@router.message(Settings.edit_style)
async def handle_style(msg: types.Message, state: FSMContext):
    user_id = msg.chat.id
    user_data = users_data_list[user_id]
    try:
        data = float(msg.text)
    except ValueError: 
        await msg.answer("Style value must be a number")
        return

    # According to an API checks ranges
    if data > 1.0 or data < 0.0:
        await msg.answer("Style value must be between 0 and 1")
        return

    user_data.style = data

    await msg.answer("Style updated!")
    await state.clear()

# Edit speed state handler
@router.message(Settings.edit_speed)
async def handle_speed(msg: types.Message, state: FSMContext):
    user_id = msg.chat.id
    user_data = users_data_list[user_id]
    try:
        data = float(msg.text)
    except Exception as e:
        await msg.answer("Speed value must be a number")
        return

    # According to an API checks ranges
    if data > 1.2 or data < 0.7:
        await msg.answer("Speed value must be between 0.7 and 1.2")
        return
    
    user_data.speed = data

    await msg.answer("Speed updated!")
    await state.clear()

# Edit ElevenLab API state handler
@router.message(Settings.edit_eleven_api)
async def handle_eleven_api(msg: types.Message, state: FSMContext):
    data = msg.text
    user_id = msg.chat.id 

    config.set('Main', 'ELEVEN_API', data)
    
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

    if user_id in users_data_list:
        users_data_list[user_id].eleven_api = data
    
    await msg.answer("ElevenLab API key updated!")
    await state.clear()


# Message handler.
# Important to have this handler at the end of the file.
# DO NOT move this block of code to the top, the bot will not work correctly.
@router.message(lambda msg: not msg.text.startswith('/'))
async def handle_message(msg: types.Message, state: FSMContext):
    user_id = msg.chat.id
    text = msg.text

    if not user_id == int(config["Main"]['ADMIN_ID']):
        return

    # If state is not None return to prevent issues
    if await state.get_state() is not None:
        return


    if not user_id in users_data_list:
        users_data_list[user_id] = User(user_id)
    
    user_data = users_data_list[user_id]
    file = None

    if "{time}" in msg.text:
        text = replace_time(msg.text)
    
    # Try to convert text to speech
    try:
        file = text_to_speech(text=text,
                              voice_id=user_data.voice_id,
                              stability=user_data.stability,
                              similarity=user_data.similarity_boost,
                              style=user_data.style,
                              speed=user_data.speed)
        
        # Check file and send it to the user
        if file:
            await msg.answer_document(FSInputFile(file))
            os.remove(os.path.join(os.curdir, file))
        else:
            print(f"Error occured while converting text to speech: {file}") # for debugging
            await msg.answer("Error occured while converting text to speech")

    except Exception as e:
        print(f"An error occured: {e}")
        await msg.answer(e.body.get('detail', {}).get('message'))
        os.remove(os.path.join(os.curdir, file))


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    print("Bot started!")

    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot stopped!")
