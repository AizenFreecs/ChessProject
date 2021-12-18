# Imports
import pygame
from Chess import Engine, Ai

# Global variables
Width = Height = 512
Dimensions = 8
SQ_SIZE = Width // Dimensions
Max_FPS = 24
IMAGES = {}


# functions
def LoadImages():
    # Loads the images and scales the images according to our board size
    pieces = ["bR", "bN", "bB", "bQ", "bK", "wR", "wN", "wB", "wQ", "wK", "bp", "wp"]
    for piece in pieces:
        IMAGES[piece] = pygame.transform.scale(pygame.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))


def main():
    # initializing PyGame
    pygame.init()
    screen = pygame.display.set_mode((Width, Height))
    pygame.display.set_caption('Project Chess')
    icon = pygame.image.load("images/bN.png")
    pygame.display.set_icon(icon)
    clock = pygame.time.Clock()
    screen.fill(pygame.Color("white"))
    gs = Engine.GameState()
    menu_bg = pygame.transform.scale(pygame.image.load("images/menu_bg.jpg"), (Width, Height))  # BG Image

    pOne = True  # if player them true else if ai then false
    pTwo = True

    # Here we are running our initial main menu loop which will call the final game loop
    while True:
        # Drawing on the screen
        screen.blit(menu_bg, (0, 0))
        drawText('Ready To Play Chess...', screen, 220, 100)
        drawText(' Press 1 for ', screen, 275, 150)
        drawText(' Player Vs Player ', screen, 235, 175)
        drawText(' Press 2 for ', screen, 275, 225)
        drawText(' Player Vs Computer ', screen, 215, 255)

        # Checking for events
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_1:
                    mainGame(pOne, pTwo, screen, clock, gs)
                if e.key == pygame.K_2:
                    pTwo = False
                    mainGame(pOne, pTwo, screen, clock, gs)
        clock.tick(Max_FPS)
        pygame.display.update()


# The main game loop which contains the the game itself

def mainGame(pOne, pTwo, screen, clock, gs):
    running = True
    gameOver = False  # game ended flag
    selectedSQ = ()  # keeps track of the last square selected by the user
    playerClicks = []  # Keeps track of the players clicks
    LoadImages()
    validMoves = gs.getValidMoves()  # gets the initial list of valid moves for pieces
    moveMade = False  # flag for if the user made a move
    # Loading the sounds
    sound_mov = pygame.mixer.Sound("sounds/Chess_Media_Sounds_move.wav")
    sound_cap = pygame.mixer.Sound("sounds/Chess_Media_Sounds_capture.wav")

    while running:
        # To check if we are playing against another player or computer
        isPlayerTurn = (gs.whiteToMove and pOne) or (not gs.whiteToMove and pTwo)
        # Checking for events
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                gs = Engine.GameState()
                validMoves = gs.getValidMoves()
                selectedSQ = ()
                playerClicks = []
                moveMade = False
                gameOver = False
                running = False
            # Mouse Handlers
            elif e.type == pygame.MOUSEBUTTONDOWN:  # When we Click the mouse button
                if not gameOver and isPlayerTurn:
                    location = pygame.mouse.get_pos()  # Location of the Mouse Pointer
                    col = location[0] // SQ_SIZE  # get column from X-Coordinate
                    row = location[1] // SQ_SIZE  # get row from Y-coordinate
                    if selectedSQ == (row, col):  # get the square which was clicked and store its location
                        selectedSQ == ()
                        playerClicks == []
                    else:
                        selectedSQ = (row, col)

                        playerClicks.append(selectedSQ)
                    if len(playerClicks) == 2:
                        move = Engine.Move(playerClicks[0], playerClicks[1], gs.board)
                        print(move.getChessNotation())
                        for i in range(len(validMoves)):  # Making the Valid Move
                            if move == validMoves[i]:
                                gs.makeMove(validMoves[i])
                                moveMade = True
                                selectedSQ = ()
                                playerClicks = []

                        if not moveMade:
                            playerClicks = [selectedSQ]

            # Key Handlers
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_z:  # For Undo
                    gs.undoMove()
                    moveMade = True
                if e.key == pygame.K_r:  # For Resetting the board
                    gs = Engine.GameState()
                    validMoves = gs.getValidMoves()
                    selectedSQ = ()
                    playerClicks = []
                    moveMade = False
                    gameOver = False

        # Ai Logic
        if not gameOver and not isPlayerTurn:
            AiMove = Ai.findBestMove(gs, validMoves)
            if AiMove is None:
                AiMove = Ai.findRandomMove(validMoves)
            gs.makeMove(AiMove)
            moveMade = True

        if moveMade:  # To reset the validmoves and movemade flag
            validMoves = gs.getValidMoves()
            moveMade = False
            if move.pieceMoved != '--':  # getting the sounds to play
                pygame.mixer.Sound.play(sound_mov)
            if move.pieceCaptured != '--':
                pygame.mixer.Sound.play(sound_cap)
        DrawGameState(screen, gs, validMoves, selectedSQ)  # Drawing the board and pieces

        # Game End Conditions
        if gs.checkMate:
            gameOver = True
            if gs.whiteToMove:
                drawEndText(screen, "Black win by checkmate")
            else:
                drawEndText(screen, "White win by checkmate")
        elif gs.staleMate:
            gameOver = True
            drawEndText(screen, "Stalemate")

        clock.tick(Max_FPS)
        pygame.display.flip()


def highlightSquares(screen, gs, validMoves, selectedSQ):
    # This Functions highlights the current selected square and all the possible square where the piece can move
    if selectedSQ != ():
        r, c = selectedSQ
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'):  # make sure the selected square can be moved
            # highlight selected square
            s = pygame.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)  # transparency value
            s.fill(pygame.Color('blue'))
            screen.blit(s, (c * SQ_SIZE, r * SQ_SIZE))

            # highlight the possible moves
            s.fill(pygame.Color('red'))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (SQ_SIZE * move.endCol, move.endRow * SQ_SIZE))


def DrawGameState(screen, gs, validMoves, selectedSQ):
    # This function Draws the game board and pieces
    drawBoard(screen)
    highlightSquares(screen, gs, validMoves, selectedSQ)
    drawPieces(screen, gs.board)


def drawBoard(screen):
    # Draws the Board
    colors = [pygame.Color(235, 235, 208), pygame.Color(119, 148, 85)]
    for r in range(Dimensions):
        for c in range(Dimensions):
            color = colors[((r + c) % 2)]
            pygame.draw.rect(screen, color, pygame.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def drawPieces(screen, board):
    # Draws the pieces
    for r in range(Dimensions):
        for c in range(Dimensions):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], pygame.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def drawEndText(screen, text):
    # Draw the end Game Text
    font = pygame.font.SysFont("Comic Sans", 32, True, False)
    textObject = font.render(text, 0, pygame.Color('Black'))
    textLocation = pygame.Rect(0, 0, Width, Height).move(Width // 2 - textObject.get_width() // 2,
                                                         Height // 2 - textObject.get_height() // 2)
    screen.blit(textObject, textLocation)


def drawText(text, screen, x, y):  # Draws text on the screen
    font = pygame.font.SysFont("Comic Sans", 32, True, False)
    textObj = font.render(text, 1, pygame.Color("White"))
    textRect = textObj.get_rect()
    textRect.topleft = (x, y)
    screen.blit(textObj, textRect)


if __name__ == '__main__':
    main()
