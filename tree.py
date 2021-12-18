# -*- coding: utf-8 -*-
"""
Created on Sat May 15 10:28:20 2021

@author: 10353
"""

import os
import random
import torch
import numpy as np
import time

# %%
def bingo_judge(chessList):
    for i in range(0, 7, 3):
        if chessList[i] == 1 and chessList[i+1] == 1 and chessList[i+2] == 1:
            return True
    for i in range(3):
        if chessList[i] == 1 and chessList[i+3] == 1 and chessList[i+6] == 1:
            return True
    if chessList[0] == 1 and chessList[4] == 1 and chessList[8] == 1:
        return True
    if chessList[2] == 1 and chessList[4] == 1 and chessList[6] == 1:
        return True
    return False

def Tree_AI1(index, chess_AI1):
    global Tree
    global start
    if len(Tree) % 10000== 0:
        stop = time.time()
        print(stop - start)
    
    if bingo_judge(chess_AI1) == True:
        Tree[index]['P_win'] = 1
        return
    
    if sum(chess_AI1 == 0) == 0:
        Tree[index]['P_draw'] = 1
        return
    
    chess_AI2 = -chess_AI1
    for i in range(9):
        chess_AI2_played = chess_AI2.clone()
        if chess_AI2_played[i] == 0:
            chess_AI2_played[i] = 1
            Tree[index]['child'].append(len(Tree))
            Tree.append({'step': i, 'child': [], 'P_win': 0, 'P_lose': 0, 'P_draw': 0})
            
            Tree_AI2(Tree[index]['child'][-1], chess_AI2_played)
            
    P_win = P_lose = P_draw = 0
    for t in range(len(Tree[index]['child'])):
        P_win = P_win + Tree[Tree[index]['child'][t]]['P_win']
        P_lose = P_lose + Tree[Tree[index]['child'][t]]['P_lose']
        P_draw = P_draw + Tree[Tree[index]['child'][t]]['P_draw']
    Tree[index]['P_win'] = P_win / len(Tree[index]['child'])
    Tree[index]['P_lose'] = P_lose / len(Tree[index]['child'])
    Tree[index]['P_draw'] = P_draw / len(Tree[index]['child'])
    
def Tree_AI2(index, chess_AI2):
    global Tree
    global start
    if len(Tree) == 0:
        stop = time.time()
        print(stop - start)
    
    if bingo_judge(chess_AI2) == True:
        Tree[index]['P_lose'] = 1
        return
    
    if sum(chess_AI2 == 0) == 0:
        Tree[index]['P_draw'] = 1
        return
    
    chess_AI1 = -chess_AI2
    for i in range(9):
        chess_AI1_played = chess_AI1.clone()
        if chess_AI1_played[i] == 0:
            chess_AI1_played[i] = 1
            Tree[index]['child'].append(len(Tree))
            Tree.append({'step': i, 'child': [], 'P_win': 0, 'P_lose': 0, 'P_draw': 0})
            
            Tree_AI1(Tree[index]['child'][-1], chess_AI1_played)
            
    P_win = P_lose = P_draw = 0
    for t in range(len(Tree[index]['child'])):
        P_win = P_win + Tree[Tree[index]['child'][t]]['P_win']
        P_lose = P_lose + Tree[Tree[index]['child'][t]]['P_lose']
        P_draw = P_draw + Tree[Tree[index]['child'][t]]['P_draw']
    Tree[index]['P_win'] = P_win / len(Tree[index]['child'])
    Tree[index]['P_lose'] = P_lose / len(Tree[index]['child'])
    Tree[index]['P_draw'] = P_draw / len(Tree[index]['child'])

def Tree_create():
    global Tree
    Tree = []
    chess_AI1 = torch.zeros(9)
    Tree.append({'step': -1, 'child': [], 'P_win': 0, 'P_lose': 0, 'P_draw': 0})
    
    for i in range(9):
        chess_AI1_played = chess_AI1.clone()
        chess_AI1_played[i] = 1
        Tree[0]['child'].append(len(Tree))
        Tree.append({'step': i, 'child': [], 'P_win': 0, 'P_lose': 0, 'P_draw': 0})
        
        Tree_AI1(Tree[0]['child'][-1], chess_AI1_played)
        
    P_win = P_lose = P_draw = 0
    for t in range(len(Tree[0]['child'])):
        P_win = P_win + Tree[Tree[0]['child'][t]]['P_win']
        P_lose = P_lose + Tree[Tree[0]['child'][t]]['P_lose']
        P_draw = P_draw + Tree[Tree[0]['child'][t]]['P_draw']
    Tree[0]['P_win'] = P_win / len(Tree[0]['child'])
    Tree[0]['P_lose'] = P_lose / len(Tree[0]['child'])
    Tree[0]['P_draw'] = P_draw / len(Tree[0]['child'])      

def combat_random():
    win = lose = tie = 0
    global Tree
    for t in range(1000): 
        chess_AI1 = torch.zeros(9)
        chess_AI2 = torch.zeros(9)
        first = random.randint(0, 1)
        
        first_index = 0
        
        play_A2 = -1
        
        if first == 1:
            empty_index = []
            for i in range(9):
                if chess_AI1[i] == 0:
                    empty_index.append(i)
            n = random.randint(0, len(empty_index) - 1)
            play_i = empty_index[n]
            chess_AI2[play_i] = 1
            chess_AI1 = - chess_AI2
            play_A2 = play_i
            
            for t in range(len(Tree[first_index]['child'])):
                if Tree[Tree[first_index]['child'][t]]['step'] == play_A2:
                    first_index = Tree[first_index]['child'][t]
                    break
        
        while(True):
            
            best_child = []
            best_step = []
            score_best = -2
            for t in range(len(Tree[first_index]['child'])):
                win_p = Tree[Tree[first_index]['child'][t]]['P_win']
                draw_p = Tree[Tree[first_index]['child'][t]]['P_draw']
                lose_p = Tree[Tree[first_index]['child'][t]]['P_lose']
                score_temp = 3* win_p - 0.02 * draw_p - lose_p
                if first == 1:
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
            chess_AI1[play_i] = 1
            chess_AI2 = - chess_AI1
            
            if bingo_judge(chess_AI1) == True:
                win = win + 1
                break
        
            if sum(chess_AI1 == 0) == 0:
                tie = tie + 1
                break
            
            # 
            empty_index = []
            for i in range(9):
                if chess_AI1[i] == 0:
                    empty_index.append(i)
            n = random.randint(0, len(empty_index) - 1)
            play_i = empty_index[n]
            chess_AI2[play_i] = 1
            chess_AI1 = - chess_AI2
            play_A2 = play_i
            
            if bingo_judge(chess_AI2) == True:
                lose = lose + 1
                break
        
            if sum(chess_AI2 == 0) == 0:
                tie = tie + 1
                break
            
            for t in range(len(Tree[first_index]['child'])):
                if Tree[Tree[first_index]['child'][t]]['step'] == play_A2:
                    first_index = Tree[first_index]['child'][t]
                    break
    
    return win, lose, tie

# %%
if os.path.exists('tree.npy'):
    Tree = np.load('tree.npy', allow_pickle=True).tolist()
        
# %%
else:
    start = time.time()
    Tree_create()
    print('OK.')
    # %%
    np.save('tree.npy', Tree) 
    
# %%
win_avg = lose_avg = tie_avg = 0
for i in range(10):
    win, lose, tie = combat_random()
    win_avg = win_avg + win
    lose_avg = lose_avg + lose
    tie_avg = tie_avg + tie
    
win_avg = win_avg / 10
lose_avg = lose_avg / 10
tie_avg = tie_avg / 10
print('win_avg:%d' % win_avg)
print('lose_avg:%d' % lose_avg)
print('tie_avg:%d' % tie_avg)