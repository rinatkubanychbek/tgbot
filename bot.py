import aiogram
import os
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
import asyncio
import logging
from dotenv import load_dotenv
import requests
import json

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


def get_response(messages: list[dict]) -> str:
    response = requests.post(
    url="https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {os.environ.get('AI_TOKEN')}"
    },
    data=json.dumps({
        "model": "deepseek/deepseek-r1:free", 
        "messages": messages
    })
    )

    return response.json()['choices'][0]['message']['content']
router = Router()

messages = {} 

@router.message(CommandStart())
async def start(msg: Message) -> None:
    await msg.mark("Started")
@router.message(Command("help"))
async def help(msg: Message) -> None:
    await msg.answer("There's no help left...")


@router.message()
async def message_handler(msg: Message) -> None:
    if msg.chat.id not in messages.keys():
        messages[msg.chat.id] = []
    messages[msg.chat.id].append({'role': 'user', 'content': msg.text})
    response = get_response(messages[msg.chat.id])
    await msg.answer(response, parse_mode=ParseMode.MARKDOWN)

    
async def main():
    bot = aiogram.Bot(os.environ.get("TOKEN") )

    dp = aiogram.Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
