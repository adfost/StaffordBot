import torch
import torch.nn as nn
from chess import *
from chess import polyglot, syzygy, engine
from random import choice
from strategies import MinimalEngine
from utils.getannotated import *


class Net(nn.Module):
    def __init__(self):
        # Define all the parameters of the net
        super(Net, self).__init__()
        self.fc1 = nn.Linear(64 * 12 + 6, 200, dtype=float)
        self.fc2 = nn.Linear(200, 200, dtype=float)
        self.fc3 = nn.Linear(200, 200, dtype=float)
        self.fc4 = nn.Linear(200, 200, dtype=float)
        self.fc5 = nn.Linear(200, 1, dtype=float)

    def forward(self, x):
        # Do the forward pass
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = F.relu(self.fc3(x))
        x = F.relu(self.fc4(x))
        x = self.fc5(x)
        return x


model = Net()
model.load_state_dict(torch.load("model.pt"))


def value(b):
    b2 = convertBoard(b)
    return model(torch.tensor(b2, dtype=float))

MAXDEPTH = 5


class StaffordBot(MinimalEngine):
    def __init__(self, commands, options, stderr, draw_or_resign, name="StaffordBot", **popen_args):
        super().__init__(commands, options, stderr, draw_or_resign, name, **popen_args)
        self.reader = polyglot.open_reader("Book/book.bin")
        self.tablebase = syzygy.open_tablebase("3-4-5_pieces_Syzygy/3-4-5")
        self.store = False
        self.saved = {}

    def search(self, board, *args):
        savedposition = {}

        def bestWithDepth(n, alpha, beta, start, nullmove, total):
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
            elif board.can_claim_draw():
                return 0, None
            elif self.store and board.fen() in self.saved:
                return self.saved[board.fen()]
            else:
                if board.turn == WHITE:
                    if board.is_checkmate():
                        return -999999, None
                    best = -9999999
                    bestMove = None
                    if len(moves) > 0:
                        bestMove = moves[0]
                    if len(moves) < 4 and total < 8:
                        n += 1
                        total += 1
                    '''if len(moves) > 8 and not nullmove and n > 2:
                        board.push(Move.null())
                        nullEval, _ = bestWithDepth(n - 2, alpha, beta, False, True)
                        if nullEval > best:
                            best = nullEval -10
                        board.pop()
                        alpha = max(alpha, best)'''
                    for m in checksAndCapturesFirst(moves):
                        board.push(m)
                        if n == MAXDEPTH and board.can_claim_draw():
                            nextEval = 0
                        elif board.fen() in savedposition:
                            nextEval, refutation = savedposition[board.fen()]
                        else:
                            nextEval, refutation = bestWithDepth(n - 1, alpha, beta, False, False, total)
                        if nextEval > best:
                            best = nextEval
                            bestMove = m
                        if start:
                            print(m, nextEval)
                            print(bestMove, best)
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
                    if len(moves) > 0:
                        bestMove = moves[0]
                    if len(moves) < 4 and total < 8:
                        n += 1
                        total += 1
                    '''if len(moves) > 8 and not nullmove and n > 2:
                        board.push(Move.null())
                        nullEval, _ = bestWithDepth(n - 2, alpha, beta, False, True)
                        if nullEval < best:
                            best = nullEval + 10
                        board.pop()
                        beta = min(beta, best)'''
                    for m in checksAndCapturesFirst(moves):
                        board.push(m)
                        if n == MAXDEPTH and board.can_claim_draw():
                            nextEval = 0
                        elif board.fen() in savedposition:
                            nextEval, refutation = savedposition[board.fen()]
                        else:
                            nextEval, refutation = bestWithDepth(n - 1, alpha, beta, False, False, total)
                        if nextEval < best:
                            best = nextEval
                            bestMove = m
                        if start:
                            print(m, nextEval)
                            print(bestMove, best)
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
                    return engine.PlayResult(candidates[i].move, None)

        dtz = self.tablebase.get_dtz(board)
        best = -99999999999
        best_move = None
        least_bad = 0
        least_bad_move = None
        if dtz is not None and board.pawns == 0:
            moves = list(board.legal_moves)
            for m in moves:
                board.push(m)
                newdtz = self.tablebase.get_dtz(board)
                print(m, newdtz)
                print(best, best_move)
                if newdtz is None:
                    board.pop()
                    continue
                if newdtz == 0:
                    result = self.tablebase.get_wdl(board)
                    if result == 1:
                        return engine.PlayResult(m, None)
                    elif result == 0:
                        least_bad = 0
                        least_bad_move = m
                if 0 > newdtz > best:
                    best = newdtz
                    best_move = m
                elif newdtz > least_bad:
                    least_bad = newdtz
                    least_bad_move = m
                board.pop()
            if best_move is not None:
                return engine.PlayResult(best_move, None)
            else:
                return engine.PlayResult(least_bad_move, None)
        result = None
        try:
            print("Called")
            depth = MAXDEPTH
            if len(list(board.legal_moves)) < 18:
                depth += 1
            if len(list(board.legal_moves)) < 10:
                depth += 2
            result = bestWithDepth(MAXDEPTH, -15000, 15000, True, False, depth)[1]
        except Exception as e:
            print(e)
        if self.store:
            self.saved = savedposition
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
