import os, discord, requests, json
from dotenv import load_dotenv
from discord.ext import commands

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
        rst['guild_owner'] = guild.owner

        # - permissions
        rst['roles'] = guild.roles

        rst['members_count'] = guild.member_count

        rst['text_channels'] = guild.text_channels

        # test request
        url = "https://discord.com/api/guilds/504433781927575583/channels"
        headers = {
            "Authorization": "Bot " + TOKEN
        }
        request = requests.get(url=url, headers=headers)
        channels = request.content.decode('utf-8')
        channels_dict = json.loads(channels)

        # text_channels, voice_channels = [], []
        voice_channels = []
        for channel in channels_dict:
            if channel['type'] != 4:
                if "bitrate" not in channel.keys():
                    # text_channels.append(channel)
                    pass
                else:
                    voice_channels.append(channel)

        rst['voice_channels'] = voice_channels

        members_in_voice_channel = 0
        for voice in voice_channels:
            for member in client.get_channel(int(voice['id'])).members:
                members_in_voice_channel += 1

        rst['members_in_voice_channel'] = members_in_voice_channel

        total_count = 0
        for txt in rst['text_channels']:
            async for _ in client.get_channel(int(txt['id'])).history(limit=None):
                total_count += 1

        print(rst)
        with open("./result.json", "w") as outfile:
            json.dump(rst, outfile, indent=3)

        print("> [debug] - result obj successfully stored")
        await ctx.send("All data are successfully updated !")

client.run(TOKEN)
