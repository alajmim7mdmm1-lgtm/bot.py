import os
import discord
from discord.ext import commands
from flask import Flask
from threading import Thread

# --- خادم الويب للتشغيل المستمر 24/7 ---
app = Flask('')

@app.route('/')
def home():
    return "M7M HUB Bot is Online 24/7!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- إعدادات البوت والـ Intents ---
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'تم تسجيل الدخول بنجاح باسم: {bot.user}')

# --- 1. الرد الآلي ونظام الكلمات المفتاحية ---
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content.strip() == "سستم" or message.content.startswith("!سستم"):
        await message.channel.send("أهلاً بك في نظام الدعم الآلي! أرسل استفسارك وسنقوم بمساعدتك.")

    await bot.process_commands(message)

# --- 2. نظام اللوقات (Logs) ---
@bot.event
async def on_message_delete(message):
    print(f"لوق: تم حذف رسالة من {message.author}: {message.content}")

# --- 3. أمر الحماية والإدارة (طرد/حظر) ---
@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f"تم طرد العضو {member.mention} بنجاح.")

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f"تم حظر العضو {member.mention} بنجاح.")

# --- تشغيل خادم الويب والبوت ---
keep_alive()
bot.run(os.getenv('DISCORD_TOKEN'))
