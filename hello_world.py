from tkinter import *
from tkinter import messagebox
import tkinter as tk
from tkinter import ttk, Menu, filedialog, StringVar
import os

import test_data
import DialogDoF

class TaskPlanFrame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self._root = tk.Toplevel()
        self._root.title("TaskPlanTool")

        self.tree = ttk.Treeview(self._root)
        self.sy = tk.Scrollbar(self.tree)
        self.sy.pack(side=tk.RIGHT, fill=tk.Y)
        self.sy.config(command=self.tree.yview)
        self.tree.config(yscrollcommand=self.sy.set)

        self.tree["column"] = (1, 2)
        self.tree["show"] = "headings"
        self.tree.heading(1, text="ID")
        self.tree.heading(2, text="Pose")

        self.tree.pack(fill=tk.BOTH, expand=True)

        self._button_frame = tk.Frame(self._root)
        add_button = tk.Button(self._button_frame, text="ADD", command=self.add_func)
        remove_button = tk.Button(self._button_frame, text="REMOVE", command=self.remove_func)
        save_button = tk.Button(self._button_frame, text="SAVE", command=self.save_button)
        load_button = tk.Button(self._button_frame, text="LOAD", command=self.load_button)
        plan_button = tk.Button(self._button_frame, text="PLAN", command=self.plan_button)
        check_button = tk.Button(self._button_frame, text="CHECK", command=self.check_button)

        add_button.grid(row=0, column=0, padx=20, pady=0, sticky=tk.EW)
        remove_button.grid(row=0, column=1, padx=20, pady=0, sticky=tk.EW)
        save_button.grid(row=1, column=0, padx=20, pady=0, sticky=tk.EW)
        load_button.grid(row=1, column=1, padx=20, pady=0, sticky=tk.EW)
        plan_button.grid(row=2, column=0, padx=20, pady=0, sticky=tk.EW)
        check_button.grid(row=2, column=1, padx=20, pady=0, sticky=tk.EW)

        label = tk.Label(self._button_frame, text="Check File = ")
        label.grid(row=3, column=0, padx=0, pady=0, sticky=tk.EW)
        self.file_entry = tk.Entry(self._button_frame, text="")
        self.file_entry.grid(row=3, column=1, padx=0, pady=0, sticky=tk.EW)

        self._button_frame.grid_rowconfigure(0, weight=1, uniform="group1")
        self._button_frame.grid_rowconfigure(1, weight=1, uniform="group1")
        self._button_frame.grid_rowconfigure(2, weight=1, uniform="group1")
        self._button_frame.grid_rowconfigure(3, weight=1, uniform="group1")
        self._button_frame.grid_columnconfigure(0, weight=1, uniform="group1")
        self._button_frame.grid_columnconfigure(1, weight=1, uniform="group1")

        self._button_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=False)
        self._root.protocol("WM_DELETE_WINDOW", self.exit)

    def exit(self):
        self._root.destroy()
        self.destroy()

    def add_func(self):
        print("test add func")
        pass

    def remove_func(self):
        print("remove add func")
        pass

    def save_button(self):
        print("save add func")
        pass

    def load_button(self):

        type = [('JSONファイル', '*.json')]
        file = filedialog.askopenfilename(filetype=type)

        if file and os.path.isfile(file):
            #task_info = load_task_info(file)
            print(file)

            if self.tree.get_children():
                yes = messagebox.askyesno("Confirmation", "Overwrite ?")
                if yes:
                    self.tree.delete(*self.tree.get_children())

        pass

    def plan_button(self):
        print("plan add func")
        pass

    def check_button(self):
        print("check add func")
        print(self.file_entry.get())
        pass


class TreeFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self._frame = tk.LabelFrame(master, text="Tree Info")
        self.tree = ttk.Treeview(self._frame)

        self.tree.heading("#0", text="Cell Tree", anchor=tk.W)

        self.sy = tk.Scrollbar(self._frame)
        self.sy.pack(side=tk.RIGHT, fill=tk.Y)
        self.sy.config(command=self.tree.yview)
        self.tree.config(yscrollcommand=self.sy.set)
        self.tree.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.tree.bind("<<TreeviewSelect>>", self.func)
        self._frame.grid(row=0, column=0, padx=0, pady=0, sticky=tk.NSEW)

    def insert_node(self, parent, value):
        return self.tree.insert(parent, "end", text=value.Name, open=False, value=value)

    def func(self, event):
        value = self.tree.item(self.tree.focus())['values']
        print(value)

    def build(self, tree_info):
        if self.tree.get_children():
            self.tree.delete(*self.tree.get_children())

        for cell in tree_info:
            cell_node = self.insert_node("", cell)
            for controller in cell.Controllers:
                controller_node = self.insert_node(cell_node, controller)
                for robot in controller.Robots:
                    robot_node = self.insert_node(controller_node, robot)
            for model in cell.Models:
                model_node = self.insert_node(cell_node, model)


class InfoWindows(tk.Frame):
    def __init__(self, master):
        main_frame = tk.Frame(master)
        rob_frame = tk.LabelFrame(main_frame, text="Robot Info")
        pos_frame = tk.LabelFrame(main_frame, text="Position Info")

        #"""
        self.txt2 = tk.Text(rob_frame)
        self.txt2.pack(fill=tk.BOTH, expand=True)
        self.position = DialogDoF.PositionDialog(pos_frame)
        self.position.pack(fill=tk.BOTH, expand=True)
        #"""
        pos_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        rob_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        main_frame.grid(row=0, column=1, padx=0, pady=0, sticky=(tk.N, tk.S, tk.E, tk.W))

    def build_position_frame(self, frame):
        pass

    def build_robot_frame(self, frame):
        pass

class MainFrame(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self._root = master
        master.title('Planning Tool')

        self._task_plan_frame = None

        self._ini_file_path = ""
        self._cells = []

        self.build_menu()
        self.build_frame()

    def build_menu(self):
        menu_bar = Menu(self._root)
        self._root.config(menu=menu_bar)

        file_menu = Menu(menu_bar, tearoff=0)
        file_menu.add_command(label='Load', command=self.loading)
        # file_menu.add_command(label='Save')
        file_menu.add_separator()
        file_menu.add_command(label='Exit', command=self.exit)
        menu_bar.add_cascade(label='Files', menu=file_menu)

        tool_menu = Menu(menu_bar, tearoff=0)
        tool_menu.add_command(label='Task Plan', command=self.open_task_plan_frame)
        menu_bar.add_cascade(label='Tools', menu=tool_menu)

    def open_task_plan_frame(self):
        print("test open_task_plan_frame")
        if self._task_plan_frame is None or not self._task_plan_frame.winfo_exists():
            self._task_plan_frame = TaskPlanFrame()

    def build_frame(self):
        self.info_frame = InfoWindows(self._root)
        self.tree_frame = TreeFrame(self._root)

    def run(self):
        self._root.mainloop()

    def exit(self):
        self._root.quit()

    def loading(self):
        type = [('JSONファイル', '*.json')]
        file = filedialog.askopenfilename(filetype=type)

        if file and os.path.isfile(file):
            #task plan frame destroy
            if self._task_plan_frame is not None:
                self._task_plan_frame.exit()
            self._ini_file_path = file
            cells = test_data.load_info(file)
            print(cells)
            self.tree_frame.build(cells)
        else:
            self._ini_file_path = None


if __name__ == '__main__':
    root = tk.Tk()
    app = MainFrame(root)
    #root.bind('<F4>', app.change_dir)
    #root.bind('<F5>', app.update_dir)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    root.mainloop()
