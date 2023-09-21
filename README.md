# Chess for IRC

`chess4irc` is a chess board game written in PyGame which uses IRC protocol to send/receive data.

The application consists of a basic chess board, where each piece movement of the game is sent to the opponent through the IRC protocol.

The [asynchat](https://docs.python.org/3/library/asynchat.html) module is used to implement the IRC client and the graphical part is written with [PyGame](https://www.pygame.org/) as a programming exercise, so use at your own risk.


## Usage
```
$ chess4irc <local_player> <remote_player> <white|black>
```

## Examples

Player 1 (joe)
```
$ chess4irc.py joe bob white
```

Player 2 (bob)
```
$ chess4irc.py bob joe black
```

## Run chess4irc from Docker image

Build the image
```
$ docker build -t chess4irc .
```

Disable X server access control, clients can connect from any host
```
$ xhost +
```

Run with some additional arguments to use your X server. Sound is a requirement in PyGame even though chess4irc does not have sound
```
$ docker run -it --rm \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    -v $PWD:/home \
    -e DISPLAY=unix$DISPLAY \
    --device /dev/snd \
    chess4irc joe bob white
```

## Chess Notation Cheat Sheet

`king = K`\
`queen = Q`\
`rook = R`\
`knight = N`\
`bishop = B`

castles kingside = O-O\
castles queenside = O-O-O\

takes = x\
check = +\
checkmate = #

Some examples:
* `Bxf3` bishop takes f3
* `Qe7+` queen to e7 check
* `Rb8#` rook b8 mate
* `exf6` e takes f6 (the e-pawn is capturing the pawn or piece on f6)
* `d8=Q` (the d-pawn reached the 8th rank and turned into a queen)
* `Nbd2` (both knights could go to d2, but the knight that was on the b-file was the one that went to d2)
* `R8c2` (both rooks were on the c-file, but the rook that was on the 8th rank was the on that went to c2).