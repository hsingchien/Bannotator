import os
import subprocess

# List of .ui files to convert and merge
path_to_ui = os.path.join(os.getcwd(), "bannotator","ui")
ui_files = [f for f in os.listdir(path_to_ui) if f.endswith(".ui")]


# Convert .ui files to .py files
for ui_file in ui_files:
    py_file_path = os.path.join(path_to_ui,'ui_'+ ui_file.replace("ui","py"))
    ui_file_path = os.path.join(path_to_ui,ui_file)
    command = " ".join(['pyside6-uic', ui_file_path,'-o',py_file_path])
    subprocess.run(command)
