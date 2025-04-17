import wx
import os

import numpy as np

import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('WXAgg')
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas

from Processor import Loader as Loader
from Processor import Filter as Filter
from DrawGraph import drawBar, drawDAG

class GUI(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        print("C")
        self.SetSizer(wx.BoxSizer(wx.VERTICAL))
        self.add_file_region()
        self.add_antecedents_region()
        self.add_consequents_region()
        self.add_picture_region()                  
        self.SetAllFont()

    def add_file_region(self):
        file_region = wx.Panel(self)
        file_hbox = wx.BoxSizer()

        self.file_select = wx.Button(file_region, label = "Open")
        file_hbox.Add(self.file_select,0,wx.ALL,10)
        self.file_path = wx.StaticText(file_region, label = "...",size=(1000,50))
        file_hbox.Add(self.file_path,0,wx.ALL|wx.EXPAND,10)

        file_region.SetSizer(file_hbox)
        self.GetSizer().Add(file_region,0,wx.CENTER|wx.TOP,0)
    
    def add_antecedents_region(self):
        antecedents_region = wx.Panel(self)
        antecedents_hbox = wx.BoxSizer()

        self.antecedents_text = wx.StaticText(antecedents_region, label = "antecedents: ")
        antecedents_hbox.Add(self.antecedents_text,0,0,0)
        self.antecedents_combo = wx.ComboBox(antecedents_region, value="none", choices=["none"]
                                             ,size = (500,50), style = wx.CB_READONLY)
        antecedents_hbox.Add(self.antecedents_combo,0,0,0)
        self.antecedents_add = wx.Button(antecedents_region, label = "add")
        antecedents_hbox.Add(self.antecedents_add,0,0,0)
        self.antecedents_tags = wx.StaticText(antecedents_region, label = " tags: ", size=(500,50))
        antecedents_hbox.Add(self.antecedents_tags,0,0,0)

        antecedents_region.SetSizer(antecedents_hbox)
        self.GetSizer().Add(antecedents_region,0,wx.CENTER|wx.TOP,0)

    def add_consequents_region(self):
        consequents_region = wx.Panel(self)
        consequents_hbox = wx.BoxSizer()

        self.consequents_text = wx.StaticText(consequents_region, label = "consequents: ")
        consequents_hbox.Add(self.consequents_text,0,0,0)
        self.consequents_combo = wx.ComboBox(consequents_region, value="none", choices=["none"]
                                             ,size = (500,50), style = wx.CB_READONLY)
        consequents_hbox.Add(self.consequents_combo,0,0,0)
        self.consequents_add = wx.Button(consequents_region, label = "add")
        consequents_hbox.Add(self.consequents_add,0,0,0)
        self.consequents_tags = wx.StaticText(consequents_region, label = " tags: ", size=(500,50))
        consequents_hbox.Add(self.consequents_tags,0,0,0)

        consequents_region.SetSizer(consequents_hbox)
        self.GetSizer().Add(consequents_region,0,wx.CENTER|wx.TOP,0)

    def add_picture_region(self):
        self.picture_region = wx.Panel(self)
        self.picture_grid = wx.GridSizer(1,2,0,0)

        self.DAG_region = wx.Panel(self.picture_region)
        self.picture_grid.Add(self.DAG_region,0,wx.EXPAND)
        self.DAG_region.SetBackgroundColour("red")
        self.DAG = FigureCanvas(self.DAG_region, -1, None)
        self.DAG_region.SetSizer(wx.GridSizer(1,1,0,0))
        self.DAG_region.GetSizer().Add(self.DAG,0,wx.EXPAND)

        self.BAR_region = wx.Panel(self.picture_region)
        self.picture_grid.Add(self.BAR_region,0,wx.EXPAND)
        self.BAR_region.SetBackgroundColour("blue")
        self.BAR = FigureCanvas(self.BAR_region, -1, None)
        self.BAR_region.SetSizer(wx.GridSizer(1,1,0,0))
        self.BAR_region.GetSizer().Add(self.BAR,0,wx.EXPAND)

        self.picture_region.SetSizer(self.picture_grid)
        self.GetSizer().Add(self.picture_region,2,wx.EXPAND,0)

    def SetAllFont(self):
        self.font = wx.Font(pointSize=15, family=wx.FONTFAMILY_ROMAN, style=0, weight=90)

        self.file_select.SetFont(self.font)
        self.file_path.SetFont(self.font)

        self.antecedents_text.SetFont(self.font)
        self.antecedents_combo.SetFont(self.font)
        self.antecedents_add.SetFont(self.font)
        self.antecedents_tags.SetFont(self.font)

        self.consequents_text.SetFont(self.font)
        self.consequents_combo.SetFont(self.font)
        self.consequents_add.SetFont(self.font)
        self.consequents_tags.SetFont(self.font)



class Control(GUI):

    ant_col = 0
    con_col = 1
    odd_col = 2


    def __init__(self, parent):
        super().__init__(parent)
        print("B")
        self.__base_data = None
        self.__current_data = None

        self.antecedents = []
        self.consequents = []

        self.__loader = Loader()
        self.__filter = Filter()

        self.file_select.Bind(wx.EVT_BUTTON, self.onButtonOpen)
        self.antecedents_add.Bind(wx.EVT_BUTTON, self.onButtonAddAnt)
        self.consequents_add.Bind(wx.EVT_BUTTON, self.onButtonAddCon)

    def onButtonOpen(self, event):
        openFileDialog = wx.FileDialog(self, "Open", "", "", "", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        openFileDialog.ShowModal()
        if os.path.isfile(openFileDialog.GetPath()):
            self.__loader.open_file(openFileDialog.GetPath())
            self.file_path.SetLabel(openFileDialog.GetPath())
            # get all data
            self.__base_data = self.__loader.get_data()
            self.__current_data = np.copy(self.__base_data)
            self.__set_combo()
        else:
            self.file_path.SetLabel("...")

    def __set_combo(self):
        
        self.antecedents_combo.SetItems(["none"])
        for item in self.__filter.get_unique_tags(self.__current_data[:,self.ant_col]):
            flag = True
            for tag in self.antecedents:
                if item == tag:
                    flag = False
                    break
            if flag:
                self.antecedents_combo.AppendItems([item])
        self.antecedents_combo.SetValue("none")

        self.consequents_combo.SetItems(["none"])
        for item in self.__filter.get_unique_tags(self.__current_data[:,self.con_col]):
            flag = True
            for tag in self.consequents:
                if item == tag:
                    flag = False
                    break
            if flag:
                self.consequents_combo.AppendItems([item])
        self.consequents_combo.SetValue("none")

    def onButtonAddAnt(self, event):
        tag = self.antecedents_combo.GetValue()

        if tag == "none":
            self.antecedents = []
            self.__reset_data()
        else:
            self.antecedents.append(tag)
            self.__current_data = self.__filter.filter(self.__current_data, "antecedents", tag)
        # common part
        try:
            self.__set_combo()
            self.__set_tags()
            self.draw()
        except:
            print("error: no data")

    def onButtonAddCon(self, event):
        tag = self.consequents_combo.GetValue()

        if tag == "none":
            self.consequents = []
            self.__reset_data()
        else:
            self.consequents.append(tag)
            self.__current_data = self.__filter.filter(self.__current_data, "consequents", tag)
        # common part
        try:
            self.__set_combo()
            self.__set_tags()
            self.draw()       
        except:
            print("error: no data")

    def __set_tags(self):
        tags = " tags:"
        for tag in self.antecedents:
            tags += "  " + tag 
        self.antecedents_tags.SetLabel(tags)
        
        tags = " tags:"
        for tag in self.consequents:
            tags += "  " + tag
        self.consequents_tags.SetLabel(tags)
        
    def __reset_data(self):
        self.__current_data = np.copy(self.__base_data)
        for tag in self.antecedents:
            self.__current_data = self.__filter.filter(self.__current_data, "antecedents", tag)
        for tag in self.consequents:
            self.__current_data = self.__filter.filter(self.__current_data, "consequents", tag)

    def draw(self):
        self.DAG.Destroy()
        self.BAR.Destroy()

        self.dag = drawDAG(self.__current_data[:, self.ant_col],
                            self.__current_data[:, self.con_col],
                            self.__current_data[:, self.odd_col], 
                            self.__loader.get_path(), 
                            0)
        self.bar = drawBar(self.__current_data[:, self.ant_col],
                            self.__current_data[:, self.con_col], 
                            self.__current_data[:, self.odd_col], 
                            self.__loader.get_path(), 
                            0)

        self.DAG = FigureCanvas(self.DAG_region, -1, self.dag)
        self.DAG_region.GetSizer().Add(self.DAG, 0, wx.EXPAND)

        self.BAR = FigureCanvas(self.BAR_region, -1, self.bar)
        self.BAR_region.GetSizer().Add(self.BAR, 0, wx.EXPAND)

        self.picture_region.Refresh()
        self.DAG_region.Refresh()
        self.BAR_region.Refresh()



class MainPage(Control):
    def __init__(self, parent):
        super().__init__(parent)
        print("A")

        self.close = wx.Button(self, label = "Close current Page")
        self.close.Bind(wx.EVT_BUTTON, self.onClose)
        self.GetSizer().Add(self.close,0,wx.CENTER,0)
        

    def onClose(self, event):
        for index in range(self.GetParent().GetPageCount()):
            if self.GetParent().GetPage(index) == self:
                self.GetParent().DeletePage(index)
                break