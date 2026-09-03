from CTkMenuBar import (
    CTkMenuBar,
    CustomDropdownMenu,
)


class MenuBar:
    def __init__(self, master, **commands):

        self.menu = CTkMenuBar(master)
        self.menu.grid(row=0, column=0, sticky="ew")

        # create File menu
        self.file = self.menu.add_cascade("File")
        file_dropdown = CustomDropdownMenu(widget=self.file)
        file_dropdown.add_option(option="Open project ...", command=commands["open_command"])
        file_dropdown.add_option(option="Save project as ...", command=commands["save_as_command"])

        # create About menu
        self.about = self.menu.add_cascade("About")
        about_dropdown = CustomDropdownMenu(widget=self.about)
        about_dropdown.add_option(option="About Xsection Generator", command=commands["about_command"])
        about_dropdown.add_option(option="License", command=self.about_license)

    def open_project(self):
        print("Open project")

    def about_app(self):
        print("About Xsection Generator")

    def about_license(self):
        print("License")