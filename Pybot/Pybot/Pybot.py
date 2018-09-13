# Work with Python 3.6
import discord
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

    if message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)

    my_name = ['pybot', 'Pybot', '!489837711750987787']

    if any(x in message.content for x in my_name):
        # switch statements are saved
        if "who is our lord" in message.content:
            await client.send_message(message.channel, '{0.author.mention} OUR LORD AND SAVIOR IS CHIN-CHIN REEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE!!!!!!!!!!!!!'.format(message))
        elif "thoughts on" in message.content:
            result = re.search('thoughts on <@(.*)>', message.content)
            print(message.content)
            print(result.group(1))
            await client.send_message(message.channel, "<@"  + result.group(1) + ">" + " is a cuck")
        elif "anne" in message.content:
            try:
                await client.send_file(message.channel, 'C:\\pybot\\anne_robinson.jpg')
            except ValueError:
                print('Could not open C:\\pybot\\anne_robinson.jpg')
        elif "hi" in message.content:
            for file in listdir('C:\\pybot\\hi'):
                await client.send_file(message.channel, 'C:\\pybot\\hi\\' + file)
        else:
            client.send_message(message.channel, "What the fuck are you on about you absolute unit???")
            print('Could not match responce to:\n' + message.content + '\n')

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)