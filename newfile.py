import telebot
from yt_dlp import YoutubeDL
import os

TOKEN = "8628355750:AAGqT2SsTft1sfgnmRZfXMo--XMEJFSt3Tc"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Salom! Menga istalgan qo'shiq nomini yozib yubor, men uni YouTube'dan topib audio formatida yuboraman 🎵")

@bot.message_handler(func=lambda message: True)
def search_and_download_song(message):
    query = message.text
    msg = bot.reply_to(message, f"🔍 '{query}' bo'yicha qo'shiq qidirilmoqda va yuklab olinmoqda, biroz kuting...")
    
    output_filename = "song.m4a"
    
    # Eskidan qolgan fayl bo'lsa o'chirib tashlaymiz
    if os.path.exists(output_filename):
        try:
            os.remove(output_filename)
        except:
            pass
    
    try:
        # FFmpeg talab qilmaydigan to'g'ridan-to'g'ri audio yuklash rejimi
        ydl_opts = {
            'format': 'bestaudio[ext=m4a]/bestaudio/best',
            'outtmpl': output_filename,
            'default_search': 'ytsearch1',
            'noplaylist': True,
        }
        
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([query])
            
        with open(output_filename, 'rb') as audio:
            bot.send_audio(message.chat.id, audio, caption=f"🎧 {query}")
            
        bot.delete_message(message.chat.id, msg.message_id)
        
    except Exception as e:
        bot.reply_to(message, f"❌ Xatolik yuz berdi: {str(e)}")

bot.infinity_polling()
