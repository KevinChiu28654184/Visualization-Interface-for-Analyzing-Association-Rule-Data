import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
import random
import itertools
import math
# Digraph part
def draw(antecedents, consequent, oddsratio, path, choice):
    # DAG part
    graph = nx.DiGraph()
    pos = {}
    uni_fea = np.unique(np.array(list(np.unique(antecedents)) + list(np.unique(consequent))))
    n = uni_fea.size
    random_list = list(itertools.product(range(1, 150), range(1, 150)))
    potential_pos = random.sample(random_list, n)
    for i in range(uni_fea.size):
        pos[uni_fea[i]] = potential_pos[i]
    data_size = antecedents.size
    interval = 0
    for i in range(data_size):
        graph.add_edge(antecedents[i + interval], consequent[i + interval])
    
    # plt part
    plt.rcParams['font.sans-serif'] = ['Noto Sans TC']
    plt.rcParams['axes.unicode_minus'] = False
    plt.cla()
    fig = plt.figure(figsize=(4, 2), dpi=300)
    # gs = gridspec.GridSpec(1, 2, height_ratios=[3,1])
    gs = fig.add_gridspec(2, 2)
    f3_ax1 = fig.add_subplot(gs[:, 0])
    nx.draw_networkx(graph,
                     pos=pos,
                     with_labels=False,
                     arrows=True,
                     node_size=10,
                     font_size=4,
                     font_color='r',
                     node_color='y',
                     width=1,
                     arrowsize=5)
    plt.title(f"{path}\nexample size:{data_size}", fontsize=5)
     
    plt.plot()
    
    '''長條圖'''
    fig.add_subplot(gs[0, 1])
    x = []
    h = []
    minimum = 0
    min_por = 0
    '''判斷是選ant還是con'''
    xname = []
    if choice==1:
        name=antecedents
    elif choice==0:
        name=consequent
    for i in range(len(name)):
        if len(x) < 5:
            print(oddsratio[i])
            h.append(float(oddsratio[i]))
            x.append(name[i])
            minimum = min(h)
            min_por = h.index(minimum)
        elif float(oddsratio[i]) > minimum:
            x[min_por] = (name[i])
            h[min_por] = float(oddsratio[i])
            minimum = min(h)
            min_por = h.index(minimum)
    for i in range(len(x)):
        for j in range(len(x)):
            if h[i] < h[j]:
                h[i], h[j] = h[j], h[i]
                x[i], x[j] = x[j], x[i]
    tmpstr = ""
    for i in range(len(x)):
        tmpstr += ( str(i + 1) + ". " + x[len(x) - 1-i] )
        tmpstr+="\n"
        xname.append(str(len(x)-i))
    print(len(tmpstr))
    xname.reverse()
    h.reverse()
    plt.barh(np.array(xname), np.array(h))
    def reveal_name(event):
        if event.inaxes is None:
            pass
        else:
            x = round(int(event.xdata))
            y = round(int(event.ydata))
            bind = (x,y)
            found = [key for key, value in pos.items() if value == bind]
            if found != []:
                plt.annotate(found[0], xy=(event.x,event.y), color='r')
    fig.canvas.mpl_connect("motion_notify_event", reveal_name)
    plt.ylim(5, -1)
    plt.xlabel( tmpstr, horizontalalignment="left", fontsize=5, x=0)
    plt.plot()
    return fig