from rich.console import Console
from rich.table import Table
from rich.columns import Columns
import textwrap  # Added import

# Sample data with lengthy texts
data = [
    ("Name", "Alice"),
    ("Bio", "Alice is an engineer with over ten years of experience in developing complex software systems for various industries including finance, healthcare, and logistics."),
    ("Bio", "Alice is an engineer with over ten years of experience in developing complex software systems for various industries including finance, healthcare, and logistics."),
    ("Bio", "Alice is an engineer with over ten years of experience in developing complex software systems for various industries including finance, healthcare, and logistics."),
    ("Bio", "Alice is an engineer with over ten years of experience in developing complex software systems for various industries including finance, healthcare, and logistics."),
    ("Hobbies", "Reading, hiking, painting, traveling around the world, and experimenting with new technologies."),
    ("Favorite Quote", "The only way to do great work is to love what you do. - Steve Jobs"),
    ("Goals", "To contribute to open source projects and make a positive impact on the tech community."),
    ("Achievements", "Developed a scalable application that handles millions of transactions per day."),
    ("Additional Info", "She is passionate about mentoring young engineers and participates in community tech events."),
    ("Contact", "Email: alice@example.com\nLinkedIn: linkedin.com/in/alice-engineer"),
    ("Projects", "Project Alpha: A machine learning platform.\nProject Beta: An IoT device network."),
    ("Publications", "Authored multiple papers on software architecture and system design."),
    # Add more items as needed
]

console = Console()
terminal_height = console.size.height

# Column settings
first_column_width = 10
second_column_width = 50

# Function to calculate the height of a row considering wrapped text
def calculate_row_height(first_cell_text, second_cell_text, second_col_width):
    # First column doesn't wrap
    lines_first_cell = first_cell_text.count('\n') + 1

    # Second column wraps text, handle manual newlines
    lines_in_second_cell = 0
    for line in second_cell_text.split('\n'):
        wrapped_lines = textwrap.wrap(line, width=second_col_width)
        if not wrapped_lines:
            # Empty line
            lines_in_second_cell += 1
        else:
            lines_in_second_cell += len(wrapped_lines)

    # Row height is the maximum of the two cells
    row_height = max(lines_first_cell, lines_in_second_cell)
    return row_height

# Split data into chunks based on terminal height
tables = []
current_chunk = []
current_height = 0  # Current accumulated height

for key, value in data:
    row_height = calculate_row_height(key, value, second_column_width)

    # Add 0 for the line spacing between rows (since pad_edge=False, no extra lines)
    total_row_height = row_height

    if current_height + total_row_height > terminal_height - 2:  # Reserve space for table padding
        # Start a new table
        tables.append(current_chunk)
        current_chunk = [(key, value)]
        current_height = total_row_height
    else:
        current_chunk.append((key, value))
        current_height += total_row_height

# Don't forget to add the last chunk
if current_chunk:
    tables.append(current_chunk)

# Build tables for each chunk
table_renderables = []

for chunk in tables:
    table = Table(show_header=False, box=None, pad_edge=False)
    table.add_column(style="green", justify="left", width=first_column_width, no_wrap=True)
    table.add_column(style="white", justify="left", width=second_column_width, overflow="fold", no_wrap=False)
    
    for key, value in chunk:
        table.add_row(key, value)
    table_renderables.append(table)

# Render the tables side by side
console.print(Columns(table_renderables, expand=True))

