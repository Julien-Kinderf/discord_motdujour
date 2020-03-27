import discord
from discord.ext import commands
import os
import random
from dotenv import load_dotenv

# Global variables
pathToCurrentDirectory = os.path.realpath(__file__)
pathToWords = os.path.dirname(pathToCurrentDirectory) + "/../ocr/txt/words"
pathToUsedWords = os.path.dirname(
    pathToCurrentDirectory) + "/../ocr/txt/used_words"


def getword():
    # This function returns a list containing :
    # - the word of the day
    # - it's defintion
    # - the examples

    # let's choose a random word among all of our words
    word = random.choice(os.listdir(pathToWords))
    #print(f"Le mot choisi est : {word}")

    # let's get the textfile associated with this word
    with open(pathToWords + '/' + word, 'r') as textfile:
        word_text = textfile.read()

    # let's format it nicely for discord
    word_text = word_text.replace("\n", " ").replace(
        ".", ".\n").strip().replace("\n ", "\n")
    #print(f"Sa définition est la suivante : \n{word_text}\n")

    # let's move the file to the used words folder
    #os.replace(pathToWords + '/' + word, pathToUsedWords + '/' + word)
    #print(f"==> Mot {word} déplacé dans 'used_words/'")

    result = [word, word_text]
    return(result)


def backToDefault():
    # This function is useful only in developpment phase
    # It transfers back all of the files from used_words to words
    for word in os.listdir(pathToUsedWords):
        os.replace(pathToUsedWords + '/' + word, pathToWords + '/' + word)


os.system('clear')
# backToDefault()

# First get the word of the day
wordOfTheDay = getword()

# Then connect to discord
load_dotenv()
token = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='=', description="test")


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

    activity = discord.Activity(
        name='Confinement Simulator 2020', type=discord.ActivityType.playing)
    await bot.change_presence(activity=activity)


@bot.event
async def on_message(message):
    """Answers to messages"""
    if message.author != bot.user:
        if ("di" in message.content.lower()):
            index = message.content.lower().index("di") + 2
            # Si il a dit dit
            print(message.content[index: index + 1])
            if (message.content[index: index + 2] == "t "):
                print("Il a dit dit !")
                index += 2
            response = message.content[index:] + " :D"
            await message.channel.send(response)

    await bot.process_commands(message)


@bot.command()
async def quitter(ctx):
    """Leaves the server."""
    print(f"Closing the bot as asked by {ctx.author.name}")
    await bot.close()


@bot.command()
async def mot(ctx):
    """Send a random word and it's definition"""
    word = getword()
    #print(f"Le mot trouvé est :\n{word}")

    definition = word[1].replace(".\n", '.\n\n*', 1) + '*'
    word = word[0]

    message = f"__**{word} :**__\n{definition}\n"
    await ctx.send(message)
    print(f"Word asked by {ctx.author.name} : {word} delivered")


bot.run(token)
