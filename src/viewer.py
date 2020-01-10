#!/usr/bin/env python3

# Libraries for scripts
import network  # Neural net classes and algorithms
import time
import pickle
import numpy as np
import matplotlib.pyplot as plt

# Libraries for the GUI
from tkinter import Tk, Frame, Button, PhotoImage, Label, Entry  # Creating the GUI
from tkinter import ttk  # 'notebook' creating tabs
from tkinter import filedialog  # Browsing files

# Custom
from example_viewer import ExampleViewer


class NNviewer:
    def __init__(self, root):
        self.root = root
        self.root.title("NNviewer")
        self.root.geometry("1024x576")

        self.load_test_data()
        self.net = None

        # *************** GUI **********************
        self.nb = ttk.Notebook(root)
        self.nb.pack(fill="both", expand="yes")
        # ********** Tabs ************
        self.page_start = ttk.Frame(self.nb)
        self.nb.add(self.page_start, text="start")

        self.page_examples = ttk.Frame(self.nb)
        self.nb.add(self.page_examples, text="examples", state="normal")

        self.page_weights = ttk.Frame(self.nb)
        self.nb.add(self.page_weights, text="weights", state="disabled")

        # ***************** Start page ********************
        self.frame_start = Frame(self.page_start)
        self.frame_start.pack(pady=32)

        self.btn_load_net = Button(
            self.frame_start, text="load the network", command=self.load_network
        )
        self.btn_load_net.pack(side="left")

        self.btn_load_second = Button(
            self.frame_start,
            text="second layer",
            command=self.generate_second_layer,
            state="disabled",
        )
        self.btn_load_second.pack(pady=32)

        # ***************** Examples page *****************
        frame_output = Frame(self.page_examples)
        frame_output.pack()
        self.example_viewer = ExampleViewer(frame_output, self.test_data, self.net)

        frame_bottom = Frame(self.page_examples)
        frame_bottom.pack(ipadx=8, ipady=8)

        self.btn_previous = Button(
            frame_bottom,
            text="previous",
            command=lambda: self.example_viewer.load_image(self.example_viewer.data_id - 1),
        )
        self.btn_previous.pack(side="left")

        entry_index = Entry(frame_bottom)
        entry_index.pack(side="left", ipadx=4, ipady=4, padx=4)

        self.btn_next = Button(
            frame_bottom,
            text="next",
            command=lambda: self.example_viewer.load_image(self.example_viewer.data_id + 1),
        )
        self.btn_next.pack(side="left")

        self.btn_submit = Button(
            self.page_examples,
            text="go to index",
            command=lambda: self.example_viewer.load_image(entry_index.get()),
        )
        self.btn_submit.pack()

    def load_test_data(self):
        data_file = open("../data/test_data.pkl", "rb")
        self.test_data = pickle.load(data_file, encoding="latin1")
        data_file.close()

    def load_network(self):
        fileName = filedialog.askopenfilename(parent=root, initialdir="../networks/")
        # fileName = "../networks/net_01.pkl"
        if not fileName:
            print("Error opening file")
            return

        start = time.clock()
        file_network = open(fileName, "rb")  #'./networks/net_pickle'
        self.net = pickle.load(file_network, encoding="latin1")
        file_network.close()

        print("\nNetwork loaded:")
        print("Sizes:    ", self.net.sizes)
        print("Loaded the network in %.3f seconds" % (time.clock() - start))

        self.nb.tab(2, state="normal")  # enable weights page
        self.btn_load_second.config(state="normal")

        # Update weights page
        start = time.clock()
        layer_id = 0
        for neuron_id in range(self.net.sizes[layer_id + 1]):

            # Calculate the relevant importance of the weight
            weight_relevance = 0
            for w in range(len(self.net.weights[0][0])):
                weight_relevance += abs(self.net.weights[0][neuron_id][w])
            weight_relevance /= len(self.net.weights[0][0])
            weight_relevance_str = "I: %.2f" % weight_relevance

            bias = self.net.biases[0][neuron_id]
            bias_str = "B: %.2f" % bias

            save_str = "../output/neuron_%d_%d.png" % (layer_id, neuron_id)
            plt.imsave(
                save_str,
                self.net.weights[layer_id][neuron_id].reshape(28, 28),
                cmap="viridis",
            )  # save the image of weights

            if neuron_id % 8 == 0:
                frame_neuron_column = Frame(self.page_weights)
                frame_neuron_column.pack(side="left", padx=32)

            frame_neuron = Frame(frame_neuron_column)
            frame_neuron.pack()
            l_id = Label(frame_neuron, text=neuron_id, width=2)
            l_id.pack(side="left")
            neuron_png = PhotoImage(file=save_str).zoom(2, 2)  # Load the image
            l_img = Label(frame_neuron, image=neuron_png)
            l_img.image = (
                neuron_png
            )  # if you don't use this, the garbage collector will destroy the image
            l_img.pack(side="left")
            l_weight_relevance = Label(
                frame_neuron, text=weight_relevance_str, width=10
            )
            l_weight_relevance.pack()
            l_bias = Label(frame_neuron, text=bias_str, width=10)
            l_bias.pack()

        print("Loaded the image in %.3f seconds" % (time.clock() - start))

    def generate_second_layer(self):
        page_second_weights = ttk.Frame(self.nb)
        self.nb.add(page_second_weights, text="second weights", state="normal")

        layer_id = 1
        for neuron_id in range(self.net.sizes[layer_id + 1]):

            second_img = np.zeros(784)
            for sub_neuron_id in range(self.net.sizes[layer_id]):
                # bias_vector = np.full( (784), net.biases[layer_id-1][sub_neuron_id])
                second_img = (
                    second_img
                    + self.net.weights[layer_id - 1][sub_neuron_id]
                    * self.net.weights[layer_id][neuron_id][sub_neuron_id]
                )

            save_str = "../output/neuron_%d_%d.png" % (layer_id, neuron_id)
            plt.imsave(
                save_str, second_img.reshape(28, 28), cmap="inferno"
            )  # save the image of weights

            if neuron_id % 3 == 0:
                frame_neuron_column = Frame(page_second_weights)
                frame_neuron_column.pack(side="left", padx=32)

            frame_neuron = Frame(frame_neuron_column)
            frame_neuron.pack()
            l_id = Label(frame_neuron, text=neuron_id, width=2)
            l_id.pack(side="left")
            neuron_png = PhotoImage(file=save_str).zoom(2, 2)  # Load the image
            l_img = Label(frame_neuron, image=neuron_png)
            l_img.image = (
                neuron_png
            )  # if you don't use this, the garbage collector will destroy the image
            l_img.pack(side="left")

root = Tk()
app = NNviewer(root)
root.mainloop()
