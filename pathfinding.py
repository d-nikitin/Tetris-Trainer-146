import tetris
import heapq
import copy
# x {-2, 7}
# y {-1 18}



# Falling Piece x,y,r,s
# Placement Piece x,y,r,s

# All neighbor moves
    # For each rotation of falling Piece
    #   For move_left and move_right
    #   For drop

# Has dropped
# Has moved horizontally

# board

# . is blank
# BLANK

'''
shapeToDraw = PIECES[piece['shape']][piece['rotation']]
    if pixelx == None and pixely == None:
        # if pixelx & pixely hasn't been specified, use the location stored in the piece data structure
        pixelx, pixely = convertToPixelCoords(piece['x'], piece['y'])

    # draw each of the boxes that make up the piece
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            if shapeToDraw[y][x] != BLANK:
                if phantomPiece: drawPhantomPiece(piece['color'], pixelx + (x* BOXSIZE), pixely + (y*BOXSIZE))
                else: drawBox(None, None, piece['color'], pixelx + (x * BOXSIZE), pixely + (y * BOXSIZE))
'''
DATA = {
        "height": [],
        "comp": [],
        "moves": [],
        }

def will_clear_line(placement, board):
    tempBoard = copy.deepcopy(board)
    tetris.addToBoard(tempBoard, placement)
    comp_lines = 0
    for y in range(tetris.BOARDHEIGHT):
        if tetris.isCompleteLine(tempBoard, y):
            comp_lines += 1
        DATA.get('comp').append(comp_lines)
    return comp_lines

def pieceToBoard(piece):
    blocks = []
    shapeToDraw = tetris.PIECES[piece['shape']][piece['rotation']]
    for x in range(tetris.TEMPLATEWIDTH):
        for y in range(tetris.TEMPLATEHEIGHT):
            if shapeToDraw[y][x] != tetris.BLANK:
                blocks.append((piece['x'] + x, piece['y'] + y))
    return blocks

def creates_enclosedSpaces(placement, board):
    tempBoard = copy.deepcopy(board)
    tetris.addToBoard(tempBoard, placement)
    if len(getEnclosedSpaces(board)) < len(getEnclosedSpaces(tempBoard)):
        return True
    else: return False

def getEnclosedSpaces(board):
    enclosed_boxes = []
    searched_space = []
    for x in range(0,10):
        for y in range(2,20):
            if board[x][y] == tetris.BLANK and (x,y) not in searched_space:
                unexplored = []
                explored = []
                touched_roof = False
                unexplored.append((x,y))
                while(unexplored):
                    node = unexplored.pop()
                    for neighbor in get_neighbor_cells(board, node[0], node[1]):
                        a = neighbor[0]
                        b = neighbor[1]
                        if board[a][b] == tetris.BLANK and neighbor not in explored:
                            unexplored.append(neighbor)
                        if b <= 1: touched_roof = True
                    explored.append(node)
                    searched_space.append(node)
                if not touched_roof:
                    for node in explored:
                        enclosed_boxes.append(node)
    res = []
    for i in enclosed_boxes:
        if i not in res:
            res.append(i)
    return res

def get_neighbor_cells(board, x, y):
    neighbors = []
    for i in [-1,1]:
        if tetris.isOnBoard(x+i,y):
            neighbors.append((x+i,y))
    for j in [-1,1]:
        if tetris.isOnBoard(x,y+j):
            neighbors.append((x,y+j))
    return neighbors

def strip_enclosed(enclosure_list, placements):
    res = []
    for placement in placements:
        if not is_enclosed(enclosure_list, placement):
            res.append(placement)
    return res

def is_enclosed(enclosure_list, piece):
    blocks = pieceToBoard(piece)
    for block in blocks:
        if block in enclosure_list:
            return True
    return False

def heightAdded(piece, board):
    blocks = pieceToBoard(piece)
    lowest_y = 19
    for x in range(0,10):
        for y in range(2,20):
            if board[x][y] != tetris.BLANK:
                DATA.get("hieght").append(y)
                if y < lowest_y:
                    lowest_y = y

    height_added = -1000
    for block in blocks:
        diff = lowest_y - block[1]
        if diff > height_added:
            height_added = diff
    return height_added

def get_shortestHeight(placements, board):
    minimum_height_index = None
    minimum_height = 500
    for i in range(len(placements)):
        height_added = heightAdded(placements[i], board)
        if height_added < minimum_height:
            minimum_height = height_added
            minimum_height_index = i
    return placements[minimum_height_index]




