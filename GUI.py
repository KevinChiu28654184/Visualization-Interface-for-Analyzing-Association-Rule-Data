import wx
import matplotlib

matplotlib.use('WXAgg')
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas

# wxApp -> wxFrame -> wxPanel -> wxSizer -> wxControl

class MainFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Causal Rule")

        self.SetSize(1200,800)
        self.Center() 
                          
        self.panel = wx.Panel(self)
        vbox = wx.BoxSizer(orient=wx.VERTICAL)



        file_region = wx.Panel(self.panel)
        file_hbox = wx.BoxSizer()

        self.file_select = wx.Button(file_region, label = "Open")
        file_hbox.Add(self.file_select,0,wx.ALL,10)
        self.file_path = wx.StaticText(file_region, label = "...",size=(1000,50))
        file_hbox.Add(self.file_path,0,wx.ALL|wx.EXPAND,10)

        file_region.SetSizer(file_hbox)
        vbox.Add(file_region,0,wx.CENTER|wx.TOP,0)



        antecedents_region = wx.Panel(self.panel)
        antecedents_hbox = wx.BoxSizer()

        self.antecedents_text = wx.StaticText(antecedents_region, label = "antecedents: ")
        antecedents_hbox.Add(self.antecedents_text,0,0,0)
        self.antecedents_combo = wx.ComboBox(antecedents_region, value="none", choices=["none"]
                                             ,size = (1000,50), style = wx.CB_READONLY)
        antecedents_hbox.Add(self.antecedents_combo,0,0,0)

        antecedents_region.SetSizer(antecedents_hbox)
        vbox.Add(antecedents_region,0,wx.CENTER|wx.TOP,0)

 

        consequents_region = wx.Panel(self.panel)
        consequents_hbox = wx.BoxSizer()

        self.consequents_text = wx.StaticText(consequents_region, label = "consequents: ")
        consequents_hbox.Add(self.consequents_text,0,0,0)
        self.consequents_combo = wx.ComboBox(consequents_region, value="none", choices=["none"]
                                             ,size = (1000,50), style = wx.CB_READONLY)
        consequents_hbox.Add(self.consequents_combo,0,0,0)

        consequents_region.SetSizer(consequents_hbox)
        vbox.Add(consequents_region,0,wx.CENTER|wx.TOP,0)



        self.picture_region = wx.Panel(self.panel)
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
        vbox.Add(self.picture_region,2,wx.EXPAND,0)



        self.panel.SetSizer(vbox)

        self.SetAllFont()

    def SetAllFont(self):
        self.font = wx.Font(pointSize=20, family=wx.FONTFAMILY_ROMAN, style=0, weight=90)

        self.file_select.SetFont(self.font)
        self.file_path.SetFont(self.font)

        self.antecedents_text.SetFont(self.font)
        self.antecedents_combo.SetFont(self.font)

        self.consequents_text.SetFont(self.font)
        self.consequents_combo.SetFont(self.font)


