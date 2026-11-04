from typing import List, Any


# task 2 function: takes a list of namedtuples and converts yes/no/blank strings into 1 and 0 integers
def convert_yesno_to_binary(table: List[tuple]) -> List[tuple]:
    # create an empty list to hold our converted namedtuple rows
    converted_table: List[tuple] = []
    # type() grabs the WASHRow namedtuple class from the first row so we can rebuild rows at the end
    row_class = type(table[0])

    # dictionary mapping blank, 'Do not know', and 'No' strings to 0, and 'Yes' string to 1
    conversion_dictionary = {
        '': 0,
        'Do not know': 0,
        'No': 0,
        'Yes': 1
    }

    # loop through each namedtuple row in our table
    for row in table:
        # turn the locked namedtuple row into a regular editable list of values
        row_values: List[Any] = list(row)

        # loop through each cell position (index) and cell value in the row list
        for index, value in enumerate(row_values):
            # if the cell string is in conversion_dictionary, replace it with its 0 or 1 integer
            if value in conversion_dictionary:
                row_values[index] = conversion_dictionary[value]

        # unpack (*) the updated row_values list back into a WASHRow namedtuple and append to converted_table
        converted_row = row_class(*row_values)
        converted_table.append(converted_row)

    return converted_table


# task 3 function: maps any remaining unique text strings in each column to unique integers (1, 2, 3...)
def convert_values_to_numeric(table: List[tuple]) -> List[tuple]:
    # grab the WASHRow namedtuple class using type() and the tuple of column names using ._fields
    row_class = type(table[0])
    columns = table[0]._fields

    # step 1: create a master dictionary that will map each column name to its own value-mapping dictionary
    master_dictionary = {}

    # step 2: loop through each column name string to find all unique text answers in that column
    for column in columns:
        # collect all unique string values in this column using a set (skips values that are already 0 or 1 integers)
        unique_strings = sorted(list(set(
            getattr(row, column) for row in table
            if type(getattr(row, column)) == str
        )))

        # create the inner mapping dictionary for this column where each unique string gets a unique integer (1, 2, 3...)
        mapping_dictionary = {}
        for index, text_value in enumerate(unique_strings):
            mapping_dictionary[text_value] = index + 1

        # store this column's mapping dictionary inside master_dictionary under the column name key
        master_dictionary[column] = mapping_dictionary

    # step 3 & 4: loop through every row and replace any remaining text string with its mapped integer
    converted_table: List[tuple] = []

    for row in table:
        # convert the locked namedtuple row into a regular editable list
        row_values: List[Any] = list(row)

        # check each cell in the row by its column index and value
        for index, value in enumerate(row_values):
            column = columns[index]
            # if this cell's string value is in this column's mapping dictionary, replace it with its integer
            if value in master_dictionary[column]:
                row_values[index] = master_dictionary[column][value]

        # unpack (*) the all-numeric row_values list back into a WASHRow namedtuple and append to converted_table
        converted_row = row_class(*row_values)
        converted_table.append(converted_row)

    return converted_table
