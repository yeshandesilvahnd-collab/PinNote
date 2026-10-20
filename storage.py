import os
import sys
import json
import logging

APP_DIR_NAME = ".pinnote"
DATA_FILE_NAME = "data.json"
STARTUP_VBS_NAME = "PinNote.vbs"
STARTUP_LNK_NAME = "PinNote.lnk"
MAC_LAUNCH_AGENT_LABEL = "com.pinnote.app"
MAC_PLIST_NAME = f"{MAC_LAUNCH_AGENT_LABEL}.plist"

DEFAULT_SETTINGS = {
    "html": "",
    "text": "",
    "theme": "dark",
    "always_on_top": True,
    "geometry": "380x480",
    "font_size": 13,
    "start_on_boot": True,
    "idle_transparency_enabled": True,
    "idle_timeout_seconds": 60,
    "idle_opacity": 50,
}

def get_app_data_dir() -> str:
    user_home = os.path.expanduser("~")
    data_dir = os.path.join(user_home, APP_DIR_NAME)
    os.makedirs(data_dir, exist_ok=True)
    return data_dir

def get_data_file_path() -> str:
    return os.path.join(get_app_data_dir(), DATA_FILE_NAME)

def get_startup_dir() -> str:
    return os.path.expandvars(r"%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup")

def get_startup_vbs_path() -> str:
    return os.path.join(get_startup_dir(), STARTUP_VBS_NAME)

def get_startup_lnk_path() -> str:
    return os.path.join(get_startup_dir(), STARTUP_LNK_NAME)

def get_mac_launch_agent_path() -> str:
    user_home = os.path.expanduser("~")
    launch_agents_dir = os.path.join(user_home, "Library", "LaunchAgents")
    return os.path.join(launch_agents_dir, MAC_PLIST_NAME)

def load_data() -> dict:
    path = get_data_file_path()
    data = dict(DEFAULT_SETTINGS)
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                saved = json.load(f)
                if isinstance(saved, dict):
                    data.update(saved)
        except Exception as e:
            logging.error(f"Error loading data from {path}: {e}")
    return data

def save_data(data: dict) -> bool:
    path = get_data_file_path()
    temp_path = path + ".tmp"
    try:
        with open(temp_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        if os.path.exists(path):
            os.replace(temp_path, path)
        else:
            os.rename(temp_path, path)
        return True
    except Exception as e:
        logging.error(f"Error saving data to {path}: {e}")
        return False

def _create_windows_shortcut(target_lnk: str, target_exe: str, working_dir: str = "", description: str = "", icon_location: str = ""):
    """Creates a standard Windows .lnk shortcut via WScript.Shell."""
    vbs_helper = os.path.join(os.environ.get("TEMP", "."), "pinnote_shortcut_helper.vbs")
    escaped_lnk = target_lnk.replace('"', '""')
    escaped_exe = target_exe.replace('"', '""')
    escaped_dir = working_dir.replace('"', '""')
    escaped_desc = description.replace('"', '""')
    escaped_icon = icon_location.replace('"', '""')

    icon_line = f'Shortcut.IconLocation = "{escaped_icon}"' if icon_location else ''
    vbs_content = f'''Set WshShell = CreateObject("WScript.Shell")
Set Shortcut = WshShell.CreateShortcut("{escaped_lnk}")
Shortcut.TargetPath = "{escaped_exe}"
Shortcut.WorkingDirectory = "{escaped_dir}"
Shortcut.Description = "{escaped_desc}"
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

def is_start_on_boot_enabled() -> bool:
    if sys.platform == "darwin":
        return os.path.exists(get_mac_launch_agent_path())
    elif sys.platform == "win32":
        # Check if either standard shortcut (.lnk) or script (.vbs) exists in Windows Startup
        return os.path.exists(get_startup_lnk_path()) or os.path.exists(get_startup_vbs_path())
    return False

def set_start_on_boot(enabled: bool, main_script_path: str = None) -> bool:
    if sys.platform == "darwin":
        plist_path = get_mac_launch_agent_path()
        if enabled:
            try:
                os.makedirs(os.path.dirname(plist_path), exist_ok=True)
                if getattr(sys, "frozen", False):
                    exe_path = sys.executable
                    prog_args = f"        <string>{exe_path}</string>"
                else:
                    if not main_script_path:
                        current_dir = os.path.dirname(os.path.abspath(__file__))
                        main_script_path = os.path.join(current_dir, "pin_note.py")
                    python_exe = sys.executable
                    prog_args = f"        <string>{python_exe}</string>\n        <string>{main_script_path}</string>"

                plist_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>{MAC_LAUNCH_AGENT_LABEL}</string>
    <key>ProgramArguments</key>
    <array>
{prog_args}
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>ProcessType</key>
    <string>Interactive</string>
</dict>
</plist>
"""
                with open(plist_path, "w", encoding="utf-8") as f:
                    f.write(plist_content)
                return True
            except Exception as e:
                logging.error(f"Failed to enable macOS startup: {e}")
                return False
        else:
            try:
                if os.path.exists(plist_path):
                    os.remove(plist_path)
                return True
            except Exception as e:
                logging.error(f"Failed to disable macOS startup: {e}")
                return False

    elif sys.platform == "win32":
        vbs_path = get_startup_vbs_path()
        lnk_path = get_startup_lnk_path()

        if enabled:
            try:
                os.makedirs(get_startup_dir(), exist_ok=True)

                if getattr(sys, "frozen", False):
                    # PyInstaller compiled executable:
                    # Clean up any legacy .vbs so .lnk and .vbs NEVER duplicate
                    if os.path.exists(vbs_path):
                        try:
                            os.remove(vbs_path)
                        except Exception:
                            pass

                    exe_path = sys.executable
                    icon_path = os.path.join(os.path.dirname(exe_path), "assets", "icon.ico")
                    if not os.path.exists(icon_path):
                        icon_path = exe_path

                    _create_windows_shortcut(
                        target_lnk=lnk_path,
                        target_exe=exe_path,
                        working_dir=os.path.dirname(exe_path),
                        description="PinNote - Minimalist Sticky Note",
                        icon_location=icon_path
                    )
                else:
                    # Running from source:
                    # Clean up any stray .lnk in startup to avoid duplicates
                    if os.path.exists(lnk_path):
                        try:
                            os.remove(lnk_path)
                        except Exception:
                            pass

                    if not main_script_path:
                        current_dir = os.path.dirname(os.path.abspath(__file__))
                        main_script_path = os.path.join(current_dir, "pin_note.py")

                    python_exe = sys.executable
                    pythonw_exe = python_exe.replace("python.exe", "pythonw.exe")
                    if not os.path.exists(pythonw_exe):
                        pythonw_exe = python_exe

                    vbs_content = f'''Set WshShell = CreateObject("WScript.Shell")
WshShell.Run """{pythonw_exe}"" ""{main_script_path}""", 0, False
'''
                    with open(vbs_path, "w", encoding="utf-8") as f:
                        f.write(vbs_content)

                return True
            except Exception as e:
                logging.error(f"Failed to enable Windows startup: {e}")
                return False
        else:
            try:
                # Disable startup: Clean up BOTH .vbs and .lnk
                if os.path.exists(vbs_path):
                    os.remove(vbs_path)
                if os.path.exists(lnk_path):
                    os.remove(lnk_path)
                return True
            except Exception as e:
                logging.error(f"Failed to disable Windows startup: {e}")
                return False

    return False
