import discord
from discord.ext import commands
from discord.ui import Button, View
import datetime
import os
from flask import Flask
from threading import Thread

# --- خادم الويب للتشغيل المستمر ---
app = Flask('')

@app.route('/')
def home():
    return "M7M HUB Bot is Online 24/7!"

def run_web():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run_web)
    t.start()

# --- إعدادات البوت ---
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True
intents.moderation = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ⚠️ ضع هنا آيدي الرومات الخاصة بسيرفرك ⚠️
LOGS_CHANNEL_ID = 123456789012345678      # آيدي روم اللوقات
TICKET_CATEGORY_ID = 123456789012345678   # آيدي كاتيجوري التكتات

user_actions = {}
ACTION_LIMIT = 3
ACTION_WINDOW = 10

# --- نظام التكت ---
class CloseTicketView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="إغلاق التكت 🔒", style=discord.ButtonStyle.red, custom_id="close_ticket")
    async def close_ticket(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message("سيتم إغلاق التكت خلال 5 ثوانٍ...")
        await discord.utils.sleep_until(datetime.datetime.now() + datetime.timedelta(seconds=5))
        await interaction.channel.delete()

class TicketView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="فتح تكت 📩", style=discord.ButtonStyle.green, custom_id="open_ticket")
    async def open_ticket(self, interaction: discord.Interaction, button: Button):
        guild = interaction.guild
        category = guild.get_channel(TICKET_CATEGORY_ID)
        
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }
        
        channel = await guild.create_text_channel(
            name=f"ticket-{interaction.user.name}",
            category=category,
            overwrites=overwrites
        )
        
        embed = discord.Embed(title="🎫 تكت جديد", description=f"مرحباً {interaction.user.mention}، اطرح استفسارك هنا.", color=discord.Color.gold())
        await channel.send(embed=embed, view=CloseTicketView())
        await interaction.response.send_message(f"تم إنشاء التكت: {channel.mention}", ephemeral=True)

@bot.command()
@commands.has_permissions(administrator=True)
async def setup_ticket(ctx):
    embed = discord.Embed(title="👑 نظام الدعم الفني", description="اضغط لفتح تكت جديد.", color=discord.Color.gold())
    await ctx.send(embed=embed, view=TicketView())

# --- نظام السيستم ---
@bot.event
async def on_message(message):
    if message.author.bot: return
    if "سستم" in message.content.lower() or message.content.startswith("!سستم"):
        embed = discord.Embed(title="⚙️ نظام M7M", description="السيستم يعمل بنجاح!", color=discord.Color.green())
        await message.channel.send(embed=embed)
    await bot.process_commands(message)

# --- نظام اللوقات ---
@bot.event
async def on_message_delete(message):
    if message.author.bot: return
    log_channel = bot.get_channel(LOGS_CHANNEL_ID)
    if log_channel:
        embed = discord.Embed(title="🗑️ رسالة محذوفة", color=discord.Color.red())
        embed.add_field(name="العضو:", value=message.author.mention)
        embed.add_field(name="المحتوى:", value=message.content or "بدون نص")
        await log_channel.send(embed=embed)

# --- التشغيل ---
@bot.event
async def on_ready():
    bot.add_view(TicketView())
    bot.add_view(CloseTicketView())
    print(f"✅ البوت يعمل: {bot.user}")

keep_alive()
TOKEN = os.getenv("DISCORD_TOKEN")
bot.run(TOKEN)
