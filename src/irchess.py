#/usr/bin/env python

from IRCClient import IRCClient
from ChessClient import ChessClient
from ChessBoard import ChessBoard
from asyncore import loop

class irchess:

	# self vars
	version = "0.1"
	# self objects
	irc, gui = None, None

	def __init__(self):
	    host, port = 'irc.freenode.org', 6667
	    nick = username = 'irchess_bot'
	    channels = ['#irchess']
	    self.gui = ChessClient(self)
	    self.irc = IRCClient(self, host, port, nick, username, channels)
	    # start threaded objects
	    self.gui.start() # gui - sync thread
	    loop()           # irc - async thread

	def close(self):
	    self.irc.close()
	    self.gui.close()


if __name__ == "__main__":
	ichess = irchess()
