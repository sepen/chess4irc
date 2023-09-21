#!/usr/bin/env python

import asynchat
import asyncore
import socket

class IRCClient(asynchat.async_chat):
    chess4irc = None
    debug = 0
    terminator = '\r\n'

    def __init__(self, chess4irc, host, port, nickname, username, channels=None):

        asynchat.async_chat.__init__(self)
        self.chess4irc = chess4irc

        # Set the terminating condition to be recognized
        self.set_terminator(b"\r\n")

        # Set input and output data buffers
        self.ibuffer = []
        self.obuffer = b""

        # Set IRC specific
        self.host = host
        self.port = port
        self.nickname = nickname
        self.username = username
        self.channels = [] if (channels is None) else channels

        # Create socket connection
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.print_debug('init(): connecting to %(host)s:%(port)d' % {
            'host': host,
            'port': port
        })
        self.connect((host, port))

    def collect_incoming_data(self, data):
        self.print_debug('collect_incoming_data(): (%(bytes)d bytes)' % {'bytes': len(data)})
        self.print_debug('collect_incoming_data(): """%(data)s"""' % { 'data': data.decode()})
        self.ibuffer.append(data)

    def found_terminator(self):
        self.print_debug('found_terminator()')
        self.handle_data(b"".join(self.ibuffer))
        self.ibuffer = []

    def handle_connect(self):
        self.print_debug('handle connect()')
        self.set_nick()
        self.set_user()

    def _connection_made(self):
        self.print_debug('_connection_made()')
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
        self.print_debug('send_data(): %(data)s' % {'data': repr(data)})
        data += "\r\n"
        self.push(data.encode())

    def handle_close(self):
        self.close()

    def handle_expt():
        self.close()

    def handle_data(self, data):
        self.print_debug('handle_data(): %(data)s' % {'data': data.decode()})
        token = data.split()
        print(type(token))
        self.print_debug('len(token): %(len)s' % {'len': str(len(token))})

        if (token[0].decode() == 'ERROR'):
            self.chess4irc.quit()

        elif (token[0].decode() == 'PING'):
            self.on_ping(token[1].decode())

        else:
            src = token[0].decode()
            cmd = token[1].decode()
            dst = token[2].decode()

            self.print_debug('handle_data(): src = %(src)s | cmd = %(cmd)s | dst = %(dst)s' % {
                'src': src,
                'cmd': cmd,
                'dst': dst,
            })
            self.print_debug('handle_data(): len(token) = %(len)s' % {'len': str(len(token))})
            if (len(token) > 2):
                msg = ' '.join(str(token[3:])).lstrip(':')
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
                msg = token[3].decode()
                self.on_privmsg(src, dst, msg)

            elif (cmd == 'NOTICE'):
                self.on_notice(src, dst, msg)

            elif (cmd == 'JOIN'):
                self.on_join(src, dst)

            elif (cmd == 'PART'):
                self.on_part(src, dst, msg)

            else:
                self.on_unknown_data(data)

    ##########################
    ## IRC COMMANDS METHODS ##
    ##########################

    def set_nick(self):
        self.send_data('NICK %(nick)s' % {
            'nick': self.nickname
        })

    def set_user(self):
        self.send_data('USER %(nick)s %(host)s * :%(user)s' % {
            'nick': self.nickname,
            'host': self.host,
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
        self.print_debug('on_unknown_data(): %(data)s' % {
            'data': data,
        })
        pass

    def on_connection(self):
        self.print_debug('on_connection()')
        pass

    def on_action(self, src, dst, msg):
        self.print_debug('on_action(): from = %(src)s | dst = %(dst)s | msg = %(msg)s' % {
            'src': src,
            'dst': dst,
            'msg': msg,
        })
        pass

    def on_privmsg(self, src, dst, msg):
        self.print_debug('on_privmsg(): from = %(src)s | dst = %(dst)s | msg = %(msg)s' % {
            'src': src,
            'dst': dst,
            'msg': msg,
        })
        (nick, user, host) = self.split_netmask(src)
        self.print_debug('on_privmsg(): nick = %(nick)s' % {'nick': nick})
        if (nick == self.chess4irc.rplayer):
            self.print_debug('on_privmsg(): msg = %(msg)s' % {'msg': msg})
            self.chess4irc.gui.remote_text_move = msg
            print(type(self.chess4irc.gui.remote_text_move))
        pass

    def on_notice(self, src, dst, msg):
        self.print_debug('on_notice(): from = %(src)s | dst = %(dst)s | msg = %(msg)s' % {
            'src': src,
            'dst': dst,
            'msg': msg,
        })
        pass

    def on_join(self, src, dst):
        self.print_debug('on_join(): from = %(src)s | dst = %(dst)s' % {
            'src': src,
            'dst': dst,
        })
        pass

    def on_part(self, src, dst, msg):
        self.print_debug('on_part(): from = %(src)s | dst = %(dst)s | msg = %(msg)s' % {
            'src': src,
            'dst': dst,
            'msg': msg,
        })
        pass

    def on_quit(self, src, msg):
        self.print_debug('on_part(): from = %(src)s | msg = %(msg)s' % {
            'src': src,
            'msg': msg,
        })
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
        self.set_nick()
        self.set_user()

    def print_debug(self, line=""):
        if (self.debug == 1): print("[IRCClient] " + str(line))
