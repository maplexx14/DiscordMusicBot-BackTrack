import discord
import requests
from discord.ext import commands
import yt_dlp
import re
import asyncio
import os
import audioTools

token = ''
prefix = '!'
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
bot = commands.Bot(command_prefix = prefix, intents = intents)

bot.remove_command('help')
media = 'media/'

ytdlOps = {
    'format': 'mp3/bestaudio/best',
    'outtmpl': 'media/%(id)s.%(ext)s',
   
    'postprocessors': [{  
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
    }]
}
@bot.event
async def on_ready():
    print('Bot online')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name = 'Cyberpunk 2777'))


@bot.command(aliases=['p'])
async def play(ctx, *, link):
    print(ctx.message.author.name + "#" + ctx.message.author.discriminator + " played some music. " + str(link))

 
    voiceChannel = audioTools.getVoiceChannel(ctx, bot)
    print("Gonna try to play some music")
    print(bot.voice_clients)

    if audioTools.checkInvalidLink(link):
        await ctx.send(
            embed=discord.Embed(title="Ошибка", description="Введите YT ID(.\nПример: `!play dQw4w9WgXcQ`",
                                color=0x00BBFF))
        await ctx.send(file=discord.File('1.png'))
        return

    if voiceChannel == -1:
        await ctx.send(
            embed=discord.Embed(title="Ошибка", description="Присоедини бота к каналу. `!join`",
                                color=0x00BBFF))
        return

 
    if os.path.isfile(media + link + ".mp3"):
        try:
            await ctx.send(embed=discord.Embed(title='Сейчас играет', description=f'Поставил **{ctx.message.author.name}**',
                                               color=0x00BBFF))
            voiceChannel.play(discord.FFmpegPCMAudio(media + link + ".mp3"))
        except:
            await ctx.send(embed=discord.Embed(title="Ошибка", description="Присоединись к каналу для проигрывания музыки",
                                               color=0x00BBFF))
        return

    async with ctx.typing():
     
        with yt_dlp.YoutubeDL(ytdlOps) as ydl:
            error_code = ydl.download([link])
    await ctx.send(embed=discord.Embed(title='Сейчас играет', description=f'Поставил **{ctx.message.author.name}**', color=0x00BBFF))

    voiceChannel.play(discord.FFmpegPCMAudio(media + link + ".mp3"))



@bot.command()

async def pause(ctx):

    voiceChannel = audioTools.getVoiceChannel(ctx, bot)

    if voiceChannel == -1:
        await ctx.send(embed = discord.Embed(title = "Ошибка", description = "Ты не в войс чате", color = 0x00BBFF))
        return
    voiceChannel.pause()


@bot.command()
async def resume(ctx):

    voiceChannel = audioTools.getVoiceChannel(ctx, bot)

    if voiceChannel == -1:
        await ctx.send(embed = discord.Embed(title = "Ошибка", description = "Не в войсе", color = 0x880000))
        return
    voiceChannel.resume()



@bot.command()
async def skip(ctx):
 
    voiceChannel = audioTools.getVoiceChannel(ctx, bot)

    if voiceChannel == -1:
        await ctx.send(embed = discord.Embed(title = "Ошибка", description = "Не в войсе", color = 0x880000))
        return
    voiceChannel.stop()



@bot.command()
async def join(ctx):
    try:
        if not ctx.guild.voice_client in bot.voice_clients:
            channel = ctx.author.voice.channel
            await channel.connect()
        else:
            await ctx.channel.send('Я в войс чате')
    except IndexError:
        await ctx.channel.send('Ты не в войсе')


@bot.command()
async def dc(ctx):
    if ctx.guild.voice_client in bot.voice_clients:
        await ctx.send('До связи', tts = True)
        await ctx.voice_client.disconnect()
    else:
        await ctx.channel.send('Я не в войсе')



bot.run(token)
