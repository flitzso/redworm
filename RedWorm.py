import os
import time
import tkinter as tk
from tkinter import scrolledtext
import webbrowser

class RedWorm(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("RedWorm")
        self.geometry("800x600")

        # Área de texto para exibir a saída
        self.text_area = scrolledtext.ScrolledText(self, wrap=tk.WORD, bg="black", fg="green", state="disabled")
        self.text_area.pack(fill=tk.BOTH, expand=True)

        # Linha de entrada para comandos
        self.input_line = tk.Entry(self)
        self.input_line.pack(fill=tk.X)
        self.input_line.bind("<Return>", lambda event: self.execute_command())

        self.current_directory = os.getcwd()
        self.prompt = f"{self.current_directory}> "

        self.display_text(self.prompt)  # Mostra o diretório atual na inicialização

    def display_text(self, text):
        self.text_area.configure(state="normal")
        self.text_area.insert(tk.END, text + "\n")
        self.text_area.configure(state="disabled")
        self.text_area.see(tk.END)

    def execute_command(self):
        command = self.input_line.get().strip()
        self.input_line.delete(0, tk.END)

        if command == "clear":
            self.text_area.configure(state="normal")
            self.text_area.delete("1.0", tk.END)
            self.text_area.configure(state="disabled")
            self.display_text(self.prompt)
        elif command.startswith("wopen "):
            url = command.split(" ", 1)[1]
            self.display_text(f"{self.prompt}{command}")
            self.display_text(f"Opening website: {url}")
            webbrowser.open(url)
        elif command.startswith("wm install "):
            package = command.split(" ", 2)[2]
            self.display_text(f"{self.prompt}{command}")
            self.install_package_simulation(package)
        elif command == "ac":
            os.chdir("..")
            self.update_prompt()
            self.display_text(f"{self.prompt}ac")
            self.display_text(f"Directory changed to: {self.current_directory}")
        elif command.startswith("dc "):
            new_directory = command.split(" ", 1)[1]
            if os.path.exists(new_directory):
                os.chdir(new_directory)
                self.update_prompt()
                self.display_text(f"{self.prompt}dc {new_directory}")
                self.display_text(f"Directory changed to: {self.current_directory}")
            else:
                self.display_text(f"{self.prompt}{command}")
                self.display_text(f"Directory {new_directory} not found.")
        elif command.startswith("warq "):
            file_name = command.split(" ", 1)[1]
            self.display_text(f"{self.prompt}{command}")
            self.open_file(file_name)
        elif command == "list":
            self.list_files_in_directory()
        elif command == "pst":
            self.list_subfolders_in_directory()
        elif len(command) == 2 and command[1] == ":" and command[0].isalpha():
            drive = command[0].upper()
            if os.path.exists(drive + ":\\"):
                os.chdir(drive + ":\\")
                self.update_prompt()
            else:
                self.display_text(f"{self.prompt}{command}")
                self.display_text(f"Drive {drive} not found.")
        else:
            self.display_text(f"{self.prompt}{command}")
            self.display_text("Command not recognized. Type 'help' for available commands.")

    def update_prompt(self):
        self.current_directory = os.getcwd()
        self.prompt = f"{self.current_directory}> "

    def list_files_in_directory(self):
        files = [f.name for f in os.scandir() if f.is_file()]
        self.display_text(f"{self.prompt}list")
        self.display_text("Files in current directory:")
        for file in files:
            self.display_text(file)

    def list_subfolders_in_directory(self):
        subfolders = [f.name for f in os.scandir() if f.is_dir()]
        self.display_text(f"{self.prompt}pst")
        self.display_text("Subfolders in current directory:")
        for folder in subfolders:
            self.display_text(folder)

    def install_package_simulation(self, package):
        self.display_text("Downloading...")
        self.update()  # Força uma atualização para mostrar a mensagem "Downloading..."
        time.sleep(2)  # Simula o processo de download
        self.display_text(f"Installing package: {package}")
        self.display_text("Installation completed.")

    def open_file(self, file_name):
        if os.path.exists(file_name):
            try:
                os.startfile(file_name)  # Abre o arquivo com o programa padrão associado
            except Exception:
                self.display_text("Error opening file.")
        else:
            self.display_text(f"File {file_name} not found.")

if __name__ == "__main__":
    app = RedWorm()
    app.mainloop()
