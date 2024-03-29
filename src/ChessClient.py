#!/usr/bin/env python3

import pygame
import time
from threading import Thread

from ChessBoard import ChessBoard
from pygame.locals import *


class ChessClient(Thread):
    chess4irc = None
    debug = 0
    selected_turn = 0  # 0=white, 1=black
    remote_text_move = ""
    exitnow = 0

    def __init__(self, chess4irc, wb):
        self.chess4irc = chess4irc
        if (wb == "white"):
            self.selected_turn = 0
        else:
            self.selected_turn = 1
        Thread.__init__(self)

    def quit(self):
        pygame.quit()
        self._Thread__stop()

    def run(self):
        pygame.init()

        pieces = {}
        chess = ChessBoard()
        board = chess.getBoard()
        turn = chess.getTurn()

        screen = pygame.display.set_mode((480, 480), 1)
        pygame.display.set_caption('Chess for IRC')

        # load all images
        pieces = [{}, {}]
        pieces[0]["r"] = pygame.image.load("./img/brw.png")
        pieces[0]["n"] = pygame.image.load("./img/bnw.png")
        pieces[0]["b"] = pygame.image.load("./img/bbw.png")
        pieces[0]["k"] = pygame.image.load("./img/bkw.png")
        pieces[0]["q"] = pygame.image.load("./img/bqw.png")
        pieces[0]["p"] = pygame.image.load("./img/bpw.png")
        pieces[0]["R"] = pygame.image.load("./img/wrw.png")
        pieces[0]["N"] = pygame.image.load("./img/wnw.png")
        pieces[0]["B"] = pygame.image.load("./img/wbw.png")
        pieces[0]["K"] = pygame.image.load("./img/wkw.png")
        pieces[0]["Q"] = pygame.image.load("./img/wqw.png")
        pieces[0]["P"] = pygame.image.load("./img/wpw.png")
        pieces[0]["."] = pygame.image.load("./img/w.png")
        pieces[1]["r"] = pygame.image.load("./img/brb.png")
        pieces[1]["n"] = pygame.image.load("./img/bnb.png")
        pieces[1]["b"] = pygame.image.load("./img/bbb.png")
        pieces[1]["k"] = pygame.image.load("./img/bkb.png")
        pieces[1]["q"] = pygame.image.load("./img/bqb.png")
        pieces[1]["p"] = pygame.image.load("./img/bpb.png")
        pieces[1]["R"] = pygame.image.load("./img/wrb.png")
        pieces[1]["N"] = pygame.image.load("./img/wnb.png")
        pieces[1]["B"] = pygame.image.load("./img/wbb.png")
        pieces[1]["K"] = pygame.image.load("./img/wkb.png")
        pieces[1]["Q"] = pygame.image.load("./img/wqb.png")
        pieces[1]["P"] = pygame.image.load("./img/wpb.png")
        pieces[1]["."] = pygame.image.load("./img/b.png")

        clock = pygame.time.Clock()
        posRect = pygame.Rect(0, 0, 60, 60)

        mousePos = [-1, -1]
        markPos = [-1, -1]
        validMoves = []

        gameResults = ["", "WHITE WINS!", "BLACK WINS!", "STALEMATE",
                       "DRAW BY THE FIFTHY MOVES RULE", "DRAW BY THE THREE REPETITION RULE"]

        # show init screen
        # - create some fonts
        font1 = pygame.font.Font(None, 40)
        # - render text
        text1 = font1.render('chess4irc', True, (255, 255, 255), (0, 0, 0))
        # - make rectangles
        rect1 = text1.get_rect()
        # - position rectangles
        rect1.centerx = screen.get_rect().centerx
        rect1.centery = screen.get_rect().centery - 30
        # - blit text
        screen.blit(text1, rect1)
        # - update screen
        pygame.display.update()

        # waiting loop
        self.chess4irc.status = 'Connecting to IRC server. Please wait...'
        margin = 20
        while not self.exitnow:
            # exit when player be ready
            if (self.chess4irc.ready == 1): break

            clock.tick(10)

            # search for gui events
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.chess4irc.quit()
                    time.sleep(1)
                    return

            # refresh screen with new status message from irc client
            if (self.chess4irc.status_changed == 1):
                # update status
                self.chess4irc.status_changed = 0
                # update screen
                font2 = pygame.font.Font(None, 20)
                text2 = font2.render(self.chess4irc.status, True, (122, 122, 122), (0, 0, 0))
                rect2 = text2.get_rect()
                rect2.centerx = screen.get_rect().centerx
                rect2.centery = screen.get_rect().centery + margin
                screen.blit(text2, rect2)
                pygame.display.update()
                margin += 14

        # game loop
        while not self.exitnow:
            clock.tick(30)

            # if remote turn and remote move is not empty
            if self.selected_turn != turn and self.remote_text_move != "":
                self.print_debug("Remote move: " + self.remote_text_move)
                res = chess.addTextMove(self.remote_text_move)
                if res:
                    self.print_debug("Added remote move, res: " + str(res))
                    board = chess.getBoard()
                    turn = chess.getTurn()
                    self.remote_text_move = ""
                    markPos[0] = -1
                    validMoves = []

            # search for gui events
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.exitnow = 1
                    self.chess4irc.quit()
                    time.sleep(5)
                    return
                    '''
                    elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                    return
                    elif event.key == K_LEFT:
                    chess.undo()
                            elif event.key == K_RIGHT:
                                chess.redo()
                            elif event.unicode in ("f","F"):
                                print chess.getFEN()
                            elif event.unicode in ("a","A"):
                                an = chess.getAllTextMoves(chess.AN)
                                if an:
                                    print "AN: " + ", ".join(an)
                            elif event.unicode in ("s","S"):
                                san = chess.getAllTextMoves(chess.SAN)
                                if san:
                                    print "SAN: " + ", ".join(san)
                            elif event.unicode in ("l","L"):
                                lan = chess.getAllTextMoves(chess.LAN)
                                if lan:
                                    print "LAN: " + ", ".join(lan)
                            board = chess.getBoard()
                            turn = chess.getTurn()
                            markPos[0] = -1
                            validMoves = []
                    '''
                if not chess.isGameOver() and self.selected_turn == turn:
                    # local turn
                    if event.type == MOUSEMOTION:
                        mx = event.pos[0]
                        my = event.pos[1]
                        mousePos[0] = int(mx / 60)
                        mousePos[1] = int(my / 60)
                    elif event.type == MOUSEBUTTONDOWN:
                        if mousePos[0] != -1:
                            if markPos[0] == mousePos[0] and markPos[1] == mousePos[1]:
                                markPos[0] = -1
                                validMoves = []
                            else:
                                # blancas
                                # if (turn==ChessBoard.WHITE and board[mousePos[1]][mousePos[0]].isupper()):
                                #    print "turn: " + str(turn) + " | ChessBoard.WHITE: " + str(ChessBoard.WHITE)
                                #    print "pos (is upper?): " + str(board[mousePos[1]][mousePos[0]])
                                # negras
                                # elif (turn==ChessBoard.BLACK and board[mousePos[1]][mousePos[0]].islower()):
                                #    print "turn: " + str(turn) + " | ChessBoard.BLACK: " + str(ChessBoard.BLACK)
                                #    print "pos (is lower?): " + str(board[mousePos[1]][mousePos[0]])

                                # get valid moves
                                if (turn == ChessBoard.WHITE and board[mousePos[1]][mousePos[0]].isupper()) or \
                                        (turn == ChessBoard.BLACK and board[mousePos[1]][mousePos[0]].islower()):
                                    markPos[0] = mousePos[0]
                                    markPos[1] = mousePos[1]
                                    validMoves = chess.getValidMoves(tuple(markPos))
                                # move it
                                else:
                                    if markPos[0] != -1:
                                        res = chess.addMove(markPos, mousePos)
                                        if not res and chess.getReason() == chess.MUST_SET_PROMOTION:
                                            chess.setPromotion(chess.QUEEN)
                                            res = chess.addMove(markPos, mousePos)
                                        if res:
                                            # print chess.getLastMove()
                                            msg = chess.getLastTextMove(chess.SAN)
                                            self.print_debug("Move: " + msg)
                                            self.chess4irc.irc.privmsg("#chess4irc", msg)
                                            board = chess.getBoard()
                                            turn = chess.getTurn()
                                            # moved
                                            self.print_debug("New turn: " + str(turn))
                                            markPos[0] = -1
                                            validMoves = []

            if chess.isGameOver():
                pygame.display.set_caption("Game Over! (Reason:%s)" % gameResults[chess.getGameResult()])
                validMove = []
                markPos[0] = -1
                markPos[1] = -1
            else:
                pygame.display.set_caption('chess4irc')

            y = 0
            for rank in board:
                x = 0
                for p in rank:
                    screen.blit(pieces[(x + y) % 2][p], (x * 60, y * 60))
                    x += 1
                y += 1

            if markPos[0] != -1:
                posRect.left = markPos[0] * 60
                posRect.top = markPos[1] * 60
                pygame.draw.rect(screen, (255, 255, 0), posRect, 4)

            for v in validMoves:
                posRect.left = v[0] * 60
                posRect.top = v[1] * 60
                pygame.draw.rect(screen, (255, 255, 0), posRect, 4)

            pygame.display.flip()

    ####################
    ## MISC FUNCTIONS ##
    ####################

    def print_debug(self, line=""):
        if (self.debug == 1): print
        "[ChessClient] " + str(line)
