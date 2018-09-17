# Work with Python 3.6
import discord
import random
import json
import re
import os
from os import listdir, path
from sys import exit


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

    if not path.exists(home_dir): 
        os.mkdir(home_dir)

    if not path.exists(config_path):
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
            TOKEN = settings['token']
        else:
            TOKEN = input('Please enter your bot token: ')
            settings['token'] = TOKEN
            save_settings()
    else:
        exit('\'token\' not found in json.')

    if 'admin_list' not in settings:
        settings['admin_list'] = []
        admin_list = []
        save_settings()
    else: 
        admin_list = settings['admin_list']

    client = discord.Client()

    @client.event
    async def on_message(message):

        def reply(msg):
            return client.send_message(message.channel, msg)

        # we do not want the bot to reply to itself
        if message.author == client.user:
            return

        msg = message.content
        my_name = ['pybot', 'Pybot', '<@' + client.user.id + '>']

        if message.author.id in admin_list:
            if '!admin ' in msg:
                args = msg[7:len(msg)].split(' ')
                if len(args) >= 1:
                    if args[0] == 'add':
                        if len(args) == 2:
                            if args[1][:3] == '<@!' and args[1][-1:] == '>':
                                id = args[1][3:-1]
                                if id in admin_list:
                                    await reply('Already admin.')
                                else:
                                    admin_list.append(id)
                                    save_settings()
                                        
                                    await reply('Added successfully')
                            else:
                                await reply('wrong for format for id arg !admin add [id]')
                        else:
                            await reply('unknown command !admin add ???')

                    elif args[0] == 'remove':
                        if len(args) == 2:
                            if args[1][:2] == '<@' and args[1][-1:] == '>':
                                id = args[1][2:-1]
                                if id not in admin_list:
                                    await reply('Admin not found.')
                                else:
                                    admin_list.remove(id)
                                    settings['admin_list'].remove(id)
                                    save_settings()
                                    await reply('Removed successfully')
                            else:
                                await reply('wrong for format for id arg !admin add [id]')
                        else:
                            await reply('unknown command !admin add ???')
                    elif args[0] == 'list':
                        await reply(settings['admin_list'])
                    else:
                        await reply('unknown command !admin ???')
                else: 
                    await reply('missing arg !admin [arg]')

            if '!scattertheweak' in msg:
                voice_channels = []
                for server in client.servers:
                    for channel in server.channels:
                        # categorys have channel type as a int where as text and voice are an set of string and int [name, value]
                        if not isinstance(channel.type, int):
                            if channel.type.value == 2:
                                voice_channels.append(channel)

                # copy list so it will not be updated when a user is removed from the voice channel
                static_member_list = message.author.voice.voice_channel.voice_members.copy()

                for member in static_member_list:
                    await reply('BEGONE THOT! <@' + member.id + '>')
                    await client.move_member(member, random.choice(voice_channels))


        if any(x in msg for x in my_name):
            # switch statements are saved
            if "who is our lord" in msg:
                await reply('{0.author.mention} OUR LORD AND SAVIOR IS CHIN-CHIN REEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE!!!!!!!!!!!!!'.format(message))
            elif "thoughts on" in msg:
                result = re.search('thoughts on <@(.*)>', msg)
                await reply("<@"  + result.group(1) + ">" + " is a cuck")
            elif "anne" in msg:
                try:
                    await client.send_file(message.channel, home_dir + "\\" + 'anne.jpg')
                except ValueError:
                    print('Could not open' + home_dir + 'anne.jpg')
            elif "hi" in msg:
                for file in listdir(home_dir + '\\' + 'hi'):
                    await client.send_file(message.channel, home_dir + '\\' + 'hi' + '\\' + file)
            else:
                await reply('What the fuck are you on about you absolute unit???')
                print('Could not match response to:\n' + msg + '\n')

        if '!howdy' in msg:
            None


    @client.event
    async def on_ready():
        print('Logged in as')
        print(client.user.name)
        print(client.user.id)
        print('------')
        print('config path: ' + config_path)
        print('------')
        print("Current Admin List:-")
        print(admin_list)
        print('------')

    client.run(TOKEN)

if __name__== "__main__":
    main()