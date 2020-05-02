#!/usr/bin/env python3

import numpy
import os
import gc
import curses


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

class Node(object):
    def __init__(self, parent):
        self.board = None
        self.parent = parent
        self.board = None
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
        self.board = self.parent.board
        #printBoard(self.board)
        #print(self.getSequence())
        self.board = move(self.board, self.move)
        self.depth = len(self.getSequence())
        if self.board == goal:
            print('i think we won')
            printBoard(self.board)
            test = input()
        avails = availableMoves(self.board)
        for avail in avails:
            self.addChild(avail)
        for i in range(len(self.children)):
            stdscr.addstr(self.depth, self.depth, str(i+1) + '/' + str(len(self.children)))
            stdscr.refresh()
            self.children[i].process()
        stdscr.addstr(self.depth, self.depth, '                                      ')
        stdscr.refresh()
        gc.collect()
        del self


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


def availableMoves1d(board, d):
    indexes = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j:j+3] == [2, 1, 1]:
                indexes.append((d, i, j))
    return indexes

def availableMoves(board):
    moves = []
    moves += availableMoves1d(board, 0)
    moves += availableMoves1d(numpy.transpose(numpy.matrix(board)).tolist(), 1)
    moves += availableMoves1d(numpy.flip(numpy.matrix(board)).tolist(), 2)
    moves += availableMoves1d(numpy.flip(numpy.transpose(numpy.matrix(board))).tolist(), 3)
    return moves

def move(board, move):
    if move[0] == 0:
        boardTmp = board
    elif move[0] == 1:
        boardTmp = numpy.transpose(numpy.matrix(board)).tolist()
    elif move[0] == 2:
        boardTmp = numpy.flip(numpy.matrix(board)).tolist()
    elif move[0] == 3:
        boardTmp = numpy.flip(numpy.transpose(numpy.matrix(board))).tolist()

    y = move[1]
    x = move[2]

    boardTmp[y][x] = 1
    boardTmp[y][x+1] = 2
    boardTmp[y][x+2] = 2

    if move[0] == 0:
        board = boardTmp
    elif move[0] == 1:
        board = numpy.transpose(numpy.matrix(boardTmp)).tolist()
    elif move[0] == 2:
        board = numpy.flip(numpy.matrix(boardTmp)).tolist()
    elif move[0] == 3:
        board = numpy.flip(numpy.transpose(numpy.matrix(boardTmp))).tolist()

    return board

def reverseMove(board, move):
    if move[0] == 0:
        boardTmp = board
    elif move[0] == 1:
        boardTmp = numpy.transpose(numpy.matrix(board)).tolist()
    elif move[0] == 2:
        boardTmp = numpy.flip(numpy.matrix(board)).tolist()
    elif move[0] == 3:
        boardTmp = numpy.flip(numpy.transpose(numpy.matrix(board))).tolist()

    y = move[1]
    x = move[2]

    boardTmp[y][x] = 2
    boardTmp[y][x+1] = 1
    boardTmp[y][x+2] = 1

    if move[0] == 0:
        board = boardTmp
    elif move[0] == 1:
        board = numpy.transpose(numpy.matrix(boardTmp)).tolist()
    elif move[0] == 2:
        board = numpy.flip(numpy.matrix(boardTmp)).tolist()
    elif move[0] == 3:
        board = numpy.flip(numpy.transpose(numpy.matrix(boardTmp))).tolist()

    return board

"""
def nextMove(board, triedMoves, moveSeq):
    print(moveSeq)
    print(triedMoves)
    printBoard(board)
    availMoves = availableMoves(board)
    if len(availMoves) == 0:
        print('NO MORE AVAILABLE MOVES')
        failed = moveSeq.pop()
        board = reverseMove(board, failed)
        triedMoves.append(failed)
        return
    counter = 0
    for i in range(len(availMoves)):
        if availMoves[i] in triedMoves:
            counter += 1
            continue
        board = move(board, availMoves[i])
        if board == goal:
            print('WIN')
            return
        nextMove(board, [], moveSeq + [availMoves[i]])
    if i == counter:
        print('TRIED ALL THE MOVES')
        failed = moveSeq.pop()
        board = reverseMove(board, failed)
        triedMoves.append(failed)
        return
    print('NOT SURE')
    return
"""


def moveToString(move):
    direction = {
        0: " ←",
        1: " ↑",
        2: " →",
        3: " ↓"
    }
    column = {
        0: "A ",
        1: "B ",
        2: "C ",
        3: "D ",
        4: "E ",
        5: "F ",
        6: "G "
    }

    if move[0] == 0:
        return column[move[2]+2] + str(move[1]+1) + direction[move[0]]
    elif move[0] == 1:
        return column[move[1]] + str(move[2]+1+2) + direction[move[0]]
    elif move[0] == 2:
        return column[6-move[2]-2] + str(6-move[1]+1) + direction[move[0]]
    elif move[0] == 3:
        return column[6-move[1]] + str(6-move[2]+1-2) + direction[move[0]]



#print(board)
#print(numpy.transpose(board))

#nextMove(board, [], [])

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


manual(board)
#stdscr = curses.initscr()
#auto(board)
