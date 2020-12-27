import asyncio
import os
from typing import cast

import discord
from discord import FFmpegPCMAudio, VoiceChannel, VoiceClient
from discord.ext import commands
from discord.ext.commands import Context

from game import Game

DISCORD_TOKEN = open("token.txt", "r").read()

# guilds - required for bot to function
# voice_states - list members in voice channel
# messages - see text command
intents = discord.Intents(guilds=True, voice_states=True, messages=True)
bot = commands.Bot(command_prefix="~", intents=intents)

# Stores currently active game instances.  Key = channel_id, value = Game
active_games = {}
lock = asyncio.Lock()


@bot.command()
async def creategame(ctx):
    async with lock:
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
    async with lock:
        channel_id = ctx.message.channel.id

        # Check that there is actually a game created in the channel
        if channel_id not in active_games:
            await ctx.message.channel.send("There is no game in this channel.  Create a game with the creategame command!")
            return

        game = active_games[channel_id]

        if game.started:
            await ctx.message.channel.send("There is already a game running in this channel.  Please wait for it to end, or create a game in a different text channel.")
            return


        # Loop through reactions to signup message and extract players
        signup_message = await ctx.fetch_message(game.signup_message_id)
        for reaction in signup_message.reactions:
            async for user in reaction.users():
                if user.id != bot.user.id:
                    game.enrollPlayer(user)
        
        # Make sure the game has enough players
        if len(game.players) < 2:
            await ctx.message.channel.send("Not enough players to start the game.  At least two players must react to the signup message to start the game.")
            return

        await game.startGame()
        await ctx.message.channel.send("The game has started!  Please check your DMs to see which cards you got.  When you are ready to submit a guess, use the command `~accuse <suspect> <weapon> <location>`")


@bot.command()
async def accuse(ctx, person, weapon, location):
    async with lock:

        channel_id = ctx.message.channel.id

        if channel_id not in active_games:
            await ctx.message.channel.send("There is no game in this channel.  Create a game with the creategame command!")
            return

        game = active_games[channel_id]

        # Check that the user sending the message is an active player in the game
        if not game.isPlayerInGame(ctx.message.author):
            await ctx.message.channel.send("You are not in this game, so you cannot submit a guess.  If you would like to play, please enroll in the next game.")
            return

        isCorrect = game.makeAccusation(ctx.message.author, person, weapon, location)
        if (isCorrect):
            # A correct guess means the player won.  Congratulate them and end the game.
            del active_games[channel_id]
            await ctx.message.channel.send("Congratulations {}! You are right!  The game has ended, you win!".format(ctx.message.author.mention))
        else:
            # An incorrect guess means the player lost and can no longer make accusations.  DM them the answer and broadcast in the channel that they have lost.
            # They were already removed from the game bu the makeAccusation method.
            await ctx.message.author.send("You are wrong. The solution was: {}".format(game.getSolutionMessage()))
            await ctx.message.channel.send("You are wrong {}.  You have been eliminated from the game.".format(ctx.message.author.mention))

        # if there are no players left, end the game and display the solution.
        if len(game.players) == 0:
            del active_games[channel_id]
            await ctx.message.channel.send("The game has ended, nobody won!  The solution was: {}".format(game.getSolutionMessage()))


@bot.command()
async def endgame(ctx):
    async with lock:
        channel_id = ctx.message.channel.id

        if channel_id not in active_games:
            await ctx.message.channel.send("There is no game in this channel.  Create a game with the creategame command!")
            return

        game = active_games[channel_id]
        del active_games[channel_id]
        await ctx.message.channel.send("The game has been forcibly ended.  The solution was: " + game.getSolutionMessage())


@bot.event
async def on_ready():
    print("Ready!")


bot.run(DISCORD_TOKEN)
