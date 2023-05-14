import time
from tkinter import *
from tkinter import ttk
import copy
import asyncio
from aiogram import Bot, Dispatcher, executor, types
import pyautogui
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import pyperclip
from PIL import ImageGrab, ImageChops, Image
import win32gui
from stash_search import Stash
import keyboard

hwnd = win32gui.FindWindow(None, "Path of Exile")
past_line = []
past_line_afk = []
waiting_join = 6

def exit_action(icon):
    icon.visible = False
    icon.stop()
bot_token = "5845477607:AAEtus14W-ZTRu2df0zwp6Reu-YisrHmuws"
url = "https://api.telegram.org/bot"
bot = Bot(bot_token)
dp = Dispatcher(bot)

# Создаем клавиатуру с одной кнопкой "Старт"
inv_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('/inv'))
#start_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('/start'))

# Обработчик команды "/start"
@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    await message.answer("Привет! Я запущен.", reply_markup=inv_keyboard)
    await check_for_stop(message)
global stopped
stopped = False
# Обработчик команды "/stop"
@dp.message_handler(commands=['inv'])
async def stop_handler(message: types.Message):
    global stopped
    stopped = True
    await message.answer("Остановлено.", )

invite = ""
# Бесконечный цикл
async def check_for_stop(message: types.Message):
    global stopped
    while stopped == False:
        if stopped:
            break  # прерываем цикл при получении команды /stop
        global file_path
        file = open(file_path, 'r', encoding='utf-8')
        last_line = file.readlines()[-1]
        time.sleep(.1)
        file.close() 
        if '@From' in last_line:
            global past_line
            # print (last_line)
            if last_line != past_line:
                time.sleep(.1)
                trade_msg = last_line
                print(trade_msg)
                past_line = copy.copy(last_line)
                print('past'+past_line)
                await bot.send_message(chatid, past_line)
                global invite
                invite = ('/invite'+str(past_line.split('@From')[-1].split(':')[0]))
                base_x = int(1295)
                base_y = int(615)
                stash = Stash(base_x, base_y)
                try:
                    Stash.click_stash()
                    stash.clear()
                except:
                    await bot.send_message(chatid, 'Стешь не смог очистить мда')
                break
                
                # with open(file_path,'a',  encoding='utf-8', ) as file:
                #     file.write('@From invite\n')
            else:
                time.sleep(.02)  
        elif "AFK mode is now ON" in last_line:
            global past_line_afk
            time.sleep(.1)
            try:
                Stash.click_stash()
                await bot.send_message(chatid, "antiAFK")
            except:
                time.sleep(20)
                await bot.send_message(chatid, "стешь не нашел пиздос")
        else:
            time.sleep(.1)

        
    await asyncio.sleep(12)
    if stopped == True:
        win32gui.SetForegroundWindow(hwnd)    
        time.sleep(.1)
        pyautogui.press('Enter')
        if '>' in invite:
            invite = '/invite'+str(invite.split('>')[-1])
            trade_request = '/tradewith'+str(invite.split('>')[-1])
        else:
            pass

        time.sleep(.5)
        keyboard.write('/leave')
        time.sleep(.5)
        pyautogui.press('Enter')
        time.sleep(.5)
        pyautogui.press('Enter')
        pyperclip.copy(invite)
        time.sleep(.5)
        keyboard.write(invite)
        time.sleep(.5)
        pyautogui.press('Enter')
        print (invite)
        time.sleep(.4)
        pyautogui.press('s')
        time.sleep(1)

        await bot.send_message(chatid, 'пробуем приглосить в пати')
        wait_party()
        pyautogui.moveTo(350,180)
        pyautogui.click()
        time.sleep(1)

        while stopped == True:
            time.sleep(2)
            location = pyautogui.locateOnScreen('join.png')
            if location is not None:
                # Если маленькое изображение найдено, вызываем функцию1()
                await bot.send_message(chatid, 'Он в пати епта')
                try:
                    Stash.click_stash()
                    search_tab = past_line.split('stash tab "')[1].split('"')[0]
                    position_x = int(past_line.split('left ')[1].split(',')[0])-1
                    position_y = int(past_line.split(', top ')[1].split(')')[0])-1
                    number_tab = stash.stesh_tabs(0, 0, search_tab)[0]
                    quantity_all_tab = stash.stesh_tabs(0, 0, search_tab)[1]
                    base_x = 39
                    base_y = 155
                    x_coord = base_x+position_x*52
                    y_coord = base_y+position_y*52
                    n = 0
                    print('all_tab '+str(quantity_all_tab))
                    print('number_tab '+str(number_tab))
                    while n <= quantity_all_tab:
                        pyautogui.press('left')
                        time.sleep(.1)
                        n += 1
                    n = 1
                    while n <= number_tab:
                        pyautogui.press('right')
                        time.sleep(.1)
                        n += 1  
                    pyautogui.moveTo(x_coord, y_coord)   
                    time.sleep(.5)
                    pyautogui.keyDown('ctrl') 
                    time.sleep(.1)
                    pyautogui.click(button='left') 
                    time.sleep(.1)
                    pyautogui.keyUp('ctrl') 
                except:
                    await bot.send_message(chatid, 'ты даже строку вырезать не смог')
                stopped = False
                break
            else:
                location = pyautogui.locateOnScreen('invitation.png')
                if location is not None:
                    await bot.send_message(chatid, 'Жду пока додик примет пати')
                else:
                    await bot.send_message(chatid, 'Сделки не будет')
                    stopped = False
                    break
        await check_for_stop(message)


    else:
        stopped = False
        await check_for_stop(message)
    
def wait_party():
        screen_party = ImageGrab.grab(bbox=(225,50,440,85))
        party_check = Image.open('party_check.png')
        diff = ImageChops.difference(screen_party, party_check)
        bbox = diff.getbbox()
        if bbox is None or (bbox[2] - bbox[0]) * (bbox[3] - bbox[1]) <= 80: #если изобаржения сопадают
            pass
        else:
            time.sleep(.1)
            pyautogui.press('s')


#Chatid
text1 = []
text2 = []
def show_message():
    label["text"] = 'Нажми крестик'    
    global text1
    text1 = entry.get() 
    entry.delete(0, END)
    chatid_txt = open("chatid.txt", "w+")
    chatid_txt.write(text1)
    chatid_txt.close()

try:
    chatid_txt = open('chatid.txt', 'r')
    text1 = chatid_txt.readlines()[0]
    chatid_txt.close() 
    print(text1)

except:
    root = Tk()
    root.title("Trade_alert_poebot")
    root.geometry("350x150") 

    instruction = ttk.Label()
    instruction["text"] = 'Введите чат ID'
    instruction.pack(anchor=NW, padx=6, pady=6)

    entry = ttk.Entry()
    entry.pack(anchor=NW, padx=6, pady=6)

    btn = ttk.Button(text="Click", command = show_message)
    btn.pack(anchor=NW, padx=6, pady=6)

    label = ttk.Label()
    label.pack(anchor=NW, padx=6, pady=6)

    root.mainloop()
#Путь к логам
def path_file():
    label["text"] = 'Нажми крестик'    
    global text2
    text2 = entry.get() 
    entry.delete(0, END)
    file_path_txt = open("file_path.txt", "w+")
    file_path_txt.write(text2)
    file_path_txt.close()

try:
    file_path = open('file_path.txt', 'r')
    text2 = file_path.readlines()[0]
    file_path.close() 
    print(text2)

except:
    root = Tk()
    root.title("Trade_alert_poebot")
    root.geometry("350x150") 

    instruction = ttk.Label()
    instruction["text"] = 'Введите путь к файлу Client.txt\nПример: D:\Games\poe\logs\Client.txt'

    instruction.pack(anchor=NW, padx=6, pady=6)

    entry = ttk.Entry()
    entry.pack(anchor=NW, padx=6, pady=6)

    btn = ttk.Button(text="Click", command = path_file)
    btn.pack(anchor=NW, padx=6, pady=6)

    label = ttk.Label()
    label.pack(anchor=NW, padx=6, pady=6)

    root.mainloop()

chatid = text1
file_path = text2

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
# asyncio.run(send_welcome())
