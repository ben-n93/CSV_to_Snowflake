"""Write a CSV file's data into a specified Snowflake table."""

import argparse

import snowflake.connector
import pandas as pd
from snowflake.connector.pandas_tools import write_pandas

parser = argparse.ArgumentParser(description='Write CSV data to Snowflake table.')
parser.add_argument('-csv_file_path','-c', #required=True)
parser.add_argument('-table_name','-t', description='Name of SQL table in Snowflake', #required=True)
parser.add_argument('-list','-l', type = list, description='Name of SQL table in Snowflake', #required=True)
args = parser.parse_args()
