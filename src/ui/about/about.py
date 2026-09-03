import customtkinter as ctk

from src.ui.fonts import MyFonts
from src.version import __version__


class AboutWindow(ctk.CTkToplevel):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # window
        self.geometry("300x150")
        fonts = MyFonts()

        self.grid_columnconfigure(0, weight=1)

        # labels
        self.title_label = ctk.CTkLabel(self, text=f"Xsection Generator {__version__}", font=fonts.tab_font)

        info = "Copyright (c) 2026 Ming-Ching Cheng \n" \
               "This software is released under the MIT License. "

        self.author_label = ctk.CTkLabel(
            self, text=info, font=fonts.desc_font, text_color="gray"
        )

        self.title_label.grid(row=0, column=0, pady=(20, 10))
        self.author_label.grid(row=2, column=0, padx=10)

        # button
        self.close_button = ctk.CTkButton(self, text="Close", command=self.destroy)
        self.close_button.grid(row=4, column=0, pady=(20, 10))

class LicenseWindow(ctk.CTkToplevel):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # window
        self.geometry("550x300")
        fonts = MyFonts()

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # labels
        self.title_label = ctk.CTkLabel(self, text="License", font=fonts.tab_font)
        self.title_label.grid(row=0, column=0, pady=(20, 10))

        # read the license file and display it in a text box
        with open("LICENSE", "r") as f:
            license_text = f.read()
        self.license_textbox = ctk.CTkTextbox(self, font=fonts.lice_font)
        self.license_textbox.insert("0.0", license_text)
        self.license_textbox.configure(state="disabled")  # make it read-only
        self.license_textbox.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

class ThirdPartyLicenseWindow(ctk.CTkToplevel):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # window
        self.geometry("550x300")
        fonts = MyFonts()

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # labels
        self.title_label = ctk.CTkLabel(self, text="Third-Party Licenses", font=fonts.tab_font)
        self.title_label.grid(row=0, column=0, pady=(20, 10))

        # read the license file and display it in a text box
        with open("THIRD_PARTY_LICENSES.txt", "r") as f:
            license_text = f.read()
        self.license_textbox = ctk.CTkTextbox(self, font=fonts.lice_font)
        self.license_textbox.insert("0.0", license_text)
        self.license_textbox.configure(state="disabled")  # make it read-only
        self.license_textbox.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
    