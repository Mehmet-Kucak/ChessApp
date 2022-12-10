from MathX import Vector2
import copy


board = [["BR", "BN", "BB", "BQ", "BK", "BB", "BN", "BR"],
         ["BP", "BP", "BP", "BP", "BP", "BP", "BP", "BP"],
         ["--", "--", "--", "--", "--", "--", "--", "--"],
         ["--", "--", "--", "--", "--", "--", "--", "--"],
         ["--", "--", "--", "--", "--", "--", "--", "--"],
         ["--", "--", "--", "--", "--", "--", "--", "--"],
         ["WP", "WP", "WP", "WP", "WP", "WP", "WP", "WP"],
         ["WR", "WN", "WB", "WQ", "WK", "WB", "WN", "WR"]]
turn = "W"
wkMoved = False
bkMoved = False

"""
TODO:
Fix castling
Add ui with kivy
Try sockets
"""

class tColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def boardToText(_board: [[str]] = board) -> str:
    text = ""

    pieces = getPieces("W" if turn == "B" else "B", _board)
    poses = []
    for i in pieces:
        if canGo(i, findValue(turn + "K", _board), _board):
            poses.append(i)

    for i in range(8):
        text += str(8 - i) + "|"
        for j in range(8):
            pos = Vector2(j, 7 - i)
            if pos in poses:
                text += tColors.FAIL
            text += _board[i][j]
            if pos in poses:
                text += tColors.ENDC
            text += "|" if j == 7 else " "

        text += "\n"
    text += "  aa bb cc dd ee ff gg hh "

    return text


def getValue(position: Vector2, _board: [[str]] = board) -> str:
    return _board[int(7 - position.y)][int(position.x)]


def setValue(position: Vector2, value: str, _board: [[str]] = board):
    _board[int(7 - position.y)][int(position.x)] = value


def changePos(start: Vector2, end: Vector2, _board: [[str]] = board, main_move=False):
    global wkMoved
    global bkMoved

    if getValue(start, _board) == "WP" and end.y == 7:
        setValue(end, "WQ", _board)
    elif getValue(start, _board) == "BP" and end.y == 0:
        setValue(end, "BQ", _board)
    elif getValue(start, _board) == "WK" and (not wkMoved) and (end == Vector2(6, 0) or end == Vector2(2, 0)):
        if end == Vector2(6, 0):
            setValue(end, "WK", _board)
            setValue(Vector2(5, 0), "WR", _board)
            setValue(Vector2(7, 0), "--", _board)
        elif end == Vector2(2, 0):
            setValue(end, "WK", _board)
            setValue(Vector2(3, 0), "WR", _board)
            setValue(Vector2(0, 0), "--", _board)
    elif getValue(start, _board) == "BK" and (not bkMoved) and (end == Vector2(6, 7) or end == Vector2(2, 7)):
        if end == Vector2(6, 7):
            setValue(end, "BK", _board)
            setValue(Vector2(5, 7), "BR", _board)
            setValue(Vector2(7, 7), "--", _board)
        elif end == Vector2(2, 7):
            setValue(end, "BK", _board)
            setValue(Vector2(3, 7), "BR", _board)
            setValue(Vector2(0, 7), "--", _board)
    else:
        setValue(end, getValue(start, _board), _board)
    setValue(start, "--", _board)
    if getValue(end, _board)[1] == "K" and main_move:
        if getValue(end, _board)[0] == "W":
            wkMoved = True
        else:
            bkMoved = True


def changeTurn():
    global turn
    turn = "W" if turn == "B" else "B"


def move(start: Vector2, end: Vector2):
    can_move, reason = canMove(start, end)
    if not can_move:
        print(reason)
    else:
        changePos(start, end, board, True)
        print("\n")
        changeTurn()
        print(boardToText() + "\n")


def canMove(start: Vector2, end: Vector2) -> (bool, str):  # bool=if piece can move, str=reason why piece cant move
    piece = getValue(start)
    if piece[0] != turn:
        return False, "The opponent's turn."
    if piece == "--":
        return False, "Square is empty."
    if not canGo(start, end, board):
        return False, "Invalid move."

    newBoard = copy.deepcopy(board)
    changePos(start, end, newBoard)

    pieces = getPieces("W" if turn == "B" else "B", newBoard)
    check = False
    for i in pieces:
        if canGo(i, findValue(turn + "K", newBoard), newBoard):
            check = True
            break

    if check:
        return False, "The king is under attack."

    return True, ""


# Differences between canMove and canGo is canMove checks if there is a check and if its the wrong turn.
# canGo only checks if piece can go to to destination.
def canGo(start: Vector2, _board: [[str]], checkr=False) -> [Vector2]:
    piece = getValue(start)
    pm = []

    if piece == "--":
        return pm
    if piece[1] == "P":
        if piece[0] == "W":
            if start.y != 7:
                if getValue(start + Vector2(0, 1), _board) == "--":
                    pm.append(start + Vector2(0, 1))
                    if start.y == 1 and getValue(start + Vector2(0, 2), _board) == "--":
                        pm.append(start + Vector2(0, 2))
                if start.x != 0:
                    if getValue(start + Vector2(-1, 1), _board)[0] == "B":
                        pm.append(start + Vector2(-1, 1))
                if start.x != 7:
                    if getValue(start + Vector2(1, 1), _board)[0] == "B":
                        pm.append(start + Vector2(1, 1))

        else:
            if start.y != 0:
                if getValue(start + Vector2(0, -1), _board) == "--":
                    pm.append(start + Vector2(0, -1))
                    if start.y == 6 and getValue(start + Vector2(0, -2), _board) == "--":
                        pm.append(start + Vector2(0, -2))
                if start.x != 0:
                    if getValue(start + Vector2(-1, -1), _board)[0] == "W":
                        pm.append(start + Vector2(-1, -1))
                if start.x != 7:
                    if getValue(start + Vector2(1, -1), _board)[0] == "W":
                        pm.append(start + Vector2(1, -1))
    elif piece[1] == "R":
        # Up
        if start.y != 7:
            for y1 in range(start.y + 1, 8):
                if getValue(Vector2(start.x, y1), _board) == "--":
                    pm.append(Vector2(start.x, y1))
                elif getValue(Vector2(start.x, y1), _board)[0] != piece[0]:
                    pm.append(Vector2(start.x, y1))
                    break
                else:
                    break

        # Down
        if start.y != 0:
            for y2 in range(start.y - 1, -1, -1):
                if getValue(Vector2(start.x, y2), _board) == "--":
                    pm.append(Vector2(start.x, y2))
                elif getValue(Vector2(start.x, y2), _board)[0] != piece[0]:
                    pm.append(Vector2(start.x, y2))
                    break
                else:
                    break

        # Right
        if start.x != 7:
            for x1 in range(start.x + 1, 8):
                if getValue(Vector2(x1, start.y), _board) == "--":
                    pm.append(Vector2(x1, start.y))
                elif getValue(Vector2(x1, start.y), _board)[0] != piece[0]:
                    pm.append(Vector2(x1, start.y))
                    break
                else:
                    break

        # Left
        if start.x != 0:
            for x2 in range(start.x - 1, -1, -1):
                if getValue(Vector2(x2, start.y), _board) == "--":
                    pm.append(Vector2(x2, start.y))
                elif getValue(Vector2(x2, start.y), _board)[0] != piece[0]:
                    pm.append(Vector2(x2, start.y))
                    break
                else:
                    break
    elif piece[1] == "N":
        pos = start + Vector2(-1, 2)
        if -1 < pos.x < 8 and -1 < pos.y < 8:
            if getValue(pos, _board)[0] != piece[0]:
                pm.append(pos)

        pos = start + Vector2(1, 2)
        if -1 < pos.x < 8 and -1 < pos.y < 8:
            if getValue(pos, _board)[0] != piece[0]:
                pm.append(pos)

        pos = start + Vector2(-2, 1)
        if -1 < pos.x < 8 and -1 < pos.y < 8:
            if getValue(pos, _board)[0] != piece[0]:
                pm.append(pos)

        pos = start + Vector2(2, 1)
        if -1 < pos.x < 8 and -1 < pos.y < 8:
            if getValue(pos, _board)[0] != piece[0]:
                pm.append(pos)

        pos = start + Vector2(-2, -1)
        if -1 < pos.x < 8 and -1 < pos.y < 8:
            if getValue(pos, _board)[0] != piece[0]:
                pm.append(pos)

        pos = start + Vector2(2, -1)
        if -1 < pos.x < 8 and -1 < pos.y < 8:
            if getValue(pos, _board)[0] != piece[0]:
                pm.append(pos)

        pos = start + Vector2(-1, -2)
        if -1 < pos.x < 8 and -1 < pos.y < 8:
            if getValue(pos, _board)[0] != piece[0]:
                pm.append(pos)

        pos = start + Vector2(1, -2)
        if -1 < pos.x < 8 and -1 < pos.y < 8:
            if getValue(pos, _board)[0] != piece[0]:
                pm.append(pos)
    elif piece[1] == "B":
        # Top Right
        for i1 in range(1, 8):
            pos = start + Vector2(i1, i1)
            if pos.x > 7 or pos.y > 7:
                break
            elif getValue(pos, _board) == "--":
                pm.append(pos)
            elif getValue(pos, _board)[0] != piece[0]:
                pm.append(pos)
                break
            else:
                break

        # Top Left
        for i2 in range(1, 8):
            pos = start + Vector2(-i2, i2)
            if pos.x < 0 or pos.y > 7:
                break
            elif getValue(pos, _board) == "--":
                pm.append(pos)
            elif getValue(pos, _board)[0] != piece[0]:
                pm.append(pos)
                break
            else:
                break

        # Bottom Right
        for i3 in range(1, 8):
            pos = start + Vector2(i3, -i3)
            if pos.x > 7 or pos.y < 0:
                break
            elif getValue(pos, _board) == "--":
                pm.append(pos)
            elif getValue(pos, _board)[0] != piece[0]:
                pm.append(pos)
                break
            else:
                break

        # Bottom Left
        for i4 in range(1, 8):
            pos = start + Vector2(-i4, -i4)
            if pos.x < 0 or pos.y < 0:
                break
            elif getValue(pos, _board) == "--":
                pm.append(pos)
            elif getValue(pos, _board)[0] != piece[0]:
                pm.append(pos)
                break
            else:
                break
    elif piece[1] == "Q":
        # Up
        if start.y != 7:
            for y1 in range(start.y + 1, 8):
                if getValue(Vector2(start.x, y1), _board) == "--":
                    pm.append(Vector2(start.x, y1))
                elif getValue(Vector2(start.x, y1), _board)[0] != piece[0]:
                    pm.append(Vector2(start.x, y1))
                    break
                else:
                    break

        # Down
        if start.y != 0:
            for y2 in range(start.y - 1, -1, -1):
                if getValue(Vector2(start.x, y2), _board) == "--":
                    pm.append(Vector2(start.x, y2))
                elif getValue(Vector2(start.x, y2), _board)[0] != piece[0]:
                    pm.append(Vector2(start.x, y2))
                    break
                else:
                    break

        # Right
        if start.x != 7:
            for x1 in range(start.x + 1, 8):
                if getValue(Vector2(x1, start.y), _board) == "--":
                    pm.append(Vector2(x1, start.y))
                elif getValue(Vector2(x1, start.y), _board)[0] != piece[0]:
                    pm.append(Vector2(x1, start.y))
                    break
                else:
                    break

        # Left
        if start.x != 0:
            for x2 in range(start.x - 1, -1, -1):
                if getValue(Vector2(x2, start.y), _board) == "--":
                    pm.append(Vector2(x2, start.y))
                elif getValue(Vector2(x2, start.y), _board)[0] != piece[0]:
                    pm.append(Vector2(x2, start.y))
                    break
                else:
                    break

        # Top Right
        for i1 in range(1, 8):
            pos = start + Vector2(i1, i1)
            if pos.x > 7 or pos.y > 7:
                break
            elif getValue(pos, _board) == "--":
                pm.append(pos)
            elif getValue(pos, _board)[0] != piece[0]:
                pm.append(pos)
                break
            else:
                break

        # Top Left
        for i2 in range(1, 8):
            pos = start + Vector2(-i2, i2)
            if pos.x < 0 or pos.y > 7:
                break
            elif getValue(pos, _board) == "--":
                pm.append(pos)
            elif getValue(pos, _board)[0] != piece[0]:
                pm.append(pos)
                break
            else:
                break

        # Bottom Right
        for i3 in range(1, 8):
            pos = start + Vector2(i3, -i3)
            if pos.x > 7 or pos.y < 0:
                break
            elif getValue(pos, _board) == "--":
                pm.append(pos)
            elif getValue(pos, _board)[0] != piece[0]:
                pm.append(pos)
                break
            else:
                break

        # Bottom Left
        for i4 in range(1, 8):
            pos = start + Vector2(-i4, -i4)
            if pos.x < 0 or pos.y < 0:
                break
            elif getValue(pos, _board) == "--":
                pm.append(pos)
            elif getValue(pos, _board)[0] != piece[0]:
                pm.append(pos)
                break
            else:
                break
    elif piece[1] == "K":
        pos = start + Vector2(-1, 1)
        if -1 < pos.x < 8 and -1 < pos.y < 8:
            if getValue(pos, _board)[0] != piece[0]:
                pm.append(pos)
        pos = start + Vector2(0, 1)
        if -1 < pos.x < 8 and -1 < pos.y < 8:
            if getValue(pos, _board)[0] != piece[0]:
                pm.append(pos)
        pos = start + Vector2(1, 1)
        if -1 < pos.x < 8 and -1 < pos.y < 8:
            if getValue(pos, _board)[0] != piece[0]:
                pm.append(pos)
        pos = start + Vector2(-1, 0)
        if -1 < pos.x < 8 and -1 < pos.y < 8:
            if getValue(pos, _board)[0] != piece[0]:
                pm.append(pos)
        pos = start + Vector2(1, 0)
        if -1 < pos.x < 8 and -1 < pos.y < 8:
            if getValue(pos, _board)[0] != piece[0]:
                pm.append(pos)
        pos = start + Vector2(-1, -1)
        if -1 < pos.x < 8 and -1 < pos.y < 8:
            if getValue(pos, _board)[0] != piece[0]:
                pm.append(pos)
        pos = start + Vector2(0, -1)
        if -1 < pos.x < 8 and -1 < pos.y < 8:
            if getValue(pos, _board)[0] != piece[0]:
                pm.append(pos)
        pos = start + Vector2(1, -1)
        if -1 < pos.x < 8 and -1 < pos.y < 8:
            if getValue(pos, _board)[0] != piece[0]:
                pm.append(pos)

        if not checkr:
            pieces = getPieces("W" if piece[0] == "B" else "B", _board)
            check = False
            for i in pieces:
                if canGo(i, findValue(turn + "K", _board), _board, True):
                    check = True
                    break

            if piece[0] == "W":
                if not wkMoved and not check:
                    if getValue(Vector2(5, 0)) == "--" and getValue(Vector2(6, 0)) == "--" and getValue(
                            Vector2(7, 0)) == "WR":
                        pm.append(Vector2(6, 0))
                    if getValue(Vector2(3, 0)) == "--" and getValue(Vector2(2, 0)) == "--" and getValue(
                            Vector2(1, 0)) == "--" and getValue(Vector2(0, 0)) == "WR":
                        pm.append(Vector2(2, 0))

            if piece[0] == "B":
                print(bkMoved, check)
                if not bkMoved and not check:
                    if getValue(Vector2(5, 7)) == "--" and getValue(Vector2(6, 7)) == "--" and getValue(
                            Vector2(7, 7)) == "BR":
                        pm.append(Vector2(6, 7))
                    if getValue(Vector2(3, 7)) == "--" and getValue(Vector2(2, 7)) == "--" and getValue(
                            Vector2(1, 7)) == "--" and getValue(Vector2(0, 7)) == "BR":
                        pm.append(Vector2(2, 7))

    return pm


def canGo(start: Vector2, end: Vector2, _board: [[str]], checkr=False) -> [Vector2]:
    piece = getValue(start)
    pm = []

    if piece == "--":
        return pm
    if piece[1] == "P":
        if piece[0] == "W":
            if start.y != 7:
                if getValue(start + Vector2(0, 1), _board) == "--":
                    pm.append(start + Vector2(0, 1))
                    if start.y == 1 and getValue(start + Vector2(0, 2), _board) == "--":
                        pm.append(start + Vector2(0, 2))
                if start.x != 0:
                    if getValue(start + Vector2(-1, 1), _board)[0] == "B":
                        pm.append(start + Vector2(-1, 1))
                if start.x != 7:
                    if getValue(start + Vector2(1, 1), _board)[0] == "B":
                        pm.append(start + Vector2(1, 1))

        else:
            if start.y != 0:
                if getValue(start + Vector2(0, -1), _board) == "--":
                    pm.append(start + Vector2(0, -1))
                    if start.y == 6 and getValue(start + Vector2(0, -2), _board) == "--":
                        pm.append(start + Vector2(0, -2))
                if start.x != 0:
                    if getValue(start + Vector2(-1, -1), _board)[0] == "W":
                        pm.append(start + Vector2(-1, -1))
                if start.x != 7:
                    if getValue(start + Vector2(1, -1), _board)[0] == "W":
                        pm.append(start + Vector2(1, -1))
    elif piece[1] == "R":
        # Up
        if start.y != 7:
            for y1 in range(start.y + 1, 8):
                if getValue(Vector2(start.x, y1), _board) == "--":
                    pm.append(Vector2(start.x, y1))
                elif getValue(Vector2(start.x, y1), _board)[0] != piece[0]:
                    pm.append(Vector2(start.x, y1))
                    break
                else:
                    break

        # Down
        if start.y != 0:
            for y2 in range(start.y - 1, -1, -1):
                if getValue(Vector2(start.x, y2), _board) == "--":
                    pm.append(Vector2(start.x, y2))
                elif getValue(Vector2(start.x, y2), _board)[0] != piece[0]:
                    pm.append(Vector2(start.x, y2))
                    break
                else:
                    break

        # Right
        if start.x != 7:
            for x1 in range(start.x + 1, 8):
                if getValue(Vector2(x1, start.y), _board) == "--":
                    pm.append(Vector2(x1, start.y))
                elif getValue(Vector2(x1, start.y), _board)[0] != piece[0]:
                    pm.append(Vector2(x1, start.y))
                    break
                else:
                    break

        # Left
        if start.x != 0:
            for x2 in range(start.x - 1, -1, -1):
                if getValue(Vector2(x2, start.y), _board) == "--":
                    pm.append(Vector2(x2, start.y))
                elif getValue(Vector2(x2, start.y), _board)[0] != piece[0]:
                    pm.append(Vector2(x2, start.y))
                    break
                else:
                    break
    elif piece[1] == "N":
        pos = start + Vector2(-1, 2)
        if -1 < pos.x < 8 and -1 < pos.y < 8:
            if getValue(pos, _board)[0] != piece[0]:
                pm.append(pos)

        pos = start + Vector2(1, 2)
        if -1 < pos.x < 8 and -1 < pos.y < 8:
            if getValue(pos, _board)[0] != piece[0]:
                pm.append(pos)

        pos = start + Vector2(-2, 1)
        if -1 < pos.x < 8 and -1 < pos.y < 8:
            if getValue(pos, _board)[0] != piece[0]:
                pm.append(pos)

        pos = start + Vector2(2, 1)
        if -1 < pos.x < 8 and -1 < pos.y < 8:
            if getValue(pos, _board)[0] != piece[0]:
                pm.append(pos)

        pos = start + Vector2(-2, -1)
        if -1 < pos.x < 8 and -1 < pos.y < 8:
            if getValue(pos, _board)[0] != piece[0]:
                pm.append(pos)

        pos = start + Vector2(2, -1)
        if -1 < pos.x < 8 and -1 < pos.y < 8:
            if getValue(pos, _board)[0] != piece[0]:
                pm.append(pos)

        pos = start + Vector2(-1, -2)
        if -1 < pos.x < 8 and -1 < pos.y < 8:
            if getValue(pos, _board)[0] != piece[0]:
                pm.append(pos)

        pos = start + Vector2(1, -2)
        if -1 < pos.x < 8 and -1 < pos.y < 8:
            if getValue(pos, _board)[0] != piece[0]:
                pm.append(pos)
    elif piece[1] == "B":
        # Top Right
        for i1 in range(1, 8):
            pos = start + Vector2(i1, i1)
            if pos.x > 7 or pos.y > 7:
                break
            elif getValue(pos, _board) == "--":
                pm.append(pos)
            elif getValue(pos, _board)[0] != piece[0]:
                pm.append(pos)
                break
            else:
                break

        # Top Left
        for i2 in range(1, 8):
            pos = start + Vector2(-i2, i2)
            if pos.x < 0 or pos.y > 7:
                break
            elif getValue(pos, _board) == "--":
                pm.append(pos)
            elif getValue(pos, _board)[0] != piece[0]:
                pm.append(pos)
                break
            else:
                break

        # Bottom Right
        for i3 in range(1, 8):
            pos = start + Vector2(i3, -i3)
            if pos.x > 7 or pos.y < 0:
                break
            elif getValue(pos, _board) == "--":
                pm.append(pos)
            elif getValue(pos, _board)[0] != piece[0]:
                pm.append(pos)
                break
            else:
                break

        # Bottom Left
        for i4 in range(1, 8):
            pos = start + Vector2(-i4, -i4)
            if pos.x < 0 or pos.y < 0:
                break
            elif getValue(pos, _board) == "--":
                pm.append(pos)
            elif getValue(pos, _board)[0] != piece[0]:
                pm.append(pos)
                break
            else:
                break
    elif piece[1] == "Q":
        # Up
        if start.y != 7:
            for y1 in range(start.y + 1, 8):
                if getValue(Vector2(start.x, y1), _board) == "--":
                    pm.append(Vector2(start.x, y1))
                elif getValue(Vector2(start.x, y1), _board)[0] != piece[0]:
                    pm.append(Vector2(start.x, y1))
                    break
                else:
                    break

        # Down
        if start.y != 0:
            for y2 in range(start.y - 1, -1, -1):
                if getValue(Vector2(start.x, y2), _board) == "--":
                    pm.append(Vector2(start.x, y2))
                elif getValue(Vector2(start.x, y2), _board)[0] != piece[0]:
                    pm.append(Vector2(start.x, y2))
                    break
                else:
                    break

        # Right
        if start.x != 7:
            for x1 in range(start.x + 1, 8):
                if getValue(Vector2(x1, start.y), _board) == "--":
                    pm.append(Vector2(x1, start.y))
                elif getValue(Vector2(x1, start.y), _board)[0] != piece[0]:
                    pm.append(Vector2(x1, start.y))
                    break
                else:
                    break

        # Left
        if start.x != 0:
            for x2 in range(start.x - 1, -1, -1):
                if getValue(Vector2(x2, start.y), _board) == "--":
                    pm.append(Vector2(x2, start.y))
                elif getValue(Vector2(x2, start.y), _board)[0] != piece[0]:
                    pm.append(Vector2(x2, start.y))
                    break
                else:
                    break

        # Top Right
        for i1 in range(1, 8):
            pos = start + Vector2(i1, i1)
            if pos.x > 7 or pos.y > 7:
                break
            elif getValue(pos, _board) == "--":
                pm.append(pos)
            elif getValue(pos, _board)[0] != piece[0]:
                pm.append(pos)
                break
            else:
                break

        # Top Left
        for i2 in range(1, 8):
            pos = start + Vector2(-i2, i2)
            if pos.x < 0 or pos.y > 7:
                break
            elif getValue(pos, _board) == "--":
                pm.append(pos)
            elif getValue(pos, _board)[0] != piece[0]:
                pm.append(pos)
                break
            else:
                break

        # Bottom Right
        for i3 in range(1, 8):
            pos = start + Vector2(i3, -i3)
            if pos.x > 7 or pos.y < 0:
                break
            elif getValue(pos, _board) == "--":
                pm.append(pos)
            elif getValue(pos, _board)[0] != piece[0]:
                pm.append(pos)
                break
            else:
                break

        # Bottom Left
        for i4 in range(1, 8):
            pos = start + Vector2(-i4, -i4)
            if pos.x < 0 or pos.y < 0:
                break
            elif getValue(pos, _board) == "--":
                pm.append(pos)
            elif getValue(pos, _board)[0] != piece[0]:
                pm.append(pos)
                break
            else:
                break
    elif piece[1] == "K":
        pos = start + Vector2(-1, 1)
        if -1 < pos.x < 8 and -1 < pos.y < 8:
            if getValue(pos, _board)[0] != piece[0]:
                pm.append(pos)
        pos = start + Vector2(0, 1)
        if -1 < pos.x < 8 and -1 < pos.y < 8:
            if getValue(pos, _board)[0] != piece[0]:
                pm.append(pos)
        pos = start + Vector2(1, 1)
        if -1 < pos.x < 8 and -1 < pos.y < 8:
            if getValue(pos, _board)[0] != piece[0]:
                pm.append(pos)
        pos = start + Vector2(-1, 0)
        if -1 < pos.x < 8 and -1 < pos.y < 8:
            if getValue(pos, _board)[0] != piece[0]:
                pm.append(pos)
        pos = start + Vector2(1, 0)
        if -1 < pos.x < 8 and -1 < pos.y < 8:
            if getValue(pos, _board)[0] != piece[0]:
                pm.append(pos)
        pos = start + Vector2(-1, -1)
        if -1 < pos.x < 8 and -1 < pos.y < 8:
            if getValue(pos, _board)[0] != piece[0]:
                pm.append(pos)
        pos = start + Vector2(0, -1)
        if -1 < pos.x < 8 and -1 < pos.y < 8:
            if getValue(pos, _board)[0] != piece[0]:
                pm.append(pos)
        pos = start + Vector2(1, -1)
        if -1 < pos.x < 8 and -1 < pos.y < 8:
            if getValue(pos, _board)[0] != piece[0]:
                pm.append(pos)

        if not checkr:
            pieces = getPieces("W" if piece[0] == "B" else "B", _board)
            check = False
            for i in pieces:
                if canGo(i, findValue(turn + "K", _board), _board, True):
                    check = True
                    break

            if piece[0] == "W":
                if not wkMoved and not check:
                    if getValue(Vector2(5, 0)) == "--" and getValue(Vector2(6, 0)) == "--" and getValue(
                            Vector2(7, 0)) == "WR":
                        pm.append(Vector2(6, 0))
                    if getValue(Vector2(3, 0)) == "--" and getValue(Vector2(2, 0)) == "--" and getValue(
                            Vector2(1, 0)) == "--" and getValue(Vector2(0, 0)) == "WR":
                        pm.append(Vector2(2, 0))

            if piece[0] == "B":
                if not bkMoved and not check:
                    if getValue(Vector2(5, 7)) == "--" and getValue(Vector2(6, 7)) == "--" and getValue(
                            Vector2(7, 7)) == "BR":
                        pm.append(Vector2(6, 7))
                    if getValue(Vector2(3, 7)) == "--" and getValue(Vector2(2, 7)) == "--" and getValue(
                            Vector2(1, 7)) == "--" and getValue(Vector2(0, 7)) == "BR":
                        pm.append(Vector2(2, 7))

    return end in pm


def getPieces(color: str, _board: [[str]]) -> [Vector2]:
    arr = []
    for i in range(8):
        for j in range(8):
            if _board[i][j][0] == color:
                arr.append(Vector2(j, 7 - i))

    return arr


def findValue(value: str, _board: [[str]]) -> Vector2 or [Vector2]:
    arr = []
    for i in range(8):
        for j in range(8):
            if _board[i][j] == value:
                arr.append(Vector2(j, 7 - i))

    return arr[0] if len(arr) == 1 else arr


def convertCordToV2(value: str) -> (Vector2, Vector2):
    arr = ["a", "b", "c", "d", "e", "f", "g", "h"]

    return Vector2(arr.index(value[0]), int(value[1]) - 1), Vector2(arr.index(value[3]), int(value[4]) - 1)


"""print("Welcome to the chess app. To move one of your pieces first write the position of your piece, leave a space "
      "then write the position of the square that you want to move your piece to. For example a1 a2.\n")
print(boardToText() + "\n")
while True:
    _move = input("move:")

    _start = Vector2(0, 0)
    _end = Vector2(0, 0)
    try:
        _start, _end = convertCordToV2(_move)
    except:
        print("Invalid syntax.")
        continue

    move(_start, _end)
"""