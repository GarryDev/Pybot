# Work with Python 3.6
import asyncio
import traceback
import aiohttp
import random
import json
import re
import os
from sys import exit
from discord import Game
from discord.ext.commands import Bot

BOT_PREFIX = ("?", "!")
settings = []
admin_list = []
home_dir = os.getenv('LOCALAPPDATA') + "\\pybot\\"
config_path = home_dir + 'config.json'

def save_settings():
    global settings

    with open(config_path, 'w') as fp:
        json.dump(settings, fp)

def main():

    global settings

    if not os.path.exists(home_dir): 
        os.mkdir(home_dir)

    if not os.path.exists(config_path):
        settings =	{
        "token": '###',
        "admin_list": []
        }

        with open(config_path, 'w+') as fp:
            json.dump(settings, fp)

    with open(config_path) as f:
        settings = json.load(f)

    # error_str = 'Please give a valid value for \'{}\' in your ' + config_file + '.'

    if 'token' in settings:
        if settings['token'] != '###':
            token = settings['token']
        else:
            token = input('Please enter your bot token: ')
            settings['token'] = token
            save_settings()
    else:
        exit('\'token\' not found in json.')

    if 'admin_list' not in settings:
        settings['admin_list'] = []
        admin_list = []
        save_settings()
    else: 
        admin_list = settings['admin_list']

    bot = Bot(command_prefix=BOT_PREFIX)

    @bot.command(name='8ball',
                    description="Answers a yes/no question.",
                    brief="Answers from the beyond.",
                    aliases=['eight_ball', 'eightball', '8-ball'],
                    pass_context=True)
    async def eight_ball(context):
        possible_responses = [
            'That is a resounding no',
            'It is not looking likely',
            'Too hard to tell',
            'It is quite possible',
            'Definitely',
        ]
        await bot.say(random.choice(possible_responses) + ", " + context.message.author.mention)


    @bot.command()
    async def square(number):
        squared_value = int(number) * int(number)
        await bot.say(str(number) + " squared is " + str(squared_value))


    @bot.event
    async def on_ready():
        await bot.change_presence(game=Game(name="with humans"))
        print("Logged in as " + bot.user.name)

    @bot.event
    async def on_error(event, *args, **kwargs):
        await bot.send_message(args[0].channel, traceback.format_exc())
        print("fuck")

    @bot.command()
    async def bitcoin():
        url = 'https://api.coindesk.com/v1/bpi/currentprice/BTC.json'
        async with aiohttp.ClientSession() as session:  # Async HTTP request
            raw_response = await session.get(url)
            response = await raw_response.text()
            response = json.loads(response)
            await bot.say("Bitcoin price is: $" + response['bpi']['USD']['rate'])

    #{0.author.mention}'.format(ctx.message)

    @bot.group(pass_context=True)
    async def admin(ctx):
        print('admin(ctx)')
        if ctx.invoked_subcommand is None:
            await bot.say('Invald usage, use !admin <add/remove> <@user>')

    @admin.command(pass_context=True)
    async def add(ctx, arg):
        print('add(ctx, arg)')
        if(arg is None):
            await bot.say('Invald usage, use !admin <add/remove> <@user>')
        else:
            await bot.say('{} was added to admin list.'.format(arg))

    @add.error
    async def test_on_error(ctx, error):
        await bot.send_message(error.message.channel, '!admin <add/remove> <@user>')

    @admin.command(pass_context=True)
    async def remove(ctx, arg):
        print('remove(ctx, arg)')
        if(arg is None):
            await bot.say('Missing argument use \'admin remove {@user}\'')
        else:
            await bot.say('{} was removed from admin list.'.format(arg))

    async def list_servers():
        await bot.wait_until_ready()
        while not bot.is_closed:
            print("Current servers:")
            for server in bot.servers:
                print(server.name)
            await asyncio.sleep(600)

    bot.loop.create_task(list_servers())
    bot.run(token)

if __name__== "__main__":
    main()