from pathlib import Path
from collections import namedtuple
from typing import List, Type
import csv
import sys

# Task 1: load the survey csv and keep only columns starting with 'G' as a list of NamedTuples
csv_path = Path(r"C:\Users\wolki\Documents\School\PENN\Fall 2026\Fundamentals of Data\Week 08 - Object-Oriented Data Analysis\Week08AssignmentData\IOM_Rohingya_WASH_Survey.csv")

wash_table: List[tuple] = []

# open csv with utf-8-sig to strip any hidden characters and use next(reader) to grab the header row list
with open(csv_path, 'r', encoding='utf-8-sig') as csv_file:
    reader = csv.reader(csv_file)
    headers: List[str] = next(reader)

    # list comprehension finding the integer column positions (indices) of all headers that start with 'G'
    g_indices: List[int] = [
        index
        for index, header in enumerate(headers)
        if header.startswith('G')
    ]

    # list comprehension grabbing the actual column name strings for those 'G' indices
    g_headers: List[str] = [
        headers[index]
        for index in g_indices
    ]

    # dynamically create the WASHRow namedtuple class using the 'G' column names as its fields
    WASHRow: Type[tuple] = namedtuple(
        typename='WASHRow',
        field_names=g_headers
    )

    # loop through each row in the csv, pull out only the 'G' column values, and unpack (*) into WASHRow
    for row in reader:
        g_values: List[str] = [
            row[index]
            for index in g_indices
        ]

        wash_row = WASHRow(*g_values)
        wash_table.append(wash_row)

print(wash_table[0])


# Task 2: import convert_yesno_to_binary from our datalib file and convert yes/no/blank strings to 1 and 0
sys.path.insert(
    1,
    r"C:\Users\wolki\PycharmProjects\envs-5726-fundamentals-of-data\Week 8"
)

from Week08Assignment_Datalib import convert_yesno_to_binary, convert_values_to_numeric

converted_wash_table = convert_yesno_to_binary(wash_table)
print(converted_wash_table[0])


# Task 3: run convert_values_to_numeric on converted_wash_table so all remaining text strings become unique integers
final_converted_table = convert_values_to_numeric(converted_wash_table)
print(final_converted_table[0])