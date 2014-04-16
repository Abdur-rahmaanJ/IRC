__author__ = 'Jeroen'

import socket
import datetime


class IRCBot():
    BOT_NICKNAME = "jbBot"
    BOT_OWNER = "jpower13"

    def __init__(self, server, channel, port):
        self.BOT_IRC_SERVER = server
        self.BOT_IRC_CHANNEL = channel
        self.BOT_IRC_PORT = port

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
        messagetime = datetime.datetime.now().time().replace(microsecond=0)  # gets the time when the message was sent
        print(
            "[%s] %s: %s\n" % (messagetime, sender, message))  # prints all the messages "[time] sender:message" format.
        if message[0] == '!':  # checks if the message is a command
            messagecommand = message[1:].split()
            if sender == self.BOT_OWNER or sender == self.BOT_IRC_CHANNEL[1:]:
                if messagecommand[0].lower() == "author":
                    self.irc.sendmessage(self.BOT_IRC_CHANNEL, self.BOT_OWNER)
                elif messagecommand[0].lower() == "info":
                    self.irc.send(bytes('PRIVMSG ' + self.BOT_IRC_CHANNEL + ' :Server: %s Channel: %s Port: %s\r\n' %
                                        (self.BOT_IRC_SERVER, self.BOT_IRC_CHANNEL, self.BOT_IRC_PORT), 'utf-8'))
                elif messagecommand[0].lower() == "slap":
                    self.irc.send(bytes('PRIVMSG %s :%s slaps %s in the face with a big wet tuna fish, ouch!\r\n' %
                                        (self.BOT_IRC_CHANNEL, sender, messagecommand[1]), 'utf-8'))
                elif messagecommand[0].lower() == "gear" and len(messagecommand) > 1:
                    gearCheck = messagecommand[1].lower()
                    if gearCheck == "helm" or gearCheck == "head" or gearCheck == "mask":
                        self.sendmessage(self.BOT_IRC_CHANNEL, self.gear.get("head"))
                    elif gearCheck == "ring" or gearCheck == "rings" or gearCheck == "blingbling":
                        self.sendmessage(self.BOT_IRC_CHANNEL, self.gear.get("ring"))
                    elif gearCheck == "chest" or gearCheck == "torso":
                        self.sendmessage(self.BOT_IRC_CHANNEL, self.gear.get("chest"))
                    elif gearCheck == "neck":
                        self.sendmessage(self.BOT_IRC_CHANNEL, self.gear.get("neck"))
                    elif gearCheck == "pants":
                        self.sendmessage(self.BOT_IRC_CHANNEL, self.gear.get("pants"))
                    elif gearCheck == "feet" or gearCheck == "shoes":
                        self.sendmessage(self.BOT_IRC_CHANNEL, self.gear.get("feet"))
                    elif gearCheck == "gloves" or gearCheck == "hands":
                        self.sendmessage(self.BOT_IRC_CHANNEL, self.gear.get("gloves"))
                    elif gearCheck == "shoulder" or gearCheck == "shoulders":
                        self.sendmessage(self.BOT_IRC_CHANNEL, self.gear.get("shoulders"))
            """else:
                if messagecommand[0].lower() == "slap":
                    self.irc.send(bytes('PRIVMSG %s :%s slaps %s in the face with a big wet tuna fish, ouch!\r\n' %
                                        (self.BOT_IRC_CHANNEL, sender, messagecommand[1]), 'utf-8'))"""

    def sendmessage(self, rcv, msg):
        print(bytes('PRIVMSG %s :%s\r\n' % (rcv, msg), 'utf-8'))
        self.irc.send(bytes('PRIVMSG %s :%s\r\n' % (rcv, msg), 'utf-8'))

    def printinfo(self):
        print("Server: %s\r\nChannel: %s\r\nPort: %s\r\n" % (
            self.BOT_IRC_SERVER, self.BOT_IRC_CHANNEL, self.BOT_IRC_PORT))


class TwitchBot(IRCBot):
    BOT_PASSWORD = "password"  # changed for obvious reasons

    gear = {
        "head": "Head 1: Jade Harvester's Wisdom http://us.battle.net/d3/en/item/jade-harvesters-wisdom | "  # gearset for the diablo 3 streamer j_macc
                "Head 2: Quetzalcoatl http://eu.battle.net/d3/en/item/quetzalcoatl",
        "ring": "Ring 1: Stone of Jordan http://us.battle.net/d3/en/item/stone-of-jordan | "
                "Ring 2: Ring of Royal Grandeur http://us.battle.net/d3/en/item/ring-of-royal-grandeur-3qRFop",
        "neck": "Neck: Golden Gorget of Leoric http://us.battle.net/d3/en/item/golden-gorget-of-leoric-1I0CCL",
        "chest": "Chest: Helltooth Tunic http://us.battle.net/d3/en/item/helltooth-tunic",
        "pants": "Pants: Jade Harvester's Courage http://us.battle.net/d3/en/item/jade-harvesters-courage",
        "gloves": "Gloves: Jade Harvester's Mercy http://us.battle.net/d3/en/item/jade-harvesters-mercy",
        "feet": "Feet: Jade Harvester's Swiftness http://us.battle.net/d3/en/item/jade-harvesters-swiftness",
        "shoulders": "Shoulders: Jade Harvester's Joy http://us.battle.net/d3/en/item/jade-harvesters-joy"}

    def connect(self):
        self.irc = socket.socket()
        self.irc.connect((self.BOT_IRC_SERVER, self.BOT_IRC_PORT))
        self.irc.send(bytes('PASS ' + self.BOT_PASSWORD + '\r\n', 'utf-8'))
        self.irc.send(bytes('USER jbBot jbBot jbBot : jb IRC\r\n', 'utf-8'))
        self.irc.send(bytes('NICK ' + self.BOT_NICKNAME + '\r\n', 'utf-8'))
        self.irc.send(bytes('JOIN ' + self.BOT_IRC_CHANNEL + '\r\n', 'utf-8'))
        self.lineparser()


print("==============\nSTART PROGRAM\n")
#testBot = IRCBot("irc.geekshed.net", "#bottesting", 6667)
#testBot.connect()
twitchBot = TwitchBot("irc.twitch.tv", "#kingkongor", 6667)
twitchBot.connect()
print("END PROGRAM\n==============")