#!/usr/bin/env python3

import asyncore
import sys
import _thread

from ChessClient import ChessClient
from IRCClient import IRCClient


class chess4irc:
    # self vars
    ready, status, statuschanged = None, None, None
    lplayer, rplayer = None, None
    # self objects
    irc, gui = None, None

    def __init__(self, lplayer, rplayer, wb):
        self.ready = 0
        self.status, self.status_changed = '', 1
        self.lplayer, self.rplayer = lplayer, rplayer
        host, port = 'irc.libera.chat', 6667
        #host, port = 'localhost', 6667
        nick = username = lplayer
        channels = ['#chess4irc']
        # initialize objects
        try:
            self.gui = ChessClient(self, wb)
        except (thread.error, KeyboardInterrupt, SystemExit):
            self.quit()
        try:
            self.irc = IRCClient(self, host, port, nick, username, channels)
        except (asyncore.ExitNow, KeyboardInterrupt, SystemExit):
            self.quit()
        # start threads
        try:
            self.gui.start()  # gui - sync thread
        except (thread.error, KeyboardInterrupt, SystemExit):
            self.quit()
        try:
            asyncore.loop()  # irc - async thread
        except (asyncore.ExitNow, KeyboardInterrupt, SystemExit):
            self.quit()

    def quit(self):
        self.irc.quit()
        self.gui.quit()
        sys.exit()


def printUsage():
    print("chess4irc v0.1")
    print("Usage: chess4irc <local_player> <remote_player> <white|black>")
    sys.exit()


if __name__ == "__main__":
    if (len(sys.argv) < 4):
        printUsage()
    local_player = sys.argv[1]
    remote_player = sys.argv[2]
    white_or_black = sys.argv[3]
    try:
        chess4irc(local_player, remote_player, white_or_black)
    except (asyncore.ExitNow, thread.error, KeyboardInterrupt, SystemExit):
        sys.exit()
