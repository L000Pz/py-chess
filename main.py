import pygame as p
import engine
from button import Button

HEIGHT = WIDTH = 512
DIMENSION = 8
SQ_SIZE=HEIGHT//DIMENSION
MAX_FPS = 15
IMAGES = {}
UNDOICON = p.image.load("chess/images/undo.png")
REDOICON = p.image.load("chess/images/redo.png")
NEWGAMEICON = p.image.load("chess/images/plus.png")
UNDO = Button(UNDOICON, (3*SQ_SIZE+SQ_SIZE/2-3, HEIGHT+SQ_SIZE + 40), 15, 30,None)
REDO = Button(REDOICON, (30+4*SQ_SIZE+SQ_SIZE/2, HEIGHT+SQ_SIZE + 40), 15, 30, None)
NEWGAME = Button(NEWGAMEICON, (SQ_SIZE+SQ_SIZE/2 +32, HEIGHT+SQ_SIZE + 40), 30, 30, None)

def loadImg():
    pieces = ['wp','wR','wN','wB','wQ','wK','bp','bR','bN','bB','bQ','bK']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("chess/images/"+piece+".png"),(SQ_SIZE,SQ_SIZE))
    icon = p.image.load(("chess/images/icon.png")) 
    
    p.display.set_icon(icon)   
    p.display.set_caption("CHOSS.CUM")

def main():
    p.init()
    screen = p.display.set_mode((WIDTH+(3*SQ_SIZE),HEIGHT+(3*SQ_SIZE)))
    clock = p.time.Clock()
    screen.fill(p.Color(238,238,210))
    gameState = engine.state()
    validMoves = gameState.validMoves()
    moveMade = False
    currentSec = 30
    p.time.set_timer(p.USEREVENT, 1000)
    loadImg()
    selectedSQ = ()
    clicks = []
    running = True
    global gameOver
    gameOver = False
    global moveLog
    moveLog =[]
    redoLog =[]
    while running: 
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver:
                    loc = p.mouse.get_pos()
                    if 0<loc[0] -SQ_SIZE <=512 and  0<loc [1] -SQ_SIZE<=512:
                        col = (loc[0] - SQ_SIZE)//SQ_SIZE 
                        row = (loc[1] - SQ_SIZE)//SQ_SIZE 
                        if selectedSQ == (row,col):
                            selectedSQ = ()
                            clicks = []
                        else:
                            selectedSQ = (row , col)
                            clicks.append(selectedSQ)
                        if len(clicks)==2:
                            print (clicks)
                            move = engine.Move(clicks[0],clicks[1],gameState.board)
                            print(move.Notation())
                            for i in range(len(validMoves)):
                                if move == validMoves[i]:
                                    gameState.makeMove(validMoves[i])
                                    
                                    saveMoveLog(move.Notation())
                                    redoLog = []
                                    moveMade = True
                                    selectedSQ = ()
                                    clicks = []
                                if not moveMade:
                                    clicks = [selectedSQ]
                if UNDO.check_for_input(p.mouse.get_pos()):
                    if len(moveLog)>0:
                        gameState.undo()
                        move = moveLog.pop()
                        redoLog.append(move)
                        moveMade = True
                if REDO.check_for_input(p.mouse.get_pos()):
                    if len(redoLog)>0 :
                        gameState.redo()
                        move = redoLog.pop()
                        moveLog.append(move)
                        moveMade = True
                if NEWGAME.check_for_input(p.mouse.get_pos()):
                    gameState = engine.state()
                    validMoves = gameState.validMoves()
                    selectedSQ = ()
                    clicks = []
                    moveLog = []
                    redoLog = []
                    moveMade = False
                    gameOver = False
                    currentSec = 30
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    if len(moveLog)>0:
                        gameState.undo()
                        move = moveLog.pop()
                        redoLog.append(move)
                        moveMade = True
                elif e.key == p.K_x:
                    if len(redoLog)>0 :
                        gameState.redo()
                        move = redoLog.pop()
                        moveLog.append(move)
                        moveMade = True
                elif e.key == p.K_r:
                    gameState = engine.state()
                    validMoves = gameState.validMoves()
                    selectedSQ = ()
                    clicks = []
                    moveLog = []
                    redoLog = []
                    moveMade = False
                    gameOver = False
                    currentSec = 30
                elif e.key == p.K_s:
                    save()
            
            if e.type == p.USEREVENT and not moveMade and not gameOver :
                currentSec -= 1
                if currentSec == 0 and not moveMade:
                    gameState.checkMate = True
                    
            elif moveMade or gameOver: currentSec = 30
        if moveMade:
            validMoves = gameState.validMoves()
            moveMade = False
            drawGS(screen,gameState,currentSec,validMoves,selectedSQ)
        drawGS(screen,gameState,currentSec,validMoves,selectedSQ)
        if gameState.checkMate:
            gameOver = True
            if gameState.whiteToMove:
                drawTxt(screen,'Black Wins')
            else:
                drawTxt(screen,'White Wins')
        elif gameState.staleMate:
            gameOver = True
            drawTxt(screen,'STOOLMATE,NOONE WIIIIINSSSSS')
        UNDO.update(screen)
        REDO.update(screen)
        NEWGAME.update(screen)
        clock.tick(MAX_FPS)
        p.display.flip()

def highSQs(screen,gameState,validMoves,selectedSQs):
    if selectedSQs != ():
        row,col =selectedSQs
        if gameState.board[row][col][0] == ('w'if gameState.whiteToMove else 'b'):
            s = p.Surface((SQ_SIZE,SQ_SIZE))
            s.fill(p.Color(187,204,58))
            screen.blit(s,(col*SQ_SIZE + SQ_SIZE,row*SQ_SIZE + SQ_SIZE))
            i = 0
            for move in validMoves:
                if move.startRow == row and move.startCol == col:
                    s.fill(p.Color("black"))
                    s.set_alpha(80)
                    # s.fill(p.Color(0 + i , 50 + i, 0 + i))
                    screen.blit(s,(SQ_SIZE*move.endCol + SQ_SIZE,SQ_SIZE *move.endRow+SQ_SIZE))
                    i = i+10

def drawGS(screen,gameState,currentSec,validMoves,selectedSQs):
    drawSQs(screen)
    highSQs(screen,gameState,validMoves,selectedSQs)
    drawPCs(screen,gameState.board)
    drawClockAndTurn(screen,gameState,currentSec)
    drawSQNames(screen)
    drawBTNS(screen)
    drawTaken(screen,gameState)

def drawSQs(screen):
    global colors
    colors = [p.Color((238,238,210)),p.Color((118,150,86))]
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            color = colors[((row+col)%2)]
            p.draw.rect(screen,color,p.Rect(col*SQ_SIZE + SQ_SIZE,row*SQ_SIZE + SQ_SIZE,SQ_SIZE,SQ_SIZE))
    # newWidth = WIDTH + SQ_SIZE
    # newHeight = HEIGHT +SQ_SIZE
    # p.draw.line(screen,'black',(newWidth+4,SQ_SIZE),(newWidth+4,newHeight+5),10)
    # p.draw.line(screen,'black',(SQ_SIZE,newHeight+4),(newHeight,newWidth+4),10)
    # p.draw.line(screen,'black',(SQ_SIZE-6,SQ_SIZE-5),(SQ_SIZE-6,newHeight+5),10)
    # p.draw.line(screen,'black',(SQ_SIZE-9,SQ_SIZE-6),(newWidth+5,SQ_SIZE-6),10)
def drawPCs(screen,board):
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            piece = board[row][col]
            if piece != "--":
                screen.blit(IMAGES[piece],p.Rect(col*SQ_SIZE + SQ_SIZE,row*SQ_SIZE + SQ_SIZE,SQ_SIZE,SQ_SIZE))
def drawClockAndTurn(screen,gameState,currentSec):
    colors = [p.Color((186,202,68))]
    p.draw.rect(screen, (33,32,30), p.Rect(0,0,SQ_SIZE,11*SQ_SIZE))
    p.draw.rect(screen, (33,32,30), p.Rect(0,0,11*SQ_SIZE,SQ_SIZE))
    p.draw.rect(screen, (33,32,30), p.Rect(0,WIDTH+SQ_SIZE,11*SQ_SIZE,2*SQ_SIZE))
    p.draw.rect(screen, colors[0], p.Rect(HEIGHT-SQ_SIZE,WIDTH+SQ_SIZE+15,2*SQ_SIZE,SQ_SIZE-20),0,7)
    FONT = p.font.Font("chess/assets/Montserrat-Bold.ttf", 30)
    if currentSec >= 0 :
        display_seconds = currentSec % 60
        display_minutes = int(currentSec / 60) % 60
    timer_text = FONT.render(f"{display_minutes:02}:{display_seconds:02}", True, "white") 
    timer_text_rect = timer_text.get_rect(center=(HEIGHT, WIDTH+SQ_SIZE+36))
    screen.blit(timer_text, timer_text_rect)
    if gameState.whiteToMove:
        FONT = p.font.Font("chess/assets/Montserrat-Bold.ttf", 20)
        Turn = FONT.render("White to Move", True, "white")
        Turn_rect = Turn.get_rect(center=(HEIGHT, WIDTH+2*SQ_SIZE+10))     
        screen.blit(Turn, Turn_rect)
    if not gameState.whiteToMove:
        FONT = p.font.Font("chess/assets/Montserrat-Bold.ttf", 20)
        Turn = FONT.render("Black to Move", True, (82, 79, 76))
        Turn_rect = Turn.get_rect(center=(HEIGHT, WIDTH+2*SQ_SIZE+10))     
        screen.blit(Turn, Turn_rect)
def drawSQNames(screen):
    colors = [p.Color((238,238,210)),p.Color((118,150,86))]
    letters = ['a','b','c','d','e','f','g','h']
    FONT = p.font.Font("chess/assets/Montserrat-SemiBold.ttf", 15)
    for i in range(DIMENSION):
        color = colors[((i)%2)]
        letter = FONT.render(letters[i], True, color)
        letters_rect = letter.get_rect(bottomright=(2*SQ_SIZE-3+SQ_SIZE*i,HEIGHT+SQ_SIZE-3 ))     
        screen.blit(letter, letters_rect)
    num = 1
    for i in range(8,0,-1):
        if num<=8:
            color = colors[((num)%2)]
            nums = FONT.render(f"{i}", True, color)
            nums_rect = nums.get_rect(topleft=(SQ_SIZE+2,SQ_SIZE*num ))     
            screen.blit(nums, nums_rect)
            num = num +1
        else : num = 0
def drawBTNS(screen):
    p.draw.rect(screen,(50,49,47),p.Rect(3*SQ_SIZE-8.5,HEIGHT+SQ_SIZE+15,SQ_SIZE+15,SQ_SIZE-15),0,4)
    p.draw.rect(screen,(50,49,47),p.Rect(30+4*SQ_SIZE-7.5,HEIGHT+SQ_SIZE+15,SQ_SIZE+15,SQ_SIZE-15),0,4)
    p.draw.rect(screen,(50,49,47),p.Rect(SQ_SIZE-7.5+32,HEIGHT+SQ_SIZE+15,SQ_SIZE+15,SQ_SIZE-15),0,4)
def drawTaken(screen,gameState):
    white_pieces = [piece for piece in gameState.taken if piece[0] == 'w']
    black_pieces = [piece for piece in gameState.taken if piece[0] == 'b']
    BG_COLOR = (33,32,30)
    p.draw.rect(screen,BG_COLOR,p.Rect(SQ_SIZE+WIDTH,0 ,SQ_SIZE+WIDTH,SQ_SIZE+HEIGHT))
    for i, piece in enumerate(white_pieces):
        row = i // 5 + 1
        col = i % 5
        screen.blit(p.transform.scale(IMAGES[piece],(40,40)),p.Rect(WIDTH + SQ_SIZE+col*23,row *5*SQ_SIZE,20,20))
    for i, piece in enumerate(black_pieces):
        row = i // 5
        col = i % 5
        screen.blit(p.transform.scale(IMAGES[piece],(40,40)),p.Rect(WIDTH + SQ_SIZE+col*23,row*SQ_SIZE + SQ_SIZE ,20,20))
def drawTxt(screen,text):
    font = p.font.Font("chess/assets/Montserrat-Bold.ttf", 60)
    if text == 'White Wins':
        s = p.Surface((8*SQ_SIZE,8*SQ_SIZE))
        s.fill(p.Color('black'))
        s.set_alpha(100)
        screen.blit(s,(SQ_SIZE,SQ_SIZE))
        textObj = font.render(text,0,p.Color(197,197,196))
        textLoc = p.Rect(0,0,WIDTH+SQ_SIZE,HEIGHT+SQ_SIZE).move((WIDTH+2*SQ_SIZE)/2 - textObj.get_width()/2,(HEIGHT+2*SQ_SIZE)/2-textObj.get_height()/2)
        screen.blit(textObj,textLoc)
    elif text == 'Black Wins':
        s = p.Surface((8*SQ_SIZE,8*SQ_SIZE))
        s.fill(p.Color('white'))
        s.set_alpha(120)
        screen.blit(s,(SQ_SIZE,SQ_SIZE))
        textObj = font.render(text,0,p.Color(50,49,47))
        textLoc = p.Rect(0,0,WIDTH+SQ_SIZE,HEIGHT+SQ_SIZE).move((WIDTH+2*SQ_SIZE)/2 - textObj.get_width()/2,(HEIGHT+2*SQ_SIZE)/2-textObj.get_height()/2)
        screen.blit(textObj,textLoc)
    elif text == 'STOOLMATE,NOONE WIIIIINSSSSS':
        font = p.font.Font("chess/assets/Montserrat-Bold.ttf", 20)
        s = p.Surface((8*SQ_SIZE,8*SQ_SIZE))
        s.fill(p.Color('black'))
        s.set_alpha(120)
        screen.blit(s,(SQ_SIZE,SQ_SIZE))
        textObj = font.render(text,0,p.Color(255,0,244))
        textLoc = p.Rect(0,0,WIDTH+SQ_SIZE,HEIGHT+SQ_SIZE).move((WIDTH+2*SQ_SIZE)/2 - textObj.get_width()/2,(HEIGHT+2*SQ_SIZE)/2-textObj.get_height()/2)
        screen.blit(textObj,textLoc) 
def saveMoveLog(Note):
    moveLog.append(Note)
    print(moveLog)
    
def save():
    moveText = []
    for i in range(0, len(moveLog), 2):
                moveString = str(i // 2 + 1) + '. ' + str(moveLog[i]) 
                if i + 1 < len(moveLog):
                    moveString += " - " + str(moveLog[i + 1]) + " "
                moveText.append(moveString)
    print (moveText)
    textFile = open('chess/saves/save.txt', 'w')
    content  = "\n".join(moveText)
    textFile.writelines(content)
    textFile.close()
if __name__ == "__main__":
    main()
