import chess as c
import Backend.Convert as conv
from copy import deepcopy
from stockfish import Stockfish


class Logic:

    def __init__(self, gui):
        # init new Game
        self.board = c.Board()
        self.saved_input = None
        self.save_color = None
        self.saved_posl = None
        self.finished = False
        self.gui = gui
        self.round = 0
        self.stock = Stockfish(path="/opt/homebrew/Cellar/stockfish/15.1/bin/stockfish", depth=18, parameters={"Threads": 4, "Minimum Thinking Time": 30})
        #self.stock = Stockfish(path="C:/Users/konst/Downloads/stockfish_15.1_win_x64_popcnt/stockfish-windows-2022-x86-64-modern.exe", depth=18, parameters={"Threads": 4, "Minimum Thinking Time": 30})


    # input of mouseClick
    def input(self, x, y):
        print("###########\nStatus:")
        print(self.board.unicode())
        ret_value = 0

        self.gui.deleteArrow()
        delete = False

        # if the game is not finished:
        if not self.finished:
            cv = conv.Convert()
            # convert pixel pos to field:
            pos = cv.convPosFie(x, y)
            # convert first var to letter
            l2 = cv.convFieLet(pos[0])
            # position with letter
            posl = l2 + str(pos[1])

            # get the piece
            piece = self.board.piece_at(c.parse_square(l2 + str(pos[1])))

            # if no piece was selected earlier
            if self.saved_input is None:
                # check legal Pick
                if piece:
                    # get its color
                    color = piece.color
                    if self._checkColor(color):
                        print("found Piece")
                        self.saved_input = pos
                        self.saved_posl = posl
                        self.save_piece = piece
                        self.save_color = color
                        self.gui.legalPick(pos)
                    else:
                        print("Wrong Color")
                        self.gui.illegalColor()
                else:
                    print("there is no piece")
                    self.gui.illegalPick()
            else:
                # choose another piece
                if piece:
                    if self.save_color == self.board.piece_at(c.parse_square(l2 + str(pos[1]))).color:
                        print("other piece chosen")
                        self.saved_input = pos
                        self.saved_posl = posl
                        self.save_piece = piece
                        self.gui.legalPick(pos)
                        return

                # convert to letter:
                l1 = cv.convFieLet(self.saved_input[0])
                # create the move
                move = c.Move.from_uci(l1+str(self.saved_input[1])+l2+str(pos[1]))

                # check legal Move
                if move in self.board.legal_moves:
                    if self.board.is_castling(move):
                        # do something
                        self.gui.castling(posl, True)
                        self.gui.insertItemInList("cg", posl, str(self.save_piece), None)
                    else:
                        # if legal move then
                        self.gui.legalMove(self.saved_input, pos, self.save_piece)
                        self.gui.insertItemInList(self.saved_posl, posl, str(self.save_piece), str(piece))
                    print("legal Move")
                    self.board.push(move)
                    print(str(self.save_piece), str(piece))
                    self.saved_input = None
                    self.save_color = None
                    self.round += 1
                    ret_value = 1
                # pawn promotion
                elif c.Move.from_uci(str(move) + "q") in self.board.legal_moves:
                        print("Pawn Promotion detected")
                        # löschen die id von der Position und setzen einfach eine Dame darauf
                        self.gui.pawnPromo(self.saved_input, pos, True)
                        self.gui.insertItemInList(self.saved_posl, posl, str(self.save_piece), str(piece))
                        print("legal Move")
                        self.board.push(c.Move.from_uci(str(move) + "q"))
                        print(str(self.save_piece), str(piece))
                        self.saved_input = None
                        self.save_color = None
                        self.round += 1
                else:
                    # GUI Change
                    print("illegal Move")
                    self.gui.illegalMove()

                # check game finished
                self._checkCheck()

        return ret_value

    def _checkCheck(self):
        if self.board.is_checkmate():
            print("Schachmatt, Spiel vorbei")
            self.finished = True
            self.gui.checkMate()
        elif self.board.is_stalemate():
            print("Remis, Spiel vorbei")
            self.finished = True
            self.gui.staleMate()
        elif self.board.is_check():
            print("Schach erkannt")
            self.gui.check("Schach " + self.side)

    def _checkColor(self, color):
        if(self.round % 2 == 0) and (color == c.WHITE):
            self.side = "Schwarz"
            return True
        elif(self.round % 2 == 1) and (color == c.BLACK):
            self.side = "Weiß"
            return True
        else:
            return False

    def _getFinished(self):
        return self.finished

    scoring = {'p': -1,
               'n': -3,
               'b': -3,
               'r': -5,
               'q': -9,
               'k': 0,
               'P': 1,
               'N': 3,
               'B': 3,
               'R': 5,
               'Q': 9,
               'K': 0,
    }

    def eval_board(self, BOARD):
        score = 0
        pieces = BOARD.piece_map()
        for key in pieces:
            score += self.scoring[str(pieces[key])]

        return score

    def getTipp(self):
        return self.min_maxN(self.board, 3)

    def byStock(self):
        self.stock.set_fen_position(self.board.fen())
        return self.stock.get_best_move()

