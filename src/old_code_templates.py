########################################################
"""rows = 0
while rows < 50:
    root.rowconfigure(rows, weight=1)
    root.columnconfigure(rows, weight=1)
    rows += 1

nb = ttk.Notebook(root)
nb.grid(row=1, column=0, columnspan=50, rowspan=49, sticky='NESW')

page_examples = ttk.Frame(nb)
nb.add(page_examples, text="examples")

page_weights = ttk.Frame(nb)
nb.add(page_weights, text="weights")"""
########################################################
"""photo = PhotoImage(file="overfitting_full.png")
label1 = Label(root, image=photo)
label1.pack()"""
########################################################
"""root = Tk()

canvas = Canvas(root, width=200, height=100)
canvas.pack()

blackLine = canvas.create_line(0,0,200,50)
redLine = canvas.create_line(0,100,200,50, fill="red")
greenBox = canvas.create_rectangle(25,25, 100,40, fill="green")
canvas.delete(redLine)

root.mainloop()"""
########################################################
"""import tkMessageBox
root = Tk()
tkMessageBox.showinfo("Window Title", "lorem ipsum dolor sit amet")
answer = tkMessageBox.askquestion('Question 1', 'Do you like silly faces')
if answer == 'yes':
    print("xD")

root.mainloop()"""
###########################################################
"""
def doNothing():
    print("Ok, no worries")

root = Tk()
##### Menu ***********************
menu = Menu(root)
root.config(menu=menu)
subMenu = Menu(menu)
menu.add_cascade(label="File", menu=subMenu)
subMenu.add_command(label="Down with this sort of thing!", command=doNothing)
subMenu.add_command(label="Careful now", command=doNothing)
subMenu.add_separator()
subMenu.add_command(label="Exit", command=quit)

editMenu = Menu(menu)
menu.add_cascade(label="Edit", menu=editMenu)
editMenu.add_command(label="Redo", command=doNothing)

##### Toolbar ************************
toolbar = Frame(root, bg="blue")
insertButton = Button(toolbar, text="Insert Image", command=doNothing)
insertButton.pack(side=LEFT, padx=2, pady=2)

printButton = Button(toolbar, text="Print", command=doNothing)
printButton.pack(side=LEFT, padx=2, pady=2)

toolbar.pack(fill=X)

##### Status bar ***************************
status = Label(root, text="Preparing to do Nothing", bd=1, relief=SUNKEN, anchor=W)
status.pack(side=BOTTOM, fill=X)

root.mainloop()
"""

#######################################################
"""class Application:

    def __init__(self, master):
        frame = Frame(master)
        frame.pack()

        self.printButton = Button(frame, text="print(message", command=self.printMessage))
        self.printButton.pack(side=LEFT)

        self.quitButton = Button(frame, text="Quit", command=frame.quit)
        self.quitButton.pack(side=LEFT)

    def printMessage(self):
        print("Well this actualy worked")

root = Tk()
root.title("NNviewer")
b = Application(root)

root.mainloop()"""
##################################################################
"""def leftClick(event):
    print("left")

def rightClick(event):
    print("right")

def middleClick(event):
    print("middle")

frame1 = Frame(root, width=300, height= 250)
frame1.bind("<Button-1>", leftClick)
frame1.bind("<Button-2>", middleClick)
frame1.bind("<Button-3>", rightClick)

button1 = Button(frame1, text="Do something")
button1.bind("<Button-1>", leftClick)

label1 = Label(frame1, text="Name")
label2 = Label(frame1, text="Password")

entry1 = Entry(frame1)
entry2 = Entry(frame1)

checkbox = Checkbutton(frame1, text="Keep me logged in")

frame1.pack()

label1.grid(row=0, sticky=E)
label2.grid(row=1, sticky=E)

entry1.grid(row=0, column=1)
entry2.grid(row=1, column=1)

checkbox.grid(columnspan=2 )
button1.grid(columnspan=2)"""
