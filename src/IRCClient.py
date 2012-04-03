#!/usr/bin/env python

from asynchat import async_chat
from socket import AF_INET, SOCK_STREAM

class IRCClient(async_chat):

    chess4irc = None
    debug = 0
    terminator = '\r\n'

    def __init__(self, chess4irc, host, port, nickname, username, channels=None):
        async_chat.__init__(self)
	self.shutdown = 0
        self.chess4irc = chess4irc
        self.host = host
        self.port = port
        self.nickname = nickname
        self.username = username
        self.channels = [] if (channels is None) else channels
        self.received_data = ''
        self.print_debug('__init__: connecting to %(host)s:%(port)d' % {
	    'host': host,
	    'port': port
	})
        self.create_socket(AF_INET, SOCK_STREAM)
	self.connect((host, port))

    def _connection_made(self):
        self.print_debug('_connection_made: <nothing to do>')
	self.chess4irc.status = "Identified with Nickname: " + self.nickname
        for channel in self.channels:
            self.send_data('JOIN %(chan)s' % {'chan': channel})
        self.on_connection()

    def split_netmask(self, netmask):
        nick = netmask.split('!')[0].lstrip(':')
        user = netmask.split('@')[0].split('!')[1]
        host = netmask.split('@')[1]
        return (nick, user, host)

    def send_data(self, data):
        self.print_debug('send_data: %(data)s' % {'data': repr(data)})
        data += self.terminator
        self.push(data)

    def handle_connect(self):
	self.identify()

    def handle_close(self):
	self.close()

    def handle_expt():
	self.close()

    def handle_data(self, data):
        self.print_debug('handle_data: ' + str(data))
        token = data.split()

	if (token[0] == 'ERROR'):
	    self.chess4irc.quit()

	elif (token[0] == 'PING'):
	    self.on_ping(token[1])

	else:
	    src = token[0]
	    cmd = token[1]
	    dst = token[2]
	    #self.print_debug('len(token): ' + str(len(token)))
	    if (len(token) > 2):
		msg = ' '.join(token[3:]).lstrip(':')
	    else:
		msg = ''

	    if (cmd == '376'):
		self._connection_made()

	    # End of /NAMES list
	    elif (cmd == '366'):
		self.chess4irc.ready = 1

	    # Erroneous Nickname
	    elif (cmd == '432'):
		self.chess4irc.status = "Erroneous Nickname. Trying random one ..."
		self.chess4irc.status_changed = 1
		self.try_random_nick()

	    # Nickname is already in use
	    elif (token[1] == '433'):
		self.chess4irc.status = "Nickname in use. Trying random one ..."
		self.chess4irc.status_changed = 1
		self.try_random_nick()

	    elif (cmd == 'PRIVMSG'):
		self.on_privmsg(src, dst, msg)
    
	    elif (cmd == 'NOTICE'):
		self.on_notice(src, dst, msg)
    
	    elif (cmd == 'JOIN'):
		self.on_join(src, dst)
    
	    elif (cmd == 'PART'):
		self.on_part(src, dst, msg)
    
	    else:
		self.on_unknown_data(data)

    def found_terminator(self):
        self.handle_data(self.received_data)
        self.received_data = ''

    def collect_incoming_data(self, data):
        self.received_data += data

    ##########################
    ## IRC COMMANDS METHODS ##
    ##########################

    def set_nick(self):
        self.send_data('NICK %(nick)s' % {'nick': self.nickname})

    def set_user(self):
	self.send_data('USER %(nick)s %(nick)s %(nick)s :%(user)s' % {
            'nick': self.nickname,
            'user': self.username,
        })

    def privmsg(self, dst, msg, color=None):
        self.send_data('PRIVMSG %(dst)s :%(msg)s' % {
            'dst': dst,
            'msg': msg,
        })

    def notice(self, dst, msg):
        self.send_data('NOTICE %(dst)s :%(msg)s' % {
            'dst': dst,
            'msg': msg,
        })

    def identify(self):
	self.set_nick()
	self.set_user()

    def join(self, *dst):
        for channel in dst:
            self.send_data('JOIN %(dst)s' % {'dst': channel})

    def part(self, dst, msg=None):
        data = 'PART %(dst)s' % {'dst': dst}
        if msg is not None:
            data += ' :%(msg)s' % {'msg': msg}
        self.send_data(data)

    def quit(self, msg=None):
	if self.chess4irc.ready == 1:
	    data = 'QUIT'
	    if msg is not None:
		data += ' :%(msg)s' % {'msg': msg}
		self.send_data(data)
	self.close_when_done()

    def on_ping(self, ping_id):
        self.send_data('PONG %(id)s' % {'id': ping_id})

    #####################################################
    ## EVENTS HANDLERS TO (RE-)IMPLEMENT IN A SUBCLASS ##
    #####################################################

    def on_unknown_data(self, data):
        pass

    def on_connection(self):
	self.print_debug('on_connection: <nothing to do>')
        pass

    def on_action(self, src, dst, msg):
	self.print_debug('on_action: from=' + src + ' to=' + dst + ' msg=' + msg)
        pass

    def on_privmsg(self, src, dst, msg):
	(nick, user, host) = self.split_netmask(src)
	self.print_debug('on_privmsg: from=' + src + ' from_nick=' + nick + ' to=' + dst + ' msg=' + msg)
	if (nick == self.chess4irc.rplayer):
	    self.chess4irc.gui.remote_text_move = msg
        pass

    def on_notice(self, src, dst, msg):
	self.print_debug('on_notice: from=' + src + ' to=' + dst + ' msg=' + msg)
        pass

    def on_join(self, src, dst):
	self.print_debug('on_join: from=' + src + ' to=' + dst)
        pass

    def on_part(self, src, dst, msg):
	self.print_debug('on_part: from=' + src + ' to=' + dst + ' msg=' + msg)
        pass

    def on_quit(self, src, msg):
	self.print_debug('on_quit: from=' + src + ' msg=' + msg)
        pass

    ####################
    ## MISC FUNCTIONS ##
    ####################

    def try_random_nick(self):
	# max length should be 15 chars
	import random
	suffixes = ["player", "king", "hacker", "queen", "newbie", "alien", "freak"]
	self.nickname = "ch4irc_" + (random.choice(suffixes))
	self.username = self.nickname
	self.print_debug("trying random nick: " + self.nickname)
	self.identify()

    def print_debug(self, line = ""):
	if (self.debug == 1): print "[IRCClient] " + str(line)
