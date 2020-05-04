# chess4irc

Chess for IRC

Networking chess game written in PyGame which uses IRC protocol to send/receive data.
This is a PyGame programming exercise. It is not intended to use this for any purpose.

## Requirements

PyGame (http://www.pygame.org)


# Installation

Build and install
```
$ make
$ sudo make install
```

The command above will place the binary in _/usr/bin_. \
Alternatively you can also install it as a user in another path (i.e: _$HOME/.local/bin_)
```
$ make install DESTDIR=$HOME/.local/bin
```

## Usage
```
chess4irc <local_player> <remote_player> <white|black>
```

## Examples

Player 1:
```
$ python chess4irc.py c4i_player1 c4i_player2 white
```

Player 2:
```
$ python chess4irc.py c4i_player2 c4i_player1 black
```