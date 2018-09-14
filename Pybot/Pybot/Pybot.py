# Work with Python 3.6
import discord
import random
import re
from os import listdir

TOKEN = 'NDg5ODM3NzExNzUwOTg3Nzg3.DnwkmA.uPRENdAZeB3eHUwCsw_rw4SyXKk'
CLIENT_ID = '489837711750987787'

client = discord.Client()

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    msg = message.content

    my_name = ['pybot', 'Pybot', '<@' + client.user.id + '>']

    if any(x in msg for x in my_name):
        # switch statements are saved
        if "who is our lord" in msg:
            await client.send_message(message.channel, '{0.author.mention} OUR LORD AND SAVIOR IS CHIN-CHIN REEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE!!!!!!!!!!!!!'.format(message))
        elif "thoughts on" in msg:
            result = re.search('thoughts on <@(.*)>', msg)
            await client.send_message(message.channel, "<@"  + result.group(1) + ">" + " is a cuck")
        elif "anne" in msg:
            try:
                await client.send_file(message.channel, 'C:\\pybot\\anne_robinson.jpg')
            except ValueError:
                print('Could not open C:\\pybot\\anne_robinson.jpg')
        elif "hi" in msg:
            for file in listdir('C:\\pybot\\hi'):
                await client.send_file(message.channel, 'C:\\pybot\\hi\\' + file)
        else:
            await client.send_message(message.channel, 'What the fuck are you on about you absolute unit???')
            print('Could not match responce to:\n' + msg + '\n')

    immune = "155863164544614402", "175030721876852736"

    if message.author.id in immune and "!scattertheweak" in msg:

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
            await client.send_message(message.channel, 'BEGONE THOT! <@' + member.id + '>')
            await client.move_member(member, random.choice(voice_channels))
    if '!howdy' in msg:


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)