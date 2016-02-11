from win32api import *
import win32gui
class MainWindow:

    #Creats the window in the client's screen and prints the screen of server"
    def __init__(self):
        self.width  = GetSystemMetrics(0) #get the width of the screen 
        self.height = GetSystemMetrics(1) #get the height of the screen 
        win32gui.InitCommonControls()
        self.hinst = win32api.GetModuleHandle(None)
        self.CreateWindow()
        network = Network(self.hwnd)
        network.start()
        win32gui.PumpMessages()

        
    def CreateWindow(self):
        className = self.RegisterClass()
        self.BuildWindow(className)


    def RegisterClass(self):
        className = "window"
        message_map = { win32con.WM_DESTROY: self.OnDestroy, win32con.WM_PAINT: self.OnPaint, }
        wc = win32gui.WNDCLASS()
        wc.style = win32con.CS_HREDRAW | win32con.CS_VREDRAW
        wc.lpfnWndProc = message_map
        wc.cbWndExtra = 0
        wc.hCursor = win32gui.LoadCursor( 0, win32con.IDC_ARROW )
        wc.hbrBackground = win32con.COLOR_WINDOW + 1
        wc.hIcon = win32gui.LoadIcon(0, win32con.IDI_APPLICATION)
        wc.lpszClassName = className
        wc.cbWndExtra = win32con.DLGWINDOWEXTRA + struct.calcsize("Pi")
        classAtom = win32gui.RegisterClass(wc)
        return className

    #building the window
    def BuildWindow(self, className):
        style = win32con.WS_MINIMIZE  
        xstyle = win32con.WS_EX_LEFT
        self.hwnd = win32gui.CreateWindow(className,
                             "",
                             style,
                             win32con.CW_USEDEFAULT,
                             win32con.CW_USEDEFAULT,
                             self.width,
                             self.height,
                             0,  
                             0,
                             self.hinst,
                             None)
        win32gui.SetWindowLong(self.hwnd, win32con.GWL_STYLE, 0); 
        win32gui.ShowWindow(self.hwnd, win32con.SW_SHOW)

    # destroying the window
    def OnDestroy(self, hwnd, message, wparam, lparam):
        win32gui.PostQuitMessage(0)
        return True

    # painting the picture
    def OnPaint(self, hWnd, msg, wparam, lparam):   
        dc, ps=win32gui.BeginPaint(hWnd)
        wndrect = win32gui.GetClientRect(hWnd)
        wndwidth = wndrect[2]-wndrect[0] 
        wndheight = wndrect[3]-wndrect[1]
        if os.path.isfile(FILENAME):
            hBitmap = win32gui.LoadImage(0, FILENAME, win32con.IMAGE_BITMAP, 0, 0, win32con.LR_LOADFROMFILE )           
            hdcBitmap = win32gui.CreateCompatibleDC(dc)
            hOldBitmap = win32gui.SelectObject(hdcBitmap,hBitmap)
            bminfo = win32gui.GetObject(hBitmap)
            win32gui.SetStretchBltMode(dc,win32con.COLORONCOLOR)
            win32gui.StretchBlt(dc, 0, 0, wndwidth, wndheight, hdcBitmap, 0, 0, bminfo.bmWidth, bminfo.bmHeight, win32con.SRCCOPY)
            win32gui.SelectObject(hdcBitmap, hOldBitmap)
        
        win32gui.EndPaint(hWnd, ps)
        return 0

#--------------------------------------MAIN---------------------------------------
#mainWindow = MainWindow()
MainWindow()
