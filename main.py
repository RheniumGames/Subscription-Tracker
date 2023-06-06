import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from itertools import count
from idlelib.tooltip import Hovertip
import os
import math

width = 1280
height = 720
GREEN = "\033[92m"
BLUE = "\033[94m"
COLOURLESS = "\033[0m"
SMALLFONT = "Helvetica 12"
NORMALFONT = "Helvetica 14"
BIGFONT = "Helvetica 18"
# CLEAR = "\033[F                                           \r"
CLEAR = ""
bgcolour = "#4c4c4c"
textcolour = "#ffffff"
ACCENTCOLOUR = "#eb3434"
subscription_list = [
    ["Sub1", "16 May"], ["Sub2", "?????"], ["Sub3", "?????"], ["Sub4", "?????"],
    ["Sub5", "?????"], ["Sub6", "?????"], ["Sub7", "?????"], ["Sub8", "?????"],
    ["Sub9", "?????"], ["Sub10", "?????"], ["Sub11", "?????"], ["Sub12", "?????"]
    ]
frames = {}


# The main class
class Window(tk.Tk):
    def __init__(self):
        # Initialise functions from the parent class.
        super().__init__()
        global frames
        self.title("Subscription Manager")
        self.width = 640
        self.height = 360
        self.geometry(f"{self.width}x{self.height}")
        self.minsize(width=640, height=360)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        container = tk.Frame()
        container.grid(row=0, column=0, sticky="nesw")
        container.columnconfigure([0, 2], weight=0)
        container.columnconfigure([1], weight=1)
        container.rowconfigure([0], weight=1)
        container.config(bg=bgcolour)
        self.bind("<Configure>", self.resize)
        # Lambda function used so that window is not destroyed on launch.
        self.bind("<Escape>", lambda x: self.destroy())

# https://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter
        self.frames = frames
        for Frame in (Sidebar, MainMenu, Configuration, SubscriptionManager):
            name = Frame.__name__
            frame = Frame(parent=container, controller=self)
            frame.config(bg=bgcolour)
            self.frames[name] = frame
            if name == "Sidebar":
                frame.grid(row=0, column=0, sticky="nesw")
                frame.grid(
                    row=0, rowspan=1, column=0, padx=(20, 0), pady=20, sticky="nsew"
                    )
            else:
                frame.grid(row=0, column=1, sticky="nesw")
                pass

        self.showframe("MainMenu")

    def showframe(self, page_name):
        # Show the frame provided.
        frame = self.frames[page_name]
        frame.tkraise()

    def resize(self, event):
        if event.widget == self:
            if getattr(self, "_after_id", None):
                self.parent.after_cancel(self._after_id)
            global width, height
            width, height = self.winfo_width(), self.winfo_height()


class Sidebar(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.parent = parent
        self.columnconfigure([0, 2], weight=1)
        self.rowconfigure([0, 1], weight=1)
        self.configure(bg=bgcolour)
        # self.grid(
        #     row=0, rowspan=1, column=0, padx=(20, 0), pady=20, sticky="nsew"
        #     )
        self.label = tk.Label(
            self, text="Navigation", fg=textcolour, bg=bgcolour
            )
        self.mainbutton = tk.Button(
            self, text="M", font=BIGFONT, fg=textcolour, bg=bgcolour,
            command=lambda: [
                self.controller.showframe("MainMenu"),
                print(f"{CLEAR}[{BLUE}Frame Swapped{COLOURLESS}] -> MainMenu")
            ]
            )
        self.maintip = Hovertip(self.mainbutton, "Open the Main Menu")
        self.managerbutton = tk.Button(
            self, text="E", font=BIGFONT, fg=textcolour, bg=bgcolour,
            command=lambda: [
                self.controller.showframe("SubscriptionManager"),
                print(f"{CLEAR}[{BLUE}Frame Swapped{COLOURLESS}] -> SubscriptionManager")
            ]
            )
        self.managertip = Hovertip(self.managerbutton, "Edit your current subscriptions")
        self.configbutton = tk.Button(
            self, text="\u2699", font=BIGFONT, fg=textcolour, bg=bgcolour,
            command=lambda: [
                self.controller.showframe("Configuration"),
                print(f"{CLEAR}[{BLUE}Frame Swapped{COLOURLESS}] -> Configuration")
            ]
            )
        self.configtip = Hovertip(self.configbutton, "Change the settings of the application")
        self.label.grid(row=0, column=0, sticky="new")
        self.mainbutton.grid(row=1, column=0, sticky="ews")
        self.managerbutton.grid(row=2, column=0, sticky="ews")
        self.configbutton.grid(row=3, column=0, sticky="ews")


class MainMenu(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.columnconfigure([1, 2, 3], weight=1)
        self.rowconfigure([0, 2, 4], weight=1)
        self.config(bg=bgcolour)
        print(f"[{GREEN}Main Menu{COLOURLESS}] - Executed")
        self.grid(
            row=0, column=1, columnspan=3, padx=20, pady=20, sticky="nsew"
            )
        self.label = tk.Label(
            self,
            text=(
                "Here are your current subscriptions:"
                ),
            font=BIGFONT, bg=bgcolour, fg=textcolour
            )
        self.label.grid(row=0, column=1, columnspan=3)
        labels: list[...] = []
        infolabels: list[...] = []
        constant: int = 0
        i_val: int = 0
        # print(subscription_list[0])
        for i in range(len(subscription_list)):
            labels.append(
                tk.Label(
                    self, text=subscription_list[i][0], font=NORMALFONT,
                    bg=bgcolour, fg=textcolour,
                    borderwidth=1, relief="solid"
                    )
                )
            infolabels.append(
                tk.Label(
                    self, text=(
                        f"Time until refresh:\n{subscription_list[i][1]}"
                        ),
                    font=NORMALFONT,
                    bg=bgcolour, fg=textcolour,
                    borderwidth=1, relief="solid"
                    )
                )
            i += 1
            # print(f"i = {i}")
            # print(f"Ceiling i = {math.ceil(i/3)}")
            ceiling_i = math.ceil(i/3)
            # labels[-1].grid(row=int((i/3)+1), column=(i+1), sticky="nsew")
            if i % 3 == 0:
                labels[-1].grid(
                    row=(math.floor(i/4)+(constant+1)),
                    column=(i-(constant*3)), sticky="nesw"
                    )
                infolabels[-1].grid(
                    row=(math.floor(i/4)+(constant+1)+1),
                    column=(i-(constant*3)), sticky="nesw"
                    )
                self.rowconfigure((ceiling_i * 2), weight=1)
                constant += 1
                print(f"The constant is now {constant}")
            else:
                labels[-1].grid(
                    row=(math.floor(i/3)+(constant+1)),
                    column=(i-(constant*3)), sticky="nesw"
                    )
                infolabels[-1].grid(
                    row=(math.floor(i/3)+(constant+1)+1),
                    column=(i-(constant*3)), sticky="nesw"
                    )
                if ceiling_i % 3 == 0:
                    self.rowconfigure((ceiling_i * 2), weight=1)
            i_val = i
        print(i_val)
        if (i_val / 3) > 3:
            scrollbar = tk.Scrollbar(self)
            scrollbar.grid()
        print(self.master.winfo_children())


class Configuration(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.parent = parent
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.rowconfigure([1], weight=0)
        self.rowconfigure([0], weight=1)
        self.configure(bg="white")
        print(f"[{GREEN}Configuration{COLOURLESS}] - Executed")
        self.grid(
            row=0, column=1, columnspan=3, padx=20, pady=20, sticky="nsew"
            )
        # self.place(x=width/2, y=height/2)
        darkswitch = AnimatedButton(self)
        darkswitch.config(bg=bgcolour)
        darkswitch.grid(row=0, column=0, padx=(10, 0))
        darkswitch.onswitch(
            f"{os.getcwd()}/textures/On-Off-merged-frames.gif", "Sidebar", False
            )
        darklabel = tk.Label(self, text="Left Sided Navigation", fg=textcolour, bg=bgcolour, font=NORMALFONT)
        print(f"Darkswitch\n")
        if darkswitch is False:
            master.controller.frames["Sidebar"].grid(row=0, column=2, sticky="nesw")
        darklabel.grid(row=0, column=1, sticky="w", padx=(20, 20))
        # self.label = tk.Label(
        #     self, text="Configuration Menu", bg="black", fg="white"
        #     )
        # self.label.grid(row=0, column=1)


class SubscriptionManager(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.parent = parent
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.rowconfigure([1], weight=0)
        self.rowconfigure([0], weight=1)
        self.configure(bg="white")
        print(f"[{GREEN}SubscriptionManager{COLOURLESS}] - Executed")
        self.grid(
            row=0, column=1, columnspan=3, padx=20, pady=20, sticky="nsew"
            )
        self.testlabel = tk.Label(
            self, text="Test", fg=textcolour, bg=bgcolour, font=NORMALFONT
            )
        self.testlabel.grid(row=0, column=0, padx=10)


# https://stackoverflow.com/questions/43770847/play-an-animated-gif-in-python-with-tkinter
class AnimatedButton(tk.Label):
    def onswitch(self, image, setting, automatic=True):
        if isinstance(image, str):
            image = Image.open(image)
        self.location = 0
        self.frames = []
        self.setting = setting
        try:
            for i in count(1):
                self.frames.append(
                    ImageTk.PhotoImage(
                        image.copy().resize((101, 51))
                        )
                    )
                image.seek(i)

        except EOFError:
            pass

        try:
            self.delay = int((image.info['duration'])/3)
        except:
            self.delay = 100

        if len(self.frames) == 1:
            self.config(image=self.frames[0])
        elif automatic is False:
            self.load_frame()
        else:
            self.next_frame()

    def next_frame(self):
        if self.frames:
            try:
                self.location += 1
                # self.location %= len(self.frames)
                self.config(image=self.frames[self.location])
                self.after(self.delay, self.next_frame)
            except IndexError:
                print(f"{CLEAR}[{GREEN}GIF Playback{COLOURLESS}] -> Complete")
                self.bind(
                        "<Button-1>", lambda event: [
                            self.unbind("<Button-1>"),
                            ChangeSettings(f"{self.setting}2"),
                            self.prev_frame()
                        ]
                    )
                return True
    
    def prev_frame(self):
        if self.frames:
            try:
                self.location -= 1
                if self.location == -1:
                    raise IndexError
                self.config(image=self.frames[self.location])
                self.after(self.delay, self.prev_frame)
            except IndexError:
                print(f"{CLEAR}[{GREEN}GIF Playback{COLOURLESS}] -> Reversed")
                self.bind(
                    "<Button-1>", lambda event: [
                        self.unbind("<Button-1>"),
                        ChangeSettings(f"{self.setting}1"),
                        self.next_frame()
                        ]
                    )
                return False
    
    def load_frame(self):
        if self.frames:
            self.config(image=self.frames[self.location])
            self.bind(
                "<Button-1>", lambda event: [
                    self.unbind("<Button-1>"),
                    ChangeSettings(f"{self.setting}1"),
                    self.next_frame()
                    ]
                )


class ChangeSettings():
    def __init__(self, setting):
        self.setting = setting

        if setting == "Sidebar1":
            print("Here")
            # Index [:-1] will remove the last character from the string
            frame = frames[setting[:-1]]
            # frame.grid_forget()
            frame.grid(row=0, column=2, padx=(0, 20), pady=20, sticky="nesw")
            # print(frames)
            for Frame in frames:
                frame = frames[Frame]
                # print(frame)
                if Frame != "Sidebar":
                    print(f"{Frame} asf")
                    frame.grid_forget()
                    frame.grid(row=0, padx=20, pady=20, column=1, sticky="nesw")

        elif setting == "Sidebar2":
            frame = frames[setting[:-1]]
            frame.grid(
                row=0, rowspan=1, column=0, padx=(20, 0), pady=20, sticky="nsew"
                )


if __name__ == "__main__":
    window = Window()
    window.mainloop()
