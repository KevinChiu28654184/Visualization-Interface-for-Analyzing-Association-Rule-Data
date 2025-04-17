import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
import networkx as nx
import numpy as np
import pandas as pd
import random
import itertools
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import math
from Processor import Locator
import TTF

locator = Locator()

print(plt.__file__)
# Digraph part

def drawDAG(antecedents, consequent, oddsratio, path, choice):

    fig = plt.figure()
    graph = nx.DiGraph()
    #pos1 = locator.get_pos(antecedents, consequent, oddsratio, pos_type="random")
    global pos
    pos = {}
    
    uni_fea = np.unique(np.array(list(np.unique(antecedents)) + list(np.unique(consequent))))
    tmp_wid=[]
    #odd=np.array(oddsratio)
    for i in range(len(oddsratio)):
        if oddsratio[i]>=5.5:
            tmp_wid.append(1.7)
        else:
            tmp_wid.append(1+(oddsratio[i]-1)/10)
    wid=np.array(tmp_wid)
    print("uni_fea")
    print(uni_fea)
    print("\n")
    data_size = antecedents.size
    for i in range(data_size):
        graph.add_edge(antecedents[i], consequent[i])
    
    # plt part
    plt.rcParams['font.sans-serif'] = [TTF.get_font()]
    plt.rcParams['axes.unicode_minus'] = False

    plt.cla()
    
    fig = plt.figure(figsize=(2,2),dpi=300)
    gs = fig.add_gridspec(2, 2)
    global f3_ax1
    f3_ax1 = fig.add_subplot(gs[:, :])

    pos = nx.spring_layout(graph)
    nx.draw_networkx(graph,
                     pos=pos,
                     with_labels=False,
                     arrows=True,
                     node_size=10,
                     font_size=4,
                     font_color='r',
                     node_color='y',
                     width=wid,  
                     arrowsize=5)
    #nx.set_node_attributes(graph, 1)
    
    annot = f3_ax1.annotate('', xy=(0, 0), xytext=(10, 10), xycoords='data', textcoords='offset points', arrowprops=dict(arrowstyle='->'), fontsize=5, bbox={
                            'boxstyle':'round',
                            'facecolor':'#ff0',
                            'edgecolor':'#f00',
                            'pad':0.5,
                            'linewidth':1})
    annot2 = f3_ax1.annotate('', xy=(0, 0), xytext=(-50, 10), xycoords='data', textcoords='offset points', arrowprops=dict(arrowstyle='->'), fontsize=5, bbox={
                            'boxstyle':'round',
                            'facecolor':'#ff0',
                            'edgecolor':'#f00',
                            'pad':0.5,
                            'linewidth':1})
    annot3 = f3_ax1.annotate('', xy=(0, 0), xytext=(10, -10), xycoords='data', textcoords='offset points', arrowprops=dict(arrowstyle='->'), fontsize=5, bbox={
                            'boxstyle':'round',
                            'facecolor':'#ff0',
                            'edgecolor':'#f00',
                            'pad':0.5,
                            'linewidth':1})
    annot4 = f3_ax1.annotate('', xy=(0, 0), xytext=(-50, -10), xycoords='data', textcoords='offset points', arrowprops=dict(arrowstyle='->'), fontsize=5, bbox={
                            'boxstyle':'round',
                            'facecolor':'#ff0',
                            'edgecolor':'#f00',
                            'pad':0.5,
                            'linewidth':1})
    annot.set_visible(False)
    annot2.set_visible(False)
    annot3.set_visible(False)
    annot4.set_visible(False)

    global press
    global lastx
    global lasty
    lastx=0
    lasty=0
    press=False
    def on_press(event):
        global press
        global lastx
        global lasty
        if event.inaxes:
            if event.button==1:
                global press
                press = True
                lastx = event.xdata
                lasty = event.ydata
    def on_move(event):
        axtemp=event.inaxes
        if axtemp is None:
            pass
        else:
            if press:
                x=event.xdata-lastx
                y=event.ydata-lasty
                xmin, xmax=axtemp.get_xlim()
                ymin, ymax=axtemp.get_ylim()

                xmin=xmin-x
                ymin=ymin-y
                xmax=xmax-x
                ymax=ymax-y

                axtemp.set_xlim(xmin, xmax)
                axtemp.set_ylim(ymin, ymax)
                fig.canvas.draw()
    def on_release(event):
        global press
        if press:
            press=False
    
    fig.canvas.mpl_connect("button_press_event", on_press)
    fig.canvas.mpl_connect("button_release_event", on_release)
    fig.canvas.mpl_connect("motion_notify_event", on_move)

    def call_back(event):
        axtemp=event.inaxes
        xmin, xmax=axtemp.get_xlim()
        ymin, ymax=axtemp.get_ylim()
        xrange=(xmax-xmin)/10
        yrange=(ymax-ymin)/10
        if event.button=='up':
            axtemp.set(xlim=(xmin+xrange, xmax-xrange))
            axtemp.set(ylim=(ymin+yrange, ymax-yrange))
        elif event.button=='down':
            axtemp.set(xlim=(xmin-xrange, xmax+xrange))
            axtemp.set(ylim=(ymin-yrange, ymax+yrange))
        fig.canvas.draw_idle()
    fig.canvas.mpl_connect('scroll_event', call_back)

    def hovor(event):
        global pos
        global tmpstr
        vis=annot.get_visible()
        if event.inaxes is None:
            pass
        else:
                
            for p in pos:
                xpos=event.xdata+20
                ypos=event.ydata+20

                print("vis ", vis)
                print(p, " ", pos[p])
                print("mouse ", event.xdata, " ", event.ydata)
                if (event.xdata>=pos[p][0]-0.05 and event.xdata<=pos[p][0]+0.05) and event.ydata >= pos[p][1]-0.05 and event.ydata <= pos[p][1]+0.05:
                    
                    w,h = fig.get_size_inches()*fig.dpi
                    ws = (event.x > w/2.)*(-1) + (event.x <= w/2.) 
                    hs = (event.y > h/2.)*(-1) + (event.y <= h/2.)
                    print("ws, hs ", ws, hs)
                    tmpp=repr(p)
                    tmpp=tmpp.replace(',', '\n')
                    print("tmpp ", tmpp)
                    # if event occurs in the top or right quadrant of the figure,
                    # change the annotation box position relative to mouse.
                    if ws==-1:
                        if hs==-1:
                            annot4.xy=(event.xdata, event.ydata)
                            annot4.set_text(tmpp)
                            annot4.set_visible(True)
                        elif hs==1:
                            annot2.xy=(event.xdata, event.ydata)
                            annot2.set_text(tmpp)
                            annot2.set_visible(True)
                    elif ws==1:
                        if hs==-1:
                            annot3.xy=(event.xdata, event.ydata)
                            annot3.set_text(tmpp)
                            annot3.set_visible(True)
                        elif hs==1:
                            annot.xy=(event.xdata, event.ydata)
                            annot.set_text(tmpp)
                            annot.set_visible(True) 
                    print("get")
                    fig.canvas.draw_idle()
                    break
                else:
                    if annot.get_visible():
                        annot.set_visible(False)
                    if annot2.get_visible():
                        annot2.set_visible(False)
                    if annot3.get_visible():
                        annot3.set_visible(False)
                    if annot4.get_visible():
                        annot4.set_visible(False)
                    print("no found")
                    fig.canvas.draw_idle()
        fig.canvas.draw_idle()
    global cid
    cid=fig.canvas.mpl_connect('motion_notify_event', hovor)
    plt.plot()
    return fig

def drawBar(antecedents, consequent, oddsratio, path, choice):
    fig1 = plt.figure(figsize=(2,2),dpi=300)
    gs2 = fig1.add_gridspec(2, 2)
    f3_ax2 = fig1.add_subplot(gs2[0, :])
    x = []
    h = []
    minimum = 0
    min_por = 0
    maxlen=0
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
    global tmpstr
    tmpstr = ""
    for i in range(len(x)):
        if maxlen<len(x[i]):
            maxlen=len(x[i])
    for i in range(len(x)):
        tmpstr += ( str(i + 1) + ". " + x[len(x) - 1-i] )
        #if len(x[len(x)-i-1])<maxlen:
            #for j in range(maxlen-len(x[len(x)-i-1])):
                #tmpstr+=" "
        tmpstr+="\n"
        xname.append(str(len(x)-i))
    xname.reverse()
    h.reverse()
    #y_major_locator = MultipuleLocator(1)
    #plt.yaxis.set_major_locator(y_major_locator)
    ax=plt.gca()
    ax.xaxis.set_major_locator(MultipleLocator((int(h[0])+(5-(int(h[0])%5)))/5))
    plt.barh(np.array(xname), np.array(h))
    plt.ylim(5, -1)
    plt.xlabel( tmpstr, horizontalalignment="left", fontsize=5, x=0)
    plt.plot()
    return fig1
