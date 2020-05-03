#!/usr/bin/env python3

import os

board = [
    [0, 0, 1, 1, 1, 0, 0],
    [0, 0, 1, 1, 1, 0, 0],
    [1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 2, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1],
    [0, 0, 1, 1, 1, 0, 0],
    [0, 0, 1, 1, 1, 0, 0]
    ]

goal = [
    [0, 0, 2, 2, 2, 0, 0],
    [0, 0, 2, 2, 2, 0, 0],
    [2, 2, 2, 2, 2, 2, 2],
    [2, 2, 2, 1, 2, 2, 2],
    [2, 2, 2, 2, 2, 2, 2],
    [0, 0, 2, 2, 2, 0, 0],
    [0, 0, 2, 2, 2, 0, 0]
    ]

solutions = []

class Node(object):
    def __init__(self, parent):
        self.parent = parent
        self.move = None
        self.depth = None
        self.children = []
    def getSequence(self):
        node = self
        sequence = []
        while(node.parent.move != None):
            sequence.append(node.move)
            node = node.parent
        sequence.reverse()
        return sequence
    def addChild(self, move):
        child = Node(self)
        child.move = move
        self.children.append(child)
    def process(self):
        global board
        global solutions
        board = move(board, self.move)
        self.depth = len(self.getSequence())
        if board == goal:
            print('Solution found:')
            print(seqToString(self.getSequence()))
            solutions.append([self.getSequence()])
            printBoard(board)
            return True
        avails = availableMoves(board)
        for avail in avails:
            self.addChild(avail)
        for i in range(len(self.children)):
            self.children[i].process()
        board = reverseMove(board, self.move)


def printBoard(board):
    print()
    print('    A  B  C  D  E  F  G ')
    i = 1
    for line in board:
        lineStr = ' ' + str(i) + ' '
        for cell in line:
            if cell == 0:
                lineStr += '   '
            elif cell == 1:
                lineStr += ' ● '
            elif cell == 2:
                lineStr += ' ○ '
        print(lineStr)
        i+=1
    print()

def availableMoves(board):
    dirs = [(0,1), (0,-1), (1,0), (-1,0)]
    l = len(board)
    moves = []
    for y in range(l):
        for x in range(l):
            for d in dirs:
                if 0 <= x+2*d[0] < l and 0 <= y+2*d[1] < l:
                    if board[y][x] == 1 and board[y+d[1]][x+d[0]] == 1 and board[y+2*d[1]][x+2*d[0]] == 2:
                        moves.append((d, x, y))
                
    return moves 

def moveAux(board, move, p1, p2, p3):
    d = move[0]
    x = move[1]
    y = move[2]
    
    board[y][x] = p1
    board[y+d[1]][x+d[0]] = p2
    board[y+2*d[1]][x+2*d[0]] = p3

    return board

def move(board, move):
    board = moveAux(board, move, 2, 2, 1)
    return board

def reverseMove(board, move):
    board = moveAux(board, move, 1, 1, 2)
    return board

def moveToString(move):
    dirs = [[" ↑"," ↓"," ↑"],[" →"],[" ←"]]
    column = {
        0: "A ",
        1: "B ",
        2: "C ",
        3: "D ",
        4: "E ",
        5: "F ",
        6: "G "
    }
    return column[move[1]] + str(move[2]+1) + dirs[move[0][0]][move[0][1]]

def seqToString(seq):
    seqStr = ""
    for move in seq:
        seqStr += moveToString(move) + ', '
    return seqStr[:-2]
        

def manualAux(board, moveSeq):
    os.system('clear')
    moveSeqStr = ''
    for moveDone in moveSeq:
        moveSeqStr += moveToString(moveDone) + ', '
    print(moveSeqStr[:-2])
    printBoard(board)
    i = 0
    avail = availableMoves(board)
    print('0. undo')
    for moveToDo in avail:
        i+=1
        print(str(i) + '. ' + moveToString(moveToDo))
    sel = input()
    if sel == '0':
        undo = moveSeq.pop()
        return reverseMove(board, undo), 0
    return move(board, avail[int(sel) - 1]), avail[int(sel) - 1]

def manual(board):
    moveSeq = []
    gameOver = False
    while not gameOver:
        board,movePrev = manualAux(board, moveSeq)
        if movePrev != 0:
            moveSeq.append(movePrev)
        if board == goal:
            gameOver = True
    print('well done!')
    printBoard(board)


def auto(board):
    tree = Node(None)
    tree.board = board
    avails = availableMoves(board)
    avails.reverse()
    for avail in avails:
        tree.addChild(avail)
    for child in tree.children:
        child.process()


#manual(board)
#stdscr = curses.initscr()
auto(board)
