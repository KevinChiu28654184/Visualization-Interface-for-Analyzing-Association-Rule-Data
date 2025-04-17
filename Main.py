
import wx
from Page import MainPage as Page

class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="Causal Rule")
        self.Bind(wx.EVT_CLOSE, self.onClose)
        self.SetSize((1200, 800))

        panel  = wx.Panel(self)
        vbox    = wx.BoxSizer(wx.VERTICAL)

        self.buttonInsert = wx.Button(panel, id=wx.ID_ANY, label="Create new Page")
        self.buttonInsert.Bind(wx.EVT_BUTTON, self.onButtonInsert)
        vbox.Add(self.buttonInsert, 0 , wx.CENTER, 0)

        self.notebook = wx.Notebook(panel)
        vbox.Add(self.notebook, 2, flag=wx.EXPAND)

        panel.SetSizer(vbox)

        self.pageCounter = 0
        self.addPage()
        self.Center()

    def addPage(self):
        self.pageCounter += 1
        page      = Page(self.notebook)
        pageTitle = "Page: {0}".format(str(self.pageCounter))
        self.notebook.AddPage(page, pageTitle)

    def onButtonInsert(self, event):   
        self.addPage()

    def onClose(self, event):
        self.Destroy()

if __name__ == "__main__":
    app = wx.App()
    MainFrame().Show()
    app.MainLoop()