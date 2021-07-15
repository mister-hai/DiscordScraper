import discord
from discord import commands,ext

import pandas

from src.HTTPRequest import HTTPDownloadRequest
from src.MessageHandler import MessageHandler
from src.DiscordScrape import DiscordScrape,DatabasePacker
from src.database import DiscordMsgDB,DiscordMessage,addmsgtodb
from src.util import redprint,blueprint,greenprint,errormessage,debugmessage
from src.util import warn,yellowboldprint,warning_message,scanfilesbyextension

COMMAND_PREFIX      = "."
bot_help_message    = "I AM"
BOT_PERMISSIONS     = 3072
devs                = [712737412018733076]
#cog_directory_files = os.listdir("./cogs")
load_cogs           = False
bot = commands.Bot(command_prefix=(COMMAND_PREFIX))
#client = discord.Client()
guild = discord.Guild


###############################################################################
#                DISCORD COMMANDS
###############################################################################
# WHEN STARTED, APPLY DIRECTLY TO FOREHEAD
@bot.event
async def on_ready():
    print("Discrod Scraper ALPHA")
    await bot.change_presence(activity=discord.Game(name="yo mamma say .help"))
    #await lookup_bot.connect()

@bot.command(name='command_name', description="SCRAPER SAY CACAWWWWW!")
async def channelpicker(ctx,channel,limit):
    channel.history(limit=200).flatten()

#function to call the scraper class when ordered
@bot.command(name='command_name', description="scraper go BRRRRRR")
# .scrapemessages 10000
async def scrapemessages(ctx,limit = 10000):
    '''performs the operation on the channel it is called in'''
    #start the count!
    scrapecounter = 0
    # set the channel name to scrape
    current_channel = ctx.message.channel
    botusername = bot.user
    #---pandas.dataframe--- something that holds structured information
    # this is essentially a cartridge you push into a slot
    dataframe       = pandas.DataFrame(columns =listofpandascolumns)
    # ---dbpcker--- packs the dataframe into the database
    # feed it the DF
    #   this slot, in this module
    dbpacker        = DatabasePacker(dataframe = dataframe)
    # msghandler filters messages and attachments
    # and its a module in a machine that fits alongside this module 
    msghandler      = MessageHandler(domainlist = domainlist)
    # This machine right here
    # This machine that takes two modules, one of which takes a cartridge to hold stuff
    scraper         = DiscordScrape(token = token,
                                    username = botusername,
                                    #dbtype = dbtype,
                                    dbsaveformat = dbsaveformat,
                                    current_channel = current_channel,
                                    dbpacker = dbpacker,
                                    msghandler = msghandler,
                                    imagesaveformat = imagesaveformat,
                                    images = images
                                    )
    #itterate over messages in channel until limit is reached
    for msg in current_channel.history(limit):
        # filter the message
        # even if you dont expect a message from the bot to be in there
        # you should filter that out JUST IN CASE
        # never allow "reflections"
        if ctx.message.author != bot.user:
            #if the messages scan right
            if scraper.handler.filtermessage(message=msg):
                scraper.processmessageinloop(message=msg)
                scrapecounter += 1
            #stop at message limit
            if scrapecounter == limit:
                break
            else:
                pass
greenprint("[+] Loaded Discord commands")