"""Write a CSV file's data into a specified Snowflake table.

Extended Summary
----------------
This script is intended to be run from the command line and presumes
that a table exists in Snowflake that you want to add CSV data to.

The `--csv_file_path` and `--table_name` flag arguments are mandatory, for 
obvious reasons.

Notes
-----
You'll want to update the source code if your enviromental variables have
different names.

If your CSV and table column header names don't match you will get an 
error, so be sure to pass the `--rename columns` flag.
See Examples, below.

If the DataFrame `read_csv.()` method encounters non-uniform data types in 
the CSV file (e.g. a column with a mix of strings and integers) Pandas will 
*guess* the data type and insert data instead  of stopping. I have ensured 
this warning is treated as an exception in order to ensure accurate data 
conversion. The solution to this error is to specify the column/s data type 
by using the `--column_datatype` flag. See Examples, below.

Examples
--------

Renaming CSV column headers to match Snowflake table headers:

>>> $ python csv_to_snowflake.py --csv product_data.csv --table PRODUCTS --rc ID PRODUCT_ID customer_name CUSTOMER_NAME

Specifying the data type of a column:

>>> $ python csv_to_snowflake.py --csv product_data.csv --table PRODUCTS --column_datatype PRODUCT_ID int

"""

import os
import warnings
import argparse
from copy import deepcopy

import snowflake.connector
import pandas as pd
from snowflake.connector.pandas_tools import write_pandas

warnings.simplefilter('error')

parser = argparse.ArgumentParser(description="Write CSV data to Snowflake table.")

parser.add_argument(
    "--csv_file_path", "--csv", help="File path of CSV file. Use double quotation marks around file path.", required=True
)
parser.add_argument(
    "--table_name", "--table", help="Name of table in Snowflake", required=True
)
parser.add_argument(
    "--rename_columns",
    "--rc",
    nargs="+",
    help='CSV column names and what they need to be renamed to in order to match SQL table column headers. E.g. "--rc column_a COLUMN A"'
)
parser.add_argument(
    "--column_datatype",
    "--dt",
    nargs="+",
    help='Specify the datatypes of CSV columns, e.g. "first_column str"'
    )

if __name__ == "__main__":

    args = parser.parse_args()
    
    # Establishes connection to Snowflake.
    conn = snowflake.connector.connect(
        user = os.environ['USER'],
        account = os.environ['DATABASE_ACCOUNT'],
        role = os.environ['DATABASE_ROLE'],
        authenticator = "externalbrowser",
        warehouse = os.environ['WAREHOUSE'],
        database = os.environ['DATABASE'],
        schema = os.environ['SCHEMA']
    )
    
    # Reads CSV data into a Pandas Data Frame.
    if args.column_datatype is not None: # User has specified column/s data type.
        column_names = deepcopy(args.column_datatype[:-1:2])
        data_types = deepcopy(args.column_datatype[1::2])
        column_data_types_dict = dict(zip(column_names, data_types))

        try:
            df = pd.read_csv(args.csv_file_path, dtype=column_data_types_dict)
        except pd.errors.DtypeWarning as e:
            error_message = str(e).split("Specify dtype option on import or set low_memory=False.") # Unnecessary information for user.
            print(f"{error_message[0]} Use the --column_datatype flag to specify data type of column contents.")
    else:
        try:
            df = pd.read_csv(args.csv_file_path)
        except pd.errors.DtypeWarning as e:
            error_message = str(e).split("Specify dtype option on import or set low_memory=False.")
            print(f"{error_message[0]} Use the --column_datatype flag to specify data type of column contents.")

    if args.rename_columns is not None: # User has specified CSV columns to be renamed.
        original_columns = deepcopy(args.rename_columns[:-1:2])
        renamed_columns = deepcopy(args.rename_columns[1::2])
        renamed_columns_dictionary = dict(zip(original_columns, renamed_columns))
        df.rename(columns=renamed_columns_dictionary, inplace=True)

    # Writes CSV data to Snowflake table.
    write_pandas(conn, df, args.table_name)
