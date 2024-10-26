class state():
    def __init__(self):
        self.board = [
            ["bR","bN","bB","bQ","bK","bB","bN","bR"],
            ["bp","bp","bp","bp","bp","bp","bp","bp"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["wp","wp","wp","wp","wp","wp","wp","wp"],
            ["wR","wN","wB","wQ","wK","wB","wN","wR"],
        ]
        # for castling test:
        
        # self.board = [
        #     ["bR","--","--","--","bK","--","--","bR"],
        #     ["bp","bp","bp","bp","bp","bp","bp","bp"],
        #     ["--","--","--","--","--","--","--","--"],
        #     ["--","--","--","--","--","--","--","--"],
        #     ["--","--","--","--","--","--","--","--"],
        #     ["--","--","--","--","--","--","--","--"],
        #     ["wp","wp","wp","wp","wp","wp","wp","wp"],
        #     ["wR","--","--","--","wK","--","--","wR"],
        # ]
        self.movefunc = {'p':self.getPawnMoves,'R':self.getRookMoves,'N':self.getKnightMoves,'B':self.getBishopMoves,'Q':self.getQueenMoves,'K':self.getKingMoves}
        
        self.whiteToMove = True
        self.movelog = []
        self.redolog = []
        self.taken = []
        self.wKingLoc = (7,4)
        self.bKingLoc = (0,4)
        self.inCheck = False
        self.checkMate = False
        self.staleMate = False
        self.pins = []
        self.cheks = []
        self.enPossible = ()
        self.currentCastlingRights = castleRights(True,True,True,True)
        self.castleRightLog = [castleRights(self.currentCastlingRights.wks,self.currentCastlingRights.bks,
                                            self.currentCastlingRights.wqs,self.currentCastlingRights.bqs)]
        
    def makeMove(self,move):
        self.board[move.startRow][move.startCol]= "--" 
        self.board[move.endRow][move.endCol]= move.movedPC 
        self.movelog.append(move)
        self.taken.append(move.capturedPC) if move.capturedPC != "--" else None
        self.redolog = []
        self.whiteToMove = not self.whiteToMove
        if move.movedPC == 'wK':
            self.wKingLoc = (move.endRow,move.endCol)
        elif move.movedPC == 'bK':
            self.bKingLoc = (move.endRow,move.endCol)
        if move.Promotion:
            promoted_piece = input("Promote to Q, R, B, or N:") 
            self.board[move.endRow][move.endCol]= move.movedPC[0] + promoted_piece
        if move.isEnMove:
            self.board[move.startRow][move.endCol]="--"
        if move.movedPC[1] == 'p' and abs(move.startRow - move.endRow)==2:
            self.enPossible = ((move.startRow + move.endRow)//2,move.startCol)
        else : 
            self.enPossible = ()
            
        if move.isCastle:
            if move.endCol - move.startCol == 2 :
                self.board[move.endRow][move.endCol-1] = self.board[move.endRow][move.endCol+1]
                self.board[move.endRow][move.endCol+1] = "--"
            else:
                self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol-2]
                self.board[move.endRow][move.endCol-2] = "--"
        self.updateCastleRights(move)
        self.castleRightLog.append(castleRights(self.currentCastlingRights.wks,self.currentCastlingRights.bks,self.currentCastlingRights.wqs,self.currentCastlingRights.bqs))
    
    
    
    def undo(self):
        if len(self.movelog) != 0:
            move = self.movelog.pop()
            self.redolog.append(move)
            self.board[move.startRow][move.startCol]=move.movedPC
            self.board[move.endRow][move.endCol]=move.capturedPC
            if move.capturedPC in self.taken:
                self.taken.remove(move.capturedPC)
            self.whiteToMove = not self.whiteToMove
            if move.movedPC == 'wK':
                self.wKingLoc = (move.startRow,move.startCol)
            elif move.movedPC == 'bK':
                self.bKingLoc = (move.startRow,move.startCol)
            if move.isEnMove:
                self.board[move.endRow][move.endCol]="--"
                self.board[move.startRow][move.endCol]= move.capturedPC
                self.enPossible = (move.endRow,move.endCol)
            if move.movedPC[1] == 'p' and abs(move.startRow - move.endRow)==2:
                self.enPossible = ()
            
            self.castleRightLog.pop()
            newRights = self.castleRightLog[-1]
            self.currentCastlingRights = castleRights(newRights.wks,newRights.bks,newRights.wqs,newRights.bqs)
            
            if move.isCastle:
                if move.endCol - move.startCol == 2 :
                    self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol-1]
                    self.board[move.endRow][move.endCol-1] = "--"
                else:
                    self.board[move.endRow][move.endCol-2] = self.board[move.endRow][move.endCol+1]
                    self.board[move.endRow][move.endCol+1] = "--"
            
    def redo(self):
        if len(self.redolog)!=0:
            move = self.redolog.pop()
            self.movelog.append(move)
            self.taken.append(move.capturedPC) if move.capturedPC != "--" else None
            self.board[move.startRow][move.startCol]= "--" 
            self.board[move.endRow][move.endCol]= move.movedPC 
            self.whiteToMove = not self.whiteToMove
            if move.movedPC == 'wK':
                self.wKingLoc = (move.endRow,move.endCol)
            elif move.movedPC == 'bK':
                self.bKingLoc = (move.endRow,move.endCol)
            if move.Promotion:
                global promoted_piece
                promoted_piece = input("Promote to Q, R, B, or N:") 
                self.board[move.endRow][move.endCol]= move.movedPC[0] + promoted_piece
            if move.isEnMove:
                self.board[move.startRow][move.endCol]="--"
            if move.movedPC[1] == 'p' and abs(move.startRow - move.endRow)==2:
                self.enPossible = ((move.startRow + move.endRow)//2,move.startCol)
            if move.isCastle:
                if move.endCol - move.startCol == 2 :
                    self.board[move.endRow][move.endCol-1] = self.board[move.endRow][move.endCol+1]
                    self.board[move.endRow][move.endCol+1] = "--"
                else:
                    self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol-2]
                    self.board[move.endRow][move.endCol-2] = "--"
            self.updateCastleRights(move)
            self.castleRightLog.append(castleRights(self.currentCastlingRights.wks,self.currentCastlingRights.bks,self.currentCastlingRights.wqs,self.currentCastlingRights.bqs))
    


    def validMoves(self):
        temp_castle_rights = castleRights(self.currentCastlingRights.wks, self.currentCastlingRights.bks,self.currentCastlingRights.wqs, self.currentCastlingRights.bqs)
        moves = []
        self.inCheck,self.pins,self.cheks = self.ChecksAndPins()
        if self.whiteToMove:
            kingRow = self.wKingLoc[0]
            kingCol = self.wKingLoc[1]
        else:
            kingRow = self.bKingLoc[0]
            kingCol = self.bKingLoc[1]
        if self.inCheck:
            if len(self.cheks)==1:
                moves = self.possibleMoves()
                check = self.cheks[0]
                checkRow = check[0]
                checkCol = check[1]
                pieceChecking = self.board[checkRow][checkCol]
                validSQs = []
                if pieceChecking == 'N':
                    validSQs = [(checkRow,checkCol)]
                else:
                    for i in range(1,8):
                        validSQ = (kingRow + check[2]*i,kingCol + check[3]*i)
                        validSQs.append(validSQ)
                        if validSQ[0] == checkRow and validSQ[1]==checkCol:
                            break
                for i in range(len(moves)-1,-1,-1):
                    if moves[i].movedPC[1] != 'K':
                        if not (moves[i].endRow,moves[i].endCol) in validSQs:
                            moves.remove(moves[i])
            else:
                self.getKingMoves(kingRow,kingCol,moves)
        else:
            moves = self.possibleMoves()
        if self.whiteToMove:
            self.getCastleMoves(self.wKingLoc[0], self.wKingLoc[1], moves)
        else:
            self.getCastleMoves(self.bKingLoc[0], self.bKingLoc[1], moves)

        self.currentCastlingRights = temp_castle_rights
        if len(moves) == 0:
            if self.inCheck:
                self.checkMate = True
            else:
                self.staleMate = True
        else:
            self.checkMate = False
            self.staleMate = False
        return moves                
        
    def possibleMoves(self):
        moves = []
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                turn = self.board[row][col][0]
                if (turn == 'w'and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[row][col][1]
                    self.movefunc[piece](row,col,moves)
        return moves
    def ChecksAndPins(self):
        pins = []
        cheks = []
        inCheck = False
        if self.whiteToMove : 
            enemy = 'b'
            ally = 'w'
            startRow = self.wKingLoc[0]
            startCol = self.wKingLoc[1]
        else:
            enemy = 'w'
            ally = 'b'
            startRow = self.bKingLoc[0]
            startCol = self.bKingLoc[1]
        directions = ((-1,0),(0,-1),(1,0),(0,1),(-1,-1),(-1,1),(1,-1),(1,1))
        for j in range(len(directions)):
            d = directions[j]
            possiblePin = ()
            for i in range(1,8):
                endRow = startRow + d[0]*i
                endCol = startCol + d[1]*i
                if 0<=endRow<=7 and 0<=endCol<=7:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] == ally and endPiece[1] != 'K':
                        if possiblePin == ():
                            possiblePin = (endRow,endCol,d[0],d[1])
                        else:
                            break
                    elif endPiece[0] == enemy:
                        type = endPiece[1]
                        if (0 <= j <= 3 and type == "R") or (4 <= j <= 7 and type == "B") or (
                                i == 1 and type == "p" and (
                                (enemy == "w" and 6 <= j <= 7) or (enemy == "b" and 4 <= j <= 5))) or (
                                type == "Q") or (i == 1 and type == "K"):
                            if possiblePin == ():
                                inCheck = True
                                cheks.append((endRow,endCol,d[0],d[1]))
                                break
                            else:
                                pins.append(possiblePin)
                                break
                        else:
                            break
                else:
                    break
        Knightdirections = ((-2, -1), (-2, 1), (-1, 2), (1, 2), (2, -1), (2, 1), (-1, -2), (1, -2))
        for m in Knightdirections:
            endRow = startRow + m[0]
            endCol = startCol + m[1]
            if 0<=endRow <=7 and 0 <= endCol <=7 :
                endPiece = self.board[endRow][endCol]
                if endPiece[0] ==enemy and endPiece[1]=='N':
                    inCheck = True
                    cheks.append((endRow,endCol,m[0],m[1]))
        return inCheck,pins,cheks

    def getPawnMoves(self,row,col,moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0] == row and self.pins[i][1]== col:
                piecePinned = True
                pinDirection = (self.pins[i][2] ,self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        if self.whiteToMove :
            if self.board[row-1][col]=="--":
                if not piecePinned or pinDirection == (-1,0):
                    moves.append(Move((row,col),(row-1,col),self.board))
                    if row == 6 and self.board[row-2][col] == "--":
                        moves.append(Move((row,col),(row-2,col),self.board))
            if col-1 >= 0:
                if self.board[row-1][col-1][0] == 'b':
                    if not piecePinned or pinDirection == (-1,-1): 
                        moves.append(Move((row,col),(row-1,col-1),self.board))
                elif (row-1,col-1) == self.enPossible:
                    if not piecePinned or pinDirection == (-1,-1): 
                        moves.append(Move((row,col),(row-1,col-1),self.board,enpass=True))
            if col+1 <= 7:
                if self.board[row-1][col+1][0] == 'b':
                    if not piecePinned or pinDirection == (-1,1):
                        moves.append(Move((row,col),(row-1,col+1),self.board))
                elif (row-1,col+1) == self.enPossible:
                    if not piecePinned or pinDirection == (-1,1):
                        moves.append(Move((row,col),(row-1,col+1),self.board,enpass=True))
        else:
            if self.board[row+1][col]=="--":
                if not piecePinned or pinDirection == (-1,0):
                    moves.append(Move((row,col),(row+1,col),self.board))
                    if row == 1 and self.board[row+2][col] == "--":
                        moves.append(Move((row,col),(row+2,col),self.board))
            if col-1 >= 0:
                if self.board[row+1][col-1][0] == 'w':
                    if not piecePinned or pinDirection == (1,-1):
                        moves.append(Move((row,col),(row+1,col-1),self.board))
                elif (row+1,col-1) == self.enPossible:
                    if not piecePinned or pinDirection == (1,-1):
                        moves.append(Move((row,col),(row+1,col-1),self.board,enpass=True))
            if col+1 <= 7:
                if self.board[row+1][col+1][0] == 'w':
                    if not piecePinned or pinDirection == (1,1):
                        moves.append(Move((row,col),(row+1,col+1),self.board))
                elif (row+1,col+1) == self.enPossible:
                    if not piecePinned or pinDirection == (1,1):
                        moves.append(Move((row,col),(row+1,col+1),self.board,enpass=True))

    def getRookMoves(self,row,col,moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0] == row and self.pins[i][1]== col:
                piecePinned = True
                pinDirection = (self.pins[i][2] ,self.pins[i][3])
                if self.board[row][col][1]!='Q':
                    self.pins.remove(self.pins[i])
                break
        directions = ((-1,0),(0,-1),(1,0),(0,1))
        enemy = 'b' if self.whiteToMove else 'w'
        for d in directions:
            for i in range(1,8):
                endrow = row + d[0]*i
                endcol = col + d[1]*i
                if 0 <= endrow <8 and 0<=endcol<8:
                    if not piecePinned or pinDirection ==d or pinDirection == (-d[0],-d[1]):
                        endPiece = self.board[endrow][endcol]
                        if endPiece == "--":
                            moves.append(Move((row,col),(endrow,endcol),self.board))
                        elif endPiece[0] == enemy:
                            moves.append(Move((row,col),(endrow,endcol),self.board))
                            break
                        else:
                            break
                else:
                    break

    def getKnightMoves(self,row,col,moves):
        piecePinned = False
        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0] == row and self.pins[i][1]== col:
                piecePinned = True
                self.pins.remove(self.pins[i])
                break
        directions = ((-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1))
        ally = 'w' if self.whiteToMove else 'b'
        for d in directions:
            endrow = row + d[0]
            endcol = col + d[1]
            if 0<= endrow < 8 and 0<=endcol<8:
                if not piecePinned:
                    endPiece = self.board[endrow][endcol]
                    if endPiece[0] != ally:
                        moves.append(Move((row,col),(endrow,endcol),self.board))

    def getBishopMoves(self,row,col,moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0] == row and self.pins[i][1]== col:
                piecePinned = True
                pinDirection = (self.pins[i][2] ,self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        directions = ((-1,-1),(-1,1),(1,-1),(1,1))
        enemy = 'b' if self.whiteToMove else 'w'
        for d in directions:
            for i in range(1,8):
                endrow = row + d[0]*i
                endcol = col + d[1]*i
                if 0 <= endrow <8 and 0<=endcol<8:
                    if not piecePinned or pinDirection ==d or pinDirection == (-d[0],-d[1]):
                        endPiece = self.board[endrow][endcol]
                        if endPiece == "--":
                            moves.append(Move((row,col),(endrow,endcol),self.board))
                        elif endPiece[0] == enemy:
                            moves.append(Move((row,col),(endrow,endcol),self.board))
                            break
                        else:
                            break
                else:
                    break
    
    def getQueenMoves(self,row,col,moves):
        self.getBishopMoves(row,col,moves)
        self.getRookMoves(row,col,moves)
    
    def getKingMoves(self,row,col,moves):
        rowMoves = (-1,-1,-1,0,0,1,1,1)
        colMoves = (-1,0,1,-1,1,-1,0,1)
        ally = 'w' if self.whiteToMove else 'b'
        for i in range(8):
            endrow = row+rowMoves[i]
            endcol = col+colMoves[i]
            if 0<=endrow<8 and 0<=endcol<8:
                endPiece = self.board[endrow][endcol]
                if endPiece[0]!= ally:
                    if ally == 'w':
                        self.wKingLoc = (endrow,endcol)
                    else:
                        self.bKingLoc = (endrow,endcol)
                    inCheck , pins,checks = self.ChecksAndPins()
                    if not inCheck:
                        moves.append(Move((row,col),(endrow,endcol),self.board))
                    if ally == 'w':
                        self.wKingLoc = (row,col)
                    else:
                        self.bKingLoc = (row,col)
    
    
    def in_Check(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.wKingLoc[0], self.wKingLoc[1])
        else:
            return self.squareUnderAttack(self.bKingLoc[0], self.bKingLoc[1])

    def squareUnderAttack(self, row, col):
        self.whiteToMove = not self.whiteToMove  
        opponents_moves = self.possibleMoves()
        self.whiteToMove = not self.whiteToMove
        for move in opponents_moves:
            if move.endRow == row and move.endCol == col:
                return True
        return False
    
    def updateCastleRights(self,move):
        if move.movedPC == 'wK':
            self.currentCastlingRights.wks = False
            self.currentCastlingRights.wqs = False
        elif move.movedPC == 'bK':
            self.currentCastlingRights.bks = False
            self.currentCastlingRights.bqs = False
        elif move.movedPC == 'wR':
            if move.startRow == 7:
                if move.startCol == 0:
                    self.currentCastlingRights.wqs = False
                elif move.startCol == 7:
                    self.currentCastlingRights.wks = False
        elif move.movedPC == 'bR':
            if move.startRow == 0:
                if move.startCol == 0:
                    self.currentCastlingRights.bqs = False
                elif move.startCol == 7:
                    self.currentCastlingRights.bks = False
                    
    def getCastleMoves(self,r,c,moves):
        if self.squareUnderAttack(r,c):
            return
        if (self.whiteToMove and self.currentCastlingRights.wks) or (not self.whiteToMove and self.currentCastlingRights.bks):
            self.getKSCMoves(r,c,moves)
        if (self.whiteToMove and self.currentCastlingRights.wqs) or (not self.whiteToMove and self.currentCastlingRights.bqs):
            self.getQSCMoves(r,c,moves) 
        
    def getKSCMoves(self,row,col,moves):
        if self.board[row][col + 1] == '--' and self.board[row][col + 2] == '--':
            if not self.squareUnderAttack(row, col + 1) and not self.squareUnderAttack(row, col + 2):
                moves.append(Move((row, col), (row, col + 2), self.board, isCastle=True))
    
    def getQSCMoves(self,row,col,moves):
        if self.board[row][col - 1] == '--' and self.board[row][col - 2] == '--' and self.board[row][col - 3] == '--':
            if not self.squareUnderAttack(row, col - 1) and not self.squareUnderAttack(row, col - 2):
                moves.append(Move((row, col), (row, col - 2), self.board, isCastle=True))

class castleRights():
    def __init__(self,wks,bks,wqs,bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs
        

class Move(): 
    ranksToRows = {"1":7,"2":6,"3":5,"4":4,"5":3,"6":2,"7":1,"8":0}
    rowsToRanks = {v: k for k,v in ranksToRows.items()}
    filesToCols = {"a":0,"b":1,"c":2,"d":3,"e":4,"f":5,"g":6,"h":7}
    colsToFiles = {v:k for k,v in filesToCols.items()}
    
    def __init__(self, startSQ, endSQ, board,enpass=False,isCastle=False):
        self.startRow = startSQ[0] 
        self.startCol = startSQ[1] 
        self.endRow = endSQ[0] 
        self.endCol = endSQ[1] 
        self.movedPC = board[self.startRow][self.startCol] 
        self.capturedPC = board[self.endRow][self.endCol]  
        self.Promotion = ((self.movedPC == 'wp' and self.endRow == 0) or (self.movedPC == 'bp'and self.endRow == 7))
        self.isEnMove = enpass
        self.isCastle = isCastle
        self.isCapture = self.capturedPC != "--"
        if self.isEnMove : 
            self.capturedPC = 'wp' if self.movedPC == 'bp' else 'bp'
        self.moveID = self.startRow * 1000 + self.startCol *100 + self.endRow*10+self.endCol
    
    def Notation(self):
        endsq = self.RankFile(self.endRow,self.endCol)
        if self.movedPC[1] == "p":
            if self.isCapture or (abs(self.startRow - self.endRow)==1 and abs(self.startCol - self.endCol)==1 ):
                if state().inCheck:
                    return self.colsToFiles[self.startCol] + "x" + endsq+"+"
                else :
                    return self.colsToFiles[self.startCol] + "x" + endsq
            else:
                return endsq + promoted_piece if self.Promotion else endsq
        move_string = self.movedPC[1]
        if self.isCapture:
            if state().inCheck:
                move_string += "x"
                return move_string + endsq +"+"
            else:
                move_string += "x"
        if state().inCheck:
            return move_string + endsq+'+'
        
        elif self.movedPC[1] == 'K' and abs(self.endCol - self.startCol) == 2:
            if self.endCol == 2:
                return "0-0-0"
            else:
                return "0-0"
            
        print(state().inCheck)
        return move_string + endsq
    
    def __eq__(self, other):
        if isinstance(other,Move):
            return self.moveID == other.moveID
        return False
    
    

    
    def RankFile(self,row,col):
        return self.colsToFiles[col]+self.rowsToRanks[row]