# Import the required libraries
from tkinter import *
from tkinter import ttk
import minimalmodbus

# Create an instance of Tkinter Frame
win = Tk()

# Set the geometry
win.geometry("1024x768")
win.resizable(width=FALSE,height=FALSE)

instrument = minimalmodbus.Instrument('COM3', 1, mode= minimalmodbus.MODE_RTU)
instrument.serial.baudrate = 19200
instrument.serial.bytesize = 8
instrument.serial._stopbits = 1
instrument.serial.parity = minimalmodbus.serial.PARITY_EVEN
instrument.serial.timeout = 1

def Start_button():
    instrument.write_register(0x2000, 0b10, functioncode=6)

def Stop_button():
    instrument.write_register(0x2000, 0b01, functioncode=6)

def Frekvence(udalost):
    para = frekvence.get() * 100
    instrument.write_register(0x2001, para , functioncode=6)
    
def updateProud():
    proudHodnota['text'] = str(instrument.read_register(0x2104)/100)+"A"
    win.after(500,updateProud)

def updateFrekvence():
    frekvenceHodnota['text'] = str(instrument.read_register(0x2103)/100)+"Hz"
    win.after(500,updateFrekvence)

def updateError():
    precti = instrument.read_register(0x2100)
    if precti == 0:
        errorHodnota['text'] = "No errors occurred"
    
    elif precti ==1:
        errorHodnota['text'] = "Over-current"

    elif precti ==2:
        errorHodnota['text'] = "Over-voltage"
    
    elif precti ==3:
        errorHodnota['text'] = "Overheat"

    elif precti ==5:
        errorHodnota['text'] = "Overload1"
    
    elif precti == 6:
        errorHodnota['text'] = "External fault"
    
    elif precti == 7:
        errorHodnota['text'] = "CPU failure"

    elif precti == 8:
        errorHodnota['text'] = "Hardware protection failure"
    
    elif precti == 9:
        errorHodnota['text'] = "Current exceeds 2 times rated current during accel"
    
    elif precti == 10:
        errorHodnota['text'] = "Current exceeds 2 times rated current during decel"
    
    elif precti == 11:
        errorHodnota['text'] = "Current exceeds 2 times rated current during steady state operation"
    
    elif precti == 12:
        errorHodnota['text'] = "Reserved"
    
    elif precti == 13:
        errorHodnota['text'] = "Reserved"
    
    elif precti == 14:
        errorHodnota['text'] = "Low voltage"
    
    elif precti == 15:
        errorHodnota['text'] = "CPU failure 1"
    
    elif precti == 16:
        errorHodnota['text'] = "CPU failure 2"
    
    elif precti == 17:
        errorHodnota['text'] = "Base block"
    
    elif precti == 18:
        errorHodnota['text'] = "Overload"
    
    elif precti == 19:
        errorHodnota['text'] = "Auto accel/decel failure"
    
    elif precti == 20:
        errorHodnota['text'] = "Software protection enable"
    
    win.after(500,updateError)

#nastaveni slideru
frekvence = Scale(win,from_= 0,to=400,orient=HORIZONTAL,length=600, command=Frekvence)
frekvence.place(x= 212,y=368)
#nastaveni start tlacitka
start= Button(win,bg="green",text="START", command= Start_button)
start.place(x=212,y=450)

#nastaveni STOP tlacitka
stop = Button(win,bg="red",text="STOP", command= Stop_button)
stop.place(x=512,y=450)

#reset tlacitko
reset = Button(win,bg="yellow",text="RESET")
reset.place(x=760,y=450)

proud = Label(win,text="Proud:")
proud.place(x=185,y= 50 )
proudHodnota = Label(win)
proudHodnota.place(x=260,y=50)

frekvencevystup = Label(win,text="Frekvence:")
frekvencevystup.place(x=185,y= 100 )
frekvenceHodnota = Label(win)
frekvenceHodnota.place(x=260,y=100)

error = Label(win,text="Error:")
error.place(x=185,y= 150 )
errorHodnota = Label(win)
errorHodnota.place(x=260,y=150)

updateProud()
updateFrekvence()
updateError()
win.mainloop()