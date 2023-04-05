import torch
from chess import polyglot, syzygy, engine
from random import choice

from chess.polyglot import zobrist_hash

from strategies import MinimalEngine
from utils.getannotated import *
from nnmodel import *

model = Net()
model.load_state_dict(torch.load("model685.pt", map_location=torch.device('cpu')))


def value(b):
    b2 = convertBoard(b)
    return model(torch.tensor(b2, dtype=float))

MAXDEPTH = 3
EXTENDEDDEPTH = 8

class StaffordBot(MinimalEngine):
    def __init__(self, commands, options, stderr, draw_or_resign, name="StaffordBot", **popen_args):
        super().__init__(commands, options, stderr, draw_or_resign, name, **popen_args)
        self.reader = polyglot.open_reader("Book/full_combined.bin")
        self.tablebase = syzygy.open_tablebase("3-4-5_pieces_Syzygy/3-4-5")
        self.store = False
        self.saved = {}

    def search(self, board, *args):
        savedposition = {}
        count = 0
        total1 = 0

        def bestWithDepth(n, alpha, beta, start, nullmove, total):
            nonlocal board
            nonlocal savedposition
            nonlocal count
            nonlocal total1

            def checksAndCapturesFirst(move_list):
                next_non_forcing1 = 0
                for i in range(len(move_list)):
                    if board.gives_check(move_list[i]) or board.is_capture(move_list[i]):
                        temp = move_list[next_non_forcing1]
                        move_list[next_non_forcing1] = move_list[i]
                        move_list[i] = temp
                        next_non_forcing1 += 1
                return move_list, next_non_forcing1

            def checksAndCapturesOnly(move_list):
                result = []
                for i in range(len(move_list)):
                    if board.gives_check(move_list[i]) or board.is_capture(move_list[i]):
                        result.append(move_list[i])
                return result, len(result)

            moves = list(board.legal_moves)
            if zobrist_hash(board) in savedposition:
                count += 1
                return savedposition[zobrist_hash(board)]
            elif n == 0 or total >= EXTENDEDDEPTH:
                total1 += 1
                return value(board), None
            if board.is_checkmate():
                if board.turn == WHITE:
                    return -999999, None
                else:
                    return 999999, None
            elif board.is_stalemate():
                return 0, None
            elif board.can_claim_draw():
                return 0, None
            else:
                if board.turn == WHITE:
                    best = -9999999
                    bestMove = None
                    if len(moves) > 0:
                        bestMove = moves[0]
                    # Null Move
                    if start:
                        board.push(Move.null())
                        best, _ = bestWithDepth(n, alpha, beta, False, True, total + 3)
                        print("Null")
                        print(best)
                        alpha = max(alpha, best)
                        board.pop()
                    if total > MAXDEPTH:
                        modifiedMoves, next_non_forcing = checksAndCapturesOnly(moves)
                        best = value(board)
                    else:
                        modifiedMoves, next_non_forcing = checksAndCapturesFirst(moves)
                    for j in range(len(modifiedMoves)):
                        board.push(modifiedMoves[j])
                        if n == MAXDEPTH and board.can_claim_draw():
                            nextEval = 0
                        elif j < next_non_forcing or board.is_check():
                            nextEval, refutation = bestWithDepth(n, alpha, beta, False, False, total+1)
                        else:
                            nextEval, refutation = bestWithDepth(n - 1, alpha, beta, False, False, total+1)
                        if nextEval > best:
                            best = nextEval
                            bestMove = modifiedMoves[j]
                        if start:
                            print(modifiedMoves[j], refutation, nextEval)
                            print(bestMove, best)
                        board.pop()
                        if best < -99999 and n == MAXDEPTH - 1:
                            self.store = True
                        savedposition[zobrist_hash(board)] = best, bestMove
                        if best >= beta:
                            break
                        alpha = max(alpha, best)
                    return best, bestMove
                else:
                    best = 9999999
                    bestMove = None
                    if len(moves) > 0:
                        bestMove = moves[0]
                    # Null Move
                    if start:
                        board.push(Move.null())
                        best, _ = bestWithDepth(n, alpha, beta, False, True, total + 3)
                        print("Null")
                        print(best)
                        beta = min(beta, best)
                        board.pop()
                    if total > MAXDEPTH:
                        modifiedMoves, next_non_forcing = checksAndCapturesOnly(moves)
                        best = value(board)
                    else:
                        modifiedMoves, next_non_forcing = checksAndCapturesFirst(moves)
                    for j in range(len(modifiedMoves)):
                        board.push(modifiedMoves[j])
                        if n == MAXDEPTH and board.can_claim_draw():
                            nextEval = 0
                        elif j < next_non_forcing or board.is_check():
                            nextEval, refutation = bestWithDepth(n, alpha, beta, False, False, total+1)
                        else:
                            nextEval, refutation = bestWithDepth(n - 1, alpha, beta, False, False, total+1)
                        if nextEval < best:
                            best = nextEval
                            bestMove = modifiedMoves[j]
                        if start:
                            print(modifiedMoves[j], refutation, nextEval)
                            print(bestMove, best)
                        board.pop()
                        if best > 99999 and n == MAXDEPTH - 1:
                            self.store = True
                        savedposition[zobrist_hash(board)] = best, bestMove
                        if best <= alpha:
                            break
                        beta = min(beta, best)
                    return best, bestMove

        candidates = list(self.reader.find_all(board))
        if len(candidates) > 0:
            if board.fen() == "rnbqkbnr/ppp1pppp/8/3p4/2PP4/8/PP2PPPP/RNBQKBNR b KQkq - 0 2":
                return engine.PlayResult(candidates[0].move, None)
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
                    return engine.PlayResult(candidates[i].move, None)

        wdl = self.tablebase.get_wdl(board)
        best = 2
        best_move = None
        least_bad = 0
        least_bad_move = None
        best_dtz = 99999999
        if wdl is not None:
            moves = list(board.legal_moves)
            for m in moves:
                board.push(m)
                newwdl = self.tablebase.get_wdl(board)
                print(newwdl, m)
                print(best, best_move)
                if newwdl is None or best < newwdl:
                    board.pop()
                    continue
                elif newwdl < best:
                    best = newwdl
                    best_move = m
                    best_dtz = self.tablebase.get_dtz(board)
                elif best == -2:
                    dtz = self.tablebase.get_dtz(board)
                    if dtz is None or dtz > best_dtz:
                        best_dtz = dtz
                        best_move = m
                elif best < 0:
                    dtz = self.tablebase.get_dtz(board)
                    if dtz is not None and dtz < least_bad:
                        least_bad = dtz
                        least_bad_move = m
                board.pop()
            if best_move is not None:
                return engine.PlayResult(best_move, None)
            else:
                return engine.PlayResult(least_bad_move, None)

        result = None
        try:
            print("Called")
            result = bestWithDepth(MAXDEPTH, -15000, 15000, True, False, 0)[1]
        except Exception as e:
            print(e)
        #if self.store:
            #self.saved = savedposition
        print(total1)
        print(count)
        return engine.PlayResult(result, None)


# Test Code
'''b = Board("4k3/8/8/8/8/8/8/4K2R w - - 0 1")
while not b.is_checkmate():
    print(b)
    print("Enter Move:")
    yourmove = Move.from_uci(input())
    b.push(yourmove)
    print(b)
    b.clear_stack()
    print("Searching")
    best = findBestMove(b)
    b.push(best)'''
