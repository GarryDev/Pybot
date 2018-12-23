# Work with Python 3.6
import traceback
import logging
import aiohttp
import asyncio
import random
import json
import re
import os
import math
from sys import exit
from random import randint
from discord.ext import commands
from discord.ext.commands import Bot
import discord.utils

logging.basicConfig(level=logging.INFO)

BOT_PREFIX = ("?", ">")
SETTINGS = []
ADMIN_LIST = []
SUPER_ADMIN_LIST = []
HOME_DIR = os.getenv("LOCALAPPDATA") + "\\PyBot\\"
CONFIG_PATH = HOME_DIR + "config.json"


class NeedAdminPriv(Exception):
    pass


# region    - Misc Functions -

# Retrieves a copy of the voice members in the same channel as the author
def copy_local_vms(ctx):
    return ctx.message.author.voice.voice_channel.voice_members.copy()


# endregion  Misc Functions

# region     -Discord Id Manipulation-


def to_dcid(id):
    return "<@!" + id + ">"


def strp_dcid(id):
    return id[3:-1]


def is_valid_format(str):
    return str[:3] == "<@!" and str[-1:] == ">"


# endregion  -Discord Id Manipulation-


def save_settings():
    global SETTINGS

    with open(CONFIG_PATH, "w") as fp:
        json.dump(SETTINGS, fp)


def main():

    global SETTINGS, ADMIN_LIST, SUPER_ADMIN_LIST

    if not os.path.exists(HOME_DIR):
        os.mkdir(HOME_DIR)

    if not os.path.exists(CONFIG_PATH):
        SETTINGS = {
            "token": "###",
            "admin_list": [],
            "super_admin_list": [],
            "bound_t_channels": [],
        }

        with open(CONFIG_PATH, "w+") as fp:
            json.dump(SETTINGS, fp)

    with open(CONFIG_PATH) as f:
        SETTINGS = json.load(f)

    if "token" in SETTINGS:
        if SETTINGS["token"] != "###":
            token = SETTINGS["token"]
        else:
            token = input("Please enter your bot token: ")
            SETTINGS["token"] = token
            save_settings()
    else:
        exit("'token' not found in json.")

    if "admin_list" not in SETTINGS:
        SETTINGS["admin_list"] = []
        ADMIN_LIST = []
        save_settings()
    else:
        ADMIN_LIST = SETTINGS["admin_list"]

    if "super_admin_list" not in SETTINGS:
        SETTINGS["super_admin_list"] = []
        SUPER_ADMIN_LIST = ["155863164544614402", "175030721876852736"]
        save_settings()
        print("superadmin list not found")
    else:
        SUPER_ADMIN_LIST = SETTINGS["super_admin_list"]
        print("set super admin list")

    if "bound_t_channels" not in SETTINGS:
        SETTINGS["bound_t_channels"] = []
        bound_t_channels = ["403643650522873857"]
        save_settings()
    else:
        bound_t_channels = SETTINGS["bound_t_channels"]

    print("Currently bound to text channels:-")
    print(bound_t_channels)

    # def in_channel(channel_id):
    #    def predicate(ctx):
    #        return ctx.message.channel.id == channel_id

    # return commands.check(predicate)

    bot = Bot(command_prefix=BOT_PREFIX)

    @bot.event
    async def on_command_error(error, ctx):
        """The event triggered when an error is raised while invoking a command.
        ctx   : Context
        error : Exception"""

        # This prevents any commands with local handlers being handled here in on_command_error.
        if hasattr(ctx.command, "on_error"):
            return

        if isinstance(error, commands.MissingRequiredArgument):
            await bot.send_message(
                ctx.message.channel,
                'error: Command "{0.clean_content}" requires addtional an argument.'.format(
                    ctx.message
                ),
            )
        elif isinstance(error, commands.CommandNotFound):
            await bot.send_message(
                ctx.message.channel,
                "What the fuck are you on about, you absolute unit???",
            )
        elif isinstance(error, NeedAdminPriv):
            await bot.send_message(
                ctx.message.channel,
                "You must be an admin to use admin commands, loser.",
            )
        else:
            await bot.send_message(
                ctx.message.channel, "Error caught. Type: {}".format(str(error))
            )

    @bot.event
    async def on_ready():
        await bot.change_presence(
            game=discord.Game(name="Can spell better than Kieran.")
        )
        print("Logged in as " + bot.user.name)

    # {0.author.mention}'.format(ctx.message)

    @bot.group(pass_context=True)
    async def admin(ctx):

        print("admin(ctx)")

        if ctx.message.author.id not in ADMIN_LIST:
            raise NeedAdminPriv("You're not an admin you fuck.")

        if ctx.invoked_subcommand is None:
            await bot.say("Invalid usage, use >admin <add/remove> <@user>")

    @admin.command(pass_context=True)
    async def add(ctx, arg):
        print("add(ctx, arg)")

        if arg is None:
            await bot.say("Invalid usage, use >admin <add/remove> <@user>")
        elif is_valid_format(arg):
            id = strp_dcid(arg)

            if id in ADMIN_LIST:
                await bot.say("Already admin.")
            else:
                ADMIN_LIST.append(id)
                save_settings()
                await bot.say("{} was added to admin list.".format(arg))
        else:
            await bot.say("Invalid usage, use >admin add <@user>")

    @admin.command(pass_context=True)
    async def remove(ctx, arg):
        print("remove(ctx, arg)")
        if arg is None:
            await bot.say("Missing argument use 'admin remove {@user}'")
        elif is_valid_format(arg):
            id = strp_dcid(arg)

            if id not in ADMIN_LIST:
                await bot.say("Admin not found.")
            else:
                ADMIN_LIST.remove(id)
                save_settings()
                await bot.say("{} was removed from admin list.".format(arg))
        else:
            await bot.say("Invalid usage, use >admin remove <@user>")

    @bot.group(pass_context=True)
    async def superadmin(ctx):

        print("superadmin(ctx)")

        if ctx.message.author.id not in SUPER_ADMIN_LIST:
            raise NeedAdminPriv("not superadmin")

        if ctx.invoked_subcommand is None:
            await bot.say("Invalid usage, use >superadmin <add/remove> <@user>")

    @superadmin.command(pass_context=True)
    async def add(ctx, arg):
        print("add(ctx, arg)")

        if arg is None:
            await bot.say("Invalid usage, use >superadmin <add/remove> <@user>")
        elif is_valid_format(arg):
            id = strp_dcid(arg)

            if id in SUPER_ADMIN_LIST:
                await bot.say("Already superadmin.")
            else:
                SUPER_ADMIN_LIST.append(id)
                save_settings()
                await bot.say("{} was added to superadmin list.".format(arg))
        else:
            await bot.say("Invalid usage, use >superadmin add <@user>")

    @superadmin.command(pass_context=True)
    async def remove(ctx, arg):
        print("remove(ctx, arg)")
        if arg is None:
            await bot.say("Missing argument use 'superadmin remove {@user}'")
        elif is_valid_format(arg):
            id = strp_dcid(arg)

            if id not in SUPER_ADMIN_LIST:
                await bot.say("superadmin not found.")
            else:
                SUPER_ADMIN_LIST.remove(id)
                save_settings()
                await bot.say("{} was removed from superadmin list.".format(arg))
        else:
            await bot.say("Invalid usage, use >superadmin remove <@user>")

    @admin.command(pass_context=True)
    async def list(ctx):
        for admin in ADMIN_LIST:
            await bot.say(to_dcid(admin))

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
            static_member_list = copy_local_vms(ctx)

            for member in static_member_list:
                await bot.say("BEGONE THOT! {}".format(to_dcid(member.id)))
                await bot.move_member(member, random.choice(voice_channels))

    @superadmin.command(pass_context=True)
    async def kickthecunt(ctx):
        await bot.say(
            "GET FUKT! {}".format(to_dcid(random.choice(copy_local_vms(ctx)).id))
        )
        await bot.kick(chosen_one)

    @superadmin.command(pass_context=True)
    async def SNAP(ctx):
        current_voice_list = copy_local_vms(ctx)
        half_of_current_voice_list = math.ceil(len(current_voice_list) / 2)
        snapped_users = random.sample(current_voice_list, half_of_current_voice_list)
        snapped_channel = discord.utils.get(
            ctx.message.server.channels, name="The Soul Stone"
        )

        await bot.say("You should have gone for the head.")
        await bot.say("**SNAP!**")
        for member in snapped_users:
            await bot.move_member(member, snapped_channel)

    @bot.command(pass_context=True)
    async def ridethebus(ctx, arg):

        print(
            "member no: {}".format(
                len(ctx.message.author.voice.voice_channel.voice_members)
            )
        )

        for x in range(0, 20):
            for member in ctx.message.author.voice.voice_channel.voice_members:

                old_name = "".join(str(member.display_name))

                if old_name == arg or old_name == "Loki":
                    pass
                else:
                    await bot.change_nickname(member, arg)
                    await asyncio.sleep(0.5)
                    await bot.change_nickname(member, old_name)

    @admin.command(pass_context=True)
    async def icantspell(ctx):

        vowels = "aeiouaeiou"

        for member in ctx.message.server.members:

            correct_spelling = member.display_name

            if correct_spelling != "Loki" or "PyBot":

                print("jumbling -> {}".format(correct_spelling))
                await bot.say("jumbling -> {}".format(correct_spelling))

                new_spelling = ""

                for char in correct_spelling:

                    rnd = randint(0, 4)

                    if char in vowels:
                        if char is "a":
                            new_spelling += vowels[rnd + 1]
                        elif char is "e":
                            new_spelling += vowels[rnd + 2]
                        elif char is "i":
                            new_spelling += vowels[rnd + 3]
                        elif char is "o":
                            new_spelling += vowels[rnd + 4]
                        elif char is "u":
                            new_spelling += vowels[rnd + 5]
                    else:
                        new_spelling += char

                await bot.change_nickname(member, new_spelling)
                print("result = {}".format(new_spelling))
                await bot.say("result = {}".format(new_spelling))

    @bot.command(pass_context=True)
    async def format_nic(ctx, arg):

        formats = {
            "neg_squared": (127344, False),
            "circled_latin": (9398, False),
            "negative_circled_latin": (127323, False),
            "mathematical_bold_fraktur": (120172, False),
        }

        if arg in formats:
            format = formats[arg]
        else:
            await bot.say(
                "Requested format not supported. Run '>format help' for more options."
            )

        new_name = ""

        name = ctx.message.author.display_name

        if format[1] is False:
            name.lower()

        for char in name:
            new_name += chr(ord(char) - 97 + format[0])

        await bot.change_nickname(ctx.message.author, new_name)

    async def list_servers():
        await bot.wait_until_ready()
        while not bot.is_closed:
            print("Current servers:")
            for server in bot.servers:
                print(server.name)
            await asyncio.sleep(200)

    bot.loop.create_task(list_servers())
    bot.run(token)


if __name__ == "__main__":
    main()
