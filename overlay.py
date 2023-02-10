import time
from pymem import *
from pymem.process import *
from pymem.ptypes import RemotePointer
import dearpygui.dearpygui as dpg
import threading
import ctypes
import sys

try:
    pm = pymem.Pymem("echovr.exe")
except Exception:
    ctypes.windll.user32.MessageBoxW(0, "Game Not Found, make sure it's running!", "Error!", 1)
    sys.exit(1)

gameModule = module_from_name(pm.process_handle, "echovr.exe").lpBaseOfDll
matchmakingModule = module_from_name(pm.process_handle, "pnsradmatchmaking.dll").lpBaseOfDll
pnsovr = module_from_name(pm.process_handle, "pnsovr.DLL").lpBaseOfDll

def GetPtrAddr(base, offsets):
    remote_pointer = RemotePointer(pm.process_handle, base)
    for offset in offsets:
        if offset != offsets[-1]:
            remote_pointer = RemotePointer(pm.process_handle, remote_pointer.value + offset)
        else:
            return remote_pointer.value + offset

# Addresses
BaseCoords = GetPtrAddr(gameModule + 0x020A3138,[0x60, 0x2A0, 0xF8, 0xEA0, 0xD8, 0x134, 0x118])
BasePlayerList = GetPtrAddr(matchmakingModule + 0x009C49D8,[0x88, 0x0, 0x440, 0x28, 0x40, 0x378, 0x3C])
BaseView = GetPtrAddr(gameModule + 0x020A3138,[0x60, 0x2A0, 0xF8, 0xEA0, 0xD8, 0x134, 0x118]) - 196

def update_value():
    while True:
      dpg.set_value(text_label, "("+str(round(pm.read_float(BaseCoords),2))+" ,"+str(round(pm.read_float(BaseCoords+4),2))+" ,"+str(round(pm.read_float(BaseCoords+8),2))+")")
      time.sleep(0.1)

def update_playerlistvalues():
    while True:
        for i in range(10):
              thehex = "0xD8"
              result = int(thehex, 16) * i
              if pm.read_string(BasePlayerList+result) == "":
                  dpg.set_value(globals()['playerslot' + str(i)], "Player #"+str(i)+": Player Not Detected")
              else:
                dpg.set_value(globals()['playerslot' + str(i)], "Player #"+str(i)+": "+pm.read_string(BasePlayerList+result))
        time.sleep(0.4)

def update_speedvalue():
    while True:
      dpg.set_value(speed_label, "Speed: "+ str(round(pm.read_float(BaseCoords-28),2))+ " M/s")
      time.sleep(0.1)

def update_ViewX():
    while True:
        dpg.set_value(ViewX_label, "ViewX: "+ str(round(pm.read_float(BaseView),2)))
        time.sleep(0.4)
def update_ViewY():
    while True:
        dpg.set_value(ViewY_label, "ViewY: "+ str(round(pm.read_float(BaseView+4),2)))
        time.sleep(0.4)

dpg.create_context()
dpg.create_viewport(title='Echo Overlay', width=200, height=515)
dpg.setup_dearpygui()

with dpg.window(label="Echo Overlay, Welcome"):
    dpg.set_viewport_always_top(True)
    dpg.add_text("---------- Account Info ---------")
    dpg.add_text("Username: "+  pm.read_string(pnsovr + 0xA01B80))
    dpg.add_text("Scoped ID: "+  pm.read_string(pnsovr + 0xA01BF0))
    dpg.add_text("---------------------------------")
    text_label = dpg.add_text("XYZ")
    speed_label = dpg.add_text("Speed: Null M/s")
    ViewX_label = dpg.add_text("ViewX")
    ViewY_label = dpg.add_text("ViewY")
    dpg.add_text("---------- Player List ----------")
    playerslot0 = dpg.add_text("Player #"+":")
    playerslot1 = dpg.add_text("Player #"+":")
    playerslot2 = dpg.add_text("Player #"+":")
    playerslot3 = dpg.add_text("Player #"+":")
    playerslot4 = dpg.add_text("Player #"+":")
    playerslot5 = dpg.add_text("Player #"+":")
    playerslot6 = dpg.add_text("Player #"+":")
    playerslot7 = dpg.add_text("Player #"+":")
    playerslot8 = dpg.add_text("Player #"+":")
    playerslot9 = dpg.add_text("Player #"+":")
    playerlistupdate = threading.Thread(target=update_playerlistvalues)
    speedupdate = threading.Thread(target=update_speedvalue)
    viewXUpdate = threading.Thread(target=update_ViewX)
    viewYUpdate =  threading.Thread(target=update_ViewY)
    thread = threading.Thread(target=update_value)
    viewXUpdate.start()
    viewYUpdate.start()
    thread.start()
    speedupdate.start()
    playerlistupdate.start()
    
      



dpg.show_viewport()
dpg.start_dearpygui()

dpg.destroy_context()
