import os
from discord.ext import commands
import discord

intents = discord.Intents.all()
client = commands.Bot(command_prefix="!", intents=intents)

def get_client():
    return client

def run_client():
    client.run(os.environ['TOKEN'])