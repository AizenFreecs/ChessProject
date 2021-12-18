import random

# variable
pieceValue = {"K": 0, "Q": 10, "R": 5, "N": 3, "B": 3.25, "p": 1}
CheckMate = 1000
StaleMate = 0
DEPTH = 3


# To get a random move from all the possible moves
def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves) - 1)]


# To find the best possible move for the AI
def findBestMove(gs, validMoves):
    global nextMove
    nextMove = None
    findMoveNegaMaxABP(gs, validMoves, DEPTH, 1 if gs.whiteToMove else -1, -CheckMate, CheckMate)
    return nextMove


# This implements the NegaMax algorithm along with Alpha Beta Pruning
def findMoveNegaMaxABP(gs, validmoves, depth, turnCheck, alpha, beta):
    global nextMove
    if depth == 0:
        return turnCheck * valueBoard(gs)
    maxScore = -CheckMate
    for move in validmoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMaxABP(gs, nextMoves, depth - 1, -turnCheck, -beta, -alpha)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMoves = move
        gs.undoMove()
        if maxScore > alpha:
            alpha = maxScore
        if alpha >= beta:
            break
    return maxScore


# To get value of the board at a time
def valueBoard(gs):
    if gs.checkMate:
        if gs.whiteToMove:
            return -CheckMate
        else:
            return CheckMate
    elif gs.staleMate:
        return StaleMate
    score = 0
    for row in gs.board:
        for square in row:
            if square[0] == 'w':
                score += pieceValue[square[1]]
            elif square[0] == 'b':
                score -= pieceValue[square[1]]
    return score
