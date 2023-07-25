import tkinter as tk
from tkinter import ttk
# PIL for image manipulation and playback
from PIL import Image, ImageTk
# Allow me to increment a number infinitely
from itertools import count
# A module that will allow me to add a popup for when a user hovers over an
# element
from idlelib.tooltip import Hovertip
import datetime
# A module that will allow me to increment dates
from dateutil.relativedelta import relativedelta
import os
import math
# Allow me to add type hints to my code
from typing import Dict, Any
import json

# Window Configuration and Terminal Log Configuration
width = 1280
height = 720
GREEN = "\033[92m"
BLUE = "\033[94m"
COLOURLESS = "\033[0m"
SMALLFONT = "Helvetica 12"
NORMALFONT = "Helvetica 14"
BIGFONT = "Helvetica 18"
CLEAR = "\033[F                                           \r"
# CLEAR = ""
bgcolour = "#4c4c4c"
darkbg = "#404040"
textcolour = "#ffffff"
ACCENTCOLOUR = "#eb3434"
currentdate = datetime.date.today()
path = os.path.dirname(__file__)
print(path)

try:
    with open(f"{path}/subscription_info.json", "r") as file:
        subscription_dict = json.load(file)
        print(subscription_dict)
        subscription_list: list = []
        for i in range(len(subscription_dict["Subscriptions"])):
            name = subscription_dict["Subscriptions"][i]["name"]
            date = datetime.datetime.strptime(
                subscription_dict["Subscriptions"][i]["date"], "%d-%m-%Y"
                ).date()
            subscription_list.append([name, date])
        file.close()

except FileNotFoundError as error:
    # A list of all subscriptions and their refresh dates
    subscription_list = [
        ["Sub1", datetime.date(2023, 1, 1)],
        ["Sub2", datetime.date(2022, 11, 11)],
        ["Sub3", "Sub3"], ["Sub4", "Sub4"], ["Sub5", "Sub5"], ["Sub6", "Sub6"],
        ["Sub7", "Sub7"], ["Sub8", "Sub8"], ["Sub9", "Sub9"],
        ["Sub10", "Sub10"], ["Sub11", "Sub11"], ["Sub12", "Sub12"],
        ["Sub13", "Sub13"], ["Sub14", "Sub14"], ["Sub15", "Sub15"],
        # Extra values in list to test scrolling
        # ["Sub16", "Sub16"], ["Sub17", "Sub17"], ["Sub18", "Sub18"],
        # ["Sub19", "Sub19"], ["Sub20", "Sub20"], ["Sub21", "Sub21"],
        # ["Sub22", "Sub22"], ["Sub23", "Sub23"], ["Sub24", "Sub24"],
        # ["Sub25", "Sub25"], ["Sub26", "Sub26"], ["Sub27", "Sub27"],
        # ["Sub28", "Sub28"], ["Sub29", "Sub29"], ["Sub30", "Sub30"],
        # ["Sub31", "Sub31"], ["Sub32", "Sub32"], ["Sub33", "Sub33"],
        # ["Sub34", "Sub34"], ["Sub35", "Sub35"], ["Sub36", "Sub36"],
        # ["Sub37", "Sub37"], ["Sub38", "Sub38"], ["Sub39", "Sub39"],
        # ["Sub40", "Sub40"], ["Sub41", "Sub41"], ["Sub42", "Sub42"],
        # ["Sub43", "Sub43"], ["Sub44", "Sub44"], ["Sub45", "Sub45"],
        # ["Sub46", "Sub46"], ["Sub47", "Sub47"], ["Sub48", "Sub48"]
        ]
    print(error)

# A dictionary containing all of the frames so they can be called again
frames: Dict[Any, Any] = {}


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

    # This frame swapping code was adapted from this stackoverflow page
    # https://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter
        self.frames = frames
        # For each frame class that I have
        for Frame in (Sidebar, MainMenu, Configuration, SubscriptionManager):
            # Set the name of the variable to the name of the frame
            name = Frame.__name__
            # Set the "parent" or master window to be a frame created to
            # hold all frames and set the controller of the frame to be the
            # main window class
            frame = Frame(parent=container, controller=self)
            frame.config(bg=bgcolour)
            self.frames[name] = frame
            print(name)
            if name == "Sidebar":
                frame.grid(row=0, column=0, sticky="nesw")
                frame.grid(
                    row=0, rowspan=1, column=0, padx=(20, 0), pady=20,
                    sticky="nsew"
                    )
            else:
                frame.grid(row=0, column=1, sticky="nesw")
                pass

        self.showframe("MainMenu")

    def showframe(self, frame_name):
        # Show the frame provided.
        frame = self.frames[frame_name]
        frame.tkraise()

    def resize(self, event):
        # Change the width and height variables to the width and height of
        # the adjusted window
        if event.widget == self:
            global width, height
            print(width, height)
            width, height = self.winfo_width(), self.winfo_height()


class Sidebar(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.parent = parent
        self.columnconfigure([0, 2], weight=1)
        self.rowconfigure([0, 1], weight=1)
        self.configure(bg=bgcolour)
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
        # Show a tip when hovering over a navigation option to inform the user
        # about its function
        self.maintip = Hovertip(self.mainbutton, "Open the Main Menu")
        self.managerbutton = tk.Button(
            self, text="E", font=BIGFONT, fg=textcolour, bg=bgcolour,
            command=lambda: [
                self.controller.showframe("SubscriptionManager"),
                print(
                    f"{CLEAR}[{BLUE}Frame Swapped{COLOURLESS}]"
                    " -> SubscriptionManager"
                    )
                ]
            )
        self.managertip = Hovertip(
            self.managerbutton, "Edit your current subscriptions"
            )
        self.configbutton = tk.Button(
            self, text="\u2699", font=BIGFONT, fg=textcolour, bg=bgcolour,
            command=lambda: [
                self.controller.showframe("Configuration"),
                print(
                    f"{CLEAR}[{BLUE}Frame Swapped{COLOURLESS}]"
                    " -> Configuration"
                    )
            ]
            )
        self.configtip = Hovertip(
            self.configbutton, "Change the settings of the application"
            )
        self.label.grid(row=0, column=0, sticky="new")
        self.mainbutton.grid(row=1, column=0, sticky="ews")
        self.managerbutton.grid(row=2, column=0, sticky="ews")
        self.configbutton.grid(row=3, column=0, sticky="ews")


class MainMenu(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.config(bg=bgcolour)
        print(f"[{GREEN}Main Menu{COLOURLESS}] - Executed")
        # https://stackoverflow.com/questions/3085696/adding-a-scrollbar-to-a-group-of-widgets-in-tkinter/3092341#3092341
        self.canvas = tk.Canvas(
            self, borderwidth=0, bg=bgcolour, highlightthickness=0
            )
        self.frame = tk.Frame(self.canvas, bg=bgcolour)
        self.scrollbar = tk.Scrollbar(
            self, orient="vertical", command=self.canvas.yview
            )
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.grid(row=0, column=1, sticky="nes")
        self.canvas.grid(row=0, column=0, sticky="nesw", padx=20, pady=20)
        # Create a window inside of a new frame through which I can view the
        # main menu
        self.newframe = self.canvas.create_window(
            (0, 0), window=self.frame, anchor="nw"
            )

        self.frame.bind("<Configure>", self.onFrameConfigure)
        self.canvas.bind("<Configure>", self.onCanvasConfigure)
        self.canvas.bind_all("<MouseWheel>", self.onMouseWheel)
        self.frame.columnconfigure([1, 2, 3], weight=1)
        self.frame.rowconfigure([0, 2, 4], weight=1)

        heading = tk.Label(
            self.frame,
            text=(
                "Here are your current subscriptions:"
                ),
            font=BIGFONT, bg=bgcolour, fg=textcolour
            )
        heading.grid(row=0, column=1, columnspan=3)
        labels: list[...] = []
        infolabels: list[...] = []
        constant: int = 0
        i_val: int = 0

        # The functions below will change the colour of each label when
        # hovered over
        # This code was adapted from the StackOverflow Page below
        # https://stackoverflow.com/questions/66239329/how-to-highlight-two-different-labels-when-hovered-on-any-one-of-them-in-tkinter
        def hovercolouron(event):
            event.widget["bg"] = darkbg

        def hovercolouroff(event):
            event.widget["bg"] = bgcolour
        # print(subscription_list[0])
        for i in range(len(subscription_list)):
            labels.append(
                tk.Label(
                    self.frame, text=subscription_list[i][0], font=NORMALFONT,
                    bg=bgcolour, fg=textcolour,
                    borderwidth=1, relief="solid"
                    )
                )
            try:
                # You can subtract datetime.date objects and it will leave the
                # difference. Then I can get the number of days remaining from
                # that
                days_remaining = (subscription_list[i][1] - currentdate).days
                if days_remaining < 0:
                    while days_remaining < 0:
                        subscription_list[i][1] += relativedelta(months=1)
                        days_remaining = (
                            (subscription_list[i][1] - currentdate).days
                            )
            # If calulations cannot be performed, replace the days remaining
            # with "???"
            except TypeError:
                days_remaining = "???"
            infolabels.append(
                tk.Label(
                    self.frame, text=(
                        f"Refreshes on:\n{subscription_list[i][1]}\n"
                        f"In: {days_remaining} Days"
                        # f"On:\n... of ..."
                        ),
                    font=NORMALFONT,
                    bg=bgcolour, fg=textcolour,
                    borderwidth=1, relief="solid"
                    )
                )
            i += 1
            # Using the math module, round i up
            ceiling_i = math.ceil(i/3)
            # Round i down to the nearest whole number
            floor_i = math.floor(i/3)
            if i % 3 == 0:
                labels[-1].grid(
                    row=(floor_i + constant),
                    column=(i-(constant*3)), sticky="nesw"
                    )
                infolabels[-1].grid(
                    row=(floor_i + constant + 1),
                    column=(i - (constant * 3)), sticky="nesw"
                    )
                self.frame.rowconfigure((ceiling_i * 2), weight=1)
                print(
                    f"Label: {i}, InfoLabel: {i} Gridded. Constant: "
                    f"{constant} has changed to {constant + 1}")
                constant += 1
            else:
                labels[-1].grid(
                    row=(floor_i + constant + 1),
                    column=(i - (constant * 3)), sticky="nesw"
                    )
                infolabels[-1].grid(
                    row=(floor_i + constant + 2),
                    column=(i - (constant * 3)), sticky="nesw"
                    )
                if ceiling_i % 3 == 0:
                    self.frame.rowconfigure((ceiling_i * 2), weight=1)
            # Bind when the mouse hovers over an element to change its colour
            # and when it leaves, change it back
            labels[-1].bind("<Enter>", hovercolouron)
            labels[-1].bind("<Leave>", hovercolouroff)
            infolabels[-1].bind("<Enter>", hovercolouron)
            infolabels[-1].bind("<Leave>", hovercolouroff)

        print(self.master.winfo_children())

    def onFrameConfigure(self, event):
        # Changes the area of scrolling to be the entire bounding box for the
        # frame. This will only be called when the size of the window is
        # changed
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    # https://stackoverflow.com/questions/63926996/tkinter-frame-inside-of-canvas-not-expanding-to-fill-area/63946783#63946783
    def onCanvasConfigure(self, event):
        # If the canvas changes size, change its width to be the width of the
        # Frame
        self.canvas.itemconfig(self.newframe, width=event.width)
        print("Triggered")

    # https://stackoverflow.com/a/17457843
    def onMouseWheel(self, event):
        # When the mousewheel is used, move the canvas by the integer specified
        # and move that number of units "units" can also be "pages", but that
        # will move the canvas too much
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")


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
        darkswitch = AnimatedButton(self)
        darkswitch.config(bg=bgcolour)
        darkswitch.grid(row=0, column=0, padx=(10, 0))
        darkswitch.onswitch(
            f"{os.getcwd()}/textures/On-Off-merged-frames.gif",
            "Sidebar", False
            )
        darklabel = tk.Label(
            self, text="Left Sided Navigation", fg=textcolour,
            bg=bgcolour, font=NORMALFONT
            )
        if darkswitch is False:
            master.controller.frames["Sidebar"].grid(
                row=0, column=2, sticky="nesw"
                )
        darklabel.grid(row=0, column=1, sticky="w", padx=(20, 20))


class SubscriptionManager(tk.Frame):
    # Main menu with the text for each widget displayed in a text box instead
    # of a label
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.parent = parent
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.rowconfigure([0, 1], weight=1)
        self.configure(bg="white")
        print(f"[{GREEN}SubscriptionManager{COLOURLESS}] - Executed")
        self.grid(
            row=0, column=1, columnspan=3, padx=20, pady=20, sticky="nsew"
            )
        heading = tk.Label(
            self, text="Edit your current subscriptions",
            fg=textcolour, bg=bgcolour, font=NORMALFONT
            )
        heading.grid(row=0, column=0, padx=10)
        text = tk.Label(
            self, text="Not implemented yet", fg=textcolour, bg=bgcolour,
            font=NORMALFONT
        )
        text.grid(row=1, column=0)

        # update = tk.Button(self)


# https://stackoverflow.com/questions/43770847/play-an-animated-gif-in-python-with-tkinter
class AnimatedButton(tk.Label):
    def onswitch(self, image, setting, automatic=True):
        # Checks if the image parameter is a string, if it is, open the image
        if isinstance(image, str):
            image = Image.open(image)
        self.location = 0
        self.frames = []
        self.setting = setting
        try:
            # count is from itertools and allows me to count up one step
            # starting at 1 (1, 2, 3, 4, ...)
            # This is preferable to the range() function as the number of
            # frames per image may vary, so therefore using range() will not
            # allow me to iterate through each frame infinitely as it requires
            # an end number. This will also allow me to use GIFs that have
            # varying numbers of frames.
            for i in count(1):
                # Add a copy of each frame of the image to the list
                self.frames.append(
                    ImageTk.PhotoImage(
                        image.copy().resize((101, 51))
                        )
                    )
                # seek/move to the next frame of the image
                image.seek(i)
        # When there are no more frames in the image, stop.
        except EOFError:
            pass

        # Try to set the delay value to that of the image, but 3 times faster
        # This will allow the GIF to play 3x faster than the actual file
        try:
            self.delay = int((image.info['duration'])/3)
        # If there is an error, print what it is and set the delay between
        # Frames to a default value
        except Exception as error:
            print(error)
            self.delay = 100

        # If there is only one frame, set the image to be the first frame
        if len(self.frames) == 1:
            self.config(image=self.frames[0])
        # If the frame is not set to play automatically, call a function to
        # trigger the animation on click.
        elif automatic is False:
            self.load_frame()
        # Play the next frame
        else:
            self.next_frame()

    def next_frame(self):
        if self.frames:
            try:
                self.location += 1
                # Change the image to the frame at the specified location.
                self.config(image=self.frames[self.location])
                # After a delay, play the next frame.
                self.after(self.delay, self.next_frame)
            # When there are no more frames in the list, stop
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
                # If a location that doesn't exist is called, break out of the
                # loop
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
        # if there are frames
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
            # Index [:-1] will remove the last character from the string
            frame = frames[setting[:-1]]
            frame.grid(row=0, column=2, padx=(0, 20), pady=20, sticky="nesw")
            for Frame in frames:
                frame = frames[Frame]
                if Frame != "Sidebar":
                    print(f"{Frame} edited")
                    frame.grid_forget()
                    frame.grid(
                        row=0, padx=20, pady=20, column=1, sticky="nesw"
                        )

        elif setting == "Sidebar2":
            frame = frames[setting[:-1]]
            frame.grid(
                row=0, rowspan=1, column=0, padx=(20, 0), pady=20,
                sticky="nsew"
                )


if __name__ == "__main__":
    window = Window()
    window.mainloop()
