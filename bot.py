import os
from dotenv import load_dotenv
from discord import app_commands

load_dotenv()

GUILD = discord.Object(id=int(os.environ["GUILD_ID"]))

bambu = BambuPrinter(
    os.environ["BAMBU_IP"],
    os.environ["BAMBU_SERIAL"],
    os.environ["BAMBU_ACCESS_CODE"],
)

client = discord.Client(intents=discord.Intents.default())
tree = app_commands.CommandTree(client)

client.run(os.environ["DISCORD_TOKEN"])