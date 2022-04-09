import discord
import json
import os
import time

from Models.Role import Role
from Models.TextChannel import TextChannel
from Models.VoiceChannel import VoiceChannel
from discord.ext import commands
from dotenv import load_dotenv
from datetime import datetime

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
    global_time = time.time()
    if str(ctx.message.author) in AUTHORIZED:
        print("[debug] - Update Triggered")

        rst = {}

        guild = ctx.message.guild

        # GET DATA

        # - general info about the guild and the owner
        buffer_time = time.time()

        rst['guild_id'] = guild.id
        rst['guild_name'] = guild.name
        rst['guild_owner'] = str(guild.owner)

        print(f"[debug] - Fetched general data (guild and owner) in {round(time.time() - buffer_time, 2)}s !")

        # - roles
        buffer_time = time.time()

        roles = guild.roles
        roles_list = []
        for role in roles:
            roles_list.append(Role(role.id, role.name).__dict__)

        rst['roles'] = roles_list

        print(f"[debug] - Fetched roles data in {round(time.time() - buffer_time, 2)}s !")

        # - members count
        buffer_time = time.time()

        rst['members_count'] = guild.member_count

        print(f"[debug] - Fetched members count in {round(time.time() - buffer_time, 2)}s !")

        # - text and voice channels
        buffer_time = time.time()

        text_channels = guild.text_channels
        text_channels_list = []
        for txt in text_channels:
            text_channels_list.append(TextChannel(
                txt.id,
                txt.name,
                txt.position,
                txt.nsfw
            ).__dict__)

        rst['text_channels'] = text_channels_list

        voice_channels = guild.voice_channels
        voice_channels_list = []
        for voice in voice_channels:
            voice_channels_list.append(VoiceChannel(
                voice.id,
                voice.name,
                voice.position,
                voice.bitrate,
                voice.user_limit,
                voice.category_id
            ).__dict__)

        rst['voice_channels'] = voice_channels_list

        print(f"[debug] - Fetched Text and Voice Channels in {round(time.time() - buffer_time, 2)}s !")

        # - members in voice channels
        buffer_time = time.time()

        in_voice = {
            "total_count": 0,
            "details": []
        }

        for voice in rst['voice_channels']:
            voice_buffer = client.get_channel(int(voice['id']))
            len_buffer = len(voice_buffer.members)
            if len_buffer > 0:
                in_voice['total_count'] += len(voice_buffer.members)
                members = [member.name for member in voice_buffer.members]
                in_voice['details'].append({
                    "channel_name": str(voice_buffer.name),
                    "channel_id": voice_buffer.id,
                    'members': members
                })
                await ctx.send(f"There are {len(voice_buffer.members)} members in {voice_buffer.name} "
                               f"channel: {members}")

        rst['in_voice'] = in_voice

        print(f"[debug] - Fetched Members in Voice Channels in {round(time.time() - buffer_time, 2)}s !")

        # - count messages
        buffer_time = time.time()

        count_messages = {
            "count": 0,
            "details": []
        }
        # for txt in rst['text_channels']:
        #     count = 0
        #     async for _ in client.get_channel(int(txt['id'])).history(limit=None):
        #         count += 1
        #     count_messages['details'].append({
        #         "channel_name": txt['name'],
        #         "channel_id": txt['id'],
        #         "total": count
        #     })
        #     count_messages['count'] += count

        rst['count_messages'] = count_messages

        print(f"[debug] - Fetched counted messages in {round(time.time() - buffer_time, 2)}s !")

        # write into json file
        buffer_time = time.time()

        timestamp_filename = "extraction-"+str(datetime.timestamp(datetime.now()))+".json"
        timestamp_path = "./"+timestamp_filename

        with open(timestamp_path, "w") as outfile:
            json.dump(rst, outfile, indent=3)

        print(f"[debug] - Wrote into json file in {round(time.time() - buffer_time, 2)}s !")

        global_end_time = round(time.time()-global_time, 2)
        print(f"> [debug] - All the data are successfully stored into json file in {global_end_time}s !")
        await ctx.send(f"All the data are successfully stored into json file in {global_end_time}s ! "
                       f"I just have sent you your json file. ")
        await ctx.message.author.send(file=discord.File(timestamp_path))

        # delete timestamp file
        if os.path.exists(timestamp_path):
            os.remove(timestamp_path)
        else:
            print(f"[error] - The {timestamp_path} does not exist...")


client.run(TOKEN)
