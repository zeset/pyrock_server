import os
import discord

TOKEN = os.getenv('DISCORD_TOKEN', 'token not provided')

PREFIX = '!'

class RedstoneServer(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.content == f'{PREFIX}ping':
            await message.channel.send('pong')

#client = RedstoneServer()
#client.run(TOKEN)