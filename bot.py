import os
import asyncio
import threading
from flask import Flask
import discord

# --- MINI WEBSITE / WEB SERVER FOR UPTIMEROBOT ---
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive and running!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

def keep_alive():
    t = threading.Thread(target=run_web)
    t.daemon = True
    t.start()
# ------------------------------------------------

# --- DISCORD BOT SETUP ---
bot = discord.Bot(intents=discord.Intents.default())

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("Bot is ready and online!")

@bot.slash_command(
    name="deepocean",
    description="Announce the deep ocean invite a specified number of times.",
    integration_types={
        discord.IntegrationType.guild_install,
        discord.IntegrationType.user_install,
    },
    contexts={
        discord.InteractionContextType.guild,
        discord.InteractionContextType.bot_dm,
        discord.InteractionContextType.private_channel,
    },
)
async def deep_ocean(
    ctx: discord.ApplicationContext,
    count: discord.Option(
        int,
        "How many times should the bot say it? (1-50)",
        required=False,
        default=1,
        min_value=1,
        max_value=50,
    ),
):
    await ctx.defer(ephemeral=True)

    message_text = "@everyone\n# join deep ocean\n# https://discord.gg/SX7ZK5ucHJ"

    for _ in range(count):
        await ctx.channel.send(message_text)
        await asyncio.sleep(1)  # avoid rate limits

    await ctx.followup.send(
        f"Successfully sent the message {count} time(s)!", ephemeral=True
    )

# Run the mini web server in the background first
if __name__ == "__main__":
    keep_alive()
    bot.run(os.environ["DISCORD_TOKEN"])
