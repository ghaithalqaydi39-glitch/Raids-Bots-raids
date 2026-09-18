import os
import threading
from flask import Flask
import discord
from discord.ext import commands
from discord.commands import option

# --- MINI WEBSITE / WEB SERVER FOR UPTIMEROBOT ---
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive and running!"

def run_web():
    # Render assigns a port dynamically via environment variables, default to 8080 if not present
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

def keep_alive():
    t = threading.Thread(target=run_web)
    t.daemon = True
    t.start()
# ------------------------------------------------_

# --- DISCORD BOT SETUP ---
bot = discord.Bot(intents=discord.Intents.default())

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("Bot is ready and online!")

@bot.slash_command(
    name="deepocean",
    description="Announce '@everyone join deep ocean' a specified number of times."
)
@option(
    name="count",
    description="How many times should the bot say it? (1-50)",
    required=False,
    type=int,
    min_value=1,
    max_value=50
)
async def deep_ocean(ctx: discord.ApplicationContext, count: int = 1):
    await ctx.defer(ephemeral=True)
    
    message_text = "@everyone join deep ocean"
    for _ in range(count):
        await ctx.channel.send(message_text)
        
    await ctx.followup.send(f"Successfully sent the message {count} time(s)!", ephemeral=True)

# Run the mini web server in the background first
if __name__ == "__main__":
    keep_alive()
    # Run the bot using the token stored in Render's environment variables
    bot.run(os.environ["DISCORD_TOKEN"])
