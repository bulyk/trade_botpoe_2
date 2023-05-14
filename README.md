# trade_botpoe_2

[https://www.youtube.com/watch?v=0RDvuULShM8](https://www.youtube.com/watch?v=BOdEPLgEvHI)

This program allows you to duplicate messages received from the Path of Exile game in the Telegram chat, this will let you always know when someone wants to buy something from you. If you do not have access to a computer, then you can always use remote access programs: remotedesktop.google, TeamViewer, etc.

Differences from the previous bot https://github.com/bulyk/trade_alert_botpoe/pulls

used libraries:
win32gui
PIL
pyautogui
time
requests
tkinter
copy
asyncio
aiogram
pyperclip
keyboard

1. Added anti afk system
2.Switching to the working window of the game
3.Using the POE API allows you to find an item in a stashe (the bot will find the item itself and put it in your inventory)
4.Added auto-clearing stasha when receiving a message
5. Added an invite button to the telegram bot that will allow you to invite a person to a party and get an item of interest from the stesh
