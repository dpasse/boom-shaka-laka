from typing import Iterator
from .column import Column
import re


class Table(object):
    max_number_of_labels: int
    columns: Iterator[Column]

    def compress(self, column_values: Iterator[Iterator[str]]) -> Iterator[str]:
        current_row_index = 0
        rows = [ ]
        
        tabs = 2
        
        r_i = 0;
        while True:
            
            row = ''
            
            quit = False
            
            for column in self.columns:
                c_i = column.order
                
                val = ''
                if len(column_values[c_i]) > r_i:
                    val += column_values[c_i][r_i]
                    quit = False
                else:
                    quit = True
                    
                padding = column.column_length() - len(val)
                val += ''.join([ ' ' for _ in range(padding)])
                val += ''.join([ ' ' for _ in range(tabs)])
                row += val
                
            rows.append(re.sub(r'[ ]+$', '', row))
            r_i += 1
            
            if quit:
                break

        return rows
