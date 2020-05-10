"""
- VisualNucleus by Geegaz -
This is an UI port of Nucleus by Gnottero
"""

# Import all the required libraries
import json
import os
import re
import tkinter as tk
import webbrowser

try:
    import requests

    requests_present = True
except:
    requests_present = False


def callback(url):
    # Open new link in the default browser
    webbrowser.open_new(url)


class UI(tk.Frame):
    """
    Creates the VisualNucleus interface

    style: dict
    messages: dict
    default_values: dict

    create_widgets(self) -> None
    place_widgets(self) -> None
    generate(self) -> None
    get_values(self) -> dict
    """

    style = {}
    messages = {
        "init": 'Fill in the fields and click "Generate". Empty fields will use default values.',
        "requests_absent": "You don't have the requests module installed, please refer to the github for how to install it (link in the bottom corner).",
        "invalid_path": 'Invalid path "{}". Check it and and try again.',
        "path_error": 'Error creating folder "{}". Check the fields and and try again.',
        "invalid_player_name": "Invalid player name. Check the fields and and try again.",
        "generating": "Generating...",
        "success": 'Sucessfuly generated {} in "{}"',
    }
    default_values = {
        "dev_name": "Player_Name",
        "dp_name": "Datapack_Name",
        "dp_desc": "datapack description",
        "dp_item": "minecraft:name_tag",
        "project_name": "project_name",
        "namespace": "namespace",
        "tick_name": "tick",
        "load_name": "load",
        "dp_path": "./out",
    }

    def __init__(self, master):
        with open("resources/style.json", "r") as f:
            # Use an external file to style the widgets
            self.style = json.load(f)
        # Default path to use is the "out" folder in the working directory
        self.default_values["dp_path"] = os.getcwd() + "/out"

        # Initialize the window (master)
        super().__init__(master)
        self.master = master
        self.master.geometry("+20+20")
        self.master.resizable(False, False)
        self.master.title("VisualNucleus")
        self.master.iconbitmap("icon.ico")
        self.master.config(self.style["window"])

        # Initialize the main frame
        self.pack()
        self.config(self.style["main_frame"])

        # Create the widgets
        self.create_widgets()
        self.place_widgets()

    def create_widgets(self):
        """
        Creates the different widgets
        """
        self.title_text = tk.Label(self, self.style["title"], text="Visual\nNucleus")

        t_image = tk.PhotoImage(file="resources/icon.gif")
        self.title_image = tk.Label(self, self.style["title_image"], image=t_image)
        self.title_image.w_image = t_image

        self.fields_frame = tk.Frame(self, self.style["fields_frame"])

        self.fields_frame.fields = {
            "HEADER_advancements": tk.Label(
                self.fields_frame, self.style["header"], text="Advancements"
            ),
            "ENTRY_dev_name": {
                "label": tk.Label(
                    self.fields_frame,
                    self.style["entry_text"],
                    text="Minecraft username:",
                ),
                "entry": tk.Entry(self.fields_frame, self.style["entry"]),
            },
            "ENTRY_dp_name": {
                "label": tk.Label(
                    self.fields_frame, self.style["entry_text"], text="Datapack name:"
                ),
                "entry": tk.Entry(self.fields_frame, self.style["entry"]),
            },
            "TEXT_dp_desc": {
                "label": tk.Label(
                    self.fields_frame,
                    self.style["entry_text"],
                    text="Datapack description:",
                ),
                "text": tk.Text(self.fields_frame, self.style["text"]),
            },
            "ENTRY_dp_item": {
                "label": tk.Label(
                    self.fields_frame,
                    self.style["entry_text"],
                    text="Displayed item id:",
                ),
                "entry": tk.Entry(self.fields_frame, self.style["entry"]),
            },
            "HEADER_folders": tk.Label(
                self.fields_frame, self.style["header"], text="Folders"
            ),
            "ENTRY_project_name": {
                "label": tk.Label(
                    self.fields_frame, self.style["entry_text"], text="Project name:"
                ),
                "entry": tk.Entry(self.fields_frame, self.style["entry"]),
            },
            "ENTRY_namespace": {
                "label": tk.Label(
                    self.fields_frame, self.style["entry_text"], text="Namespace:"
                ),
                "entry": tk.Entry(self.fields_frame, self.style["entry"]),
            },
            "ENTRY_tick_name": {
                "label": tk.Label(
                    self.fields_frame,
                    self.style["entry_text"],
                    text="Ticking function name:",
                ),
                "entry": tk.Entry(self.fields_frame, self.style["entry"]),
            },
            "ENTRY_load_name": {
                "label": tk.Label(
                    self.fields_frame,
                    self.style["entry_text"],
                    text="Loading function name:",
                ),
                "entry": tk.Entry(self.fields_frame, self.style["entry"]),
            },
            "HEADER_separator": tk.Frame(
                self.fields_frame, self.style["fields_frame"], height=10
            ),
            "ENTRY_dp_path": {
                "label": tk.Label(
                    self.fields_frame,
                    self.style["entry_text"],
                    text="Datapack folder path:",
                ),
                "entry": tk.Entry(self.fields_frame, self.style["entry"]),
            },
        }
        self.message_text = tk.StringVar()
        self.message_label = tk.Label(
            self, self.style["message"], textvariable=self.message_text
        )
        self.message_text.set(self.messages["init"])

        self.buttons_frame = tk.Frame(self, self.style["buttons_frame"])

        self.generate_button = tk.Button(
            self.buttons_frame,
            self.style["button"],
            text="Generate",
            bg="#21a946",
            command=self.generate,
        )
        self.quit_button = tk.Button(
            self.buttons_frame,
            self.style["button"],
            text="Quit",
            command=self.master.destroy,
        )

        g_image = tk.PhotoImage(file="resources/GitHub_icon.gif")
        self.github_label = tk.Label(
            self, self.style["github_link"], text="Github", image=g_image
        )
        self.github_label.g_image = g_image
        self.github_label.bind(
            "<Button-1>", lambda e: callback("https://github.com/geegaz/VisualNucleus")
        )

    def place_widgets(self):
        """
        Places the widgets in a grid layout
        """
        self.title_text.grid(row=0, column=0, sticky="W")
        self.title_image.grid(row=0, column=1, sticky="E")
        self.fields_frame.grid(row=1, column=0, columnspan=2)
        self.message_label.grid(row=2, column=0, columnspan=2, sticky="W")
        self.buttons_frame.grid(row=3, column=0, columnspan=2)
        self.github_label.grid(row=4, column=1, sticky="E")

        r = 0
        for field in self.fields_frame.fields:
            if field.startswith("HEADER"):
                self.fields_frame.fields[field].grid(row=r, column=0, columnspan=3)
            elif field.startswith("ENTRY"):
                self.fields_frame.fields[field]["label"].grid(
                    row=r, column=0, sticky="W"
                )
                self.fields_frame.fields[field]["entry"].grid(
                    row=r, column=1, columnspan=2, sticky="W"
                )
            elif field.startswith("TEXT"):
                self.fields_frame.fields[field]["label"].grid(
                    row=r, column=0, sticky="NW"
                )
                self.fields_frame.fields[field]["text"].grid(
                    row=r, column=1, columnspan=2, sticky="W"
                )
            else:
                print("Error: Invalid field")
            r += 1
        self.fields_frame.fields["ENTRY_dp_item"]["entry"].insert(0, "minecraft:")

        self.generate_button.grid(row=0, column=0)
        self.quit_button.grid(row=0, column=1)

    def get_values(self) -> dict:
        """
        Gets the values in the fields
        """
        values = self.default_values.copy()

        dev_name = re.sub(
            r"\W+", "_", self.fields_frame.fields["ENTRY_dev_name"]["entry"].get()
        )
        dp_name = re.sub(
            r"\W+", "_", self.fields_frame.fields["ENTRY_dp_name"]["entry"].get()
        )
        dp_desc = self.fields_frame.fields["TEXT_dp_desc"]["text"].get(1.0, tk.END)
        dp_item = re.sub(
            r"[^\w:]+",
            "_",
            (self.fields_frame.fields["ENTRY_dp_item"]["entry"].get().lower()),
        )

        project_name = re.sub(
            r"\W+",
            "_",
            (self.fields_frame.fields["ENTRY_project_name"]["entry"].get().lower()),
        )
        namespace = re.sub(
            r"\W+",
            "_",
            (self.fields_frame.fields["ENTRY_namespace"]["entry"].get().lower()),
        )
        tick_name = re.sub(
            r"\W+",
            "_",
            (self.fields_frame.fields["ENTRY_tick_name"]["entry"].get().lower()),
        )
        load_name = re.sub(
            r"\W+",
            "_",
            (self.fields_frame.fields["ENTRY_load_name"]["entry"].get().lower()),
        )

        dp_path = self.fields_frame.fields["ENTRY_dp_path"]["entry"].get()

        if len(dev_name) > 0:
            values["dev_name"] = dev_name
        if len(dp_name) > 0:
            values["dp_name"] = dp_name
        if len(dp_desc) > 1:
            values["dp_desc"] = dp_desc
        if len(dp_item) > 0:
            values["dp_item"] = dp_item

        if len(project_name) == 0:
            project_name = values["dp_name"].lower()
        values["project_name"] = project_name

        if len(namespace) == 0:
            namespace = values["dev_name"].lower()
        values["namespace"] = namespace

        if len(tick_name) != 0:
            values["tick_name"] = tick_name
        if len(load_name) != 0:
            values["load_name"] = load_name
        if values["load_name"] == values["tick_name"]:
            values["tick_name"] += "_tick"
            values["load_name"] += "_load"

        if len(dp_path) == 0:
            if not os.path.exists(values["dp_path"]):
                os.makedirs(values["dp_path"])
        else:
            values["dp_path"] = dp_path

        return values

    def generate(self):
        """
        Generates a datapack template using the values entered in the fields
        """
        self.message_text.set(self.messages["generating"])
        self.message_label.update()  # updates the message box
        values = self.get_values()

        if not os.path.exists(values["dp_path"]):
            self.message_text.set(
                self.messages["invalid_path"].format(values["dp_path"])
            )
            return

        if not requests_present:
            self.message_text.set(self.messages["requests_absent"])
            return

        g_adv_path = f"{values['dp_path']}/{values['dp_name']}/data/global/advancements"
        dp_adv_path = f"{values['dp_path']}/{values['dp_name']}/data/{values['namespace']}/advancements/{values['project_name']}"
        mc_tags_path = (
            f"{values['dp_path']}/{values['dp_name']}/data/minecraft/tags/functions"
        )
        dp_tags_path = f"{values['dp_path']}/{values['dp_name']}/data/{values['namespace']}/tags/functions/{values['project_name']}"
        dp_fun_path = f"{values['dp_path']}/{values['dp_name']}/data/{values['namespace']}/functions/{values['project_name']}"

        paths = [g_adv_path, dp_adv_path, mc_tags_path, dp_tags_path, dp_fun_path]
        for path in paths:
            try:
                os.makedirs(path)
            except FileExistsError:
                pass
            except OSError:
                self.message_text.set(self.messages["path_error"].format(path))
                return

        # Generating pack.mcmeta
        pack = {
            "pack": {
                "pack_format": 5,
                "description": f"{values['dp_name']} by {values['dev_name']}",
            }
        }
        with open(f"{values['dp_path']}/{values['dp_name']}/pack.mcmeta", "w") as f:
            f.write(json.dumps(pack, indent=5, sort_keys=True))

        # Getting player head
        try:
            uuid_rq = requests.get(
                f"https://api.mojang.com/users/profiles/minecraft/{values['dev_name']}"
            )
            player_uuid = uuid_rq.json()["id"]
            skull_value_rq = requests.get(
                f"https://sessionserver.mojang.com/session/minecraft/profile/{player_uuid}"
            )
            skull_value = skull_value_rq.json()["properties"][0]["value"]
        except:
            self.message_text.set(self.messages["invalid_player_name"])
            return

        # Global advancements
        root = {
            "display": {
                "title": "Installed Datapacks",
                "description": "",
                "icon": {"item": "minecraft:knowledge_book"},
                "background": "minecraft:textures/block/gray_concrete.png",
                "show_toast": False,
                "announce_to_chat": False,
            },
            "criteria": {"trigger": {"trigger": "minecraft:tick"}},
        }
        dev = {
            "display": {
                "title": f"{values['dev_name']}",
                "description": "",
                "icon": {
                    "item": "minecraft:player_head",
                    "nbt": f"{{SkullOwner:{{Name: \"{values['dev_name']}\", Properties: {{textures: [{{Value: \"{skull_value}\"}}]}}}}}}",
                },
                "show_toast": False,
                "announce_to_chat": False,
            },
            "parent": "global:root",
            "criteria": {"trigger": {"trigger": "minecraft:tick"}},
        }

        with open(f"{g_adv_path}/root.json", "w") as f:
            f.write(json.dumps(root, indent=5, sort_keys=True))
        with open(f"{g_adv_path}/{values['namespace']}.json", "w") as f:
            f.write(json.dumps(dev, indent=5, sort_keys=True))

        # Pack advancement
        dp_adv = {
            "display": {
                "title": f"{values['dp_name'].title()}",
                "description": f"{values['dp_desc']}",
                "icon": {"item": f"{values['dp_item']}"},
                "announce_to_chat": False,
                "show_toast": False,
            },
            "parent": f"global:{values['namespace']}",
            "criteria": {"trigger": {"trigger": "minecraft:tick"}},
        }
        with open(f"{dp_adv_path}/{values['project_name']}.json", "w") as f:
            f.write(json.dumps(dp_adv, indent=5, sort_keys=True))

        # Minecraft tick and load tags
        mc_load = {"values": [f"#{values['namespace']}:{values['project_name']}/load"]}
        mc_tick = {"values": [f"#{values['namespace']}:{values['project_name']}/tick"]}

        with open(f"{mc_tags_path}/load.json", "w") as f:
            f.write(json.dumps(mc_load, indent=5, sort_keys=True))
        with open(f"{mc_tags_path}/tick.json", "w") as f:
            f.write(json.dumps(mc_tick, indent=5, sort_keys=True))

        # Datapack-specific tick and load tags
        ns_load = {
            "values": [
                f"{values['namespace']}:{values['project_name']}/{values['load_name']}"
            ]
        }
        ns_tick = {
            "values": [
                f"{values['namespace']}:{values['project_name']}/{values['tick_name']}"
            ]
        }

        with open(f"{dp_tags_path}/load.json", "w") as f:
            f.write(json.dumps(ns_load, indent=5, sort_keys=True))
        with open(f"{dp_tags_path}/tick.json", "w") as f:
            f.write(json.dumps(ns_tick, indent=5, sort_keys=True))

        # Tick and Load functions
        with open(f"{dp_fun_path}/{values['tick_name']}.mcfunction", "w") as f:
            f.write("#> This is the main function, that will run once per tick")
        with open(f"{dp_fun_path}/{values['load_name']}.mcfunction", "w") as f:
            f.write("#> This function will run on datapack loading")

        self.message_text.set(
            self.messages["success"].format(values["dp_name"], values["dp_path"])
        )


root = tk.Tk()
ui = UI(master=root)
ui.mainloop()
