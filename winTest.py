#!/usr/bin/env python3.6
from tkinter import *
import colorsys
import math
import sys
import time
import pexpect


class Window(Frame):

    def __init__(self,master=None):
        Frame.__init__(self,master)
        self.master = master
        self.init_window()        
        
        self.bulb = "98:7B:F3:67:4E:8A"

        # Run gatttool interactively.
        self.gatt = pexpect.spawn('gatttool -I')

        # Connect to the device.
        self.gatt.sendline('connect {0}'.format(self.bulb))
        self.gatt.expect('Connection successful')


    def init_window(self):

        self.master.title("FluxGUI")

        self.pack(fill=BOTH, expand=1)

        self.w = Scale(self, from_=0, to=255, length=175)
        self.w.place(x=100,y = 5)

        greenButton = Button(self,text="Green",command=lambda: self.send_color(0,self.w.get(),0))
        greenButton.config(width=5)
        greenButton.place(x=5,y=5)

        redButton = Button(self,text="Red",command=lambda: self.send_color(self.w.get(),0,0))
        redButton.config(width=5)
        redButton.place(x=5,y=55)

        blueButton = Button(self,text="Blue",command=lambda: self.send_color(0,0,self.w.get()))
        blueButton.config(width=5)
        blueButton.place(x=5,y=105)

        warmButton = Button(self,text="Warm",command=lambda: self.send_warm(self.w.get()))
        warmButton.config(width=5)
        warmButton.place(x=5,y=155)

        self.redSlider = Scale(self,from_=0, to=255, orient=HORIZONTAL,command=self.color_slider)
        self.redSlider.place(x=200,y=5)

        self.greenSlider = Scale(self,from_=0, to=255, orient=HORIZONTAL,command=self.color_slider)
        self.greenSlider.place(x=200,y=55)

        self.blueSlider = Scale(self,from_=0, to=255, orient=HORIZONTAL,command=self.color_slider)
        self.blueSlider.place(x=200,y=105)

        reconnectButton = Button(self,text="Reconnect",command=self.reconnect())
        reconnectButton.place(x = 250,y = 205)

    def send_warm(self,i):
        line = 'char-write-cmd 0x002e 560000ff{0:02X}0faa'.format(i)
        self.gatt.sendline(line)

    def send_color(self,r,g,b):
        line = 'char-write-cmd 0x002e 56{0:02X}{1:02X}{2:02X}00f0aa'.format(r, g, b)
        self.gatt.sendline(line)

    def send_green(self):
        r = 0
        g = 255
        b = 0
        line = 'char-write-cmd 0x002e 56{0:02X}{1:02X}{2:02X}00f0aa'.format(r, g, b)
        self.gatt.sendline(line)

    def color_slider(self,event):
        r = self.redSlider.get()
        g = self.greenSlider.get()
        b = self.blueSlider.get()
        line = 'char-write-cmd 0x002e 56{0:02X}{1:02X}{2:02X}00f0aa'.format(r, g, b)
        self.gatt.sendline(line)

    def reconnect(self):
        # Run gatttool interactively.
        self.gatt = pexpect.spawn('gatttool -I')

        # Connect to the device.
        self.bulb = "98:7B:F3:67:4E:8A"

        self.gatt.sendline('connect {0}'.format(self.bulb))
        self.gatt.expect('Connection successful')


root = Tk()
root.geometry("400x300")

app = Window(root)
root.mainloop()
