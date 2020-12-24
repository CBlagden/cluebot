import asyncio
import os
from typing import cast

import discord
from discord import FFmpegPCMAudio, VoiceChannel, VoiceClient
from discord.ext import commands
from discord.ext.commands import Context

from game import Game

# Channel id to listen for commands from
CMD_CHANNEL_ID = 790772134016188476
# Voice channel id to E X I S T in
AUDIO_CHANNEL_ID = 790829385606234112
# Voice channel id to move members to after playing
TARGET_CHANNEL_ID = 790829461816999946

# Only the president can use the mugs
PRESIDENT_ROLE = "Admin"

DISCORD_TOKEN = "fill me in"

# guilds - required for bot to function
# voice_states - list members in voice channel
# messages - see text command
intents = discord.Intents(guilds=True, voice_states=True, messages=True)
bot = commands.Bot(command_prefix="~", intents=intents)

# Stores currently active game instances.  Key = channel_id, value = Game
active_games = {}


@bot.command()
async def creategame(ctx):
    # Get channel command was sent in
    channel_id = ctx.message.channel.id

    # Enforce one game per text channel
    if channel_id in active_games:
        await ctx.message.channel.send("There is already a game running in this text channel.  Please wait for it to end, or create a game in a different text channel.")
        return

    # send message 'react to this to be added to game
    signup_message = await ctx.message.channel.send('React to be added to the game!')
    await signup_message.add_reaction('👍')
    # Create a game and add to active games list
    game = Game(channel_id, signup_message.id)
    active_games[channel_id] = game


@bot.command()
async def startgame(ctx):
    channel_id = ctx.message.channel.id

    # Check that there is actually a game created in the channel
    if channel_id not in active_games:
        await ctx.message.channel.send("There is no game in this channel.  Create a game with the creategame command!")
        return

    game = active_games[channel_id]

    # Loop through reactions to signup message and extract players
    signup_message = await ctx.fetch_message(game.signup_message_id)
    for reaction in signup_message.reactions:
        async for user in reaction.users():
            if user.id != bot.user.id:
                game.enrollPlayer(user)

    await game.startGame()
    await ctx.message.channel.send("The game has started!  Please check your DMs to see which cards you got.  When you are ready to submit a guess, use the ~makeguess command")


@bot.command()
async def makeguess(ctx, player, weapon, location):
    channel_id = ctx.message.channel.id

    if channel_id not in active_games:
        await ctx.message.channel.send("There is no game in this channel.  Create a game with the creategame command!")
        return

    game = active_games[channel_id]

    isCorrect = game.makeGuess(player, weapon, location)

    if (isCorrect):
        # Make the game end somehow
        pass
    else:
        # Mark the person who guessed wrong as no longer a player
        pass


@bot.event
async def on_ready():
    print("Ready!")


bot.run(DISCORD_TOKEN)
