import requests
import os
import telebot
import asyncio
import threading
import time
import logging

format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

def save_actual_ip(actual_ip):
    with open("ip.txt", "w") as ipfile:
        ipfile.write(actual_ip)

def get_actual_ip():
    with open("ip.txt", "r") as ipfile:
        actual_ip = ipfile.read()
    
    return actual_ip

def save_last_ip(ip_received):
    actual_ip = get_actual_ip().strip()

    if actual_ip != ip_received:
        save_actual_ip(ip_received)
        return True

    return False

def get_external_ip():
    ip = requests.get('https://api.ipify.org?format=json')
    ret_ip = ip.json()['ip']
    return ret_ip

def send_message_to_chat(bot, chat):
    ip = get_external_ip()
    changed = save_last_ip(ip)

    if changed:
        bot.send_message(chat, f"O IP mudou, novo IP: {ip}")

def thread_func(bot, chat):
    while True:
        logging.info("Checking IP")
        send_message_to_chat(bot, chat)
        time.sleep(300)

BOT_TOKEN = ""

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'hello', 'ola'])
def send_welcome(message):
    print(message.chat.id)
    bot.reply_to(message, "Opa, tudo bem?")

@bot.message_handler(commands=['ip'])
def send_welcome(message):
    try:
        ip = get_external_ip()
        print(message.chat.id)
        if message.chat.id == -947283941:
            bot.reply_to(message, f"O novo ip é {ip}")
        else:
            bot.reply_to(message, f"Você não esta na lista de quem pode receber essa informação.")
    except Exception as e:
        bot.reply_to(message, f"Houve um problema, entre em contato com o administrador")

#x = threading.Thread(target=thread_func, args=(bot, -947283941))
#x.start()

bot.infinity_polling()
