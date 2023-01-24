from datetime import datetime, time, date
from typing import List, Any

from chess import *
from chess import polyglot, engine, syzygy
from random import choice

count = 0

wpawn = [0, 0, 0, 0, 0, 0, 0, 0, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 10, 10, 10, 10, 10, 10, 10, 10, 12,
         12, 12, 12, 12, 12, 12, 12, 13, 13, 13, 13, 13, 13, 13, 13, 18, 18, 18, 18, 18, 18, 18, 18, 0, 0, 0, 0, 0, 0,
         0,
         0]

bpawn = [0, 0, 0, 0, 0, 0, 0, 0, 18, 18, 18, 18, 18, 18, 18, 18, 13, 13, 13, 13, 13, 13, 13, 13, 12, 12, 12, 12,
         12, 12, 12, 12, 10, 10, 10, 10, 10, 10, 10, 10, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 0, 0, 0, 0, 0,
         0, 0, 0]

wknight = [25, 28, 28, 28, 28, 28, 28, 25, 28, 30, 30, 30, 30, 30, 30, 28, 28, 30, 30, 30, 30, 30, 30, 28, 28, 30, 30,
           30, 30, 30, 30, 28, 28, 30, 32, 32, 32, 32, 30, 28, 28, 30, 38, 38, 38, 38, 30, 28, 28, 30, 30, 30, 30, 30,
           30, 28, 25, 28, 28, 28, 28, 28, 28, 25]

bknight = [25, 28, 28, 28, 28, 28, 28, 25, 28, 30, 30, 30, 30, 30, 30, 28, 28, 30, 38, 38, 38, 38, 30, 28, 28, 30,
           32, 32, 32, 32, 30, 28, 28, 30, 30, 30, 30, 30, 30, 28, 28, 30, 30, 30, 30, 30, 30, 28, 28, 30, 30, 30, 30,
           30, 30,
           28, 25, 28, 28, 28, 28, 28, 28, 25]

wbishop = [33, 33, 30, 33, 33, 30, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33,
           33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33,
           33, 33, 33, 33, 33, 33, 33, 33, 33, 33]

bbishop = [33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33,
           33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33,
           33, 33,
           33, 33, 33, 30, 33, 33, 30, 33, 33]

wrook = [50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50,
         50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 53, 53, 53, 53, 53, 53, 53, 53,
         50, 50, 50, 50, 50, 50, 50, 50]

brook = [50, 50, 50, 50, 50, 50, 50, 50, 53, 53, 53, 53, 53, 53, 53, 53, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50,
         50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50,
         50,
         50, 50, 50, 50, 50, 50, 50, 50]

wqueen = [90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90,
          90,
          90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90,
          90,
          90, 90, 90, 90, 90, 90, 90, 90]

bqueen = [90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90,
          90,
          90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90,
          90,
          90, 90, 90, 90, 90, 90, 90, 90]

wking = [2, 3, 3, 0, 1, 2, 5, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

bking = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 3, 3, 0, 1, 2, 5, 4]
def value(position):
    global count
    count += 1

    score = 0
    if position.is_check() and position.turn == WHITE:
        score += 2
    if position.is_check() and position.turn == BLACK:
        score -= 2
    if position.is_checkmate() and position.turn == WHITE:
        score += 9999999999
    if position.is_checkmate() and position.turn == BLACK:
        score -= 9999999999
    for j in b.pieces(PAWN, WHITE):
        score += wpawn[j]
    for j in b.pieces(PAWN, BLACK):
        score -= bpawn[j]
    for j in b.pieces(KNIGHT, WHITE):
        score += wknight[j]
    for j in b.pieces(KNIGHT, BLACK):
        score -= bknight[j]
    for j in b.pieces(BISHOP, WHITE):
        score += wbishop[j]
    for j in b.pieces(BISHOP, BLACK):
        score -= bbishop[j]
    for j in b.pieces(ROOK, WHITE):
        score += wrook[j]
    for j in b.pieces(ROOK, BLACK):
        score -= brook[j]
    for j in b.pieces(QUEEN, WHITE):
        score += wqueen[j]
    for j in b.pieces(QUEEN, BLACK):
        score -= bqueen[j]
    for j in b.pieces(KING, WHITE):
        score += wking[j]
    for j in b.pieces(KING, BLACK):
        score -= bking[j]
    return score

def oldvalue(position):
    pawn = [
    [0,0,0,0,0,0,0,0],
    [18,18,18,18,18,18,18,18],
    [13,13,13,13,13,13,13,13],
    [12,12,12,12,12,12,12,12],
    [11,9,11,11,11,11,9,11],
    [9,9,9,9,9,9,9,9],
    [8,8,8,8,8,8,8,8],
    [0,0,0,0,0,0,0,0]]

    knight = [[25,28,28,28,28,28,28,25],
    [28,30,30,30,30,30,30,28],
    [28,30,38,38,38,38,30,28],
    [28,30,32,32,32,32,30,28],
    [28,30,30,30,30,30,30,28],
    [28,30,31,30,30,31,30,28],
    [28,30,30,30,30,30,30,28],
    [25,28,28,28,28,28,28,25]]

    bishop = [[33,33,33,33,33,33,33,33],
    [33,33,33,33,33,33,33,33],
    [33,33,33,33,33,33,33,33],
    [33,33,33,33,33,33,33,33],
    [33,33,33,33,33,33,33,33],
    [33,33,33,33,33,33,33,33],
    [33,33,33,33,33,33,33,33],
    [33,33,30,33,33,30,33,33]]

    rook = [[50,50,50,50,50,50,50,50],
    [53,53,53,53,53,53,53,53],
    [50,50,50,50,50,50,50,50],
    [50,50,50,50,50,50,50,50],
    [50,50,50,50,50,50,50,50],
    [50,50,50,50,50,50,50,50],
    [50,50,50,50,50,50,50,50],
    [50,50,51,52,52,51,50,50]]

    queen = [[90,90,90,90,90,90,90,90],
    [90,90,90,90,90,90,90,90],
    [90,90,90,90,90,90,90,90],
    [90,90,90,90,90,90,90,90],
    [90,90,90,90,90,90,90,90],
    [90,90,90,90,90,90,90,90],
    [90,90,90,90,90,90,90,90],
    [90,90,90,90,90,90,90,90]]

    king = [[0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [2, 3, 3, 0, 1, 2, 5, 4]]

    kingendgame = [[0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 2, 2, 2, 2, 1, 0],
    [0, 1, 2, 3, 3, 2, 1, 0],
    [0, 1, 2, 3, 3, 2, 1, 0],
    [0, 1, 2, 2, 2, 2, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0]]

    score = 0
    if position.is_check() and position.turn == WHITE:
        score += 2
    if position.is_check() and position.turn == BLACK:
        score -= 2
    if position.is_checkmate() and position.turn == WHITE:
        score += 9999999999
    if position.is_checkmate() and position.turn == BLACK:
        score -= 9999999999
    for i in range(0, 8):
        for j in range(0, 8):
            piece = position.piece_at(8*i+j)
            if piece != None:
                piece = piece.symbol()
            if piece == 'R':
                score += rook[7-i][j]
            elif piece == 'r':
                score -= rook[i][j]
            elif piece == 'B':
                score += bishop[7-i][j]
            elif piece == 'b':
                score -= bishop[i][j]
            elif piece == 'N':
                score += knight[7-i][j]
            elif piece == 'n':
                score -= knight[i][j]
            elif piece == 'P':
                score += pawn[7-i][j]
            elif piece == 'p':
                score -= pawn[i][j]
            elif piece == 'Q':
                score += queen[7-i][j]
            elif piece == 'q':
                score -= queen[i][j]
            if position.queens == 0:
                if piece == 'K':
                    score += kingendgame[7-i][j]
                elif piece == 'k':
                    score -= kingendgame[i][j]
            else:
                if piece == 'K':
                    score += king[7-i][j]
                elif piece == 'k':
                    score -= king[i][j]
    return score


MAXDEPTH = 4


class StaffordBot:
    def __init__(self):
        self.reader = polyglot.open_reader("Book/book.bin")
        self.tablebase = syzygy.open_tablebase("3-4-5_pieces_Syzygy/3-4-5")
        self.store = False
        self.saved = {}

    def search(self, board, *args):
        savedposition = {}

        def bestWithDepth(n, alpha, beta, start, nullmove):
            nonlocal board
            nonlocal savedposition

            def checksAndCapturesFirst(move_list):
                next_non_forcing = 0
                for i in range(len(move_list)):
                    if board.gives_check(move_list[i]) or board.is_capture(move_list[i]):
                        temp = move_list[next_non_forcing]
                        move_list[next_non_forcing] = move_list[i]
                        move_list[i] = temp
                        next_non_forcing += 1
                return move_list

            moves = list(board.legal_moves)
            if n == 0 or board.is_checkmate() or board.is_stalemate():
                return value(board), None
            elif self.store and board.fen() in self.saved:
                return self.saved[board.fen()]
            else:
                if board.turn == WHITE:
                    best = -9999999
                    bestMove = None
                    if board.is_checkmate():
                        return -999999, None
                    '''if len(moves) < 4:
                        n += 1'''
                    '''if len(moves) > 8 and not nullmove and n > 2:
                        board.push(Move.null())
                        nullEval, _ = bestWithDepth(n - 2, alpha, beta, False, True)
                        if nullEval > best:
                            best = nullEval
                        board.pop()
                        alpha = max(alpha, best)'''
                    for m in checksAndCapturesFirst(moves):
                        board.push(m)
                        if n == MAXDEPTH and board.can_claim_draw():
                            nextEval = 0
                        elif board.fen() in savedposition:
                            nextEval, refutation = savedposition[board.fen()]
                        else:
                            nextEval, refutation = bestWithDepth(n - 1, alpha, beta, False, False)
                        if nextEval > best:
                            best = nextEval
                            bestMove = m
                        if start:
                            print(m, nextEval)
                            print(best, bestMove)
                        board.pop()
                        if best < -99999 and n == MAXDEPTH - 1:
                            self.store = True
                        savedposition[board.fen()] = best, bestMove
                        if best >= beta:
                            break
                        alpha = max(alpha, best)
                    return best, bestMove
                else:
                    if board.is_checkmate():
                        return 999999, None
                    best = 9999999
                    bestMove = None
                    '''if len(moves) < 4:
                        n += 1'''
                    '''if len(moves) > 8 and not nullmove and n > 2:
                        board.push(Move.null())
                        nullEval, _ = bestWithDepth(n - 2, alpha, beta, False, True)
                        if nullEval < best:
                            best = nullEval
                        board.pop()
                        beta = min(beta, best)'''
                    for m in checksAndCapturesFirst(moves):
                        board.push(m)
                        if n == MAXDEPTH and board.can_claim_draw():
                            nextEval = 0
                        elif board.fen() in savedposition:
                            nextEval, refutation = savedposition[board.fen()]
                        else:
                            nextEval, refutation = bestWithDepth(n - 1, alpha, beta, False, False)
                        if nextEval < best:
                            best = nextEval
                            bestMove = m
                        if start:
                            print(m, nextEval)
                            print(best, bestMove)
                        board.pop()
                        if best > 99999 and n == MAXDEPTH - 1:
                            self.store = True
                        savedposition[board.fen()] = best, bestMove
                        if best <= alpha:
                            break
                        beta = min(beta, best)
                    return best, bestMove

        candidates = list(self.reader.find_all(board))
        if len(candidates) > 0:
            total = 0
            count = 0
            weights = []
            for entry in candidates:
                total += entry.weight
                weights.append(total)
                if count == 3:
                    break
            picked = choice(range(total))
            for i in range(len(weights)):
                if picked < weights[i]:
                    candidates[i].move

        dtz = self.tablebase.get_dtz(board)
        best = -99999999999
        best_move = None
        least_bad = 0
        least_bad_move = None
        if dtz is not None:
            moves = list(board.legal_moves)
            for m in moves:
                board.push(m)
                newdtz = self.tablebase.get_dtz(board)
                if newdtz is None:
                    board.pop()
                    continue
                if newdtz == 0:
                    result = self.tablebase.get_wdl(board)
                    if result == 1:
                        return m
                    elif result == 0:
                        least_bad = 99999999999
                        least_bad_move = m
                if 0 > newdtz > best:
                    best = newdtz
                    best_move = m
                elif newdtz > least_bad:
                    least_bad = newdtz
                    least_bad_move = m
                board.pop()
            if best_move is not None:
                return best_move
            else:
                return least_bad_move
        result = None
        try:
            print("Called")
            result = bestWithDepth(MAXDEPTH, -15000, 15000, True, False)[1]
        except Exception as e:
            print(e)
        if self.store:
            self.saved = savedposition
        return result


test = StaffordBot()
b = Board("r1bq1rk1/1p2bppp/p1nppn2/6B1/P2NPP2/2N2Q2/1PP3PP/R3KB1R w KQ - 1 10")
result = test.search(b, None)
print(result)
b.push(result)
print(b)
print("Count:", count)
print(value(b))


b = [[0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 2, 2, 2, 2, 1, 0],
    [0, 1, 2, 3, 3, 2, 1, 0],
    [0, 1, 2, 3, 3, 2, 1, 0],
    [0, 1, 2, 2, 2, 2, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0]]

newb = []
for rank in b:
    newb = newb + rank
print(newb)
