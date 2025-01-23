# source code for Bark Dog discord bot

import asyncio
import typing
import discord
import requests

from discord import app_commands
from discord.ext import commands, tasks

from discord import Webhook
import aiohttp
import datetime

from typing import Optional

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

# ----------------------------------------------------------------------------------------------------------------
# classes

class SimpleView(discord.ui.View):

    @discord.ui.button(label="Get Money",
                       style=discord.ButtonStyle.success)
    async def hello(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(f"💵 - Earned {random.randrange(1, 5)} BarkBucks!")

class shopDropdown(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Cool Role", description="The Cool Role"),
            discord.SelectOption(label="VIP Role", description="The Special (VIP) Role"),
            discord.SelectOption(label="Mythical", description="The Mythical Role")
        ]

        super().__init__(placeholder="Buy something?", options=options, min_values="1", max_values="1")

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"You chose {self.values[0]}!", ephemeral=True)

class shopView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(shopDropdown())


x = range(50)

# change this please
os.chdir("C:/Users/CURRENTUSER/OneDrive/Desktop/cool/main/bark_files/barkbot-discord-bot/")

# variable declaring
# ----------------------------------------------------------------------------------------------------------------

def censorWord(word):
        bad_words_length = len(bad_words)

        censored_args = word

        for i in range(bad_words_length):
            censored_args = censored_args.replace(f"{bad_words[i]}", "[censored]")
        return censored_args

async def logo_submit(url, file, user):
    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(url, session=session)
        await webhook.send(f"NEW FILE SUBMISSION!\n\n{file}\nFrom {user}")

async def email_submit(url, email, user, leave):
    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(url, session=session)

        if (leave == True):
            await webhook.send(f"<@1223056351346036817>,\n{user} wants to to leave the mailing list :(")
        elif (leave == False):
            await webhook.send(f"<@1223056351346036817>,\nNEW EMAIL SUBMISSION!\n\n**Email: **{email}\n**From:** {user}")

        # emails.txt has emails stored

@tasks.loop(seconds=60)
async def change_bot_status():
    # await bot.change_presence(activity=discord.Game(next(bot_statuses)))

    # await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Bark Coding"))

    await bot.change_presence(activity=discord.CustomActivity(name='Dog stuff'))

@bot.event
async def on_ready():
    print("-----------------------------------------------------")
    print("ready when you are!")
    change_bot_status.start()
    try:
        # some fancy shit to add the guild id lol
        synced = await tree.sync(guild=discord.Object(id=GUILD_ID))
        print(f"Synced {len(synced)} commands on guild: {GUILD_ID}")
    except Exception as e:
        print(f"Error: {e}")

# now for actually the commands
# ----------------------------------------------------------------------------------------------------------------

@tree.command(
    name="ping",
    description="The bot replies \"Pong\" back.",
    guild=discord.Object(id=GUILD_ID)
)
async def ping(interaction: discord.Interaction):
    b = datetime.datetime.now()
    response = requests.get('http://bark.dumorando.com')

    await interaction.response.send_message(f"Pong!\n**Website Status:** {response.status_code}\n**Response Time:** {((datetime.datetime.now() - b).total_seconds() * 1000)} ms\n**Am I Being Nerdy:** True")


@tree.command(
    name="help",
    description="A list of commands for you to use.",
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
                value="- /ping\n- /say [str]\n- /treasure\n- /magic_8_ball [str]\n- /shop\n- /give [user] [amount of barkbucks]\n- /submit [file]\n- /animal\n- /bagels [use_emojis]\n- /idiotify [text]\n- /email [your_email]\n- /email_leave",
                inline=False)

    embed.set_footer(text="Bark Discord bot info")

    await interaction.response.send_message(embed=embed)


@tree.command(
    name="say",
    description="Makes the bot say something.",
    guild=discord.Object(id=GUILD_ID)
)
async def say(interaction: discord.Interaction, message: str):

        await interaction.response.send_message(f"{censorWord(message)}")

@tree.command(
    name="treasure",
    description="A random treasure finding game.",
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
    description="Ask the Magic 8 Ball a question.",
    guild=discord.Object(id=GUILD_ID)
)
async def magic_8_ball(interaction: discord.Interaction, message: str):
    embed = discord.Embed(title=f"🎱 - {random.choice(magic_8_ball_replies)}",
                      description=f"Magic 8 ball says to \"{message}\"...",
                      colour=0x3500f5)

    embed.set_author(name="Bark Dog's Magic 8 Ball",
                 url="https://discordapp.com/users/1235336441698058341",
                 icon_url="https://imagizer.imageshack.com/img923/7517/Qko5zv.png")
    await interaction.response.send_message(embed=embed)


@tree.command(
    name="submit",
    description="Like PenguinMod, submit an image that will go into our library.",
    guild=discord.Object(id=GUILD_ID)
)
async def submit(interaction: discord.Interaction, file: discord.Attachment):
    await interaction.response.send_message(f"Sended to <#1314674085032235019>\n\n{file}", ephemeral=True)

    url = "https://discord.com/api/webhooks/1314675135101407242/CSl_uzdBR3hM3-mFPU5Uv7YlMSiQSAs6rN96hYCx6jhoOnOjV7Oum7zrPF9krJvd3vJF"

    loop = asyncio.new_event_loop()
    loop.run_until_complete(await logo_submit(url, file, interaction.user.mention))
    loop.stop()

@tree.command(
    name="help_email",
    description="What the /email and /email_leave command does.",
    guild=discord.Object(id=GUILD_ID)
)
async def help_email(interaction: discord.Interaction):
    embed = discord.Embed(title="Information - /Email",
                      colour=0x00b0f4,
                      timestamp=datetime.now())

    embed.set_author(name="Bark Dog",
                 url="https://discordapp.com/users/1235336441698058341",
                 icon_url="https://cdn.discordapp.com/avatars/1235336441698058341/2778b044d76c7f3975a444c658a0ac05.webp?size=128")

    embed.add_field(name="How this works?",
                value="When `/email` is executed, a webhook is sent \nto another server, which only has the admins, for privacy. \nA Gmail account called _cytrincstudios@gmail.com_, will then \nmessage you every time a new update is made.",
                inline=False)
    embed.add_field(name="A New Field",
                value="",
                inline=False)

    embed.set_footer(text="Bark Discord email info")

    await interaction.response.send_message(embed=embed)

@tree.command(
    name="email",
    description="Enter our mailing list.",
    guild=discord.Object(id=GUILD_ID)
)
async def email(interaction: discord.Interaction, email: str):
    await interaction.response.send_message(f"Joined mailing list", ephemeral=True)

    url = "WEBHOOK_URL"

    loop = asyncio.new_event_loop()
    loop.run_until_complete(await email_submit(url, email, interaction.user.mention, False))
    loop.stop()

@tree.command(
    name="email_leave",
    description="Leave our mailing list.",
    guild=discord.Object(id=GUILD_ID)
)
async def email(interaction: discord.Interaction):
    await interaction.response.send_message(f"Left mailing list", ephemeral=True)

    url = "https://discord.com/api/webhooks/1324085179962097734/XOLpRBDBE5y7j_hWdAyc791q7JsGVwfaxpPgOkRdwJ5zDGoDX0ezmiwSJcwSyWnl4oGS"

    loop = asyncio.new_event_loop()
    loop.run_until_complete(await email_submit(url, None, interaction.user.mention, True))
    loop.stop()

@tree.command(
    name="idiotify",
    description="Idiotify your text.",
    guild=discord.Object(id=GUILD_ID)
)
async def idiotify(interaction: discord.Interaction, message: str):
    await interaction.response.send_message(f"{message}")

@tree.command(
    name="links",
    description="Sends back every Bark URL in existent.",
    guild=discord.Object(id=GUILD_ID)
)
async def links(interaction: discord.Interaction):
    await interaction.response.send_message(f"- https://bark.dumorando.com\n- https://bark-editor.vercel.app\n- https://api.bark.dumorando.com\n- https://bark-coding-pb.vercel.app")


@tree.command(
    name="animal",
    description="Play an animal guessing game.",
    guild=discord.Object(id=GUILD_ID)
)
async def animal(interaction: discord.Interaction):
    await interaction.response.send_message("Guess what animal i'm thinking of!\nReply the animal emoji, and i'll tell you if its right or wrong.\n**CHOICES:**\n😺🐶🐺🐵🐯🦁🦒🦊🦝🐮🐷🐭🐗🐹🐰🐻🐻‍❄️🐨🐼🐸🦓🐲🐔🦄🫏🫎🐴🐧\n\nreply \"leave\" to exit game.")

    animal_in_mind = random.choice(animals)

    def check(m):
        return True

    while True:
        msg = await bot.wait_for("message", check=check)
        if (msg.content == animal_in_mind):
            await interaction.followup.send(f"CORRECT!")
        if (msg.content == "leave"):
            await interaction.followup.send(f"Sorry you didn't get it right :(\nThe answer was \"{animal_in_mind}\"")
            break
        else:
            await interaction.followup.send(f"Incorrect.")

@tree.command(
    name="bagels",
    description="Play the bagels deduction game.",
    guild=discord.Object(id=GUILD_ID)
)
async def bagels(interaction: discord.Interaction, use_emojis: typing.Literal['Yes', 'No']):
    await interaction.response.send_message("In Development!")


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
    description="Shows the shop items and their price.",
    guild=discord.Object(id=GUILD_ID)
)
async def shop(interaction: discord.Interaction):
    embed = discord.Embed(title="SHOP",
                      colour=0xeb4034)

    embed.set_author(name="Bark Bot",
                 url="https://discordapp.com/users/1235336441698058341",
                 icon_url="https://cdn.discordapp.com/avatars/1235336441698058341/2778b044d76c7f3975a444c658a0ac05.webp?size=128")

    embed.add_field(name="Items",
                value="<@&1308852389016633454>\n- 300 BarkBucks\n<@&1257055961575592050>\n- 700 BarkBucks\n<@&1308852795063140434>\n- 50 BarkBucks\n<@&1311824504137318530>\n- 150 BarkBucks",
                inline=False)

    embed.set_footer(text="BarkBucks Shop")

    await interaction.response.send_message(embed=embed)

# goofy ahh me copied a tutorial
async def open_account(user):
    users = await get_bank_data()

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = 0
        users[str(user.id)]["karma"] = 0

    with open("bank.json", "w") as f:
        json.dump(users, f)
    return True


async def get_bank_data():
    with open("bank.json", "r") as f:
        users = json.load(f)
    
    return users


@tree.command(
    name="balance",
    description="Shows your/a user's BarkBuck and Karma.",
    guild=discord.Object(id=GUILD_ID)
)
async def balance(interaction: discord.Interaction, profile: Optional[discord.Member]):
    if (profile == None):
        user = interaction.user
    else:
        user = profile

    await open_account(user)

    users = await get_bank_data()

    wallet_amt = users[str(user.id)]["wallet"]
    bank_amt = users[str(user.id)]["karma"]

    if (user.id == 1235336441698058341):
        em = discord.Embed(title = f"{user.name}'s BarkBuck balance", color = discord.Color.green())
        em.add_field(name = "BarkBuck Balance:", value = "∞")
        em.add_field(name = "Karma:", value = "∞")
        await interaction.response.send_message(embed = em)
    else:
        em = discord.Embed(title = f"{user.name}'s BarkBuck balance", color = discord.Color.green())
        em.add_field(name = "BarkBuck Balance:", value = wallet_amt)
        em.add_field(name = "Karma:", value = bank_amt)
        await interaction.response.send_message(embed = em)


@tree.command(
    name="shop_buy",
    description="Buy an item from the shop.",
    guild=discord.Object(id=GUILD_ID)
)
async def buy(interaction: discord.Interaction):

    await interaction.response.send_message("Buying something?", view=shopView())


@tree.command(
    name="beg",
    description="Beg for BarkBucks.",
    guild=discord.Object(id=GUILD_ID)
)
async def beg(interaction: discord.Interaction):
    barkbucks_earned = random.randint(0, 3)

    user = interaction.user
    users = await get_bank_data()

    users[str(user.id)]["wallet"] += barkbucks_earned
    users[str(user.id)]["karma"] -= 1

    await interaction.response.send_message(f"You have earned {barkbucks_earned} BarkBucks from begging!\nBut, {user.name}, you lost 1 **Karma** :(")

    with open("bank.json", "w") as f:
        json.dump(users, f)


@tree.command(
    name="give_user",
    description="Gives a user an amount of BarkBucks.",
    guild=discord.Object(id=GUILD_ID)
)
async def give_user(interaction: discord.Interaction, target: discord.Member, amount: int):
    await open_account(interaction.user)

    target_user = target
    user = interaction.user
    users = await get_bank_data()

    if (target_user.id == interaction.user.id):
        await interaction.response.send_message("You cannot give yourself BarkBucks!", ephemeral=True)
    else:
        await interaction.response.send_message(f"{user.mention} gave {target_user.mention} **{amount} Barkbucks**!\nCongrats, {user.name}, you earned 2 **Karma**!")
        users[str(user.id)]["karma"] += 2

    embed = discord.Embed(title="BarkBuck payment",
                      description=f"Hello, {interaction.user.name}!\n\n{interaction.user.mention} from the Bark Coding server, paid you **{amount}** BarkBucks!\n\nCheerio!",
                      colour=0x00ff40)

    embed.set_author(name="Bark Dog",
                 url="https://discord.com/users/1235336441698058341",
                 icon_url="https://cdn.discordapp.com/avatars/1235336441698058341/2778b044d76c7f3975a444c658a0ac05.png")

    embed.set_footer(text="Bark Coding")

    if (target_user.id != interaction.user.id):
        await target.send(embed=embed)

    users[str(target.id)]["wallet"] += amount
    users[str(user.id)]["wallet"] -= amount

    with open("bank.json", "w") as f:
        json.dump(users, f)

'''
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
