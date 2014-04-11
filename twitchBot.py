__author__ = 'Jeroen'

import socket


class IRCBot():
    BOT_NICKNAME = "jbBot"
    BOT_OWNER = "jpower13"

    def __init__(self, server, channel, port):
        self.BOT_IRC_SERVER = server
        self.BOT_IRC_CHANNEL = channel
        self.BOT_IRC_PORT = port
        self.irc = socket.socket()

    def connect(self):  # Connecting to the given IRC, afterwards it starts the lineParser.
        self.irc = socket.socket()
        self.irc.connect((self.BOT_IRC_SERVER, self.BOT_IRC_PORT))
        self.irc.recv(4096)
        self.irc.send(bytes('NICK ' + self.BOT_NICKNAME + '\r\n', 'utf-8'))
        self.pingchecker(self.irc.recv(4096))  # Ping will sometimes be sent before motd, after joining
        self.irc.send(bytes('USER jbBot jbBot jbBot : jb IRC\r\n', 'utf-8'))
        self.pingchecker(self.irc.recv(4096))  # Sometimes after NICK, sometimes after USER.
        self.irc.send(bytes('JOIN ' + self.BOT_IRC_CHANNEL + '\r\n', 'utf-8'))
        self.lineparser()

    def pingchecker(self, pingline):
        if pingline.find(bytes('PING', 'utf-8')) != -1:
            pingline = pingline.rstrip().split()
            if pingline[0] == bytes("PING", 'utf-8'):
                self.irc.send(bytes("PONG ", 'utf-8') + pingline[1] + bytes("\r\n", 'utf-8'))

    def lineparser(self):
        while 1:
            line = self.irc.recv(4096)
            self.pingchecker(line)
            if line.find(bytes('PRIVMSG', 'utf-8')) != -1 or line.find(bytes('NOTICE', 'utf-8')) != -1:
                self.messagechecker(line)

    def messagechecker(self, msgline):
        completeline = str(msgline[1:]).split(':', 1)
        info = completeline[0].split()
        message = completeline[1].split("\\r")[0]
        sender = info[0][2:].split("!", 1)[0]
        #print("Complete Line-->" + str(completeLine))
        #print("Info-->" + str(info))
        #print("\nMessage-->" + str(message))
        #print("Sender-->" + str(sender) + "\n")
        print("%s: %s\n" % (sender, message))
        if message[0] == '!' and sender == self.BOT_OWNER:
            messagecommand = message[1:].split()
            if messagecommand[0].lower() == "author":
                self.irc.send(
                    bytes('PRIVMSG %s :I was created by %s\r\n' % (self.BOT_IRC_CHANNEL, self.BOT_OWNER), 'utf-8'))
            elif messagecommand[0].lower() == "info":
                self.irc.send(bytes(
                    'PRIVMSG ' + self.BOT_IRC_CHANNEL + ' :Server: %s Channel: %s Port: %s\r\n' %
                    (self.BOT_IRC_SERVER, self.BOT_IRC_CHANNEL, self.BOT_IRC_PORT), 'utf-8'))
        elif message[0] == '!':
            messagecommand = message[1:].split()
            if messagecommand[0].lower() == "slap":
                self.irc.send(bytes('PRIVMSG %s :%s slaps %s in the face with a big wet tuna fish, ouch!\r\n' %
                                    (self.BOT_IRC_CHANNEL, sender, messagecommand[1]), 'utf-8'))

    def sendmessage(self, rcv, msg):
        print(bytes('PRIVMSG %s :%s\r\n' % (rcv, msg), 'utf-8'))
        self.irc.send(bytes('PRIVMSG %s :%s\r\n' % (rcv, msg), 'utf-8'))

    def printinfo(self):
        print("Server: %s\r\nChannel: %s\r\nPort: %s\r\n" % (
            self.BOT_IRC_SERVER, self.BOT_IRC_CHANNEL, self.BOT_IRC_PORT))


class TwitchBot(IRCBot):
    BOT_PASSWORD = "password"

    def connect(self):
        self.irc.connect((self.BOT_IRC_SERVER, self.BOT_IRC_PORT))
        self.irc.send(bytes('PASS ' + self.BOT_PASSWORD + '\r\n', 'utf-8'))
        self.irc.send(bytes('USER jbBot jbBot jbBot : jb IRC\r\n', 'utf-8'))
        self.irc.send(bytes('NICK ' + self.BOT_NICKNAME + '\r\n', 'utf-8'))
        self.irc.send(bytes('JOIN ' + self.BOT_IRC_CHANNEL + '\r\n', 'utf-8'))
        self.lineparser()


print("==============\nSTART PROGRAM\n")
#testBot = IRCBot("irc.geekshed.net", "#bottesting", 6667)
#testBot.connect()

twitchBot = TwitchBot("irc.twitch.tv", "#jpower13", 6667)
twitchBot.connect()
twitchBot.printinfo()
print("END PROGRAM\n==============")