#####################################################
# Written by Kyle Michaels, see README.md for notes #
#####################################################

import tkinter as tk
import ctypes
from ctypes import wintypes
import time
import tempfile
import os
import sys

user32 = ctypes.WinDLL('user32', use_last_error=True)

INPUT_MOUSE    = 0
INPUT_KEYBOARD = 1
INPUT_HARDWARE = 2

KEYEVENTF_EXTENDEDKEY = 0x0001
KEYEVENTF_KEYUP       = 0x0002
KEYEVENTF_UNICODE     = 0x0004
KEYEVENTF_SCANCODE    = 0x0008

MAPVK_VK_TO_VSC = 0

##### ADD DATA #####
iconFile='HoneyBadgers48.ico'

if getattr(sys, 'frozen', False):
    application_path = sys._MEIPASS
elif __file__:
    application_path = os.path.dirname(__file__)

###### C struct definitions #####

wintypes.ULONG_PTR = wintypes.WPARAM

class MOUSEINPUT(ctypes.Structure):
    _fields_ = (("dx",          wintypes.LONG),
                ("dy",          wintypes.LONG),
                ("mouseData",   wintypes.DWORD),
                ("dwFlags",     wintypes.DWORD),
                ("time",        wintypes.DWORD),
                ("dwExtraInfo", wintypes.ULONG_PTR))

class KEYBDINPUT(ctypes.Structure):
    _fields_ = (("wVk",         wintypes.WORD),
                ("wScan",       wintypes.WORD),
                ("dwFlags",     wintypes.DWORD),
                ("time",        wintypes.DWORD),
                ("dwExtraInfo", wintypes.ULONG_PTR))

    def __init__(self, *args, **kwds):
        super(KEYBDINPUT, self).__init__(*args, **kwds)
        # some programs use the scan code even if KEYEVENTF_SCANCODE
        # isn't set in dwFflags, so attempt to map the correct code.
        if not self.dwFlags & KEYEVENTF_UNICODE:
            self.wScan = user32.MapVirtualKeyExW(self.wVk,
                                                 MAPVK_VK_TO_VSC, 0)

class HARDWAREINPUT(ctypes.Structure):
    _fields_ = (("uMsg",    wintypes.DWORD),
                ("wParamL", wintypes.WORD),
                ("wParamH", wintypes.WORD))

class INPUT(ctypes.Structure):
    class _INPUT(ctypes.Union):
        _fields_ = (("ki", KEYBDINPUT),
                    ("mi", MOUSEINPUT),
                    ("hi", HARDWAREINPUT))
    _anonymous_ = ("_input",)
    _fields_ = (("type",   wintypes.DWORD),
                ("_input", _INPUT))

LPINPUT = ctypes.POINTER(INPUT)

def _check_count(result, func, args):
    if result == 0:
        raise ctypes.WinError(ctypes.get_last_error())
    return args

user32.SendInput.errcheck = _check_count
user32.SendInput.argtypes = (wintypes.UINT, # nInputs
                             LPINPUT,       # pInputs
                             ctypes.c_int)  # cbSize

###### Classes #####
#a signle preplanned point object
class Point:
    def __init__(self, lat, lon, alt):
        if(lat>=0):
            self.NS=2 #North
        else:
            self.NS=8 #South
        self.lat=str(abs(lat)).zfill(8)[0:6]
        self.latd=str(abs(lat)).zfill(8)[6:8]

        if(lon>=0):
            self.EW=6 #East
        else:
            self.EW=3 #West
        self.lon=str(abs(lon)).zfill(8)[0:6]
        self.lond=str(abs(lon)).zfill(8)[6:8]

        self.alt = alt

###### Functions #####
def PressKey(hexKeyCode):
    x = INPUT(type=INPUT_KEYBOARD,
              ki=KEYBDINPUT(wVk=hexKeyCode))
    user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):
    x = INPUT(type=INPUT_KEYBOARD,
              ki=KEYBDINPUT(wVk=hexKeyCode,
                            dwFlags=KEYEVENTF_KEYUP))
    user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))

# msdn.microsoft.com/en-us/library/dd375731 source for scan codes
def numK(num):
    if(num<0|num>9):
        print("num out of bounds func only handles int 0-9")
        return 0x61
    else:
        return num+0x60

def LALT():
    return 0xA4

def LCTRL():
    return 0xA2

#couldn't find a scan code for Num Enter
def ENTER():
    return 0x0D

def sendNum(num):
    numStr=str(num)
    for ltr in numStr:
        key=int(ltr)
        sendKey(numK(key))
        time.sleep(.2)

def sendKey(key):
    PressKey(key)
    time.sleep(.2)
    ReleaseKey(key)

def sendCombo(mod, key):
    PressKey(mod)
    PressKey(key)
    time.sleep(.1)
    ReleaseKey(key)
    ReleaseKey(mod)

#Create the points from file for now
def CreatePlan():
    coord=entCoords.get("1.0",'end-1c')
    coord=coord.split("\n")
    plan=[]
    loop=0
    for line in coord:
        if(line==""):
            break
        elif(loop==0):
            lat=int(line)
            loop=1
        elif(loop==1):
            lon=int(line)
            loop=2
        elif(loop==2):
            elev=int(line)
            plan.append(Point(lat, lon, elev))
            loop=0
    return plan

def main():
    PP=CreatePlan()
    # give time for user to switch back to dcs
    try:
        ddd=int(boxDelay.get())
    except:
        ddd=15
    time.sleep()
    #start sending keys
    #ONCE AGAIN ASSUMING JDAMS ARE ALREAD SELECTED
    #Menu           L MDI PB 18
    sendCombo(LCTRL(),numK(6))
    time.sleep(.5)
    #JDAM DISPLAY   L MDI PB 11
    sendCombo(LCTRL(),numK(8))
    time.sleep(.5)
    #MSN Button     L MDI PB 4
    sendCombo(LCTRL(),numK(7))
    time.sleep(.5)
    #PP1            L MDI PB 6
    sendCombo(LCTRL(),numK(1))
    time.sleep(.5)
    #TGT UFC        L MDI PB 14
    sendCombo(LCTRL(),numK(9))
    time.sleep(.5)
    #POSITION       UFC OPTION 3
    sendCombo(LALT(),numK(3))
    time.sleep(.5)
    #lat            UFC OPTION 1
    sendCombo(LALT(),numK(1))
    time.sleep(.5)
    #Type latitude
    x=1
    for pnt in PP:
        sendCombo(LCTRL(),numK(x))
        time.sleep(.3)
        x+=1
        sendNum(pnt.NS)
        time.sleep(.2)
        sendNum(pnt.lat)
        sendKey(ENTER())
        time.sleep(1)
        sendNum(pnt.latd)
        sendKey(ENTER())
        time.sleep(.2)

    #lon            UFC OPTION 3
    sendCombo(LALT(),numK(3))
    #Type longitude
    x=1
    for pnt in PP:
        sendCombo(LCTRL(),numK(x))
        time.sleep(.3)
        x+=1
        sendNum(pnt.EW)
        time.sleep(.2)
        sendNum(pnt.lon)
        sendKey(ENTER())
        time.sleep(1)
        sendNum(pnt.lond)
        sendKey(ENTER())
        time.sleep(.2)

    #reselect elevation
    #TGT UFC        L MDI PB 14
    sendCombo(LCTRL(),numK(9))
    time.sleep(.5)
    #TGT UFC        L MDI PB 14
    sendCombo(LCTRL(),numK(9))
    time.sleep(.5)
    #ELEVATION      UFC OPTION 4
    sendCombo(LALT(),numK(4))
    time.sleep(.5)
    #FEET           UFC OPTION 3
    sendCombo(LALT(),numK(3))
    time.sleep(.5)
    #type elevations
    x=1
    for pnt in PP:
        sendCombo(LCTRL(),numK(x))
        time.sleep(.3)
        x+=1
        sendNum(pnt.alt)
        sendKey(ENTER())
        time.sleep(.2)

##### Create the GUI #####
#Create the window container
w=tk.Tk()
w.title("F18 JDAM \"Cartridge Loader\"")
w.iconbitmap(default=os.path.join(application_path, iconFile))
#create a label
lblHere=tk.Label(w,text="Paste Coordinates here:")
lblHere.grid(row=0, sticky="W", padx=10)
#create data entry box
entCoords=tk.Text(w, height=13, width=50)
entCoords.grid(row=1, column=0, columnspan=2, padx=10)
#create another label for the delay
lblDelay=tk.Label(w,text="Set Alt-tab Delay(sec):")
lblDelay.grid(row=2, column=0, sticky="E", padx=10, pady=10)
#create spin box
boxDelay=tk.Spinbox(w, values=(5,10,15,20,25,30,35,40,45,50,55,60), validate="all")
boxDelay.grid(row=2, column=1, sticky="W", padx=10)
#create run button
btnRun=tk.Button(w, text='Run', width=25, command=main)
btnRun.grid(row=3, column=0, columnspan=2, pady=7)
##### Run some code #####
w.mainloop()
# main()
