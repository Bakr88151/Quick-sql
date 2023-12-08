import sys
import csv
import sqlite3
from colorama import Fore, Style
from unidecode import unidecode

def main():
    if len(sys.argv) != 4:
        print(Fore.RED + 'Wrong usage of arguments' + Style.RESET_ALL)
        sys.exit(1)
    else:
        csv_file = sys.argv[1]
        db_path = sys.argv[2]
        table_name = sys.argv[3]
    
    convert_csv_to_sqlite(csv_file, db_path, table_name)

def convert_csv_to_sqlite(csv_file, db_path, table_name):
    try:
        # Read CSV file to get column names and data types
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            header = next(reader)
            column_definitions = ', '.join([f'"{column}" TEXT' for column in header])

        # Connect to SQLite database
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        # Create table with columns from CSV
        if 'id' not in header:
            column_definitions = '"id" INTEGER PRIMARY KEY, ' + column_definitions
        else:
            column_definitions = '"id" INTEGER PRIMARY KEY, ' + ', '.join([f'"{column}" TEXT' for column in header if column != 'id'])
        
        create_table_query = f'CREATE TABLE IF NOT EXISTS "{table_name}" ({column_definitions});'
        cursor.execute(create_table_query)

        # Read CSV data and insert into SQLite table
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                columns = ', '.join(f'"{key}"' for key in row.keys())
                values = ', '.join(['?' for _ in row.values()])
                insert_query = f'INSERT INTO "{table_name}" ({columns}) VALUES ({values});'
                cursor.execute(insert_query, [unidecode(value) for value in row.values()])

        # Commit and close connection
        connection.commit()
        connection.close()

        print(Fore.GREEN + 'CSV file successfully converted to SQLite table.' + Style.RESET_ALL)

    except FileNotFoundError:
        print(Fore.RED + f'Error: File {csv_file} not found.' + Style.RESET_ALL)
        sys.exit(1)
    except Exception as e:
        print(Fore.RED + f'An error occurred: {e}' + Style.RESET_ALL)
        sys.exit(1)

if __name__ == "__main__":
    main()
