import subprocess
import os

path_to_file = os.path.join(os.getcwd(), "bannotator")
path_to_app = os.path.join(path_to_file, "app.py")

pc_path_to_icon = os.path.join(path_to_file, "resources", "icon.ico")
mac_path_to_icon = os.path.join(path_to_file, "resources", "icon.icns")
pc_command = "pyinstaller -i " + pc_path_to_icon + " " + path_to_app
# subprocess.run(pc_command)

mac_command = (
    "pyinstaller --onefile --windowed --icon "
    + mac_path_to_icon
    + " --osx-bundle-identifier com.honglab.annotator --name annotator "
    + path_to_app
)
subprocess.run(["pyinstaller", "--onefile", "--windowed","--icon",mac_path_to_icon,"--osx-bundle-identifier","com.honglab.annotator","--name","annotator",path_to_app])
