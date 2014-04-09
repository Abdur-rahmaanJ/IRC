__author__ = 'Jeroen'

import socket


class IRCBot():
    BOT_NICKNAME = "jbBot"
    BOT_OWNER = "xjeroen"

    def __init__(self, server, channel, port):
        self.BOT_IRC_SERVER = server
        self.BOT_IRC_CHANNEL = channel
        self.BOT_IRC_PORT = port

    def printInfo(self):
        print("Server: %s\nChannel: %s\nPort: %s\n" % (self.BOT_IRC_SERVER, self.BOT_IRC_CHANNEL, self.BOT_IRC_PORT))

    def connect(self):
        irc = socket.socket()
        irc.connect((self.BOT_IRC_SERVER, self.BOT_IRC_PORT))
        irc.recv(4096)
        irc.send(bytes('NICK ' + self.BOT_NICKNAME + '\r\n', 'utf-8'))
        irc.send(bytes('USER jbBot jbBot jbBot : jb IRC\r\n', 'utf-8'))
        irc.send(bytes('JOIN ' + self.BOT_IRC_CHANNEL + '\r\n', 'utf-8'))
        while 1:
            line = irc.recv(4096)
            print(line)


class TwitchBot(IRCBot):
    BOT_PASSWORD = "Password"

    def connect(self):
        irc = socket.socket()
        irc.connect((self.BOT_IRC_SERVER, self.BOT_IRC_PORT))
        irc.send(bytes('PASS ' + self.BOT_PASSWORD + '\r\n', 'utf-8'))
        irc.send(bytes('USER jbBot jbBot jbBot : jb IRC\r\n', 'utf-8'))
        irc.send(bytes('NICK ' + self.BOT_NICKNAME + '\r\n', 'utf-8'))
        irc.send(bytes('JOIN ' + self.BOT_IRC_CHANNEL + '\r\n', 'utf-8'))
        while 1:
            line = irc.recv(4096)
            print(line)



#testBot = IRCBot("irc.geekshed.net", "#bottesting", 6667)
#testBot.printInfo()
#testBot.connect()

twitchBot = TwitchBot("irc.twitch.tv", "#jpower13", 6667)
twitchBot.connect()