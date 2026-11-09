import os
import discord
from discord import app_commands
from dotenv import load_dotenv

load_dotenv()

GUILD = discord.Object(id=int(os.environ["GUILD_ID"]))

client = discord.Client(intents=discord.Intents.default())
tree = app_commands.CommandTree(client)

@tree.command(name="ping", description="Testet, ob der Bot lebt")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong! 🏓")

@client.event
async def on_ready():
    print(f"Eingeloggt als {client.user}")
    print("Server:", [g.name for g in client.guilds])
    tree.copy_global_to(guild=GUILD)
    synced = await tree.sync(guild=GUILD)
    print(f"{len(synced)} Command(s) synchronisiert:", [c.name for c in synced])

client.run(os.environ["DISCORD_TOKEN"])