import sys
import time
import pexpect
import threading
from redstone import RedstoneServer, TOKEN

PATH_TO_SOFTWARE = 'bedrock_server'

LINEBREAK = r'.+'

ARENA_COORDINATES = (-18, 68, 239)

ARENA_OUTSIDE_COORDINATES = (-2, 68, 239)


class Server():
    running = False
    process = None
    bot = None

    def run(self):
        process = pexpect.spawn(f"./{PATH_TO_SOFTWARE}", encoding='utf-8')
        try:
            if not self.bot:
                try:
                    self.bot = RedstoneServer()
                    self.bot.run(TOKEN)
                    print('Redstone started.')
                except BaseException:
                    print('Redstone not started.')

            process.expect('Server started.', timeout=120)
            print(process.before)
            self.running = True
            self.process = process
        except:
            self.running = False

    def is_running(self):
        return self.running

    def command(self, command, wait_for=None):
        output = None
        self.process.sendline(f'{command}')
        if wait_for:
            self.process.expect(wait_for)
            output = self.process.before
        if self.process.before:
            self.process.expect(LINEBREAK)
        if output:
            return str(output).strip()

    def restart(self):
        try:
            self.process.kill(0)
            self.running = False
            self.run()
        except AttributeError:
            pass

    def stop(self):
        try:
            self.process.kill(0)
        except AttributeError:
            pass

    def arena_countdown(self):
        for seconds in range(1,self.prep_time)[::-1]:
            self.process.sendline('title @a title Seconds Remaining')
            self.process.sendline('title @a subtitle till Arena begins')
            self.process.sendline(f'title @a actionbar {seconds} GUARDA TUS ITEMS!')
            time.sleep(1)

    def arena_preparation(self):
        arena_x, arena_y, arena_z = ARENA_COORDINATES
        self.process.sendline('clear @a')
        self.process.sendline('give @a diamond_sword 1')
        self.process.sendline('give @a leather_helmet 1')
        self.process.sendline('give @a leather_chestplate 1')
        self.process.sendline('give @a leather_leggings 1')
        self.process.sendline('give @a leather_boots 1')
        self.process.sendline('gamerule keepinventory true')
        self.process.sendline('gamerule pvp true')
        self.process.sendline(f'tp @a {arena_x} {arena_y} {arena_z}')

    def return_to_normal(self):
        outside_x, outside_y, outside_z = ARENA_OUTSIDE_COORDINATES
        self.process.sendline('gamerule keepinventory false')
        self.process.sendline('gamerule pvp false')
        self.process.sendline('clear @a')
        self.process.sendline(f'tp @a {outside_x} {outside_y} {outside_z}')

    def arena(self, prep_time=60, duration=120):
        self.prep_time = prep_time
        self.duration = duration
        self.arena_countdown()
        self.arena_preparation()
        time.sleep(self.duration)
        self.return_to_normal()

    def set_time_as_day(self):
        self.process.sendline('time set day')

    def set_time_as_night(self):
        self.process.sendline('time set night')

    def set_weather_as_clear(self):
        self.process.sendline('weather clear')

    def set_weather_as_rain(self):
        self.process.sendline('weather rain')

    def clear_mobs(self):
        self.process.sendline('difficulty 0')
        self.process.sendline('difficulty 2')


