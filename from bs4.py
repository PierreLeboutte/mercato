from tkinter import *
from tkinter import ttk


class MainWindow():

    def __init__(self, mainWidget):
        self.main_frame = ttk.Frame(mainWidget, width=300, height=150, padding=(0, 0, 0, 0))
        self.main_frame.grid(row=0, column=0)

        self.some_kind_of_controler = 0

        self.main_gui()

    def main_gui(self):
        root.title('My Window')

        self.main_label_1 = ttk.Label(self.main_frame, text='Object_1')
        self.main_label_1.grid(row=0, column=0)

        self.main_label_2 = ttk.Label(self.main_frame, text='Object_2')
        self.main_label_2.grid(row=1, column=0)

        self.main_label_3 = ttk.Label(self.main_frame, text='Object_3')
        self.main_label_3.grid(row=2, column=0)

        self.setings_button = ttk.Button(self.main_frame, text='Setings')
        self.setings_button.grid(row=0, column=1)
        self.setings_button.bind('<Button-1>', self.setings_gui)

        self.gui_elements = [self.main_label_1,
                             self.main_label_2,
                             self.main_label_3,
                             self.setings_button]

    def setings_gui(self, event):
        self.gui_elements_remove(self.gui_elements)

        root.title('Setings')

        self.main_label_1 = ttk.Label(self.main_frame, text='Object_1')
        self.main_label_1.grid(row=2, column=0)

        self.main_menu_button = ttk.Button(self.main_frame, text='Main menu')
        self.main_menu_button.grid(row=0, column=1)
        self.main_menu_button.bind('<Button-1>', self.back_to_main)

        self.some_kind_of_controler = 1

        self.gui_elements = [self.main_label_1,
                             self.main_menu_button]

    def back_to_main(self, event):
        if self.some_kind_of_controler == 1:
            self.gui_elements_remove(self.gui_elements)
        else:
            pass
        self.main_gui()

    def gui_elements_remove(self, elements):
        for element in elements:
            element.destroy()

def main():
    global root

    root = Tk()
    root.geometry('300x150+50+50')
    window = MainWindow(root)

    root.mainloop()

if __name__ == '__main__':
    main()