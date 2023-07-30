import tkinter as tk
from tkinter import messagebox
# PIL for image manipulation and playback
from PIL import Image, ImageTk
# Allow me to increment a number infinitely
from itertools import count
# A module that will allow me to add a popup for when a user hovers over an
# element
from idlelib.tooltip import Hovertip
import datetime  # Allows me to manage dates
# A module that will allow me to increment dates
from dateutil.relativedelta import relativedelta  # pip install python-dateutil
import os  # Lets me find the file path
import math  # Allows me to round numbers
# Allow me to add type hints to my code
from typing import Dict, Any
import json  # To write to external files

# Window Configuration and Terminal Log Configuration
width = 1280
height = 720
GREEN = "\033[92m"
BLUE = "\033[94m"
COLOURLESS = "\033[0m"
SMALLFONT = "Helvetica 12"
NORMALFONT = "Helvetica 14"
BIGFONT = "Helvetica 18"
CLEAR = ""
bgcolour = "#4c4c4c"
darkbg = "#404040"
textcolour = "#ffffff"
ACCENTCOLOUR = "#eb3434"
redcolour = "#eb3434"
redtextcolour = "#ea5a5a"
yellowcolour = "#fff325"
currentdate = datetime.date.today()
path = os.path.dirname(__file__)
manager_i_max: int = 0
manager_constant: int = 0
file_location = f"{path}/subscription_info.json"

# Check if the subscription data file is there
try:
    with open(file_location, "r") as file:
        subscription_dict = json.load(file)
        subscription_list: list = []
        for i in range(len(subscription_dict["Subscriptions"])):
            name = subscription_dict["Subscriptions"][i]["name"]
            date = datetime.datetime.strptime(
                subscription_dict["Subscriptions"][i]["date"], "%Y-%m-%d"
                ).date()
            subscription_list.append([name, date])
        file.close()

# If there is no file, populate the subscription information with fake data
except FileNotFoundError as error:
    subscription_list = [
        ["Sub1", datetime.date(2023, 1, 1)],
        ["Sub2", datetime.date(2022, 11, 11)]
        ]
    print(error)

# A dictionary containing all of the frames so they can be called again
# Dict[Any, Any] is a type hint and lets the linter and I know that frames
# is a dictionary that can contain any values.
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
        for Frame in (Sidebar, MainMenu, Configuration):
            # Set the name of the variable to the name of the frame
            name = Frame.__name__
            # Set the "parent" or master window to be a frame created to
            # hold all frames and set the controller of the frame to be the
            # main window class
            frame = Frame(parent=container, controller=self)
            frame.config(bg=bgcolour)
            self.frames[name] = frame
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
        self.configbutton.grid(row=3, column=0, sticky="ews")


class MainMenu(tk.Frame):
    # Main menu with the text for each widget displayed in a text box instead
    # of a label
    def __init__(self, parent, controller):
        global manager_i_max
        global manager_constant
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.config(bg=bgcolour)
        # https://stackoverflow.com/questions/3085696/adding-a-scrollbar-to-a-group-of-widgets-in-tkinter/3092341#3092341
        print(f"[{GREEN}MainMenu{COLOURLESS}] - Executed")
        self.grid(
            row=0, column=1, columnspan=3, padx=20, pady=20, sticky="nsew"
            )
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
        # When the window moves or is resized bind the following events.
        self.frame.bind("<Configure>", self.onFrameConfigure)
        self.canvas.bind("<Configure>", self.onCanvasConfigure)
        # Bind the mouse wheel to the canvas
        self.canvas.bind_all("<MouseWheel>", self.onMouseWheel)
        self.frame.columnconfigure([1, 2, 3], weight=1)
        self.frame.rowconfigure([0, 2, 4], weight=1)

        heading = tk.Label(
            self.frame, text="Here are your current subscriptions:",
            font=BIGFONT, bg=bgcolour, fg=textcolour
            )
        heading.grid(row=0, column=1, columnspan=3)
        bgborders: list[...] = []
        labels: list[...] = []
        delbuttons: list[...] = []
        infolabels: list[...] = []
        dates: list[...] = []
        constant: int = 0
        i_max: int = 0

        # The functions below will change the colour of each label when
        # hovered over
        # This code was adapted from the StackOverflow Page below
        # https://stackoverflow.com/questions/66239329/how-to-highlight-two-different-labels-when-hovered-on-any-one-of-them-in-tkinter
        def hovercolouron(event):
            event.widget["bg"] = darkbg

        def hovercolouroff(event):
            event.widget["bg"] = bgcolour
        for i in range(len(subscription_list)):
            bgborders.append(
                tk.Label(
                    self.frame, bg=bgcolour, fg=textcolour, borderwidth=1,
                    relief="solid"
                )
            )
            # A button to delete the associated label.
            delbuttons.append(
                tk.Button(
                    self.frame, text="X", font=SMALLFONT, fg=textcolour,
                    bg=redcolour, command=lambda i=i: delButton(i)
                )
            )
            labels.append(
                tk.Entry(
                    self.frame, bg=bgcolour, fg=textcolour, justify="center",
                    font=NORMALFONT, borderwidth=1, relief="sunken"
                )
            )
            labels[-1].insert(0, subscription_list[i][0])
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
                        "Refreshes on:\n\n"
                        f"In: {days_remaining} Days"
                        ),
                    font=NORMALFONT, bg=bgcolour, fg=textcolour, borderwidth=1,
                    relief="solid"
                    )
                )
            if days_remaining <= 3:
                infolabels[-1].configure(fg=redtextcolour)
            elif days_remaining <= 7:
                infolabels[-1].configure(fg=yellowcolour)
            dates.append(
                tk.Entry(
                    self.frame, bg=bgcolour, fg=textcolour, justify="center",
                    font=NORMALFONT, borderwidth=1, relief="sunken"
                )
            )
            dates[-1].insert(
                0,
                datetime.datetime.strftime(subscription_list[i][1], "%d %B %Y")
                )
            i += 1
            # Using the math module, round i up
            ceiling_i = math.ceil(i/3)
            # Round i down to the nearest whole number
            floor_i = math.floor(i/3)
            rowpos = self.calcRowPos(i, constant)
            columnpos = i - (constant * 3)
            bgborders[-1].grid(
                row=rowpos, column=columnpos, sticky="nesw"
            )
            labels[-1].grid(
                row=rowpos, column=columnpos, sticky="nesw", padx=(1, 25),
                pady=1
                )
            delbuttons[-1].grid(
                row=rowpos, column=columnpos, sticky="e"
                )
            infolabels[-1].grid(
                row=(rowpos + 1), column=columnpos, sticky="new"
                )
            dates[-1].grid(
                row=(rowpos + 1), column=columnpos, sticky="ew", padx=5
                )
            self.frame.rowconfigure((ceiling_i * 2), weight=1)
            if i % 3 == 0:
                constant += 1
            # Bind when the mouse hovers over an element to change its colour
            # and when it leaves, change it back
            labels[-1].bind("<Enter>", hovercolouron)
            labels[-1].bind("<Leave>", hovercolouroff)
            dates[-1].bind("<Enter>", hovercolouron)
            dates[-1].bind("<Leave>", hovercolouroff)
            i_max += 1

        i_max += 1
        manager_i_max = i_max
        manager_constant = constant
        updatebutton = tk.Button(
            self, text="Update", font=NORMALFONT, fg=textcolour, bg=bgcolour,
            command=lambda: [
                self.getEntryText(labels, dates),
                ]
            )
        updatebutton.grid(
            row=2, columnspan=3, column=0, sticky="nesw", pady=(5, 0)
            )
        addbutton = tk.Button(
            self.frame, text="+", font=BIGFONT, fg=textcolour, bg=bgcolour,
            command=lambda: updateAddGrid()
            )

        def delButton(number):
            # Remove default elements
            try:
                bgborders[number].destroy()
                # Using .pop allows you to remove a value given an index
                bgborders.pop(number)
                labels[number].destroy()
                labels.pop(number)
                delbuttons[number].destroy()
                delbuttons.pop(number)
                infolabels[number].destroy()
                infolabels.pop(number)
                dates[number].destroy()
                dates.pop(number)
            # If a button was added by the "+" button it will have a number
            # That is 2 greater than the default ones. This will catch these
            # elements
            except IndexError:
                number -= 2
                bgborders[number].destroy()
                bgborders.pop(number)
                labels[number].destroy()
                labels.pop(number)
                delbuttons[number].destroy()
                delbuttons.pop(number)
                infolabels[number].destroy()
                infolabels.pop(number)
                dates[number].destroy()
                dates.pop(number)
            global manager_i_max
            global manager_constant
            manager_i_max -= 1
            # Calculate the row and column.
            rowpos = self.calcRowPos(manager_i_max, manager_constant)
            columnpos = manager_i_max - (manager_constant * 3)
            # Ensure that the constant cant go below zero
            if manager_constant > 0:
                manager_constant -= 1
            # If the element can be gridded in the 4th column, remove 3 columns
            # and add a row.
            if columnpos >= 4:
                columnpos -= 3
                rowpos += 1
            # If the element can be gridded in columns below 0, add 3.
            if columnpos <= 0:
                columnpos += 3
                rowpos -= 1
            # Grid the "+" button based on the previous math.
            addbutton.grid(
                row=rowpos, rowspan=2, column=columnpos, sticky="nesw"
                )
            # i values for the loop to store each iteration seperately.
            # (There was an issue where the elements would all be gridded)
            # In the same column
            loop_i = manager_i_max
            loop_constant = manager_constant
            for i in range(len(labels) - number):
                loop_i -= 1
                # Calculate the row and column.
                rowpos = self.calcRowPos(loop_i, loop_constant)
                columnpos = loop_i - (loop_constant * 3)
                # Ensure the loop_constant cannot go below zero
                if loop_constant > 0:
                    loop_constant -= 1
                # Reverse the order of the elements.
                if columnpos == 3:
                    columnpos = 1
                elif columnpos == 1:
                    columnpos = 3
                # Ensure the column doesnt go too high or low.
                if columnpos >= 4:
                    columnpos -= 3
                    rowpos += 1
                if columnpos <= 0:
                    columnpos += 3
                    rowpos -= 1
                # Grid each element
                bgborders[i].grid(
                    row=rowpos, column=columnpos, sticky="nesw"
                    )
                labels[i].grid(
                    row=rowpos, column=columnpos, sticky="nesw", padx=(1, 25),
                    pady=1
                    )
                delbuttons[i].grid(
                    row=rowpos, column=columnpos, sticky="e"
                    )
                delbuttons[i].configure(
                    command=lambda i=i: delButton(i)
                )
                infolabels[i].grid(
                    row=(rowpos + 1), column=columnpos, sticky="new"
                    )
                dates[i].grid(
                    row=(rowpos + 1), column=columnpos, sticky="ew", padx=5
                    )

        # A function that will update the grid for the add button when clicked.
        # This will resize the grid and add another info box where it used to
        # be
        def updateAddGrid(negative=False):
            # Allow manipulation of the global variables representing the
            # highest i value and constant value reached by the grid loop.
            global manager_i_max
            global manager_constant
            # Add one loop
            manager_i_max += 1
            # Calculate the row and column.
            rowpos = self.calcRowPos(manager_i_max, manager_constant)
            columnpos = manager_i_max - (manager_constant * 3)
            # If i is divisible by 3, add one to the constant.
            if manager_i_max % 3 == 0:
                manager_constant += 1
            # If the element can be gridded in the 4th column, remove 3 columns
            # and add a row.
            if columnpos >= 4:
                columnpos -= 3
                rowpos += 1
            if columnpos <= 0:
                columnpos += 3
                rowpos -= 1
            # Grid the "+" button based on the previous math.
            addbutton.grid(
                row=rowpos, rowspan=2, column=columnpos, sticky="nesw"
                )

            # The border for the top row
            bgborders.append(
                tk.Label(
                    self.frame, bg=bgcolour, fg=textcolour, borderwidth=1,
                    relief="solid"
                )
            )
            # Add the delete button.
            # lambda i=manager_i_max allows values to be passed into the
            # function, without this, all would have the same value passed.
            delbuttons.append(
                tk.Button(
                    self.frame, text="X", font=SMALLFONT,
                    fg=textcolour, bg=redcolour,
                    command=lambda i=manager_i_max: delButton(manager_i_max)
                )
            )
            # The text entry for the top row.
            labels.append(
                tk.Entry(
                    self.frame, bg=bgcolour, fg=textcolour, justify="center",
                    font=NORMALFONT, borderwidth=1, relief="sunken"
                )
            )
            # Add the text "name" into the entry
            labels[-1].insert(0, "name")
            # Add information on refresh date.
            infolabels.append(
                tk.Label(
                    self.frame, text="Refreshes on:\n\nIn: ??? Days",
                    font=NORMALFONT, bg=bgcolour, fg=textcolour, borderwidth=1,
                    relief="solid"
                    )
                )
            dates.append(
                tk.Entry(
                    self.frame, bg=bgcolour, fg=textcolour, justify="center",
                    font=NORMALFONT, borderwidth=1, relief="sunken"
                )
            )
            i = manager_i_max - 1
            constant = manager_constant
            if manager_i_max % 3 == 0:
                constant -= 1
            elif i % 3 == 0:
                constant -= 1
            # Using the math module, round i up
            ceiling_i = math.ceil(i/3)
            # Round i down to the nearest whole number
            floor_i = math.floor(i/3)
            rowpos = self.calcRowPos(i, constant)
            columnpos = i - (constant * 3)
            if columnpos >= 4:
                columnpos -= 3
                rowpos += 1
            elif columnpos <= 0:
                columnpos += 3
                rowpos -= 1
            # Grid each element in their calculated positions
            bgborders[-1].grid(
                row=rowpos, column=columnpos, sticky="nesw"
            )
            labels[-1].grid(
                row=rowpos, column=columnpos, sticky="nesw", padx=(1, 25),
                pady=1
                )
            delbuttons[-1].grid(
                row=rowpos, column=columnpos, sticky="e"
                )
            delbuttons[-1].configure(
                command=lambda i=i: delButton(i)
            )
            infolabels[-1].grid(
                row=(rowpos + 1), column=columnpos, sticky="new"
                )
            dates[-1].grid(
                row=(rowpos + 1), column=columnpos, sticky="ew", padx=5
                )
            self.frame.rowconfigure((ceiling_i * 2), weight=1)
            # Bind when the mouse hovers over an element to change its colour
            # and when it leaves, change it back
            labels[-1].bind("<Enter>", hovercolouron)
            labels[-1].bind("<Leave>", hovercolouroff)
            dates[-1].bind("<Enter>", hovercolouron)
            dates[-1].bind("<Leave>", hovercolouroff)

        rowpos = self.calcRowPos(i_max, constant)
        columnpos = i_max - (constant * 3)
        addbutton.grid(
            row=rowpos, rowspan=2, column=columnpos, sticky="nesw"
            )

    def calcRowPos(self, i, constant):
        # A function to calculate the row position for gridding
        # Round i down to the nearest whole number
        floor_i = math.floor(i/3)
        if i % 3 == 0:
            return (floor_i + constant)
        else:
            return (floor_i + constant + 1)

    def getEntryText(self, labels, dates):
        # Try to get text from the entries
        try:
            for i in range(len(labels)):
                name = labels[i].get()
                date = dates[i].get()
            with open(file_location, "r") as file:
                data = json.load(file)
                file.close()
            if "Subscriptions" not in data:
                data["Subscriptions"] = []
            data["Subscriptions"] = []
            for i in range(len(labels)):
                name = labels[i].get()
                date = dates[i].get()
                english_date = str(
                    datetime.datetime.strptime(date, "%d %B %Y").date()
                    )
                data["Subscriptions"].append(
                    {
                        "name": name,
                        "date": english_date
                    }
                )
            with open(file_location, "w") as file:
                json.dump(data, file, indent=4)
                file.close()
            tk.messagebox.showinfo(
                title="Success",
                message="Data successfully updated"
            )
        # If any errors occur, for example no data or others, print the error
        # in the terminal and do not continue.
        except ValueError as error:
            tk.messagebox.showerror(
                title="Invalid Date",
                message=(
                    "Please ensure that the date has been entered correctly."
                    )
                )
        except Exception as error:
            print(error)

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
        # Configure the sizing of the columns
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.rowconfigure([1], weight=0)
        self.rowconfigure([0], weight=1)
        self.configure(bg="white")
        print(f"[{GREEN}Configuration{COLOURLESS}] - Executed")
        self.grid(
            row=0, column=1, columnspan=3, padx=20, pady=20, sticky="nsew"
            )
        # Assign the class to darkswitch.
        darkswitch = AnimatedButton(self)
        # Change the label background
        darkswitch.config(bg=bgcolour)
        # Grid the label at the specified location.
        darkswitch.grid(row=0, column=0, padx=(10, 0))
        # Run the animation with the file location, what setting will change,
        # and whether to play automatically or not.
        darkswitch.onswitch(
            f"{path}/textures/On-Off-merged-frames.gif", "Sidebar", False
            )
        # A label that explains the button.
        darklabel = tk.Label(
            self, text="Left Sided Navigation", fg=textcolour,
            bg=bgcolour, font=NORMALFONT
            )
        darklabel.grid(row=0, column=1, sticky="w", padx=(20, 20))


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
            # When there are no more frames in the list, stop and bind the
            # forward playback option to the button
            except IndexError:
                print(f"{CLEAR}[{GREEN}GIF Playback{COLOURLESS}] -> Complete")
                self.bind(
                        "<Button-1>", lambda event: [
                            self.unbind("<Button-1>"),
                            ChangeSettings(f"{self.setting}R-G"),
                            self.prev_frame()
                        ]
                    )

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
            # When there are no more frames in the list, stop and bind the
            # reverse playback option to the button
            except IndexError:
                print(f"{CLEAR}[{GREEN}GIF Playback{COLOURLESS}] -> Reversed")
                self.bind(
                    "<Button-1>", lambda event: [
                        self.unbind("<Button-1>"),
                        ChangeSettings(f"{self.setting}G-R"),
                        self.next_frame()
                        ]
                    )

    def load_frame(self):
        # if there are frames
        if self.frames:
            self.config(image=self.frames[self.location])
            # Bind the reverse playback option to the button.
            self.bind(
                "<Button-1>", lambda event: [
                    self.unbind("<Button-1>"),
                    ChangeSettings(f"{self.setting}G-R"),
                    self.next_frame()
                    ]
                )


class ChangeSettings():
    def __init__(self, setting):
        self.setting = setting

        # If the sidebar goes from red to green, move the sidebar to the right
        if setting == "SidebarG-R":
            # Index [:-3] will remove the last three characters from the string
            frame = frames[setting[:-3]]
            frame.grid(row=0, column=2, padx=(0, 20), pady=20, sticky="nesw")
            for Frame in frames:
                frame = frames[Frame]
                if Frame != "Sidebar":
                    print(f"{Frame} edited")
                    print("G-R")
                    frame.grid_forget()
                    frame.grid(
                        row=0, padx=20, pady=20, column=1, sticky="nesw"
                        )

        # If the sidebar goes from red to green, move the sidebar to the left
        elif setting == "SidebarR-G":
            frame = frames[setting[:-3]]
            frame.grid(
                row=0, rowspan=1, column=0, padx=(20, 0), pady=20,
                sticky="nsew"
                )


# If this is the main file, run it.
if __name__ == "__main__":
    window = Window()
    window.mainloop()
