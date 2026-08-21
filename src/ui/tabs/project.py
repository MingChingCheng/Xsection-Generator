import customtkinter as ctk

from src.ui.fonts import MyFonts


class ProjectFrame(ctk.CTkFrame):
    def __init__(self, master, fonts:MyFonts):
        super().__init__(master, fg_color="transparent")

        # grid
        self.grid_columnconfigure((0, 2), weight=0)
        self.grid_columnconfigure((1, 3), weight=1)

        # widgets
        # Project Name
        self.project_name_label = ctk.CTkLabel(self, font=fonts.text_font, text="Project Name: ")
        self.project_name_entry = ctk.CTkEntry(self, font=fonts.text_font, placeholder_text="")
        self.project_name_label.grid(row=0, column=0, padx=5, pady=20, sticky="e")
        self.project_name_entry.grid(row=0, column=1, columnspan=3, padx=5, pady=20, sticky="we")

        # Z scaling
        self.z_scale_label = ctk.CTkLabel(self, font=fonts.text_font, text="Z scaling: ")
        self.z_scale_entry = ctk.CTkEntry(self, font=fonts.text_font, placeholder_text="e.g.: 1")
        self.z_scale_description = ctk.CTkLabel(self, font=fonts.desc_font, text="The scaling factor of Z direction, default = 1 ", text_color="dimgray")
        self.z_scale_label.grid(row=1, column=0, padx=5, sticky="e")
        self.z_scale_entry.grid(row=1, column=1, padx=5, sticky="we")
        self.z_scale_description.grid(row=2, column=0, columnspan=2, padx=5, sticky="e")

        # Resolution
        self.resolution_label = ctk.CTkLabel(self, font=fonts.text_font, text="Resolution (um): ")
        self.resolution_entry = ctk.CTkEntry(self, font=fonts.text_font, placeholder_text="e.g.: 0.001")
        self.resolution_description = ctk.CTkLabel(self, font=fonts.desc_font, text="Resolution of cross-section view, default = 0.001 ", text_color="dimgray")
        self.resolution_label.grid(row=3, column=0, padx=5, sticky="e")
        self.resolution_entry.grid(row=3, column=1, padx=5, sticky="we")
        self.resolution_description.grid(row=4, column=0, columnspan=2, padx=5, sticky="e")

        # Height
        self.height_label = ctk.CTkLabel(self, font=fonts.text_font, text="Height (um): ")
        self.height_entry = ctk.CTkEntry(self, font=fonts.text_font, placeholder_text="e.g.: 20")
        self.height_description = ctk.CTkLabel(self, font=fonts.desc_font, text="Display height above substrate, default = 20 ", text_color="dimgray")
        self.height_label.grid(row=1, column=2, padx=5, sticky="e")
        self.height_entry.grid(row=1, column=3, padx=5, sticky="we")
        self.height_description.grid(row=2, column=2, columnspan=2, padx=5, sticky="e")

        # Depth
        self.depth_label = ctk.CTkLabel(self, font=fonts.text_font, text="Depth (um): ")
        self.depth_entry = ctk.CTkEntry(self, font=fonts.text_font, placeholder_text="e.g.: 10")
        self.depth_description = ctk.CTkLabel(self, font=fonts.desc_font, text="Display depth below substrate, default = 10 ", text_color="dimgray")
        self.depth_label.grid(row=3, column=2, padx=5, sticky="e")
        self.depth_entry.grid(row=3, column=3, padx=5, sticky="we")
        self.depth_description.grid(row=4, column=2, columnspan=2, padx=5, sticky="e")

        # Below
        self.below_label = ctk.CTkLabel(self,  font=fonts.text_font, text="Below (um): ")
        self.below_entry = ctk.CTkEntry(self, font=fonts.text_font, placeholder_text="e.g.: 10")
        self.below_description = ctk.CTkLabel(self, font=fonts.desc_font, text="Display backside of substrate, default = 10 ", text_color="dimgray")
        self.below_label.grid(row=5, column=2, padx=5, sticky="e")
        self.below_entry.grid(row=5, column=3, padx=5, sticky="we")
        self.below_description.grid(row=6, column=2, columnspan=2, padx=5, sticky="e")
