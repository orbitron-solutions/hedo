from i3parser import get_sorted_binds, get_current_i3mode
from rich.console import Console
from rich.live import Live
from rich.layout import Layout
from ui import build_table

console = Console()
terminal_height = console.height
layout = Layout(name="root")


# Build initial data
data = get_sorted_binds('default')

initial_tables = build_table(data, terminal_height=terminal_height, terminal_width=console.width)
layout.split_row(
    Layout(initial_tables[0], name="0"),
    Layout(initial_tables[1], name="1"),
    Layout(initial_tables[2], name="2"),
)


with Live(layout, screen=True) as live:
    while True:
        terminal_height = console.height
        terminal_width = console.width

        # Update the data
        i3mode = get_current_i3mode()
        data = get_sorted_binds(i3mode)

        tables = build_table(data, terminal_height=terminal_height, terminal_width=terminal_width)
        layout["0"].update(tables[0])
        layout["1"].update(tables[1])
        layout["2"].update(tables[2])
        #live.update(Columns(tables, equal=True))

