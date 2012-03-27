#!/usr/bin/env python

from asynchat import async_chat
from socket import AF_INET, SOCK_STREAM

class IRCClient(async_chat):

    debug = 0
    terminator = '\r\n'

    def __init__(self, host, port, nickname, username, channels=None):
        async_chat.__init__(self)
        self.host = host
        self.port = port
        self.nickname = nickname
        self.username = username
        self.channels = [] if (channels is None) else channels
        self.received_data = ''
        self.print_debug('__init__: connecting to %(host)s:%(port)d' % {'host': host, 'port': port})
        self.create_socket(AF_INET, SOCK_STREAM)
        self.connect((host, port))

    def _connection_made(self):
        self.print_debug('_connection_made: <nothing to do>')
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
        self.send_data('NICK :%(nick)s' % {'nick': self.nickname})
        self.send_data('USER %(nick)s %(nick)s %(nick)s :%(user)s' % {
            'nick': self.nickname,
            'user': self.username,
        })

    def handle_data(self, data):
        self.print_debug('handle_data: ' + str(data))
        token = data.split()

	if (token[0] == 'PING'):
	    self.on_ping(token[1])
	else:
	    src = token[0]
	    cmd = token[1]
	    dst = token[2]
	    self.print_debug('len(token): ' + str(len(token)))
	    if (len(token) > 2):
		msg = ' '.join(token[3:]).lstrip(':')
	    else:
		msg = ''

	    if (cmd == '376'):
		self._connection_made()

	    #elif (token[1] == '433'): # :server.domain 433 * botijo :Nickname is already in use.   
	    # TODO
	    
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

    def set_nick(self, new_nick):
        self.nickname = new_nick
        self.send_data('NICK %(nick)s' % {'nick': new_nick})

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

    def join(self, *dst):
        for channel in dst:
            self.send_data('JOIN %(dst)s' % {'dst': channel})

    def part(self, dst, msg=None):
        data = 'PART %(dst)s' % {'dst': dst}
        if msg is not None:
            data += ' :%(msg)s' % {'msg': msg}
        self.send_data(data)

    def quit(self, msg=None):
        data = 'QUIT'
        if msg is not None:
            data += ' :%(msg)s' % {'msg': msg}
        self.send_data(data)

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

    def print_debug(self, line = ""):
	if (self.debug == 1): print "[DEBUG] " + str(line)


##########
## MAIN ##
##########

if __name__ == '__main__':
    from asyncore import loop
    host, port = 'irc.freenode.org', 6667
    nick = username = 'irchess_bot'
    channels = ['#irchess']
    client = IRCClient(host, port, nick, username, channels)
    loop()
