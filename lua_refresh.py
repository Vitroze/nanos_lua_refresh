import os
import sys
import asyncio
import psutil
import win32console

PROCESS_NAME = "NanosWorldServer.exe"
CMD_RELOAD = "package reload"

class BColors:
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

def print_success(message):
    print(f"{BColors.OKGREEN}[Nanos Lua Refresh] {message}{BColors.ENDC}")

def print_info(message):
    print(f"{BColors.OKBLUE}[Nanos Lua Refresh] {message}{BColors.ENDC}")

def print_error(message):
    print(f"{BColors.FAIL}[Nanos Lua Refresh] {message}{BColors.ENDC}")

if len(sys.argv) < 2:
    print_error("Usage: python lua_refresh.py <file>")
    sys.exit(1)

file_path = sys.argv[1]
if not os.path.isfile(file_path):
    print_error(f"File not found: {file_path}")
    sys.exit(1)

async def get_package_name(folder_path):
    cooldown = 0
    while True:
        if cooldown > 5: # Anti-crash
            print_error("Package.toml not found in any parent directory.")
            return None

        package_toml_path = os.path.join(folder_path, "Package.toml")
        if os.path.isfile(package_toml_path):
            return os.path.basename(folder_path)

        parent_folder = os.path.dirname(folder_path)
        if parent_folder == folder_path:
            print_error("Reached the root directory without finding Package.toml.")
            return None

        folder_path = parent_folder
        cooldown += 0.5

async def get_process_nanos_world_server():
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == PROCESS_NAME:
            return proc
    return None

async def send_command_to_process(process, command):
    pid = process.pid
    if not pid:
        print_error("Process ID not found.")
        return

    try:
        win32console.FreeConsole()
    except Exception:
        pass

    win32console.AttachConsole(pid)
    try:
        con_input = win32console.GetStdHandle(win32console.STD_INPUT_HANDLE) # Get the console input handle
        records = []
        for ch in command + "\r":
            for down in (True, False):
                r = win32console.PyINPUT_RECORDType(win32console.KEY_EVENT) # Create a key event record
                r.KeyDown = down # Set the key down/up state
                r.RepeatCount = 1 # Set the repeat count
                r.Char = ch # Set the character

                if ch == '\r': # If the character is Enter, set the virtual key code to VK_RETURN
                    r.VirtualKeyCode = 0x0D # Set the virtual key code for Enter

                records.append(r)

        con_input.WriteConsoleInput(records) # Write the key events to the console input buffer
    finally:
        win32console.FreeConsole()
        try:
            win32console.AttachConsole(-1)  # Reattach to the current console
        except Exception:
            pass

        print_success(f"Command sent to process {pid}: {command}")


async def main():
    print_info(f"Searching for package folder starting from: {file_path}")
    package_folder = await get_package_name(os.path.dirname(file_path))
    if not package_folder:
        print_error("Package folder not found. Exiting.")
        return

    process = await get_process_nanos_world_server()
    if not process:
        print_error("Nanos World Server process not found. Exiting.")
        return

    print_success(f"Found Nanos World Server process with PID: {process.pid}")
    await send_command_to_process(process, f"{CMD_RELOAD} {package_folder}")

asyncio.run(main())