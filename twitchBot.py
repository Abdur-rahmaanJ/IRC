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

    def connect(self):      # Connecting to the given IRC, afterwards it starts the lineParser.
        self.irc = socket.socket()
        self.irc.connect((self.BOT_IRC_SERVER, self.BOT_IRC_PORT))
        self.irc.recv(4096)
        self.irc.send(bytes('NICK ' + self.BOT_NICKNAME + '\r\n', 'utf-8'))
        self.pingChecker(self.irc.recv(4096))       # Ping will sometimes be sent before motd, after joining
        self.irc.send(bytes('USER jbBot jbBot jbBot : jb IRC\r\n', 'utf-8'))
        self.pingChecker(self.irc.recv(4096))       # Sometimes after NICK, sometimes after USER.
        self.irc.send(bytes('JOIN ' + self.BOT_IRC_CHANNEL + '\r\n', 'utf-8'))
        self.lineParser()


    def lineParser(self):
        while 1:
            line = self.irc.recv(4096)
            self.pingChecker(line)
            if line.find(bytes('PRIVMSG', 'utf-8')) != -1 or line.find(bytes('NOTICE', 'utf-8')) != -1:
                self.messagechecker(line)

    def messagechecker(self, msgLine):
        completeLine = str(msgLine[1:]).split(':', 1)
        info = completeLine[0].split()
        message = completeLine[1].split("\\r")[0]
        sender = info[0][2:].split("!", 1)[0]
        #print("Complete Line-->" + str(completeLine))
        #print("Info-->" + str(info))
        print("\nMessage-->" + str(message))
        print("Sender-->" + str(sender) + "\n")

    def pingChecker(self, pingLine):
        if pingLine.find(bytes('PING', 'utf-8')) != -1:
            pingLine = pingLine.rstrip().split()
            if pingLine[0] == bytes("PING", 'utf-8'):
                self.irc.send(bytes("PONG ", 'utf-8') + pingLine[1] + bytes("\r\n", 'utf-8'))

class TwitchBot(IRCBot):
    BOT_PASSWORD = "password"

    def connect(self):
        self.irc = socket.socket()
        self.irc.connect((self.BOT_IRC_SERVER, self.BOT_IRC_PORT))
        self.irc.send(bytes('PASS ' + self.BOT_PASSWORD + '\r\n', 'utf-8'))
        self.irc.send(bytes('USER jbBot jbBot jbBot : jb IRC\r\n', 'utf-8'))
        self.irc.send(bytes('NICK ' + self.BOT_NICKNAME + '\r\n', 'utf-8'))
        self.irc.send(bytes('JOIN ' + self.BOT_IRC_CHANNEL + '\r\n', 'utf-8'))
        self.lineParser()


#testBot = IRCBot("irc.geekshed.net", "#bottesting", 6667)
#testBot.connect()

twitchBot = TwitchBot("irc.twitch.tv", "#j_macc", 6667)
twitchBot.connect()