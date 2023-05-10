import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from itertools import count
import os

width = 1280
height = 1280
number = 1
GREEN = "\033[92m"
COLOURLESS = "\033[0m"
SMALLFONT = "Helvetica 12"
NORMALFONT = "Helvetica 14"
BIGFONT = "Helvetica 18"


# The main class
class Window(tk.Tk):
    def __init__(self):
        # Initialise functions from the parent class.
        super().__init__()
        self.title("Subscription Manager")
        self.width = 640
        self.height = 360
        self.geometry(f"{self.width}x{self.height}")
        self.minsize(width=640, height=360)
        self.columnconfigure(0, weight=0)
        self.columnconfigure([1, 2], weight=1)
        self.rowconfigure([0], weight=1)
        self.bind("<Configure>", self.resize)
        # Lambda function used so that window is not destroyed on launch.
        self.bind("<Escape>", lambda: self.destroy())

    def contents(self):
        self.sidebar = Sidebar(self)
        self.mainmenu = MainMenu(self)
        self.mainmenu.contents()
        print(self.winfo_children())

    def resize(self, event):
        if event.widget == self:
            if getattr(self, "_after_id", None):
                self.parent.after_cancel(self._after_id)
            global width, height
            width, height = self.winfo_width(), self.winfo_height()


class Sidebar(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.columnconfigure(0, weight=1)
        self.rowconfigure([0, 1], weight=1)
        self.configure(bg="white")
        self.contents()

    def contents(self):
        self.grid(
            row=0, rowspan=1, column=0, padx=(20, 0), pady=20, sticky="nsew"
            )
        self.label = tk.Label(self, text="Navigation")
        self.mainbutton = tk.Button(
            self, text="M", font=BIGFONT,
            command=lambda: [
                MainMenu().contents(),
                print("success")
            ]
            )
        self.configbutton = tk.Button(
            self, text="\u2699", font=BIGFONT,
            command=lambda: [
                Configuration().contents(),
                print("success")
            ]
            )
        self.label.grid(row=0, column=0, sticky="new")
        self.mainbutton.grid(row=1, column=0, sticky="ews")
        self.configbutton.grid(row=2, column=0, sticky="ews")


class MainMenu(tk.Frame):
    def __init__(self, parent=None):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.columnconfigure([1, 2, 3], weight=1)
        self.rowconfigure([0, 2, 4], weight=1)
        self.configure(bg="white")

    def contents(self):
        print(f"[{GREEN}Main Menu{COLOURLESS}] - Executed")
        self.grid(
            row=0, column=1, columnspan=3, padx=20, pady=20, sticky="nsew"
            )
        self.label = tk.Label(
            self,
            text=(
                "Here are your current subscriptions:"
                ),
            font=BIGFONT
            )
        self.label.grid(row=0, column=1, columnspan=3)
        self.sub1 = tk.Label(self, text="Sub1", font=NORMALFONT)
        self.sub1.grid(row=1, column=1, sticky="nesw")
        self.sub1info = tk.Label(
            self, text="Time until refresh:\n?????", font=NORMALFONT, borderwidth=2, relief="solid"
            )
        self.sub1info.grid(row=2, column=1, sticky="nesw")
        self.sub2 = tk.Label(self, text="Sub2", font=NORMALFONT)
        self.sub2.grid(row=1, column=2, sticky="nesw")
        self.sub2info = tk.Label(
            self, text="Time until refresh:\n?????", font=NORMALFONT, borderwidth=2, relief="solid"
            )
        self.sub2info.grid(row=2, column=2, sticky="nesw")
        self.sub3 = tk.Label(self, text="Sub3", font=NORMALFONT)
        self.sub3.grid(row=1, column=3, sticky="nesw")
        self.sub3info = tk.Label(
            self, text="Time until refresh:\n?????", font=NORMALFONT, borderwidth=2, relief="solid"
            )
        self.sub3info.grid(row=2, column=3, sticky="nesw")
        self.sub4 = tk.Label(self, text="Sub4", font=NORMALFONT)
        self.sub4.grid(row=3, column=1, sticky="nesw")
        self.sub4info = tk.Label(
            self, text="Time until refresh:\n?????", font=NORMALFONT, borderwidth=2, relief="solid"
            )
        self.sub4info.grid(row=4, column=1, sticky="nesw")

        print(self.master.winfo_children())

    def raisewindow(self):
        self.tkraise()

    def removewindow(self):
        self.destroy()


class Configuration(tk.Frame):
    def __init__(self, parent=None):
        global number
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.rowconfigure([1], weight=0)
        self.rowconfigure([0], weight=1)
        self.configure(bg="white")
        print(number)

    def contents(self):
        print(f"[{GREEN}Configuration{COLOURLESS}] - Executed")
        global number
        self.grid(
            row=0, column=1, columnspan=3, padx=20, pady=20, sticky="nsew"
            )

        darkswitch = AnimatedButton(self)
        darkswitch.config(bg="white")
        darkswitch.grid(row=0, column=0, padx=(10, 0))
        darkswitch.onswitch(
            f"{os.getcwd()}/textures/On-Off-merged-frames.gif", False
            )
        darklabel = tk.Label(self, text="Option1", fg="black", bg="white", font=NORMALFONT)
        darklabel.grid(row=0, column=1, sticky="w", padx=(20, 20))

        number += 1

    def raisewindow(self):
        self.grid()

    def removewindow(self):
        self.destroy()


# https://stackoverflow.com/questions/43770847/play-an-animated-gif-in-python-with-tkinter
class AnimatedButton(tk.Label):
    def onswitch(self, image, automatic=True):
        if isinstance(image, str):
            image = Image.open(image)
        self.location = 0
        self.frames = []
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
                print(f"[{GREEN}GIF Playback{COLOURLESS}] -> Complete")
                self.bind(
                        "<Button-1>", lambda event: [
                            self.unbind("<Button-1>"),
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
                print(f"[{GREEN}GIF Playback{COLOURLESS}] -> Reversed")
                self.bind(
                    "<Button-1>", lambda event: [
                        self.unbind("<Button-1>"),
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
                    self.next_frame()
                    ]
                )


if __name__ == "__main__":
    window = Window()
    window.contents()
    window.mainloop()
