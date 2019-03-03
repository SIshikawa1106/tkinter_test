import tkinter as tk
from tkinter import *
from tkinter import ttk

class DoFDialog(tk.LabelFrame):
    def reset(self):
        pass

    def update_target(self, target):
        pass

    def update(self, *args):
        pass

class RobotDialog(DoFDialog):
    def __init__(self, master):
        super().__init__(master, text="RobotDoF")

        self._target = None
        self._joints = []

    def reset(self):
        if self._target is not None:
            self._joints = [StringVar() for x in range(len(self._target.Joints))]
            self._tcp = [StringVar() for x in range(6)]



    def update_target(self, target):
        if hasattr(target, "Joints") and hasattr(target, "tcp") and hasattr(target, "Position"):
            self._target = target
        else:
            self._target = None

    def update(self, *args):
        pass

class PositionDialog(DoFDialog):
    def __init__(self, master, text="6Dof"):
        super().__init__(master, text=text)

        self._target = None
        self.x_var = tk.StringVar()
        self.y_var = tk.StringVar()
        self.z_var = tk.StringVar()
        self.rx_var = tk.StringVar()
        self.ry_var = tk.StringVar()
        self.rz_var = tk.StringVar()
        self.limits = [[-1,1], [-180, 180]]

        position_frame = tk.LabelFrame(self, text="Translation")
        orientation_frame = tk.LabelFrame(self, text="Orientation")

        x_label = tk.Label(position_frame, text="x[m]")
        y_label = tk.Label(position_frame, text="y[m]")
        z_label = tk.Label(position_frame, text="z[m]")

        x = Spinbox(position_frame, from_=-1, to=1, increment=0.001, width=10,
                    format='%01.3f', justify="right", textvariable=self.x_var)
        y = Spinbox(position_frame, from_=-1, to=1, increment=0.001, width=10,
                    format='%01.3f', justify="right", textvariable=self.y_var)
        z = Spinbox(position_frame, from_=-1, to=1, increment=0.001, width=10,
                    format='%01.3f', justify="right", textvariable=self.z_var)
        #x = Entry(position_frame, text="", justify="right")
        #y = Entry(position_frame, text="", justify="right")
        #z = Entry(position_frame, text="", justify="right")

        x_label.grid(column=0, row=0, sticky=tk.NSEW)
        y_label.grid(column=1, row=0, sticky=tk.NSEW)
        z_label.grid(column=2, row=0, sticky=tk.NSEW)
        x.grid(column=0, row=1, sticky=tk.NSEW)
        y.grid(column=1, row=1, sticky=tk.NSEW)
        z.grid(column=2, row=1, sticky=tk.NSEW)

        rx_label = tk.Label(orientation_frame, text="Rx[deg]")
        ry_label = tk.Label(orientation_frame, text="Ry[deg]")
        rz_label = tk.Label(orientation_frame, text="Rz[deg]")

        rx = Spinbox(orientation_frame, from_=-180, to=180, increment=0.1, width=10,
                    format='%01.1f', justify="right", textvariable=self.rx_var)
        ry = Spinbox(orientation_frame, from_=-180, to=180, increment=0.1, width=10,
                    format='%01.1f', justify="right", textvariable=self.ry_var)
        rz = Spinbox(orientation_frame, from_=-180, to=180, increment=0.1, width=10,
                    format='%01.1f', justify="right", textvariable=self.rz_var)
        #rx = Entry(orientation_frame, text="", justify="right")
        #ry = Entry(orientation_frame, text="", justify="right")
        #rz = Entry(orientation_frame, text="", justify="right")

        rx_label.grid(column=0, row=0, sticky=tk.NSEW)
        ry_label.grid(column=1, row=0, sticky=tk.NSEW)
        rz_label.grid(column=2, row=0, sticky=tk.NSEW)
        rx.grid(column=0, row=1, sticky=tk.NSEW)
        ry.grid(column=1, row=1, sticky=tk.NSEW)
        rz.grid(column=2, row=1, sticky=tk.NSEW)

        position_frame.pack()
        orientation_frame.pack()
        self.reset()

        self.x_var.trace("w", self.update)
        self.y_var.trace("w", self.update)
        self.z_var.trace("w", self.update)
        self.rx_var.trace("w", self.update)
        self.ry_var.trace("w", self.update)
        self.rz_var.trace("w", self.update)

    def reset(self):
        self.x_var.set("0.000")
        self.y_var.set("0.000")
        self.z_var.set("0.000")
        self.rx_var.set("0.0")
        self.ry_var.set("0.0")
        self.rz_var.set("0.0")

    def update_target(self, target):
        if hasattr(target, "Position"):

            self._target = None
            position = self._target.position
            self.x_var.set(str(position[0]))
            self.y_var.set(str(position[1]))
            self.z_var.set(str(position[2]))
            self.rx_var.set(str(position[3]))
            self.ry_var.set(str(position[4]))
            self.rz_var.set(str(position[5]))
            self._target = target
        else:
            self._target = None

    def update(self, *args):
        spinvals = [self.x_var, self.y_var, self.z_var, self.rx_var, self.ry_var, self.rz_var]
        values = []
        for idx, spinval in enumerate(spinvals):
            limit = self.limits[0] if idx<3 else self.limits[1]
            format = "{:01.3f}" if idx<3 else "{:01.1f}"
            if spinval.get().lstrip('-').replace('.', '', 1).isdigit():
                s = spinval.get()
                value = float(s)
                if limit[0]>value:
                    value = limit[0]
                if limit[1]<value:
                    value = limit[1]
                values.append(float(s))
                spinval.set(format.format(value))
            elif idx<2:
                spinval.set("0.000")
            else:
                spinval.set("0.0")

        if self._target is not None and len(values)==6:
            self._target.position = values


class TcpDialog(PositionDialog):
    def update_target(self, target):
        if hasattr(target, "Position"):

            self._target = None
            position = self._target.position
            self.x_var.set(str(position[0]))
            self.y_var.set(str(position[1]))
            self.z_var.set(str(position[2]))
            self.rx_var.set(str(position[3]))
            self.ry_var.set(str(position[4]))
            self.rz_var.set(str(position[5]))
            self._target = target
        else:
            self._target = None

    def update(self, *args):
        spinvals = [self.x_var, self.y_var, self.z_var, self.rx_var, self.ry_var, self.rz_var]
        values = []
        for idx, spinval in enumerate(spinvals):
            limit = self.limits[0] if idx<3 else self.limits[1]
            format = "{:01.3f}" if idx<3 else "{:01.1f}"
            if spinval.get().lstrip('-').replace('.', '', 1).isdigit():
                s = spinval.get()
                value = float(s)
                if limit[0]>value:
                    value = limit[0]
                if limit[1]<value:
                    value = limit[1]
                values.append(float(s))
                spinval.set(format.format(value))
            elif idx<2:
                spinval.set("0.000")
            else:
                spinval.set("0.0")

        if self._target is not None and len(values)==6:
            self._target.position = values





if __name__ == "__main__":

    root = tk.Tk()

    dialog = PositionDialog(root)
    dialog.pack()
    root.mainloop()
