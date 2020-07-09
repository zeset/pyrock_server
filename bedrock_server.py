import sys
import time
import pexpect
import threading

PATH_TO_SOFTWARE = 'bedrock_server'

LINEBREAK = r'.+'

ARENA_COORDINATES = {
    'x': -18,
    'y': 68,
    'z': 239
}

ARENA_OUTSIDE_COORDINATES = {
    'x': -2,
    'y': 68,
    'z': 239
}

class Server():
    running = False
    process = None

    def run(self):
        process = pexpect.spawn(f"./{PATH_TO_SOFTWARE}", encoding='utf-8')
        try:
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

    def stop(self):
        try:
            self.process.kill(0)
        except AttributeError:
            pass

    def arena_countdown(self):
        for seconds in range(1,self.prep_time)[::-1]:
            self.process.sendline('title @a title Seconds Remaining')
            self.process.sendline('title @a subtitle till Arena begins')
            self.process.sendline(f'title @a actionbar {seconds}')
            time.sleep(1)

    def arena_preparation(self):
        arena_x, arena_y, arena_z = **ARENA_COORDINATES
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
        outside_x = ARENA_OUTSIDE_COORDINATES['x']
        outside_y = ARENA_OUTSIDE_COORDINATES['y']
        outside_z = ARENA_OUTSIDE_COORDINATES['z']
        self.process.sendline('gamerule keepinventory false')
        self.process.sendline('gamerule pvp false')
        self.process.sendline('clear @a')
        self.process.sendline(f'tp @a {outside_x} {outside_y} {outside_z}')

    def arena(self, prep_time=60, duration=300, ):
        self.prep_time = prep_time
        self.duration = duration
        self.arena_countdown()
        self.arena_preparation()
        time.sleep(self.duration)
        self.return_to_normal()

server = Server()
server.run()
if server.is_running():
    print('Pyrock is successfully running!')
