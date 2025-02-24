# This file contains the inline keyboard for the bot
# Please add new inline keyboards here.

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def settings_keyboard() -> InlineKeyboardMarkup:
    
    # Generate an inline keyboard 
    kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Voice ID", callback_data="edit_voice_id"), InlineKeyboardButton(text="Stability", callback_data="edit_stability")],
                                               [InlineKeyboardButton(text="Similarity", callback_data="edit_similarity"), InlineKeyboardButton(text="Style", callback_data="edit_style")],
                                               [InlineKeyboardButton(text="Speed", callback_data="edit_speed"), InlineKeyboardButton(text="ElevenLab API", callback_data="edit_eleven_api")]])
    return kb

