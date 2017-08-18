from asyncio import sleep
from random import randint
from requests import get
from discord.ext import commands
from config import *
import discord

bot = commands.Bot(command_prefix=PREFIX, description='catchphrase bot')
players = []
game_word = ""
game_category = ""
game_active = False
voting = False

async def pick_word():
    global game_word
    wordlist = get('https://api.datamuse.com/words', {'topics': game_category}).json()
    game_word = (wordlist[randint(0, 99)]['word'])
    await message_user(players[0])


async def end_game():
    global game_word, game_category, game_active, voting
    players.clear()
    game_word = ""
    game_category = ""
    game_active = ""
    voting = False

    await bot.change_presence(game=discord.Game(name='{}newgame "category" to start a new game!'.format(PREFIX)))


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('https://discordapp.com/oauth2/authorize?client_id={}&scope=bot'.format(CLIENT_ID))
    print('---------')

    await bot.change_presence(game=discord.Game(name='{}newgame "category" to start a new game!'.format(PREFIX)))


@bot.command(pass_context=True)
async def newgame(ctx, category):
    global voting, game_active, game_category, game_word
    if not game_active:
        game_active = True
        players.append(ctx.message.author)
        await bot.say('{0} wants to start a game of ChatPhrase with category {1}! If you want to play, please {2}vote'.format(players[0].mention, category, PREFIX))
        await bot.say('Waiting 15 seconds to start game, must get three more vote to start game.')

        voting = True
        await sleep(15)
        voting = False

        if len(players) < MIN_PLAYERS:
            await bot.say('Not enough players, sorry.')
            players.clear()

            await end_game()
        else:
            await bot.change_status(game=discord.Game(name='Currently in game with category {}'.format(game_category)))
            game_category = category
            await bot.say('Starting game!')
            await bot.say('Starting game! {0} minutes on the clock!'.format(TIMER_LEN))
            await pick_word()
            await sleep(TIMER_LEN * 60 - WARNING_TIME)
            await bot.say('WARNING! {} seconds left!'.format(WARNING_TIME))
            await sleep(WARNING_TIME)
            await bot.say('Game over! {} loses!'.format(players[0].mention))

            await end_game()
    else:
        await bot.say('Wait for the current game to end.')


@bot.command(pass_context=True)
async def vote(ctx):
    if voting:
        member = ctx.message.author
        if member in players:
            await bot.say('{}, you only get one vote!'.format(member.mention))
        else:
            players.append(ctx.message.author)
            await bot.say('{} has voted to start a game of ChatPhrase.'.format(players[len(players) - 1]))
    else:
        await bot.say('There\'s nothing to vote on!')


async def message_user(user):
    message = 'Your word is: ' + game_word
    bot.send_message(destination=user, content=message, tts=True)


@bot.command(pass_context=True)
async def newword(ctx):
    if game_active:
        if ctx.message.author is not players[0]:
            await bot.say('It\'s not your turn, {}.'.format(ctx.message.author.mention))
            return
        else:
            print('current category: ' + game_category)
            await pick_word()
    else:
        await bot.say('Start a game, first!')


@bot.command(pass_context=True)
async def correct(ctx):
    if game_active:
        if ctx.message.author is not players[0]:
            await bot.say('It\'s not your turn, {}.'.format(ctx.message.author.mention))
            return
        else:
            players.append(players.pop(0))
            await bot.say('It\'s {}\'s turn!'.format(players[0].mention))
            await pick_word()
    else:
        await bot.say('Start a game, first!')


@bot.command()
async def namecategory():
    if game_active:
        await bot.say('The current category is: ' + game_category)
    else:
        await bot.say('Start a game, first!')


@bot.command(pass_context=True)
async def fstop(ctx):
    if ctx.message.author.server_permissions.administrator:
        end_game()
    else:
        await bot.say('You must be an administrator to force stop the game.')


bot.run(BOT_TOKEN)
