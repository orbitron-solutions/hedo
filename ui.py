import math

from typing import List, Tuple
from rich.console import Console
from rich.table import Table


def build_table(
        data: List[Tuple[str, str]],
        terminal_height: int,
        terminal_width: int,
        columns: int = 3,
    ) -> list[Table]:

    # Split terminal_width into three int
    table_width = int(math.floor(terminal_width / columns))
    terminal_height = terminal_height
    first_column_width: int = 15
    second_column_width: int = table_width - first_column_width
    
    last_item_index: int = columns * terminal_height
    if len(data) > last_item_index:
        data = data[:last_item_index]
        data.append(("...", ""))

    _data = data.copy()
    data = []
    for key, value in _data:
        if len(key) > first_column_width:
            key = key[:first_column_width-3] + "..."

        value = "  " + value
        if len(value
               .replace('[red]','')
               .replace('[blue]','')
               .replace('[/blue]','')
               .replace('[/red]','')
               .replace('[green]','')
               .replace('[/green]','')
               .replace('[magenta]','')
               .replace('[/magenta]','')
            ) > second_column_width:
            value = value[:second_column_width-3] + "..."

        data.append((key, value))

    
    table_renderables = []
    for i in range(columns):
        table = Table(show_header=False, box=None, pad_edge=False)
        table.add_column(style="magenta", justify="left", width=first_column_width, no_wrap=True)
        table.add_column(style="white", justify="left", width=second_column_width)
        
        for row in data[i*terminal_height:(i+1)*terminal_height]:
            table.add_row(row[0], row[1])
        table_renderables.append(table)

    return  table_renderables

if __name__=='__main__':
    data = [
        ("a", "Mode "),
        ("b", "Do that"),
        # Add more items as needed
    ]
    console = Console()
    terminal_height = console.height
    printable_table = build_table(data, terminal_height=terminal_height, terminal_width=console.width)
    console.print(printable_table)

