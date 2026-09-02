from tkinter import messagebox

from src.model.project import ProjectData


class DataChecker:
    def __init__(self):
        self.all_correct = True

    def check_project_data(self, project_data: ProjectData):
        """Check the project data for errors"""

        # Check if the project name is empty
        if not project_data.project_name:
            self.all_correct = False
            messagebox.showerror(title="Error", message="Project name cannot be empty.")