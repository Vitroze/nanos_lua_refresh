# Nanos Lua Refresh

Automatically reload a **nanos world** package every time you save a Lua file in VSCode.

## Purpose

When developing a package for a [nanos world](https://nanos.world) server, you have to type `package reload <package_name>` in the server console after every change. This quickly becomes repetitive. This script does it for you each time you save a `.lua` file in VSCode.

1. You save a `.lua` file in VSCode.
2. The script finds the package it belongs to (by walking up the folders until it finds a `Package.toml`).
3. It sends `package reload <package_name>` to the console of the already running server, **without taking focus** and without you having to switch windows.

## Requirements

- **Windows**
- **Nanos World Server** already running (the script does not start it)
- **Python 3.9+**
- **VSCode** with the **[Run On Save](https://marketplace.visualstudio.com/items?itemName=emeraldwalk.RunOnSave)** extension (`emeraldwalk.RunOnSave`)

> ⚠️ The Run On Save extension is **mandatory**: it is what triggers the script on every save. Without it, nothing happens.

## Installation

1. Clone the repository (or just copy `lua_refresh.py` and `requirements.txt` anywhere you like):

   ```bash
   git clone <repository-url>
   ```

2. Install the dependencies with the **same Python** that VSCode will call:

   ```bash
   python -m pip install -r requirements.txt
   ```

3. Install the **Run On Save** extension:

   ```bash
   code --install-extension emeraldwalk.RunOnSave
   ```

4. Add this to your VSCode `settings.json` (user or workspace):

   ```json
   "emeraldwalk.runonsave": {
     "commands": [
       {
         "match": "\\.lua$",
         "cmd": "python \"PATH\\TO\\lua_refresh.py\" \"${file}\"",
         "isAsync": true
       }
     ]
   }
   ```

   Replace `PATH\\TO` with the real location of the script. Backslashes must be doubled and quotes escaped (`\"`) in JSON, which is required if the path contains spaces. If you use a virtual environment, replace `python` with the full path to its interpreter (e.g. `\"C:\\path\\.venv\\Scripts\\python.exe\"`).

## Usage

1. Start your nanos server as usual.
2. Open a `.lua` file that belongs to one of the server's packages.
3. Save it (`Ctrl+S`).

The package is reloaded. You can follow what happens in VSCode's **Output** panel (`View > Output`) by selecting **Run On Save** in the dropdown.

The script can also be run manually:

```bash
python lua_refresh.py "...\Packages\my_package\Server\Index.lua"
```