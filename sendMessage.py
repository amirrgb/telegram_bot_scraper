import configparser
import json
import asyncio
import arabic_reshaper
from datetime import date, datetime
from bidi.algorithm import get_display
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.types import PeerChannel
# from pyrogram import Client
# from pyrogram import filters

#for persian and arabic
def convertor(text:str,printer=True):
    words=text.split()
    for word in words[::-1]:
        if printer:
            print(get_display(arabic_reshaper.reshape(word)),end=" ")
        else:
            return get_display(arabic_reshaper.reshape(word))


global contacts
contacts :dict={}
global clients
clients :dict={}
# Reading Configs

def clientMaker():
    config = configparser.ConfigParser()
    for i in range(1,3):
        config.read("config%s.ini"%(i))
        # Setting configuration values
        api_id = config['Telegram']['api_id']
        displayName=str(config["Telegram"]["name"])
        api_hash = config['Telegram']['api_hash']
        api_hash = str(api_hash)
        global phone
        phone = config['Telegram']['phone']
        username = config['Telegram']['username']
        # Create the client and connect
        clients[displayName]=TelegramClient(username, api_id, api_hash)


async def use(client):
    while True:
        i=input("1.for send message\n2.break\n")
        if "2" in i:break
        if i == "1":
            n=input("1.with name\n2.with username\n")
            if "1" in n:
                name=input("name:")
                if name in contacts:
                    ok=input("is it %s?\n"%(convertor(contacts[name].first_name,printer=False)))
                    if "y" in ok:
                        await client.send_message(contacts[name],input("message:"))
                else:
                    print("name not found")
            if "2" in n:
                username=input("username:")
                newContact = await client.get_entity(username)
                await client.send_message(newContact,input("message:"))
                contacts[username]=newContact
            print("sent")


async def main(phone,which):
    await clients[which].start()
    print("Clients[which] Created")
    # Ensure you're authorized
    if await clients[which].is_user_authorized() == False:
        await clients[which].send_code_request(phone)
        try:
            await clients[which].sign_in(phone, input('Enter the code: '))
        except SessionPasswordNeededError:
            await clients[which].sign_in(password=input('Password: '))


    contacts["mamad"]=await clients[which].get_entity("Mab1010")
    contacts["me"]=await clients[which].get_me()
    contacts["foodGroup"]=await clients[which].get_entity("https://t.me/+dJN6hF1hd201MDhk")
    await use(clients[which])


clientMaker()


while True:
    which=input("which account?\n")
    if which == "end":break
    with clients[which]:
        clients[which].loop.run_until_complete(main(phone,which))



