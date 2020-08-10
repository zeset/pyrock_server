import os
import discord
from bedrock_server import Server

TOKEN = os.getenv('DISCORD_TOKEN', 'token not provided')

PREFIX = '!'

class RedstoneServer(discord.Client):

	def __init__(self):
		self.pyrock_server = Server()
		self.pyrock_server.run()
		if self.pyrock_server.is_running():
		    print('Pyrock is successfully running!')

		super().__init__()

    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.content == f'{PREFIX}time day':
        	self.pyrock_server.set_time_as_day()
        	await message.channel.send('Time set as Day!')

        if message.content == f'{PREFIX}time night':
        	self.pyrock_server.set_time_as_night()
        	await message.channel.send('Time set as Night!')

		if message.content == f'{PREFIX}weather clear':
        	self.pyrock_server.set_weather_as_clear()
        	await message.channel.send('Weather set as Day!')

		if message.content == f'{PREFIX}weather rain':
        	self.pyrock_server.set_weather_as_rain()
        	await message.channel.send('Weather set as Rain!')

        if message.content == f'{PREFIX}mobs clear':
        	self.pyrock_server.clear_mobs()
        	await message.channel.send('Mobs got cleared!')

        if message.content == f'{PREFIX}server restart':
        	self.pyrock_server.restart()
        	await message.channel.send('Server restarted!')

        if message.content == f'{PREFIX}server up?':
        	if self.pyrock_server.is_running():
        		await message.channel.send('The server is currently up!')
        	else:
        		await message.channel.send('The server is currently down!')


client = RedstoneServer()
client.run(TOKEN)
