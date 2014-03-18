__author__ = 'Jeroen'

import socket

BOT_IRC_SERVER = "irc.geekshed.net"
BOT_IRC_CHANNEL = "#bottesting"
BOT_IRC_PORT = 6667
BOT_NICKNAME = "xjBot"
BOT_OWNER = "xjeroen"
BOT_PASSWORD = "Password"


def pingChecker(pingLine):
    if pingLine.find(bytes('PING', 'utf-8')) != -1:
        pingLine = pingLine.rstrip().split()
        if pingLine[0] == bytes("PING", 'utf-8'):
            irc.send(bytes("PONG ", 'utf-8') + pingLine[1] + bytes("\r\n", 'utf-8'))


def messagechecker(msgLine):
    completeLine = str(msgLine[1:]).split(':', 1)
    info = completeLine[0].split()
    message = completeLine[1].split("\\r")[0]
    sender = info[0][2:].split("!", 1)[0]
    print("Complete Line-->" + str(completeLine))
    print("Info-->" + str(info))
    print("Message-->" + str(message))
    print("Sender-->" + str(sender) + "\n")

    if message.lower() == "hi":
        irc.send(bytes('PRIVMSG ' + BOT_IRC_CHANNEL + ' :Hi there, ' + str(sender) + '!\r\n', 'utf-8'))

    if message[0] == '!' and sender == BOT_OWNER:
        messageCommand = message[1:].split()
        if messageCommand[0] == "Author":
            irc.send(bytes('PRIVMSG ' + BOT_IRC_CHANNEL + ' :I was created by ' + BOT_OWNER + '\r\n', 'utf-8'))


def sendmessage(rcv, msg):
    print(bytes('PRIVMSG ' + rcv + ' :' + msg + '\r\n', 'utf-8'))
    irc.send(bytes('PRIVMSG ' + rcv + ' :' + msg + '\r\n', 'utf-8'))


irc = socket.socket()
irc.connect((BOT_IRC_SERVER, BOT_IRC_PORT))
irc.recv(4096)
irc.send(bytes('NICK ' + BOT_NICKNAME + '\r\n', 'utf-8'))
pingChecker(irc.recv(4096))
irc.send(bytes('USER xjBot xjBot xjBot : xj IRC\r\n', 'utf-8'))
pingChecker(irc.recv(4096))
irc.send(bytes('JOIN ' + BOT_IRC_CHANNEL + '\r\n', 'utf-8'))

while 1:
    line = irc.recv(4096)
    print(line)
    pingChecker(line)
    if line.find(bytes('PRIVMSG', 'utf-8')) != -1 or line.find(bytes('NOTICE', 'utf-8')) != -1:
        messagechecker(line)
