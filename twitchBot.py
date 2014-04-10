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

    def messagechecker(self,msgLine):
        completeLine = str(msgLine[1:]).split(':', 1)
        info = completeLine[0].split()
        message = completeLine[1].split("\\r")[0]
        sender = info[0][2:].split("!", 1)[0]
        #print("Complete Line-->" + str(completeLine))
        #print("Info-->" + str(info))
        print("\nMessage-->" + str(message))
        print("Sender-->" + str(sender) + "\n")

    def lineParser(self, chat):
        while 1:
            line = chat.recv(4096)
            #print(line)
            if line.find(bytes('PRIVMSG', 'utf-8')) != -1 or line.find(bytes('NOTICE', 'utf-8')) != -1:
                self.messagechecker(line)


class TwitchBot(IRCBot):
    BOT_PASSWORD = "password"

    def connect(self):
        irc = socket.socket()
        irc.connect((self.BOT_IRC_SERVER, self.BOT_IRC_PORT))
        irc.send(bytes('PASS ' + self.BOT_PASSWORD + '\r\n', 'utf-8'))
        irc.send(bytes('USER jbBot jbBot jbBot : jb IRC\r\n', 'utf-8'))
        irc.send(bytes('NICK ' + self.BOT_NICKNAME + '\r\n', 'utf-8'))
        irc.send(bytes('JOIN ' + self.BOT_IRC_CHANNEL + '\r\n', 'utf-8'))
        self.lineParser(irc)


#testBot = IRCBot("irc.geekshed.net", "#bottesting", 6667)
#testBot.printInfo()
#testBot.connect()

twitchBot = TwitchBot("irc.twitch.tv", "#kungentv", 6667)
twitchBot.connect()