import os
from typing import List, Literal, Tuple
import subprocess

def get_current_i3mode() -> str:
    current_dir=__file__.rsplit('/', 1)[0]
    return subprocess.run([f"{current_dir}/get-current-mode"], capture_output=True, text=True).stdout.strip()

def get_binds():
    # Path to your i3 configuration file
    config_file_path = os.path.expanduser("~/.config/i3/config")

    # Initialize variables
    binds = {}
    current_mode = 'default'  # Default mode if none is specified
    description = ''

    # Open and read the i3 config file
    with open(config_file_path, 'r') as config_file:
        lines = config_file.readlines()

    for line in lines:
        line = line.strip()
        # Check for mode definition
        if line.startswith('# bindsym##'):
            # Extract the mode name
            current_mode = line.split('##')[1].strip()
            if current_mode not in binds:
                binds[current_mode] = []
        # Check for description
        elif line.startswith('#desc:'):
            # Extract the description text
            description = line[len('#desc:'):].strip()
        # Check for keybinding
        elif line.startswith('bindsym'):
            # Extract the keybind
            parts = line.split(None, 2)
            if len(parts) >= 2:
                keybind = parts[1]
                # Initialize the mode if not already present
                if current_mode not in binds:
                    binds[current_mode] = []
                # Append the keybind and description to the mode's list
                binds[current_mode].append({keybind: description})
                # Reset the description after use
                description = ''
        # Ignore other lines
        else:
            continue
    return binds


def get_sorted_binds(i3mode: str ='default', sort_by: Literal['command', 'keybind'] = 'command') -> List[Tuple[str, str]]:
    binds = get_binds()
    sort_splitter = "+++"
    unsorted_data = []
    if i3mode not in binds.keys():
        raise ValueError(f"Invalid mode: {i3mode}")


    if sort_by == 'command':
        unsorted_data = [
            f"{list(keybind_dict.values())[0]}  " + sort_splitter + f"{list(keybind_dict.keys())[0].strip()}" + sort_splitter + f"{list(keybind_dict.values())[0].strip()}" for keybind_dict in binds.get(i3mode, [])
        ]

    elif sort_by == 'keybind':
        unsorted_data = [
            f"{list(keybind_dict.keys())[0]}  " + sort_splitter + f"{list(keybind_dict.keys())[0]}.strip()" + sort_splitter + f"{list(keybind_dict.values())[0]}.strip()" for keybind_dict in binds.get(i3mode, [])
        ]

    else:
        raise ValueError(f"Invalid sort_by value: {sort_by}")

    unsorted_data.sort()
    data = [(v.split(sort_splitter)[1], v.split(sort_splitter)[2]) for v in unsorted_data]
    return data
