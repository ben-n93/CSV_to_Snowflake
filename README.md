# CSV to Snowflake

Command-line script for writing CSV data to a table in the Snowflake data warehouse.

The Snowflake table must exist already and match the CSV file in regards to number of columns e.g. if the CSV file features two columns of data and the Snowflake table
only has one column then this script will not work.

## Installation

Navigate into the parent directory and install the required packages:

```
$ cd CSV_to_Snowflake
$ pip3 install -r requirements.txt
```

You'll then want to configure/update your system's enviromental variables to reflect the naming convention I've used in the source code or, alternatively, update the source code
to reflect your enviromental variable names.

```python
    conn = snowflake.connector.connect(
        user = os.environ['USER'],
        account = os.environ['DATABASE_ACCOUNT'],
        role = os.environ['DATABASE_ROLE'],
        authenticator = "externalbrowser", # Update as needed.
        warehouse = os.environ['WAREHOUSE'],
        database = os.environ['DATABASE'],
        schema = os.environ['SCHEMA']
    )
```

## How to use

Call the script from the command line, specifying the CSV file path and Snowflake table name using the mandatory `--csv` and `--table` flags. 

Be sure to wrap the file path in double quotation marks.

Windows
```
$ python csv_to_snowflake.py --csv "H:\CSV files\mock_data.csv" --table_name PRODUCT_INFO
```

Mac
```
$ python3 csv_to_snowflake.py --csv "H:\CSV files\mock_data.csv" --table_name PRODUCT_INFO
```

If your CSV file features column headers that don't match the Snowflake table's headers you can pass the `--rename_columns` (or `--rc`)
flag followed by the name of the CSV column header and then the corresponding Snowflake table header, repeated as many times as necessary. For example:

Windows
```
$ python csv_to_snowflake.py --csv "H:\CSV files\mock_data.csv" --table_name PRODUCT_INFO --rc product_info PRODUCT_INFO product_cost PRODUCT_COST
```
If one or more of the columns in your CSV file features a mix of data types (e.g. strings and integers) Pandas, which is used to read the CSV file into 
a DataFrame, will (normally) raise a warning and hazard a guess as to the data type of the column in question. I have supressed this warning, treating it 
instead as an exception. You can specify column data types by using the `--column_datatype` (or `dt`) flag following the same pattern as the 
`--rename_columns` flag:

Windows
```
$ python csv_to_snowflake.py --csv "H:\CSV files\mock_data.csv" --table_name PRODUCT_INFO --dt product_info str product_cost int
```
## Planned features

- Creating a Snowflake table from CSV file rather than simply updating an existing table with CSV data.

## License

Distributed under the MIT License. See LICENSE.txt for more information.
