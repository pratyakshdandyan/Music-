import discord
import asyncio
import youtube_dl
import os
from discord.ext import commands
from discord.ext.commands import Bot


bot=commands.Bot(command_prefix='a.')

from discord import opus
OPUS_LIBS = ['libopus-0.x86.dll', 'libopus-0.x64.dll',
             'libopus-0.dll', 'libopus.so.0', 'libopus.0.dylib']


def load_opus_lib(opus_libs=OPUS_LIBS):
    if opus.is_loaded():
        return True

    for opus_lib in opus_libs:
            try:
                opus.load_opus(opus_lib)
                return
            except OSError:
                pass

    raise RuntimeError('Could not load an opus lib. Tried %s' %
                       (', '.join(opus_libs)))
load_opus_lib()

in_voice=[]


players = {}
songs = {}
playing = {}


async def all_false():
    for i in bot.servers:
        playing[i.id]=False


async def checking_voice(ctx):
    await asyncio.sleep(130)
    if playing[ctx.message.server.id]== False:
        try:
            pos = in_voice.index(ctx.message.server.id)
            del in_voice[pos]
            server = ctx.message.server
            voice_client = bot.voice_client_in(server)
            await voice_client.disconnect()
            await bot.say("{} left because there was no audio playing for a while".format(bot.user.name))
        except:
            pass

@bot.event
async def on_ready():
   print(bot.user.name)
    
@bot.command(pass_context=True)
async def join(ctx):
   channel = ctx.message.author.voice.voice_channel
   await bot.join_voice_channel(channel)
  
@bot.command(pass_context=True)
async def leave(ctx):
   server = ctx.message.server
   voice_bot = bot.voice_bot_in(server)
   await voice_bot.disconnect()
    
@bot.command(pass_context=True)
async def play(ctx, url):
   server = ctx.message.server
   voice_bot = bot.voice_bot_in(server)
   player = await voice_bot.create_ytdl_player(url)
   player[server.id] = player
   player.start()
    
bot.run(os.environ['BOT_TOKEN'])
