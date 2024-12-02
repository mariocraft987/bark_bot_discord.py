# Code for Bark Dog discord bot

import asyncio
import discord

from discord import app_commands
from discord.ext import commands, tasks
from itertools import cycle
import random
from random import sample, shuffle
import json
import os

# all bad words to censor
bad_words = ["fuck", "fock", "f0ck", "fvck", "fck", "fug", "bitch", "btch", "b!tch", "b1tch", "bich", "cock", "coc", "coc", "kok", "sex", "sexy", "kys", "kill your self", "idiot", "penis"]

# commented out because of new slash commands
# bot = commands.Bot(command_prefix="$", intents=discord.Intents.all())

intents = discord.Intents.default()
bot = discord.Client(intents=intents)
tree = app_commands.CommandTree(bot)

bot_statuses = cycle(["Bark Coding"])

welcoming_words = ["Hello, ", "Welcome, ", "Hope you brought dog treats, ", "Hiyas and hois, ", ":bark_woof: Hi, "]
magic_8_ball_replies = ["It is certain", "It is decidedly so", "Without a doubt", "Yes definitely", "You may rely on it", "As I see it, yes", "Most likely", "Outlook good", "Yes", "Signs point to yes", "Don't count on it", "My reply is no", "My sources say no", "Outlook not so good", "Very doubtful", "Reply hazy, try again", "Ask again later", "Better not tell you now", "Cannot predict now", "Concentrate and ask again"]
animals = ["😺", "🐶", "🐺", "🐵", "🐯", "🦁", "🦒", "🦊", "🦝", "🐮", "🐷", "🐭", "🐗", "🐹", "🐰", "🐻", "🐻‍❄️", "🐨", "🐼", "🐸", "🦓", "🐲", "🐔", "🦄", "🫏", "🫎", "🐴", "🐧"]

GUILD_ID = 1225552735445843978

class SimpleView(discord.ui.View):

    @discord.ui.button(label="Get Money",
                       style=discord.ButtonStyle.success)
    async def hello(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(f"💵 - Earned {random.randrange(1, 5)} BarkBucks!")

x = range(50)

os.chdir("C:/Users/mtsim/OneDrive/Desktop/cool/main/bark_files/barkbot-discord-bot/")

# variable declaring
# ----------------------------------------------------------------------------------------------------------------

def censorWord(word):
        bad_words_length = len(bad_words)

        censored_args = word

        for i in range(bad_words_length):
            censored_args = censored_args.replace(f"{bad_words[i]}", "[censored]")
        return censored_args

@tasks.loop(seconds=60)
async def change_bot_status():
    # await bot.change_presence(activity=discord.Game(next(bot_statuses)))

    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Bark Coding"))

@bot.event
async def on_ready():
    print("-----------------------------------------------------")
    print("ready when you are!")
    change_bot_status.start()
    try:
        # some fancy shit to add the guild id too
        synced = await tree.sync(guild=discord.Object(id=GUILD_ID))
        print(f"Synced {len(synced)} commands on guild: {GUILD_ID}")
    except Exception as e:
        print(f"Error: {e}")

# now for actually the commands
# ----------------------------------------------------------------------------------------------------------------

@tree.command(
    name="ping",
    description="The bot replies \"Ping Pong!\" back.",
    guild=discord.Object(id=GUILD_ID)
)
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Ping Pong!")


@tree.command(
    name="help",
    description="A list of commands for you to use",
    guild=discord.Object(id=GUILD_ID)
)
async def help(interaction: discord.Interaction):
    
    embed = discord.Embed(title="Information",
                      description="I am Bark Dog, created by AtomicBolts \n_Currently being worked on._",
                      colour=0x00b0f4)

    embed.set_author(name="Bark Dog",
                 url="https://discordapp.com/users/1235336441698058341",
                 icon_url="https://cdn.discordapp.com/avatars/1235336441698058341/2778b044d76c7f3975a444c658a0ac05.webp?size=128")

    embed.add_field(name="Available cmds",
                value="/ping\n/say [str]\n/treasure\n/magic8ball [str]\n/shop",
                inline=False)

    embed.set_footer(text="Bark Discord bot info")

    await interaction.response.send_message(embed=embed)


@tree.command(
    name="say",
    description="Makes the bot say something",
    guild=discord.Object(id=GUILD_ID)
)
async def say(interaction: discord.Interaction, message: str):

        await interaction.response.send_message(f"{censorWord(message)}")



@tree.command(
    name="treasure",
    description="A random treasure finding game",
    guild=discord.Object(id=GUILD_ID)
)
async def treasure(interaction: discord.Interaction):
    msg_to_send = f"### Treasure!\n"

    for n in x:
        if (n == 10 or n == 20 or n == 20 or n == 30 or n == 40 or n == 50):
            msg_to_send += "\n"

        if (random.randint(1, 6) == 2):
            if (random.randint(1, 8) == 5):
                msg_to_send += "||💰||"
            else:
                msg_to_send += "||🪙||"
        else:
            msg_to_send  += "||🚫||"

    await interaction.response.send_message(msg_to_send)

@tree.command(
    name="magic_8_ball",
    description="A random treasure finding game",
    guild=discord.Object(id=GUILD_ID)
)
async def magic_8_ball(interaction: discord.Interaction, message: str):
    embed = discord.Embed(title=f"🎱 - {random.choice(magic_8_ball_replies)}",
                      description=f"Magic 8 ball says to {message}...",
                      colour=0x3500f5)

    embed.set_author(name="Bark Dog",
                 url="https://discordapp.com/users/1235336441698058341",
                 icon_url="https://cdn.discordapp.com/avatars/1235336441698058341/2778b044d76c7f3975a444c658a0ac05.webp?size=128")
    await interaction.response.send_message(embed=embed)

'''

        ARCHIVED COMMANDS

# Pizza command
@bot.command()
async def pizza(ctx):
    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in ["🍴"]
    
    message = await ctx.send(f"### {ctx.author.mention} used $Pizza\nReact \"🍴\", to eat the pizza.\n\n🍕🍕🍕🍽️")
    confirmation = await bot.wait_for("reaction_add", check=check)

    if confirmation:
        await message.edit(content=message.content.replace("🍕🍕🍕🍽️", "🍽️"))

# Guess my animal game
@bot.command()
async def animal(ctx):
    guessed_animal = random.choice(animals)

    await ctx.send("I am thinking of an animal right now...\n\nChoices: \"😺🐶🐺🐵🐯🦁🦒🦊🦝🐮🐷🐭🐗🐹🐰🐻🐻‍❄️🐨🐼🐸🦓🐲🐔🦄🫏🫎🐴🐧\"\n-# Game currently under development, don't expect that much from it.")

    def check(m):
        return m.content == guessed_animal and m.channel == ctx.channel
    
    guesses = 10
    
    while 10 > 0:

        msg = await bot.wait_for("message", check=check)
        
        if msg.content == guessed_animal:
            print("right")
            await msg.reply("Right!")
            break
        else:
            print("wrong")
            await msg.reply("Wrong...")
            guesses - 1
        continue


# Bagels deduction game
@bot.command()
async def bagels(ctx):
    def check(m):
        return m.content == "hello"

    await ctx.send(f"### {ctx.author.mention} used $Bagels\nWhen I say \"Pico\", one digit is right, but in the wrong position.\nWhen I say \"Fermi\", one digit is right, and in the right position.\nWhen I say \"Bagels\", no digits are right.\nGuess what number am I thinking of.\n-# Idea by breakfast")

    letters = sample('0123456789', 3)
    if letters[0] == '0':
        letters.reverse()

    number = ''.join(letters)

    while True:
        confirmation = await bot.wait_for("message", check=check)

        if confirmation:
            if len(confirmation.content) != 3:
                await confirmation.reply("Input not 3 digits!")
            if confirmation.content == "exit":
                break
'''

@tree.command(
    name="shop",
    description="Shows the shop",
    guild=discord.Object(id=GUILD_ID)
)
async def shop(interaction: discord.Interaction):
    embed = discord.Embed(title="SHOP",
                      colour=0xeb4034)

    embed.set_author(name="Bark Bot",
                 url="https://discordapp.com/users/1235336441698058341",
                 icon_url="https://cdn.discordapp.com/avatars/1235336441698058341/2778b044d76c7f3975a444c658a0ac05.webp?size=128")

    embed.add_field(name="Items",
                value="<@&1308852389016633454>\n- 300 BarkBucks\n<@&1257055961575592050>\n- 700 BarkBucks\n<@&1308852795063140434>\n- 50 BarkBucks",
                inline=False)

    embed.set_footer(text="BarkBucks Shop")

    await interaction.response.send_message(embed=embed)

'''

# goofy ahh me copied a tutorial
async def open_account(user):
    users = await get_bank_data()

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = 0
        users[str(user.id)]["bank"] = 0

    with open("bank.json", "w") as f:
        json.dump(users, f)
    return True


async def get_bank_data():
    with open("bank.json", "r") as f:
        users = json.load(f)
    
    return users


@tree.command(
    name="balance",
    description="Shows your balance",
    guild=discord.Object(id=GUILD_ID)
)
async def balance(interaction: discord.Interaction):
    await open_account(ctx.author)

    user = ctx.author
    users = await get_bank_data()

    wallet_amt = users[str(user.id)]["wallet"]
    bank_amt = users[str(user.id)]["bank"]

    em = discord.Embed(title = f"{ctx.author.name}'s BarkBuck balance", color = discord.Color.green())
    em.add_field(name = "BarkBuck Balance:", value = wallet_amt)
    em.add_field(name = "Bank:", value = bank_amt)
    await interaction.response.send_message(embed = em)

@bot.command()
async def barkbuck_give_user(ctx, target, amount):
    await open_account(ctx.author)

    target_user = await bot.fetch_user(target)
    user = ctx.author
    users = await get_bank_data()

    await ctx.send(f"{ctx.author.name} gave {target_user.name} {amount} Barkbucks")

    users[str(target)]["wallet"] += amount
    users[str(user.id)]["wallet"] -= amount

    with open("bank.json", "w") as f:
        json.dump(users, f)

@bot.command()
async def barkbuck_shower(ctx):
    view = SimpleView()

    message = await ctx.send("Oh! it's raining BarkBucks!\n💸💸💸💸💸💸",view=view)
    message_id = message.id

    await asyncio.sleep(5)

    channel = await bot.fetch_channel(1253886083264151604)

    msg = await channel.fetch_message(message_id)   
    await msg.delete()

'''


with open("token.txt") as f:
    token = f.read()

bot.run(token)