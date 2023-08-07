from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from config import tg_bot_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1nL_E3Ut0CoEqFSI4EcxJxAujG1naqvX5j8bV0X8Kyvo'
SAMPLE_RANGE_NAME = 'Test list!A2:C'


bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply('Hi, enter your message here')


@dp.message_handler()
async def handle_message(message: types.Message):
    # Получаем имя пользователя
    user_name = message.chat.username
    # Получаем текс сообщения
    text_message = message.text
    # Получаем дату отправки сообщения
    forward_date = message.date
    # Получаем id чата с ботом
    chat_id = message.chat.id
     # Сохраняем значения для передачи в функцию записи в таблицу
    value = [[str(user_name),str(text_message),str(forward_date)]]
    # Вызываем функцию записи значений в таблицу и сохраняем в переменную check результат выполнения (либо Ok либо текс ошибки)
    check = write_data(value)
    
    # Проверяем удачная была попытка или нет
    if check == 'Ok':
        # Если все Ок, отвечаем в чате, что сообщение сохранено в таблице
        await bot.send_message(chat_id, 'Message was write in table\nhttps://docs.google.com/spreadsheets/d/1nL_E3Ut0CoEqFSI4EcxJxAujG1naqvX5j8bV0X8Kyvo/edit?usp=sharing')
    else:
        # Если произошла ошибка, то записываем дату и текст ошибку в файл log.txt
        await bot.send_message(chat_id, 'Something went wrong')
        
        with open('log.txt', 'a') as file:
            file.write(f'{forward_date} {str(check)}\n')



def write_data(data):
    creds = None
    
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    
    try:
        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        # Записываем данные в таблицу
        response = sheet.values().append(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME, valueInputOption="RAW", body={'values' : data }).execute()
        return 'Ok'

    except HttpError as err:
        return err


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)