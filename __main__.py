import discord
import time
import random
import os
from dotenv import load_dotenv

load_dotenv()
botToken = os.getenv('MAIN_TOKEN')
voiceChannelId = int(os.getenv('VOICE_CHANNEL_ID'))
musicChannelId = int(os.getenv('MUSIC_CHANNEL_ID'))

client = discord.Client()

userSounds = []
listOfSFX = []
listOfSFXString = ""

for root, dirs, files in os.walk("sounds/sfx"):
    for file in files:
        listOfSFX.append(file)

for sfx in listOfSFX:
    fileName = os.path.splitext(sfx)
    listOfSFXString = listOfSFXString + fileName[0]
    listOfSFXString = (listOfSFXString + '\n')


def getRandomSound(user):

    for root, dirs, files in os.walk("sounds/" + user):
        for file in files:
            userSounds.append(file)
    
    sound = userSounds[random.randint(0, len(userSounds) - 1)]

    return ("sounds/" + user + "/" + sound)


@client.event
async def on_voice_state_update(member, before, after):

    voiceChannel = client.get_channel(voiceChannelId)
    musicChannel = client.get_channel(musicChannelId)

    if (before.channel == None) and (after.channel == voiceChannel) and (member.name != "Announcer?"):

        print(member.name + " joined")

        vc = await voiceChannel.connect()
        vc.play(discord.FFmpegPCMAudio(executable="ffmpeg/bin/ffmpeg.exe", source=getRandomSound(member.name)))
        while vc.is_playing():
            time.sleep(.1)
        await vc.disconnect()

        return

    # elif (before.channel == voiceChannel) and (after.channel == None) and (member.name != "Announcer?"):

    #     print(member.name + " left")


@client.event
async def on_message(message):

    voiceChannel = client.get_channel(voiceChannelId)
    musicChannel = client.get_channel(musicChannelId)

    if message.author == client.user:
        return

    if message.content.startswith('+test'):
        await musicChannel.send("I log in, therefore I am")
        return

    if not message.guild:

        fileToPlay = message.content.lower() + ".wav"

        if "print" in message.content.lower():
            if (len(client.voice_clients) > 0):
                print("Connected")
            else:
                print("Not Connected")
            return

        elif "sfx" in message.content.lower():
            await message.channel.send(listOfSFXString)
            return

        elif fileToPlay in listOfSFX:

            vc = await voiceChannel.connect()
            vc.play(discord.FFmpegPCMAudio(executable="ffmpeg/bin/ffmpeg.exe", source="sounds/sfx/" + fileToPlay))
            while vc.is_playing():
                time.sleep(.1)
            await vc.disconnect()
            return            


client.run(botToken)