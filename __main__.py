import discord
from discord.ext import tasks
import time
import random
import os
from dotenv import load_dotenv
import Economy
import SFXPlayer

# Load environment variables
load_dotenv()
botName = os.getenv('BOT_NAME')
botToken = os.getenv('MAIN_TOKEN')
voiceChannelId = int(os.getenv('VOICE_CHANNEL_ID'))
musicChannelId = int(os.getenv('MUSIC_CHANNEL_ID'))
currency = os.getenv('CURRENCY')
interval = os.getenv('INTERVAL')
coinsPerInterval = os.getenv('COINSPERINTERVAL')


class EconomyClient(discord.Client):
    def __init__(self, botName, voiceChannel, musicChannel, currency, coinsPerInterval,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.botName = botName
        self.SFXPlayer = SFXPlayer.SFXPlayer()
        self.Database = Economy.EconomyDatabase(coinsPerInterval)
        self.voiceChannel = voiceChannel
        self.musicChannel = musicChannel
        self.currency = currency
        self.my_background_task.start()

    async def on_ready(self):
        print('Logged in as:')
        print(self.user.name)
        print(self.user.id)
        print('Channel ID:')
        print(self.voiceChannel)
        print('------')

    async def on_message(self, message):

        fileToPlay = message.content.lower() + ".wav"
        voiceChannel = self.get_channel(self.voiceChannel)

        if message.author == client.user:
            return

        if message.content.startswith('+test'):
            await message.reply("I log in, therefore I am", mention_author=False)
            return

        if "sfx" in message.content.lower():
            await message.reply(self.SFXPlayer.listOfSFXString, mention_author=False)
            return

        elif fileToPlay in self.SFXPlayer.listOfSFX:
            await self.SFXPlayer.playAudio(
                voiceChannel, "sounds/sfx/" + fileToPlay)
            return

        # Economy Commands
        if message.content.startswith('show me the money'):
            await message.reply('You have: ' + str(self.Database.GetUserData(message.author.name)) + " " + self.currency, mention_author=False)
            return

        if message.content.startswith('show me all the money'):
            await message.reply('Here is the current money pool: ' + str(self.Database.GetAllUserData()), mention_author=False)
            return

        if message.content.startswith('play'):
            await self.Database.Transaction(message.author.name, {
                "value": 10}, message)
            return

    async def on_voice_state_update(self, member, before, after):
        voiceChannel = self.get_channel(self.voiceChannel)
        if (before.channel == None) and (after.channel == self.get_channel(int(self.voiceChannel))) and (member.name != self.botName):
            self.Database.AddUserData(member.name)
            await self.SFXPlayer.playAudio(
                voiceChannel, self.SFXPlayer.getRandomSound(member))

    @tasks.loop(seconds=int(interval))  # task runs every x seconds
    async def my_background_task(self):
        channel = self.get_channel(int(self.voiceChannel))
        self.Database.GiveUsersMoney(channel.members)

    @my_background_task.before_loop
    async def before_my_task(self):
        await self.wait_until_ready()  # wait until the bot logs in


client = EconomyClient(botName=botName, voiceChannel=voiceChannelId, musicChannel=musicChannelId,
                       currency=currency, coinsPerInterval=coinsPerInterval)

client.run(botToken)