#/usr/bin/env python

from IRCClient import IRCClient
from ChessClient import ChessClient
from ChessBoard import ChessBoard

class irchess:

	# global vars
	version = "0.1"
	irc, gui = None, None

	def __init__(self):
		# instance objects
		from asyncore import loop
		host, port = 'irc.freenode.org', 6667
		nick = username = 'irchess_bot'
		channels = ['#irchess']
		self.irc = IRCClient(host, port, nick, username, channels)
		self.gui = ChessClient()
		# start objects
		self.gui.start() # gui
		loop()           # irc


if __name__ == "__main__":
	ichess = irchess()
