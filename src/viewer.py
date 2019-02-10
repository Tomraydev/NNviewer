#!/usr/bin/python

# Libraries for scripts
#import network
import network # Neural net classes and algorithms
import numpy as np
import cPickle # loading networks and test data
import time # calculating the execution time

# Libraries for the GUI
from Tkinter import * # Creating the GUI
import ttk # 'notebook' creating tabs
import tkFileDialog # Browsing files
import matplotlib.pyplot as plt

# ************ Load test data***************
def load_test_data():
    start = time.clock()

    data_file = open("../data/test_data.pkl", "rb")
    global test_data
    test_data = cPickle.load(data_file)
    data_file.close()

    print "Loaded the data in %f seconds" % (time.clock() - start)

    nb.tab(1, state="normal") # enable examples page
# *********** Load the network *************
def load_network():
    fileName = tkFileDialog.askopenfilename(parent=root, initialdir = "../networks/")
    #fileName = "../networks/net_01.pkl"
    if not fileName:
        print "Error opening file"
        return

    start = time.clock()
    file_network = open(fileName, 'rb') #'./networks/net_pickle'
    global net
    net = cPickle.load(file_network)
    file_network.close()

    print "\nNetwork loaded:"
    print "Sizes:    ", net.sizes
    print "Loaded the network in %.3f seconds" % (time.clock() - start)

    nb.tab(2, state="normal") # enable weights page
    btn_load_second.config(state="normal")

    # Update weights page
    start = time.clock()
    layer_id = 0
    for neuron_id in range(net.sizes[layer_id+1]):

        # Calculate the relevant importance of the weight
        weight_relevance = 0
        for w in range(len(net.weights[0][0])):
            weight_relevance += abs(net.weights[0][neuron_id][w])
        weight_relevance /= len(net.weights[0][0])
        weight_relevance_str = "I: %.2f" % weight_relevance

        bias = net.biases[0][neuron_id]
        bias_str = "B: %.2f" % bias

        save_str = "../images/neuron_%d_%d.png" % (layer_id, neuron_id)
        plt.imsave(save_str, net.weights[layer_id][neuron_id].reshape(28,28), cmap='viridis') # save the image of weights

        if (neuron_id % 8 == 0):
            frame_neuron_column = Frame(page_weights)
            frame_neuron_column.pack(side="left", padx=32)

        frame_neuron = Frame(frame_neuron_column)
        frame_neuron.pack()
        l_id = Label(frame_neuron, text=neuron_id, width=2)
        l_id.pack(side="left")
        neuron_png = PhotoImage(file=save_str).zoom(2,2) # Load the image
        l_img = Label(frame_neuron, image=neuron_png)
        l_img.image = neuron_png # hack: if you don't use this, the garbage collector will destroy the image
        l_img.pack(side="left")
        l_weight_relevance = Label(frame_neuron, text=weight_relevance_str, width=10)
        l_weight_relevance.pack()
        l_bias = Label(frame_neuron, text=bias_str, width=10)
        l_bias.pack()

    print "Loaded the images in %.3f seconds" % (time.clock() - start)

def generate_second_layer():
    page_second_weights = ttk.Frame(nb)
    nb.add(page_second_weights, text="second weights", state="normal")

    layer_id = 1
    for neuron_id in range(net.sizes[layer_id+1]):

        second_img = np.zeros(784)
        for sub_neuron_id in range(net.sizes[layer_id]):
            #bias_vector = np.full( (784), net.biases[layer_id-1][sub_neuron_id])
            second_img = second_img + net.weights[layer_id-1][sub_neuron_id] * net.weights[layer_id][neuron_id][sub_neuron_id]

        save_str = "../images/neuron_%d_%d.png" % (layer_id, neuron_id)
        plt.imsave(save_str, second_img.reshape(28,28), cmap='inferno') # save the image of weights

        if (neuron_id % 3 == 0):
            frame_neuron_column = Frame(page_second_weights)
            frame_neuron_column.pack(side="left", padx=32)

        frame_neuron = Frame(frame_neuron_column)
        frame_neuron.pack()
        l_id = Label(frame_neuron, text=neuron_id, width=2)
        l_id.pack(side="left")
        neuron_png = PhotoImage(file=save_str).zoom(2,2) # Load the image
        l_img = Label(frame_neuron, image=neuron_png)
        l_img.image = neuron_png # hack: if you don't use this, the garbage collector will destroy the image
        l_img.pack(side="left")

# *************** classes ******************

class Example:

    def __init__(self, master):
        self.l_id = Label(master)
        self.l_id.pack()

        number_png = PhotoImage(file='../important_images/placehold.png').zoom(8,8) # Load the image
        self.l_img = Label(master, image=number_png)
        self.l_img.image = number_png # hack: if you don't use this, the garbage collector will destroy the image
        self.l_img.pack(side="left")
        self.data_id = 0
        self.correct_num = 0
        self.ex_label = []

        for i in range(10):
            self.ex_label.append( Label(master, text=(str(i) + ": ---") ))
            self.ex_label[i].pack()

    def load_image(self, data_id=0):
        data_id = int(data_id)

        if data_id<0 or data_id > (len(test_data)-1):
            print "incorrect index"
            return

        self.l_id.configure(text=data_id)
        self.data_id = data_id
        self.correct_num = test_data[data_id][1]

        save_str = "../images/number_%d.png" % (data_id)
        plt.imsave(save_str, test_data[data_id][0].reshape(28,28), cmap='gray') # save the image

        number_png = PhotoImage(file=save_str).zoom(8,8) # Load the image
        self.l_img.configure(image=number_png)
        self.l_img.image = number_png # hack: if you don't use this, the garbage collector will destroy the image

        for i in range(len(self.ex_label)): # reset highlighting
            self.ex_label[i].config(fg="black")

        output = net.feedforward(test_data[data_id][0]) # classify the image
        i_max = 0
        value_max = 0
        for i in range(len(self.ex_label)):
            output_str = "%d:  %f" % (i, output[i])
            self.ex_label[i].config(text=output_str)
            if output[i] > value_max:
                value_max = output[i]
                i_max = i

        self.ex_label[i_max].config(fg="red")

        for i in range(len(self.ex_label)): # highlight the correct number
            if i == self.correct_num:
                self.ex_label[i].config(fg="green")
                break

# *************** GUI **********************
root = Tk()
root.title("NNviewer")
root.geometry('1024x576')

nb = ttk.Notebook(root)
nb.pack(fill='both', expand='yes')
# ********** Tabs ************
page_start = ttk.Frame(nb)
nb.add(page_start, text="start")

page_examples = ttk.Frame(nb)
nb.add(page_examples, text="examples", state="disabled")

page_weights = ttk.Frame(nb)
nb.add(page_weights, text="weights", state="disabled")

# ***************** Start page ********************
frame_start = Frame(page_start)
frame_start.pack(pady=32)

btn_load_data = Button(frame_start, text="load the data", command=load_test_data)
btn_load_data.pack(side="left")

btn_load_net = Button(frame_start, text="load the network", command=load_network)
btn_load_net.pack(side="left")

btn_load_second = Button(frame_start, text="second layer", command=generate_second_layer, state="disabled")
btn_load_second.pack(pady=32)

# ***************** Examples page *****************
frame_output = Frame(page_examples)
frame_output.pack()
example_viewer = Example(frame_output)

frame_bottom = Frame(page_examples)
frame_bottom.pack(ipadx=8, ipady=8)

btn_previous = Button(frame_bottom, text="previous", command=lambda:example_viewer.load_image(example_viewer.data_id-1) )
btn_previous.pack(side="left")

entry_index = Entry(frame_bottom)
entry_index.pack(side="left", ipadx=4, ipady=4, padx=4)

btn_next = Button(frame_bottom, text="next", command=lambda:example_viewer.load_image(example_viewer.data_id+1) )
btn_next.pack(side="left")

btn_submit = Button(page_examples, text="go to index", command=lambda:example_viewer.load_image(entry_index.get() ))
btn_submit.pack()

# ***************** weights page *****************
# auto-populated
# ************************************************
root.mainloop()
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
    print "xD"

root.mainloop()"""
###########################################################
"""
def doNothing():
    print "Ok, no worries"

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

        self.printButton = Button(frame, text="Print message", command=self.printMessage)
        self.printButton.pack(side=LEFT)

        self.quitButton = Button(frame, text="Quit", command=frame.quit)
        self.quitButton.pack(side=LEFT)

    def printMessage(self):
        print "Well this actualy worked"

root = Tk()
root.title("NNviewer")
b = Application(root)

root.mainloop()"""
##################################################################
"""def leftClick(event):
    print "left"

def rightClick(event):
    print "right"

def middleClick(event):
    print "middle"

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
