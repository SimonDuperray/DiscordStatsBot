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

        text_channels = []
        for channel in channels_dict:
            if channel['type'] != 4:
                if "bitrate" not in channel.keys():
                    text_channels.append(channel)



        # count = 0
        # async for _ in ctx.channel.history(limit=None):
        #     count += 1

        # print(f"total msg in {bvn_channel} = {count}")
        # await ctx.send(f"total msg in {bvn_channel}: {count}")

client.run(TOKEN)
