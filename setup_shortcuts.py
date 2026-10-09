import os
import sys

def get_paths():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    app_script = os.path.join(current_dir, "pin_note.py")
    python_exe = sys.executable
    pythonw_exe = python_exe.replace("python.exe", "pythonw.exe")
    if not os.path.exists(pythonw_exe):
        pythonw_exe = python_exe
    startup_dir = os.path.expandvars(r"%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup")
    desktop_dir = os.path.expanduser(r"~\Desktop")
    return {
        "current_dir": current_dir,
        "app_script": app_script,
        "pythonw_exe": pythonw_exe,
        "startup_dir": startup_dir,
        "desktop_dir": desktop_dir
    }

def create_vbs_launcher(target_path=None):
    paths = get_paths()
    if target_path is None:
        target_path = os.path.join(paths["current_dir"], "PinNote.vbs")
    
    script_content = f'''Set WshShell = CreateObject("WScript.Shell")
WshShell.Run """{paths["pythonw_exe"]}"" ""{paths["app_script"]}""", 0, False
'''
    with open(target_path, "w", encoding="utf-8") as f:
        f.write(script_content)
    return target_path

def create_windows_shortcut(target_lnk, target_exe, args="", working_dir="", description="", icon_location=""):
    vbs_helper = os.path.join(os.environ.get("TEMP", "."), "create_shortcut.vbs")
    # In VBScript, double quotes inside strings are doubled: ""
    escaped_target_lnk = target_lnk.replace('"', '""')
    escaped_target_exe = target_exe.replace('"', '""')
    escaped_args = args.replace('"', '""')
    escaped_working_dir = working_dir.replace('"', '""')
    escaped_description = description.replace('"', '""')
    escaped_icon = icon_location.replace('"', '""')
    
    icon_line = f'Shortcut.IconLocation = "{escaped_icon}"' if icon_location else ''

    vbs_content = f'''Set WshShell = CreateObject("WScript.Shell")
Set Shortcut = WshShell.CreateShortcut("{escaped_target_lnk}")
Shortcut.TargetPath = "{escaped_target_exe}"
Shortcut.Arguments = "{escaped_args}"
Shortcut.WorkingDirectory = "{escaped_working_dir}"
Shortcut.Description = "{escaped_description}"
{icon_line}
Shortcut.Save
'''
    with open(vbs_helper, "w", encoding="utf-8") as f:
        f.write(vbs_content)
    
    os.system(f'cscript //nologo "{vbs_helper}"')
    if os.path.exists(vbs_helper):
        try:
            os.remove(vbs_helper)
        except Exception:
            pass

def setup_all_shortcuts():
    paths = get_paths()
    # 1. Create launcher in app folder
    create_vbs_launcher()
    
    # 2. Create desktop shortcut
    desktop_lnk = os.path.join(paths["desktop_dir"], "PinNote.lnk")
    icon_file = os.path.join(paths["current_dir"], "assets", "icon.ico")
    if not os.path.exists(icon_file):
        icon_file = "notepad.exe,0"

    create_windows_shortcut(
        target_lnk=desktop_lnk,
        target_exe=paths["pythonw_exe"],
        args=f'"{paths["app_script"]}"',
        working_dir=paths["current_dir"],
        description="PinNote - Minimalist Sticky Note with Always-on-Top",
        icon_location=icon_file
    )
    print("Desktop shortcut updated with custom icon at:", desktop_lnk)

if __name__ == "__main__":
    setup_all_shortcuts()
