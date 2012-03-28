#/usr/bin/env python

from IRCClient import IRCClient
from ChessClient import ChessClient
from ChessBoard import ChessBoard
from asyncore import loop
import sys

class irchess:

    # self vars
    ready = 0
    lplayer, rplayer = None, None
    # self objects
    irc, gui = None, None

    def __init__(self, lplayer, rplayer, wb):
	self.lplayer = lplayer
	self.rplayer = rplayer
	host, port = 'irc.freenode.org', 6667
	nick = username = lplayer
	channels = ['#irchess']
	self.gui = ChessClient(self, wb)
	self.irc = IRCClient(self, host, port, nick, username, channels)
	# start threaded objects
	self.gui.start() # gui - sync thread
	loop()           # irc - async thread

    def close(self):
	self.irc.close()
	self.gui.close()

def printUsage():
    print "irchess 0.1 by Jose V Beneyto, <sepen@crux.nu>"
    print "Usage: irchess <local_player> <remote_player> <white|black>"
    sys.exit()

if __name__ == "__main__":
    print "len: " + str(len(sys.argv))
    if (len(sys.argv) < 4):
	printUsage()
    local_player = sys.argv[1]
    remote_player = sys.argv[2]
    white_or_black = sys.argv[3]
    ichess = irchess(local_player, remote_player, white_or_black)
