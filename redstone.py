import os
import discord
from bedrock_server import Server
from py_mcpe_stats import Query

TOKEN = os.getenv('DISCORD_TOKEN', 'token not provided')
SERVER_URL = os.getenv('SERVER_URL', 'sv11.minehost.com.ar')
SERVER_PORT = os.getenv('SERVER_PORT', 41666)

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
        try:
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
                await message.channel.send('Server is restarting... please wait.')
                self.pyrock_server.restart()
                await message.channel.send('Server is now up again!')

            if message.content == f'{PREFIX}server up?':
                if self.pyrock_server.is_running():
                    await message.channel.send('The server is currently up!')
                else:
                    await message.channel.send('The server is currently down!')

            if message.content == f'{PREFIX}server stats':
                q = Query(SERVER_URL, SERVER_PORT)
                server_data = q.query()
                server_data = server_data.__dict__
                await message.channel.send(
                    f'''```apache
                    Server stats:
                    -----
                    Name: {server_data['SERVER_NAME']}
                    Version: {server_data['GAME_VERSION']}
                    Gamemode: {server_data['GAMEMODE']}
                    Current Players: {server_data['NUM_PLAYERS']}
                    Max Players: {server_data['MAX_PLAYERS']}```'''
                )


        except BaseException as e:
            await message.channel.send(
                f'The last command failed with status: {repr(e)}'
            )

client = RedstoneServer()
client.run(TOKEN)