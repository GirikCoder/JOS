import os
import glob
import win32com.client
import logging

class DynamicAppResolver:
    def __init__(self):
        # ProgramData Start Menu (All Users)
        self.global_start_menu = r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs"
        # User AppData Start Menu (Current User)
        self.user_start_menu = os.path.join(os.environ.get("APPDATA", ""), r"Microsoft\Windows\Start Menu\Programs")
        
        # --- UWP & System App Fallback Dictionary ---
        # Modern Windows Store apps and core system utilities often lack standard .lnk shortcuts.
        # We hardcode their URI protocols or executable names here to merge with the dynamic list.
        self.uwp_fallback = {
            "calculator": "calc.exe",
            "calc": "calc.exe",
            "settings": "ms-settings:",
            "camera": "microsoft.windows.camera:",
            "whatsapp": "whatsapp:",
            "cmd": "cmd.exe",
            "command prompt": "cmd.exe",
            "control panel": "control.exe",
            "notepad": "notepad.exe",
            "task manager": "Taskmgr.exe"
        }
        
    def build_app_map(self):
        app_dict = {}
        try:
            shell = win32com.client.Dispatch("WScript.Shell")
        except Exception as e:
            logging.error(f"Failed to dispatch WScript.Shell: {e}")
            # If the Windows Script Host fails to initialize, return the fallback apps
            # This ensures Jarvis is never left completely blind to basic commands.
            return self.uwp_fallback

        directories_to_scan = [self.global_start_menu, self.user_start_menu]
        
        for directory in directories_to_scan:
            if not os.path.exists(directory):
                continue
            # Recursively find all .lnk files
            search_pattern = os.path.join(directory, "**", "*.lnk")
            for lnk_path in glob.glob(search_pattern, recursive=True):
                try:
                    shortcut = shell.CreateShortCut(lnk_path)
                    target_path = shortcut.Targetpath
              
                    if target_path and target_path.lower().endswith('.exe'):
                        # Clean the filename for the key e.g "Google Chrome.lnk" -> "google chrome"
                        clean_name = os.path.basename(lnk_path).replace(".lnk", "").strip().lower()
                        app_dict[clean_name] = target_path
                except Exception:
                    # Windows protects certain shortcuts, silently drop them and continue
                    continue
                    
        # Merge the dynamically scraped .lnk apps with the UWP fallback dictionary
        app_dict.update(self.uwp_fallback)
        
        return app_dict