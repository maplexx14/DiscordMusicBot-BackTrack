import re  # regex


def preJoinCheck(ctx):
    if str(ctx.message.author.voice) == "None":
     
        return 0
 
    return ctx.message.author.voice.channel


def getVoiceChannel(ctx, bot):
    if bot.voice_clients == []:
        return -1
  
    voiceChannel = bot.voice_clients[0]
 
    for connections in bot.voice_clients:
        if connections.guild == ctx.guild:
            voiceChannel = connections
            return voiceChannel
    return -1


def checkInvalidLink(link):
    
    a = link.find(" ")
    if a != -1:
        link = link[:a]
       
  
    if not re.search("^[a-zA-Z0-9_-]{11}$", link):  
        return True

    return False
