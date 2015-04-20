from tkinter import *
import serial
import io
ser = ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
line = ser.readline()

print(line)

root = Tk()

root.title("RC Throttle Splitter")
root.geometry("300x300")

sliderCH2inLabelvar = StringVar()
sliderCH2inLabel = Label( root, textvariable=sliderCH2inLabelvar, relief=RAISED )
sliderCH2inLabelvar.set("CH2 from receiver")
sliderCH2inLabel.pack()

sliderCH2in = Scale(root, from_=800, to=2200, orient=HORIZONTAL)
sliderCH2in.pack()
sliderCH2in.set(2)


sliderCH3inLabelvar = StringVar()
sliderCH3inLabel = Label( root, textvariable=sliderCH3inLabelvar, relief=RAISED )
sliderCH3inLabelvar.set("CH3 from receiver")
sliderCH3inLabel.pack()

sliderCH3in = Scale(root, from_=800, to=2200, orient=HORIZONTAL)
sliderCH3in.pack()
sliderCH3in.set(3)


sliderCH2outLabelvar = StringVar()
sliderCH2outLabel = Label( root, textvariable=sliderCH2outLabelvar, relief=RAISED )
sliderCH2outLabelvar.set("CH2 out")
sliderCH2outLabel.pack()

sliderCH2out = Scale(root, from_=800, to=2200, orient=HORIZONTAL)
sliderCH2out.pack()
sliderCH2out.set(102)


sliderCH3outLabelvar = StringVar()
sliderCH3outLabel = Label( root, textvariable=sliderCH3outLabelvar, relief=RAISED )
sliderCH3outLabelvar.set("CH3 out")
sliderCH3outLabel.pack()

sliderCH3out = Scale(root, from_=800, to=2200, orient=HORIZONTAL)
sliderCH3out.pack()
sliderCH3out.set(103)

#// Buttons
def saveButtonCallBack():
   print("savebutton")
   ser.write(b"test$save:\n 1500 \n0 \n1 \n")

saveButton = Button(root, text ="Save", command = saveButtonCallBack)
saveButton.pack()

def loadButtonCallBack():
   print("loadbutton")
   ser.write(b"test$load:\n 3 \n5 \n7 \n")

loadButton = Button(root, text ="Load", command = loadButtonCallBack)
loadButton.pack()


def serialLoop():
	line = ser.readline()
	print(line)
	stemp = "CH3:"
	linetemp = line.decode(encoding='UTF-8')
	if "CH3:" in linetemp:
		#print("found ch3")
		s = linetemp[linetemp.find("CH3:")+4:];
		ch3invalue = int(s)
		sliderCH3in.set(ch3invalue)
	if "CH2:" in linetemp:
		#print("found ch2")
		s = linetemp[linetemp.find("CH2:")+4:];
		ch2invalue = int(s)
		sliderCH2in.set(ch2invalue)
	if "CH2out:" in linetemp:
		#print("found ch2out")
		s = linetemp[linetemp.find("CH2out:")+7:];
		ch2outvalue = int(s)
		sliderCH2out.set(ch2outvalue)
	if "CH3out:" in linetemp:
		#print("found ch3out")
		s = linetemp[linetemp.find("CH3out:")+7:];
		ch3outvalue = int(s)
		sliderCH3out.set(ch3outvalue)

# Load settings
	if "LOAD:" in linetemp:
		print("found LOAD")
		s = linetemp[linetemp.find("LOAD:")+5:];
		[x.strip() for x in s.split(',')]
		print(s)


	root.after(1,serialLoop)

root.after(100,serialLoop)
root.mainloop()


