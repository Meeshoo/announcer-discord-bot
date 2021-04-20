import os
import random
import time
import discord

class SFXPlayer():

    def __init__(self):
        self.memberSounds = []

        self.listOfSFX = []

        for root, dirs, files in os.walk("./sounds/sfx"):
            for file in files:
                self.listOfSFX.append(file)

    def getRandomSound(self, member):

        filePath = os.listdir("./sounds/" + member.name + "/")
        for file in filePath:
            self.memberSounds.append(file)
        
        sound = self.memberSounds[random.randint(
            0, len(self.memberSounds) - 1)]

        return ("sounds/" + member.name + "/" + sound)

    async def playAudio(self, voiceChannel, path):

        voiceChannel = voiceChannel

        vc = await voiceChannel.connect()
        vc.play(discord.FFmpegPCMAudio(
            executable="/usr/bin/ffmpeg", source=path))
        while vc.is_playing():
            time.sleep(.1)
        time.sleep(0.2)
        await vc.disconnect()

        return
