# -*- coding: utf-8 -*-
import discord
from discord.ext import commands
import asyncio
import re, random
import chatterbot
import time
# import auth.txt
from requests import get as http_get

# client = discord.Client()

description = '''The bot to talk to you.'''

bot = commands.Bot(command_prefix='!',description=description,owner_id=101388890312552448) #CrYoZ.id
# '''owner_id can be used in commands: @commands.is_owner() like is_admin(),
# but it's a predefined coroutine.
# https://discordpy.readthedocs.io/en/rewrite/ext/commands/api.html#discord.ext.commands.is_owner'''

# Create a new chat bot named Charlie
chatbot = chatterbot.ChatBot("Zanuuudina",
                             storage_adapter="chatterbot.storage.MongoDatabaseAdapter",	# MongDB
							 #storage_adapter='chatterbot.storage.SQLStorageAdapter',	# SQLite3
                             # logic_adapters=[
                             #   "chatterbot.logic.TimeLogicAdapter",
                             #   "chatterbot.logic.MathematicalEvaluation",
                             #   "chatterbot.logic.BestMatch",
                             # {
                             #     'import_path': 'chatterbot.logic.LowConfidenceAdapter',
                             #     'threshold': 0.65,
                             #     'default_response': 'Я не понимаю. :\'('
                             # }
                             # "chatterbot.adapters.logic.ClosestMatchAdapter"
                             # "chatterbot.adapters.logic.ClosestMeaningAdapter"
                             # "chatterbot.adapters.logic.ApproximateSentenceMatchAdapter"
                             # ],
                             # filters=["chatterbot.filters.RepetitiveResponseFilter"],
                             logic_adapters=[
                                 'chatterbot.logic.BestMatch'  # ,
                                 # {
                                 #     'import_path': 'chatterbot.logic.LowConfidenceAdapter',
                                 #     'threshold': 0.65,
                                 #     'default_response': 'Я не понимаю. :\'('
                                 # }
                             ],
                             filters=[
                                 'chatterbot.filters.RepetitiveResponseFilter'
                             ],
                             database="Zanuda-01")  # mongoDB
                             #database='./Zanuda-01.sqlite3')  # SQLite3

last_messages = {}
last_user = 0
delay_response = time.time()
ignore_users =  [126624463952412672, 172002275412279296,
                83010416610906112, 83010416610906112,
                161160351591825409, 187406062989606912,
                187406062989606912, 188064764008726528,
                218483879575683073, 218109453344571392,
                209069658475593729, 159985870458322944,
                337876653395017739
                ]

allowed_channels = [354277801412788244]

admins = [101286123950592000, 101388890312552448]

chatbot.set_trainer(chatterbot.trainers.ListTrainer)

def is_admin():
    """Checks if message author is admin"""
    def predicate(ctx): # Вне is_admin не существует(имя можно использовать вне как угодно)
        return int(ctx.message.author.id) in admins
    return commands.check(predicate)

"""def check_epmty_arg(arg):
    '''Check whether arg was empty or not'''
    def predicate(ctx): # Вне check_epmty_arg не существует(имя можно использовать вне как угодно)
        return len(ctx.message) > 0
    return commands.check(predicate)"""

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print(str(len(bot.servers)) + ' servers')
    await bot.change_presence(game=discord.Game(name='Мне скучно...'))
    await bot.send_message(
        discord.utils.get(bot.get_all_channels(), server__name='Mistral-gi', name='aasdas'), random.choice(["Всем привет! ^_^", "Всем хай!", "Здравствуйте!"]))


@bot.command(pass_context=True)
@is_admin()
async def удалить(ctx, *, arg):
    """removes the string from chatbot database"""
    arg = arg.replace("{d}", '') # don't know why this was used for
    if arg is not None and len(arg) > 0:
        chatbot.storage.remove(arg)
        await bot.add_reaction(ctx.message, "BibleThump:230285403033305088")
    else:
        await bot.send_typing(ctx.message.channel)
        await bot.send_message(ctx.message.channel, "Ошибка, не могу удалить сообщение из базы.")

@bot.command(pass_context=True)
@is_admin()
async def аватарка(ctx, *, arg):
    """Adds two numbers together."""
    arg = arg.strip(" ")
    if arg is not None and len(arg) > 0:
        try:
            response = http_get(arg)
            await bot.edit_profile(avatar=response.content)
            await bot.add_reaction(ctx.message, "❤")
        except Exception:
            await bot.say('Ошибка! Не удалось загрузить изображение: '+arg)

@bot.command(pass_context=True)
@is_admin()
async def имя(ctx, *, arg):
    """Adds two numbers together."""
    name = arg.strip(" ")
    if name is not None and len(name) > 0:
        await bot.edit_profile(username=name)
        await bot.add_reaction(ctx.message, "❤")

@bot.command(pass_context=True)
@is_admin()
async def дебаг(ctx, *, arg):
    """Adds two numbers together."""
    # await bot.say(left + right)
    if arg is not None and len(arg) > 0:
        chatbot.storage.remove(arg)
        await bot.send_typing(ctx.message.channel)
        await bot.say("```{}```".format(chatbot.get_response(arg)))
    return
	
@bot.command(pass_context=True)
@is_admin()
async def debug(ctx, *, arg):
    """Adds two numbers together."""
    await bot.say(arg)
    if arg is not None and len(arg) > 0:
        chatbot.storage.remove(arg)
        await bot.send_typing(ctx.message.channel)
        await bot.say("```{}```".format(chatbot.get_response(arg)))
    return

@bot.command(pass_context=True)
@is_admin()
#@check_epmty_arg()
async def d1(ctx, *, arg):
    """Debug use only."""
    if arg is not None and len(arg) > 0:
        #chatbot.storage.remove(arg)
        await bot.send_typing(ctx.message.channel)
        #await bot.say(ctx.message.content)  # Не передаётся. Только arg
        await bot.say(ctx.message.author)
        await bot.say(arg)
        #await bot.say("```{}```".format(chatbot.get_response(arg)))
    return

@bot.command(pass_context=True)
@is_admin()
async def учить(ctx, *, arg):
    """Adds two numbers together."""
    # await bot.say(left + right)
    if arg is not None and len(arg) > 0:
        arg = arg.split(";")
        await bot.say('Насчитал '+str(len(arg))+" подстрок")
        chatbot.train(arg)
        await bot.add_reaction(ctx.message, "❤")

@bot.event
async def on_message(message):
    global delay_response
    # we do not want the bot to reply to itself
    if message.author == bot.user:
        return
    # await bot.send_message(message.channel, str(int(message.author.id)))
    mentioned = False
    msg = message.content
    if bot.user.name.lower() == message.content.lower()[:len(bot.user.name)]:
        msg = msg[len(bot.user.name):]
        mentioned = True
    else:
        while bot.user.name in msg or re.search(r'Зануде|Зануду|Зануды|Занудой', msg) is not None:
            index = None
            try:
                index = msg.index(bot.user.name)
            except:
                pass

            if index is not None and index == 0:
                msg = msg.replace(bot.user.name, '', 1).strip("    ,`")
            elif re.search(r'Зануде|Зануду|Зануды|Занудой', msg) is not None:
                msg = msg.replace("Зануде", '{U}', 1).strip("    ,`")
                msg = msg.replace("Зануду", '{U}', 1).strip("    ,`")
                msg = msg.replace("Зануды", '{U}', 1).strip("    ,`")
                msg = msg.replace("Занудой", '{U}', 1).strip("    ,`")
            else:
                msg = msg.replace(bot.user.name, '{U}', 1).strip("    ,`")

            mentioned = True

    if len(msg) > 1:
        if msg[0] == "+":
            msg = msg[1:]
            mentioned = True

    if message.server == None:
        msg = msg.strip("    ,`")
        if len(str(msg)) > 0:
            msg = msg[0].upper() + msg[1:]
    else:
        msg = msg.replace(message.server.me.mention, '').strip("    ,`")
        if len(str(msg)) > 0:
            msg = msg[0].upper() + msg[1:]

    if len(str(msg)) <= 0:
        return

    for mention in message.mentions:
        if bot.user.name != mention.name:
            msg = msg.replace(mention.mention, mention.display_name)
            try:
                index = msg.index(mention.display_name)
                if index == 0:
                    msg = msg.replace(mention.display_name, '', 1).strip("    ,`")
            except:
                pass

    if message.server == None:
        await bot.send_message(message.channel, "Извините, личка пока отключена до лучших времен. :(")
        return

    # print("ПМ | " + msg)
    # if len(str(msg)) <= 2:
    #     await client.send_typing(message.channel)
    #     await client.send_message(message.channel, "```Слишком кратенько что-то!```")
    #     return
    #
    # if len(str(msg)) >= 150:
    #     await client.send_typing(message.channel)
    #     await client.send_message(message.channel, "```Слишком сложно, я столько не осилю!```")
    #     return
    #
    # if msg[0] == "!" or msg[:2].lower() == "t!":
    #     await client.send_typing(message.channel)
    #     await client.send_message(message.channel, "```Эй, не надо меня учить всяким гадостям!```")
    #     return
    #
    # await client.send_typing(message.channel)
    # response = str(chatbot.get_response(msg))
    # if response[0] == "!" or response[0] == "|" or response[:2].lower() == "t!":
    #     chatbot.storage.remove(response)
    #     await client.send_message(message.channel,
    #                               "```В ответе была какая-то гадость и мне её пришлось удалить :(\n{}```".format(
    #                                   response))
    #     return
    #
    # response = response.strip("    ,`\t")
    # response = response[0].upper() + response[1:]
    # response = response.replace("{U}", message.author.display_name)
    #
    # await client.send_message(message.channel, response)
    elif bot.user in message.mentions or mentioned is True:
        if delay_response + 5 > time.time():
            await bot.add_reaction(message, "smug:313007336635498497")
            return
        else:
            delay_response = time.time()

        if int(message.author.id) in ignore_users:
            return

        if message.channel.permissions_for(message.server.me).send_messages is True:
            if len(str(msg)) < 1:
                # await client.send_typing(message.channel)
                # await client.send_message(message.channel, "```Слишком кратенько что-то!```")
                return

            if len(str(msg)) >= 500:
                await bot.send_message(message.channel, "```Слишком сложно, я столько не осилю!```")
                return

            if msg[0] == "!" or msg[:2].lower() == "t!" or msg[0] == ".":
                await bot.send_message(message.channel, "```Эй, не надо меня учить всяким гадостям!```")
                return

            # print("Чат | " + msg)
            await bot.send_typing(message.channel)
            response = str(chatbot.get_response(msg))
            # if response[0] == "!" or response[0] == "|" or response[:2].lower() == "t!":
            #     chatbot.storage.remove(response)
            #     await client.send_message(message.channel,
            #                               "```В ответе была какая-то гадость и мне её пришлось удалить :(\n{}```".format(
            #                                   response))
            #     return

            response = response.strip("    ,`\t").replace("```", "")
            response = response[0].upper() + response[1:]

            response = response.replace("{U}", message.author.display_name)

            await bot.send_message(message.channel, response)
            # elif 5 <= len(str(msg)) <= 150 and msg[0] != "!" and msg[0] != "|" and msg[:2] != "t!" and int(
            #         message.author.id) not in ignore_users and int(message.channel.id) in allowed_channels:
            #     channel_id = message.channel.id
            #
            #     if channel_id not in last_messages:
            #         last_messages[channel_id] = []
            #
            #     last_messages[channel_id].append(msg)
            #     if len(last_messages[channel_id]) >= 10:
            #         # print("Тренирую: " + str(last_messages[channel_id]))
            #         chatbot.train(last_messages[channel_id])
            #         last_messages[channel_id].clear()
            #         # pass
    await bot.process_commands(message)


print('Starting...')
bot.run('Bot_token') # Токен Бота
