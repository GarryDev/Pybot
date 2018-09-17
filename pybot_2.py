# Work with Python 3.6
import traceback
import logging
import aiohttp
import asyncio
import random
import json
import re
import os
from sys import exit
from discord import Game
from discord.ext import commands
from discord.ext.commands import Bot

logging.basicConfig(level=logging.INFO)

BOT_PREFIX = ('?','>')
settings = []
admin_list = []
home_dir = os.getenv('LOCALAPPDATA') + "\\pybot\\"
config_path = home_dir + 'config.json'

class NeedAdminPriv(Exception):
    pass

def to_dcid(id):
    return '<@!' + id + '>'

def strp_dcid(id):
    return id[3:-1]

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

    @bot.event
    async def on_command_error(error, ctx):
        """The event triggered when an error is raised while invoking a command.
        ctx   : Context
        error : Exception"""

        # This prevents any commands with local handlers being handled here in on_command_error.
        if hasattr(ctx.command, 'on_error'):
            return
        
        if isinstance(error, commands.MissingRequiredArgument):
            await bot.send_message(ctx.message.channel, 'error: Command "{0.clean_content}" requires addtional an argument.'.format(ctx.message))
        elif isinstance(error, commands.CommandNotFound):
            await bot.send_message(ctx.message.channel, 'What the fuck are you on about you absolute unit???')
        elif isinstance(error, NeedAdminPriv):
            await bot.send_message(ctx.message.channel, 'You must be an admin to use admin commands, loser.')
        else:
            await bot.send_message(ctx.message.channel, 'command error of type: {}'.format(str(error)))

    @bot.event
    async def on_ready():
        await bot.change_presence(game=Game(name="y'all cray cray"))
        print("Logged in as " + bot.user.name)

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

        print("admin(ctx)")

        if ctx.message.author.id not in admin_list:
            raise NeedAdminPriv('not admin')

        if ctx.invoked_subcommand is None:
            await bot.say('Invald usage, use !admin <add/remove> <@user>')

    def is_valid_format(str):
        return str[:3] == '<@!' and str[-1:] == '>'

    @admin.command(pass_context=True)
    async def add(ctx, arg):
        print('add(ctx, arg)')

        if(arg is None):
            await bot.say('Invald usage, use !admin <add/remove> <@user>')
        elif is_valid_format(arg):
            id = strp_dcid(arg)

            if id in admin_list:
                await bot.say('Already admin.')
            else:
                admin_list.append(id)
                save_settings()
                await bot.say('{} was added to admin list.'.format(arg))
        else:
            await bot.say('Invald usage, use !admin add <@user>')

    @admin.command(pass_context=True)
    async def remove(ctx, arg):
        print('remove(ctx, arg)')
        if(arg is None):
            await bot.say('Missing argument use \'admin remove {@user}\'')
        elif is_valid_format(arg):
            id = strp_dcid(arg)

            if id not in admin_list:
                await bot.say('Admin not found.')
            else:
                admin_list.remove(id)
                save_settings()
                await bot.say('{} was removed from admin list.'.format(arg))
        else:
            await bot.say('Invald usage, use !admin remove <@user>')

    @admin.command(pass_context=True)
    async def hello(ctx):
        await bot.say('hello admin!')

    @admin.command(pass_context=True)
    async def list(ctx):
        for admin in admin_list:
            await bot.say('hello admin!')
    
    @admin.command(pass_context=True)
    async def scattertheweak(ctx):
        voice_channels = []
        for server in bot.servers:
            for channel in server.channels:
                # categorys have channel type as a int where as text and voice are an set of string and int [name, value]
                if not isinstance(channel.type, int):
                    if channel.type.value == 2:
                        voice_channels.append(channel)

            # copy list so it will not be updated when a user is removed from the voice channel
            static_member_list = ctx.message.author.voice.voice_channel.voice_members.copy()

            for member in static_member_list:
                await bot.say('BEGONE THOT! <@' + member.id + '>')
                await bot.move_member(member, random.choice(voice_channels))

    # catch error locally
    # @add.error
    # async def test_on_error(ctx, error):
    #   await bot.send_message(error.message.channel, '!admin <add/remove> <@user>')

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