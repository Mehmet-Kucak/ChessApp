import tkinter as tk
from tkinter import messagebox
from functools import partial
import chess
from MathX import Vector2


class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Chess")
        self.root.geometry("405x405")
        self.root.minsize(405, 405)

        self.B__ = tk.PhotoImage(file=".\Chess\B--.png")
        self.BBB = tk.PhotoImage(file=".\Chess\BBB.png")
        self.BBK = tk.PhotoImage(file=".\Chess\BBK.png")
        self.BBN = tk.PhotoImage(file=".\Chess\BBN.png")
        self.BBP = tk.PhotoImage(file=".\Chess\BBP.png")
        self.BBQ = tk.PhotoImage(file=".\Chess\BBQ.png")
        self.BBR = tk.PhotoImage(file=".\Chess\BBR.png")
        self.BWB = tk.PhotoImage(file=".\Chess\BWB.png")
        self.BWK = tk.PhotoImage(file=".\Chess\BWK.png")
        self.BWN = tk.PhotoImage(file=".\Chess\BWN.png")
        self.BWP = tk.PhotoImage(file=".\Chess\BWP.png")
        self.BWQ = tk.PhotoImage(file=".\Chess\BWQ.png")
        self.BWR = tk.PhotoImage(file=".\Chess\BWR.png")
        self.W__ = tk.PhotoImage(file=".\Chess\W--.png")
        self.WBB = tk.PhotoImage(file=".\Chess\WBB.png")
        self.WBK = tk.PhotoImage(file=".\Chess\WBK.png")
        self.WBN = tk.PhotoImage(file=".\Chess\WBN.png")
        self.WBP = tk.PhotoImage(file=".\Chess\WBP.png")
        self.WBQ = tk.PhotoImage(file=".\Chess\WBQ.png")
        self.WBR = tk.PhotoImage(file=".\Chess\WBR.png")
        self.WWB = tk.PhotoImage(file=".\Chess\WWB.png")
        self.WWK = tk.PhotoImage(file=".\Chess\WWK.png")
        self.WWN = tk.PhotoImage(file=".\Chess\WWN.png")
        self.WWP = tk.PhotoImage(file=".\Chess\WWP.png")
        self.WWQ = tk.PhotoImage(file=".\Chess\WWQ.png")
        self.WWR = tk.PhotoImage(file=".\Chess\WWR.png")

        self.board = tk.Frame(self.root)
        self.squares = []
        self.chosenSquare = -1

        for i in range(8):
            for j in range(8):
                b = tk.Button(self.board, borderwidth=0,
                              bg="#ffce9e" if (j + i) % 2 == 0 else "#d18b47"
                              , highlightthickness=3, command=partial(self.square, i * 8 + j))
                b.grid(row=i, column=j)
                self.squares.append(b)

        self.board.pack()
        self.updateBoard()

        self.root.mainloop()

    @staticmethod
    def rgb(rgb):
        return "#%02x%02x%02x" % rgb

    def get(self, name):
        match name:
            case "B--":
                return self.B__
            case "BBB":
                return self.BBB
            case "BBK":
                return self.BBK
            case "BBN":
                return self.BBN
            case "BBP":
                return self.BBP
            case "BBQ":
                return self.BBQ
            case "BBR":
                return self.BBR
            case "BWB":
                return self.BWB
            case "BWK":
                return self.BWK
            case "BWN":
                return self.BWN
            case "BWP":
                return self.BWP
            case "BWQ":
                return self.BWQ
            case "BWR":
                return self.BWR
            case "W--":
                return self.W__
            case "WBB":
                return self.WBB
            case "WBK":
                return self.WBK
            case "WBN":
                return self.WBN
            case "WBP":
                return self.WBP
            case "WBQ":
                return self.WBQ
            case "WBR":
                return self.WBR
            case "WWB":
                return self.WWB
            case "WWK":
                return self.WWK
            case "WWN":
                return self.WWN
            case "WWP":
                return self.WWP
            case "WWQ":
                return self.WWQ
            case "WWR":
                return self.WWR
            case default:
                print(f"Couldn't find the image named {name}.")

    def square(self, i):
        if self.chosenSquare == i:
            self.chosenSquare = -1
        elif self.chosenSquare == -1:
            if chess.getValue(Vector2(i % 8, 7-(i // 8))) != "--":
                if chess.getValue(Vector2(i % 8, 7-(i // 8)))[0] == chess.turn:
                    self.chosenSquare = i
        else:
            chess.move(Vector2(self.chosenSquare % 8, 7-(self.chosenSquare // 8)), Vector2(i % 8, 7-(i // 8)))
            self.chosenSquare = -1
        self.updateBoard()

    def updateBoard(self):
        for i in range(64):
            name = ("W" if (i // 8 + i % 8) % 2 == 0 else "B") + (chess.board[i // 8][i % 8])
            photo = self.get(name)
            self.squares[i].config(image=photo)
            self.squares[i].config(
                bg="red" if i == self.chosenSquare else "#ffce9e" if (i // 8 + i % 8) % 2 == 0 else "#d18b47")


GUI()
