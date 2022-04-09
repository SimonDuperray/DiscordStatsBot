import discord
import json
import os
import requests

from Role import Role
from discord.ext import commands
from dotenv import load_dotenv

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

        rst = {}

        guild = ctx.message.guild

        # GET DATA

        # - general info about the guild and the owner
        rst['guild_id'] = guild.id
        rst['guild_name'] = guild.name
        rst['guild_owner'] = str(guild.owner)

        # - permissions
        roles = guild.roles
        roles_list = []
        for role in roles:
            roles_list.append(Role(role.id, role.name).__dict__)

        rst['roles'] = roles_list

        # rst['members_count'] = guild.member_count

        # rst['text_channels'] = guild.text_channels

        # test request
        # url = "https://discord.com/api/guilds/504433781927575583/channels"
        # headers = {
        #     "Authorization": "Bot " + TOKEN
        # }
        # request = requests.get(url=url, headers=headers)
        # channels = request.content.decode('utf-8')
        # channels_dict = json.loads(channels)
        #
        # text_channels, voice_channels = [], []
        # for channel in channels_dict:
        #     if channel['type'] != 4:
        #         if "bitrate" not in channel.keys():
        #             text_channels.append(dict(channel))
        #         else:
        #             voice_channels.append(dict(channel))

        # rst['voice_channels'] = voice_channels
        # rst['text_channels'] = text_channels

        # members_in_voice_channel = 0
        # for voice in voice_channels:
        #     voice_buffer = client.get_channel(int(voice['id']))
        #     members_in_voice_channel += len(voice_buffer.members)
            # members = [member.name for member in voice_buffer.members]
            # await ctx.send(f"There are {len(voice_buffer.members)} members in {voice_buffer.name} channel: {members}")

        # rst['members_in_voice_channel'] = members_in_voice_channel

        # total_count = 0
        # for txt in text_channels:
        #     count = 0
        #     async for _ in client.get_channel(int(txt['id'])).history(limit=None):
        #         count += 1
        #     print(f"{txt['id']} - {txt['name']}: {count} messages counted")
        #     total_count += count

        # rst['total_count_messages'] = total_count

        with open("./result.json", "w") as outfile:
            json.dump(rst, outfile, indent=3)

        print("> [debug] - result obj successfully stored")
        await ctx.send("All data are successfully updated !")

client.run(TOKEN)
