import flet as ft
import json
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message
from multiprocessing import Process, freeze_support
import re


with open('setting.json') as f:
    data = json.load(f)
    Token = data["Token"]
    ChatID = data["Channel"]
    
dp = Dispatcher()
bot = Bot(token=Token)

def runbot():
    async def mainbot():
        await dp.start_polling(bot)
    asyncio.run(mainbot())

async def savejson(value):
    with open('setting.json') as f:
            data = json.load(f)
            data["Channel"] = value
    with open('setting.json', 'w') as f:
        json.dump(data, f, indent=4)


async def send_message(сhat_id: int, text: str):
    await bot.send_message(сhat_id, text)

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    ID = message.chat.id
    await message.answer(f"Привіт! ID: " + (str)(ID))


    
def runflet():
    def main(page: ft.Page):
        page.title = "Hazeikyn - Bot Message"
        page.window.height = 600
        page.window.width = 400
        page.theme_mode = ft.ThemeMode.DARK
        page.window.icon = './icon.ico'



        async def button_clicked(e):
            text_tb1 = tb1.value
            if text_tb1 == "":
                logs_text.value = f"Ви нічого не написали"
            if re.search(r'[a-zA-Zа-яА-Я]', ChatID):
                logs_text.value = f"Ви неправильно вказали ID каналу"
            else:
                logs_text.value = f"Повідомлення було надіслано"
                await send_message(ChatID, text_tb1)
            page.update()
        
            
        logs_text = ft.Text()
        tb1 = ft.TextField(label="Текст", multiline=True, min_lines=1, max_lines=16)
        btn_send = ft.ElevatedButton("Надіслати",
                                width=400,
                                    on_click=button_clicked
                                    )
        


        def themewhite(e):
            page.theme_mode = ft.ThemeMode.LIGHT
            page.update()

        def themeblack(e):
            page.theme_mode = ft.ThemeMode.DARK
            page.update()  

        Theme_Selector = ft.PopupMenuButton(
            tooltip="",
            items=[
                ft.ElevatedButton(text="Біла тема", on_click=themewhite),
                ft.ElevatedButton(text="Чорна тема", on_click=themeblack)
            ]
        )

        Field_ChatID = ft.TextField(label="Чат ID", max_lines=1, value=ChatID)

        async def save_field_id(e):
            await savejson(Field_ChatID.value)

        bs = ft.BottomSheet(
            content=ft.Container(
                padding=50,
                content=ft.Column(
                    tight=True,
                    controls=[
                        ft.ElevatedButton("Зберегти", on_click=save_field_id),
                        Field_ChatID
                    ],
                ),
            ),
        )
        
        cid = ft.ElevatedButton(text="Змінити ChatID", on_click=lambda _: page.open(bs))
                

        page.add(
            Theme_Selector,
            tb1,
            btn_send,
            cid,
            logs_text
            
        )


    ft.app(main)



if __name__ == '__main__':
    freeze_support()
    process2 = Process(target=runflet)
    process1 = Process(target=runbot)

    process1.start()
    process2.start()


    process1.join()
    process2.join()

