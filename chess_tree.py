# -*- coding: utf-8 -*-
"""
Created on Sat May 15 18:45:12 2021

@author: 10353
"""

from tkinter import *
import torch
import random
import numpy as np

enable = True


def First():
    global enable
    global chess_player
    global chess_AI
    global first_play
    first_play = True
    chess_player = torch.zeros(9)
    chess_AI = torch.zeros(9)
    for i in range(len(Cbtn)):
        Cbtn[i].btn['text'] = ''
    message['text'] = 'You first.'
    enable = True


def Second():
    global enable
    global chess_player
    global chess_AI
    global first_index
    global first_play
    first_index = 0
    first_play = False
    chess_player = torch.zeros(9)
    chess_AI = torch.zeros(9)
    for i in range(len(Cbtn)):
        Cbtn[i].btn['text'] = ''
    message['text'] = 'AI first.'
    enable = True
    play_AI()


class chess_button:
    colMax = 3
    click_text = ''
    global enable

    def __init__(self, index):
        self.index = index
        self.row = int(index / self.colMax)
        self.col = index % self.colMax

    def ColMax(self, colMax):
        self.colMax = colMax

    def create(self, root, font=None, text=None, bg=None, relief=None):
        self.text = text
        self.btn = Button(root, font=font, text=text, bg=bg, relief=relief)
        self.btn.bind('<Button-1>', self.play)
        self.btn.place(rely=0.2 + self.row * 0.6 / self.colMax, relx=0.125 + self.col * 0.75 / self.colMax,
                       relheight=0.6 / self.colMax, relwidth=0.75 / self.colMax)

    def play(self, event):
        if event.widget['text'] == '' and enable == True:
            event.widget['text'] = self.click_text
        click(self.index)


# %%
def bingo_judge(chessList):
    for i in range(0, 7, 3):
        if chessList[i] == 1 and chessList[i + 1] == 1 and chessList[i + 2] == 1:
            return True
    for i in range(3):
        if chessList[i] == 1 and chessList[i + 3] == 1 and chessList[i + 6] == 1:
            return True
    if chessList[0] == 1 and chessList[4] == 1 and chessList[8] == 1:
        return True
    if chessList[2] == 1 and chessList[4] == 1 and chessList[6] == 1:
        return True
    return False


def click(index):
    global enable
    global chess_player
    global chess_AI
    global first_index
    if chess_player[index] != 0 or enable == False:
        return

    chess_player[index] = 1
    chess_AI = - chess_player

    if bingo_judge(chess_player):
        message['text'] = 'You win.'
        enable = False
        first_index = 0
        return

    if sum(chess_player == 0) == 0:
        message['text'] = 'Draw.'
        enable = False
        first_index = 0
        return

    for t in range(len(Tree[first_index]['child'])):
        if Tree[Tree[first_index]['child'][t]]['step'] == index:
            first_index = Tree[first_index]['child'][t]
            break

    play_AI()


def play_AI():
    global enable
    global chess_player
    global chess_AI
    global first_index
    global first_play
    best_child = []
    best_step = []
    score_best = -2
    for t in range(len(Tree[first_index]['child'])):
        win_p = Tree[Tree[first_index]['child'][t]]['P_win']
        draw_p = Tree[Tree[first_index]['child'][t]]['P_draw']
        lose_p = Tree[Tree[first_index]['child'][t]]['P_lose']
        score_temp = 3 * win_p - 0.02 * draw_p - lose_p
        if first_play:
            score_temp = -score_temp

        if score_temp - score_best > 0.000000001:
            score_best = score_temp
            best_child = []
            best_step = []
            best_child.append(Tree[first_index]['child'][t])
            best_step.append(Tree[Tree[first_index]['child'][t]]['step'])

        elif abs(score_temp - score_best) <= 0.000000001:
            best_child.append(Tree[first_index]['child'][t])
            best_step.append(Tree[Tree[first_index]['child'][t]]['step'])

    n = random.randint(0, len(best_step) - 1)
    play_i = best_step[n]
    first_index = best_child[n]
    chess_AI[play_i] = 1
    chess_player = - chess_AI
    Cbtn[play_i].btn['text'] = '❌'

    if bingo_judge(chess_AI):
        message['text'] = 'You lose.'
        enable = False
        first_index = 0
        return

    if sum(chess_AI == 0) == 0:
        message['text'] = 'Draw.'
        enable = False
        first_index = 0


# %%

root = Tk()
root.title('Chess')
winWidth = 400
winHeight = 500
screenWidth = root.winfo_screenwidth()
screenHeight = root.winfo_screenheight()
x = int((screenWidth - winWidth) / 2)
y = int((screenHeight - winHeight) / 2)
root.geometry("%sx%s+%s+%s" % (winWidth, winHeight, x, y))

first = Button(root, font=('Microsoft YaHei', 10), text='Restart(you)', relief=RAISED, command=First)
first.place(rely=0.05, relx=0.125, relheight=0.1, relwidth=0.3125)

second = Button(root, font=('Microsoft YaHei', 10), text='Restart(AI)', relief=RAISED, command=Second)
second.place(rely=0.05, relx=0.5625, relheight=0.1, relwidth=0.3125)

message = Label(root, font=('Microsoft YaHei', 10), text='You first.')
message.place(rely=0.85, relx=0.125, relheight=0.1, relwidth=0.75)

chess_button.click_text = '◯'

Cbtn = []
for i in range(9):
    cbtn = chess_button(i)
    cbtn.create(root, font=('Microsoft YaHei', 32), text='', bg='#D1D1D1', relief=FLAT)
    Cbtn.append(cbtn)

Tree = np.load('tree.npy', allow_pickle=True).tolist()
first_play = True
first_index = 0

chess_player = torch.zeros(9)
chess_AI = torch.zeros(9)
root.mainloop()
