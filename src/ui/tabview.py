import customtkinter as ctk


class TabView(ctk.CTkTabview):
    def __init__(self, master):
        super().__init__(master)

        # create tabs
        self.tab_names = ["Project", "Mask", "Material", "Process", "Output", ]
        self.tabs = []

        for name in self.tab_names:
            new_tab = self.add(name)
            new_tab.grid_rowconfigure(0, weight=1)
            new_tab.grid_columnconfigure(0, weight=1)
            self.tabs.append(new_tab)

        # insert frames to each tab
        # self.project_frame = ProjectFrame(self.tabs[0])
        # self.project_frame.grid(row=0, column=0, sticky="nwe")

        # self.mask_frame = MaskFrame(self.tabs[1])
        # self.mask_frame.grid(row=0, column=0, sticky="nsew")

        # self.process_frame = ProcessFrame(self.tabs[2])
        # self.process_frame.grid(row=0, column=0, sticky="nwe")

        # self.output_frame = OutputFrame(self.tabs[3])
        # self.output_frame.grid(row=0, column=0, sticky="nwe")