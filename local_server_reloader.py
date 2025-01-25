#code that opens http://127.0.0.1:9292/ at the first tab, so fast acces to local server when coding hmtl. 

import subprocess
import time

def find_tab_and_window_with_url():
    # AppleScript to find the window and tab with the specific URL
    applescript = '''
    tell application "Brave Browser"
        set windowIndex to 0
        repeat with w in windows
            set windowIndex to windowIndex + 1
            set tabIndex to 0
            repeat with t in tabs of w
                set tabIndex to tabIndex + 1
                if URL of t is "http://127.0.0.1:9292/" then
                    return (windowIndex as text) & "," & (tabIndex as text)
                end if
            end repeat
        end repeat
        return "not found"
    end tell
    '''

    # Run the AppleScript to find the tab and window index
    result = subprocess.run(["osascript", "-e", applescript], capture_output=True, text=True)

    if result.returncode != 0:
        print(f"AppleScript Error: {result.stderr}")
        return None
    elif result.stdout.strip() == "not found":
        print("No tab with the specified URL found.")
        return None
    else:
        # Parse the returned indices
        try:
            indices = result.stdout.strip().split(",")
            window_index = int(indices[0])
            tab_index = int(indices[1])
            return window_index, tab_index
        except (ValueError, IndexError) as e:
            print(f"Error parsing indices: {e}")
            return None

def close_tab_with_url(window_index, tab_index):
    # AppleScript to close the tab with the specified URL
    applescript = f'''
    tell application "Brave Browser"
        set t to tab {tab_index} of window {window_index}
        close t
    end tell
    '''
    result = subprocess.run(["osascript", "-e", applescript], capture_output=True, text=True)

    if result.returncode != 0:
        print(f"AppleScript Error: {result.stderr}")
    else:
        print(f"Successfully closed tab {tab_index} in window {window_index}.")

def open_new_tab_or_window():
    # AppleScript to open a new tab with the specified URL and place it at the first position
    applescript = '''
    tell application "Brave Browser"
        if (count of windows) is 0 then
            make new window
        end if
        make new tab at the beginning of tabs of front window
        set URL of the first tab of front window to "http://127.0.0.1:9292/"
    end tell
    '''
    result = subprocess.run(["osascript", "-e", applescript], capture_output=True, text=True)

    if result.returncode != 0:
        print(f"AppleScript Error: {result.stderr}")
    else:
        print("Successfully opened a new tab with the URL at the first position.")

def focus_window_with_tab(window_index):
    # AppleScript to bring the window to the front
    applescript = f'''
    tell application "Brave Browser"
        set index of window {window_index} to 1
        activate
    end tell
    '''

    # Run the AppleScript to bring the window to the front
    result = subprocess.run(["osascript", "-e", applescript], capture_output=True, text=True)

    if result.returncode != 0:
        print(f"AppleScript Error: {result.stderr}")
    else:
        print(f"Successfully focused window {window_index}.")

if __name__ == "__main__":
    result = find_tab_and_window_with_url()
    
    if result:
        window_index, tab_index = result
        print(f"Tab found in window {window_index}, tab {tab_index}.")
        
        # Close the tab with the specified URL
        close_tab_with_url(window_index, tab_index)
        
        # Open a new tab with the URL at the first position
        open_new_tab_or_window()
        
        # Focus the window and tab
        focus_window_with_tab(window_index)
    else:
        print("No tab with the specified URL found, opening a new tab...")
        # Open a new tab with the URL at the first position
        open_new_tab_or_window()
