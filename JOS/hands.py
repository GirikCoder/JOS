import os
import subprocess
import shutil
import logging
from pathlib import Path
import screen_brightness_control as sbc
from pycaw.pycaw import AudioUtilities
from app_resolver import DynamicAppResolver

# Setup basic logging to address the "No logging" issue in your known bugs
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

class JarvisHands:
    def __init__(self):
            self.home_dir = Path(os.path.expanduser('~'))
            
            # Check if Windows OneDrive folder backup is active
            onedrive_dir = self.home_dir / "OneDrive"
            
            # Dynamically set the safe zones depending on whether they are in OneDrive or not
            self.safe_zones = {
                "desktop": onedrive_dir / "Desktop" if (onedrive_dir / "Desktop").exists() else self.home_dir / "Desktop",
                "documents": onedrive_dir / "Documents" if (onedrive_dir / "Documents").exists() else self.home_dir / "Documents",
                "downloads": self.home_dir / "Downloads" # Downloads usually stays in the home directory
            }

            # App Dictionary: maps spoken names to Windows executable names
            resolver = DynamicAppResolver()
            self.app_dictionary = resolver.build_app_map()

            # Close overrides: some apps (UWP/modern) have different process
            # names than what launches them. This maps the OPEN exe to the
            # actual CLOSE process name for taskkill.
            self.close_overrides = {
                "calc.exe":                   "CalculatorApp.exe",
                "ms-settings:":               "SystemSettings.exe",
                "microsoft.windows.camera:":  "WindowsCamera.exe",
                "xbox:":                      "XboxApp.exe",
                "whatsapp:":                  "WhatsApp.Root.exe",
            }

    def _is_safe_path(self, target_path):
        """
        SECURITY CHECK: Ensures the target path is inside one of our safe zones.
        Prevents directory traversal attacks or accidental system file deletion.
        """
        try:
            target = Path(target_path).resolve()
            for safe_dir in self.safe_zones.values():
                # Check if the target is relative to (inside) a safe directory
                if target.is_relative_to(safe_dir):
                    return True
            return False
        except Exception:
            return False

    def _find_file_in_safe_zones(self, spoken_name):
        """
        Scans Desktop, Documents, and Downloads for a file matching the spoken name.
        """
        spoken_name = spoken_name.lower().strip()

        for zone_name, zone_path in self.safe_zones.items():
            if not zone_path.exists():
                continue

            # Iterate through all files in the directory
            for file_path in zone_path.iterdir():
                if file_path.is_file():
                    # If the spoken word is part of the filename (e.g., "budget" in "budget_2026.pdf")
                    if spoken_name in file_path.stem.lower():
                        return file_path
        return None

    def _find_item_in_safe_zones(self, spoken_name):
        """
        Like _find_file_in_safe_zones but matches BOTH files and folders.
        Used by delete_item to find any item type.
        """
        spoken_name = spoken_name.lower().strip()

        for zone_name, zone_path in self.safe_zones.items():
            if not zone_path.exists():
                continue
            for item_path in zone_path.iterdir():
                if spoken_name in item_path.stem.lower():
                    return item_path
        return None

    def _resolve_destination(self, spoken_destination):
        """
        Maps a spoken destination (like 'desktop' or 'documents') to the actual Path.
        """
        spoken_destination = spoken_destination.lower().strip()

        # Try to match the spoken word to our safe zones keys
        for key, path in self.safe_zones.items():
            if key in spoken_destination:
                return path
        return None

    def move_file(self, entities):
        """
        The main public method called by main.py.
        Expects 'entities' to be a list/tuple of strings extracted by spaCy.
        Example: ["budget report", "documents"]
        """
        if not entities or len(entities) < 2:
            logging.error("Not enough information provided to move a file. Need source and destination.")
            return False, "I did not catch both the file name and the destination."

        # Assume the first entity is the file, the second is the destination
        spoken_file = entities[0]
        spoken_dest = entities[1]

        # Step 1: Find the actual file path
        source_path = self._find_file_in_safe_zones(spoken_file)
        if not source_path:
            logging.warning(f"Could not find a file matching '{spoken_file}'.")
            return False, f"I could not find a file sounding like {spoken_file} in your safe folders."

        # Step 2: Resolve the destination folder path
        dest_folder = self._resolve_destination(spoken_dest)
        if not dest_folder:
            logging.warning(f"Could not resolve destination '{spoken_dest}'.")
            return False, f"I don't recognize {spoken_dest} as a safe destination folder."

        # Step 3: Construct the final target path (Destination Folder + Original File Name)
        final_target_path = dest_folder / source_path.name

        # Step 4: Security Check
        if not self._is_safe_path(source_path) or not self._is_safe_path(final_target_path):
            logging.error("Security violation: Attempted to move files outside safe zones.")
            return False, "For your system's safety, I am not allowed to move files outside of user directories."

        # Step 5: Execute the move with extreme error handling
        try:
            # Check for overwrites
            if final_target_path.exists():
                return False, f"A file named {source_path.name} already exists in the destination."

            # Actually move the file
            shutil.move(str(source_path), str(final_target_path))
            logging.info(f"Successfully moved {source_path.name} to {dest_folder.name}")
            return True, f"Successfully moved {source_path.name} to your {dest_folder.name} folder."

        except PermissionError:
            logging.error("PermissionError during move.")
            return False, "I do not have permission to move that file. It might be open in another program."
        except Exception as e:
            logging.error(f"Unexpected error during move: {e}")
            return False, "An unexpected error occurred while trying to move the file."

    def _resolve_app_name(self, entities):
        """
        Finds the matching exe name from the app dictionary.
        Pass 1: Exact match on full phrase (e.g., "google chrome")
        Pass 2: Exact match on each entity individually
        Pass 3: Fuzzy substring — check if any dict key appears INSIDE the spoken phrase
                 (handles spaCy extracting "open notepad" instead of "notepad")
                 Sorted longest-key-first so "google chrome" beats "chrome".
        """
        if not entities:
            return None, None

        # Pass 1: Exact match on full phrase
        full_phrase = " ".join(entities).lower().strip()
        if full_phrase in self.app_dictionary:
            return full_phrase, self.app_dictionary[full_phrase]

        # Pass 2: Exact match on each entity individually
        for entity in entities:
            spoken = entity.lower().strip()
            if spoken in self.app_dictionary:
                return spoken, self.app_dictionary[spoken]

        # Pass 3: Fuzzy substring match (longest key first to prefer "google chrome" over "chrome")
        for app_name in sorted(self.app_dictionary.keys(), key=len, reverse=True):
            if app_name in full_phrase:
                return app_name, self.app_dictionary[app_name]

        return full_phrase, None

    def open_app(self, entities):
        """
        Opens an application by looking up the spoken name in the app dictionary.
        Uses os.startfile() for URI protocols (ms-settings:, xbox:, etc.)
        and subprocess.Popen for regular .exe files.
        Returns (success_boolean, message_string).
        """
        if not entities:
            return False, "I didn't catch which app you want me to open."

        spoken_name, exe_name = self._resolve_app_name(entities)

        if not exe_name:
            logging.warning(f"App '{spoken_name}' not found in app dictionary.")
            return False, f"I don't know how to open '{spoken_name}'. It's not in my app dictionary."

        try:
            # We execute the absolute path directly as scraped by the resolver
            os.startfile(exe_name)

            logging.info(f"Opened {spoken_name} ({exe_name})")
            return True, f"{spoken_name.capitalize()} opened."

        except FileNotFoundError:
            logging.error(f"{exe_name} not found on this system.")
            return False, f"I couldn't find {spoken_name} on your system. Is it installed?"
        except Exception as e:
            logging.error(f"Error opening {exe_name}: {e}")
            return False, f"Something went wrong while trying to open {spoken_name}."

    def close_app(self, entities):
        """
        Closes an application using taskkill.
        Blocks dangerous processes (like explorer.exe which is the Windows shell).
        Returns (success_boolean, message_string).
        """
        # SAFETY: These processes must NEVER be killed via taskkill
        CLOSE_BLACKLIST = {"explorer.exe"}

        if not entities:
            return False, "I didn't catch which app you want me to close."

        spoken_name, exe_name = self._resolve_app_name(entities)

        if not exe_name:
            logging.warning(f"App '{spoken_name}' not found in app dictionary.")
            return False, f"I don't know how to close '{spoken_name}'. It's not in my app dictionary."

        # The dictionary values are now absolute paths, extract just the process name for overrides and taskkill.
        exe_basename = os.path.basename(exe_name)
        
        # Check if this exe has a different close process name (UWP apps)
        close_exe = self.close_overrides.get(exe_basename, exe_basename)

        # SAFETY CHECK: Block blacklisted processes
        if close_exe.lower() in CLOSE_BLACKLIST:
            logging.warning(f"Blocked attempt to kill {close_exe} (system-critical process).")
            return False, f"I can't close {spoken_name} — it's a system-critical process. Killing it would freeze your desktop."

        # URI protocols can't be killed by taskkill — need the override
        if close_exe.endswith(":"):
            logging.warning(f"Can't taskkill a URI protocol: {close_exe}")
            return False, f"I can't force-close {spoken_name}. Please close it manually."

        try:
            # taskkill /f = force, /im = by image name
            result = subprocess.run(
                ["taskkill", "/f", "/im", close_exe],
                capture_output=True, text=True
            )

            if result.returncode == 0:
                logging.info(f"Closed {spoken_name} ({close_exe})")
                return True, f"{spoken_name.capitalize()} closed."
            else:
                logging.warning(f"taskkill returned {result.returncode}: {result.stderr.strip()}")
                return False, f"{spoken_name} doesn't seem to be running right now."

        except Exception as e:
            logging.error(f"Error closing {close_exe}: {e}")
            return False, f"Something went wrong while trying to close {spoken_name}."

    def create_item(self, entities):
        """
        Creates a file or folder in a safe zone.
        If the spoken name contains 'folder' or 'directory', creates a folder.
        Otherwise creates a text file.
        Defaults to Desktop if no destination is spoken.
        Returns (success_boolean, message_string).
        """
        if not entities:
            return False, "I didn't catch what you want me to create."

        spoken_name = entities[0].lower().strip()

        # Determine destination: second entity or default to Desktop
        if len(entities) >= 2:
            dest_folder = self._resolve_destination(entities[1])
        else:
            dest_folder = self.safe_zones["desktop"]

        if not dest_folder:
            dest_folder = self.safe_zones["desktop"]

        # Determine if it's a folder or file
        # Check BEFORE cleaning so compound names like "test_folder" still detect correctly
        is_folder = any(word in spoken_name.split() for word in ["folder", "directory", "dir"])

        # Clean the name: remove type indicator words only when they are STANDALONE words
        # Split by spaces, filter out type words, rejoin
        # e.g., "reports folder" -> "reports", but "jarvis_test_folder" stays "jarvis_test_folder"
        type_words = {"folder", "directory", "dir", "file", "document", "doc"}
        name_parts = spoken_name.split()
        cleaned_parts = [w for w in name_parts if w not in type_words]
        clean_name = " ".join(cleaned_parts).strip()

        # If nothing left after cleaning, use the original spoken name
        if not clean_name:
            clean_name = spoken_name

        clean_name = clean_name.replace(" ", "_")

        try:
            if is_folder:
                target = dest_folder / clean_name
                if target.exists():
                    return False, f"A folder named '{clean_name}' already exists in {dest_folder.name}."
                os.makedirs(target)
                logging.info(f"Created folder: {target}")
                return True, f"Created folder '{clean_name}' on your {dest_folder.name}."
            else:
                # Add .txt extension if no extension provided
                if "." not in clean_name:
                    clean_name += ".txt"
                target = dest_folder / clean_name
                if target.exists():
                    return False, f"A file named '{clean_name}' already exists in {dest_folder.name}."
                target.touch()
                logging.info(f"Created file: {target}")
                return True, f"Created file '{clean_name}' on your {dest_folder.name}."

        except PermissionError:
            logging.error("PermissionError during create.")
            return False, "I don't have permission to create that item."
        except Exception as e:
            logging.error(f"Error creating item: {e}")
            return False, "An unexpected error occurred while creating the item."

    def delete_item(self, entities):
        """
        Deletes a file or folder from a safe zone.
        Uses shutil.rmtree() for folders, os.remove() for files.
        Returns (success_boolean, message_string).
        """
        if not entities:
            return False, "I didn't catch what you want me to delete."

        spoken_name = entities[0].lower().strip()

        # Find the item in safe zones (files AND folders)
        item_path = self._find_item_in_safe_zones(spoken_name)
        if not item_path:
            return False, f"I could not find anything matching '{spoken_name}' in your safe folders."

        # Security check
        if not self._is_safe_path(item_path):
            logging.error(f"Security violation: Attempted to delete {item_path}")
            return False, "For your safety, I can't delete items outside of user directories."

        try:
            if item_path.is_dir():
                shutil.rmtree(str(item_path))
                logging.info(f"Deleted folder: {item_path.name}")
                return True, f"Deleted folder '{item_path.name}' from {item_path.parent.name}."
            else:
                os.remove(str(item_path))
                logging.info(f"Deleted file: {item_path.name}")
                return True, f"Deleted file '{item_path.name}' from {item_path.parent.name}."

        except PermissionError:
            logging.error("PermissionError during delete.")
            return False, "I don't have permission to delete that. It might be open in another program."
        except Exception as e:
            logging.error(f"Error deleting item: {e}")
            return False, "An unexpected error occurred while deleting the item."

    def open_item(self, entities):
        """
        Opens a specific file or folder natively using Safe Zones logic.
        Returns (success_boolean, message_string).
        """
        if not entities:
            return False, "I didn't catch the name of the file or folder to open."

        # Extract the requested item name from the entities list
        # Strip common words like 'file' or 'folder' that might be left in entities
        spoken_name = " ".join([str(e) for e in entities]).lower().strip()
        type_words = {"folder", "directory", "dir", "file", "document", "doc"}
        name_parts = spoken_name.split()
        cleaned_parts = [w for w in name_parts if w not in type_words]
        item_name = " ".join(cleaned_parts).strip()
        
        if not item_name:
            item_name = spoken_name

        # Call our existing _find_item_in_safe_zones(item_name) helper method.
        # It handles both files and folders.
        found_path = self._find_item_in_safe_zones(item_name)
        if not found_path:
            return False, f"I could not find a file or folder matching '{item_name}' in your safe zones."

        try:
            # If the item is found, use os.startfile(found_path)
            os.startfile(str(found_path))
            logging.info(f"Opened item natively: {found_path}")
            return True, f"Opened {found_path.name}."
        except Exception as e:
            logging.error(f"Error opening item {found_path}: {e}")
            return False, "An unexpected error occurred while trying to open the item."

    def system_control(self, entities):
        """
        Controls system hardware (volume and brightness) using pycaw and screen-brightness-control.
        Returns (success_boolean, message_string).
        """
        if not entities:
            return False, "I didn't catch the system control action."

        # Parse target from entities
        is_volume = any(w in entities for w in ["volume", "sound", "mute", "unmute"])
        is_brightness = any(w in entities for w in ["brightness", "screen", "dim"])

        # Extract level (if a number is present)
        level = None
        for e in entities:
            if isinstance(e, int) or (isinstance(e, str) and str(e).isdigit()):
                level = int(e)
                break

        try:
            if is_volume:
                # Initialize pycaw
                devices = AudioUtilities.GetSpeakers()
                volume = devices.EndpointVolume

                if "mute" in entities:
                    volume.SetMute(1, None)
                    return True, "System volume muted."
                elif "unmute" in entities:
                    volume.SetMute(0, None)
                    return True, "System volume unmuted."
                elif level is not None:
                    # Enforce bounds 0-100 and convert to scalar (0.0 to 1.0) for pycaw
                    vol_float = max(0.0, min(100.0, float(level))) / 100.0
                    volume.SetMasterVolumeLevelScalar(vol_float, None)
                    return True, f"System volume set to {level}%."
                elif "up" in entities or "increase" in entities:
                    current = volume.GetMasterVolumeLevelScalar()
                    new_vol = min(1.0, current + 0.2)
                    volume.SetMasterVolumeLevelScalar(new_vol, None)
                    return True, "Volume increased."
                elif "down" in entities or "decrease" in entities or "reduce" in entities or "lower" in entities:
                    current = volume.GetMasterVolumeLevelScalar()
                    new_vol = max(0.0, current - 0.2)
                    volume.SetMasterVolumeLevelScalar(new_vol, None)
                    return True, "Volume decreased."
                else:
                    return False, "I didn't understand how you want to change the volume."

            elif is_brightness:
                # sbc.get_brightness() returns a list of values for multiple monitors. Take the primary (0).
                current_brightness = sbc.get_brightness(display=0)[0]
                
                if level is not None:
                    sbc.set_brightness(level)
                    return True, f"Screen brightness set to {level}%."
                elif "dim" in entities or "decrease" in entities or "down" in entities or "reduce" in entities or "lower" in entities:
                    new_b = max(0, current_brightness - 20)
                    sbc.set_brightness(new_b)
                    return True, f"Screen dimmed to {new_b}%."
                elif "increase" in entities or "up" in entities:
                    new_b = min(100, current_brightness + 20)
                    sbc.set_brightness(new_b)
                    return True, f"Screen brightness increased to {new_b}%."
                else:
                    return False, "I didn't understand how you want to change the brightness."

            else:
                return False, "I didn't understand which system setting to control."

        except Exception as e:
            logging.error(f"Error during SYSTEM_CONTROL hardware execution: {e}")
            return False, "Hardware system control failed."