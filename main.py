import os, discord, requests, json, ast
from dotenv import load_dotenv
from discord.ext import commands
from discord.utils import get

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")

# some variables
AUTHORIZED = ['Kartodix#2540']

# allow all intents
intents = discord.Intents.all()
client = commands.Bot(command_prefix="$", intents=intents)


@client.event
async def on_ready():
    print("> Client connected")


@client.command(name="update")
async def update(ctx):
    if str(ctx.message.author) in AUTHORIZED:
        print("[debug] - update triggered")

        guild = ctx.message.guild

        # GET DATA

        # - general info about the guild and the owner
        guild_id = guild.id
        guild_name = guild.name
        guild_ownerid = guild.owner_id
        guild_icon = guild.icon
        # print(f"guild id: {guild_id} - guild_name: {guild_name} - guild owner: {guild_ownerid}")

        # - permissions
        roles = guild.roles

        members_count = guild.member_count

        text_channels = guild.text_channels

        voice = get(client.voice_clients, guild=guild)

        # test request
        url = "https://discord.com/api/guilds/504433781927575583/channels"
        headers = {
            "Authorization": "Bot " + TOKEN
        }
        request = requests.get(url=url, headers=headers)
        channels = request.content.decode('utf-8')
        channels_dict = json.loads(channels)

        with open("./channels.json", "w") as outfile:
            json.dump(channels_dict, outfile, indent=3)

        text_channels, voice_channels = [], []
        for channel in channels_dict:
            if channel['type'] != 4:
                if "bitrate" not in channel.keys():
                    text_channels.append(channel)
                else:
                    voice_channels.append(channel)

        members_in_voice_channel = 0
        for voice in voice_channels:
            vcnl = client.get_channel(int(voice['id']))
            for member in vcnl.members:
                members_in_voice_channel += 1

        total_count = 0
        for txt in text_channels:
            cnl = client.get_channel(int(txt['id']))
            async for _ in cnl.history(limit=None):
                total_count += 1


client.run(TOKEN)
