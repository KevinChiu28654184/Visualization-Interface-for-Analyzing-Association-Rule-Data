import wx
import os
import GUI
import matplotlib

matplotlib.use('WXAgg')
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from Processor import *
from DrawGraph import *


class MainFrame(GUI.MainFrame):
    def __init__(self):
        super().__init__()
        self.Bind(wx.EVT_CLOSE, self.onClose)

        self.DP = DataProcess()
        self.DATA = None

        self.file_select.Bind(wx.EVT_BUTTON, self.onButtonOpen)
        self.antecedents_combo.Bind(wx.EVT_COMBOBOX, self.onANTselect)
        self.consequents_combo.Bind(wx.EVT_COMBOBOX, self.onCONselect)



    def onButtonOpen(self, event):
        openFileDialog = wx.FileDialog(self.panel, "Open", "", "", "", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        openFileDialog.ShowModal()
        if os.path.isfile(openFileDialog.GetPath()):
            self.DP.openFile(openFileDialog.GetPath())
            self.file_path.SetLabel(openFileDialog.GetPath())
            # get all data
            self.DATA = self.DP.selectAnt()
            self.SetANTselect()
            self.SetCONselect()
        else:
            self.file_path.SetLabel("...")

    def onANTselect(self, event):
        try:
            ant = self.antecedents_combo.GetValue()
            con = self.consequents_combo.GetValue()
            if ant == "all":
                return
            elif ant == "none":
                self.DATA = self.DP.selectAnt()
                self.SetANTselect()
                self.SetCONselect()
                return
            else:
                self.DATA = self.DP.selectAnt()
                self.DATA = self.DP.selectAnt(ant, self.DATA)
                self.consequents_combo.SetItems(["all"])
                self.consequents_combo.SetValue("all")
        except:
            pass
        self.Draw()

    def onCONselect(self, event):
        try:
            ant = self.antecedents_combo.GetValue()
            con = self.consequents_combo.GetValue()
            if con == "all":
                return
            elif con == "none":
                self.DATA = self.DP.selectCon()
                self.SetANTselect()
                self.SetCONselect()
                return
            else:
                self.DATA = self.DP.selectCon()
                self.DATA = self.DP.selectCon(con, self.DATA)
                self.antecedents_combo.SetItems(["all"])
                self.antecedents_combo.SetValue("all")
        except:
            pass
        self.Draw()

    def SetANTselect(self):
        items = np.unique(self.DATA[:, 0])
        items = np.append(["none"], items)
        self.antecedents_combo.SetItems(items)
        self.antecedents_combo.SetValue("none")

    def SetCONselect(self):
        items = np.unique(self.DATA[:, 1])
        items = np.append(["none"], items)
        self.consequents_combo.SetItems(items)
        self.consequents_combo.SetValue("none")

    def Draw(self):
        self.DAG.Destroy()
        self.BAR.Destroy()

        self.dag = drawDAG(self.DATA[:, 0], self.DATA[:, 1], self.DATA[:, 2], self.DP.get_path(), 0)
        self.bar = drawBar(self.DATA[:, 0], self.DATA[:, 1], self.DATA[:, 2], self.DP.get_path(), 0)

        self.DAG = FigureCanvas(self.DAG_region, -1, self.dag)
        self.DAG_region.GetSizer().Add(self.DAG, 0, wx.EXPAND)

        self.BAR = FigureCanvas(self.BAR_region, -1, self.bar)
        self.BAR_region.GetSizer().Add(self.BAR, 0, wx.EXPAND)

        self.picture_region.Refresh()
        self.DAG_region.Refresh()
        self.BAR_region.Refresh()

    def onClose(self, event):
        self.Destroy()
        exit(0)