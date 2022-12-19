# Importace potrebnych knihoven
from tkinter import *
from tkinter import ttk
import minimalmodbus

# vytvoreni okna 
win = Tk()

# nastaveni geometrie
win.geometry("1024x768")
win.resizable(width=FALSE,height=FALSE)

#nastaveni komunikace s menicem
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

def Reset_button():
    instrument.write_register(0x2002, 0b10, functioncode=6)

def Rev_button():
    instrument.write_register(0x2000, 0b100000, functioncode=6)
    revGreen()

def Fwd_button():
    instrument.write_register(0x2000, 0b10000, functioncode=6)
    fwdGreen()

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
        errorHodnota.config(fg="green")
    
    elif precti ==1:
        errorHodnota['text'] = "Over-current"
        errorHodnota.config(fg="red")

    elif precti ==2:
        errorHodnota['text'] = "Over-voltage"
        errorHodnota.config(fg="red")
    
    elif precti ==3:
        errorHodnota['text'] = "Overheat"
        errorHodnota.config(fg="red")

    elif precti ==5:
        errorHodnota['text'] = "Overload1"
        errorHodnota.config(fg="red")
    
    elif precti == 6:
        errorHodnota['text'] = "External fault"
        errorHodnota.config(fg="red")
    
    elif precti == 7:
        errorHodnota['text'] = "CPU failure"
        errorHodnota.config(fg="red")

    elif precti == 8:
        errorHodnota['text'] = "Hardware protection failure"
        errorHodnota.config(fg="red")
    
    elif precti == 9:
        errorHodnota['text'] = "Current exceeds 2 times rated current during accel"
        errorHodnota.config(fg="red")
    
    elif precti == 10:
        errorHodnota['text'] = "Current exceeds 2 times rated current during decel"
        errorHodnota.config(fg="red")
    
    elif precti == 11:
        errorHodnota['text'] = "Current exceeds 2 times rated current during steady state operation"
        errorHodnota.config(fg="red")
    
    elif precti == 12:
        errorHodnota['text'] = "Reserved"
        errorHodnota.config(fg="red")
    
    elif precti == 13:
        errorHodnota['text'] = "Reserved"
        errorHodnota.config(fg="red")
    
    elif precti == 14:
        errorHodnota['text'] = "Low voltage"
        errorHodnota.config(fg="red")
    
    elif precti == 15:
        errorHodnota['text'] = "CPU failure 1"
        errorHodnota.config(fg="red")
    
    elif precti == 16:
        errorHodnota['text'] = "CPU failure 2"
        errorHodnota.config(fg="red")
    
    elif precti == 17:
        errorHodnota['text'] = "Base block"
        errorHodnota.config(fg="red")
    
    elif precti == 18:
        errorHodnota['text'] = "Overload"
        errorHodnota.config(fg="red")
    
    elif precti == 19:
        errorHodnota['text'] = "Auto accel/decel failure"
        errorHodnota.config(fg="red")
    
    elif precti == 20:
        errorHodnota['text'] = "Software protection enable"
        errorHodnota.config(fg="red")
    
    win.after(500,updateError)

def motorStatus():
    precti = instrument.read_register(0x2101)
    
    if precti == 1280:
        statusHodnota['text'] = "Motor Stopped"
        fwdGreen()

    elif  precti == 1304:
        statusHodnota['text'] = "Motor Stopped"
        revGreen()
    
    elif precti == 1283:
        statusHodnota['text'] = "Motor Running with FWD direction"
        fwdGreen()

    elif precti == 1307:
        statusHodnota['text'] = "Motor running with REV direction"
        revGreen()

    elif precti == 1291:
        statusHodnota['text'] = "Motor changing direction to the FWD"

    elif precti == 1299:
        statusHodnota['text'] = "Motor changing direction to the REV"

    elif precti == 1281 or precti == 1305:
        statusHodnota['text'] = "Motor stopping right now"
    
    win.after(500, motorStatus)

def revGreen():
    fwd.config(bg="grey")
    rev.config(bg="green")

def fwdGreen():
    fwd.config(bg="green")
    rev.config(bg="grey")

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
reset = Button(win,bg="yellow",text="RESET", command= Reset_button)
reset.place(x=760,y=450)

fwd = Button(win, bg="grey", text="FWD", command=Fwd_button)
fwd.place(x=212, y=500)

rev = Button(win, bg="grey", text="REV", command=Rev_button)
rev.place(x=212, y=550)

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

motor = Label(win, text= "Motor status:")
motor.place(x=450, y=150)
statusHodnota = Label(win)
statusHodnota.place(x=550, y=150)

frekvence.set(instrument.read_register(0x2102)/100)
updateProud()
updateFrekvence()
updateError()
motorStatus()
win.mainloop()