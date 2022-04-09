import discord
import json
import os

from Models.Role import Role
from Models.TextChannel import TextChannel
from Models.VoiceChannel import VoiceChannel
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
        print("[debug] - Update Triggered")

        rst = {}

        guild = ctx.message.guild

        # GET DATA

        # - general info about the guild and the owner
        print("[debug] - Fetch general data (guild and owner)")

        rst['guild_id'] = guild.id
        rst['guild_name'] = guild.name
        rst['guild_owner'] = str(guild.owner)

        # - roles
        print("[debug] - Fetch roles data")

        roles = guild.roles
        roles_list = []
        for role in roles:
            roles_list.append(Role(role.id, role.name).__dict__)

        rst['roles'] = roles_list

        # - members count
        print("[debug] - Fetch members count")

        rst['members_count'] = guild.member_count

        # - text and voice channels
        print("[debug] - Fetch Text and Voice Channels")

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

        # - members in voice channels
        print("[debug] - Fetch Members in Voice Channels")

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
                await ctx.send(f"There are {len(voice_buffer.members)} members in {voice_buffer.name} channel: {members}")

        rst['in_voice'] = in_voice

        # - count messages
        print("[debug] - Fetch counted messages")

        count_messages = {
            "count": 0,
            "details": []
        }
        for txt in rst['text_channels']:
            count = 0
            async for _ in client.get_channel(int(txt['id'])).history(limit=None):
                count += 1
            count_messages['details'].append({
                "channel_name": txt['name'],
                "channel_id": txt['id'],
                "total": count
            })
            count_messages['count'] += count

        rst['count_messages'] = count_messages

        # write into json file
        print("[debug] - Write into json file")

        with open("./result.json", "w") as outfile:
            json.dump(rst, outfile, indent=3)

        print("> [debug] - All the data are successfully stored into json file!")
        await ctx.send("All the data are successfully stored into json file!")

client.run(TOKEN)
