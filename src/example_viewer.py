from tkinter import PhotoImage, Label
import matplotlib.pyplot as plt
import network


class ExampleViewer:
    def __init__(self, master, test_data, net):
        self.test_data = test_data
        self.net = net
        self.l_id = Label(master)
        self.l_id.pack()

        number_png = PhotoImage(file="../img/placehold.png").zoom(
            8, 8
        )  # Load the image
        self.l_img = Label(master, image=number_png)
        self.l_img.image = (
            number_png
        )  # hack: if you don't use this, the garbage collector will destroy the image
        self.l_img.pack(side="left")
        self.data_id = 0
        self.correct_num = 0
        self.ex_label = []

        for i in range(10):
            self.ex_label.append(Label(master, text=(str(i) + ": ---")))
            self.ex_label[i].pack()

    def load_image(self, data_id=0):
        data_id = int(data_id)

        if data_id < 0 or data_id > (len(self.test_data) - 1):
            print("incorrect index")
            return

        self.l_id.configure(text=data_id)
        self.data_id = data_id
        self.correct_num = self.test_data[data_id][1]

        save_str = "../output/number_%d.png" % (data_id)
        plt.imsave(
            save_str, self.test_data[data_id][0].reshape(28, 28), cmap="gray"
        )  # save the image

        number_png = PhotoImage(file=save_str).zoom(8, 8)  # Load the image
        self.l_img.configure(image=number_png)
        self.l_img.image = (
            number_png
        )  # hack: if you don't use this, the garbage collector will destroy the image

        for i in range(len(self.ex_label)):  # reset highlighting
            self.ex_label[i].config(fg="black")

        output = self.net.feedforward(self.test_data[data_id][0])  # classify the image
        i_max = 0
        value_max = 0
        for i in range(len(self.ex_label)):
            output_str = "%d:  %f" % (i, output[i])
            self.ex_label[i].config(text=output_str)
            if output[i] > value_max:
                value_max = output[i]
                i_max = i

        self.ex_label[i_max].config(fg="red")

        for i in range(len(self.ex_label)):  # highlight the correct number
            if i == self.correct_num:
                self.ex_label[i].config(fg="green")
                break
