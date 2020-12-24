import asyncio
import os
from typing import cast

import discord
from discord import FFmpegPCMAudio, VoiceChannel, VoiceClient
from discord.ext import commands
from discord.ext.commands import Context
from dotenv import load_dotenv

load_dotenv()

# Channel id to listen for commands from
CMD_CHANNEL_ID = 790772134016188476
# Voice channel id to E X I S T in
AUDIO_CHANNEL_ID = 790829385606234112
# Voice channel id to move members to after playing
TARGET_CHANNEL_ID = 790829461816999946

# Only the president can use the mugs
PRESIDENT_ROLE = "Admin"

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

# guilds - required for bot to function
# voice_states - list members in voice channel
# messages - see text command
intents = discord.Intents(guilds=True, voice_states=True, messages=True)
bot = commands.Bot(command_prefix="~", intents=intents)

# Stores currently active game instances.  Key = channel_id, value = Game
active_games = {}


@bot.command()
async def creategame(ctx: Context):
    # Get channel command was sent in
    channel_id = ctx.message.channel_id

    # send message 'react to this to be added to game
    signup_message = await ctx.message.channel.send('React to be added to the game!')
    await signup_message.add_reaction('👍')
    # Create a game and add to active games list
    game = Game(channel_id, signup_message.id)
    active_games[channel_id] = game
    

@bot.command()
async def startgame(ctx: Context):
    channel_id = ctx.message.channel_id

    # Check that there is actually a game created in the channel
    if channel_id not in active_games.keys():
        await ctx.message.channel.send("There is no game in this channel.  Create a game with the creategame command!")
        return
    
    game = active_games[channel_id]

    # Loop through reactions to signup message and extract players
    signup_message = ctx.fetch_message(game.signup_message_id)
    for reaction in signup_message.reactions:
        for user in reaction.users():
            if user.id != bot.user.id:
                game.enrollPlayer(user)

    game.startGame()


@bot.event
async def on_ready():
    # Join the target channel on bot start
    await bot.get_channel(AUDIO_CHANNEL_ID).connect()
    print("Ready!")


bot.run(DISCORD_TOKEN)


