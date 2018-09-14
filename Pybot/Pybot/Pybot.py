# Work with Python 3.6
import discord
import random
import json
import re
from os import listdir, path
from sys import exit

settings = None
admin_list = None
home_dir = 'C:\\pybot\\'
config_file = home_dir + 'config.json'

def main():

    def init_config():

        settings =	{
        "token": '###',
        "client_id": '###',
        "admin_list": '###'
        }

        with open(config_file, 'w+') as fp:
            json.dump(settings, fp)

        exit('Please fill in blank values in ' + config_file + '.')

    if(path.exists(home_dir)):
        if(path.exists(config_file)):

            with open(config_file) as f:
                settings = json.load(f)

            error_str = 'Please give a valid value for \'{}\' in your ' + config_file + '.'

            if 'token' in settings:
                if settings['token'] != '###':
                    TOKEN = settings['token']
                else: exit(error_str.format('token'))
            else: exit('\'token\' not found in json.')

            if 'client_id' in settings:
                if settings['client_id'] != '###':
                    CLIENT_ID = settings['client_id']
                else: exit(error_str.format('client_id'))
            else: exit('\'client_id\' not found in json.')

            if 'admin_list' in settings:
                if settings['admin_list'] != '###':
                    admin_list = settings['admin_list']
                else: exit(error_str.format('admin_list'))
            else: exit('\'admin_list\' not found in json.')

            client = discord.Client()

        else: init_config()
    else: init_config()

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
                                    with open(config_file, 'w') as fp:
                                        json.dump(settings, fp)
                                    await reply('Added successfully')
                            else: await reply('wrong for format for id arg !admin add [id]')
                        else: await reply('unkown command !admin add ???')

                    elif args[0] == 'remove':
                        if len(args) == 2:
                            if args[1][:2] == '<@' and args[1][-1:] == '>':
                                id = args[1][2:-1]
                                if id not in admin_list:
                                    await reply('Admin not found.')
                                else:
                                    admin_list.remove(id)
                                    settings['admin_list'].remove(id)
                                    with open(config_file, 'w') as fp:
                                        json.dump(settings, fp)
                                    await reply('Removed successfully')
                            else: await reply('wrong for format for id arg !admin add [id]')
                        else: await reply('unkown command !admin add ???')

                    elif args[0] == 'list':
                        await reply(settings['admin_list'])

                    else: await reply('unkown command !admin ???')

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
                    await client.send_file(message.channel, 'C:\\pybot\\anne_robinson.jpg')
                except ValueError:
                    print('Could not open C:\\pybot\\anne_robinson.jpg')
            elif "hi" in msg:
                for file in listdir('C:\\pybot\\hi'):
                    await client.send_file(message.channel, 'C:\\pybot\\hi\\' + file)
            else:
                await reply('What the fuck are you on about you absolute unit???')
                print('Could not match responce to:\n' + msg + '\n')

        if '!howdy' in msg:
            None


    @client.event
    async def on_ready():
        print('Logged in as')
        print(client.user.name)
        print(client.user.id)
        print('------')

    client.run(TOKEN)

if __name__== "__main__":
   main()