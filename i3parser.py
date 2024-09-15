import os


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

