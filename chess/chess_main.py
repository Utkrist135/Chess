"""
This in the main driver file, responsible for handling user input and displaying the current Game state object
"""
import pygame as p
from chess import chess_engine, ChessAI

WIDTH = HEIGHT = 520
DIMENSION = 8
SQ_SIZE = HEIGHT/DIMENSION
MAX_FPS = 15 #for animations
IMAGES = {}

'''
Initialise a global dictionary of images. This will be called once in main
'''

def loadImages():
    pieces = ['wP', 'wN', 'wK', 'wQ', 'wB','wR', 'bP', 'bB', 'bQ', 'bK', 'bN', 'bR']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/"+ piece +".png"),(SQ_SIZE,SQ_SIZE))
    #We can access an image by using the dictionary

'''
The main driver for our code. This will handle user input and updating the graphics
'''
def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = chess_engine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False #flag variable for when a move is made

    loadImages() #Only do this once, before the while loop
    running = True
    sqSelected = () # no square is selected currently, keeps track of the last click of the user(Tuple: x,y)
    playerClicks = [] #keep track of the player clicks (two tuples: [(6,4),(4,4)]
    gameOver = False
    playerOne = False # If a human is playing white it's true if AI is playing then False
    playerTwo = False # same as above


    while running:
        humanTurn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            #Mouse Handler
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver and humanTurn:
                    location = p.mouse.get_pos() #(x,y) location of the mouse
                    col = location[0]//SQ_SIZE
                    row = location[1]//SQ_SIZE
                    if sqSelected == (row, col): #user selected the same square twice
                        sqSelected = ()   #deselect
                        playerClicks = []  #clear player clicks
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected)#append for both 1st and 2nd clicks

                    if len(playerClicks) == 2: #after 2nd click
                        move = chess_engine.Move(playerClicks[0], playerClicks[1], gs.board)
                        print(move.getChessNotation())
                        for i in range(len(validMoves)):
                                if move == validMoves[i]:
                                    gs.makeMove(validMoves[i])
                                    moveMade = True
                                    sqSelected = () #reset the user click
                                    playerClicks = []
                        if not moveMade:
                            playerClicks = [sqSelected]
            #Key Handler
            elif e.type == p.KEYDOWN:
                if e.key == p.K_s: #undo when 's' is pressed
                    gs.undoMove(move)
                    moveMade = True
                if e.key == p.K_r: #reset the board if r is pressed
                    gs = chess_engine.GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False



        #AI move finder logic
        if not gameOver and not humanTurn:
            AIMove = ChessAI.findRandomMove(validMoves)
            gs.makeMove(AIMove)
            moveMade = True


        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False


        drawGameState(screen, gs, validMoves, sqSelected)

        if gs.checkmate:
            gameOver = True
            if gs.whiteToMove:
                drawText(screen, 'Black wins by checkmate. Get rekt!!')
            else:
                drawText(screen, 'White wins by checkmate. Get rekt!!')
        elif gs.stalemate:
            gameOver = True
            drawText(screen, 'Stalemate!!')



        clock.tick(MAX_FPS)
        p.display.flip()



'''
Highlights square selected and possible moves
'''
def highlightSquare(screen, gs, validmoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        r=int(r)
        c=int(c)
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'): #sqSelected is a piece
            #Highlight the selected square
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100) #Transparency Value
            s.fill(p.Color('blue'))
            screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))
            #Highlight all possible moves
            s.fill(p.Color('yellow'))
            for move in validmoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (move.endCol*SQ_SIZE, move.endRow*SQ_SIZE))






def drawGameState(screen, gs, validmoves, sqSelected):
    drawBoard(screen) #draw squares in the board
    highlightSquare(screen, gs, validmoves, sqSelected)
    drawPieces(screen, gs.board) #Draw pieces on top of the squares



'''
Draws Squares on the board
'''
def drawBoard(screen):
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c) % 2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

'''
Draw the pieces on the board using the current GameState.board
'''
def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece=board[r][c]
            if piece != "--": #not empty
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE,r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


def drawText(screen, text):
    font = p.font.SysFont("Helvitca", 32, True, False)
    textObject = font.render(text, 0, p.Color('Black'))
    textLocation = p.Rect(0, 0, WIDTH, HEIGHT). move(WIDTH/2 - textObject.get_width()/2, HEIGHT/2 - textObject.get_height()/2)
    screen.blit(textObject, textLocation)

if __name__ == "__main__":
    main()

main()
