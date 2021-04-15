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
        for root, dirs, files in os.walk("./sounds/" + member.name):
            for file in files:
                self.memberSounds.append(file)

        sound = self.memberSounds[random.randint(
            0, len(self.memberSounds) - 1)]

        return ("sounds/" + member.name + "/" + sound)

    async def playAudio(self, voiceChannel, path):
        voiceChannel = voiceChannel

        vc = await voiceChannel.connect()
        vc.play(discord.FFmpegPCMAudio(
            executable="ffmpeg/bin/ffmpeg.exe", source=path))
        while vc.is_playing():
            time.sleep(.1)
        await vc.disconnect()

        return
