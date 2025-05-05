
import telebot
import subprocess
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=["start"])
def start(msg):
    bot.send_message(msg.chat.id, "Welcome to WebScan Pro Bot!")

@bot.message_handler(commands=["scan"])
def scan(msg):
    try:
        url = msg.text.split(maxsplit=1)[1]
    except IndexError:
        bot.send_message(msg.chat.id, "Please provide a URL: /scan https://example.com")
        return

    bot.send_message(msg.chat.id, f"Scanning {url} with SQLMap...")
    try:
        result = subprocess.check_output(["python3", "sqlmap/sqlmap.py", "-u", url], stderr=subprocess.STDOUT, text=True)
        bot.send_message(msg.chat.id, f"Scan complete:\n{result[:4000]}")
    except subprocess.CalledProcessError as e:
        bot.send_message(msg.chat.id, f"Error during scan:\n{e.output[:4000]}")

bot.polling()
