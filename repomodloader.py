import os
import tkinter as tk
from tkinter import messagebox
import requests
import zipfile
import io
import shutil
import subprocess
import gdown

# ---------------------------------------
# KONFIGURATION
# ---------------------------------------
GOOGLE_DRIVE_FILE_ID = '1s9zbRSWxyIhegNtdwPYlPpNN5YeEVyW4'
PLUGIN_FOLDER_URL = 'https://drive.google.com/drive/folders/12wCuz3kg36qAfuyAngU_15HcLws4Yn7-?usp=sharing'
MODS_FOLDER_URL = 'https://drive.google.com/drive/folders/1xF81wGpW8WiulEAPgpAW_ZZMNBFkFMzV?usp=sharing'  # <- Ersetze mit deinem Google-Ordner-Link

DEST_FOLDER = os.path.expanduser("C:\\Program Files (x86)\\Steam\\steamapps\\common\\REPO")
CREATE_FOLDER_PATH = os.path.expanduser("C:\\Program Files (x86)\\Steam\\steamapps\\common\\REPO\\BepInEx\\plugins")
MODS_FOLDER_PATH = os.path.expanduser("C:\\Program Files (x86)\\Steam\\steamapps\\common\\REPO\\BepInEx\\plugins")
BEPINEX_FOLDER = os.path.expanduser("C:\\Program Files (x86)\\Steam\\steamapps\\common\\REPO")

# Dateien und Ordner, die gelöscht werden sollen
FILES_AND_FOLDERS_TO_DELETE = [
    ".doorstop_version",
    "doorstop_config.ini",
    "changelog.txt",
    "winhttp.dll",
    "BepInEx"
]

# ---------------------------------------
# FUNKTIONEN
# ---------------------------------------

def download_and_extract_zip():
    try:
        url = f"https://drive.google.com/uc?export=download&id={GOOGLE_DRIVE_FILE_ID}"
        response = requests.get(url)
        if response.status_code != 200:
            messagebox.showerror("Fehler", f"Download fehlgeschlagen: {response.status_code}")
            return

        os.makedirs(DEST_FOLDER, exist_ok=True)
        with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
            zip_ref.extractall(DEST_FOLDER)

        messagebox.showinfo("Erfolg", f"ZIP erfolgreich entpackt nach:\n{DEST_FOLDER}")

    except Exception as e:
        messagebox.showerror("Fehler", str(e))

def delete_mod_files():
    deleted = []
    not_found = []

    for name in FILES_AND_FOLDERS_TO_DELETE:
        path = os.path.join(BEPINEX_FOLDER, name)
        if os.path.exists(path):
            try:
                if os.path.isdir(path):
                    shutil.rmtree(path)
                else:
                    os.remove(path)
                deleted.append(name)
            except Exception as e:
                messagebox.showerror("Fehler", f"Fehler beim Löschen von {name}:\n{e}")
        else:
            not_found.append(name)

    msg = ""
    if deleted:
        msg += "Gelöscht:\n" + "\n".join(deleted) + "\n"
    if not_found:
        msg += "Nicht gefunden:\n" + "\n".join(not_found)

    messagebox.showinfo("Löschvorgang abgeschlossen", msg if msg else "Nichts zu löschen gefunden.")

def create_and_install_plugins():
    try:
        os.makedirs(CREATE_FOLDER_PATH, exist_ok=True)
        gdown.download_folder(PLUGIN_FOLDER_URL, output=CREATE_FOLDER_PATH, quiet=False, use_cookies=False)
        messagebox.showinfo("Erfolg", f"Plugins erfolgreich installiert in:\n{CREATE_FOLDER_PATH}")
    except Exception as e:
        messagebox.showerror("Fehler", f"Fehler beim Herunterladen der Plugins:\n{e}")

def create_and_install_mods():
    try:
        os.makedirs(MODS_FOLDER_PATH, exist_ok=True)
        gdown.download_folder(MODS_FOLDER_URL, output=MODS_FOLDER_PATH, quiet=False, use_cookies=False)
        messagebox.showinfo("Erfolg", f"Mods erfolgreich installiert in:\n{MODS_FOLDER_PATH}")
    except Exception as e:
        messagebox.showerror("Fehler", f"Fehler beim Herunterladen der Mods:\n{e}")

def delete_mods():
    try:
        if os.path.exists(MODS_FOLDER_PATH):
            for filename in os.listdir(MODS_FOLDER_PATH):
                file_path = os.path.join(MODS_FOLDER_PATH, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    messagebox.showerror("Fehler", f"Fehler beim Löschen von {file_path}:\n{e}")
            messagebox.showinfo("Erfolg", "Alle Mods wurden gelöscht.")
        else:
            messagebox.showinfo("Hinweis", "Plugins-Ordner nicht gefunden.")
    except Exception as e:
        messagebox.showerror("Fehler", f"Fehler beim Löschen der Mods:\n{e}")

def open_bepinex_folder():
    try:
        subprocess.Popen(f'explorer "{BEPINEX_FOLDER}"')
    except Exception as e:
        messagebox.showerror("Fehler", f"Ordner konnte nicht geöffnet werden:\n{e}")

# ---------------------------------------
# GUI
# ---------------------------------------

def create_gui():
    window = tk.Tk()
    window.title("Mod-Manager Menü")
    window.geometry("230x200")
    window.configure(bg="black")

    button_style = {
        "bg": "#333333",
        "fg": "white",
        "activebackground": "#555555",
        "activeforeground": "white",
        "padx": 10,
        "pady": 5,
        "bd": 0,
        "highlightthickness": 0
    }

    frame = tk.Frame(window, bg="black")
    frame.grid(row=0, column=0, sticky="nw", padx=10, pady=10)

    tk.Button(frame, text="install BepInEx", command=download_and_extract_zip, **button_style).grid(row=0, column=0)
    tk.Button(frame, text="delete BepInEx", command=delete_mod_files, **button_style).grid(row=0, column=1, padx=(8, 0))

    wide_button_style = button_style.copy()
    wide_button_style["width"] = 26

    tk.Button(window, text="open REPO folder", command=open_bepinex_folder, **wide_button_style).grid(row=1, column=0, columnspan=2, sticky="w", padx=10, pady=(5, 0))
    tk.Button(window, text="install basic plugins", command=create_and_install_plugins, **wide_button_style).grid(row=2, column=0, columnspan=2, sticky="w", padx=10, pady=(5, 0))
    tk.Button(window, text="install mods", command=create_and_install_mods, **wide_button_style).grid(row=3, column=0, columnspan=2, sticky="w", padx=10, pady=(5, 0))
    tk.Button(window, text="delete mods", command=delete_mods, **wide_button_style).grid(row=4, column=0, columnspan=2, sticky="w", padx=10, pady=(10, 0))

    window.mainloop()

# ---------------------------------------
# START
# ---------------------------------------

if __name__ == "__main__":
    create_gui()
