# Code for Bark Dog discord bot

import discord
from discord.ext import commands, tasks
from itertools import cycle
from keep_alive import keep_alive
import random
from keep_alive import keep_alive

# all bad words to censor
bad_words = ["fuck", "fock", "f0ck", "fvck", "fck", "fug", "shit", "sht", "sh!t", "shid", "$hit", "bitch", "btch", "b!tch", "b1tch", "bich", "cock", "coc", "sex",  "sexy", "kys", "kill your self", "idiot"]

bot = commands.Bot(command_prefix="$", intents=discord.Intents.all())

bot_statuses = cycle(["Bark Coding", "Bark Advanced", "Fetch", "& being worked on"])

welcoming_words = ["Hello, ", "Welcome, ", "Hope you brought dog treats, "]

@tasks.loop(seconds=50)
async def change_bot_status():
    await bot.change_presence(activity=discord.Game(next(bot_statuses)))

@bot.event
async def on_ready():
    print("ready when you are!")
    change_bot_status.start()


# info command
@bot.command()
async def info(ctx):
    embed = discord.Embed(title="Information",
                      description="My info \n_currently being workedon_",
                      colour=0x00b0f4)

    embed.set_author(name="Bark Dog",
                 url="https://discordapp.com/users/1235336441698058341",
                 icon_url="https://cdn.discordapp.com/avatars/1235336441698058341/2778b044d76c7f3975a444c658a0ac05.webp?size=128")

    embed.add_field(name="Available cmds",
                value="$info\n$welcome\n$say [text]\n$reply  [text] _(UNDER DEV)_\n$report [user] [user id] [reason]\n$reaction [id] [emoji] _(UNDER DEV)_",
                inline=False)

    embed.set_footer(text="Bark Discord bot info")

    await ctx.reply(embed=embed)


# welcome command
@bot.command()
async def welcome(ctx):
    await ctx.reply(random.choice(welcoming_words) + ctx.author.mention)


# say command
@bot.command()
async def say(ctx, args):

    if discord.utils.get(ctx.author.roles, name="botMod").name == "botMod":  
        # censor these

        bad_words_length = len(bad_words)

        censored_args = args

        for i in range(bad_words_length):
            censored_args = censored_args.replace(f"{bad_words[i]}", "[censored]")

        await ctx.send(f"{censored_args}")


    # reply command
@bot.command()
async def reply(ctx, word):
    
    if discord.utils.get(ctx.author.roles, name="botMod").name == "botMod":  
        # censor these

        bad_words_length = len(bad_words)

        censored_reply = word

        for i in range(bad_words_length):
            censored_reply = censored_reply.replace(f"{bad_words[i]}", "[censored]")
    
    await ctx.reply(f"{censored_reply}")

# send dm command
@bot.command()
async def send_dm(ctx, id):
    user = await bot.fetch_user(id)
    await user.send("Hello there!\n Bark Coding has a new account system, Just go to https://bark.dumorando.com/signup")

# report command
@bot.command()
async def report(ctx, user, userid, reason):

    banana = reason
    apple = user
    
    embed = discord.Embed(title="User report!",
          description=f"{ctx.author.mention} issued a report on Bark user: {apple} \n\nReason: {banana}",
          colour=0xf51800)

    embed.set_author(name="Bark Dog",
     url="https://discordapp.com/users/1235336441698058341",
     icon_url="https://cdn.discordapp.com/avatars/1235336441698058341/2778b044d76c7f3975a444c658a0ac05.webp?size=128")
    
    await ctx.send(embed=embed)
    user = await bot.fetch_user(userid)
    await user.send(f"You have been reported by {ctx.author.mention}\nReason: {banana}")

@bot.command()
async def reaction(ctx, id, emoji):
    msg = await ctx.fetch_message(id)
    reaction = emoji
    await msg.add_reaction(reaction)
    

with open("token.txt") as f:
    token = f.read()

keep_alive()
bot.run(token)
