from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, File
from aiogram import Bot, Dispatcher
from aiogram.types import FSInputFile
from keyboards.all_kb import main_kb
import pytesseract
import os

start_router = Router()

@start_router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Запуск сообщения по команде /start используя фильтр CommandStart()',
                         reply_markup=main_kb(message.from_user.id))

# @start_router.message(F.photo)
# async def cmd_start_photo(message: Message):
#     await message.answer('Это фото!')

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

@start_router.message(F.text == "Печатный текст")
async def text_for_printed(message: Message):
    await message.answer("Пришлите фото для обработки в ответ на это сообщение")
    
# print(pytesseract.image_to_string(Image.open('example.png'), lang='rus'))

@start_router.message(F.photo)
async def process_photo(message: Message):
    if "Пришлите фото для обработки в ответ на это сообщение" in message.reply_to_message.text:
        try:
            from PIL import Image

            file_id = message.photo[-1].file_id

            bot = message.bot
            file: File = await bot.get_file(file_id)
            file_path = file.file_path 
            downloaded_file = await bot.download_file(file_path)

            #Сохраняем файл во временное хранилище
            local_file_path = "temp_photo.jpg"
            with open(local_file_path, "wb") as f:
                f.write(downloaded_file.getvalue())

            # Открываем изображение и распознаем текст
            image = Image.open(local_file_path)
            text = pytesseract.image_to_string(image, lang='rus')

            # Отправляем распознанный текст обратно в чат
            await message.answer(text)

            # Удаляем временный файл
            os.remove(local_file_path)

        except ImportError:
            await message.answer("Ошибка: библиотека PIL не установлена.")
        except Exception as e:
            await message.answer(f"Произошла ошибка: {e}")

@start_router.message(F.text)
async def cmd_start_text(message: Message):
    if message.text[0] == '1' or message.text[0] == '0':
        if message.text[1] == ' ':
            if message.text[2] == '1' or message.text[2] == '0':
                array = [message.text[0], message.text[2]]
                await message.answer(f'{array[0], array[1]}')
    else:
        await message.answer('Это текст!')
