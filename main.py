import socket
import thread2 as threading
import tkinter as tk
from functools import partial
import chess
import client
import server
from MathX import Vector2
from tkinter import messagebox
import time

state = 0
s_receive_thread = threading.Thread(target=server.receive)
c_receive_thread = threading.Thread(target=client.receive)
c_write_thread = threading.Thread(target=client.write)
nickname = "-NICKNAME-"
move = 0

class JoinWindow:
    def __init__(self, master, menu):
        self.menu = menu
        top = self.top = tk.Toplevel(master)
        top.geometry("190x80")
        top.resizable(0, 0)
        top.title("Host")
        self.ip = ""
        self.nickname = ""

        self.l1 = tk.Label(top, text="Nickname:")
        self.l2 = tk.Label(top, text="IP:")

        self.l1.grid(row=0, column=0, sticky=tk.W, pady=2)
        self.l2.grid(row=1, column=0, sticky=tk.W, pady=2)

        self.e1 = tk.Entry(top)
        self.e2 = tk.Entry(top)

        self.e1.grid(row=0, column=1, pady=2)
        self.e2.grid(row=1, column=1, pady=2)

        self.enter = tk.Button(top, text="Join", command=partial(self.cleanup, ""))
        self.enter.grid(row=2, column=1, pady=2, sticky="WE")

    def cleanup(self, e):
        if 3 < len(self.e1.get()) < 33:
            if not any(not i.isalnum() for i in self.e1.get()):
                self.ip = self.e2.get()
                self.nickname = self.e1.get()
                self.top.destroy()
                self.menu.activateBtns()
            else:
                messagebox.showerror("Chess App", "Nickname should not contain special characters.")
        else:
            messagebox.showerror("Chess App", "Nickname length should be more than 4 and less than 32 characters.")


class HostWindow:
    def __init__(self, master, menu):
        self.menu = menu
        top = self.top = tk.Toplevel(master)
        top.geometry("190x90")
        top.resizable(0, 0)
        top.title("Host")
        self.nickname = ""

        self.l1 = tk.Label(top, text="Nickname:")
        self.l1.grid(row=0, column=0, sticky=tk.W, pady=2)

        self.e1 = tk.Entry(top)
        self.e1.grid(row=0, column=1, pady=2)

        self.l2 = tk.Label(top, text="Color:")
        self.l2.grid(row=1, column=0, sticky=tk.W, pady=2)

        self.color = tk.StringVar()
        self.color.set("White")
        self.om = tk.OptionMenu(top, self.color, *["White", "Black"])
        self.om.grid(row=1, column=1, sticky=tk.EW, pady=2)

        self.enter = tk.Button(top, text="Host", command=partial(self.cleanup, ""))
        self.enter.grid(row=2, column=1, pady=2, sticky="WE")

    def cleanup(self, e):
        if 3 < len(self.e1.get()) < 33:
            if not any(not i.isalnum() for i in self.e1.get()):
                self.nickname = self.e1.get()
                self.top.destroy()
                self.menu.activateBtns()
            else:
                messagebox.showerror("Chess App", "Nickname should not contain special characters.")
        else:
            messagebox.showerror("Chess App", "Nickname length should be more than 4 and less than 32 characters.")


class MenuUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Chess App")
        self.root.geometry("405x300")
        self.root.resizable(0, 0)

        self.label = tk.Label(self.root, text="Chess", font=("Arial", 24))
        self.label.pack()

        self.host_btn = tk.Button(self.root, text="Host", command=self.hostBTN, height=3, width=405)
        self.host_btn.pack()

        self.join_btn = tk.Button(self.root, text="Join", command=self.joinBTN, height=3, width=405)
        self.join_btn.pack()

        self.help_msg = "Welcome to Chess App! You can host a game, join a game or play against yourself. To host a " \
                        "game click the host button and wait for your friend to connect. To join a game click the " \
                        "join button and write your friend's IP address(you can learn your IP address from " \
                        "www.myip.is). To play against yourself click play button. "

        self.help_btn = tk.Button(self.root, text="Help", command=self.helpBTN, height=3, width=405)
        self.help_btn.pack()

        self.hosting = False
        self.hostingL = tk.Label(self.root, text="Waiting for other player to join.")
        self.cancelBTN = tk.Button(self.root, text="Cancel", command=self.cancelHostBTN, width=243)
        self.Hosting()

        self.root.mainloop()

    def joinBTN(self):
        global state, nickname
        self.w = JoinWindow(self.root, self)
        self.disableBtns()
        self.root.wait_window(self.w.top)
        self.activateBtns()

        ip = self.w.ip
        nickname = self.w.nickname
        if ip != "":
            server.HOST = ip
            client.HOST = ip
            client.nickname = nickname
            try:
                client.connect()
                state = 2
                self.root.destroy()
            except:
                messagebox.showerror("Chess App", f"Could not manage to connect to {ip}. This might be because of "
                                                  f"the host is offline. ")

    def hostBTN(self):
        global state, nickname
        self.w = HostWindow(self.root, self)
        self.disableBtns()
        self.root.wait_window(self.w.top)
        self.activateBtns()
        nickname = self.w.nickname
        ip = ""
        if self.w.nickname != "":
            ip = socket.gethostbyname(socket.gethostname())
        if ip != "":
            server.HOST = ip
            server.hostColor = self.w.color.get()
            client.HOST = ip
            client.nickname = nickname
            try:
                server.host()
                server.server.listen()
                client.connect()
                state = 1
                self.hosting = True
                s_receive_thread.start()
                c_receive_thread.start()
                c_write_thread.start()
            except:
                messagebox.showerror("Chess App", f"Could not manage to host.")

    def helpBTN(self):
        messagebox.showinfo("Chess App", self.help_msg)

    def disableBtns(self):
        self.host_btn["state"] = "disabled"
        self.join_btn["state"] = "disabled"
        self.help_btn["state"] = "disabled"

    def activateBtns(self):
        self.host_btn["state"] = "active"
        self.join_btn["state"] = "active"
        self.help_btn["state"] = "active"

    def Hosting(self):
        if self.hosting:
            self.hostingL.pack(pady=20)
            self.cancelBTN.pack(side="left", padx=81)
            self.disableBtns()
            if len(server.clients) == 2:
                self.root.destroy()
        else:
            self.hostingL.pack_forget()
            self.cancelBTN.pack_forget()

        self.root.after(1000, self.Hosting)

    def cancelHostBTN(self):
        self.hosting = False
        self.activateBtns()
        server.server.close()
        client.client.close()
        server.clients = []
        server.nicknames = []


class ChessUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Chess App")
        self.root.geometry("405x500")
        self.root.resizable(0, 0)

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

        self.blackNN = tk.Label(self.root, text=client.nicknames[0] if client.hostC == "Black" else client.nicknames[1]
                                , font=("Segoe UI", 24), justify=tk.LEFT)
        self.blackNN.pack(anchor="w")

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
        self.changeLabelC()

        self.whiteNN = tk.Label(self.root, text=client.nicknames[1] if client.hostC == "Black" else client.nicknames[0],
                                font=("Segoe UI", 24), justify=tk.LEFT)
        self.whiteNN.pack(anchor="w")

        self.checkMove()

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
        global move
        if self.chosenSquare == i:
            self.chosenSquare = -1
        elif self.chosenSquare == -1:
            if chess.getValue(Vector2(i % 8, 7 - (i // 8))) != "--":
                if chess.getValue(Vector2(i % 8, 7 - (i // 8)))[0] == chess.turn:
                    if chess.getValue(Vector2(i % 8, 7 - (i // 8)))[0] == client.color:
                        self.chosenSquare = i
        else:
            if chess.turn == client.color:
                v1 = Vector2(self.chosenSquare % 8, 7 - (self.chosenSquare // 8))
                v2 = Vector2(i % 8, 7 - (i // 8))
                coord = chess.convertV2ToCoord(v1, v2)
                can_move, reason = chess.canMove(v1, v2)
                if can_move:
                    chess.move(Vector2(self.chosenSquare % 8, 7 - (self.chosenSquare // 8)), Vector2(i % 8, 7 - (i // 8)))
                    move += 1
                    client.client.send(("MOVE"+coord).encode("ascii"))

                    self.chosenSquare = -1
        self.updateBoard()
        self.changeLabelC()

    def updateBoard(self):
        for i in range(64):
            name = ("W" if (i // 8 + i % 8) % 2 == 0 else "B") + (chess.board[i // 8][i % 8])
            photo = self.get(name)
            self.squares[i].config(image=photo)
            self.squares[i].config(
                bg="red" if i == self.chosenSquare else "#ffce9e" if (i // 8 + i % 8) % 2 == 0 else "#d18b47")

    def changeLabelC(self):
        if chess.turn == "W":
            self.blackNN.config(fg="#000")
            self.whiteNN.config(fg="#0F0")
        else:
            self.blackNN.config(fg="#0F0")
            self.whiteNN.config(fg="#000")

    def checkMove(self):
        global move
        if len(client.moves) > move:
            v1, v2 = chess.convertCoordToV2(client.moves[-1])
            chess.move(v1, v2)
            move += 1

            self.chosenSquare = -1
            self.updateBoard()
            self.changeLabelC()

        self.root.after(100, self.checkMove)


MenuUI()
if state == 1:
    server.sendPlayers()
    ChessUI()
if state == 2:
    c_receive_thread.start()
    c_write_thread.start()
    time.sleep(1)
    ChessUI()
