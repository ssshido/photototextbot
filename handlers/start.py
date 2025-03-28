from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram import Bot, Dispatcher
from aiogram.types import FSInputFile
from keyboards.all_kb import main_kb
import pytesseract

start_router = Router()

@start_router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Запуск сообщения по команде /start используя фильтр CommandStart()',
                         reply_markup=main_kb(message.from_user.id))

@start_router.message(F.photo)
async def cmd_start_photo(message: Message):
    await message.answer('Это фото!')

@start_router.message(Command('images'))
async def upload_photo(message: Message):
    # Сюда будем помещать file_id отправленных файлов, чтобы потом ими воспользоваться
    file_ids = []

    # Отправка файла из файловой системы
    image_from_pc = FSInputFile('images/a368e7c2f460594ec50c42428d77b945.jpg')
    result = await message.answer_photo(
        image_from_pc,
        caption="Изображение из файла на компьютере"
    )
    file_ids.append(result.photo[-1].file_id)

@start_router.message (F.text == "📖 Печатный текст")
async def text_for_printed(message: Message):
    try:
        from PIL import Image
    except ImportError:
        await message.answer("Ошибка")
    await message.answer(pytesseract.image_to_string('example.png'), lang='rus')
# print(pytesseract.image_to_string(Image.open('example.png'), lang='rus'))

@start_router.message(F.text)
async def cmd_start_text(message: Message):
    if message.text[0] == '1' or message.text[0] == '0':
        if message.text[1] == ' ':
            if message.text[2] == '1' or message.text[2] == '0':
                array = [message.text[0], message.text[2]]
                await message.answer(f'{array[0], array[1]}')
    else:
        await message.answer('Это текст!')
