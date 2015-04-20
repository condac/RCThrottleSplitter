from tkinter import *
import serial
import io
import Pmw

ser = ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
line = ser.readline()
print(line)


root = Tk()
notebook = Pmw.NoteBook(root)
notebook.pack(fill = 'both', expand = 1, padx = 10, pady = 10)
page = notebook.add('Live')
notebook.tab('Live').focus_set()

root.title("RC Throttle Splitter")
#root.geometry("300x300")
# Create the "Toolbar" contents of the page.
group = Pmw.Group(page, tag_text = 'Live values')
group.pack(fill = 'both', expand = 1, padx = 10, pady = 10)

sliderCH2inLabelvar = StringVar()
sliderCH2inLabel = Label( group.interior(), textvariable=sliderCH2inLabelvar, relief=RAISED )
sliderCH2inLabelvar.set("CH2 from receiver")
sliderCH2inLabel.pack()

sliderCH2in = Scale(group.interior(), from_=800, to=2200, orient=HORIZONTAL)
sliderCH2in.pack()
sliderCH2in.set(2)


sliderCH3inLabelvar = StringVar()
sliderCH3inLabel = Label( group.interior(), textvariable=sliderCH3inLabelvar, relief=RAISED )
sliderCH3inLabelvar.set("CH3 from receiver")
sliderCH3inLabel.pack()

sliderCH3in = Scale(group.interior(), from_=800, to=2200, orient=HORIZONTAL)
sliderCH3in.pack()
sliderCH3in.set(3)


sliderCH2outLabelvar = StringVar()
sliderCH2outLabel = Label( group.interior(), textvariable=sliderCH2outLabelvar, relief=RAISED )
sliderCH2outLabelvar.set("CH2 out")
sliderCH2outLabel.pack()

sliderCH2out = Scale(group.interior(), from_=800, to=2200, orient=HORIZONTAL)
sliderCH2out.pack()
sliderCH2out.set(102)


sliderCH3outLabelvar = StringVar()
sliderCH3outLabel = Label( group.interior(), textvariable=sliderCH3outLabelvar, relief=RAISED )
sliderCH3outLabelvar.set("CH3 out")
sliderCH3outLabel.pack()

sliderCH3out = Scale(group.interior(), from_=800, to=2200, orient=HORIZONTAL)
sliderCH3out.pack()
sliderCH3out.set(103)



# Toggle buttons
# Create the "Toolbar" contents of the page.
group = Pmw.Group(page, tag_text = 'Settings')
group.pack(fill = 'both', expand = 1, padx = 10, pady = 10)
# Create first button
CH2ReverseVar = IntVar()
CH2ReverseButton = Checkbutton(group.interior(), text = 'CH2 Reverse', variable=CH2ReverseVar)
CH2ReverseButton.pack()
# Create button
CH3ReverseVar = IntVar()
CH3ReverseButton = Checkbutton(group.interior(), text = 'CH3 Reverse', variable=CH3ReverseVar)
CH3ReverseButton.pack()

#// Buttons
def saveButtonCallBack():
   print("savebutton")
   outstring = "test$save:\n "+str(1500)+" \n "+ str(0) +" \n "+ str(0) +" \n"
   ser.write(outstring.encode('utf-8'))

saveButton = Button(group.interior(), text ="Save", command = saveButtonCallBack)
saveButton.pack()

def loadButtonCallBack():
   print("loadbutton")
   ser.write(b"test$load:\n 3 \n5 \n7 \n")

loadButton = Button(group.interior(), text ="Load", command = loadButtonCallBack)
loadButton.pack()

##Serial loop
def serialLoop():
	line = ser.readline()
	
	stemp = "CH3:"
	linetemp = line.decode(encoding='UTF-8')
	if "CH3:" in linetemp:
		#print("found ch3")
		s = linetemp[linetemp.find("CH3:")+4:];
		ch3invalue = int(s)
		sliderCH3in.set(ch3invalue)
	elif "CH2:" in linetemp:
		#print("found ch2")
		s = linetemp[linetemp.find("CH2:")+4:];
		ch2invalue = int(s)
		sliderCH2in.set(ch2invalue)
	elif "CH2out:" in linetemp:
		#print("found ch2out")
		s = linetemp[linetemp.find("CH2out:")+7:];
		ch2outvalue = int(s)
		sliderCH2out.set(ch2outvalue)
	elif "CH3out:" in linetemp:
		#print("found ch3out")
		s = linetemp[linetemp.find("CH3out:")+7:];
		ch3outvalue = int(s)
		sliderCH3out.set(ch3outvalue)

# Load settings
	elif "LOAD:" in linetemp:
		print("found LOAD")
		print(line)
		s = linetemp[linetemp.find("LOAD:")+5:];
		[x.strip() for x in s.split(',')]
		print(s[0])
		print(s[1])
		print(s[2])
		print(s[3])
	else :
		print(line)

	root.after(1,serialLoop)

notebook.setnaturalsize()
root.after(100,serialLoop)
root.mainloop()


